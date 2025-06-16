# IFPWebApp/routing.py
from django.urls import re_path
from . import consumers

print("Loading routing.py")  # Debug

websocket_urlpatterns = [
    re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),
]

print("Routing patterns loaded")  # Debug