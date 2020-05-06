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



class UserUpdateForm(forms.ModelForm):  # Allow us to update user email
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):  # Allow us to update profile image
    class Meta:
        model = Customer
        fields = ['phone', 'profile_pic']


class NewCustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'




class OrderForm(ModelForm):
	class Meta:
	    model = Order
	    fields = '__all__'
      

class UpdateOrderForm(ModelForm):
	class Meta:
	    model = Order
	    fields = ['product', 'status']




