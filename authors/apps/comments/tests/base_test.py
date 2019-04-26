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

        self.comment = {
            'comment': {
                'body': "The tables are stickier",
                "author": 1,
                'article': 1
            }
        }

        self.reply = {
            'comment': {
                'body': "A little salty"
            }
        }
        path = self.get_article_slug(created=True)
        self.post_article_comment(
            path=path, data=self.comment)
