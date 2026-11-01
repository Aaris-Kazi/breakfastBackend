from django.contrib import admin
from .models import CartModel, CartItemModel, OrderModel, OrderItemModel


# Register your models here.

@admin.register(CartModel)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "users", "status", "created_at", "updated_at")
    list_filter = ("status",)
    search_fields = ("users__username",)


@admin.register(CartItemModel)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "cart", "product", "quantity")
    list_filter = ("cart", "product")
    search_fields = ("product__name",)

@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "users", "status", "total_amount", "created_at", "updated_at")
    list_filter = ("status",)
    search_fields = ("users__username",)

@admin.register(OrderItemModel)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product", "quantity", "unit_price")
    list_filter = ("order", "product")
    search_fields = ("product__name",)