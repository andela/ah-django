from django.contrib.auth.tokens import default_token_generator


from rest_framework import generics, permissions, status, views
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from djoser import utils, signals
from djoser.compat import get_user_email, get_user_email_field_name
from djoser.conf import settings

from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer,
    PasswordResetSerializer
)

from . import mailer
from .models import User


class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't actually have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class ResetPassword(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    _users = None

    def post(self, request):

        email = request.data.get('user', {})
        serializer = self.serializer_class(
            data=email
        )

        serializer.is_valid(raise_exception=True)

        email = serializer.data['email']

        user = self.get_user(email)

        if not user:
            response = {
                "status": "400",
                "error": "Email address does not exist"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        res = self.send_reset_password_email(user[0])
        msg = "Check email to reset password"
        data = self.get_user_data(user[0])
        token = data['token']
        uid = data['uid']

        if res.status_code == 202:
            response = {
                "status": 200,
                "token": token,
                "uid": uid,
                "message": msg
            }
            return Response(response, status=status.HTTP_200_OK)

    def get_user(self, email):
        if self._users is None:
            email_field_name = get_user_email_field_name(User)
            users = User.objects.filter(
                **{email_field_name + '__iexact': email})
            self._users = [
                u for u in users if u.is_active and u.has_usable_password()
            ]
        return self._users

    def send_reset_password_email(self, user):
        context = {'user': user}
        recepient = get_user_email(user)
        data = self.get_user_data(recepient)

        return mailer.RecoverPassword(self.request,
                                      context, recepient, data).send_email()

    def get_user_data(self, email):
        user = User.objects.get(email=email).username
        user_object = User.objects.get(email=email)
        uid = User.objects.get(email=email).id
        token = default_token_generator.make_token(user_object)

        data = {
            "user": user,
            "uid": uid,
            "token": token
        }

        return data


class ResetPasswordConfirmView(generics.UpdateAPIView):
    """
    patch:
    Confirming a user's reset password.
    """
    permission_classes = [permissions.AllowAny]
    token_generator = default_token_generator

    def partial_update(self, request, pk=None):
        uid = self.request.query_params.get('uid')
        serializer = User.objects.get(id=uid)

        if request.data['new_password'] != request.data['re_new_password']:
            return Response({
                'error': 'Ensure both passwords match.',
                'status': 400
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.set_password(request.data['new_password'])
        serializer.save()
        return Response(status=status.HTTP_200_OK,
                        data={'message': 'Password reset successfully.', 'status': 200})
