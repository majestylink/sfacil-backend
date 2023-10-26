from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView

from customer.models import Customer
from transaction.models import Ledger
from transaction.serializers import LedgerSerializer
from utilities.response import ApiResponse


class TransactionView(APIView):
    def get(self, request, transaction_id=None):
        try:
            if transaction_id is not None:
                transaction = self.get_object(transaction_id)
                serializer = LedgerSerializer(transaction)
                return ApiResponse(200, message='success', data=serializer.data).response()
            else:
                transactions = Ledger.objects.all()
                serializer = LedgerSerializer(transactions, many=True)
                return ApiResponse(200, message='success', data=serializer.data).response()
        except:
            return ApiResponse(404, errors="Transaction not found.").response()

    def post(self, request):
        try:
            data = request.data
            try:
                customer = Customer.objects.get(id=int(data.get('customer')))
            except:
                return ApiResponse(404, errors="Customer not found.").response()
            ledger = Ledger.objects.create(
                customer=customer,
                description=data.get('description', ''),
                amount=data.get('amount'),
                transaction_type=data.get('transaction_type')
            )
            customer.remaining_credit += ledger.amount
            customer.save()
            serializer = LedgerSerializer(ledger)
            return ApiResponse(201, data=serializer.data, message="Transaction added successfully").response()
        except:
            return ApiResponse(400, message="An error occurred").response()

    def put(self, request, transaction_id):
        transaction = self.get_object(transaction_id)
        serializer = LedgerSerializer(transaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ApiResponse(200, data=serializer.data).response()
        return ApiResponse(400, errors=serializer.errors).response()

    def delete(self, request, transaction_id):
        transaction = self.get_object(transaction_id)
        transaction.delete()
        return ApiResponse(200, message='Deleted').response()

    def get_object(self, transaction_id):
        try:
            return Ledger.objects.get(transaction_id=transaction_id)
        except Ledger.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
