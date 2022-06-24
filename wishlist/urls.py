from django.urls import path
from . import views

urlpatterns = [
    path('', views.wishlist, name='wishlist'),
    path('add-to-wishlist/<int:product_id>/', views.add_to_wishlist, name='add-to-wishlist'),
    path('remove-from-wishlist/<int:product_id>/<int:wishlist_item_id>/', views.remove_from_wishlist,  name='remove-from-wishlist'),
]