from rest_framework import serializers
from .models import Product
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

class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
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
        fields = ['id','title','price','price_with_tax', 'created_at','last_update']
