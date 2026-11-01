from .models import AddressModels, UsersModels
from django.db.models.query import QuerySet
from .userAuthSerializer import AddressSerializer, AddressResponseSerializer

class UserServices:


    def createAddress(self, data: dict):

        AddressModels.objects.create(
            pincode = data.get("pincode"),
            state = data.get("state"),
            city = data.get("city"),
            addressLine = data.get("addressLine"),
            users = UsersModels.objects.get(username = data.get("user")) ,
        )
        


    def getAddress(self, username: str) -> dict:
        address: QuerySet = AddressModels.objects.filter(
            users = UsersModels.objects.get(username = username)
        )


        response = AddressResponseSerializer(address, many = True)
        return response.data



