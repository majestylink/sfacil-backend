from rest_framework import serializers

from customer.serializers import CustomerSerializer
from product.serializers import ProductSerializer
from .models import Order, OrderedProduct, PerProduct


class PerProductSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    def get_product(self, obj):
        return ProductSerializer(obj.product).data

    class Meta:
        model = PerProduct
        fields = '__all__'


class OrderedProductSerializer(serializers.ModelSerializer):
    mattresses = serializers.SerializerMethodField()

    def get_mattresses(self, obj):
        return PerProductSerializer(obj.mattresses.all(), many=True).data
        # return ""

    class Meta:
        model = OrderedProduct
        fields = ('mattresses',)


class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()
    ordered_products = serializers.SerializerMethodField()

    def get_customer(self, obj):
        # return CustomerSerializer(obj.customer).data
        customer = CustomerSerializer(obj.customer).data
        first_name = customer['first_name']
        last_name = customer['last_name']
        return f"{first_name} {last_name}"

    def get_ordered_products(self, obj):
        # op = OrderedProductSerializer(obj.ordered_products.all(), many=True).data
        # print(obj.ordered_products.all()[0].mattresses.all(), 'line 42')
        return OrderedProductSerializer(obj.ordered_products.all(), many=True).data

    class Meta:
        model = Order
        fields = ('customer', 'fulfilled', 'cost', 'created_at', 'ordered_products')
