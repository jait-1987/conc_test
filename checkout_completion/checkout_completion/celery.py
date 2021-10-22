# from __future__ import absolute_import

import os

from celery import Celery
from django.conf import settings  # noqa
from kombu import Queue


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'checkout_completion.settings')
app = Celery('checkout_completion')

app.conf.update(
    BROKER_URL='redis://localhost:6379/0',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    CELERY_QUEUES=(
        Queue('default', routing_key='default'),
        Queue('notification', routing_key='notification'),
    ),
    CELERY_DEFAULT_QUEUE='default',
    CELERY_DEFAULT_EXCHANGE='default',
    CELERY_DEFAULT_ROUTING_KEY='default',
    CELERY_MAX_RETRY=3,
    CELERY_RETRY_COUNTDOWN=60*15,
    CELERY_TIMEZONE='Asia/Kolkata',
)

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
