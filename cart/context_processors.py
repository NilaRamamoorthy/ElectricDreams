from .models import CartItem

def cart_context(request):
    user = request.user if request.user.is_authenticated else None
    items = CartItem.objects.filter(user=user) if user else []
    total = sum(i.total_price() for i in items)
    count = len(items)
    return {'cart_items': items, 'cart_total': total, 'cart_count': count}
