from django.contrib import admin
from .models import (
    Category, SubCategory, Service, ServiceArea,
    ProcessStep, TechnicianHighlight, TechnicianSection
)

admin.site.register(ServiceArea)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Service)
admin.site.register(ProcessStep)
admin.site.register(TechnicianHighlight)
admin.site.register(TechnicianSection)
