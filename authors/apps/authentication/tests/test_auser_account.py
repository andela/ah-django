"""
    This test module holds tests related to user accounts
"""
from rest_framework import status

from .base_test import BaseTestCase


class TestUser(BaseTestCase):
    """
        Holds user account tests
    """

    def test_user_signin_with_missing_fields(self):
        user_details = {
            "user": {
                "username": "mather",
                "email": "",
                "bio": "I am he",
                "password": "mather@12345"
            }
        }
        response = self.client.post(self.registration_path,
                                    user_details, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_signin_with_invalid_email(self):
        user_details = {
            "user": {
                "username": "mather",
                "email": "gdttyfd",
                "bio": "I am he",
                "password": "mather@12345"
            }
        }
        response = self.client.post(self.registration_path,
                                    user_details, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_signin_with_invalid_password(self):
        user_details = {
            "user": {
                "username": "matherw",
                "email": "gdttyfd@gmail.com",
                "bio": "I am he",
                "password": "refdfdsqsd"
            }
        }
        response = self.client.post(self.registration_path,
                                    user_details, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
