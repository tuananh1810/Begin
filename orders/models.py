from django.db import models
from account.models import Account
from customers.models import Customers
from products.models import Products
# Create your models here.

class StatusOrder(models.Model):
    title = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    def __str__(self):
        return self.title

class Shippers(models.Model):
    shipper_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    def __str__(self):
        return self.shipper_name
    
class Orders(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.SET_NULL, blank= True, null= True )
    shipper = models.ForeignKey(Shippers, on_delete=models.SET_NULL, blank= True, null= True )
    order_date = models.DateField()
    code = models.CharField(max_length=50)
    employee_name = models.CharField(max_length=50)
    total = models.FloatField(blank= True, null=True, default=0)
    status = models.ForeignKey(StatusOrder, on_delete=models.SET_NULL, blank= True, null= True, default=None)
    user_created = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True, related_name="create")
    user_updated = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True, related_name="update")
    def __str__(self):
        return self.code

class Orderdetails(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.SET_NULL, blank= True, null= True )
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, blank= True, null= True )
    quantity = models.IntegerField(default=1)
    unitprice = models.FloatField(default=10.2)
    discount = models.FloatField(default=4.2)
    def __str__(self):
        return str(self.order.id)






    