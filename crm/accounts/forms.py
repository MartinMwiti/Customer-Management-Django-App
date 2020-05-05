from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Order, Customer
from django import forms


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Email'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__' # use all fields



class NewCustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        