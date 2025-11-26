from rest_framework import serializers
from products.models import *
from account.serializers import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ["id", "category_name", "description", "user_created", "user_updated"]
    def create(self, validated_data):
        user = self.context["user"]
        validated_data["user_created"] = user
        return super().create(validated_data)
    def update(self, instance, validated_data):
        user = self.context["user"]
        validated_data["user_updated"] = user
    
class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suppliers
        fields = ["id", "supplier_name", "contact_name", "address", "city", "postal_code", 
                  "country", "phone","user_created", "user_updated"]
    def create(self, validated_data):
        user = self.context["user2"]
        validated_data["user_created"] = user
        return super().create(validated_data)
    def update(self, instance, validated_data):
        user = self.context["user2"]
        validated_data["user_updated"] = user

class ProductSerializer(serializers.ModelSerializer):
    category_data = CategorySerializer(source="category", read_only=True)
    supplier_data = SupplierSerializer(source="supplier", read_only =True)
    user_created_data = AccountSerializerView(source="user_created", read_only =True)
    class Meta:
        model = Products
        fields = ["id", "supplier", "category", "product_name", "unit",
                   "price", "user_created", "user_updated","category_data","supplier_data",
                  "user_created_data",]
    def create(self, validated_data):
        user = self.context["user3"]
        category_instance = self.context["category_instance"] #2 cái là 2 trường cần truyền vào để tạo
        supplier_instace = self.context["supplier_instance"]
        validated_data["supplier"] = supplier_instace
        validated_data["category"] = category_instance #truyền trong biến từ serializer vào dữ liệu
        validated_data["user_created"] = user
        return super().create(validated_data)
    def update(self, instance, validated_data):
        user = self.context["user3"]
        validated_data["user_updated"] = user
        