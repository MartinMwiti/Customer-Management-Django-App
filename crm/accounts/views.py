from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.forms import inlineformset_factory # helps with creating multiple forms within one form
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def registerPage(request):
    form = UserRegisterForm()

    if request.method=='POST':
        form = UserRegisterForm(request.POST)  # PASS IN THE POST DATA
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' +user)
            return redirect('login')

    context = {"form": form}
    return render(request, 'accounts/register.html', context)



def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.warning(request, 'Username OR password is incorrect')           

    context = {}
    return render(request, 'accounts/login.html', context)



def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders': orders, 'customers': customers,
               "total_orders": total_orders, "delivered": delivered, "pending": pending}

    return render(request, 'accounts/dashboard.html', context)


def products(request):
    products = Product.objects.all()

    return render(request, 'accounts/products.html', {'products': products})


def customers(request, pk):
    customer = Customer.objects.get(id=pk)

    orders = customer.order_set.all()
    orders_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {"customer": customer,
               "orders": orders, "orders_count": orders_count, "myFilter": myFilter}
    return render(request, 'accounts/customers.html', context)


def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=("product", "status"), extra=3) # extra specifies the number of forms to display 
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
    # form = OrderForm(initial={'customer': customer})
    if request.method == 'POST':
        #print('Printing Post', request.POST)
        # form = OrderForm(request.POST) # If the data passed is POST, pass in the POST data i.e fill the form object with the POST data
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {"formset":formset}
    return render(request, 'accounts/order_form.html', context)


def updateOrder(request,pk):

    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order) # populate all fields with data

    # makes sure the changes are saved
    if request.method == 'POST': 
        form = OrderForm(request.POST, instance=order) # takes the POST data and update the instance
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {"form": form}
    return render(request, 'accounts/update_order.html', context)


def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)

    if request.method=="POST":
        order.delete()
        return redirect('/')
    context = {"item":order}

    return render(request, 'accounts/delete.html', context)
