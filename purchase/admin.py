from django.contrib import admin

from .models import Order, OrderedProduct, PerProduct, Invoice

admin.site.register(PerProduct)
admin.site.register(Order)
admin.site.register(OrderedProduct)
admin.site.register(Invoice)
