from django.urls import path
from .views import ProductView

urlpatterns = [
    path('available_qty/<product_id>', ProductView.as_view(), name='add'),
    path('update_qty/<product_id>', ProductView.as_view(), name='add'),
]
