from django.urls import reverse

from rest_framework.test import APITestCase, APIClient

import django

django.setup()


class BaseTestCase(APITestCase):
    """
        Holds mock data and resuable test methods
    """

    def setUp(self):
        """
            Creates attributes to be used in testing
            of the application
        """
        self.client = APIClient()
        self.registration_path = reverse('authentication:activation')
        self.login_path = reverse('authentication:login')
        self.articles_path = reverse('articles:new_article')

        self.mock_user = {
            'user': {
                'username': 'GoodCow',
                'email': 'cow@mammals.milk',
                'password': 'badA55mammal!'}
        }

        self.mock_user_ = {
            'user': {
                'username': 'GoodOldCow',
                'email': 'cow@fancymammals.milk',
                'password': 'badA55mammal!',
                'bio': 'bio'
            }
        }
        self.article = {
            'article': {
                'title': 'Funny thing on the keyboard',
                'description': 'Suggestion for the name of that funny thing',
                'body': 'Now how do we go about this...',
                'author': 1
            }
        }
        self.article_slug = 'self.get_article_slug(self.article)'
        self.dislike_path = reverse(
            'user_reactions:reaction-dislike',
            kwargs={'slug': self.article_slug})
        self.like_path = reverse('user_reactions:reaction-like', kwargs={
            'slug': self.article_slug
        })

        self.register_user(data=self.mock_user)
        self.login_user(data=self.mock_user)
        self.setup_for_comments()

    def register_user(self, path=None, data={}):
        """
            Registers users to be used in testing
        """
        path = path if path else self.registration_path

        with self.settings(
                EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            res = self.client.post(path, data=data, format='json')
        print(res)

    def login_user(self, data={}):
        """
            Logs in a registereed test user
        """
        payload = self.client.post(
            self.login_path, data=data, format='json')
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + payload.json().
            get('user').get('token'))

    def create_article(self, data={}):
        """
            Creates an article to test the like
            dislike feature on
        """
        data = data if data else self.article

        return self.client.post(self.articles_path,
                                data=data,
                                format='json')

    def post_article_reaction(self, path):
        """
            Posts a user reaction to test article.
        """
        return self.client.post(path, format='json')

    def get_slug(self, data={}, rel_path='/like'):
        """
            Returns a url path to post an articles reaction
        """

        res = self.articles_path + \
            data.json().get('slug') + rel_path
        return res

    def get_single_comment_path(self):
        """
            Returns a path with a single comment ID
        """

        path = self.get_article_slug(created=True)
        # res = self.post_article_comment(path)

        resp = self.client.get(path)
        return resp.json().get('comments').get('data')[0].get('id')

    def setup_for_comments(self):
        pass
