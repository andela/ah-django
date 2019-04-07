from django.conf import settings
from rest_framework_jwt.settings import api_settings

from rest_framework import exceptions
from rest_framework.authentication import (
    get_authorization_header, BaseAuthentication)

import jwt

from .models import User


class JWTokens(object):
    """
    This class will define the setup details which will
    be useful in token generation
    """

    def generate_token(self, user_detail):
        """
        This method generates the token. Components of a JWT include
        1. A header-simply a JSON string but it contains information
            about the algorithm of JWT encryption
        2. A payload-any data that you want to include into JWT
        3. A signature-an encrypted string
        """
        # Get the payload and encoding details from the settings
        payload = api_settings.JWT_PAYLOAD_HANDLER
        encoder = api_settings.JWT_ENCODE_HANDLER

        # The payload is the email
        payload_item = payload(user_detail)
        # The generated token arises from the payload
        generated_token = encoder(payload_item)

        return generated_token


class JWTAuthentication(BaseAuthentication):
    """docstring for JWTAthentication"""

    def authenticate(self, request):
        """
            Custom token auth backend
        """
        payload = get_authorization_header(request).split()
        if not payload or payload[0].decode().lower() != 'bearer':
            return None
        if len(payload) != 2:
            raise exceptions.AuthenticationFailed('Invalid token')
        return self.authenticate_user(payload[1].decode('utf-8'))

    def authenticate_user(self, token):
        """
            Decodes the auth token
        """
        try:
            auth_payload = jwt.decode(token, settings.SECRET_KEY)
        except Exception as ex:
            exceptions.AuthenticationFailed(ex)
            print(ex)
        user = User.objects.get(email=auth_payload.get('email'))
        if not user:
            user = User.objects.get(username=auth_payload.get('username'))
        return user, token
