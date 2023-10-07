from rest_framework import serializers

from account.serializers import UserSerializer
from .models import RawMaterialCategory, RawMaterial, RawMaterialTransaction, Supplier, Accessory, CoverMaterial, \
    AccessoryTransaction, CoverMaterialTransaction


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'


class RawMaterialCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RawMaterialCategory
        fields = '__all__'


class RawMaterialSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    supplier = serializers.SerializerMethodField()

    def get_category(self, obj):
        try:
            category = RawMaterialCategory.objects.get(id=obj.category.id)
            return RawMaterialCategorySerializer(category).data
        except:
            return ""

    def get_supplier(self, obj):
        try:
            supplier = Supplier.objects.get(id=obj.supplier.id)
            return SupplierSerializer(supplier).data
        except:
            return ""

    class Meta:
        model = RawMaterial
        fields = '__all__'


class RawMaterialTransactionSerializer(serializers.ModelSerializer):
    raw_material = serializers.SerializerMethodField()

    def get_raw_material(self, obj):
        raw_material = RawMaterial.objects.get(id=obj.raw_material.id)
        return RawMaterialSerializer(raw_material).data

    class Meta:
        model = RawMaterialTransaction
        exclude = ('supplier', 'user',)


class AccessorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Accessory
        fields = "__all__"


class CoverMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoverMaterial
        fields = "__all__"


class AccessoryTransactionSerializer(serializers.ModelSerializer):
    accessory = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    def get_accessory(self, obj):
        return AccessorySerializer(obj.accessory).data

    def get_user(self, obj):
        return UserSerializer(obj.user).data

    class Meta:
        model = AccessoryTransaction
        fields = '__all__'


class CoverMaterialTransactionSerializer(serializers.ModelSerializer):
    cover_material = serializers.SerializerMethodField()

    def get_cover_material(self, obj):
        return CoverMaterialSerializer(obj.cover_material).data

    class Meta:
        model = CoverMaterialTransaction
        fields = '__all__'
