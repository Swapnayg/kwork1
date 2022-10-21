"""
ASGI config for mainKwork project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mainKwork.settings")
asgi_application = get_asgi_application()

from channels.auth import AuthMiddlewareStack

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from kworkapp import routing

application = ProtocolTypeRouter(
    {
        "http": asgi_application,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns))
        ),
    }
)