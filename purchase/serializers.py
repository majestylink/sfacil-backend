from rest_framework import serializers

from customer.serializers import CustomerSerializer
from product.serializers import ProductSerializer
from .models import Order, OrderedProduct, PerProduct, Invoice


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ('invoice_ref', 'created_at', 'updated_at', 'total_amount')


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
    invoice = serializers.SerializerMethodField()

    def get_customer(self, obj):
        # return CustomerSerializer(obj.customer).data
        # print(obj.customer)
        if obj.customer:
            customer = CustomerSerializer(obj.customer).data
            # first_name = customer['first_name']
            # last_name = customer['last_name']
            # return f"{first_name} {last_name}"
            return customer
        return None

    def get_ordered_products(self, obj):
        # op = OrderedProductSerializer(obj.ordered_products.all(), many=True).data
        # print(obj.ordered_products.all()[0].mattresses.all(), 'line 42')
        return OrderedProductSerializer(obj.ordered_products.all(), many=True).data

    def get_invoice(self, obj):
        try:
            invoice = Invoice.objects.get(order=obj)
            return InvoiceSerializer(invoice).data
        except Invoice.DoesNotExist:
            return None

    class Meta:
        model = Order
        fields = ('name', 'customer', 'fulfilled', 'cost', 'created_at', 'ordered_products', 'invoice', "retail")
