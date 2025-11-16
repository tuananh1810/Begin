from django.contrib import admin
from orders.models import Orders, Shippers, Orderdetails
admin.site.register(Orders)
admin.site.register(Shippers)
admin.site.register(Orderdetails)
# Register your models here.

