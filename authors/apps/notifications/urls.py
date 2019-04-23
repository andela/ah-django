from django.urls import path

from .views import NotificationView

app_name = "notifications"
urlpatterns = [
    path("subscription/<type>/", NotificationView.as_view()),
]
