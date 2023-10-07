from django.contrib import admin

from product.models import ProductCategory, Product, ProductBrand

admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(ProductBrand)
