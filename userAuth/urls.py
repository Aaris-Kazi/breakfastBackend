from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import Login, Register, Addresses

router = DefaultRouter()

router.register(prefix="login", viewset=Login, basename="login")
router.register(prefix="register", viewset=Register, basename="register")
router.register(prefix=r"addresses", viewset=Addresses, basename="addresses")

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
