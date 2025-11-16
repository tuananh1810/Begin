from django.contrib import admin
from products.models import Products, Suppliers, Categories
admin.site.register(Products)
admin.site.register(Suppliers)
admin.site.register(Categories)
# Register your models here.
