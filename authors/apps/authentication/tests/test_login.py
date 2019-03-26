"""
this file contains all tests pertaining user login
"""
# import json
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
import json


class RegistrationTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_1 = {
            "user": {
                "email": "premiermember@gmail.com",
                "username": "Premier Member",
                "password": "premiermember2019"
            }
        }
        self.user1_login = {
            "user": {
                "email": "premiermember@gmail.com",
                "password": "premiermember2019"
            }
        }
        self.user1_login_wrong_password = {
            "user": {
                "email": "premiermember@gmail.com",
                "password": "premiermember2018"
            }
        }

        self.user1_login_missing_email = {
            "user": {
                "password": "premiermember2018"
            }
        }

        self.user1_login_missing_password = {
            "user": {
                "email": "premiermember@gmail.com",
            }
        }

        self.user1_invalidmail = {
            "user": {
                "email": "premiermembil.com",
                "username": "premier member",
                "password": "premiermember2019"
            }
        }

    def signup(self):
        return self.client.post(
            "/api/users", self.user_1, format="json")

    def test_normal_user_login(self):
        """
        test a normal user login with no abnormalities
        """
        self.signup()
        login_user = self.client.post(
            "/api/users/login/", self.user1_login, format="json")
        self.assertEqual(login_user.status_code,
                         status.HTTP_200_OK)
        self.assertIn('username', login_user.data)
        self.assertIn('email', login_user.data)

    def test_login_with_wrong_password(self):
        """
            test user login with a wrong password
        """
        self.signup()
        login_user = self.client.post(
            "/api/users/login/", self.user1_login_wrong_password,
            format="json")
        self.assertEqual(login_user.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(login_user.content),
            {"errors":
             {"error":
              ["A user with this email and password was not found."]}})

    def test_login_with_missing_email(self):
        """
            test user login with missing email
        """
        self.signup()
        login_user = self.client.post(
            "/api/users/login/", self.user1_login_missing_email,
            format="json")
        self.assertEqual(login_user.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(login_user.content),
            {"errors":
             {"email":
              ['This field is required.']}})

    def test_login_with_missing_password(self):
        """
            test user login with missing password
        """
        self.signup()
        login_user = self.client.post(
            "/api/users/login/", self.user1_login_missing_password,
            format="json")
        self.assertEqual(login_user.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(login_user.content),
            {"errors":
             {"password":
              ['This field is required.']}})

    def test_user_login_with_invalid_mail(self):
        """
        test user logging into the app with an invalid mail
        """
        self.signup()
        login_user = self.client.post(
            "/api/users/login/", self.user1_invalidmail, format="json")
        self.assertEqual(login_user.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(login_user.content),
            {"errors":
             {"error":
              ['A user with this email and password was not found.']}})

    def test_user_login_unregistered_user(self):
        """
        test user logging into the app with an
        account that isnt saved
        """
        login_user = self.client.post(
            "/api/users/login/", self.user1_login, format="json")
        self.assertEqual(login_user.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(login_user.content),
            {'errors':
             {'error':
              ['A user with this email and password was not found.']}})
