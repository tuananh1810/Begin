from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token


from .models import Account
from .serializers import RegisterSerializer, LoginSerializer

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