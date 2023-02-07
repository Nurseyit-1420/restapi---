from django.db import models
from users.models import Vendor, Customer


class Category(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, null=False, blank=False)
    price = models.IntegerField(default=0, null=False, blank=False)

    def __str__(self):
        return f'{self.name}'


class Cart(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)

    def __str__(self):
        return f'{self.customer.email}`s cart'


class Order(models.Model):
    products = models.ManyToManyField(Product)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Order #{self.id}'

