"""
This is the basetest file where you can access the token
from instead of rewriting the signup functionality over and over again
"""

from rest_framework.test import APITestCase, APIClient
import json


class BaseTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_1 = {
            "user": {
                "email": "premiermember@gmail.com",
                "username": "Premier Member",
                "password": "premiermember2019"
            }
        }

        self.newuser = self.client.post(
            "/api/users", self.user_1, format="json")
        self.token = json.loads(self.newuser.content)[
            "user"]["token"]
