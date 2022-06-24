import profile
from django.db import  models
from django.contrib.auth. models import BaseUserManager, AbstractBaseUser


# Create your  models here.
class AccountManager(BaseUserManager):
    def create_user(self,first_name,last_name,email,mobile,password=None) :
        if not email:
            raise ValueError('User must have an email address')
        if not mobile:
            raise ValueError('User must have mobile number')
        user=self.model(
            email       =self.normalize_email(email),
            mobile      =mobile,
            first_name  =first_name,
            last_name   =last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,first_name,last_name,mobile,password) :
        user=self.create_user(
            email=self.normalize_email(email),
            mobile=mobile,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        
        user.is_admin=True
        user.is_active=True
        user.is_staff=True
        user.is_superadmin=True
        user.save(using=self._db)
        return user



class Account(AbstractBaseUser) :
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    email           = models.EmailField(max_length=100,unique=True) 
    mobile          = models.CharField(max_length=10,unique=True,null=True)
    
    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now_add=True)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=False)
    is_verified     = models.BooleanField(default=False)
    is_superadmin   = models.BooleanField(default=False)
    email_verified  = models.BooleanField(default=False)

    USERNAME_FIELD  ='email'
    REQUIRED_FIELDS =['first_name', 'last_name', 'mobile']
    
    objects=AccountManager()
    
    
    def __str__(self) :
        return self.email
    
    def full_name(self) :
        return f'{self.first_name} {self.last_name}'
    
    def has_perm(self,perm,obj=None) :
        return self.is_admin
    
    def has_module_perms(self, add_label) :
        return True 
    


class UserProfile(models.Model) :
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    address = models.CharField(blank=True, null=True, max_length=250)
    profile_picture = models.ImageField(blank=True, null=True, upload_to='profiles/')
    city = models.CharField(blank=True, null=True, max_length=50)
    state = models.CharField(blank=True, null=True, max_length=50)
    country = models.CharField(blank=True, null=True, max_length=50)
    
    def __str__(self) :
        return self.user.first_name
    

class Address(models.Model) :
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    address = models.TextField()
    city = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    country = models.CharField(max_length=150)
    pin_code = models.CharField(max_length=6)
    mobile = models.CharField(max_length=10)
    landmark = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
        
    class Meta :
        verbose_name = 'Address'
        verbose_name_plural = "Addresses"
        
    def __str__(self) :
        return self.full_name
    
    

    