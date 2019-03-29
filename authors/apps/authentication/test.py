from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status


class UserSignupTest(APITestCase):
    """ Tests for user signup """

    def setUp(self):
        """ This method does the preliminary setup """
        # We first create a user_client
        self.client = APIClient()
        # We define the URL for user sign up
        self.user_signup_url = reverse("authentication:signup")

    def test_new_user_login(self):
        """
        We test whether we can create a new user
        """

        user_details = {
                "user": {
                        "username": "yhghytfgh",
                        "email": "gdttyfdg@gmail.com",
                        "bio": "I am he",
                        "password": "mather@12345"
                        }
                    }
        response = self.client.post(
            self.user_signup_url,
            user_details, format='json'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(response.data['email'], user_details['user']['email'])

    def test_user_signin_with_missing_fields(self):
        user_details = {
                "user": {
                        "username": "mather",
                        "email": "",
                        "bio": "I am he",
                        "password": "mather@12345"
                        }
                    }
        response = self.client.post(
            self.user_signup_url,
            user_details, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_signin_with_invalid_email(self):
        user_details = {
                "user": {
                        "username": "mather",
                        "email": "gdttyfd",
                        "bio": "I am he",
                        "password": "mather@12345"
                        }
                    }
        response = self.client.post(
            self.user_signup_url,
            user_details, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_signin_with_a_short_password(self):
        user_details = {
                "user": {
                        "username": "mather",
                        "email": "gdttyfdg@gmail.com",
                        "bio": "I am he",
                        "password": "mat"
                        }
                    }
        response = self.client.post(
            self.user_signup_url,
            user_details, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
