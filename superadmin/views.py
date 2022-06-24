from django.shortcuts import redirect, render
from django.contrib import auth, messages
from cart.models import *
from users.models import Account
from django.contrib.auth import login, logout
from .forms import *
from product.models import *
from orders.models import *

from django.contrib.auth.decorators import login_required

# Create your views here.
def superadmin_login(request) :  
    if request.user.is_authenticated and request.user.is_superadmin :
        return redirect('superadmin-dashboard')
    
    if request.method == 'POST' : 
        email = request.POST['email']
        password = request.POST['password']
        
        try:
            user = Account.objects.get(email=email)
        except:
            messages.error(request, "Admin does not exist")
        
        user = auth.authenticate(email=email, password=password, is_superadmin=True)
        
        if user is not None :
            if user.is_superadmin :
                login(request, user)
                return redirect('superadmin-dashboard')
            else :
                messages.error(request, 'You are not an ADMIN!!!')
                return redirect('superadmin-login')
        else :
            messages.error(request, 'Password and Email does not match')
            return redirect('superadmin-login')
    return render(request, 'superadmin/sign-in.html')


def superadmin_logout(request) :
    if request.user.is_superadmin :
        logout(request)
        return redirect("superadmin-login")
    else :
        return redirect('superadmin-login')
    
    
@login_required(login_url='superadmin-login')
def superadmin_dashboard(request):
    if request.user.is_superadmin :
        # Total Revenue
        total_revenue = 0
        products = OrderProduct.objects.exclude(status = 'cancelled')
        for item in products :
            total_revenue += item.product_price
            
        # Total Users
        user_count = Account.objects.exclude(is_superadmin=True)
        u_count =user_count.count()
        
        # Total Products
        product=Product.objects.all()
        p_count = product.count()
        
        # Total Orders
        cancelled = OrderProduct.objects.filter(status = 'cancelled')
        c1 = cancelled.count()
        total_order = Order.objects.all()
        c2 = total_order.count()
        
        #user chart
        active_user = Account.objects.filter(is_active=True, is_superadmin=False)
        blocked_user = Account.objects.filter(is_active=False, is_superadmin=False)
        total_user = int(active_user.count()+blocked_user.count())
        data1=[active_user.count(),blocked_user.count()]
        data1_label =['Active','Blocked']

        # Orders Chart
        cod = Order.objects.filter(payment_method = 'Cash on Delivery')
        online = Order.objects.filter(payment_method = 'razor pay')
        total_orders = int(cod.count()+online.count())
        data3=[cod.count(),online.count()]
        data3_label =['Cash on Delivery','Online Payment']
        
        # Category Chart
        order_products = OrderProduct.objects.all()
        chair, table, sofa = 0, 0, 0
        for order_product in order_products :
            if order_product.product.category.category_name == 'Chair' :
                chair += order_product.quantity
            elif order_product.product.category.category_name == 'Table' :
                table += order_product.quantity
            elif order_product.product.category.category_name == 'Sofa' :
                sofa += order_product.quantity
        total_products = chair + table + sofa
        data4=[chair, table, sofa]
        print(chair, table, sofa)
        data4_label =['Chair','Table', 'Sofa']
        
    

        context = {
            'total_revenue' : total_revenue,
            'total_user':total_user,
            'data1':data1,
            'data1_label':data1_label,
            'data3' : data3,
            'data3_label':data3_label,
            'total_orders' : total_orders,
            'data4' : data4,
            'data4_label':data4_label,
            'total_products' : total_products,
            'u_count' : u_count,
            'p_count' : p_count,
            'c1' : c1,
            'c2' : c2,
        }
        return render(request,'superadmin/dashboard.html', context)
    else :
        return redirect('superadmin-login')



# Customers
@login_required(login_url='superadmin-login')
def customer(request):
    if request.user.is_superadmin :
        q = request.GET.get('q') if request.GET.get('q') != None else ''

        user = Account.objects.filter(first_name__istartswith=q, is_superadmin=False).order_by('-date_joined')
        return render(request, "superadmin/customers.html", {'user':user})
    else :
        return redirect('superadmin-login')
    

@login_required(login_url='superadmin-login')
def customer_block_unblock(request, pk):
    if request.user.is_superadmin :
        customer = Account.objects.get(id=pk)
        if customer.is_active:
            customer.is_active = False   
        else:
            customer.is_active = True
        customer.save()
        return redirect('customers')
    else :
        return redirect('superadmin-login')



# Products
@login_required(login_url='superadmin-login')
def products(request):
    if request.user.is_superadmin :
        q = request.GET.get('q') if request.GET.get('q') != None else ''

        products = Product.objects.filter(name__icontains=q).order_by('-created_on')
        context = {"products" : products}
        return render(request, "superadmin/products.html", context)
    else :
        return redirect('superadmin-login')


