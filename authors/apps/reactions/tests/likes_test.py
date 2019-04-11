"""
    This module holds tests for the article like-dislike
    feature
"""
from rest_framework import status

from .base_test import BaseTestCase


class TestArticleLike(BaseTestCase):
    """
        Holds test related to article liking and disliking
    """

    def test_like_article(self):
        """
            A liked article should have its reaction (like)
            increament by one
        """
        res = self.create_article()

        path = self.get_slug(data=res, rel_path='/like')
        response = self.post_article_reaction(path)

        self.assertEqual(
            response.json().get('reaction').get('data')
            .get('likes'), 1)
        self.assertTrue(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.json().get('reaction')
                        .get('message') == 'Reaction Created')

    def test_like_an_article_twice(self):
        """
            Posting a second like reaction should delete
            the previous like
        """
        res = self.create_article()

        path = self.get_slug(data=res, rel_path='/like')
        response = self.post_article_reaction(path)

        self.assertEqual(
            response.json().get('reaction').get('data')
            .get('likes'), 1)
        response = self.post_article_reaction(path)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json().get('reaction').get('data')
            .get('likes'), 0)

    def test_dislike_an_article(self):
        """
            Disliking an article should give it a reaction of -1
        """

        res = self.create_article()

        path = self.get_slug(data=res, rel_path='/dislike')
        response = self.post_article_reaction(path)

        self.assertEqual(
            response.json().get('reaction').get('data')
            .get('likes'), 0)
        self.assertEqual(
            response.json().get('reaction').get('data')
            .get('dislikes'), 1)

        self.assertTrue(response.status_code == status.HTTP_201_CREATED)
        self.assertTrue(response.json().get('reaction')
                        .get('message') == 'Reaction Created')

    def test_like_article_as_unauthorized_user(self):
        """
            Non-logged in users should not be able to post article
            likes or dislikes
        """

        res = self.create_article()
        self.client.credentials()

        path = self.get_slug(data=res, rel_path='/dislike')
        response = self.post_article_reaction(path)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_dislike_article_clears_like(self):
        """
            A posted dislike by the same user should
            reset the present like to 0
        """

        res = self.create_article()

        path = self.get_slug(data=res, rel_path='/dislike')
        res_dislike = self.post_article_reaction(path)

        self.assertEqual(
            res_dislike.json().get('reaction').get('data')
            .get('dislikes'), 1)

        path = self.get_slug(data=res, rel_path='/like')
        like_response = self.post_article_reaction(path)

        self.assertEqual(
            like_response.json().get('reaction').get('data')
            .get('dislikes'), 0)

    def test_dislike_nonexistent_article(self):
        """
            A user should not be able to make like or
            dislike requests for missing articles
        """
        path = self.articles_path + 'missing-article-slug/like'
        res = self.post_article_reaction(path)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_like_comment(self):
        """
            Verify: A liked  comment should have its reaction (like)
            increament by one
        """
        path = self.get_article_slug(created=True)
        with self.settings(
                EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            self.post_article_comment(path)
        comment_path = self.get_single_comment_path()

        response = self.client.post(f'{path}/{comment_path}/like')

        self.assertEqual(
            response.json().get('reaction').get('data')
            .get('likes'), 1)
        self.assertTrue(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.json().get('reaction')
                        .get('message') == 'Reaction Created')
