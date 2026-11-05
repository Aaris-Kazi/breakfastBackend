from rest_framework.serializers import Serializer, CharField, SlugField, URLField, BooleanField, IntegerField, DecimalField
from .models import CategoriesModel, ProductModel
from django.db import transaction

class CategoriesSerializer(Serializer):
    name = CharField(max_length=100)
    slug = SlugField(max_length=100)
    descriptions = CharField(max_length=100, required=False)
    image_urls = URLField(required=False)
    is_active = BooleanField(default=True)

    def create(self, validated_data):
        return CategoriesModel.objects.create(
            **validated_data
        )
class CategoriesUpdateSerializer(Serializer):
    is_active = BooleanField(default=True)

class ProductSerializer(Serializer):
    id = IntegerField(required=False)
    name = CharField(max_length=100)
    slug = SlugField(max_length=100)
    unit = CharField(max_length=100, required=True)
    stock_quantity = IntegerField(required=False)
    category = CharField(max_length=100)
    description = CharField(max_length=100, required=False)
    price = DecimalField(max_digits=10, decimal_places=2, required=False)
    image_urls = URLField(required=False)
    is_active = BooleanField(default=True)

    def create(self, validated_data):
        validated_data['category'] = CategoriesModel.objects.get(
            name=validated_data['category'])
        return ProductModel.objects.create(
            **validated_data
        )

    @transaction.atomic
    def update(self, validated_data):
        stock = validated_data.get('stock_quantity')
        if stock is not None and stock < 0:
            raise ValueError("Stock quantity cannot be negative")
        product = ProductModel.objects.select_for_update().get(
            pk=validated_data['id']
        )
        product.stock_quantity += stock
        product.unit = validated_data.get('unit', product.unit)
        product.price = validated_data.get('price', product.price)
        product.is_active = validated_data.get('is_active', product.is_active)
        product.save()
        
        return product
