from django.urls import path
from .views import OrderView

urlpatterns = [
    path('create/', OrderView.as_view(), name='order_add'),
]
