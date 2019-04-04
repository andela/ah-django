"""
this file contains tests to see whether an email is sent
upon successful registration
"""
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from django.core import mail


class EmailRegistrationTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_1 = {
            "user": {
                "email": "newmember@gmail.com",
                "username": "New_Member",
                "password": "newmember000"
            }
        }

    def test_email_notifications(self):
        """
        test if email is recieved on successful
        registration
        """
        outbox_length = len(mail.outbox)
        new_user = self.client.post(
            "/api/users", self.user_1, format="json")
        self.assertEqual(new_user.status_code,
                         status.HTTP_201_CREATED)
        self.assertTrue(len(mail.outbox) == outbox_length + 1)
