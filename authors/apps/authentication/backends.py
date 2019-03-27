# import jwt
#
# from django.conf import settings
#
# from rest_framework import authentication, exceptions
#
# from .models import User

"""Configure JWT Here"""


class JWTAuthentication(object):
    """docstring for JWTAthentication"""

    def __init__(self, arg):
        super(JWTAuthentication, self).__init__()
        self.arg = arg