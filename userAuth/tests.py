from unittest.mock import AsyncMock, patch

from asgiref.sync import async_to_sync
from django.test import SimpleTestCase
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken

from .authentication import AppJWTAuthentication
from .models import UsersModels
from .websocket_auth import JWTAuthMiddleware


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


class JWTAuthMiddlewareTests(SimpleTestCase):
    def test_extracts_bearer_token(self):
        self.assertEqual(
            JWTAuthMiddleware._get_token(
                {"headers": [(b"authorization", b"Bearer access-token")]}
            ),
            "access-token",
        )

    def test_extracts_query_token_for_browser_clients(self):
        self.assertEqual(
            JWTAuthMiddleware._get_token(
                {"query_string": b"access_token=browser-token"}
            ),
            "browser-token",
        )

    def test_injects_authenticated_user_into_websocket_scope(self):
        authenticated_user = object()
        application = AsyncMock()
        middleware = JWTAuthMiddleware(application)
        scope = {"type": "websocket", "query_string": b"access_token=test-token"}

        with patch.object(
            JWTAuthMiddleware,
            "get_user",
            new=AsyncMock(return_value=authenticated_user),
        ) as get_user:
            async_to_sync(middleware)(scope, AsyncMock(), AsyncMock())

        forwarded_scope = application.await_args.args[0]
        self.assertIs(forwarded_scope["user"], authenticated_user)
        self.assertNotIn("user", scope)
        get_user.assert_awaited_once_with("test-token")
