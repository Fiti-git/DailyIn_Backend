from rest_framework import serializers
from .models import Product, Stock


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'Itcode', 'ItDesc', 'RackNo', 'barcode', 'created_at', 'updated_at']

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id', 'product', 'outlet', 'quantity']

