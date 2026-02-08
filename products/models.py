from django.db import models
from accounts.models import User

class Supplier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    accepts_orders = models.BooleanField(default=True)

    def __str__(self):
        return self.company_name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return f"{self.name} ({self.supplier.company_name})"

class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, related_name='attributes', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}: {self.value}"