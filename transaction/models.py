import uuid
from random import randint

from django.db import models

from customer.models import Customer
from utilities.models_base import Base


class Ledger(Base):
    TRANSACTION_TYPES = [
        ('debit', 'Debit'),
        ('credit', 'Credit'),
    ]

    customer = models.ForeignKey('customer.Customer', on_delete=models.SET_NULL, blank=True, null=True)
    transaction_id = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)

    class Meta:
        ordering = ['-updated_at']

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = Ledger.generate_transaction_id()
        super().save(*args, **kwargs)

    @staticmethod
    def transaction_id_exist(transaction_id):
        transaction = Ledger.objects.filter(transaction_id=transaction_id)
        if transaction.exists():
            return True
        return False

    @staticmethod
    def generate_transaction_id():
        transaction_id = "".join(["{}".format(randint(1, 9)) for num in range(0, 7)])
        while Ledger.transaction_id_exist(transaction_id):
            transaction_id = "".join(["{}".format(randint(1, 9)) for num in range(0, 7)])
        return transaction_id


class Expense(Base):
    EXPENSE_CATEGORIES = [
        ('raw_materials', 'Raw Materials'),
        ('utilities', 'Utilities'),
        ('salaries', 'Employee Salaries'),
        ('other', 'Other'),
    ]
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='user_expenses')
    category = models.CharField(max_length=20, choices=EXPENSE_CATEGORIES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    supporting_document = models.FileField(upload_to='expense_documents/', blank=True, null=True)
    # Add more fields as needed

