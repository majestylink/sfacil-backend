from django.shortcuts import render

from rest_framework.views import APIView

from utilities.response import ApiResponse
from .models import User
from .serializers import UserSerializer


class UsersView(APIView):
    def get(self, request):
        queryset = User.objects.all()
        ser = UserSerializer(queryset, many=True).data
        return ApiResponse(200, data=ser).response()
