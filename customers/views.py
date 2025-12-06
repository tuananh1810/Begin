from django.shortcuts import render
from customers.models import Customers
from customers.serializers import CustomerSerializer
from django.http import Http404
from account.models import *
from django.db.models import Sum, Count, F
from general import convert_response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class CustomersList(APIView):
    """
    List all customners, or create a new customer.
    """

    def get(self, request, format=None):
        customers = Customers.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get_object(self, pk):
        try:
            return Customers.objects.get(pk=pk)
        except Customers.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        customers = self.get_object(pk)
        serializer = CustomerSerializer(customers)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        customers = self.get_object(pk)
        serializer = CustomerSerializer(customers, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        customers = self.get_object(pk)
        customers.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 8. Khách hàng đã mua bao nhiêu đơn hàng
class CustomerOrderCount(APIView):

    def get(self, request):
        data = Customers.objects.annotate(
            total_orders=Count("orders")
        ).values("id", "name", "total_orders")
        return convert_response({"CustomerOrderCount": list(data)}, status_code=200)

# 9. Khách hàng đã tiêu bao nhiêu tiền
class CustomerTotalSpent(APIView):

    def get(self, request):
        data = Customers.objects.annotate(
            total_spent=Sum("orders__total")
        ).values("id", "name", "total_spent")
        return convert_response({"CustomerTotalSpent": list(data)}, status_code=200)