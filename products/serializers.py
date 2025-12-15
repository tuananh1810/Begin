from rest_framework import serializers
from products.models import *
from account.serializers import *
from orders.models import *

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
    total_sold = serializers.SerializerMethodField()
    count_order = serializers.SerializerMethodField()
    count_customer = serializers.SerializerMethodField()
    total_order = serializers.IntegerField(read_only=True)
    total_customer = serializers.IntegerField(read_only=True)



    category_data = CategorySerializer(source="category", read_only=True)
    supplier_data = SupplierSerializer(source="supplier", read_only =True)
    user_created_data = AccountSerializerView(source="user_created", read_only =True)
    class Meta:
        model = Products
        fields = ["id", "supplier", "category", "product_name", "unit",
                   "price", "user_created", "user_updated","category_data","supplier_data",
                  "user_created_data","total_sold","count_order", "count_customer","total_order","total_customer"]
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

    def get_total_sold(self, obj):
        order_detail = Orderdetails.objects.filter(product=obj)
        total = 0
        for item in order_detail:
            total += item.quantity
        return total
    def get_count_order(self, instance):
        orders = Orderdetails.objects.filter(product=instance).count()
        return orders
    def get_count_customer(self, instance):
        customers = Orderdetails.objects.filter(product=instance).count()
        return customers
    
# lấy nhân viên có số lượng bán nhiều nhất: 
# 1. lấy danh sách nhân viên
# 2. duyệt qua từng phần tử trong danh sách nhân viên đẻ lấy ra số lượng sản phẩm bán của từng nhân viên
# 3. so sánh số lượng bán nhiều nhất rồi trả ra

#lấy nhân viên có doanh thu nhieu nhất giống ở trên trừ  bước 3

