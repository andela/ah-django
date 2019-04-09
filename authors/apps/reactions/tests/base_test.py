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

        self.article_mock = {
            'article': {
                'title': 'Funny things on the keyboard',
                'description': 'Suggestion for the \
            name of that other funny thing',
                'body': 'Now how do we go about this other thing...',
                'author': 1
            }
        }

        self.mock_comment = {
            'comment': {
                'body': "The chairs are sticky",
                "author": 1,
                'article': 1
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
        self.create_article(data=self.article_mock)
        self.setup_for_comments()

    def register_user(self, path=None, data={}):
        """
            Registers users to be used in testing
        """
        path = path if path else self.registration_path

        with self.settings(
                EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            res = self.client.post(path, data=data, format='json')

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

        resp = self.client.get(path)
        return resp.json().get('comments').get('data')[0].get('id')

    def get_article_slug(self, data={}, rel_path='/comments', created=False):
        """
            Returns a url path to post an articles reaction
        """
        if created:
            return self.articles_path + \
                'funny-things-on-the-keyboard_GoodCow' + rel_path
        if not data:
            data = self.create_article()
        return self.articles_path + \
            data.json().get('slug') + rel_path

    def post_article_comment(self, path, data={}):
        """
            Posts a comment to a test article
        """
        data = self.mock_comment if not data else data
        return self.client.post(
            path,
            data=data,
            format='json')

    def post_reply_to_comment(self, data={}):
        """
            Posts a reply to a comment
        """

        data = self.reply if not data else data

        comment_path = self.get_single_comment_path()
        path = self.get_article_slug(created=True)
        self.post_article_comment(path)

        return self.client.post(
            f'{path}/{comment_path}/reply',
            data=data,
            format='json')

    def get_single_reply_path(self, rel_path=''):
        """
            Returns the absolute URL for
            testing a reply to article comments
        """
        if not rel_path:
            res = self.post_reply_to_comment()
            rel_path = res.json().get('replies').get('data').get('id')

        comment_path = self.get_single_comment_path()
        path = self.get_article_slug(created=True)
        self.post_article_comment(path)

        return f'{path}/{comment_path}/reply/{rel_path}'

    def setup_for_comments(self):
        pass
