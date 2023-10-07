from rest_framework import serializers

from customer.serializers import CustomerSerializer
from .models import Ledger


class LedgerSerializer(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()

    def get_customer(self, obj):
        print(obj, 'obj')
        return CustomerSerializer(obj.customer).data

    class Meta:
        model = Ledger
        fields = '__all__'
