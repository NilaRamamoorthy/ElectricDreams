from .models import SiteSetting, FAQ

def site_settings(request):
    settings = SiteSetting.objects.first()
    return {
        "site_settings": settings
    }


def faqs_processor(request):
    return {
        "faqs": FAQ.objects.all()
    }
