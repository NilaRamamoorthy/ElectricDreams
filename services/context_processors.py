from .models import Category  # adjust to your actual model name

def service_categories(request):
    return {
        "categories": Category.objects.prefetch_related("subcategories").all()
    }

from .models import Category

def default_category(request):
    return {
        "default_category": Category.objects.filter(is_default=True).first()
    }

