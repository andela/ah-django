"""
this file contains all tests pertaining user signup
"""
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
        self.duplicate_user1email = {
            "user": {
                "email": "premiermember@gmail.com",
                "username": "Premier Member 2",
                "password": "premiermember2019"
            }
        }

        self.duplicate_user1username = {
            "user": {
                "email": "premiermember2@gmail.com",
                "username": "Premier Member",
                "password": "premiermember2019"
            }
        }

        self.missing_email = {
            "user": {
                "username": "Premier Member",
                "password": "premiermember2019"
            }
        }

        self.missing_username = {
            "user": {
                "email": "premiermember2@gmail.com",
                "password": "premiermember2019"
            }
        }
        self.short_password = {
            "user": {
                "email": "premiermember2@gmail.com",
                "username": "premier member",
                "password": "2019"
            }
        }

        self.invalidmail = {
            "user": {
                "email": "premiermembil.com",
                "username": "premier member",
                "password": "premiermember2019"
            }
        }
        self.invalid_password = {
            "user": {
                "email": "premiermember2@gmail.com",
                "username": "premier member",
                "password": "2019*!//]"
            }
        }

    def test_normal_user_registration(self):
        """
        test a normal user registration with no abnormalities
        """
        register_new_user = self.client.post(
            "/api/users", self.user_1, format="json")
        self.assertEqual(register_new_user.status_code,
                         status.HTTP_201_CREATED)
        self.assertIn('username', register_new_user.data)

    def test_double_sign_up_with_same_credentials(self):
        """
            test that a user cannot register twice in the app
        """
        self.client.post(
            "/api/users", self.user_1, format="json")
        res = self.client.post(
            "/api/users", self.user_1, format="json")
        self.assertEqual(res.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(res.content),
                         {"errors":
                          {"email": ["user with this email already exists."],
                           "username":
                           ["user with this username already exists."]}})

    def test_signup_with_existent_email(self):
        """
            this tests a user signing up with an existent email
        """
        self.client.post(
            "/api/users", self.user_1, format="json")
        res = self.client.post(
            "/api/users", self.duplicate_user1email, format="json")
        self.assertEqual(res.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(res.content),
                         {"errors":
                          {"email": ["user with this email already exists."]}})

    def test_signup_with_existent_username(self):
        """
            this tests a user signing up with an existent username
        """
        self.client.post(
            "/api/users", self.user_1, format="json")
        res = self.client.post(
            "/api/users", self.duplicate_user1username, format="json")
        self.assertEqual(res.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(res.content),
                         {"errors":
                          {"username":
                              ["user with this username already exists."]}})

    def test_missing_user_email(self):
        """
        test a normal user registration with no email
        """
        register_new_user = self.client.post(
            "/api/users", self.missing_email, format="json")
        self.assertEqual(register_new_user.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(register_new_user.content),
                         {"errors": {"email": ["This field is required."]}})

    def test_missing_user_username(self):
        """
        test a normal user registration with no username
        """
        register_new_user = self.client.post(
            "/api/users", self.missing_username, format="json")
        self.assertEqual(register_new_user.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(register_new_user.content),
                         {"errors": {"username": ["This field is required."]}})

    def test_user_registration_with_short_password(self):
        """
        test user registering into the app with a short password
        """
        register_new_user = self.client.post(
            "/api/users", self.short_password, format="json")
        self.assertEqual(register_new_user.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(register_new_user.content),
                         {"errors":
                          {"password":
                           ["Ensure this field has at least 8 characters."]}})

    def test_user_registration_with_invalid_mail(self):
        """
        test user registering into the app with an invalid mail
        """
        register_new_user = self.client.post(
            "/api/users", self.invalidmail, format="json")
        self.assertEqual(register_new_user.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(register_new_user.content),
                         {"errors":
                          {"email":
                           ['Enter a valid email address.']}})

    def test_user_registration_with_invalid_password(self):
        """
        test user registering into the app with an invalid password
        """
        register_new_user = self.client.post(
            "/api/users", self.invalid_password, format="json")
        self.assertEqual(register_new_user.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(register_new_user.content),
                         {"errors":
                          {"password":
                           ["Ensure this field only has alphanumerics."]}})
        
    def test_getting_token_after_signup(self):
        """
        test a normal user will get a token upon signup
        """
        register_new_user = self.client.post(
            "/api/users", self.user_1, format="json")
        self.assertEqual(register_new_user.status_code,
                         status.HTTP_201_CREATED)
        self.assertIn('token', json.loads(register_new_user.content)["user"])
