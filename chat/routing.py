from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('chat/<str:other_user>', consumers.ChatConsumer.as_asgi()),
]
