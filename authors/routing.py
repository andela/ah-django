from .consumers import NotificationConsumer
from django.urls import path
from django.conf.urls import url
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            url(r"^api/notifications/(?P<stream>\w+)/$", NotificationConsumer),
            url(r"", NotificationConsumer),
        ])
    )

})
