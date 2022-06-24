from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from numpy import product

from .forms import AddressForm, RegistrationForm, ReviewForm, UserForm, UserProfileForm
from .models import *
from . otp import *
from product.models import *
from cart.models import *
from wishlist.models import *
from orders.models import *
from cart.views import _cart_id
from wishlist.views import _wishlist_id

# verify email and forgot password
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


# pagination
from django.core.paginator import Paginator

# searching
from django.db.models import Q

"""
- You have to install requests module to use this
- To redirect to somepage after '?next=' in url
- Here we redirect to checkout after login
"""
import requests

# Create your views here.
def loginPage(request):
    
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if email == '' and password == '':
            messages.error(request, "Please provide an email and password")
        elif password == '':
            messages.error(request, "Please provide password")
        elif email == '':
            messages.error(request, "Please provide an email")
        else:
            try:
                user = Account.objects.get(email=email)
            except:
                messages.error(request, "user does not exist")
                
        user = authenticate(email=email, password=password)
        
        if user is not None:

            # Assigning current cart to the user
            try :
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                
                if is_cart_item_exists :
                    cart_items = CartItem.objects.filter(cart=cart)
                    
                    for item in cart_items :
                        item.user = user
                        item.save()
            except :
                pass
            
            # Assigning current wishlist to the user
            try :
                wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
                is_wishlist_item_exists = WishlistItem.objects.filter(wishlist=wishlist).exists()
                
                if is_wishlist_item_exists :
                    wishlist_items = WishlistItem.objects.filter(wishlist=wishlist)
                    for item in wishlist_items :
                        item.user = user
                        item.save()
            except :
                pass
                        
            login(request, user)
            
            """
            Redirecting to checkout page
            """
            # url => collect the previous url where we came from
            url = request.META.get('HTTP_REFERER')
            
            try :
                query = requests.utils.urlparse(url).query
                # result of query when we come from checkout => next=/cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params :
                    next_page = params['next']
                    return redirect(next_page)
            except :
                return redirect('home')
        else:
            messages.error(request, "email or password does not match")
            return redirect('login')
            
    return render(request,'users/login.html')



def registerPage(request):
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            mobile = form.cleaned_data['mobile']
            password = form.cleaned_data['password']
            
            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                mobile=mobile,
                password=password,
            )
            user.save()
            
            user_profile = UserProfile()
            user_profile.user = user
            user_profile.save()
            
            messages.success(request, 'Registration Successful!')
            request.session['mobile']=mobile
            send_otp(mobile)
            return redirect('register-otp')
    else :
        form=RegistrationForm()
            
    
    context = {'form' : form}
    return render(request, 'users/sign-up.html', context)


def register_otp(request):
    if request.method == 'POST':
        check_otp = request.POST.get('otp')
        mobile=request.session['mobile']
        check=verify_otp(mobile,check_otp)
        if check:
            user = Account.objects.get(mobile=mobile)
            user.is_verified = True
            user.is_active = True
            user.save()
            messages.success(request, 'Otp verification Completed')
            return redirect('login')
        else:
            messages.error(request,'Invalid OTP')
            return redirect('register-otp')
    return render(request,'users/register-otp.html')

def resend_otp(request) :
    if request.method == 'POST' :
        mobile = request.POST['mobile']
        request.session['mobile']=mobile
        send_otp(mobile)
        return redirect('register-otp')
    return render(request, 'users/mobile-number.html')

def logoutUser(request):
    logout(request) 
    return redirect('login')


# forgot password
def forgot_password(request) :
    if request.method == 'POST' :
        email = request.POST['email']
        
        if Account.objects.filter(email=email).exists() :
            user = Account.objects.get(email__exact = email)
            
            # reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            
            context = {
                'user' : user,
                'domain' : current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
            }
            
            message = render_to_string('users/reset-password-mail.html', context)
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            
            messages.success(request, 'Password reset email have sent to your email')
            return redirect('login')
        else :
            messages.error(request, 'Account does not exist, Please Sign up ')
            return redirect('forgot-password')
    else :
        return render(request, 'users/user-email.html')

def reset_password_validate(request, uidb64, token) :
    try :
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist) :
        user = None
        
    if user is not None and default_token_generator.check_token(user, token) :
        request.session['uid'] = uid
        messages.success(request, 'Please Reset Your Password')
        return redirect('reset-password')
    else :
        messages.error(request, 'The link has been expired')
        return redirect('login')
    
