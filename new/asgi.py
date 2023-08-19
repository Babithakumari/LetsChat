"""
ASGI config for new project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url

from chat.consumers import *
import chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'new.settings')

#Configure application to route http and websocket connection
application = ProtocolTypeRouter({
    "http":get_asgi_application(),

    # When a wss connection is sent control is transferred to AuthMiddlewareStack
    "websocket":AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),

})
