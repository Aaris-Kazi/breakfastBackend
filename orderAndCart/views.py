from rest_framework.serializers import ValidationError
from rest_framework.viewsets import ViewSet
from django.http import JsonResponse
from rest_framework.request import Request

from .OrderCartService import OrderCartService
from .orderCartSerial import OrderSerializer, CartSerializer, CartResponseSerializer, CartUpdateSerializer, OrderItemResponseSerializer, OrderResponseSerializer, OrderUpdateSerializer
from rest_framework.permissions import IsAuthenticated
import logging
# Create your views here.

service = OrderCartService()
logger = logging.getLogger(__name__)


class OrderViewset(ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request: Request):
        try:
            serializer = OrderSerializer(data=request.data)

            if serializer.is_valid():
                service.createOrder(request.user, serializer.validated_data)
                return JsonResponse({"msg": "success"})

            logger.error(
                f"serializer update error due to {serializer.error_messages} ")
            return JsonResponse({"msg": "invalid request"}, status=400)
        except ValidationError as e:
                logger.error(f"ValidationError occured due to {e.args[0]}")
                return JsonResponse({"status": "error", "msg": e.args[0]}, status=400)
        except Exception as e:
            logger.error(f"Exception occured in create cart {e.args[0]}")
            return JsonResponse({"status": "error", "msg": e.args[0]}, status=403)
        

    def list(self, request: Request):
        orderItem = service.getOrder(request.user)
        orderSerial = OrderResponseSerializer(orderItem[0].order)


        orderItemSerial = OrderItemResponseSerializer(
            orderItem,
            many=True
        )
        response:dict = orderSerial.data
        response.update({"order_list": orderItemSerial.data})
        return JsonResponse({"data": response})

    def update(self, request: Request, pk: int):

        try:
            serializer = OrderUpdateSerializer(data = request.data)
            if serializer.is_valid():
                data = serializer.validated_data
                service.updateOrderStatus(request.user, pk, data.get("paymentStatus"), data.get("status"))
                return JsonResponse({"msg": "success"})

            return JsonResponse({"status": "failure", "msg": serializer.error_messages}, status = 400)
        
        except ValidationError as e:
            logger.error(f"ValidationError occured due to {e.args[0]}")
            return JsonResponse({"status": "error", "msg": e.args[0]}, status=400)
        except Exception as e:
            logger.error(f"Exception occured in create cart {e.args[0]}")
            return JsonResponse({"status": "error", "msg": e.args[0]}, status=500)


class CartViewset(ViewSet):

    permission_classes = [IsAuthenticated]

    def create(self, request: Request):
        try:
            cart_serializer = CartSerializer(data=request.data)

            if cart_serializer.is_valid():
                data = cart_serializer.validated_data
                cart, cartItem = service.createCart(data, request.user)
                service.notify_cart_size(request.user.id, service.get_cart_size(cart.id))
                return JsonResponse({"msg": "success", "cart_id": cartItem.id})
            
            logger.error(f"serializer update error due to {cart_serializer.error_messages} ")
            return JsonResponse({"msg": "invalid request"}, status=400)
        except ValidationError as e:
            logger.error(f"ValidationError occured due to {e.args[0]}")
            return JsonResponse({"status": "error", "msg": e.args[0]}, status=400)
        except Exception as e:
            logger.error(f"Exception occured in create cart {str(e)}")
            return JsonResponse({"status": "error", "msg": str(e)}, status=403)

    def list(self, request: Request):
        model = service.getCart(request.user)
        response = CartResponseSerializer(
            model,
            many=True
        )
        return JsonResponse({"data": response.data})

    def update(self, request: Request, pk: int):

        try:
            serializer = CartUpdateSerializer(data=request.data)
            if serializer.is_valid():
                service.updateCart(request.user.username, int(pk), serializer.validated_data)
                service.notify_cart_updated(request.user.id, pk)
                return JsonResponse({"status": "success"})
            logger.error(f"serializer update error due to {serializer.error_messages} ")
            return JsonResponse({"msg": "invalid request"}, status=400)
        except ValidationError as e:
            logger.error(f"ValidationError occured due to {e.args[0]}")
            return JsonResponse({"status": "error", "msg": e.args[0]}, status=400)
        except Exception as e:
            logger.error(f"Exception occured due to {str(e.args[0])}")
            return JsonResponse({"status": "error", "msg": str(e)}, status=403)

    def delete(self, request: Request, pk: int):
        try:
            service.deleteCart(request.user, int(pk))
            # service.notify_cart_size(request.user.id, service.get_cart_size(cart.id))
            return JsonResponse({"msg": "success"})
        except Exception as e:
            logger.error(f"Exception occured in delete due to {e.args[0]}")
            return JsonResponse({"status": "error", "msg": str(e)}, status=403)
