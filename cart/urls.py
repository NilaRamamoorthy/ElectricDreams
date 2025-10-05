# cart/urls.py
from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("add/<int:service_id>/", views.add_to_cart, name="add_to_cart"),
    path("update/<int:item_id>/", views.update_quantity, name="update_quantity"),
    path("offcanvas/", views.cart_offcanvas, name="cart_offcanvas"),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    # Checkout
    path("checkout/", views.checkout, name="checkout"),
    path("checkout_success/", views.checkout_success, name="checkout_success"),
]
