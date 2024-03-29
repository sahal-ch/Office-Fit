from .models import *
from .views import _cart_id


"""
- You have to add this context processor in settings.py
- Go to settings.py -> TEMPLATES -> OPTIONS
- add 'app_name.file_name.function_name'
- In this case => 'cart.context_processors.counter'
"""
def counter(request) :
    cart_count = 0
    if 'admin' in request.path :
        return ()
    else :
        try :
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            if request.user.is_authenticated :
                cart_items = CartItem.objects.all().filter(user=request.user)
            else :
                cart_items = CartItem.objects.all().filter(cart=cart[:1])
            
            cart_count = 0
            for cart_item in cart_items :
                cart_count += 1
        except Cart.DoesNotExist :
            cart_count = 0
            
    return dict(cart_count=cart_count)