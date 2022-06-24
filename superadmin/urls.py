from django.urls import path
from . import views

urlpatterns = [
    path('', views.superadmin_login, name='superadmin-login' ),
    path('dashboard/', views.superadmin_dashboard, name='superadmin-dashboard' ),
    path('superadmin-logout', views.superadmin_logout, name='superadmin-logout' ),
    
    # Product
    path('products/', views.products, name="products"),
    path('products/add-product/', views.add_product, name="add-product"),
    path('products/edit-product/<str:pk>/', views.edit_product, name='edit-product'),
    path('products/delete-product/<str:pk>/', views.delete_product, name='delete-product'),
    
    # Category
    path('category/', views.category, name="category"),
    path('category/add-category/', views.add_category, name="add-category"),
    path('category/edit-category/<str:pk>/', views.edit_category, name='edit-category'),
    path('category/delete-category/<str:pk>/', views.delete_category, name='delete-category'),
    
    
    # Customers
    path('customers/', views.customer, name="customers"),
    path('customers/customer_block/<pk>', views.customer_block_unblock, name="customer-block"),
    
    # Orders
    path('orders/', views.product_orders, name='orders'),
    path('orders/delete-order/<str:track_no>/', views.delete_order, name='delete-order'),
    path('orders/ordered-products/<str:track_no>/', views.view_shipping_product, name='ordered-products'),
    path('orders/edit-shipping-product/<str:pk>/', views.edit_shipping_product, name='edit-shipping-product'),
    
    
    
]