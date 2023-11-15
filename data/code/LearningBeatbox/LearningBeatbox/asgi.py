# LearningBeatbox/asgi.py

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path
from webapp import consumers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LearningBeatbox.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path('ws/sounds/', consumers.SoundConsumer.as_asgi()),
        ])
    ),
})
