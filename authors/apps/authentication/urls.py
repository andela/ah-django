from django.conf.urls import url

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView,
    ForgotPasswordAPIview, ResetPasswordAPIView
)
app_name = 'authentication'


urlpatterns = [
    url(r'^user/?$', UserRetrieveUpdateAPIView.as_view()),
    url(r'^users/login/?$', LoginAPIView.as_view(), name="login"),
    url(r'^users/', RegistrationAPIView.as_view(), name='activation'),
    url(r'^users/login/?$', LoginAPIView.as_view()),
    url(r'^account/forgot_password/?$',
        ForgotPasswordAPIview.as_view(), name="forgot_password"),
    url(r'^account/reset_password/?(?P<token>[a-zA-Z0-9_\.-]{3,1000})?/?$',
        ResetPasswordAPIView.as_view(), name="reset_password"),
]
