import requests
import json
from celery.app import shared_task
from django.conf import settings
from .models import Order


@shared_task(name='UpdateOrderTask')
def update_order_task(order_data):
    Order.objects.create(**order_data)