@login_required(login_url='superadmin-login')
def add_product(request) :
    if request.user.is_superadmin :
        form = AddProductForm()
        
        if request.method == "POST":
            form = AddProductForm(request.POST, request.FILES)
            if form.is_valid() :
                form.save()
                messages.success(request, 'Product Added Successfully!')
                return redirect('products')
            else:
                messages.error(request, 'Oops, An Error occured while adding the Product!!!')        
        return render(request,'superadmin/add-product.html', {'form' : form})
    else :
        return redirect('superadmin-login')


@login_required(login_url='superadmin-login')
def edit_product(request, pk) :
    if request.user.is_superadmin :
        product = Product.objects.get(id=pk)
        
        if request.method == 'POST' :
            form = AddProductForm(request.POST, request.FILES, instance=product)
            
            if form.is_valid() :
                form.save()
                messages.success(request, 'Product Edited Successfully')
                return redirect('products')
            else:
                messages.error(request, 'Edited version does not saved')
            
        form = AddProductForm(instance=product)
        context = {'form' : form}
        return render(request, 'superadmin/edit-product.html', context)
    else :
        return redirect('superadmin-login')

@login_required(login_url='superadmin-login')
def delete_product(request, pk) :
    if request.user.is_superadmin :
        product = Product.objects.get(id=pk)
        context = {'product' : product}
        
        if request.method == 'POST' :
            product.delete()
            messages.success(request, 'Product Deleted Successfully')
            return redirect('products')
        
        return render(request, 'superadmin/delete-product.html', context)
    else :
        return redirect('superadmin-login')

# category
@login_required(login_url='superadmin-login')
def category(request):
    if request.user.is_superadmin :
        q = request.GET.get('q') if request.GET.get('q') != None else ''

        categories = Category.objects.filter(category_name__icontains=q)
        
        context = {"categories" : categories}
        return render(request, "superadmin/category.html", context)
    else :
        return redirect('superadmin-login')


@login_required(login_url='superadmin-login')
def add_category(request) :
    if request.user.is_superadmin :
        form = AddCategoryForm()
        
        if request.method == "POST":
            form = AddCategoryForm(request.POST, request.FILES)
            if form.is_valid() :
                form.save()
                messages.success(request, 'Category added Successfully!')
                return redirect('category')
            else:
                messages.error(request, 'Oops, An Error occured while adding the Category!!!')        
        return render(request,'superadmin/add-category.html', {'form' : form})
    else :
        return redirect('superadmin-login')


@login_required(login_url='superadmin-login')
def edit_category(request, pk) :
    if request.user.is_superadmin :
        category = Category.objects.get(id=pk)

        if request.method == 'POST' :
            form = AddCategoryForm(request.POST, request.FILES, instance=category)
            
            if form.is_valid() :
                form.save()
                messages.success(request, 'Category Edited Successfully')
                return redirect('category')
            else:
                messages.error(request, 'Edited version does not saved')
            
        form = AddCategoryForm(instance=category)
        context = {'form' : form}
        return render(request, 'superadmin/edit-category.html', context)
    else :
        return redirect('superadmin-login')


@login_required(login_url='superadmin-login')
def delete_category(request, pk) :
    if request.user.is_superadmin :
        category = Category.objects.get(id=pk)
        
        context = {'category' : category}
        
        if request.method == 'POST' :
            category.delete()
            messages.success(request, 'Category Deleted Successfully')
            return redirect('category')
        
        return render(request, 'superadmin/delete-category.html', context)
    else :
        return redirect('superadmin-login')

@login_required(login_url='superadmin-login')
def product_orders(request) :
    if request.user.is_superadmin :
        orders = Order.objects.all().order_by('-created_at')
        context = {
            'orders' : orders
        }
        return render(request, 'superadmin/orders.html', context)
    else :
        return redirect('superadmin-login')
    

@login_required(login_url='superadmin-login')
def delete_order(request, track_no) :
    if request.user.is_superadmin :
        order = Order.objects.get(tracking_no=track_no)
        order.delete()
        messages.success(request, 'Order Deleted Successfully')
        
        return redirect('orders')
    else :
        return redirect('superadmin-login') 


@login_required(login_url='superadmin-login')
def view_shipping_product(request, track_no):
    if request.user.is_superadmin :
        order = Order.objects.get(tracking_no=track_no)
        order_item = OrderProduct.objects.filter(order__tracking_no=track_no).order_by('-created_at')
        
            
        context ={
            'order_item' : order_item,
            'order' : order,
        }
        
        return render(request, "superadmin/order-details.html", context)
    else :
        return redirect('superadmin-login')


@login_required(login_url='superadmin-login')
def edit_shipping_product(request, pk):
    if request.user.is_superadmin :
        url = request.META.get('HTTP_REFERER')
        order_item = OrderProduct.objects.get(id=pk)
        
        if  order_item.status == 'ordered':
            order_item.status = 'shipped'
        elif order_item.status == 'shipped':
            order_item.status = 'out_for_delivery'
        elif order_item.status == 'out_for_delivery':
            order_item.status = 'delivered'
            if order_item.status == 'delivered':
                if order_item.is_paid == False:
                    order_item.is_paid = True
                    order_item.save()
        
        order_item.save()
        return redirect(url)
    else :
        return redirect('superadmin-login')


