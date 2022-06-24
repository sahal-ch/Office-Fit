from pyexpat import model
from django.db import models
from users.models import Account
from product.models import Product

# Create your models here.
class Payment(models.Model) :
    user                =  models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    name                =  models.CharField(max_length=100, null=True, blank=True)
    email               =  models.CharField(max_length=100, null=True, blank=True)
    
    # amount => total amount paid
    amount              =  models.CharField(max_length=100)
    order_id            =  models.CharField(max_length=100)
    razorpay_payment_id =  models.CharField(max_length=100, null=True, blank=True)
    payment_method      =  models.CharField(max_length=100)
    paid                =  models.BooleanField(default=False)
    created_at          =  models.DateTimeField(auto_now_add=True)
    
    def __str__(self) :
        return self.order_id


class Order(models.Model):
    user             = models.ForeignKey(Account, on_delete=models.CASCADE)
    full_name        = models.CharField(max_length=100)
    address          = models.TextField(max_length=100)
    city             = models.CharField(max_length=100)
    pin_code         = models.CharField(max_length=10)
    state            = models.CharField(max_length=50)
    country          = models.CharField(max_length=50)
    mobile           = models.CharField(max_length=15)
    landmark         = models.CharField(max_length=100)
    total_price      = models.FloatField()
    tax              = models.FloatField()
    
    payment_method   = models.CharField(max_length=100)
    is_paid          = models.BooleanField(default=False)
    payment          = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    
    ip              = models.CharField(blank=True, null=True, max_length=20)
    message         = models.TextField(null=True, blank=True)
    is_ordered      = models.BooleanField(default=False)
    tracking_no     = models.CharField(max_length=150)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    
    
    def __str__(self) :
        return self.full_name
    
class OrderProduct(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    ORDER_STATUS = (
        ('ordered', 'ordered'),
        ('shipped','shipped'),
        ('out_for_delivery', 'out_for_delivery'),
        ('delivered','delivered'),
        ('cancelled','cancelled'),
    )
    status = models.CharField(max_length=150, choices=ORDER_STATUS, default='ordered')
    is_paid = models.BooleanField(default=False)


    def __str__(self) :
        return self.product.name
    
    def total(self) :
        price = (self.product_price * self.quantity)
        tax = (5 * price) / 100
        total_price = price + tax
        return total_price
    
    def tax(self) :
        price = (self.product_price * self.quantity)
        tax = (5 * price) / 100
        return tax