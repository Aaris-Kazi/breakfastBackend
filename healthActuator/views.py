from django.http import JsonResponse
from rest_framework.decorators import api_view


# Create your views here.


@api_view(['GET'])
def health(request):
    return JsonResponse({"status": "healthy"}, status=200)