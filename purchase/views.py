from collections import defaultdict
from datetime import date, datetime
from decimal import Decimal

from django.db.models import Prefetch
from django.db.models.functions import TruncMonth, TruncYear
from rest_framework.views import APIView
# from .models import Order, OrderItem, Variant, Product, Size
from customer.models import Customer
from transaction.models import Ledger
from .serializers import CustomerSerializer
from product.models import Product
from .models import PerProduct, OrderedProduct, Order, Invoice
from .serializers import OrderSerializer
from utilities.response import ApiResponse


class PurchaseIndexView(APIView):
    def get(self, request):
        queryset = Order.objects.all()
        ser = OrderSerializer(queryset, many=True).data
        return ApiResponse(200, data=ser).response()


class DistributorOrderAPIView(APIView):

    def get(self, request, customer_id):
        customer = Customer.objects.get(id=customer_id)
        orders = customer.orders.order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        data = {
            'customer': CustomerSerializer(customer).data,
            'orders': serializer.data
        }
        # print(data)
        return ApiResponse(200, data=data).response()

    def post(self, request, *args, **kwargs):
        customer_id = request.data.get('customer')
        products_data = request.data.get('products', [])

        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return ApiResponse(400, message='Customer not found').response()

        ordered = []
        total_cost = 0

        for product_data in products_data:
            selected_product_id = product_data.get('selectedProduct')
            quantity = product_data.get('quantity')

            try:
                product = Product.objects.get(id=selected_product_id)
                ordered_product, created = PerProduct.objects.get_or_create(
                    product=product, quantity=quantity
                )
                ordered.append(ordered_product)
                total_cost += product.price * quantity
            except Product.DoesNotExist:
                return ApiResponse(400, message=f'Product with ID {selected_product_id} not found').response()

        if customer.can_order(total_cost):
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
            data = OrderSerializer(order).data

            print(customer.remaining_credit)
            customer.remaining_credit -= order.cost
            print(customer.remaining_credit)
            customer.save()

            ledger = Ledger.objects.create(
                customer=customer,
                description=data.get(f'New order from {customer.first_name} {customer.last_name}'),
                amount=total_cost,
                transaction_type='debit'
            )

            return ApiResponse(200, message='Order created successfully', data=data).response()
        else:
            return ApiResponse(400, message="Amount is above customer's credit unit").response()


class RetailOrderAPIView(APIView):
    def get(self, request, customer_id=None):
        orders = Order.objects.filter(retail=True).order_by('-created_at')

        serializer = OrderSerializer(orders, many=True)

        return ApiResponse(200, data=serializer.data).response()

    def post(self, request):
        ordered = []
        total_cost = 0
        for x in request.data["products"]:
            product = Product.objects.get(product_id=x['product_id'])
            ordered_product = PerProduct.objects.get_or_create(
                product=product, quantity=x['quantity']
            )[0]
            ordered.append(ordered_product)
            total_cost += product.price * x['quantity']

        ordered_products = OrderedProduct.objects.create()
        ordered_products.mattresses.add(*ordered)
        ordered_products.save()
        order = Order.objects.create(
            name=request.data["customerName"],
            fulfilled=True,
            cost=total_cost,
            retail=True
        )
        order.ordered_products.add(ordered_products)
        order.save()

        invoice = Invoice.objects.create(
            order=order,
            total_amount=total_cost,
        )
        data = OrderSerializer(order).data
        return ApiResponse(200, message='success', data=data).response()


class EarningsView(APIView):
    def get(self, request):
        current_month = datetime.now().month
        current_year = datetime.now().year

        monthly_earnings = defaultdict(Decimal)  # Initialize as Decimal
        annual_earnings = defaultdict(Decimal)  # Initialize as Decimal

        filtered_orders = Order.objects.annotate(month=TruncMonth('created_at')).annotate(year=TruncYear('created_at'))

        for order in filtered_orders:
            month = order.created_at.month
            year = order.created_at.year
            earnings = order.calculate_cost()
            monthly_earnings[month] += Decimal(str(earnings))  # Convert earnings to Decimal
            annual_earnings[year] += Decimal(str(earnings))  # Convert earnings to Decimal

        data = {
            'monthly_earnings': float(monthly_earnings[current_month]),  # Convert to float
            'annual_earnings': float(annual_earnings[current_year]),  # Convert to float
        }
        return ApiResponse(200, message='success', data=data).response()
