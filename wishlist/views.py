from django.shortcuts import render, redirect, get_object_or_404
from product.models import Product
from wishlist.models import Wishlist, WishlistItem

# Create your views here.
def wishlist(request, wishlist_items=None) :
    
    try :
        if request.user.is_authenticated :
            wishlist_items = WishlistItem.objects.filter(user=request.user)
        else :
            # for guest user
            wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
            wishlist_items = WishlistItem.objects.filter(wishlist=wishlist, is_active=True)
    except :
        pass
                
    context = {
        'wishlist_items' : wishlist_items,
    }
    return render(request, 'wishlist/wishlist.html', context)

# getting wishlist id as session id
def _wishlist_id(request) :
    wishlist = request.session.session_key
    
    if not wishlist :
        wishlist = request.session.create()
    
    return wishlist

# add to wishlist
def add_to_wishlist(request, product_id) :
    current_user = request.user
    product = Product.objects.get(id=product_id)
    
    if current_user.is_authenticated :
        """ if the user is authenticated """

        try :
            wishlist_item = WishlistItem.objects.get(product=product, user=current_user)
            wishlist_item.save()
        except WishlistItem.DoesNotExist :
            wishlist_item = WishlistItem.objects.create(product=product, user=current_user)
            wishlist_item.save()
    else :
        """ for guest users """
        try :
            # get the wishlist usign the wishlist_id present in the session
            wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
            wishlist.save()
        except Wishlist.DoesNotExist :
            wishlist = Wishlist.objects.create(wishlist_id=_wishlist_id(request))
            wishlist.save()

        
        try :
            wishlist_item = WishlistItem.objects.get(product=product, wishlist=wishlist)
            wishlist_item.save()
        except WishlistItem.DoesNotExist :
            wishlist_item = WishlistItem.objects.create(product=product, wishlist=wishlist)
            wishlist_item.save()
    return redirect('wishlist')


def remove_from_wishlist(request, product_id, wishlist_item_id) :
    product = get_object_or_404(Product, id=product_id)
    
    try :
        if request.user.is_authenticated :
            wishlist_item = WishlistItem.objects.get(product=product, user=request.user, id=wishlist_item_id)
        else :
            wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
            wishlist_item = WishlistItem.objects.get(product=product, wishlist=wishlist, id=wishlist_item_id)
    except :
        pass
    wishlist_item.delete()
    return redirect('wishlist')
    