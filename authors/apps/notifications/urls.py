from django.conf.urls import url
from django.urls import path
from authors.apps.notifications.views import NotificationListViews, ReadNotificationApiView, ReadUpdateDeleteApiView

urlpatterns = [
    url(r'^unread/', NotificationListViews.as_view(), name='unread-notifications'),
    url(r'^read/', ReadNotificationApiView.as_view(), name='read-notifications'),
    path('<int:pk>/', ReadUpdateDeleteApiView.as_view(), name='specific_notifications'),
]