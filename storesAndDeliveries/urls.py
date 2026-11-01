from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import Delivery



router = DefaultRouter()

router.register(r"delivery", Delivery, basename="delivery")

urlpatterns = [
    path("api/v1/", include(router.urls))
]