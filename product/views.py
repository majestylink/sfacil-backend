import re

from django.shortcuts import render
from rest_framework.views import APIView

from .models import Product, ProductCategory, ProductBrand
from utilities.response import ApiResponse
from .serializers import ProductSerializer, ProductCategorySerializer, ProductBrandSerializer


class ProductAPIView(APIView):
    def get(self, request):
        queryset = Product.objects.all()
        ser = ProductSerializer(queryset, many=True).data
        return ApiResponse(200, data=ser).response()

    def post(self, request):
        print(request.data)
        try:
            product_category = request.data.get('product_category', None)
            product_category = ProductCategory.objects.get(id=product_category)
        except:
            return ApiResponse(400, data=[], message="Invalid data entry").response()
        try:
            product_brand = request.data.get('product_brand', None)
            product_brand = ProductBrand.objects.get(id=product_brand)
        except:
            return ApiResponse(400, data=[], message="Invalid data entry").response()
        inches = request.data['inches']
        try:
            dimensions = request.data.get('dimensions', None)
            pattern = r"^\d{2}x\d{2}$"
            if re.match(pattern, dimensions):
                pass
            else:
                return ApiResponse(400, data=[], message="Dimensions should be in this format 00x00").response()
        except:
            return ApiResponse(400, data=[], message="Dimensions should be in this format 00x00").response()
        price = request.data['price']
        current_quantity = request.data.get('current_quantity', 0)
        product, created = Product.objects.get_or_create(
            product_category=product_category,
            price=price,
            dimensions=dimensions,
            inches=inches,
            product_brand=product_brand,
            current_quantity=current_quantity,
        )
        if not created:
            return ApiResponse(400, message="Product already exists").response()
        product.product_id = Product.generate_product_id()
        product.save()
        data = ProductSerializer(product).data
        return ApiResponse(200, data=data, message="Product added successfully").response()


class ProductCategoryView(APIView):
    def get(self, request):
        queryset = ProductCategory.objects.all()
        ser = ProductCategorySerializer(queryset, many=True).data
        return ApiResponse(200, data=ser).response()


class ProductBrandView(APIView):
    def get(self, request):
        queryset = ProductBrand.objects.all()
        ser = ProductBrandSerializer(queryset, many=True).data
        return ApiResponse(200, data=ser).response()
