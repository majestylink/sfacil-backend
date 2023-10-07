import uuid

from django.db import models
from django.db.models import Q, Sum

from utilities.constants import STATUS_CHOICES, TYPE_CHOICES
from utilities.models_base import Base
from .utils import generate_reference


class MonnifyAccount(Base):
    monnify_account_number = models.CharField(unique=True, blank=True, null=True, max_length=50)
    account_reference = models.CharField(max_length=255, help_text='Your unique reference used to identify this reserved account')
    account_name = models.CharField(max_length=255, null=True)
    currency_code = models.CharField(max_length=255, default="NGN")
    user = models.OneToOneField("customer.Customer", on_delete=models.CASCADE, related_name="monnify")
    bvn = models.CharField(max_length=255, blank=True, null=True)


class InitiatedMonnifyTransaction(Base):
    transaction_reference = models.CharField(max_length=255)
    payment_reference = models.CharField(max_length=255)
    payment_status = models.CharField(max_length=255, default='UNPAID')
    oder_id = models.CharField(max_length=100, null=True, blank=True, default="")
    user = models.ForeignKey('customer.Customer', related_name='initiated_monnify_transaction', on_delete=models.CASCADE)


class UserWallet(Base):
    wallet_id = models.UUIDField(unique=True, default=uuid.uuid4)
    user = models.OneToOneField("customer.Customer", on_delete=models.CASCADE, related_name="wallet")
    currency = models.CharField(max_length=10, default="NGN")

    def __str__(self):
        return self.user.email

    def get_balance(self):
        query = (Q(status="success") | Q(status="processing")) & Q(wallet=self)
        balance = WalletTransaction.objects.filter(query).aggregate(Sum("amount"))
        return balance

    def to_dict(self):
        balance = self.get_balance()["amount__sum"]
        return {
            "wallet_id": self.wallet_id,
            "balance": f"{balance:.2f}" if balance else "0.00",
            "currency": self.currency,
            "currency_symbol": "₦",
        }

    def get_earnings(self):
        total = (
            WalletTransaction.objects.filter(wallet=self, transaction_type="payment")
            .filter(Q(status="success") | Q(status="processing"))
            .aggregate(Sum("amount"))
        )
        return total

    def get_withdrawals(self):
        total = (
            WalletTransaction.objects.filter(wallet=self, transaction_type="withdrawal")
            .filter(Q(status="success") | Q(status="processing"))
            .aggregate(Sum("amount"))
        )
        return total

    def get_transfers(self):
        total = WalletTransaction.objects.filter(
            wallet=self, transaction_type="transfer", status="success"
        ).aggregate(Sum("amount"))
        return total

    def get_deposits(self):
        total = WalletTransaction.objects.filter(
            wallet=self, transaction_type="deposit", status="success"
        ).aggregate(Sum("amount"))
        return total


class WalletTransaction(models.Model):

    transaction_id = models.UUIDField(unique=True, default=uuid.uuid4)
    reference = models.CharField(max_length=15, unique=True, default=generate_reference)
    wallet = models.ForeignKey(UserWallet, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, db_index=True)
    description = models.CharField(max_length=500)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    transaction_type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    extras = models.JSONField(null=True, blank=True)
