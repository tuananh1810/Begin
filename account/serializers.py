from rest_framework import serializers
from django.contrib.auth import authenticate
from account.models import *
from orders import *
from orders.models import Orders
from customers.models import Customers

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField()

    class Meta:
        model = Account
        fields = ["email", "username", "password"]

        def create(self, validated_data):
            user = Account(
                email = validated_data['email'],
                username = validated_data['username']
            )
            user.set_password(validated_data['password'])
            user.save()
            return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def varidate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Sai tài khoản hoặc mật khẩu")

class AccountSerializerView(serializers.ModelSerializer):
    revenua = serializers.SerializerMethodField()
    kpi = serializers.SerializerMethodField()
    count_order = serializers.SerializerMethodField()
    count_customer = serializers.SerializerMethodField()
    class Meta:
        model = Account
        fields = ["email", "username", "date_joined", "is_active", "is_staff","revenua","kpi","count_order","count_customer"]
        

    def get_revenua(self, instance): #instance = account
        orders = Orders.objects.filter(user_created=instance) # list danh sách đơn hàng
        total = 0 
        for order in orders: #duyệt qua từng phần từ trong list order
            total += order.total #Tính tông total trong danh sách order
        return total
    

    #tạo thêm trường dữ liệu trả thêm trường kpi hiển thị nếu doanh số đơn hàng nhỏ hơn 10k trả ra string là ko đạt kpi
    def get_kpi(self, object):
        total_order = Orders.objects.filter(user_created=object)
        total = 0
        for order in total_order:
            total += order.total
        if total <10000:
            return "không đạt kpi"
        return "đạt kpi"
    
    # đếm số lượng khách hàng và đơn hàng của từng account để tên trường là count_order và count_customer
    def get_count_order(self, instance):
        return Orders.objects.filter(user_created=instance).count()
    def get_count_customer(self, instance):
        return Customers.objects.filter(user_created=instance).count()

class StaffSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Account
        field = "__all__"



    
    
    
    

        