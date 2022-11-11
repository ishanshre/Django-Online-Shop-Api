from django.shortcuts import render
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer
from .models import Product, Collection, Review
# from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.parsers import JSONParser
from django.http import Http404
# from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import viewsets
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend # for generic filters
from .filters import ProductFilter # importing custom generic filter
from rest_framework.filters import SearchFilter, OrderingFilter
# from rest_framework import mixins
# Create your views here.



# @api_view()
# def ProductList(request):
#     query_set = Product.objects.all()
#     serializer = ProductSerializer(query_set, many=True)
#     return Response(serializer.data)

# @api_view(['GET','POST'])
# def ProductList(request, format=None):
#     if request.method == 'GET':
#         query_set = Product.objects.all()
#         serializer = ProductSerializer(query_set, many=True)
#         return Response(serializer.data)
    
#     if request.method == "POST":
#         serializer = ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    

# @api_view(['GET','PUT','DELETE'])
# def ProductDetail(request, pk, format=None):
#     try:
#         #get the object of product item using id
#         query_set = Product.objects.get(pk=pk)
#     except Product.DoesNotExist:
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#     if request.method == 'GET':
#         serializer = ProductSerializer(query_set)#display the product item detail
#         return Response(serializer.data)
#     if request.method == 'PUT':
#         serializer = ProductSerializer(query_set,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     if request.method == 'DELETE':
#         query_set.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class ProductList(APIView):
#     def get(self, request, format=None, *args, **kwargs):   
#         query_set = Product.objects.all() 
#         serializer = ProductSerializer(query_set, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None, *args, **kwargs):
#         query_set = Product.objects.all()
#         serializer = ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ProductDetail(APIView):
#     def get_object(self, pk):
#         try:
#             return Product.objects.get(pk=pk)
#         except Product.DoesNotExist:
#             raise Http404
    
#     def get(self, request, format=None, *args, **kwargs):
#         query_set = self.get_object(kwargs.get('pk'))#pass product item id to get_object method 
#         serializer = ProductSerializer(query_set)
#         return Response(serializer.data)

#     def put(self, request, format=None, *args, **kwargs):
#         query_set = self.get_object(kwargs.get('pk'))
#         serializer = ProductSerializer(query_set, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, *args, **kwargs):
#         query_set =self.get_object(kwargs.get('pk'))
#         query_set.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class ProductList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

# class ProductDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

#     def get(self, request, format=None, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
    
#     def put(self, request, format=None, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
    
#     def delete(self, request, format=None, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

'''
Class based Views
class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.product_orderitems.count() > 0:
            return Response({
                'error':'Product cannot be deleted because it is associated with order items',
            }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().delete(request, *args, **kwargs)

'''

class ProductViewSet(viewsets.ModelViewSet):
    # queryset = Product.objects.all()
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # specifying a django filter backend 
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # creating a list named filterset_fields of fileds for filtering
    #filterset_fields = ['collection_id']
    filterset_class = ProductFilter
    search_fields = ['title','description']
    ordering_fields = ['unit_price','last_update']

    # def get_queryset(self):
    #     queryset = Product.objects.all()#return all product
    #     collection_id = self.request.query_params.get('collection_id')# get the collection_id if given in the query parameters. 
    #     # query_params is a dict that stores parameters in given url
    #     # check collection is None. If Not none return product that has collection_id else return all product
    #     if collection_id is not None:
    #         return queryset.filter(collection_id=collection_id)
    #     return queryset

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.product_orderitems.count() > 0:
            return Response({
                'error':'Product cannot be deleted when more than one product is associated with order items.'
            }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

'''
class CollectionList(generics.ListCreateAPIView):
    queryset = Collection.objects.annotate(products_count=Count('collection_products')).all()
    serializer_class = CollectionSerializer

class CollectionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.annotate(products_count=Count('collection_products')).all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        if self.get_object().collection_products.count() > 0:
            return Response({'error':'collection cannot be deleted when 1 or more products'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
'''

class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('collection_products')).all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.collection_products.count() > 0:
            return Response({
                'error': 'Collection cannot be deleted when it has one or more products'
            }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)



class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])
    

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}# return the prodcut id where we write the review
