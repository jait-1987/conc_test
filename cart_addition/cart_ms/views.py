import json
import requests
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.conf import settings
from .models import UserCart


@method_decorator(csrf_exempt, name='dispatch')
class UserCartView(View):
    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        p_id = data.get('product_id')
        u_id = data.get('user_id')
        p_name = data.get('product_name')
        p_price = data.get('product_price')
        p_quantity = data.get('product_quantity')

        cart_data = {
            'product_id': p_id,
            'user_id': u_id,
            'product_name': p_name,
            'product_price': p_price,
            'product_quantity': p_quantity,
        }

        # Basic data for urls
        base_url = settings.AVAILABLE_QTY_URL
        available_qty_ep = settings.AVAILABLE_QTY_EP
        available_url = base_url + available_qty_ep + str(p_id)
        with transaction.atomic():

            # Check latest available qty from other microservice
            available_qty_resp = requests.get(available_url)
            if available_qty_resp.status_code == 200:
                available_qty = available_qty_resp.json().get('product_quantity')
                print ("Product Qty Available: %s" % available_qty)

                if available_qty <= 0:
                    data = {"message": "No stock", "status": "error"}
                    status = 400
                elif available_qty < p_quantity:
                    error_msg = "Only %s left in stock" % available_qty
                    data = {"message": error_msg, "status": "error"}
                    status = 400
                else:
                    user_cart = UserCart.objects.create(**cart_data)
                    data = {
                        "message": "New item added to Cart with id: %s" % user_cart.id
                    }
                    status = 200

            else:
                data = {"message": "Server Error", "status": "error"}
                status = 400
        return JsonResponse(data, status=status)
