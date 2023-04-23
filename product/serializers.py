from rest_framework import serializers

from .models import Product, ProductCategory


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        exclude = ('created_at', 'updated_at')


class ProductSerializer(serializers.ModelSerializer):
    product_category = serializers.SerializerMethodField()

    def get_product_category(self, obj):
        return ProductCategorySerializer(obj.product_category).data

    class Meta:
        model = Product
        exclude = ('created_at', 'updated_at')
