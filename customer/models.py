from random import randint

from django.db import models


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Customer(Base):
    customer_id = models.CharField(max_length=200, blank=True, null=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    other_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    image = models.FileField(upload_to='customers', blank=True, null=True)

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
