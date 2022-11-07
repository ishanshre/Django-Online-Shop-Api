from django.shortcuts import render
from .serializers import ProductSerializer
from .models import Product
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# Create your views here.



@api_view()
def product_list(request):
    query_set = Product.objects.all()
    serializer = ProductSerializer(query_set, many=True)
    return Response(serializer.data)

@api_view()
def product_detail(request, id):
    try:
        query_set = Product.objects.get(pk=id)
        serializer = ProductSerializer(query_set)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
