from rest_framework import serializers
from django.contrib.auth import authenticate
from account.models import *

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField()

    class Meta:
        model = Account
        fields = ["email", "username", "password"]

        def create(self, validated_data):
            user = Account(
                email = validated_data['email'],
                username = validated_data['username']
            )
            user.set_password(validated_data['password'])
            user.save()
            return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def varidate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Sai tài khoản hoặc mật khẩu")

