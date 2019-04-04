from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
import json


class BaseTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.postlist_article_url = '/api/articles/'
        self.get_article_url = '/api/articles/{article_id}/'
        self.user_signup = {
            "user": {
                "email": "testuser@gmail.com",
                "username": "testuser",
                "password": "testuserpass123"
            }
        }
        self.article = {
            "article": {
                "title": "This is the article title",
                "description": "This is the article description",
                "body": "This is the article body",
                "image_url": "https://imageurl.com"
            }

        }

        self.edit_article = {
            "title": "This article title is edited",
            "body": "This article body is edited"
        }

        self.signup = self.client.post(
            "/api/users",
            self.user_signup,
            format="json"
        )

        self.credentials = json.loads(self.signup.content)[
            "user"]["token"]
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.credentials)

    def create_article(self, data=None):
        """ method for creating and article """
        data = data

        return self.client.post(
            self.postlist_article_url,
            data,
            format='json', follow=True
        )
