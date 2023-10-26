from random import randint

from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from purchase.models import Order
from utilities.models_base import Base
from wallet.models import MonnifyAccount


class Customer(Base):
    customer_id = models.CharField(max_length=200, blank=True, null=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    other_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    debt_amount = models.DecimalField(max_digits=12, decimal_places=2, default=4000000)
    remaining_credit = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ['-created_at', '-updated_at']

    def __str__(self):
        return self.first_name

    @staticmethod
    def customer_id_exist(customer_id):
        customers = Customer.objects.filter(customer_id=customer_id)
        if customers.exists():
            return True
        return False

    @staticmethod
    def generate_customer_id():
        customer_id = "".join(["{}".format(randint(1, 9)) for num in range(0, 7)])
        while Customer.customer_id_exist(customer_id):
            customer_id = "".join(["{}".format(randint(1, 9)) for num in range(0, 7)])
        return customer_id

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def can_order(self, total):
        if total <= self.remaining_credit and total <= self.debt_amount:
            return True
        return False


@receiver(pre_save, sender=Customer)
def remaining_credit(sender, instance, **kwargs):
    if not instance.pk:
        instance.remaining_credit = instance.debt_amount


@receiver(post_save, sender=Customer)
def user_setup(sender, instance, created, **kwargs):
    if created:
        try:
            query = MonnifyAccount.objects.get(user=instance)
        except:
            query = None
        if not query:
            import requests
            import json
            import datetime
            import time

            accountReference = instance.first_name + instance.last_name + str(
                int(time.mktime(datetime.datetime.now().timetuple())))
            accountName = instance.first_name + instance.last_name

            data = {
                "accountReference": accountReference,
                "accountName": accountName,
                "contractCode": "8418534685",
                "customerEmail": instance.email,
                "customerName": accountName,
                "getAllAvailableBanks": False,
                "preferredBanks": ["035"],
                "currencyCode": "NGN"
            }

            # BASE_URL = 'https://api.monnify.com/api/v2/bank-transfer/reserved-accounts'
            BASE_URL = 'https://sandbox.monnify.com/api/v2/bank-transfer/reserved-accounts'
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + get_access_token()['responseBody']['accessToken']
            }

            response = requests.post(f"{BASE_URL}", data=json.dumps(data), headers=headers)
            # print(response.status_code)
            # print(response.json())
            MonnifyAccount.objects.create(
                monnify_account_number=response.json()['responseBody']['accounts'][0]['accountNumber'],
                account_reference=response.json()['responseBody']['accountReference'],
                account_name=response.json()['responseBody']['accountName'],
                user=instance,
            )


def get_access_token():
    import requests

    BASE_URL = 'https://sandbox.monnify.com/api/v1/auth/login'
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Basic TUtfVEVTVF81MDkxN1NKU1pXOkhFMk01SEhZSFdFVDhBOVpKVEg5OVZIRTg0V0U0RDE5"
    }

    response = requests.post(f"{BASE_URL}", headers=headers)
    return response.json()
