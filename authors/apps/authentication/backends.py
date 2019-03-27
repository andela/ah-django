"""
    This Class will be checking for the
    Authorization header if it does exist in the headers list
    and will also be checking if the format of the Authorization
    value is
    token thetokenhere
    ie:
    Authorization: token yourtokenhere
"""
import jwt

from django.conf import settings
from django.http import HttpResponse
from rest_framework import authentication, exceptions
from rest_framework import status

from .models import User


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        """
            This method checks if the token is valid

        """
        auth = authentication.get_authorization_header(request).split()
        # get_authorization_header returns headers as bytesstring
        # hence the need to check
        # against b'token'
        if not auth or auth[0].lower() != b'token':
            return None

        if len(auth) != 2:
            message = "Token header is invalid"
            raise exceptions.AuthenticationFailed(message)

        try:
            token = auth[1]

        except UnicodeError:
            message = "Token contains invalid characters"
            raise exceptions.AuthenticationFailed(message)

        # once all the above checks have passed its now time
        # to check if the token belongs to an actual user
        # by decoding it and checking against the email address
        return self.authenticate_credentials(token)

        def authenticate_credentials(self, token):
            """
                checks if the token belongs to a valid user.
            """
        # we use the same key for encoding as well
        payload = jwt.decode(token, settings.SECRET_KEY)
        email = payload['email']
        try:
            user = User.objects.get(
                email=email,
                is_active=True
            )
            if not user:
                message = "User does not exist"
                raise exceptions.AuthenticationFailed(message)
        except jwt.DecodeError or jwt.InvalidTokenError:
            return HttpResponse(
                {'Error': "Token is invalid"},
                status=status.HTTP_403_FORBIDDEN)
        except jwt.ExpiredSignature:
            return HttpResponse(
                {'Error': "The token has expired, Kindly generate a new one"},
                status=status.HTTP_403_FORBIDDEN)

        return user, token
