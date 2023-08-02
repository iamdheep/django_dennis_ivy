from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

# create your view here
from . models import *
from . forms import OrderForms
from . filters import Orderfilter


# Create your views here.
def login(request):
    
    context = {}
    return render(request, 'accounts/login.html', context)

def register(request):
    form = UserCreationForm()
    context = {}
    return render(request, 'accouts/register.html',context)

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


def product(request):
    products = Product.objects.all()
    return render(request, 'accounts/product.html', {'products': products})


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

def deleteOrder(request, pk_d_id):
    order = Order.objects.get(id=pk_d_id)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'item':order}
    print("success")
    return render(request, 'accounts/delete.html',context)