"""
    This test module holds tests related to user accounts
"""
from rest_framework import status

from .base_test import BaseTestCase
from authors.apps.authentication.models import User


class UserModelTest(BaseTestCase):
    """
    Test for creating a new user account
    """

    def test_create_user(self):
        """
        Test user model can be created successfully
        """
        self.assertIsInstance(
            User.objects.create_user(username="jmehere",
                                     email="j@mehere.com",
                                     password="password"), User)

        data1 = {
            "user": {
                "username": "jmehere",
                "email": "j1@mehere.com",
                "password": "password"
                }
            }

        data2 = {
            "user": {
                "username": "jmehere1",
                "email": "j@mehere.com",
                "password": "password"
                }
            }

        # test duplicate returns 409
        response = self.client.post(self.registration_path,
                                    data=data1,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

        response = self.client.post(self.registration_path,
                                    data=data2,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
