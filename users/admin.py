from django.contrib import admin
from .models import Account, UserProfile, Address
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html


class AccountAdmin(UserAdmin) :
    list_display = ('email', 'first_name', 'last_name', 'date_joined', 'last_login', 'is_active')
    
    # To make first name also a link
    list_display_links = ('email', 'first_name')
    
    # To make readonly on django admin
    readonly_fields = ('date_joined', 'last_login')
    
    # Order of the users in the django admin
    ordering = ('-date_joined',)
    
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    
class UserProfileAdmin(admin.ModelAdmin) :
    
    
    
    
    list_display = ('user', 'city', 'state', 'country')
    list_display_links = ('user',)
    
    
# Register your models here.
admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Address)