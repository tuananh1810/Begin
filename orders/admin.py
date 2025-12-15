from django.contrib import admin
from orders.models import Orders, Shippers, Orderdetails, StatusOrder
admin.site.register(Orders)
admin.site.register(Shippers)
admin.site.register(Orderdetails)
admin.site.register(StatusOrder)
# Register your models here.

