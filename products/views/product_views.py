from django.shortcuts import render
from products.models import Products, Categories
from products.serializers import ProductSerializer
from django.http import Http404
from products.serializers import ProductSerializer, CategorySerializer, SupplierSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from handle import Paginate



class ProductList(APIView):
    permission_classes = [IsAuthenticated]

    """
    List all customners, or create a new customer.
    """

    def get(self, request, format=None):
        products = Products.objects.all()
        search = request.query_params.get("search")
        if search:
            products = products.filter(product_name__icontains=search) #icontains: ký tự search nằm trong product_name(so sánh ==)
        products = Paginate(products, request.GET)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        input = request.data
        cate_name = input["category_name"]
        category = Categories.objects.get(category_name = cate_name)
        input["category"] = category.id
        print(input)
        serializer = ProductSerializer(data=input)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProductDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get_object(self, pk):
        try:
            return Products.objects.get(pk=pk)
        except Products.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        products = self.get_object(pk)
        serializer = ProductSerializer(products)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        products = self.get_object(pk)
        serializer = ProductSerializer(products, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        products = self.get_object(pk)
        products.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ProductSupplierCategoryCreate(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request): #lấy dữ liệu
        user = request.user
        product_input = request.data.get("product") 
        category_input = request.data.get("category")
        supplier_input = request.data.get("supplier")
        # product_input["user_created"] = user.id
        # category_input["user_created"] = user.id
        # supplier_input["user_created"] = user.id

        # product_input["user_updated"] = user.id
        # category_input["user_updated"] = user.id
        # supplier_input["user_updated"] = user.id        
        print(product_input)
        print(category_input)
        print(supplier_input)
        if not product_input or not category_input or not supplier_input: #nếu trong padload ko tồn tại 3 t.tin -> lỗi 
            return Response("lỗi",  status=status.HTTP_400_BAD_REQUEST)
        category_serializer = CategorySerializer(data=category_input, context={"user": request.user})
        if not category_serializer.is_valid():
            return Response(category_serializer.errors,  status=status.HTTP_400_BAD_REQUEST)
        supplier_serializer = SupplierSerializer(data=supplier_input, context={"user2": request.user})
        if not supplier_serializer.is_valid():
            return Response(supplier_serializer.errors,  status=status.HTTP_400_BAD_REQUEST)
        category_instance = category_serializer.save()
        supplier_instance = supplier_serializer.save()
        # print("Suplier ==", supplier_instance)
        # product_input["category"] = category_instance.id
        # product_input["supplier"] = supplier_instance.id
        product_serializer = ProductSerializer(data=product_input, context={"user3": request.user, "category_instance": category_instance, "supplier_instance": supplier_instance})
        if not product_serializer.is_valid():
            return Response(product_serializer.errors,  status=status.HTTP_400_BAD_REQUEST)
        product_instance = product_serializer.save()
        return Response(product_serializer.data, status=status.HTTP_201_CREATED)
    
class ProductListView(APIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer 
    filter_backends = [DjangoFilterBackend] # bộ lọc (filter backend) lọc dữ liệu trong API bằng query parameters
    filterset_fields = ['category', 'supplier']