from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from services.models import Service
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from .models import CartItem, Order 
from decimal import Decimal



def cart_offcanvas(request):
    user = request.user if request.user.is_authenticated else None
    items = CartItem.objects.filter(user=user)
    total = sum(i.total_price() for i in items)
    return render(request, 'cart/offcanvas.html', {'items': items, 'total': total})

@require_POST
@login_required
def add_to_cart(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    user = request.user

    item, created = CartItem.objects.get_or_create(user=user, service=service)

    if not created:
        item.quantity += 1
    item.save()

    count = CartItem.objects.filter(user=user).count()

    return JsonResponse({
        'success': True,
        'message': f'{service.name} added to cart!',
        'count': count
    })

def update_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    action = request.GET.get('action')

    if action == 'increase':
        item.quantity += 1
    elif action == 'decrease' and item.quantity > 1:
        item.quantity -= 1
    item.save()

    return JsonResponse({
        'quantity': item.quantity,
        'total': item.total_price(),
        'grand_total': sum(i.total_price() for i in CartItem.objects.filter(user=item.user))
    })



@require_POST
@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()

    # Recalculate the remaining total for the user's cart
    grand_total = sum(i.total_price() for i in CartItem.objects.filter(user=request.user))

    return JsonResponse({
        'success': True,
        'message': 'Item removed from cart.',
        'grand_total': grand_total,
        'count': CartItem.objects.filter(user=request.user).count()
    })



# Checkout
@login_required
def checkout(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect('/')

    item_total = sum(i.total_price() for i in cart_items)
    visitation_fees = Decimal('60.00') if item_total < Decimal('200.00') else Decimal('0.00')
    taxes = (item_total * Decimal('0.05')).quantize(Decimal('0.01'))
    total_amount = item_total + visitation_fees + taxes

    if request.method == "POST":
        # form fields
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        service_date_str = request.POST.get("service_date")

        try:
            service_date = datetime.strptime(service_date_str, "%Y-%m-%d").date()
        except:
            messages.error(request, "Please select a valid date.")
            return redirect("cart:checkout")

        if service_date < timezone.now().date():
            messages.error(request, "Service date cannot be in the past.")
            return redirect("cart:checkout")

        order = Order.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address,
            total_amount=total_amount,
            service_date=service_date,
        )

        cart_items.delete()
        return redirect("cart:checkout_success")

    context = {
        "cart_items": cart_items,
        "item_total": item_total,
        "visitation_fees": visitation_fees,
        "taxes": taxes,
        "total_amount": total_amount,
        "today": timezone.now().date().isoformat(),
    }
    return render(request, "cart/checkout.html", context)



@login_required
def checkout_success(request):
    order = Order.objects.filter(user=request.user).last()
    return render(request, "cart/checkout_success.html", {"order": order})

