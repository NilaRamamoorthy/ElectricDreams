from django.shortcuts import render, get_object_or_404
from .models import ServiceArea, Category, SubCategory, Service, ProcessStep, TechnicianSection, TechnicianHighlight, Review
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def areas_we_serve(request):
    areas = ServiceArea.objects.all()
    return render(request, "services/areas_we_serve.html", {"areas": areas})


def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    subcategories = category.subcategories.all()  # requires related_name="subcategories"
    default_category = Category.objects.filter(is_default=True).first()
    return render(request, "services/service_category.html", {
        "category": category,
        "subcategories": subcategories,
        "default_category": default_category
    })


def service_list(request, pk):
    subcategory = get_object_or_404(SubCategory, pk=pk)
    services = subcategory.services.all()  # because of related_name="services"
    return render(request, "services/service_list.html", {
        "subcategory": subcategory,
        "services": services,
    })




def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    process_steps = ProcessStep.objects.all()
    technician_section = TechnicianSection.objects.first()  # single image
    technician_highlights = TechnicianHighlight.objects.all()

    return render(request, "services/service_detail.html", {
        "service": service,
        "process_steps": process_steps,
        "technician_section": technician_section,
        "technician_highlights": technician_highlights,
    })



@login_required
def add_review(request, service_id):
    service = get_object_or_404(Service, id=service_id)

    if request.method == 'POST':
        rating = int(request.POST.get('rating'))
        comment = request.POST.get('comment')
        profile_image = request.FILES.get('profile_image')  # 👈 fetch uploaded image

        Review.objects.create(
            service=service,
            user=request.user,
            rating=rating,
            comment=comment,
            profile_image=profile_image,  # optional
        )

        messages.success(request, 'Your review has been added successfully!')
        return redirect('services:service_detail', pk=service.id)

    return redirect('services:service_detail', pk=service.id)


# Search Bar
def search_suggestions(request):
    query = request.GET.get("q", "").strip()
    results = []

    if query:
        # SubCategory → title field
        subcategories = SubCategory.objects.filter(title__icontains=query)[:5]

        # Service → name field
        services = Service.objects.filter(name__icontains=query)[:5]

        # Format SubCategory results
        for sub in subcategories:
            results.append({
                "type": "subcategory",
                "id": sub.id,
                "name": sub.title,
                "url": f"/services/subcategory/{sub.id}/"
            })

        # Format Service results
        for service in services:
            results.append({
                "type": "service",
                "id": service.id,
                "name": service.name,
                "url": f"/services/service/{service.id}/"
            })

    return JsonResponse({"results": results})
