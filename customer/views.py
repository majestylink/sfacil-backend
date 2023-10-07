from django.shortcuts import render
from rest_framework.views import APIView
from .models import Customer
from .serializers import CustomerSerializer

from utilities.response import ApiResponse


class CustomerView(APIView):

    def get(self, request):
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
        print("In put method")
        return ApiResponse(200).response()
