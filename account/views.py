from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from django.db.models import F, Sum, Count, Min, Max, Avg, Q
from general import convert_response
from handle import Paginate
from account.serializers import AccountSerializerView
from account.models import Account
from .serializers import RegisterSerializer, LoginSerializer, StaffSerializer
from orders.models import Orders
from django.http import Http404

# Create your views here.
class RegisterAPI(generics.CreateAPIView):
    
    queryset = Account.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class LoginAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user1 = serializer.validated_data
            print(user1)
            username_ss = user1["username"]
            users = Account.objects.get(username = username_ss) 
            token, created = Token.objects.get_or_create(user=users)
            return Response({
                "token": token.key,
                "username": users.username,
                # "email": users.email
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AccountList(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        account_data = Account.objects.all()
        accounts = Paginate(account_data, request.GET)
        serializer = AccountSerializerView(accounts, many=True)
        return Response(serializer.data)

class StaffView(APIView):
    permission_classes = [IsAuthenticated]
    # Lọc theo trạng thái is_active, mã nhân viên (code), tên nhân viên (full_name), và search giống view trong products
    def get(self, request): 
        staff_list = Account.objects.filter(system__code="STAFF")
        is_active = request.query_params.get("is_active")
        # code = request.query_params.get("code")
        # full_name = request.query_params.get("full_name")
        search = request.query_params.get("search")

        if is_active is not None:
            staff_list = staff_list.filter(is_active=is_active in ["true", "True",  "1", "False", "false", "0"]) #truyền active = true hay false đều lọc dc 
        if search:
            staff_list = staff_list.filter(
                Q(full_name__icontains=search) |
                Q(phone__icontains=search) |
                Q(code__icontains=search)
            )
        staff_list = Paginate(staff_list, request.GET)
        serializer = StaffSerializer(staff_list, many=True)
        return Response(convert_response("Success", 200, serializer.data))
    
    
    def post(self, request):
        user = request.user
        if user.system.code != "ADMIN":
            return Response(convert_response("Bạn không có quyền hạn",400))
        data = request.data
        data["user_created"]= user.id

        serializer = StaffSerializer(data = data)
        if not serializer.is_valid():
            return Response(convert_response("Fail",400, serializer.errors))
        
        serializer.save()
        return Response(convert_response("Success",200, serializer.data))
    
# API Nhân viên bổ xung 
class StaffDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Account.objects.get(pk=pk)
        except Account.DoesNotExist:
            return Response(convert_response("Không tìm thấy nhân viên", 404), status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        staff = self.get_object(pk)
        serializer = StaffSerializer(staff)
        return Response(convert_response("Success", 200, serializer.data))

    def put(self, request, pk, format=None):
        staff = self.get_object(pk)
        serializer = StaffSerializer(staff, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(convert_response("Cập nhật thành công", 200, serializer.data))
        return Response(convert_response("Cập nhật thất bại", 400, serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        staff = self.get_object(pk)
        staff.delete()
        return Response(convert_response("Xóa thành công", 204), status=status.HTTP_204_NO_CONTENT)

"""
{
"is_active": True
}

"""
# API  vô hiệu hóa nhân viên
class UpdateStatusStaff(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk, format=None):
        is_active = request.data.get("is_active", True)
        user = request.user
        if user.system.code != "ADMIN":
            return Response(convert_response("Bạn không có quyền hạn", 400))
        try:
            staff = Account.objects.get(pk=pk, system__code="STAFF")
        except Account.DoesNotExist:
            return Response(convert_response("Không tìm thấy nhân viên", 404), status=status.HTTP_404_NOT_FOUND)
        staff.is_active = is_active
        staff.save()
        return Response(convert_response("Thành công", 200))
        