from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from .views import OrderViewset, CartViewset
from .Consumers import CartConsumer


router = DefaultRouter()
router.register(r'orders', OrderViewset, basename='orders')
router.register(r'cart', CartViewset, basename='cart')

urlpatterns = [
    path('api/v1/', include(router.urls)),
]

websocket_urlpatterns = [
    re_path(r"ws/cart/$", CartConsumer.as_asgi()),
]