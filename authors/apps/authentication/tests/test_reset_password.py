"""
this file contains tests for reset password

"""
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from django.urls import reverse


class ResetPasswordTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.reset_password_url = reverse('password_reset')
        self.user_register = {
            "user": {
                "email": "premiermember@gmail.com",
                "username": "premier",
                "password": "premiermemberpass001"
            }
        }

        self.old_pass = {
            "user": {
                "email": "premiermember@gmail.com",
                "password": "premiermemberpass001"
            }
        }
        self.user_login = {
            "user": {
                "email": "premiermember@gmail.com",
                "password": "newpassword1234"
            }
        }

        self.empty_email = {
            "user": {
                "email": ''
            }
        }

        self.reset_password_email = {
            "user": {
                "email": 'premiermember@gmail.com'
            }
        }

        self.unregistered_email = {
            "user": {
                "email": "premier01@gmail.com",
            }
        }

        self.reset_password_data = {
            "new_password": "newpassword1234",
            "re_new_password": "newpassword1234"
        }

    def signup(self):
        """
        method for signing up a user
        return user id and token
        """

        self.client.post(
            "/api/users",
            self.user_register,
            format="json"
        )

    def password_rest(self, data=None):
        self.signup()

        return self.client.post(
            reverse('password_reset'),
            data,
            format="json"
        )

    def test_reset_password(self):
        data = self.reset_password_email

        reset_password = self.password_rest(data)

        self.assertEqual(reset_password.status_code,
                         status.HTTP_200_OK)

    def test_no_email(self):
        data = self.empty_email

        empty_email = self.password_rest(data)

        self.assertEqual(empty_email.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_unregistered_email(self):
        data = self.unregistered_email
        unregistered_email = self.password_rest(data)

        self.assertEqual(unregistered_email.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_reset_password_confirm(self):

        self.signup()

        reset_password = self.client.post(
            reverse('password_reset'),
            self.reset_password_email,
            format="json"
        )

        data = reset_password.data

        uid = data['uid']
        token = data['token']

        reset_password_url = reverse('password_reset_confirm')
        extra_params = '?uid={}&token={}'.format(uid, token)
        new_url = (reset_password_url + extra_params)

        reset_response = self.client.patch(
            new_url, self.reset_password_data,
            format="json"
        )

        old_password_login = self.client.post(
            "/api/users/login/", self.old_pass,
            format="json"
        )

        new_password_login = self.client.post(
            "/api/users/login/", self.user_login,
            format="json"
        )

        self.assertEqual(reset_response.status_code,
                         status.HTTP_200_OK)

        self.assertEqual(old_password_login.status_code,
                         status.HTTP_400_BAD_REQUEST)

        self.assertEqual(new_password_login.status_code,
                         status.HTTP_200_OK)