def reset_password(request) :
    if request.method == 'POST' :
        new_password = request.POST['password']
        confirm_password = request.POST['confirm-password'] 
        
        if new_password == confirm_password :
            uid = request.session['uid']
            user = Account.objects.get(pk=uid)
            user.set_password(new_password)
            user.save()
            messages.success(request, 'PASSWORD RESET SUCCESS!')
            return redirect('login')
        else :
            messages.error(request, 'Password does not match')
            return redirect('reset-password')
    else :
        return render(request, 'users/reset-password.html')
         


def home(request) :
    return render(request, 'users/home.html')

# shop
def shop(request, category_slug=None) :
    categories = None
    products = None
    
    if category_slug is not None :
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, available=True)
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else :
        products = Product.objects.all().filter(available=True).order_by('id')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
        
        
    context = {
        
        # for paginations, instead of passing the whole products, only pass paged products which will be 6 in this case.
        'products' : paged_products,
        'product_count' : product_count,
    }
    return render(request, 'users/shop.html', context)


# single product
def product_details(request, category_slug, product_slug) :
    
    user_profile = None
    
    try :
        user_profile = UserProfile.objects.get(user_id=request.user.id)
    except :
        pass

    try :
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        
        
        if request.user.is_authenticated :
            in_cart = CartItem.objects.filter(user=request.user, product=single_product).exists()
            
            in_wishlist = WishlistItem.objects.filter(user=request.user, product=single_product).exists()
        else :
            
            # cart => is the foriegn key of CartItem model
            in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
            
            in_wishlist = WishlistItem.objects.filter(wishlist__wishlist_id=_wishlist_id(request), product=single_product).exists()
    except Exception as e :
        raise e
    
    order_product = None    
    try :
        try :
            order_product = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except :
            pass
    except OrderProduct.DoesNotExist :
        order_product = None
        
    # Get the Reviews
    reviews = ProductReview.objects.filter(product_id=single_product.id, status=True)
        
    context = {
        'product' : single_product,
        'in_cart' : in_cart,
        'in_wishlist' : in_wishlist,
        'order_product' : order_product,
        'reviews' : reviews,
        'user_profile' : user_profile,
    }
    return render(request,'users/product-details.html', context)


# product search
def search(request) :
    
    if 'keyword' in request.GET :
        keyword = request.GET['keyword']
        if keyword :
            products = Product.objects.order_by('-created_on').filter(Q(description__icontains = keyword) | Q(name__icontains = keyword))
            
            paginator = Paginator(products, 6)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
            product_count = products.count()
        else :
            products = Product.objects.all().filter(available=True).order_by('id')
            paginator = Paginator(products, 6)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
            product_count = products.count()
    
    context = {
        'products' : paged_products,
        'product_count' : product_count
    }
    return render(request, 'users/shop.html', context)


# PRODUCT FILTERING
def filter_product(request) :
    if request.method == 'POST' :
        
        if request.POST['min_price'] == "" :
            min_price = 0
        else :
            min_price = request.POST['min_price']
            
        if request.POST['max_price'] == "" :
            max_price = 9999999999999999
        else :
            max_price = request.POST['max_price']
        
        
        try :
            url = request.META.get('HTTP_REFERER')
            categories = Category.objects.all()
            category_slug = ""
            for category in categories :
                if '/shop/category/'+category.slug in url :
                    category_slug = category.slug
                
            category = Category.objects.get(slug=category_slug)
            
            products = Product.objects.filter(price__range=(min_price, max_price), category=category)
        except Category.DoesNotExist :
            products = Product.objects.all().filter(
                price__range=(min_price, max_price)
            )
    else :
        products = Product.objects.all()
        
        
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = products.count()
    
    context = {
        'products' : paged_products,
        'product_count' : product_count,
    }
    
    return render(request, 'users/shop.html', context)   


""" USER PROFILE """
@login_required(login_url='login')
def my_account(request) :
    
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()
    order_items = OrderProduct.objects.filter(order=orders)
    user_profile = UserProfile.objects.get(user_id=request.user.id)
   
    context = {
        'orders' : orders,
        'order_items' : order_items,
        'orders_count' : orders_count,
        'user_profile' : user_profile,
    }
    return render(request, 'users/my-account.html', context)

@login_required(login_url='login')
def my_address(request) :
    if request.method == 'POST' :
        form = AddressForm(request.POST)
        if form.is_valid() :
            new_address = form.save(commit=False)
            new_address.user = request.user
            new_address.save()
            
            messages.success(request, 'Address Added Successfully!')
            return redirect('my-address')
        else :
            messages.error(request, 'Oops, There is an error while adding the Address')
            return redirect('my-address')
            
    address = Address.objects.filter(user=request.user).order_by('-created_at')
    form = AddressForm()
    context = {
        'form' : form,
        'address' : address,
    }
    return render(request, 'users/my-address.html', context)

