from unittest.mock import patch

from django.test import SimpleTestCase
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken

from .authentication import AppJWTAuthentication
from .models import UsersModels


def make_token(**claims) -> AccessToken:
    token = AccessToken()
    for claim, value in claims.items():
        token[claim] = value
    return token


class AppJWTAuthenticationTests(SimpleTestCase):
    @patch("userAuth.authentication.UsersModels.objects.get")
    def test_role_token_resolves_custom_user(self, get_user):
        user = UsersModels(username="delivery-agent")
        get_user.return_value = user

        authenticated_user = AppJWTAuthentication().get_user(
            make_token(user_id="3", role="DELIVERY_AGENT")
        )

        self.assertIs(authenticated_user, user)
        self.assertTrue(authenticated_user.is_authenticated)
        get_user.assert_called_once_with(id="3")

    @patch("userAuth.authentication.UsersModels.objects.get")
    def test_missing_custom_user_raises_user_not_found(self, get_user):
        get_user.side_effect = UsersModels.DoesNotExist

        with self.assertRaises(AuthenticationFailed) as error:
            AppJWTAuthentication().get_user(
                make_token(user_id="3", role="DELIVERY_AGENT")
            )

        self.assertEqual(error.exception.detail["code"], "user_not_found")

    @patch.object(JWTAuthentication, "get_user")
    def test_token_without_role_uses_standard_user_lookup(self, get_user):
        legacy_user = object()
        get_user.return_value = legacy_user

        authenticated_user = AppJWTAuthentication().get_user(
            make_token(user_id="3")
        )

        self.assertIs(authenticated_user, legacy_user)
        get_user.assert_called_once()
