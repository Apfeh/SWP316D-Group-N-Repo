# IFPSystem/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import IFPWebApp.routing

print("Loading ASGI application")  # Debug
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'IFPSystem.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(IFPWebApp.routing.websocket_urlpatterns)
    ),
})
print("ASGI application loaded")  # Debug