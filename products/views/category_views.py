from django.shortcuts import render
from products.models import Categories
from products.serializers import CategorySerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class CategoryList(APIView):
    """
    List all customners, or create a new customer.
    """

    def get(self, request, format=None):
        categories = Categories.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get_object(self, pk):
        try:
            return Categories.objects.get(pk=pk)
        except Categories.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        categories = self.get_object(pk)
        serializer = CategorySerializer(categories)
        return Response(serializer.data)

    def put(self, request, pk, format=None):

        categories = self.get_object(pk)
        serializer = CategorySerializer(categories, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        categories = self.get_object(pk)
        categories.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)