from random import randint

from django.db import models

from customer.models import Base


class ProductCategory(Base):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Product(Base):
    product_id = models.CharField(max_length=200, blank=True, null=True)
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products', null=True)
    inches = models.CharField(max_length=3)
    dimensions = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self) -> str:
        return f'{self.inches} inches - {self.dimensions} => {self.product_category.name}'


    @staticmethod
    def product_id_exist(product_id):
        products = Product.objects.filter(product_id=product_id)
        if products.exists():
            return True
        return False

    @staticmethod
    def generate_product_id():
        product_id = "".join(["{}".format(randint(1, 9)) for num in range(0, 7)])
        while Product.product_id_exist(product_id):
            product_id = "".join(["{}".format(randint(1, 9)) for num in range(0, 7)])
        return product_id
