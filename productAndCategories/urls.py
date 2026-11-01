from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoriesViewset, ProductViewset


router = DefaultRouter()
router.register(r'categories', CategoriesViewset, basename="categories")
router.register(r'products', ProductViewset, basename="products")

urlpatterns = [
    path('api/v1/', include(router.urls)),
]