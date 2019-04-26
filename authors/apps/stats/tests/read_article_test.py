"""
    This test module holds tests for the Reader Stats
"""
from rest_framework import status

from .base_test import ReaderStatsBaseTestCase


class TestReaderStats(ReaderStatsBaseTestCase):
    """
        Holds tests for the user views and read count
    """

    def test_add_read_to_article(self):
        """
            Verify: Sending a read request to an article increaments

        """
        path = self.get_article_slug(created=True)

        res = self.client.post(path, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_get_read_stats(self):
        """
            Verifies: User should be able to see their views and read count
        """

        path = self.articles_path
        path_ = ''.join(path.split('articles')[
                        :-1]) + 'profiles/GoodCow/stats/'

        res = self.client.get(path_)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_read_stats_as_nonowner(self):
        """
            Verifies: Stats visible to profile owner only
        """

        path = self.articles_path
        path = ''.join(path.split('articles')[
                       :-1]) + 'profiles/MissingCow/stats/'

        res = self.client.get(path)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
