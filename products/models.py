from django.db import models
from account.models import Account

# Create your models here.
class Categories(models.Model):
    category_name = models.CharField(max_length=100)
    description = models.TextField(blank= True, null= True)
    user_created = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True, related_name="cre_category")
    user_updated = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True, related_name="upd_category")
    def __str__(self):
        return self.category_name
    
class Suppliers(models.Model):
    supplier_name = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=100, blank= True, null= True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank= True, null= True)
    country = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    user_created = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True, related_name="cre_supplier")
    user_updated = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True, related_name="upd_supplier")
    def __str__(self):
        return self.supplier_name

class Products(models.Model):
    supplier = models.ForeignKey(Suppliers, on_delete=models.SET_NULL, blank= True, null= True )
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL,  blank= True, null= True)
    product_name = models.CharField(max_length=100)
    unit = models.CharField(max_length=50)
    price = models.FloatField(default=10.2)
    user_created = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True, related_name="cre_product")
    user_updated = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True, related_name="upd_product")
    def __str__(self):
        return self.product_name