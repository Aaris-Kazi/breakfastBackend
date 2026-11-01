from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewset, CartViewset


router = DefaultRouter()
router.register(r'orders', OrderViewset, basename='orders')
router.register(r'cart', CartViewset, basename='cart')

urlpatterns = [
    path('api/v1/', include(router.urls)),
]