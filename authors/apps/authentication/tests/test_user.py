"""
    This test module holds tests related to user accounts
"""
from rest_framework import status

from .base_test import BaseTestCase


class TestUser(BaseTestCase):
    """
        Holds user account tests
    """

    def test_new_user_can_register(self):
        """
            A user should be informed of a verification email sent to
            them upon successful registration.
        """
        success_msg = 'sent to your email'

        with self.settings(
                EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
                res = self.register_new_user(data=self.user_to_register)

        self.assertIn(success_msg, res.data.get('message'))
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
