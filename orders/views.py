from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from general import convert_response
from account.models import *
from django.db.models import Sum, Count, F
from .models import Orders, Orderdetails 
from orders.serializers import OrdersSerializer, OrderdetailsSerializer 


class OrderList(APIView):
    """
    List all orders, or create a new order.
    """

    def get(self, request, format=None):
        total_revenue = Orders.objects.aggregate(
            total_revenue=Sum('total'),
            total_order = Count("id")
        )


        orders = Orders.objects.all()
        serializer = OrdersSerializer(orders, many=True)
        return Response(convert_response
                        (message="success", 
                         status_code=200, 
                         data=serializer.data,
                         bonus=total_revenue))
    

    def post(self, request, format=None):
        order_input = request.data.get("order")  # dict
        order_item_input = request.data.get("orderitem")
        # order_input["user_created"] = user.id
        # order_input["user_updated"] = user.id

        serilizer = OrdersSerializer(data=order_input, context={"user": request.user, "name": "hao nguyen"}) #contex này để truyền tham số bên ngoài vào serializer

        if not serilizer.is_valid():
            return Response("fail", 400)
        order_instance = serilizer.save()  # tạo bản ghi order
        # order_id = order_instance.id

        # for item in order_item_input:
        #     item["order"] = order_id
        serializer_orderitem = OrderdetailsSerializer(data=item, context={"order": request.user})
        if not serializer_orderitem.is_valid():
            return Response("fail", 400)
        serializer_orderitem.save()

        return Response(convert_response("Success", 200, {"order_id": order_id}))

class OrderDetail(APIView):
    """
    Retrieve, update or delete an order instance.
    """

    def get_object(self, pk):
        try:
            return Orders.objects.get(pk=pk)
        except Orders.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        order = self.get_object(pk)
        serializer = OrdersSerializer(order)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        order = self.get_object(pk)
        serializer = OrdersSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        order = self.get_object(pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#7. Tổng doanh thu theo mỗi đơn hàng
class OrderRevenue(APIView):

    def get(self, request):
        data = Orders.objects.annotate(
            revenue=Sum(
                F("orderdetails__quantity") * F("orderdetails__unitprice") - F("orderdetails__discount")
            )
        ).values("id", "code", "revenue")

        return convert_response({"OrderRevenue": list(data)}, status_code=200)
