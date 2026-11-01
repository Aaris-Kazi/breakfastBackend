from django.shortcuts import render
from rest_framework.serializers import ValidationError
from rest_framework.viewsets import ViewSet
from django.http import JsonResponse
from rest_framework.request import Request

from orderAndCart.orderCartSerial import OrderUpdateSerializer
from orderAndCart.OrderCartService import OrderCartService
import logging
from rest_framework.permissions import IsAuthenticated

from utils.permissionClasses import IsDeliveryAgent
# Create your views here.

logger = logging.Logger(__name__)
service = OrderCartService()

class Delivery(ViewSet):
    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsDeliveryAgent()]

        return [IsAuthenticated()]
    permission_classes = [IsAuthenticated]


    def create(self, request: Request):
        return JsonResponse({"msg": "success"})

    def update(self, request: Request, pk: int):

        try:
            serializer = OrderUpdateSerializer(data=request.data)
            if serializer.is_valid():
                data:dict = serializer.validated_data
                service.updateOrderStatus(request.user.username, pk, data.get(
                    "paymentStatus"), data.get("status"))
                return JsonResponse({"msg": "success"})

            return JsonResponse({"status": "failure", "msg": serializer.error_messages}, status=400)

        except ValidationError as e:
            logger.error(f"ValidationError occured due to {e.args[0]}")
            return JsonResponse({"status": "error", "msg": e.args[0]}, status=400)
        except Exception as e:
            logger.error(f"Exception occured in create cart {e.args[0]}")
            return JsonResponse({"status": "error", "msg": e.args[0]}, status=500)
