"""
    This module contains tests for article
    comment functionality
"""
from rest_framework import status

from .base_test import CommentsBaseTestCase


class TestComment(CommentsBaseTestCase):
    """
        Article comments tests
    """

    def test_user_can_create_comment(self):
        """
            An authenticated user should be able to
            post a comment to an article
        """

        path = self.get_article_slug()
        res = self.post_article_comment(path)

        self.assertEqual(res.json().get('comments')
                         .get('message'), 'Comment created')

    def test_comment_to_nonexistent_article(self):
        """
            Comments should be made to articles that exist
        """
        fail_msg = 'nonexistent'

        path = '/api/articles/missing-article/comments'
        res = self.post_article_comment(path)
        print(res.json())

        self.assertIn(fail_msg, res.json().get('errors')
                      .get('detail'))

    def test_get_individual_article_comment(self):
        """
            A single article should be retrieved by its ID
        """

        comment_path = self.get_single_comment_path()
        path = self.get_article_slug(created=True)
        self.post_article_comment(path)

        resp = self.client.get(f'{path}/{comment_path}')

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_delete_article_comment(self):
        """
            A user should be able to delete existing comments
        """

        comment_path = self.get_single_comment_path()
        path = self.get_article_slug(created=True)
        self.post_article_comment(path)

        resp = self.client.delete(f'{path}/{comment_path}')

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_update_comment_to_an_existing_comment(self):
        """
            A user shouldn't reword a comment to
            match one present on the article
        """

        comment_path = self.get_single_comment_path()
        path = self.get_article_slug(created=True)
        self.post_article_comment(path)
        msg = "You've posted a similar comment before"

        self.client.post(f'{path}/{comment_path}',
                         data=self.comment, format='json')

        resp = self.client.put(
            f'{path}/{comment_path}',
            data=self.comment,
            format='json')
        self.assertEqual(resp.json().get('comments')
                         .get('message'),
                         msg)

    def test_update_existing_comment(self):
        """
            Verifies: A user shouldn't reword a comment
        """

        comment_path = self.get_single_comment_path()
        path = self.get_article_slug(created=True)
        self.post_article_comment(path)

        comment = {
            "comment": {"body": "It's Avocado"}
        }
        new_comment = {
            "comment": {"body": "yeaaah, but Ovacado sounds fancier"}
        }

        self.client.post(f'{path}',
                         data=comment, format='json')

        resp = self.client.put(
            f'{path}/{comment_path}',
            data=new_comment,
            format='json')
        self.assertEqual(resp.json().get('comments')
                         .get('body'),
                         new_comment.get('comment').get('body'))

    def test_post_existing_comment(self):
        """
            An article should not have identical comments
        """
        path = self.get_article_slug(created=True)
        resp = self.post_article_comment(path)
        msg = "posted an exact comment"

        resp = self.client.post(
            f'{path}',
            data=self.comment,
            format='json')
        self.assertIn(msg, resp.json().get('comments').get('message'))
        self.assertTrue(resp.status_code, status.HTTP_409_CONFLICT)

    def test_get_missing_comment(self):
        comment_path = 404
        path = self.get_article_slug(created=True)
        self.post_article_comment(path)

        self.client.delete(f'{path}/{comment_path}')
        resp = self.client.get(f'{path}/{comment_path}')
        self.assertEqual(resp.json().get('comments').get(
            'error'), 'Comment of ID 404 nonexistent')

    def test_create_comment_with_invalid_body(self):
        """
           Validate: comment shouldn't be made of characters
           only
        """

        path = self.get_article_slug()
        comment = {
            'comment': {
                'body': "5)))89"
            }
        }
        res = self.post_article_comment(path, data=comment)

        self.assertIn("Provide a readable comment, cool?",
                      res.json().get('comments') .get('errors').get('body')[0])

    def test_retrieve_comment_history(self):
        """
            Validate: History records of comments can be seen
        """
        comment_path = self.get_single_comment_path()
        path = self.get_article_slug(created=True)
        self.post_article_comment(path)

        self.client.post(f'{path}/{comment_path}',
                         data=self.comment, format='json')

        resp = self.client.get(
            f'{path}/{comment_path}/history')

        self.assertIn('comment_history',
                      resp.json().get('comments').keys(),
                      )
