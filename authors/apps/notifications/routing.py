""" Define url patterns for the channel layer """
from django.conf.urls import url

from authors.apps.notifications.consumers import NotificationConsumer

websocket_urlpatterns = [
    url(r'^ws/notifications/(?P<group>\w+)/$', NotificationConsumer),
    url(r"", NotificationConsumer),
]
