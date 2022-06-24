from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginPage, name='login'),
    path('register/',views.registerPage,name='register'),
    path('register-otp/',views.register_otp,name='register-otp'),
    path('resend-otp/', views.resend_otp, name='resend-otp'),
    path('logout/',views.logoutUser,name='logout'),
    
    # forgot password
    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('reset-password-validate/<uidb64>/<token>/', views.reset_password_validate, name='reset-password-validate'),
    path('reset-password/', views.reset_password, name='reset-password'),
    
    # Products
    path('shop/', views.shop, name='shop'),
    
    # Product by Category
    path('shop/category/<slug:category_slug>/', views.shop, name='products-by-category'),
    
    # Single Product
    path('shop/category/<slug:category_slug>/<slug:product_slug>/', views.product_details, name='product-details'),
    
    # Search
    path('shop/search/', views.search, name='search'),
    
    # Filter Product
    path('shop/filter/', views.filter_product, name='filter-product'),
    
    # User Profile
    path('my-account/', views.my_account, name='my-account'),
    path('my-account/my-address/', views.my_address, name='my-address'),
    path('my-account/my-address/delete-address/<str:id>/', views.delete_address, name='delete-address'),
    path('my-account/my-orders/', views.my_orders, name='my-orders'),
    path('my-account/edit-profile/', views.edit_profile, name='edit-profile'),
    path('my-account/change-password/', views.change_password, name='change-password'),
    path('my-account/my-orders/order-details/<int:order_id>/', views.order_details, name='order-details'),
    path('my-account/my-orders/cancel-order/<str:pk>/', views.cancel_order, name='cancel-order'),
    path('my-account/verify-email/', views.verify_email, name='verify-email'),
    path('my-account/verify-email/send-email-link/', views.send_email_link, name='send-email-link'),
    path('my-account/verify-email/activate/<uidb64>/<token>/', views.activate, name='activate'),
    
    # Review Product
    path('submit-review/<int:product_id>/', views.submit_review, name='submit-review'),
    
]