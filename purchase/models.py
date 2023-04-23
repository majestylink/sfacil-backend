from django.db import models

from customer.models import Base, Customer
from product.models import Product


class PerProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='per_products', null=True)
    quantity = models.PositiveIntegerField(default=0)


class OrderedProduct(Base):
    mattresses = models.ManyToManyField(PerProduct, related_name='ordered_products')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='ordered_products')


class Order(Base):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    fulfilled = models.BooleanField(default=False)
    ordered_products = models.ManyToManyField(OrderedProduct, blank=True)
    cost = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

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


