from django.shortcuts import render
from customers.models import Customers
from customers.serializers import CustomerSerializer
from django.http import Http404
from account.models import *
from django.db.models import Sum, Count, F, Q
from orders.models import Orderdetails
from general import convert_response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models.functions import Coalesce
from django.db.models import Subquery, OuterRef, Max, Avg, Value, IntegerField, CharField, FloatField, Case, When
from handle import Paginate


class CustomersList(APIView):
    
    #Hiển thị thêm thông tin của user_created và tìm kiếm theo mã khách hàng, tên khách hàng, sdt(phone) khách hàng và tên nhân viên (user_created)
    #Thêm bộ lọc theo ngày sinh(birthday) gợi ý: dùng filter Birthday > -> gte(lớn hơn hoặc bằng), lte(nhỏ hơn hoặc bằng)
    #thêm bộ lọc theo (user_created) filter thêm điều kiện
    """
    List all customners, or create a new customer.
    """
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        customers = Customers.objects.all()
        user_created = request.query_params.get("user_created")
        search = request.query_params.get("search")
        bd_from = request.query_params.get("birthday_from")
        bd_to = request.query_params.get("birthday_to")
        if bd_from and bd_to:
            customers = customers.filter(birthday__gte=bd_from, birthday__lte=bd_to)
        if user_created:
            customers = customers.filter(user_created_id=user_created)
        if search:
            customers = customers.filter(
                Q(customer_name__icontains=search) |
                Q(phone__icontains=search) |
                Q(user_created__username__icontains=search) |
                Q(code__icontains=search)
        )
        customers = Paginate(customers, request.GET)
        serializer = CustomerSerializer(customers, many=True)
        return Response(convert_response("Success", 200, serializer.data))
    # tự động sinh mã khách hàng nếu người dùng ko nhập vào theo công thức: KH-số thứ tự khách hàng trong hệ thống
    def post(self, request, format=None):
        serializer = CustomerSerializer(data=request.data, context={"user": request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''Yêu cầu trong màn chi tiết khách hàng:
1. Trong api chi tiết khách hàng(get detail) Bổ sung thông tin:
- Thông tin người tạo (user_created_data) bao gồm thông tin: tên, số điện thoại, mã 
- Doanh số khách hàng(revenua)
- Tổng số lượng đơn hàng (total_order)
- Thông tin cấp độ khách hàng(level_customer)
* revenua  từ 0 - 1 triệu thì level_customer: Đồng
* revenua  từ 1 - 10 triệu thì level_customer: Bạc
* revenua  từ 10- 100 triệu thì level_customer: Vàng
* revenua  từ 100- 500 triệu thì level_customer: Kim cương
* revenua  > 500  triệu thì level_customer: Ruby
2. Cũng trong màn chi tiết khách hàng , Viết thêm API danh sách đơn hàng của khách hàng đó, bao gồm các thông tin: Mã đơn hàng(code), ngày tạo(created_at), tổng tiền(total), trạng thái đơn hàng(đã xác nhận, chờ xác nhận, …)
- Thêm bộ lọc Theo thời gian tạo(created_at) 
- tìm kiếm đơn hàng: theo mã đơn hàng
chưa làm xong
'''

class CustomerDetail(APIView):
    """
    Retrieve, update or delete a customer instance with extra info.
    """
    def get_object(self, pk):
        try:
            return Customers.objects.get(pk=pk)
        except Customers.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        customer = self.get_object(pk)
        serializer = CustomerSerializer(customer)
        # Thông tin người tạo
        user_created = getattr(customer, 'user_created', None)
        user_created_data = None
        if user_created:
            user_created_data = {
                "name": getattr(user_created, "username", ""),
                "phone": getattr(user_created, "phone", ""),
                "code": getattr(user_created, "code", ""),
            }
        # Doanh số khách hàng
        # Doanh số khách hàng (revenua)
        revenua = Orderdetails.objects.filter(
            order__customer=customer
        ).aggregate(
            total=Coalesce(
                Sum(F("quantity") * F("unitprice"), output_field=FloatField()),
                0.0
            )
        )["total"] or 0
        # Tổng số lượng đơn hàng
        total_order = customer.orders_set.count()
        # Cấp độ khách hàng
        if revenua <= 1000000:
            level_customer = "Đồng"
        elif revenua <= 10000000:
            level_customer = "Bạc"
        elif revenua <= 100000000:
            level_customer = "Vàng"
        elif revenua <= 500000000:
            level_customer = "Kim cương"
        else:
            level_customer = "Ruby"
        data = serializer.data
        data.update({
            "user_created_data": user_created_data,
            "revenua": revenua,
            "total_order": total_order,
            "level_customer": level_customer,
        })
        return Response(convert_response("Success", 200, data))

    def put(self, request, pk, format=None):
        customer = self.get_object(pk)
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(convert_response("Success", 200, serializer.data))
        return Response(convert_response("Error", 400, serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        customer = self.get_object(pk)
        customer.delete()
        return Response(convert_response("Deleted", 204, {}), status=status.HTTP_204_NO_CONTENT)

# 8. Khách hàng đã mua bao nhiêu đơn hàng
class CustomerOrderCount(APIView):

    def get(self, request):
        data = Customers.objects.annotate(
            total_orders=Count("orders")
        ).values("id", "name", "total_orders")
        return Response(convert_response({"CustomerOrderCount": list(data)}, status_code=200))

# 9. Khách hàng đã tiêu bao nhiêu tiền
class CustomerTotalSpent(APIView):

    def get(self, request):
        data = Customers.objects.annotate(
            total_spent=Sum("orders__total")
        ).values("id", "name", "total_spent")
        return Response(convert_response({"CustomerTotalSpent": list(data)}, status_code=200))
    
# TRong api báo cáo khách hàng trả lại thông tin: id khách hàn, mã khách hàng, tên khách hàng, ngày tạo, hoanh số, trung bình đơn, giá trị hàng lớn nhất, sản phẩm mua nhiều nhất, sản phẩm giá trị cao nhất, số lượng sản phẩm đã mua, tìm kiếm theo tên và mã khách hàng
# Bộ lọc : 
# lọc theo id khách hàng (từ cao đến thấp và thấp đến cao)
# lọc theo doanh số (từ cao đến thấp và thấp đến cao)
# nếu có dữ liệu -> phân trang

# 10. Báo cáo tổng hợp khách hàng
class CustomerReport(APIView):
    def get(self, request):  # Hàm mới: API trả về báo cáo tổng hợp khách hàng

        # Lấy tham số lọc và sắp xếp
        search = request.GET.get('search', '')
        sort_by = request.GET.get('sort_by', 'id')
        order = request.GET.get('order', 'desc')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))

        customers = Customers.objects.all()

        # Tìm kiếm theo tên hoặc mã khách hàng
        if search:
            customers = customers.filter(
                Q(name__icontains=search) | Q(code__icontains=search)
            )

        customers = customers.annotate(
            total_sales=Coalesce(Sum("orders__total"), 0),
            avg_sales=Coalesce(Avg("orders__total"), 0),
            max_order_value=Coalesce(Max("orders__total"), 0),
            total_products=Coalesce(Sum("orders__orderdetails__quantity"), 0),
            created_at=F("created_at"),
        )

        # Sản phẩm được mua nhiều nhất
        most_bought_product = Orderdetails.objects.filter(
            order__customer=OuterRef('pk')
        ).values('product__name').annotate(
            total_qty=Sum('quantity')
        ).order_by('-total_qty').values('product__name')[:1]

        # Sản phẩm giá trị cao nhất đã mua
        highest_value_product = Orderdetails.objects.filter(
            order__customer=OuterRef('pk')
        ).annotate(
            total_value=F('quantity') * F('price')
        ).order_by('-total_value').values('product__name')[:1]

        customers = customers.annotate(
            most_bought_product=Subquery(most_bought_product, output_field=CharField()),
            highest_value_product=Subquery(highest_value_product, output_field=CharField()),
        )

        # Sắp xếp
        if sort_by in ['id', 'total_sales']:
            if order == 'desc':
                sort_by = '-' + sort_by
            customers = customers.order_by(sort_by)

        # Phân trang
        total = customers.count()
        start = (page - 1) * page_size
        end = start + page_size
        customers = customers[start:end]

        # Chuẩn bị dữ liệu trả về
        data = []
        for c in customers:
            data.append({
                "id": c.id,
                "code": c.code,
                "name": c.name,
                "created_at": c.created_at,
                "total_sales": c.total_sales,
                "avg_sales": c.avg_sales,
                "max_order_value": c.max_order_value,
                "most_bought_product": c.most_bought_product,
                "highest_value_product": c.highest_value_product,
                "total_products": c.total_products,
            })

        return Response(convert_response({
            "CustomerReport": data,
            "total": total,
            "page": page,
            "page_size": page_size
        }, status_code=200))


