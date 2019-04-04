from ..core.mail import mail_helper

from .renderers import UserJSONRenderer
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from .models import User
from django.conf import settings
from authors.apps.core import client
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from rest_framework import exceptions
import jwt
import os

from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer,
    ForgotPasswordSerializer, ResetPasswordSerializer
)


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

        JWT_payload = {'username': user.get("username")}
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


class ForgotPasswordAPIview(APIView):
    """
    This will send a reset link to the user on request
    """

    permission_classes = (AllowAny,)
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()

        if user is None:
            msg = {'Account with that email does not exist.'}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        """
        Adds token a new token to reset password
        """
        token = jwt.encode({
            'email': email,
            'type': 'reset password',
        },
            settings.SECRET_KEY
        ).decode('utf-8')

        reset_link = client.get_password_reset_link(request, token)

        subject = "Password reset link"
        from_email = os.getenv('EMAIL_HOST_USER')
        from_email, to_email, subject = from_email, email, subject
        # render password reset template with a dynamic value
        html = render_to_string('password_reset.html', {
                                'reset_password_link': reset_link})
        # strip html tags from the html content
        text_content = strip_tags(html)

        # create an email and attach content as html
        mail = EmailMultiAlternatives(
            subject, text_content, from_email, [to_email])
        mail.attach_alternative(html, "text/html")
        mail.send()

        response = {
            "message": "Please use the provided link to reset your password"}

        return Response(response, status=status.HTTP_200_OK)


class ResetPasswordAPIView(APIView):
    """
    This view updates user password and sends a success email to the user
    """
    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordSerializer

    def put(self, request, *args, **kwargs):
        data = request.data
        token = self.kwargs.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except Exception as e:
            if e.__class__.__name__ == 'ExpiredSignatureError':
                raise exceptions.AuthenticationFailed('Token has expired')
            elif e.__class__.__name__ == 'DecodeError':
                raise exceptions.AuthenticationFailed(
                    'Unable to decode the given token')
            else:
                raise exceptions.AuthenticationFailed(str(e))
        reset_type = payload.get('type', '')
        # check the reset type
        if reset_type != 'reset password':
            response = {"message": "Something went wrong try again"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        if data.get('password') != data.get('confirm_password'):
            response = {"message": "Passwords do not match"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        # get user by email/the registered email
        user = User.objects.filter(email=payload.get('email')).first()
        user.set_password(data.get('password'))
        user.save()

        subject = "Password reset notification"
        email = payload.get('email')
        from_email = os.getenv('EMAIL_HOST_USER')
        from_email, to_email, subject = from_email, email, subject
        # render password reset  done template
        html = render_to_string('password_reset_done.html')
        # strip html tags from the html content
        text_content = strip_tags(html)
        # create an email and attach content as html
        mail = EmailMultiAlternatives(
            subject, text_content, from_email, [to_email])
        mail.attach_alternative(html, "text/html")
        mail.send()
        response = {"message": "Password updated successfully"}
        return Response(response, status=status.HTTP_200_OK)
