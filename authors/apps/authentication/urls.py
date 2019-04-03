from django.conf.urls import url
from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView,
    ResetPassword, ResetPasswordConfirmView,

    UserListApiView, SocialAuthView

)


urlpatterns = [
    url(r'^user/?$', UserRetrieveUpdateAPIView.as_view()),
    url(r'^users/?$', RegistrationAPIView.as_view()),
    url(r'^users/list/?$', UserListApiView.as_view()),
    url(r'^users/login/?$', LoginAPIView.as_view()),
    url(r'^users/password-reset/?$', ResetPassword.as_view(), name='password_reset'),
    url(r'^users/password-reset-confirm/?$', ResetPasswordConfirmView.as_view(),
        name='password_reset_confirm'),

    path('social_auth', SocialAuthView.as_view(), name="social_auth"),
]
