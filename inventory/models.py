from django.db import models

from utilities.constants import NOTIFICATION_TYPE
from utilities.models_base import Base


class RawMaterialCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class RawMaterial(Base):
    category = models.ForeignKey(RawMaterialCategory, on_delete=models.PROTECT, blank=True, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    unit_of_measurement = models.CharField(max_length=20)
    reorder_point = models.PositiveIntegerField(default=0)
    supplier = models.ForeignKey('Supplier', on_delete=models.SET_NULL, blank=True, null=True,
                                 related_name='raw_materials')
    current_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class RawMaterialTransaction(Base):
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20, choices=[('purchase', 'Purchase'), ('usage', 'Usage')])
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.ForeignKey('Supplier', on_delete=models.SET_NULL, null=True,
                                 related_name='raw_material_transactions')
    user = models.ForeignKey('account.User', on_delete=models.CASCADE,
                             related_name='raw_material_transactions')

    def __str__(self):
        return f"{self.quantity} {self.transaction_type} of {self.raw_material.name}"


class Supplier(Base):
    name = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return self.name


class Notification(Base):
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='user_notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPE, default='General Notification')

    def __str__(self):
        return self.message


class Accessory(Base):
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class CoverMaterial(Base):
    name = models.CharField(max_length=100)
    pattern = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    texture = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class AccessoryTransaction(Base):
    accessory = models.ForeignKey(Accessory, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20, choices=[('purchase', 'Purchase'), ('usage', 'Usage')])
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='accessory_transactions')


class CoverMaterialTransaction(Base):
    cover_material = models.ForeignKey(CoverMaterial, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20, choices=[('purchase', 'Purchase'), ('usage', 'Usage')])
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='cover_material_transactions')
