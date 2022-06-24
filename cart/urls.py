from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
    path('decrement-from-cart/<int:product_id>/<int:cart_item_id>/', views.decrement_cart_item, name='decrement-from-cart'),
    path('remove-cart-item/<int:product_id>/<int:cart_item_id>/', views.remove_cart_item,  name='remove-cart-item'),
    
    # checkout
    path('checkout/', views.checkout, name='checkout'),
]

