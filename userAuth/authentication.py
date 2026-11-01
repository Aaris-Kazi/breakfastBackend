from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import Token

from .models import UsersModels


class AppJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token: Token):
        if "role" not in validated_token:
            return super().get_user(validated_token)

        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError as error:
            raise InvalidToken(
                _("Token contained no recognizable user identification")
            ) from error

        try:
            return UsersModels.objects.get(
                **{api_settings.USER_ID_FIELD: user_id}
            )
        except UsersModels.DoesNotExist as error:
            raise AuthenticationFailed(
                _("User not found"), code="user_not_found"
            ) from error
