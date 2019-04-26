"""
    This test module holds tests related to sending of mails
"""
from rest_framework import status
from .base_test import BaseTestCase


class ForgotPasswordTestCase(BaseTestCase):
    """
        This is the class for mail tests
    """

    def test_1new_user_can_register(self):
        """
            A user should be informed of a verification email sent to
            them upon successful registration.
        """
        success_msg = 'activation link has been sent'

        with self.settings(
                EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            res = self.register_new_user(data=self.user_to_register)

        self.assertIn(success_msg, res.data.get('message'))
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_user_receive_reset_link_on_email(self):
        """
        A user should be able to receive a reset link on email
        """
        with self.settings(
                EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            response = self.register_new_user(data=self.user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        with self.settings(
                EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            response = self.forgot_password(
                data={"email": self.user['user']['email']})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_receive_link_with_empty_email(self):
        """
        A user cannot receive a link with unregistered email
        """
        response = self.forgot_password(
            data={"email": ""})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.content,
            b'["Account with that email does not exist."]')

    def test_receive_link_with_unregistered_email(self):
        """
        A user cannot receive a link with unregistered email
        """
        response = self.forgot_password(
            data={"email": self.user['user']['email']})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.content,
            b'["Account with that email does not exist."]')


class TestResetPassword(BaseTestCase):
    """
    Holds tests for reseting password
    """

    def test_password_reset_password(self):
        """Test that a user with valid credentials can reset password"""
        response = self.forgot_password(data=self.reset_password_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_password(self):
        self.reset_password_empty_payload['password'] = "this password"
        response = self.forgot_password(data=self.reset_password_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
