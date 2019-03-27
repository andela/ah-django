from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView, ResetPassword
)

urlpatterns = [
    url(r'^user/?$', UserRetrieveUpdateAPIView.as_view()),
    url(r'^users/?$', RegistrationAPIView.as_view()),
    url(r'^users/login/?$', LoginAPIView.as_view()),
    path('password-reset/', ResetPassword.as_view()),
    # path('password-reset-confirm/<uidb64>/token', )
]
