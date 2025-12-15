from rest_framework import serializers
from .models import Orders, Orderdetails, Shippers 
from customers.models import Customers 
from products.models import Products 
from django.db.models import Count, Sum



class ShippersSerializer(serializers.ModelSerializer):
    """
    Serializer cho model Shippers (Người giao hàng)
    """
    class Meta:
        model = Shippers
        fields = '__all__'


class OrderdetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Orderdetails
        fields = ('id','order', 'product', 'quantity', 'unitprice', 'discount')



class OrdersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Orders
        fields = (
            'id', 
            'customer', 
            'shipper', 
            'order_date', 
            'code', 
            'employee_name', 
            'total',
            'user_created',
            'user_updated',

        )
    def create(self, validated_data):
        user = self.contex["order"]
        name = self.contex["order"]
        return super().create(validated_data) 




class OrderAdminSerializer(serializers.ModelSerializer):
    """
    Serializer dùng để Ghi/Tạo (Write/POST) đơn hàng mới.
    Đây là Serializer mà bạn sử dụng trong hàm post() của OrderList
    """
    class Meta:
        model = Orders
        fields = ('customer', 'shipper', 'order_date', 'code', 'employee_name')
        
# số lượng khách hàng trên từng đơn hàng của bảng order
# dùng hàm cout đề đếm số lượng khách hàng của tất cả các bản ghi trong đơn hàng
# tính tổng doanh thu của đơn hàng
# trong api danh sách sp, total customer, total count



