from rest_framework import serializers
from .models import Product, ProductAttribute

class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ('name', 'value')

class ProductSerializer(serializers.ModelSerializer):
    attributes = ProductAttributeSerializer(many=True, read_only=True)
    supplier_name = serializers.CharField(source='supplier.company_name', read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'supplier_name', 'attributes')