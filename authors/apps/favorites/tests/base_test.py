from django.urls import reverse

from rest_framework.test import APITestCase, APIClient


def generate_slug_url(slug):
    """Include slug in url path"""
    full_url = reverse('favorites:user-favorite', args=[slug])
    return full_url


class FavoriteTestBase(APITestCase):
    """
    This is the base test class that shall be inherited by favorite test files
    """

    def setUp(self):
        """Set up configurations that shall be run every time a test runs"""
        self.user = {
            "user": {
                "username": "tester",
                "email": "tester123@gmail.com",
                "password": "tester232#$$"
            }
        }
        self.second_user = {
            "user": {
                "username": "tester",
                "email": "tester123@gmail.com",
                "password": "tester232#$$"}
        }
        self.article = {
            "article":  {
                "slug": "how-to-train-your-dragon",
                "title": "How to train your dragon",
                "description": "Ever wonder how?",
                "body": "It takes a Jacobian",
                "tagList": ["dragons", "training"]
            }
        }
        self.article_slug = "how-to-train-your-dragon_tester"
        self.non_existent_article_slug = "article-not-existing_me"
        self.client = APIClient()
        self.registration_path = reverse('authentication:activation')
        self.login_path = reverse('authentication:login')
        self.all_favorites_url = reverse('favorites:user-favorites')
        self.new_article_path = reverse('articles:new_article')
        self.articles_feed = reverse('articles:articles_feed')

    def register_user(self, data):
        return self.client.post(
            self.registration_path,
            data,
            format='json'
        )

    def login_a_user(self, data):
        return self.client.post(
            self.login_path,
            data,
            format='json'
        ).data

    def authorize_user(self, user_login_details):
        """
        Obtain token for access to protected endpoints
        """
        with self.settings(
                EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            self.register_user(data=self.user)
        payload = self.login_a_user(data=user_login_details)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + payload['token'])
