from django.db import models

# Create your models here.


class Products(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    category = models.CharField(max_length=100)
    in_stock = models.BooleanField(default=True)

class Order(models.Model):
    pass

class RefundRequest(models.Model):
    pass