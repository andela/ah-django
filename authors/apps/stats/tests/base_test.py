from authors.apps.reactions.tests.base_test import BaseTestCase


class ReaderStatsBaseTestCase(BaseTestCase):
    """
        Holds mock data and test helpers for the reader stats
    """

    def get_article_slug(self, data={}, rel_path='/read', created=False):
        """
            Returns a url path to post an articles reaction
        """
        self.create_article(data=self.article_mock)

        if created:
            return self.articles_path + \
                'funny-things-on-the-keyboard_GoodCow' + rel_path
