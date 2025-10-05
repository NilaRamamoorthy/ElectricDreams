from django.urls import path
from . import views

app_name = "services"

urlpatterns = [
    path("areas/", views.areas_we_serve, name="areas_we_serve"),
    path("category/<int:pk>/", views.category_detail, name="category_detail"),
    path("subcategory/<int:pk>/", views.service_list, name="service_list"), 
    path("service/<int:pk>/", views.service_detail, name="service_detail"),
   
    path('service/<int:service_id>/add-review/', views.add_review, name='add_review'),
    path("search/", views.search_suggestions, name="search_suggestions"),




]
