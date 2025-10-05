from django.shortcuts import render, redirect
from .models import AboutSection, ServiceSection, CommitmentSection, FAQ, WhyChooseImage,Brand
from services.models import Category, Review, SubCategory
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import EmergencyElectricianPage
from .forms import CallbackRequestForm
from django.core.mail import EmailMultiAlternatives
from .forms import ContactForm
from .models import SiteSetting, ContactThankYou

# Home
def home(request):
    faqs = FAQ.objects.all()
    subcategories = SubCategory.objects.all()[:8]
    brands = Brand.objects.all()
    images = WhyChooseImage.objects.all()[:4]
    categories = Category.objects.prefetch_related("subcategories").all()
    reviews = Review.objects.select_related("service", "user").order_by("-created_at")[:4]
    return render(request, "core/home.html", {
        "faqs": faqs,
        "subcategories": subcategories,
        "brands": brands,
        "why_choose_images": images,
        "categories": categories,
        "reviews": reviews,
    })



# About
def about(request):
    about_data = AboutSection.objects.first()
    service_data = ServiceSection.objects.first()
    commitment_data = CommitmentSection.objects.first()
    return render(request, "core/about.html", {
        "about_data": about_data,
        "service_data": service_data,
        "commitment_data": commitment_data,
    })

# Emergency Electrician

def emergency_electrician(request):
    page_content = EmergencyElectricianPage.objects.first()  # Load page content
    form = CallbackRequestForm()

    if request.method == "POST":
        form = CallbackRequestForm(request.POST)
        if form.is_valid():
            callback = form.save()

            # Send email to admin
            send_mail(
                subject="New Callback Request",
                message=f"""
                Name: {callback.name}
                Mobile: {callback.mobile}
                Email: {callback.email}
                Services: {callback.services}
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],  # Define in settings.py
            )

            messages.success(request, "We have received your request. We’ll get back to you in 30 minutes or less.")
            return redirect("emergency_electrician")

    return render(request, "core/emergency_electrician.html", {
        "page_content": page_content,
        "form": form
    })


# Contact
def contact_view(request):
    form = ContactForm()

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()  # Save message to DB

            # Get site settings
            site = SiteSetting.objects.first()

            # ---------------- EMAIL TO ADMIN ----------------
            subject_admin = f"New Contact Message from {contact.first_name}"
            html_content_admin = f"""
                <h2 style="color:#E25C26;">New Contact Message</h2>
                <p><b>Name:</b> {contact.first_name} {contact.last_name or ''}</p>
                <p><b>Email:</b> {contact.email}</p>
                <p><b>Phone:</b> {contact.phone}</p>
                <p><b>Address:</b> {contact.address}</p>
                <p><b>Message:</b><br>{contact.message}</p>
            """
            msg_admin = EmailMultiAlternatives(
                subject_admin,
                contact.message,
                settings.DEFAULT_FROM_EMAIL,
                [site.email],
            )
            msg_admin.attach_alternative(html_content_admin, "text/html")
            msg_admin.send()

            # ---------------- AUTO REPLY TO USER ----------------
            thank_you = ContactThankYou.objects.first()
            thank_you_message = thank_you.message if thank_you else "Thanks for reaching out! We will get back to you soon."

            subject_user = f"Thanks for contacting {site.site_name}"
            html_content_user = f"""
                <div style="font-family: Arial, sans-serif; color:#333;">
                    <div style="background:#E25C26; padding:10px; text-align:center;">
                        {"<img src='" + site.logo.url + "' alt='" + site.site_name + "' style='height:50px;'>" if site and site.logo else f"<h2 style='color:white'>{site.site_name}</h2>"}
                    </div>
                    <div style="padding:20px;">
                        <h2 style="color:#E25C26;">Hi {contact.first_name},</h2>
                        <p>{thank_you_message}</p>
                        <blockquote style="border-left:4px solid #E25C26; padding-left:10px; margin:10px 0;">
                            {contact.message}
                        </blockquote>
                        <p style="margin-top:20px;">
                            Regards,<br>
                            <b>{site.site_name}</b><br>
                            📞 {site.phone}<br>
                            ✉️ {site.email}
                        </p>
                    </div>
                    <div style="background:#E25C26; color:white; text-align:center; padding:10px;">
                        © {site.site_name} - All Rights Reserved
                    </div>
                </div>
            """
            msg_user = EmailMultiAlternatives(
                subject_user,
                thank_you_message,
                settings.DEFAULT_FROM_EMAIL,
                [contact.email],
            )
            msg_user.attach_alternative(html_content_user, "text/html")
            msg_user.send()

            # ---------------- SUCCESS MESSAGE ----------------
            messages.success(request, thank_you_message)

            return redirect("contact")  # Redirect so refresh won’t resubmit

    return render(request, "core/contact.html", {"form": form})

