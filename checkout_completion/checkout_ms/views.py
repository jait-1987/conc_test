import json
import requests
import traceback
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.conf import settings
from .models import Order
from .tasks import update_order_task


@method_decorator(csrf_exempt, name='dispatch')
class OrderView(View):
    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        p_id = data.get('product_id')
        u_id = data.get('user_id')
        p_name = data.get('product_name')
        p_price = data.get('product_price')
        p_quantity = data.get('product_quantity')
        order_data = {
            'product_id': p_id,
            'user_id': u_id,
            'product_name': p_name,
            'product_price': p_price,
            'product_quantity': p_quantity,
        }

        # Basic data for urls
        base_url = settings.AVAILABLE_QTY_URL
        available_qty_ep = settings.AVAILABLE_QTY_EP
        update_qty_ep = settings.UPDATE_QTY_EP

        with transaction.atomic():
            try:
                order = Order.objects.filter().select_for_update().first()
                available_url = base_url + available_qty_ep + str(p_id)

                # Check latest available qty from other microservice
                available_qty_resp = requests.get(available_url)
                if available_qty_resp.status_code == 200:
                    available_qty = available_qty_resp.json().get('product_quantity')
                    print ("Product Qty Available: %s" % available_qty)

                    if available_qty <= 0:
                        data = {"message": "No stock", "status": "error"}
                        print ("No stock")
                        return JsonResponse(data, status=400)
                    elif available_qty < p_quantity:
                        error_msg = "Only %s left in stock" % available_qty
                        print ("Less stock: %s", available_qty)
                        data = {"message": error_msg, "status": "error"}
                        return JsonResponse(data, status=400)
                    # Update quantity to other microservice
                    update_qty_url = base_url + update_qty_ep + str(p_id)
                    payload = {"product_quantity": p_quantity}
                    update_qty_resp = requests.put(update_qty_url, data=json.dumps(payload))

                    if update_qty_resp.status_code == 200:
                        task_queue = "default"
                        update_order_task.apply_async(args=[order_data], kwargs={}, queue=task_queue)
                        data = {"message": "Order created for product Id :%s" % p_id, "status": "ok"}
                else:
                    data = {"message": "Server Error", "status": "error"}
                    return JsonResponse(data, status=400)
            except:
                data = {"message": "Server Error", "status": "error"}
                print ("Server Error", traceback.format_exc())
                return JsonResponse(data, status=400)
        return JsonResponse(data)
