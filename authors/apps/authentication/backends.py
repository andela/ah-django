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
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
from .models import User


class JWTAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        """
            This method checks if the token is valid
            the return value is the users token
        """

        auth = authentication.get_authorization_header(request).split()

        # Ensure we have a token
        # get_authorization_header returns headers as bytesstring
        # hence the need to check
        # against b'token'

        if not auth or auth[0].lower() != b'bearer':
            return None
        try:
            token = auth[1]

        except UnicodeError:
            message = "Token contains invalid characters"
            raise AuthenticationFailed(message)
        # Attempt decoding the token
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except:
            raise AuthenticationFailed('Invalid token.')

        # Get the user owning the token by the decoded email prop
        try:
            user = User.objects.get(email=payload['email'])
        except User.DoesNotExist:
            raise AuthenticationFailed('No user found for token provided')

        return (user, token)

    def validate_token(self, token):
        # we use the same key for encoding as well

        try:
            jwt.decode(token, settings.SECRET_KEY)
        except jwt.DecodeError or jwt.InvalidTokenError:
            return False
        except jwt.ExpiredSignature:
            return False
        return True
