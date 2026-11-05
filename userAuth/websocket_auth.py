from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from .authentication import AppJWTAuthentication


class JWTAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        scope = dict(scope)
        token = self._get_token(scope)

        if token:
            scope["user"] = await self.get_user(token)

        return await self.app(scope, receive, send)

    @staticmethod
    def _get_token(scope):
        authorization = next(
            (
                value
                for key, value in scope.get("headers", [])
                if key.lower() == b"authorization"
            ),
            None,
        )

        if authorization:
            parts = authorization.decode("latin-1").split()
            if len(parts) == 2 and parts[0].lower() == "bearer":
                return parts[1]

        query = parse_qs(scope.get("query_string", b"").decode("utf-8"))
        return query.get("access_token", [None])[0]

    @staticmethod
    @database_sync_to_async
    def get_user(token):
        authentication = AppJWTAuthentication()
        try:
            validated_token = authentication.get_validated_token(token)
            return authentication.get_user(validated_token)
        except AuthenticationFailed:
            return AnonymousUser()
