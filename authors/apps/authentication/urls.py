from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView,
    ForgotPasswordAPIview, ResetPasswordAPIView
)

urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view()),
    path('users/', RegistrationAPIView.as_view(), name="register_url"),
    path('users/login', LoginAPIView.as_view(), name="login_url"),
	path('users/forgot_password/', ForgotPasswordAPIview.as_view(), name="forgot_password"),
    path('users/reset_password/<token>', ResetPasswordAPIView.as_view(), name="reset_password"),
]
