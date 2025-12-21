from rest_framework import serializers
from customers.models import Customers
from account.serializers import *


class CustomerSerializer(serializers.ModelSerializer):
    user_created_data = AccountSerializerView(source="user_created", read_only=True)
    class Meta:
        model = Customers
        fields = ["id", "customer_name", "contact_name", "address", "city",
                   "postal_code", "country", "nhom_khach_hang", "gender", 
                   "birthday", "type_customer", "user_created","user_created_data","code","created_at","updated_at", "phone", "email"]
    def create(self, validated_data):
        user = self.context["user"]
        validated_data["user_created"] = user
        code = validated_data.get("code")
        if not code:
            count = Customers.objects.count()
            validated_data["code"] =  f"KH{str(count + 1)}"
        return super().create(validated_data)
# a= {
#   "user_name": "haohao",
#   "pass": "1234"
# }
# user_name = a.get("user_name"``)