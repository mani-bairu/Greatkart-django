from .models import Cart,Cart_items
from .views import _cart_id

def total_cart_items(request):
    total_items=0
    if request.user.is_authenticated:
        cart_items=Cart_items.objects.filter(user=request.user)
    else:
        cart_items=Cart_items.objects.filter(cart__cart_id=_cart_id(request))
    for cart_item in cart_items:
        total_items+=cart_item.quantity
    
    return dict(items=total_items)
