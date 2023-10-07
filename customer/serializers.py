from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    account_name = serializers.SerializerMethodField()
    account_number = serializers.SerializerMethodField()

    def get_account_name(self, obj):
        try:
            return obj.monnify.account_name
        except:
            return ''

    def get_account_number(self, obj):
        try:
            return obj.monnify.monnify_account_number
        except:
            return ''

    class Meta:
        model = Customer
        fields = "__all__"
