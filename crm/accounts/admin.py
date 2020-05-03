from django.contrib import admin

# Register your models here.
from .models import * # IMPORT ALL MODELS

admin.site.register(Customer) # to view the created customer database table in the admin
admin.site.register(Product)
admin.site.register(Tag)
admin.site.register(Order)
