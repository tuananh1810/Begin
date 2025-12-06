from django.shortcuts import render
from products.models import Suppliers
from products.serializers import SupplierSerializer
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class SupplierList(APIView):
    """
    List all customners, or create a new customer.
    """

    def get(self, request, format=None):
        suppliers = Suppliers.objects.all()
        search = request.query_params.get("search")
        if search: 
            suppliers = suppliers.filter(supplier_name__icontains=search)
        postal_code = request.query_params.get("post_code")
        if postal_code:
            suppliers = suppliers.filter(postal_code=postal_code)
        
        user_created = request.query_params.get("user_cre")
        if user_created:
            suppliers = suppliers.filter(user_created=user_created)

        
        serializer = SupplierSerializer(suppliers, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SupplierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SpplierDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get_object(self, pk):
        try:
            return Suppliers.objects.get(pk=pk)
        except Suppliers.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        Suppliers = self.get_object(pk)
        serializer = SupplierSerializer(Suppliers)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        Suppliers = self.get_object(pk)
        serializer = SupplierSerializer(Suppliers, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        Suppliers = self.get_object(pk)
        Suppliers.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class SupplierListView(APIView):
    queryset = Suppliers.objects.all()
    serializer_class = SupplierSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    # Lọc theo user_created
    filterset_fields = ['user_created']
    # Tìm kiếm
    search_fields = ['supplier_name', 'contact_name', 'phone']

# 13. Tổng số lượng sản phẩm mà mỗi Supplier cung cấp
class SupplierProductCount(APIView):

    def get(self, request):
        data = Suppliers.objects.annotate(
            total_products=Count("products")
        ).values("id", "supplier_name", "total_products")
        return convert_response({"SupplierProductCount": list(data)}, status_code=200)

# 14. Doanh thu theo mỗi Supplier
class SupplierTotalRevenue(APIView):

    def get(self, request):
        data = Suppliers.objects.annotate(
            total_revenue=Sum(
                F("products__orderdetails__quantity") * F("products__orderdetails__unitprice") - F("products__orderdetails__discount")
            )
        ).values("id", "supplier_name", "total_revenue")

        return convert_response({"SupplierTotalRevenue": list(data)}, status_code=200)