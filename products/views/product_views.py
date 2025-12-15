from django.shortcuts import render
from products.models import Products, Categories
from products.serializers import ProductSerializer
from django.http import Http404
from products.serializers import ProductSerializer, CategorySerializer, SupplierSerializer
from django.db.models import F, Sum, Count, Min, Max, Avg, Q
from orders.models import Orders
from customers.models import Customers
from general import convert_response
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
        #tính toàn MỖI sản phẩm có bao nhiêu đơn hành được bán *(mỗi/từng -> group by)
        
        products = Products.objects.select_related("supplier","category","user_created").annotate( 
            total_order=Count('orderdetails__order', distinct=True),
            total_customer = Count('orderdetails__order__customer', distinct=True)
        )
        
        
        search = request.query_params.get("search")
        
        if search:
            products = products.filter(product_name__icontains=search) #icontains: ký tự search nằm trong product_name(so sánh ==)
        category_id = request.query_params.get("category")  # trả về 10 / None
        if category_id:
            # #TH1 L si sánh theo đối tượng category
            # # category filter id (id là giá trị tuyệt đối)
            # category_instance = Categories.objects.get(id=category_id)
            # # Không thể so sánh 1 đối tượng với 1 trường id
            # products = products.filter(category=category_id)
            
            #TH2: So sánh theo id
            products = products.filter(category_id=category_id)

        supplier_id = request.query_params.get("supplier")
        if supplier_id:
            products = products.filter(supplier_id=supplier_id)
        
        

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
    
class ReportStatistics(APIView):
    def get(self, request):
        result = {
            "total_product_quantity": self.total_product_quantity(),
            "product_price_range": self.product_price_range(),
            "total_revenue": self.total_revenue(),
            "avg_price_by_category": self.avg_price_by_category(),
            "total_customers": self.total_customers(),
        }
        return Response(convert_response
                        (message="success", 
                         status_code=200, 
                         data=result))

    # 1) Tổng số lượng sản phẩm trong hệ thống
    def total_product_quantity(self):
        data = Products.objects.aggregate(
            total_quantity=Count("id")
        )
        print(data)
        return data["total_quantity"]
    # 2) Giá cao nhất & thấp nhất của sản phẩm
    def product_price_range(self):
        data = Products.objects.aggregate(
            max_price=Max("price"),
            min_price=Min("price")
        )
        return data
    # 3) Tổng doanh thu của tất cả đơn hàng
    def total_revenue(self):
        data = Orders.objects.aggregate(
            revenue=Sum("total")
        )
        return data["revenue"]

    # 4) Trung bình giá sản phẩm theo từng category
    def avg_price_by_category(self):
        data = Categories.objects.annotate(
            avg_price=Avg("products__price")
        ).values(
            "id", "category_name", "avg_price"
        )
        return list(data)

    # 5) Tổng số lượng khách hàng
    def total_customers(self):
        data = Customers.objects.aggregate(
            total_customer=Count("id")
        )
        return data["total_customer"]
    
# 10. Tổng số lượng sản phẩm đã bán cho từng sản phẩm
class ProductSalesCount(APIView):

    def get(self, request):
        data = Products.objects.annotate(
            total_sales=Sum("orderdetails__quantity")
        ).values("id", "name", "total_sales")
        return Response( convert_response({"ProductSalesCount": list(data)}, status_code=200))

# 11. Tổng tiền đã bán theo từng sản phẩm
class ProductTotalRevenue(APIView):

    def get(self, request):
        data = Products.objects.annotate(
            total_revenue=Sum(
                F("orderdetails__quantity") * F("orderdetails__unitprice") - F("orderdetails__discount")
            )
        ).values("id", "name", "total_revenue")

        return Response(convert_response({"ProductTotalRevenue": list(data)}, status_code=200))

# 12. Lấy sản phẩm bán chạy nhất
class ProductBestSeller(APIView):

    def get(self, request):
        data = Products.objects.annotate(
            total_sales=Sum("orderdetails__quantity")
        ).values("id", "name", "total_sales").order_by("-total_sales")[:1]

        return Response(convert_response({"ProductBestSeller": data}, status_code=200))

# 17. Top 5 sản phẩm tạo doanh thu cao nhất
#tính theo sản phẩm, tính daonh thu theo từng sp 
#sắp xếp theo giảm dần -> lấy 5 data đầu tiên 
class Top5ProductRevenue(APIView):
    def get(self, request):
        data = Products.objects.annotate(
            total_revenue=Sum(
                F("orderdetails__quantity") * F("orderdetails__unitprice") - F("orderdetails__discount")
            )
        ).values("id", "product_name", "total_revenue").order_by("-total_revenue")[:5]
        data2 = Products.objects.annotate(
            total_revenue=Sum(
                F("orderdetails__quantity") * F("orderdetails__unitprice") - F("orderdetails__discount")
            )
        ).filter(total_revenue__gt=50000).values("id", "product_name", "total_revenue")
        result = {
            "Top5ProductRevenue": list(data),
            "ProductOver10m" : list(data2)
        }
        return Response(convert_response(result, status_code=200)) 


# 18. Lọc các sản phẩm có doanh thu > 10 triệu
class ProductRevenueOver10M(APIView):
    def get(self, request):
        data = Products.objects.annotate(
            total_revenue=Sum(
                F("orderdetails__quantity") * F("orderdetails__unitprice") - F("orderdetails__discount")
            )
        ).filter(total_revenue__gt=50000).values("id", "product_name", "total_revenue")
        return Response(convert_response(list(data), status_code=200)) 
