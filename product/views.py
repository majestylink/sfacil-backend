import re

from django.shortcuts import render
from rest_framework.views import APIView

from .models import Product, ProductCategory
from utilities.response import ApiResponse
from .serializers import ProductSerializer


class ProductAPIView(APIView):
    def get(self, request):
        queryset = Product.objects.all()
        ser = ProductSerializer(queryset, many=True).data
        return ApiResponse(200, data=ser).response()

    def post(self, request):
        try:
            product_category = request.data.get('product_category', None)
            product_category = ProductCategory.objects.get(name=product_category)
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
        product, created = Product.objects.get_or_create(
            product_category=product_category,
            price=price,
            dimensions=dimensions,
            inches=inches
        )
        if not created:
            return ApiResponse(400, message="Product already exists").response()
        product.product_id = Product.generate_product_id()
        product.save()
        data = ProductSerializer(product).data
        return ApiResponse(200, data=data, message="Product added successfully").response()
