from rest_framework.views import status

import json

from .test_comments import TestCommentsOperations


class TestLikeComments(TestCommentsOperations):

    def setUp(self):
        super().setUp()
        self.like_url = '/api/comments/{id}/like'
        self.like = {
            "action": "like"
        }
        self.dislike = {
            "action": "dislike"
        }

    def post_comment(self):
        """ post a comment
            returns the id
        """
        article = self.client.post(
            self.post_article_url,
            data=self.article,
            format='json'
        )
        data = json.loads(article.content)
        article_slug = data['article']['slug']

        comment = self.client.post(
            self.post_get_url.format(
                article_slug=article_slug),
            data=self.create_comment,
            format='json'
        )
        comment_data = json.loads(comment.content)
        comment_id = comment_data['id']
        return comment_id

    def test_like_comment(self):
        """ test like comment """
        comment_id = self.post_comment()

        like = self.client.post(
            self.like_url.format(id=comment_id),
            data=self.like,
            format='json'
        )

        self.assertEqual(like.status_code,
                         status.HTTP_200_OK)

    def test_like_comment_no_action(self):
        """ test like comment with no action"""
        comment_id = self.post_comment()

        like = self.client.post(
            self.like_url.format(id=comment_id),
            data=None,
            format='json'
        )

        self.assertEqual(like.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_dislike_comment(self):
        """ test dislkie comment """
        comment_id = self.post_comment()

        dislike = self.client.post(
            self.like_url.format(id=comment_id),
            data=self.dislike,
            format='json'
        )

        self.assertEqual(dislike.status_code,
                         status.HTTP_200_OK)

    def test_get_likes_and_dislikes(self):
        """
        Test getting likes and dislikes
        for a particular comment
        """
        comment_id = self.post_comment()

        self.client.post(
            self.like_url.format(id=comment_id),
            data=self.like,
            format='json'
        )

        likes = self.client.get(
            self.like_url.format(id=comment_id)
        )

        self.assertEqual(likes.status_code,
                         status.HTTP_200_OK)

    def test_delete_like(self):
        """Tests for deleting like"""

        comment_id = self.post_comment()

        self.client.post(
            self.like_url.format(id=comment_id),
            data=self.like,
            format='json'
        )

        delete_like = self.client.delete(
            self.like_url.format(id=comment_id)
        )

        self.assertEqual(delete_like.status_code,
                         status.HTTP_200_OK)

    def test_delete_dislike(self):
        """Tests for deleting dislike"""

        comment_id = self.post_comment()

        self.client.post(
            self.like_url.format(id=comment_id),
            data=self.dislike,
            format='json'
        )

        delete_dislike = self.client.delete(
            self.like_url.format(id=comment_id)
        )

        self.assertEqual(delete_dislike.status_code,
                         status.HTTP_200_OK)

    def test_like_non_exsiting_comment(self):
        """Test for liking non existing comments"""

        like = self.client.post(
            self.like_url.format(id=1),
            data=self.like,
            format='json'
        )

        self.assertEqual(like.status_code,
                         status.HTTP_404_NOT_FOUND)

    def test_delete_non_existing_like(self):
        """Test for deleting a non existant like or dislike"""
        comment_id = self.post_comment()

        delete_like = self.client.delete(
            self.like_url.format(id=comment_id)
        )

        self.assertEqual(delete_like.status_code,
                         status.HTTP_404_NOT_FOUND)
