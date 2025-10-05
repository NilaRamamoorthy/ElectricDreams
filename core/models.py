from django.db import models
import os

# Context_Processor
class SiteSetting(models.Model):
    site_name = models.CharField(max_length=255, default="Electric Dreams")
    logo = models.ImageField(upload_to="logos/", null=True, blank=True)
    phone = models.CharField(max_length=20, default="+911234567890")
    email = models.EmailField(default="support@electricdreams.com")
    address = models.CharField(max_length=255, default="Chennai, India")

    def __str__(self):
        return self.site_name

    @property
    def has_logo(self):
        return self.logo and os.path.isfile(self.logo.path)
    


# Home
class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question

# class Service(models.Model):
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     image = models.ImageField(upload_to="services/")

#     def __str__(self):
#         return self.title



class Brand(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to="brands/")

    def __str__(self):
        return self.name


class WhyChooseImage(models.Model):
    image = models.ImageField(upload_to="why_choose_us/")


#About
class AboutSection(models.Model):
    title = models.CharField(max_length=255, default="About Electric Dreams")
    subtitle = models.CharField(max_length=500, blank=True, null=True)
    description = models.TextField()
    image = models.ImageField(upload_to="about/", blank=True, null=True)
    certifications = models.TextField(
        blank=True,
        help_text="Enter one certification/license per line"
    )

    def __str__(self):
        return self.title



class ServiceSection(models.Model):
    title = models.CharField(max_length=255, default="Our Services")
    description = models.TextField()
    image = models.ImageField(upload_to="services/", blank=True, null=True)

    def __str__(self):
        return self.title


class CommitmentSection(models.Model):
    title = models.CharField(max_length=255, default="Our Commitment to You")
    description = models.TextField()
    image = models.ImageField(upload_to="commitment/", blank=True, null=True)

    def __str__(self):
        return self.title


# Emergency Electrician

class EmergencyElectricianPage(models.Model):
    banner_image = models.ImageField(upload_to="emergency/")
    small_image = models.ImageField(upload_to="emergency/")
    workmanship_image = models.ImageField(upload_to="emergency/", null=True, blank=True) 

    def __str__(self):
        return "Emergency Electrician Page Content"


class CallbackRequest(models.Model):
    name = models.CharField(max_length=200)
    mobile = models.CharField(max_length=20)
    email = models.EmailField()
    services = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Callback from {self.name} - {self.mobile}"



# Contact Page

class ContactMessage(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField()
    address = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"
    

class ContactThankYou(models.Model):
    message = models.TextField(default="Thanks for reaching out. We will get back to you soon!")

    def __str__(self):
        return "Contact Thank You Message"

