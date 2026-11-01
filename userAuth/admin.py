from django.contrib import admin
from .models import UsersModels, AddressModels
# Register your models here.


@admin.register(UsersModels)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "role",
        "firstName",
        "lastName",
        "username",
        "email",
        "password",
    ]
    search_fields = [
        "first_name",
        "lastName",
        "email"
    ]


@admin.register(AddressModels)
class AddressAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "users",
        "longitude",
        "latitude",
        "pincode",
        "state",
        "city",
        "addressLine",
    ]
    search_fields = [
        "city"
    ]
