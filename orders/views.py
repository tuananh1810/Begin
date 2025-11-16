from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Orders, Orderdetails 
from orders.serializers import OrdersSerializer, OrderdetailsSerializer 


class OrderList(APIView):
    """
    List all orders, or create a new order.
    """

    def get(self, request, format=None):
        orders = Orders.objects.all()
        serializer = OrdersSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        order_input = request.data.get("order") 
        order_item_input = request.data.get("orderitem")

        serilizer = OrdersSerializer(data=order_input)

        if not serilizer.is_valid():
            return Response(serilizer.errors, status=status.HTTP_400_BAD_REQUEST)
        order_instance = serilizer.save()  
        order_id = order_instance.id

        for item in order_item_input:
            item["order"] = order_id
            serializer_orderitem = OrderdetailsSerializer(data=item)
            if not serializer_orderitem.is_valid():
                return Response(serializer_orderitem.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer_orderitem.save()

        return Response(serilizer.data, status=status.HTTP_201_CREATED)

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

