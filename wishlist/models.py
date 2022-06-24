import imp
from django.db import models
from product.models import Product
from users.models import Account

# Create your models here.
class Wishlist(models.Model) :
    wishlist_id = models.CharField(max_length=250, null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)
    
    def __str__(self) :
        return self.wishlist_id
    
    
class WishlistItem(models.Model) :
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self) :
        return self.product.name
    