from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.forms import inlineformset_factory # helps with creating multiple forms within one form
from .filters import OrderFilter

from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .decorators import *


@unathenticated_user
def registerPage(request):
    form = UserRegisterForm()

    if request.method=='POST':
        form = UserRegisterForm(request.POST)  # PASS IN THE POST DATA
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customer')
            user.groups.add(group) # Associate a new user with the 'customer' account Group
            Customer.objects.create(
                user=user
            ) # make sure when a new user registers, he/she is linked to customer profile.

            messages.success(request, 'Account was created for ' +username)
            return redirect('login')

    context = {"form": form}
    return render(request, 'accounts/register.html', context)



@unathenticated_user
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



def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only  
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



@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all() # applying the 'User' onetoone relationship with 'Customer'
    
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {"orders": orders, "total_orders": total_orders,
               "delivered": delivered, "pending": pending}
    return render(request, 'accounts/user.html', context)



@login_required(login_url='login')
# 'admin' is one of the two groups i created in the admin page
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()

    return render(request, 'accounts/products.html', {'products': products})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createCustomer(request):
    if request.method == 'POST':
        form = NewCustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'New customer has been created')
            return redirect('home')
    else: 
        form = NewCustomerForm()
    return render(request, 'accounts/new_customer.html', {'form': form})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateCustomer(request, pk):

    customer = Customer.objects.get(id=pk)
    form = NewCustomerForm(instance=customer)  # populate all fields with data

    if request.method == 'POST':
        form = NewCustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {"form": form}
    return render(request, 'accounts/update_customer.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customers(request, pk):
    customer = Customer.objects.get(id=pk)

    orders = customer.order_set.all()
    orders_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {"customer": customer,
               "orders": orders, "orders_count": orders_count, "myFilter": myFilter}
    return render(request, 'accounts/customers.html', context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
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


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
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


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)

    if request.method=="POST":
        order.delete()
        return redirect('/')
    context = {"item":order}

    return render(request, 'accounts/delete.html', context)
