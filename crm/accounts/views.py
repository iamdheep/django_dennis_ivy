from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# create your view here
from . models import *
from . forms import OrderForms, CreateUserForm, CustomerForm
from . filters import Orderfilter
from . decorators import unauthenticated_user,allowed_users,admin_only

# Create your views here.
@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username= username, password= password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')
            return render(request, 'accounts/login.html')
    context = {}
    return render(request, 'accounts/login.html', context)

# @unauthenticated_user
# def registerPage(request):
#     form = CreateUserForm()
#     if request.method == 'POST':
#         form  = CreateUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             user = form.cleaned_data.get('username')
#             messages.success(request, 'Account was created for '+ user)
#             return redirect('login')
#     context = {'form':form}
#     return render(request, 'accounts/register.html',context)

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form  = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            

            messages.success(request, 'Account was created for '+ username)
            return redirect('login')
    context = {'form':form}
    return render(request, 'accounts/register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_Customer = customers.count()
    total_Orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='pending').count()
    context = {'order': orders, 'customers': customers, 'total_orders': total_Orders,
               'delivered': delivered, 'pending': pending}
    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_Orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='pending').count()
    print('ORDERS : ',orders)
    context = {'orders':orders, 'total_orders': total_Orders,
               'delivered': delivered, 'pending': pending}
    return render(request, 'accounts/user.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)
	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES,instance=customer)
		if form.is_valid():
			form.save()
	context = {'form':form}
	return render(request, 'accounts/account_setting.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def product(request):
    products = Product.objects.all()
    return render(request, 'accounts/product.html', {'products': products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk_c_id):
    customer = Customer.objects.get(id=pk_c_id)
    order = customer.order_set.all()
    order_count = Order.objects.count()
    order_cnt = order.filter(customer=pk_c_id).count()

    myFilter = Orderfilter(request.GET, queryset=order)
    order = myFilter.qs

    context = {'customer': customer, 'order': order,
               'order_count': order_count, 'order_cnt': order_cnt, 'myFilter':myFilter}
    return render(request, 'accounts/customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk_c_id):
    #creating objects with parent instances and form set 
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'),extra = 10)
    customer = Customer.objects.get(id=pk_c_id)
    formset = OrderFormSet( queryset=Order.objects.none(), instance=customer)
    # form = OrderForms(initial={'customer':customer})    
    if request.method == 'POST':
        # form = OrderForms(request.POST)
        formset = OrderForms(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'formset': formset}
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk_u_id):
    order = Order.objects.get(id=pk_u_id)
    form = OrderForms(instance=order)
    if request.method == 'POST':
        form = OrderForms(request.POST, instance = order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk_d_id):
    order = Order.objects.get(id=pk_d_id)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'item':order}
    return render(request, 'accounts/delete.html',context)
