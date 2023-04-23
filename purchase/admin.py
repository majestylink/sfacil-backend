from django.contrib import admin

from .models import Order, OrderedProduct, PerProduct


admin.site.register(PerProduct)
admin.site.register(Order)
admin.site.register(OrderedProduct)
