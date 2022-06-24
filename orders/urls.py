from django.urls import path
from . import views

urlpatterns = [
    path('place-order/',views.place_order,name="place-order"),
    path('payments/', views.payments, name='payments'),
    path('payment-status/', views.payment_status, name='payment-status'),
    path('cash-on-delivery/', views.cash_on_delivery, name='cash-on-delivery'),
]