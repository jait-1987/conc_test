from django.db import models

class Order(models.Model):
    product_id = models.CharField(max_length=200)
    user_id = models.CharField(max_length=200)
    product_name = models.CharField(max_length=200)
    product_price = models.FloatField()
    product_quantity = models.PositiveIntegerField()