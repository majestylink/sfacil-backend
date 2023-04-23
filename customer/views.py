from django.shortcuts import render
from rest_framework.views import APIView
from .models import Customer
from .serializers import CustomerSerializer

from utilities.response import ApiResponse


class CustomerView(APIView):

    def get(self, request):
        customers = Customer.objects.all()
        print(customers)
        ser = CustomerSerializer(customers, many=True)
        print(ser.data)
        data = [
            {
                'id': 'number',
                'name': 'string',
                'address': 'string',
                'phone': 'string',
                'email': 'email',
                'job': 'job',
                'location': 'location',
            },
            {
                'id': 'number 1',
                'name': 'string 1',
                'address': 'string 1',
                'phone': 'string 1',
                'email': 'email 1',
                'job': 'job 1',
                'location': 'location 1',
            }
        ]
        return ApiResponse(200, message='success', data=ser.data).response()
