from django.contrib import admin
from .models import CategoriesModel, ProductModel
# Register your models here.


@admin.register(CategoriesModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "slug",
        "descriptions",
        "image_urls",
        "is_active"
    ]
    search_fields = []


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "category",
        "name",
        "slug",
        "unit",
        "stock_quantity",
        "description",
        "price",
        "is_active",
    ]
    search_fields = []