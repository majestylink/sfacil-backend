from rest_framework import serializers

from .models import Product, ProductCategory, ProductBrand


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        exclude = ('created_at', 'updated_at')


class ProductBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBrand
        exclude = ('created_at', 'updated_at')


class ProductSerializer(serializers.ModelSerializer):
    product_category = serializers.SerializerMethodField()
    product_brand = serializers.SerializerMethodField()

    def get_product_category(self, obj):
        return ProductCategorySerializer(obj.product_category).data

    def get_product_brand(self, obj):
        return ProductBrandSerializer(obj.product_brand).data

    class Meta:
        model = Product
        exclude = ('created_at', 'updated_at')
