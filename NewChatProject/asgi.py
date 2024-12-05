"""
ASGI config for NewChatProject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import path
from chat.consumers import *


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewChatProject.settings')

application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        
       "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/timer/", TimerConsumer.as_asgi()),
            path("ws/counter/", CounterConsumer.as_asgi()),
            path("ws/chat/<int:from_user>/<int:to_user>/", ChatGetConsumer.as_asgi()),
        ])
    ),
    }
)
