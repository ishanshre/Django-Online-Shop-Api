from rest_framework import serializers
from .models import Product, Collection, Review, Cart, CartItem
from decimal import Decimal
from django.utils.timesince import timesince


# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(max_length=255)
#     slug = serializers.CharField(max_length=255)
#     # we can also have different name field from models and we must define source i.e price links to the unit price
#     price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
#     # calling a method in serializer field
#     price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

#     def calculate_tax(self, product: Product):
#         return product.unit_price * Decimal(1.1)



class CollectionSerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Collection
        fields = ['id','title','products_count']



class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    '''
    Serializing a collection models ID 
    collection = serializers.PrimaryKeyRelatedField(
        queryset = Collection.objects.all()
    )
    '''
    '''
    Serializing a collection models object into string
    collection = serializers.StringRelatedField()
    '''
    '''
    Serializing a collection model object 
    collection = CollectionSerializer()
    '''
    '''
    serializers.HyperLinkRelatedField ---> used to represent the target of the relationship using hyperlink
    collection = serializers.HyperlinkedRelatedField(read_only=True, view_name='shop:collection-detail')
    '''
    collection = serializers.HyperlinkedRelatedField(read_only=True, view_name='shop:collection-detail')


    created_at = serializers.SerializerMethodField(method_name='create_timesince')
    last_update = serializers.SerializerMethodField(method_name='update_timesince')
    
    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
    
    def create_timesince(self, product: Product):
        return timesince(product.created_at)

    def update_timesince(self, product: Product):
        return timesince(product.last_update)

    class Meta:
        model = Product
        fields = ['id','title','price','price_with_tax', 'collection', 'created_at','last_update']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'rating','name','description']


    #overide create method to add product id of page where we write the review
    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)


class SimpleProductSerializer(ProductSerializer):
    class Meta:
        model = Product
        fields = ['id','title','price', 'price_with_tax']


class CartItemsSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    class Meta:
        model = CartItem
        fields = ['id','product', 'quantity']
class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemsSerializer(many=True, source='cart_items', read_only=True)
    total_price = serializers.SerializerMethodField(method_name='get_total_price')


    def get_total_price(self, cart:Cart):
        return sum([item.quantity * item.product.unit_price for item in cart.cart_items.all()])
    class Meta:
        model = Cart
        fields = ['id','items','total_price']
