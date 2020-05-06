from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),

    path('register/', views.registerPage, name="register"),
    path('user/', views.userPage, name="user-page"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('account/', views.accountSettings, name="account"),

    path('products/', views.products, name="products"),

    path('customers/<str:pk>', views.customers, name="customers"),
    path('new_customers/', views.createCustomer, name="new_customers"),
    path('update_customer/<int:pk>', views.updateCustomer, name="update_customer"),


    path('create_order/<str:pk>/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),
]
