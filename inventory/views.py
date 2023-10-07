from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from account.models import User
from utilities.response import ApiResponse
from .models import RawMaterialCategory, RawMaterial, RawMaterialTransaction, Supplier, Accessory, CoverMaterial, \
    AccessoryTransaction, CoverMaterialTransaction
from .serializers import RawMaterialCategorySerializer, RawMaterialSerializer, RawMaterialTransactionSerializer, \
    SupplierSerializer, AccessorySerializer, CoverMaterialSerializer, AccessoryTransactionSerializer, \
    CoverMaterialTransactionSerializer


class RawMaterialCategoryAPIView(APIView):
    def get(self, request):
        categories = RawMaterialCategory.objects.all()
        serializer = RawMaterialCategorySerializer(categories, many=True)
        return ApiResponse(200, data=serializer.data).response()

    def post(self, request):
        serializer = RawMaterialCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RawMaterialCategoryAPIView(APIView):
    def get(self, request):
        categories = RawMaterialCategory.objects.all()
        serializer = RawMaterialCategorySerializer(categories, many=True)
        return ApiResponse(200, data=serializer.data).response()

    def post(self, request):
        serializer = RawMaterialCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RawMaterialAPIView(APIView):
    def get(self, request):
        raw_materials = RawMaterial.objects.all()
        serializer = RawMaterialSerializer(raw_materials, many=True)
        return ApiResponse(200, data=serializer.data).response()

    def post(self, request):
        try:
            data = request.data
            category = RawMaterialCategory.objects.get(id=data['category'])
            rm = RawMaterial.objects.create(
                category=category,
                name=data['name'],
                description=data['description'],
                unit_of_measurement=data['unitOfMeasurement'],
                reorder_point=data['reorder_point'],
                current_quantity=data['current_quantity']
            )
            serializer = RawMaterialSerializer(rm)
            return ApiResponse(201, data=serializer.data).response()
        except:
            return ApiResponse(400, message="Invalid request").response()


class RawMaterialTransactionAPIView(APIView):
    def get(self, request):
        transactions = RawMaterialTransaction.objects.all()
        serializer = RawMaterialTransactionSerializer(transactions, many=True)
        return ApiResponse(200, data=serializer.data).response()

    def post(self, request):
        data = request.data
        try:
            cost_per_unit = RawMaterialTransaction.objects.filter(transaction_type="purchase")
            cost_per_unit = cost_per_unit.last().cost_per_unit
        except:
            return ApiResponse(400, message="Record for this material does not exist yet").response()
        try:
            try:
                raw_mat = RawMaterial.objects.get(id=data['rawMaterial'])
            except:
                return ApiResponse(404, message="Raw material not found").response()
            try:
                user = User.objects.get(id=data['user'])
            except:
                return ApiResponse(404, message="User not found").response()
            raw_mat_trn = RawMaterialTransaction.objects.create(
                raw_material=raw_mat,
                transaction_type='Usage',
                quantity=data['quantity'],
                cost_per_unit=cost_per_unit,
                user=user
            )
            ser = RawMaterialTransactionSerializer(raw_mat_trn).data
            return ApiResponse(201, data=ser, message="Raw material transaction created").response()
        except:
            return ApiResponse(400, message="Unable to create raw material transaction").response()


class AccessoryTransactionAPIView(APIView):
    def get(self, request):
        transactions = AccessoryTransaction.objects.all()
        serializer = AccessoryTransactionSerializer(transactions, many=True)
        return ApiResponse(200, data=serializer.data).response()

    def post(self, request):
        data = request.data
        try:
            cost_per_unit = AccessoryTransaction.objects.filter(transaction_type="purchase")
            cost_per_unit = cost_per_unit.last().cost_per_unit
        except:
            return ApiResponse(400, message="Record for this material does not exist yet").response()
        try:
            try:
                accessory = Accessory.objects.get(id=data['accessory'])
            except:
                return ApiResponse(404, message="Accessory not found").response()
            try:
                user = User.objects.get(id=data['user'])
            except:
                return ApiResponse(404, message="User not found").response()
            accessory_trn = AccessoryTransaction.objects.create(
                accessory=accessory,
                transaction_type='Usage',
                quantity=data['quantity'],
                cost_per_unit=cost_per_unit,
                user=user
            )
            ser = AccessoryTransactionSerializer(accessory_trn).data
            return ApiResponse(201, data=ser, message="Accessory transaction created").response()
        except:
            return ApiResponse(400, message="Unable to create accessory transaction").response()


class CoverMaterialsTransactionAPIView(APIView):
    def get(self, request):
        transactions = CoverMaterialTransaction.objects.all()
        serializer = CoverMaterialTransactionSerializer(transactions, many=True)
        return ApiResponse(200, data=serializer.data).response()

    def post(self, request):
        data = request.data
        print(data)
        try:
            cost_per_unit = CoverMaterialTransaction.objects.filter(transaction_type="purchase")
            cost_per_unit = cost_per_unit.last().cost_per_unit
            print("Line 149", cost_per_unit)
        except:
            return ApiResponse(400, message="Record for this material does not exist yet").response()
        try:
            try:
                cover_mat = CoverMaterial.objects.get(id=data['coverMaterial'])
            except:
                return ApiResponse(404, message="Cover material not found").response()
            try:
                user = User.objects.get(id=data['user'])
            except:
                return ApiResponse(404, message="User not found").response()
            cover_mat_trn = CoverMaterialTransaction.objects.create(
                cover_material=cover_mat,
                transaction_type='Usage',
                quantity=data['quantity'],
                cost_per_unit=cost_per_unit,
                user=user
            )
            ser = CoverMaterialTransactionSerializer(cover_mat_trn).data
            return ApiResponse(201, data=ser, message="Cover material transaction created").response()
        except:
            return ApiResponse(400, message="Unable to create cover material transaction").response()


class SupplierAPIView(APIView):
    def get(self, request):
        transactions = Supplier.objects.all()
        serializer = SupplierSerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SupplierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccessoryAPIView(APIView):
    def get(self, request):
        accessory = Accessory.objects.all()
        serializer = AccessorySerializer(accessory, many=True)
        return ApiResponse(200, data=serializer.data).response()

    def post(self, request):
        serializer = AccessorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ApiResponse(201, data=serializer.data).response()
        return ApiResponse(400, errors=serializer.errors).response()


class CoverMaterialAPIView(APIView):
    def get(self, request):
        cover_material = CoverMaterial.objects.all()
        serializer = CoverMaterialSerializer(cover_material, many=True)
        return ApiResponse(200, data=serializer.data).response()

    def post(self, request):
        serializer = CoverMaterialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ApiResponse(201, data=serializer.data).response()
        return ApiResponse(400, errors=serializer.errors).response()
