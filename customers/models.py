from django.db import models
from account.models import Account
# Create your models here.
class Customers(models.Model):
    customer_name = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=100, blank= True, null= True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank= True, null= True)
    country = models.CharField(max_length=50)
    nhom_khach_hang = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=5, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    code = models.CharField(max_length=50, blank=True, null=True, default=None)
    phone = models.CharField(max_length=20, blank=True, null=True, default=None)
    email = models.EmailField(blank=True, null=True, default=None)
    type_customer = models.CharField(max_length=100, blank=True, null=True)
    user_created = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return self.customer_name





