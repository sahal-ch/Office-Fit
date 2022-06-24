import random
from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from users.models import Address
from .models import *
from orders.models import *

# Create your views here.
def cart(request, total=0, quantity=0, cart_items=None) :
    
    try :
        tax, grand_total = 0, 0
        if request.user.is_authenticated :
            cart_items = CartItem.objects.filter(user=request.user, is_active=True).order_by('-created_on')
        else :
            # for guest user
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True).order_by('-created_on')
            
        for cart_item in cart_items :
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
            
            
        tax = (5 * total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist :
        pass
    
    context = {
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        'tax' : tax,
        'grand_total' : grand_total,
    }
    
    return render(request, 'cart/cart.html', context)


"""
- private function
- assigning session id to the variable cart
- if there is no session, we will create one
"""
def _cart_id(request) :
    cart = request.session.session_key
    if not cart :
        cart = request.session.create()
    return cart

# add to cart
def add_to_cart(request, product_id) :
    product = Product.objects.get(id=product_id)
    
    if request.user.is_authenticated :
        """ if the user is authenticated """
        try :
            cart_item = CartItem.objects.get(product=product, user=request.user)
            
            if cart_item.product.stock < cart_item.quantity + 1 :
                messages.error(request, f'There is not enough Stock to add {cart_item.product.name} to the cart !!!')
                return redirect('cart')
            else :
                cart_item.quantity += 1
                cart_item.save()
        except CartItem.DoesNotExist :
            cart_item = CartItem.objects.create(product=product, user=request.user)
            cart_item.save()
    else :
        """ for guest users """
        try :
            # get the cart using the cart id present in the session 
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist :
            cart = Cart.objects.create(cart_id = _cart_id(request))
            cart.save()
            
        try :
            cart_item = CartItem.objects.get(product=product, cart=cart)
            if cart_item.product.stock < cart_item.quantity + 1 :
                messages.error(request, f'There is not enough stock to add {cart_item.product.name} to the cart !!!')
                return redirect('cart')
            else :
                cart_item.quantity += 1
                cart_item.save()
                messages.success(request, 'Product Added to Cart!')
        except CartItem.DoesNotExist :
            cart_item = CartItem.objects.create(product=product, cart=cart)
            cart_item.save()
            messages.success(request, 'Product Added to Cart!')
    return redirect('cart')

def decrement_cart_item(request, product_id, cart_item_id) :
    product = get_object_or_404(Product, id=product_id)
    
    try :
        if request.user.is_authenticated :
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
            if cart_item.quantity > 1 :
                cart_item.quantity -= 1
                cart_item.save()
            else :
                cart_item.delete()
        else :
            cart = Cart.objects.get(cart_id=_cart_id(request))
            
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
            if cart_item.quantity > 1 :
                cart_item.quantity -= 1
                cart_item.save()
            else :
                cart_item.delete()
    except :
        pass
    return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id) :
    product = get_object_or_404(Product, id=product_id)
    
    try :
        if request.user.is_authenticated :
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
            cart_item.delete()
        else :
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
            cart_item.delete()
    except :
        pass
    return redirect('cart')

# checkout
@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None) :
    try :
        tax, grand_total = 0, 0
        if request.user.is_authenticated :
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else :
            # for guest user
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            
        for cart_item in cart_items :
            if cart_item.product.stock < cart_item.quantity :
                messages.error(request, f'There is no enough stock of {cart_item.product.name} !!!')
                return redirect('cart')
            else :
                total += (cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity
            
        tax = (5 * total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist :
        pass
    
    addresses = Address.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        'tax' : tax,
        'grand_total' : grand_total,
        'addresses' : addresses,
    }
    
    return render(request, 'cart/checkout.html', context)


