"""
    This test module holds tests related to user accounts
"""
from django.test import TestCase

from authors.apps.authentication.models import User


class UserModelTest(TestCase):
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
