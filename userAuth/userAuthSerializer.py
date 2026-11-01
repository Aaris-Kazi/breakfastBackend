from rest_framework.serializers import Serializer, CharField, EmailField, IntegerField, ChoiceField
from django.contrib.auth import authenticate, get_user_model, hashers
from .models import UsersModels


class RegisterSerializer(Serializer):
    
    firstName = CharField(max_length=50)
    lastName = CharField(max_length=50)

    role = ChoiceField(
        choices = UsersModels.UserRole.choices,
        default = UsersModels.UserRole.CUSTOMER,
        required=False
    )



    username = CharField(max_length=50)
    email = EmailField(max_length=50)
    password = CharField(max_length=100)

    def create(self, validated_data: dict):
        return UsersModels.objects.create(
            firstName = validated_data.get("firstName"),
            lastName = validated_data.get("lastName"),
            username = validated_data.get("username"),
            role = validated_data.get("role"),
            email = validated_data.get("email"),
            password = hashers.make_password(
                validated_data.get("password"),
                hasher="argon2"
            )
        )

    class Meta:
        model = UsersModels
        fields = ["firstName", "lastName", "username", "email", "password"]

class LoginSerializer(Serializer):
    
    email = EmailField(max_length=50)
    password = CharField(max_length=100)

    def is_valid_user(self, validated_data: dict) -> str:
        user = UsersModels.objects.get(email = validated_data.get("email"))
        is_valid = hashers.check_password(
            validated_data.get("password"),
            user.password
        )

        if not is_valid:
            raise Exception("Invalid username or password")
        return user


class AddressSerializer(Serializer):

    pincode = CharField(max_length=6)
    state = CharField(max_length=100)
    city = CharField(max_length=100)
    addressLine = CharField(max_length=255)
    email = CharField(max_length = 255)


class AddressResponseSerializer(Serializer):
    id = IntegerField()
    pincode = CharField(max_length=6)
    state = CharField(max_length=100)
    city = CharField(max_length=100)
    addressLine = CharField(max_length=255)

    
