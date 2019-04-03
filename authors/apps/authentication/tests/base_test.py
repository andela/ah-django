"""
    This module contains the base test class
"""

from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.test.client import RequestFactory

import django

django.setup()


class BaseTestCase(APITestCase):
    """
        Holds the base authentication attributes and test methods
    """

    def setUp(self):
        """
            Creates reusable mock data and test functions.
        """
        self.client = APIClient()
        self.registration_path = reverse('authentication:activation')
        self.factory = RequestFactory()
        self.forgot_password_url = reverse('authentication:forgot_password')

        self.user_to_register = {
            'user': {
                'username': 'GoodCow',
                'email': 'cow@mammals.milk',
                'password': 'badA55mammal!',
                'bio': 'bio'
            }
        }

        self.user = {
            "user": {
                "email": "authorshaven2@gmail.com",
                "username": "test_me1",
                "password": "testuser!23",
                "bio": "I love programming"
            }
        }

        self.reset_password_data = {
            "password": "Itr!3d21",
            "confirm_password": "Itr!3d21"
        }

        self.reset_password_empty_payload = {
            "email": "",
        }

        self.reset_password_correct_email = {
            "email": "cow@mammals.milk",
        }

    def register_new_user(self, data={}):
        """
            Creates a new user account and returns the request response
        """
        return self.client.post(self.registration_path,
                                data=data,
                                format='json')

    def forgot_password(self, data):
        return self.client.post(
            self.forgot_password_url,
            data=data,
            format="json")
