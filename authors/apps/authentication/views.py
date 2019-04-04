from .backends import JWTAuthentication as auth


from rest_framework import generics, status, permissions
from django.core.mail import send_mail

from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User

from djoser.compat import get_user_email, get_user_email_field_name

from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer,
    PasswordResetSerializer, SocialSerializer
)

from . import mailer
from requests.exceptions import HTTPError

from social_django.utils import load_strategy, load_backend
from social_core.backends.oauth import BaseOAuth2, BaseOAuth1
from social_core.exceptions import MissingBackend, AuthTokenError, AuthForbidden


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

        # Set all variables to be used with send_email function
        subject = "Welcome to Authors Haven"

        # Checks if connections uses https or http
        if request.is_secure():
            protocol = 'https://'
        else:
            protocol = 'http://'

        # Get host name and append url to login
        link = request.get_host() + "/api/users/login"

        full_link = protocol+link

        contact_message = "To {},".format(serializer.data.get('username')) +\
            "\n Thank you for joining Authors Haven. " +\
            "We are glad to have you on board. " +\
            "Please use the link {}".format(full_link) +\
            " to sign in to your new account"

        from_email = 'no-reply@authorshaven.com'
        to_email = [serializer.data.get('email')]

        send_mail(subject, contact_message, from_email, to_email,
                  fail_silently=True)

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
        token = user_object.token

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

    def partial_update(self, request, pk=None):
        uid = self.request.query_params.get('uid')
        token = self.request.query_params.get('token')
        if not auth().validate_token(token):
            return Response({
                'error': 'Invalid token',
                'status': 403
            }, status=status.HTTP_403_FORBIDDEN)
        try:
            serializer = User.objects.get(id=uid)
        except User.DoesNotExist:
            return Response({
                'error': 'User does not exist',
                'status': 400
            }, status=status.HTTP_400_BAD_REQUEST)

        if request.data['new_password'] != request.data['re_new_password']:
            return Response({
                'error': 'Ensure both passwords match.',
                'status': 400
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.set_password(request.data['new_password'])
        serializer.save()
        return Response(status=status.HTTP_200_OK,
                        data={'message': 'Password reset successfully.',
                              'status': 200})


class UserListApiView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = UserSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)


class SocialAuthView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = SocialSerializer

    def post(self, request, *args, **kwargs):
        """ interrupt social_auth authentication pipeline"""
        # pass the request to serializer to make it a python object
        # serializer also catches errors of blank request objects
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        provider = serializer.data.get('provider', None)
        strategy = load_strategy(request)  # creates the app instance

        try:
            # load backend with strategy and provider from settings(AUTHENTICATION_BACKENDS)
            backend = load_backend(
                strategy=strategy, name=provider, redirect_uri=None)

        except MissingBackend as error:

            return Response({
                "errors": str(error)
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # check type of oauth provider e.g facebook is BaseOAuth2 twitter is BaseOAuth1
            if isinstance(backend, BaseOAuth1):
                # oath1 passes access token and secret
                access_token = {
                    "oauth_token": serializer.data.get('access_token'),
                    "oauth_token_secret": serializer.data.get('access_token_secret'),
                }

            elif isinstance(backend, BaseOAuth2):
                # oauth2 only has access token
                access_token = serializer.data.get('access_token')

            authenticated_user = backend.do_auth(access_token)

        except HTTPError as error:
            # catch any error as a result of the authentication
            return Response({
                "error": "Http Error",
                "details": str(error)
            }, status=status.HTTP_400_BAD_REQUEST)

        except AuthForbidden as error:
            return Response({
                "error": "invalid token",
                "details": str(error)
            }, status=status.HTTP_400_BAD_REQUEST)

        if authenticated_user and authenticated_user.is_active:
            # Check if the user you intend to authenticate is active
            response = {"email": authenticated_user.email,
                        "username": authenticated_user.username,
                        "token": authenticated_user.token}

            return Response(status=status.HTTP_200_OK, data=response)
