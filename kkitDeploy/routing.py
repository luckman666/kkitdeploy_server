
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import apps.utils.routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            apps.utils.routing.websocket_urlpatterns  # 指明路由文件是app01.routing.py
        )
    ),
})