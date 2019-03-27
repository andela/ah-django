import os
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

        self.user_to_register = {
            'user': {
                'username': 'author',
                'email': 'author@haven.com',
                'password': 'Ag00dacc3ss!'
            }
        }

    def register_new_user(self, data={}):
        """
            Creates a new user account and returns the request response
        """
        return self.client.post(self.registration_path,
                                data=data,
                                format='json')