from django.db import models
from product.models import *
from users.models import Account

# Create your models here.
class Cart(models.Model) :
    cart_id = models.CharField(max_length=250, blank=True, null=True)
    date_added = models.DateField(auto_now_add=True)
    
    def __str__(self) :
        return self.cart_id
    

class CartItem(models.Model) :
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    ordered = models.BooleanField(default=False, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    
    def sub_total(self) :
        tax_price = self.product.price + self.product.price * (5/100)
        return tax_price * self.quantity
    
    def __str__(self) :
        return self.product.name
    

