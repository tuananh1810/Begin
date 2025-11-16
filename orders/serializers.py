from rest_framework import serializers
from .models import Orders, Orderdetails, Shippers 
from customers.models import Customers 
from products.models import Products 



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

        )




class OrderAdminSerializer(serializers.ModelSerializer):
    """
    Serializer dùng để Ghi/Tạo (Write/POST) đơn hàng mới.
    Đây là Serializer mà bạn sử dụng trong hàm post() của OrderList
    """
    class Meta:
        model = Orders
        fields = ('customer', 'shipper', 'order_date', 'code', 'employee_name')
        
