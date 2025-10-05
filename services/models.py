from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)
    is_default = models.BooleanField(default=False, help_text="Mark this as the default category")

    def __str__(self):
        return self.name



class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name="subcategories", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="subcategory_images/", blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.category.name} → {self.title}"



class Service(models.Model):
    category = models.ForeignKey("SubCategory",related_name="services",on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="service_images/", blank=True, null=True)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # New fields
    rating = models.DecimalField(
        max_digits=3, decimal_places=2,
        default=0.0,
        help_text="Average rating (1.0 to 5.0)"
    )
    num_reviews = models.PositiveIntegerField(
        default=0,
        help_text="Number of reviews submitted"
    )

    def __str__(self):
        return f"{self.category.title} → {self.name}"  # use .title instead of .name for SubCategory


# Service Area
class ServiceArea(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]  # Always sorted alphabetically

    def __str__(self):
        return self.name


# Service Details
class ProcessStep(models.Model):
    step_number = models.PositiveIntegerField()
    title = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        ordering = ["step_number"]

    def __str__(self):
        return f"Step {self.step_number}: {self.title}"


class TechnicianHighlight(models.Model):
    icon = models.CharField(max_length=50, help_text="Bootstrap icon class, e.g. 'bi-shield-check'")
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class TechnicianSection(models.Model):
    image = models.ImageField(upload_to="technicians/")

    def __str__(self):
        return f"Technician Section {self.id}"



class Review(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5)
    comment = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='reviews/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_profile_image_url(self):
        """Return uploaded profile image or default static image."""
        if self.profile_image:
            return self.profile_image.url
        return '/static/images/default-profile.png'  # 👈 change path if needed

    def __str__(self):
        return f"{self.user.username} - {self.service.name}"
