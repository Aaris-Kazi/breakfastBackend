from rest_framework.viewsets import ViewSet
from rest_framework.request import Request
from django.http import JsonResponse
from .prodAndCatSerializer import CategoriesSerializer, ProductSerializer, CategoriesUpdateSerializer
from .ProdAndCatService import ProdAndCatService
import logging

service = ProdAndCatService()
logger = logging.getLogger(__name__)

class CategoriesViewset(ViewSet):


    def create(self, request: Request):
        try:
            serializer = CategoriesSerializer(data = request.data)

            if serializer.is_valid():
                serializer.save()

                return JsonResponse({"msg": "success"})
            logger.error(f"Serializer error in Creating Categories due to {serializer.error_messages}")
            return JsonResponse({"msg": serializer.errors}, status=400)
        except Exception as e:
            logger.error(f"Create categoery exception due to :: {e.args[1]}")
            return JsonResponse({"msg": str(e)}, status=400)

    def list(self, request: Request):
        categories = service.getCategory()
        serializer = CategoriesSerializer(categories, many=True)

        return JsonResponse({"data": serializer.data})

    def update(self, request: Request, pk:str):
        try:
            data = request.data
            serializer = CategoriesUpdateSerializer(data=data)
            if not serializer.is_valid():
                logger.error(f"Serializer error in Updating Categories due to {serializer.error_messages}")
                return JsonResponse({"msg": serializer.errors}, status=400)
            

            
            service.updateCategory(pk, serializer.validated_data)
            return JsonResponse({"msg": "success"}, status=201)
        except Exception as e:
            logger.error(f"update category exception due to :: {e.args[0]}")
            return JsonResponse({"status": "failed", "msg": e.args[0]}, status = 500)



class ProductViewset(ViewSet):

    def create(self, request: Request):
        try:
            serializer = ProductSerializer(data = request.data)

            if serializer.is_valid():
                serializer.save()

                return JsonResponse({"msg": "success"})

            logger.error(f"Serializer error in Creating Product due to {serializer.error_messages}")
            return JsonResponse({"msg": serializer.errors}, status=400)
        except Exception as e:
            logger.error(f"Create categoery exception due to :: {e.args[1]}")
            return JsonResponse({"msg": str(e)}, status=400)

    def update(self, request: Request, pk: int):
        try:
            product = service.product_model.objects.get(pk=pk)
            serializer = ProductSerializer(product, data=request.data, partial=True)

            if serializer.is_valid():
                data = serializer.validated_data
                data['id'] = pk
                serializer.update(data)
                return JsonResponse({"msg": "success"})
            logger.error(f"Serializer error in Updating Product due to {serializer.error_messages}")
            return JsonResponse({"msg": serializer.errors}, status=400)
        except Exception as e:
            logger.error(f"Create categoery exception due to :: {e.args[1]}")
            return JsonResponse({"msg": str(e)}, status=400)


    def list(self, request: Request):
        products = service.getProduct()
        serializer = ProductSerializer(products, many=True)

        return JsonResponse({"data": serializer.data})