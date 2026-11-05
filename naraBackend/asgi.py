"""
ASGI config for naraBackend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'naraBackend.settings')

django_asgi_app = get_asgi_application()
from orderAndCart.urls import websocket_urlpatterns
from userAuth.websocket_auth import JWTAuthMiddleware


application = ProtocolTypeRouter({
    "http": django_asgi_app,

    "websocket": AuthMiddlewareStack(
        # JWTAuthMiddleware(URLRouter(websocket_urlpatterns))
        URLRouter(websocket_urlpatterns)
    ),
})