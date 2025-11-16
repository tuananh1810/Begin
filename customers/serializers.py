from rest_framework import serializers
from customers.models import Customers


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = ["id", "customer_name", "contact_name", "address", "city", "postal_code", "country"]
    