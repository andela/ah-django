"""
    This module holds the base test class for
    the comments tests
"""

import django

from authors.apps.reactions.tests.base_test import BaseTestCase


django.setup()


class CommentsBaseTestCase(BaseTestCase):
    """
        Holds test data and methods for reuse in
        testing the article comments
    """

    def setup_for_comments(self):

        self.mock_comment = {
            'comment': {
                'body': "The chairs are sticky",
                "author": 1,
                'article': 1
            }
        }

        self.comment = {
            'comment': {
                'body': "The tables are stickier",
                "author": 1,
                'article': 1
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
        self.reply = {
            'comment': {
                'body': "A little salty"
            }
        }
        data_ = self.create_article(data=self.article_mock)
        path = self.get_article_slug(data=data_)
        self.post_article_comment(
            path=path, data=self.comment)

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
