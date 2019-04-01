from rest_framework_jwt.settings import api_settings


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


class JWTAuthentication(object):
    """docstring for JWTAthentication"""

    def __init__(self):
        pass

    def authenticate(self, request):
        pass
