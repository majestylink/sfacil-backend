from django.db import models

from product.models import Product
from utilities.invoice_ref import generate_invoice_ref
from utilities.models_base import Base


class PerProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='per_products', null=True)
    quantity = models.PositiveIntegerField(default=0)


class OrderedProduct(Base):
    mattresses = models.ManyToManyField(PerProduct, related_name='ordered_products')
    customer = models.ForeignKey('customer.Customer', on_delete=models.CASCADE, related_name='ordered_products', blank=True, null=True)


class Order(Base):
    name = models.CharField(max_length=255, blank=True, null=True)
    customer = models.ForeignKey('customer.Customer', on_delete=models.CASCADE, related_name='orders', blank=True, null=True)
    fulfilled = models.BooleanField(default=False)
    ordered_products = models.ManyToManyField(OrderedProduct, blank=True)
    cost = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    retail = models.BooleanField(default=False)

    def calculate_cost(self):
        total_cost = 0
        for ordered_product in self.ordered_products.all():
            for per_product in ordered_product.mattresses.all():
                total_cost += per_product.product.price * per_product.quantity
        return total_cost

    def save(self, *args, **kwargs):
        if not self.cost:
            self.cost = self.calculate_cost()
        super(Order, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-updated_at"]


class Invoice(Base):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    invoice_ref = models.CharField(max_length=50, unique=True, default=generate_invoice_ref)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.invoice_ref


