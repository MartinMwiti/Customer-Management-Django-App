from django.shortcuts import render, redirect
from .models import *
from .forms import *

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

    context = {"customer": customer,
               "orders": orders, "orders_count": orders_count}
    return render(request, 'accounts/customers.html', context)


def createOrder(request):

    form = OrderForm()
    if request.method == 'POST':
        #print('Printing Post', request.POST)
        form = OrderForm(request.POST) # If the data passed is POST, pass in the POST data i.e fill the form object with the POST data
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {"form":form}
    return render(request, 'accounts/order_form.html', context)


def updateOrder(request,pk):

    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order) # populate with data
    
    # makes sure the changes are saved
    if request.method == 'POST': 
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {"form": form}
    return render(request, 'accounts/order_form.html', context)