@login_required(login_url='login')
def delete_address(request, id) :
    if request.method == 'POST' :
        delete_address = Address.objects.get(pk=id)
        delete_address.delete()
        return redirect('my-address')


@login_required(login_url='login')
def my_orders(request) :
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'orders' : orders
    }
    return render(request, 'users/my-orders.html', context)


@login_required(login_url='login')
def edit_profile(request) :
    
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST' :
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        
        if user_form.is_valid() and profile_form.is_valid() :
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your Profile has been updated')
            return redirect('edit-profile')
    else :    
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)    
    
    context = {
        'user_form' : user_form,
        'profile_form' : profile_form,
        'user_profile' : user_profile,
    }
    
    return render(request, 'users/edit-profile.html', context)

@login_required(login_url='login')
def change_password(request) :
    if request.method == 'POST' :
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(email__exact = request.user.email)
        
        if new_password == confirm_password :
            success = user.check_password(current_password)
            if success :
                user.set_password(new_password)
                user.save()
                
                # logout(request) 
                
                messages.success(request, 'Password changed successfully')
                return redirect('my-account')
            else :
                messages.error(request, 'Please enter correct Current Password')
                return redirect('change-password')
        else :
            messages.error(request, 'New Password Does Not Match')
            return redirect('change-password')
        
    
    return render(request, 'users/change-password.html')


@login_required(login_url='login')
def order_details(request, order_id) :
    order_details = OrderProduct.objects.filter(order__tracking_no=order_id).order_by('-created_at')
    order = Order.objects.get(tracking_no=order_id)
    
    context = {
        'order_details' : order_details,
        'order' : order,
    }
    
    return render(request, 'users/order-details.html', context)


@login_required(login_url='login')
def cancel_order(request, pk):
    cancel_product = OrderProduct.objects.get(id=pk)
    cancel_product.status = 'cancelled'
    cancel_product.save()
    
    product_id = cancel_product.product.id
    
    product = Product.objects.get(id=product_id)
    product.stock += cancel_product.quantity
    product.save()
    
    return redirect('my-orders')

# VERIFY MOBILE NUMBER
def verify_mobile_number(request):
    user = request.user
    mobile = user.mobile
    request.session['mobile'] = mobile
    user_profile = UserProfile.objects.get(user_id=request.user.id)
    
    context = {
        'mobile' : mobile,
        'user_profile' : user_profile,
    }
    
    return render(request, 'users/verify-mobile-number.html', context)
    

# VERIFY EMAIL
@login_required(login_url='login')
def verify_email(request) :
    user = request.user
    email = user.email
    user_profile = UserProfile.objects.get(user_id=request.user.id)
    context = {
        'email' : email,
        'user_profile' : user_profile,
    }
    return render(request, 'users/verify-email.html', context)

@login_required(login_url='login')
def send_email_link(request):
    user = request.user
    email = user.email
    user_profile = UserProfile.objects.get(user_id=request.user.id)
    
    current_site = get_current_site(request)
    mail_subject = 'Verify Your email for Office Fit Account'
    message = render_to_string('users/verify-email-link.html', {
        'user' : user,
        'domain' : current_site,
        'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
        'token' : default_token_generator.make_token(user),
    })
    to_email = email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()
    messages.success(request, 'Verification Link send to your mail.')
    
    return redirect('verify-email')

@login_required(login_url='login')
def activate(request, uidb64, token) :
    
    try :
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist) :
        user = None
        
    if user is not None and default_token_generator.check_token(user, token) :
        user.email_verified = True
        user.save()
        messages.success(request, 'Your Email is Verified!')
        return redirect('verify-email')
    else :
        messages.error(request, 'Something went wrong while verifying your Email!!!')
        return redirect('verify-email')

    

# Review Product
def submit_review(request, product_id) :
    
    # To redirect into the same page
    url = request.META.get('HTTP_REFERER')
    
    if request.method == 'POST' :
        try :
            reviews = ProductReview.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you, Your review has been Updated!')
            return redirect(url)
        except ProductReview.DoesNotExist :
            form = ReviewForm(request.POST)
            if form.is_valid() :
                data = ProductReview.objects.create(
                    subject = form.cleaned_data['subject'],
                    rating = form.cleaned_data['rating'],
                    review = form.cleaned_data['review'],
                    ip = request.META.get('REMOTE_ADDR'),
                    product_id = product_id,
                    user_id = request.user.id,
                )
                data.save()
                messages.success(request, 'Thank You, Your review has been Submitted!')
                return redirect(url)
            
# 404 error Page
def error_404(request, exception) :
    return render(request, 'error-404.html', status=404)