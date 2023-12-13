from django.shortcuts import render
from rest_framework.views import APIView

from utilities.auth import IsInAccountsGroup
from .models import Customer
from .serializers import CustomerSerializer

from utilities.response import ApiResponse


class CustomerView(APIView):
    permission_classes = [IsInAccountsGroup]

    def get(self, request):
        print(request.headers)
        customers = Customer.objects.all()
        ser = CustomerSerializer(customers, many=True)
        return ApiResponse(200, message='success', data=ser.data).response()

    def post(self, request):
        data = request.data
        # data['image'] = data['image'] if data['image'] else None
        serializer = CustomerSerializer(data=data)
        if serializer.is_valid():
            customer_id = Customer.generate_customer_id()
            # debt_amount = request.data.get()
            serializer.save(customer_id=customer_id)
            return ApiResponse(201, data=serializer.data, message="Customer created successfully").response()
        return ApiResponse(200, message=serializer.error_messages).response()

    def put(self, request):
        # print("In put method")
        # print(request.data)
        data = request.data

        try:
            customer_id = data.get('id')

            # Retrieve the existing customer object from the database
            customer = Customer.objects.get(id=customer_id)

            # Update customer fields with data from the request
            customer.first_name = data.get('first_name', customer.first_name)
            customer.last_name = data.get('last_name', customer.last_name)
            customer.email = data.get('email', customer.email)
            customer.phone = data.get('phone', customer.phone)
            customer.address = data.get('address', customer.address)
            customer.debt_amount = data.get('debt_amount', customer.debt_amount)

            customer.save()

            return ApiResponse(200, message="Customer info updated successfully").response()
        except Exception as e:
            return ApiResponse(400, message=f"Error: {e}").response()
