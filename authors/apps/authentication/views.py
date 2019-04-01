from ..core.mail import mail_helper
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer)

from .renderers import UserJSONRenderer
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from django.conf import settings
import jwt


class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    """ post:

        Register a user

    Creates a new user instance
    """
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    @swagger_auto_schema(
        query_serializer=LoginSerializer,
        response={status.HTTP_200_OK: LoginSerializer}
    )
    def post(self, request):
        """
            Register a user
            Creates a new user instance
        """
        user = request.data.get('user', {})
        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.

        JWT_payload = {'email': user.get("email")}
        # This line generates the token
        JWT_token = jwt.encode(JWT_payload, settings.SECRET_KEY,
                               algorithm='HS256').decode()

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        mail_helper(request=request)
        activation_link = mail_helper.get_link(
            path='activate',
            token=serializer.data.get('token', JWT_token)
        )

        mail_helper.send_mail(
            subject='Activate Account',
            to_addrs=[serializer.data.get('email')],
            multiple_alternatives=True,
            template_name='user_account_activation.html',
            template_values={
                'username': serializer.data.get('username'),
                'activation_link': activation_link
            }
        )
        res_message = {"message": "User account created." +
                       " An activation link has been sent to " +
                       f"{serializer.data.get('email')}."
                       }

        data = serializer.data
        data['token'] = JWT_token

        res_message['data'] = data

        return Response(
            data=res_message,
            status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    """ post:

        Logs in a user

    Provided a valid password and email, logs the user into the system
    """
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    @swagger_auto_schema(
        query_serializer=LoginSerializer,
        response={status.HTTP_200_OK: LoginSerializer}
    )
    def post(self, request):
        """
            Logs in a user
            Provided a valid password and email,
            logs the user into the system
        """
        user = request.data.get('user', {})

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't actually have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    """ get:

        Retrieves a single user

    Provided an id, retrieves a user from the system

    put:
        Update all details of a user

    Updates all user information in the system

    patch:
        Update a single detail of a user

    Updates part of the information by the user
    """

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
