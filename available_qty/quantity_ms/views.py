import json
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from .models import Product


@method_decorator(csrf_exempt, name='dispatch')
class ProductView(View):
    def get(self, request, product_id):
        product = Product.objects.filter(product_id=product_id).first()
        if not product:
            error_msg = "No Product found for product Id %s" % product_id
            return JsonResponse({"error": error_msg}, status=400)
        product_quantity = product.product_quantity
        data = {
            'product_id': product_id,
            'product_quantity': product_quantity,
        }

        return JsonResponse(data)

    def put(self, request, product_id):
        data = json.loads(request.body.decode("utf-8"))
        with transaction.atomic():
            try:
                product = Product.objects.filter(product_id=product_id).select_for_update(nowait=True).first()
            except:
                data = {"message": "Server Error", "status": "error"}
                return JsonResponse(data, status=400)

            if not product:
                data = {"message": "Product Id not found", "status": "error"}
                return JsonResponse(data, status=400)

            product.product_quantity = product.product_quantity - int(data['product_quantity'])
            product.save()

        data = {"message": "Product Id: %s , has been updated" % product.product_id, "status": "ok"}
        return JsonResponse(data)