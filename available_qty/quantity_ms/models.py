from django.db import models

class Product(models.Model):
    product_id = models.CharField(max_length=200, unique=True)
    product_name = models.CharField(max_length=200)
    product_price = models.FloatField()
    product_quantity = models.PositiveIntegerField()