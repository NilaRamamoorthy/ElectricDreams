from django.contrib import admin
from .models import SiteSetting, AboutSection, ServiceSection, CommitmentSection, FAQ, Service, Brand, EmergencyElectricianPage, CallbackRequest, WhyChooseImage 

# Context_Processor
admin.site.register(SiteSetting)

# Home
admin.site.register(FAQ)   
admin.site.register(Service)   
admin.site.register(Brand)   
admin.site.register(WhyChooseImage)   




# About
admin.site.register(AboutSection)
admin.site.register(ServiceSection)
admin.site.register(CommitmentSection)

# Emergency electrician
admin.site.register(EmergencyElectricianPage)
admin.site.register(CallbackRequest)


#Contact
from .models import ContactMessage, SiteSetting, ContactThankYou

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "phone", "created_at")
    search_fields = ("first_name", "last_name", "email", "phone")


admin.site.register(ContactThankYou)