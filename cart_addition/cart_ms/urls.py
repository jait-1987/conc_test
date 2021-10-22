from django.urls import path
from .views import UserCartView

urlpatterns = [
    path('create/', UserCartView.as_view(), name='cart_create'),
]
