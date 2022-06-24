from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.db.models import Avg, Count

class Product(models.Model):
    name         = models.CharField(max_length=100 , null=True)
    slug         = models.SlugField(max_length=100, unique=True)
    category     = models.ForeignKey('Category',on_delete=models.CASCADE)
    price        = models.FloatField()
    image_1      = models.ImageField (upload_to="image/product")
    image_2      = models.ImageField (blank=True, null=True, upload_to="image/product")
    image_3      = models.ImageField (blank=True, null=True, upload_to="image/product")
    image_4      = models.ImageField (blank=True, null=True, upload_to="image/product")
    description  = models.TextField(max_length=500, blank=True, null=True)
    stock        = models.IntegerField(default=0)
    available    = models.BooleanField(default=True)
    created_on   = models.DateTimeField(auto_now_add=True)
    
    # to auto generate slug on our Admin
    def save(self, *args, **kwargs) :
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)
        
    
    def get_url(self) :
        return reverse('product-details', args=[self.category.slug, self.slug])
    
    def average_rating(self) :
        reviews = ProductReview.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None :
            avg = float(reviews['average'])
        return avg
    
    def count_rating(self) :
        reviews = ProductReview.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None :
            count = int(reviews['count'])
        return count
 
    def __str__(self):
        return self.name
    
    
class Category(models.Model):
    category_name = models.CharField(max_length=200, unique=True, null=True, blank=True)
    category_description = models.TextField()
    category_image = models.ImageField(upload_to="image/category")
    
    # slug in Django Admin
    slug = models.SlugField(max_length=100, unique=True)
    
    
    # to auto generate slug on our Admin
    def save(self, *args, **kwargs) :
        self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)
    
    # To get url and to give it on the a tag href
    def get_url(self) :
        return reverse('products-by-category', args=[self.slug])
        
        
    # To fix Plural of category in admin side
    class Meta :
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.category_name
    
    
# Product Review
class ProductReview(models.Model) :
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(to='users.Account', on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, null=True, blank=True) 
    review = models.TextField(null=True, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=30, blank=True, null=True)
    status = models.BooleanField(default=True)
    create_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) :
        return f'{self.user.first_name} - {self.product.name} - {self.rating}'
    

