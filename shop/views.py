from django.shortcuts import render, get_object_or_404
from .serializers import (
    ProductSerializer, 
    ProductImageSerializer,
    CollectionSerializer, 
    ReviewSerializer, 
    CartSerializer, 
    CartItemsSerializer,
    AddCartItemSerializer,
    UpdateCartItemSerializer,
    CustomerSerializer,
    OrderSerializer,
    CreateOrderSerializer,
    UpdateOrderSerializer,
)
from .models import (
    Product, 
    ProductImage,
    Collection, 
    Review, 
    Cart, 
    CartItem,
    Customer,
    Order,
)
# from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly
# from rest_framework.parsers import JSONParser
from django.http import Http404
# from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import mixins
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend # for generic filters
from .filters import ProductFilter # importing custom generic filter
from rest_framework.filters import SearchFilter, OrderingFilter
#from rest_framework.pagination import PageNumberPagination
from .pagination import CustomDefaultPagination
# from rest_framework import mixins
from typing import List

from shop.permissions import IsAdminOrReadOnly, FullDjangoModelPermission
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
    queryset = Product.objects.prefetch_related("images").all()
    serializer_class = ProductSerializer
    # specifying a django filter backend 
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # creating a list named filterset_fields of fileds for filtering
    #filterset_fields = ['collection_id']
    filterset_class = ProductFilter
    search_fields = ['title','description']
    ordering_fields = ['unit_price','last_update']
    #pagination_class = PageNumberPagination # specification pagination class and add no. of items in setting.py
    pagination_class = CustomDefaultPagination
    permission_classes = [IsAdminOrReadOnly]

    
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


class ProductImageViewSet(viewsets.ModelViewSet):
    serializer_class = ProductImageSerializer

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs['product_pk'])

    # product_id is null at this point so we pass product id from get_serializer_context in modelview set
    # We extract product id from the url
    def get_serializer_context(self):
        return {"product_id": self.kwargs["product_pk"]}

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
    permission_classes = [IsAdminOrReadOnly]

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


class CartViewSet(mixins.CreateModelMixin,
                mixins.ListModelMixin, 
                mixins.RetrieveModelMixin, 
                mixins.DestroyModelMixin,
                viewsets.GenericViewSet):
    # using prefetch_related to get all the cartitem with associated products
    queryset = Cart.objects.prefetch_related('cart_items__product').all()
    serializer_class = CartSerializer



class CartItemsViewSet(viewsets.ModelViewSet):
    # http_method_name are the method that client have access to 
    http_method_names = ['get','post','patch','delete']

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer
        if self.request.method == "PATCH":
            return UpdateCartItemSerializer
        return CartItemsSerializer


    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']} # get the cart pk 
    def get_queryset(self):
        # return a cartitem related to cart and optimize product query in cartitem using select related
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')

 

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    #permission_classes = [IsAdminUser]
    permission_classes = [IsAdminOrReadOnly]

    @action(detail=False, methods=['GET','PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        customer = get_object_or_404(Customer, id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

class OrderViewSet(viewsets.ModelViewSet):
    http_method_names: List[str] = ['get', 'post', 'patch','delete','head','options']

    def get_permissions(self):
        if self.request.method in ['PATCH','DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]


    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(
            data = request.data,
            context = {"user_id":request.user.id}
        )
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        seralizer = OrderSerializer(order)
        return Response(serializer.data)
        

    # This method is only used for default create method.
    # # it passes the data to the validated data in serializer
    # def get_serializer_context(self):
    #     return {"user_id": self.request.user.id}

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateOrderSerializer
        elif self.request.method == "PATCH":
            return UpdateOrderSerializer
        return OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Order.objects.all()
        customer_id = Customer.objects.only("id").get(user__id=user.id)
        return Order.objects.filter(customer_id=customer_id)
