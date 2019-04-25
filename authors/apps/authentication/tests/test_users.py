"""
These are tests for users endpoint
"""
# import json
from rest_framework.test import APITestCase
from rest_framework.views import status
import json


class UserListTestCase(APITestCase):
    def setUp(self):
        self.user_1 = {
            "user": {
                "email": "premiermember@gmail.com",
                "username": "premiermember",
                "password": "premiermember2019"
            }
        }
        self.user_2 = {
            "user": {
                "email": "premiermember2@gmail.com",
                "username": "premiermember2",
                "password": "premiermember2019"
            }
        }
        self.newuser = self.client.post(
            "/api/users", self.user_1, format="json")
        self.token = json.loads(self.newuser.content)[
            "user"]["token"]

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_user_list(self):
        """
        List users Test
        """

        user_list = self.client.get('/api/users/list')
        data = json.loads(user_list.content)
        self.assertEqual(user_list.status_code, status.HTTP_200_OK)
        self.assertEqual(data, json.loads(
            """[{"email":"premiermember@gmail.com",
                "username":"premiermember", "bio": "", "image": ""}
                ]
            """))

    def test_user_list_add_one(self):
        """
        List users Test when we add 1 user
        """
        user_list = self.client.get('/api/users/list')
        data = json.loads(user_list.content)
        length = len(data)
        self.client.post(
            "/api/users", self.user_2, format="json")
        user_list = self.client.get('/api/users/list')
        data2 = json.loads(user_list.content)
        self.assertEqual(user_list.status_code, status.HTTP_200_OK)
        self.assertTrue(len(data2)-length, 1)

    def test_user_list_without_login(self):
        """
        List users Test without login
        """
        self.client.credentials()
        user_list = self.client.get('/api/users/list')
        self.assertEqual(user_list.status_code, status.HTTP_403_FORBIDDEN)
