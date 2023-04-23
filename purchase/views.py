from rest_framework.views import APIView
# from .models import Order, OrderItem, Variant, Product, Size
from customer.models import Customer
from product.models import Product
from .models import PerProduct, OrderedProduct, Order
from .serializers import OrderSerializer
from utilities.response import ApiResponse


class OrderAPIView(APIView):

    def get(self, request, customer_id):
        customer = Customer.objects.get(id=customer_id)
        orders = customer.orders.order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return ApiResponse(200, data=serializer.data).response()

    def post(self, request, *args, **kwargs):
        customer = Customer.objects.get(id=request.data['customer'])
        ordered = []
        total_cost = 0
        for x in request.data["products_id"]:
            product = Product.objects.get(product_id=x[0])
            ordered_product = PerProduct.objects.get_or_create(product=product, quantity=x[1])[0]
            ordered.append(ordered_product)
            total_cost += product.price * x[1]
        ordered_products = OrderedProduct.objects.create(customer=customer)
        ordered_products.mattresses.add(*ordered)
        ordered_products.save()
        order = Order.objects.create(
            customer=customer,
            fulfilled=True,
            cost=total_cost,
        )
        order.ordered_products.add(ordered_products)
        order.save()
        return ApiResponse(200, message='success', data='serializer.data').response()