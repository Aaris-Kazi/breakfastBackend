from django.http import JsonResponse
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request

from userAuth.customToken import CustomTokenSerializer
from utils.permissionClasses import IsCustomer
from .userAuthSerializer import RegisterSerializer, LoginSerializer, AddressSerializer
from .services import UserServices

# from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
import logging
# Create your views here.

log = logging.getLogger(__name__)

services = UserServices()
serializer_class = CustomTokenSerializer()


class Login(ViewSet):


    def create(self, request: Request):

        try:
            serializer = LoginSerializer(data = request.data)

            if serializer.is_valid():
                data = serializer.validated_data
                user = serializer.is_valid_user(data)
                
                token = serializer_class.get_token(user)
                
                # token = RefreshToken.for_user(user)
                return JsonResponse(
                    {
                        "access_token": str(token.access_token),
                        "refresh_token": str(token)
                    }, status=201
                )
            
            return JsonResponse({"msg": serializer.error_messages}, status=401)
        except Exception as e:
                    return JsonResponse({"msg": str(e)}, status=500)


class Register(ViewSet):
    def create(self, request: Request):
        try:
            serializer = RegisterSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"data": "register"}, status=201)
            
            return JsonResponse({"msg": serializer.error_messages}, 401)
        except Exception as e:
            log.error(f"Creating register error due to {e.args[0]}")
            
            return JsonResponse({"msg": str(e)}, status=500)


class Addresses(ViewSet):

    # permission_classes = [IsAuthenticated]
    def get_permissions(self):
        if self.action in ["create", "update", "list", "partial_update", "destroy"]:
            return [IsCustomer()]
    
        return [IsAuthenticated()]

    def create(self, request: Request):
        try:
            serializer = AddressSerializer(data = request.data)

            if serializer.is_valid(): 
                data = serializer.validated_data
                data['user'] = request.user
                services.createAddress(serializer.validated_data)
                return JsonResponse({"data": "address"}, status=201)
            return JsonResponse({"msg": "address"}, status=401)
        except Exception as e:
            log.error(f"Creating address error due to {e.args[0]}")
            return JsonResponse({"msg": str(e)}, status=500)

    def retrieve(self, request: Request, pk: str):

        return JsonResponse({"msg": pk})

    def list(self, request: Request):

        try:
            # email = request.query_params.get("email")

            # if email == None or email == "":
            #     return JsonResponse({"error": "empty params"}, status=401)

            response:list = services.getAddress(request.user)

            return JsonResponse({"data": response})
        except Exception as e:
            log.error(f"listing address error due to {e.args[0]}")
            return JsonResponse({"msg": str(e)})