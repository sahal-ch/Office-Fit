from atexit import register
from django.contrib import admin
from .models import Payment, Order, OrderProduct


class OrderProductInline(admin.TabularInline) :
    model = OrderProduct
    readonly_fields = ['payment', 'user', 'product', 'status', 'quantity', 'product_price', 'ordered']
    extra = 0

class OrderAdmin(admin.ModelAdmin) :
    list_display = ['tracking_no', 'full_name', 'total_price', 'is_ordered']
    list_filter = ['is_ordered']
    search_fields = ['tracking_no', 'full_name']
    list_per_page = 20
    inlines = [OrderProductInline]
    
class OrderProductAdmin(admin.ModelAdmin) :
    list_display = ['user', 'product', 'payment', 'status', 'product_price', 'quantity', 'ordered']
    list_filter = ['status', 'ordered']
    search_fields = ['user', 'product', 'status']
    list_per_page = 20
    

# Register your models here.
admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
