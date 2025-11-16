from rest_framework import serializers
from products.models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ["id", "category_name", "description", "user_created", "user_updated"]
    
class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suppliers
        fields = ["id", "supplier_name", "contact_name", "address", "city", "postal_code", "country", "phone","user_created", "user_updated"]

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ["id", "supplier", "category", "product_name", "unit", "price", "user_created", "user_updated"]
    