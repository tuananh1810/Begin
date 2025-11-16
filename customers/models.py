from django.db import models

# Create your models here.
class Customers(models.Model):
    customer_name = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=100, blank= True, null= True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank= True, null= True)
    country = models.CharField(max_length=50)
    def __str__(self):
        return self.customer_name





