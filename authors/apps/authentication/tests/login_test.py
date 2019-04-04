from rest_framework.views import status
from .base_test import BaseTestCase


class TestUserLogin(BaseTestCase):
    """
            Holds test for handling login
    """

    def test_login_successful(self):
        """User can successfully log in"""

        user_details = {
            "user": {
                "email": "cow@mammals.milk",
                "password": "badA55mammal!"
            }
        }
        with self.settings(
                EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            self.register_new_user(data=self.user_to_register)
        response = self.client.post(
            self.login_path,
            user_details,
            format='json'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertIn("token", response.data)

    def test_login_failure(self):
        """User can unsuccessfully log in"""

        user_details = {
            "user": {
                "email": "cow@mammals.milk",
                "password": "bad"
            }
        }
        with self.settings(
                EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            self.register_new_user(data=self.user_to_register)
        response = self.client.post(
            self.login_path,
            user_details,
            format='json'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertNotIn("token", response.data)
