from django.urls import reverse
from rest_framework.test import APITestCase, APIClient


class BookmarkTestBase(APITestCase):
    """
    This is the base test class that shall be inherited by article test files
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
        self.user1 = {
            "user": {
                "username": "tester1",
                "email": "tester1234@gmail.com",
                "password": "tester232#$$"
            }
        }
        self.user_login_details = {
            "user": {
                "username": "tester1",
                "email": "tester123@gmail.com",
                "password": "tester232#$$"}
        }
        self.user_login_details1 = {
            "user": {
                "username": "tester1",
                "email": "tester1234@gmail.com",
                "password": "tester232#$$"}
        }
        self.article = {
            "article": {
                "title": "How to milk a grade one cow",
                "description": "Ever wonder how?",
                "body": "It takes a courage",
                "tagList": ["writing", "training"]
            }
        }
        self.client = APIClient()
        self.register_url = reverse('authentication:activation')
        self.login_url = reverse('authentication:login')
        self.articles_url = reverse('articles:new_article')
        self.bookmark_url = reverse('bookmark:get-bookmark')
        self.register_user(self.user)
        self.register_user(self.user1)
        self.token1 = self.login_a_user(self.user_login_details)['token']
        self.token2 = self.login_a_user(self.user_login_details1)['token']

    def register_user(self, data):
        """register a user"""
        return self.client.post(self.register_url, data, format='json')

    def login_a_user(self, data):
        """Login a user"""
        return self.client.post(self.login_url, data, format='json').data

    def authorize_user(self, user_details):
        """Register and login user to obtain token"""
        self.register_user(data=self.user)
        payload = self.login_a_user(data=user_details)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + payload['token'])

    def post_article_req(self, data):
        return self.client.post(
            self.articles_url,
            data=data,
            HTTP_AUTHORIZATION='Bearer ' + self.token1,
            format="json")

    def toogle_bookmark_feature(self):
        """ Article bookmark toogle """
        response = self.post_article_req(self.article)
        # print(response.data.get('slug', ''))
        url = reverse('bookmark:bookmark-article',
                      kwargs={
                          'slug': response.data.get('slug', '')
                      })
        bookmark_response = self.client.post(url,
                                             HTTP_AUTHORIZATION='Bearer ' +
                                             self.token1, format="json")
        res_unmark = self.client.delete(url,
                                        HTTP_AUTHORIZATION='Bearer ' +
                                        self.token1, format="json")
        return (bookmark_response,  res_unmark)
