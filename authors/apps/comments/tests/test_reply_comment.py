"""
    Contains the test class for replies to comments
"""
from rest_framework import status

from .base_test import CommentsBaseTestCase


class TestCommentReply(CommentsBaseTestCase):
    """
       Holds tests for replies to article comments
    """

    def test_make_reply_to_comment(self):
        """
            Verifies: A user should be able to post a reply to
            an existing article comment
        """
        path = self.get_article_slug(created=True)
        self.post_article_comment(path)

        res = self.post_reply_to_comment()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_get_replies_to_comment(self):
        """
            Get request for all replies
        """
        comment_path = self.get_single_comment_path()
        path = self.get_article_slug(created=True)
        self.post_article_comment(path)

        res = self.client.get(f'{path}/{comment_path}/reply')

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_individual_comment_reply(self):
        """
            Verifies: Retrieve reply by comment ID
        """

        path = self.get_single_reply_path()
        res = self.client.get(path)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_comment_reply(self):
        """
            Verifies: user should be able to update an exisiting comment
        """

        path = self.get_single_reply_path()

        res = self.client.put(path)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_comment_reply(self):
        """
            Verifies: Authors of the replies should be able to delete them
        """

        path = self.get_single_reply_path()

        res = self.client.delete(path)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_reply_to_nonexistent_comment(self):
        """
            Verifies: Replies should only be made to comments
            present on an article
        """
        comment_path = 404
        fail_msg = 'Comment of ID 404 nonexistent'

        path = self.get_article_slug(created=True)
        self.post_article_comment(path)
        res = self.client.get(f'{path}/{comment_path}/reply')

        self.assertEqual(res.json().get('errors').get('detail'), fail_msg)

    def test_post_same_reply_to_comment_twice(self):
        """
            Verifes: Replies should be unique to
                a comment for each author
        """
        fail_msg = "Seems you've posted an exact comment before"

        self.post_reply_to_comment()
        res = self.post_reply_to_comment()

        self.assertEqual(res.json().get('replies').get('message'),
                         fail_msg)

    def test_get_missing_comment_reply(self):
        """
            Verifies: Return error for retirieval of
                missing reply ID
        """
        message = 'Comment reply of ID 404 nonexistent'
        path = self.get_single_reply_path(rel_path=404)

        res = self.client.get(path)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            res.json().get('errors').get('detail'),
            message)

    def test_alter_update_comment_reply(self):
        """
            Verifies: user shoudn't reword a reply to make it
                similar to one the've authored before
        """
        comment_path = self.get_single_comment_path()
        path = self.get_article_slug(created=True)
        self.post_article_comment(path)

        msg = 'posted a similar'

        resp = self.client.post(
            f'{path}/{comment_path}/reply',
            data=self.reply,
            format='json')

        id_ = resp.json().get('replies').get('data').get('id')
        res = self.client.put(f'{path}/{comment_path}/reply/{id_}',
                              data=self.reply,
                              format='json')
        self.assertEqual(res.status_code, status.HTTP_409_CONFLICT)
        self.assertIn(msg, res.json().get('replies').get('message'))
