from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
import json


class TestCommentsOperations(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.post_article_url = '/api/articles/'
        self.post_get_url = '/api/articles/{article_slug}/comments'
        self.delete_put_url = '/api/articles/{article_slug}/comments/{comm_id}'
        self.history_url = '/api/comments/{id}/history'
        self.user_signup = {
            "user": {
                "email": "testuser@gmail.com",
                "username": "testuser",
                "password": "password123"
            }
        }
        self.article = {
            "article": {
                "title": "This is the article title",
                "description": "This is the article description",
                "body": "This is the article body",
                "image_url": "https://imageurl.com",
                "tags": ["test", "trial"]

            }

        }

        self.create_comment = {
            "comment": {"body": "This is a good read"}
        }

        self.edit_comment = {
            "comment": {"body": "This is a good read"}
        }

        self.fasle_slug = 'no-slug'

        self.signup = self.client.post(
            "/api/users",
            self.user_signup,
            format="json"
        )

        self.credentials = json.loads(self.signup.content)[
            "user"]["token"]
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.credentials)

    def create_article(self, data=None):
        """ method for creating and article """
        data = data

        return self.client.post(
            self.post_article_url,
            data,
            format='json', follow=True
        )

    def test_create_comment(self):
        article = self.client.post(
            self.post_article_url,
            data=self.article,
            format='json', follow=True
        )
        data = json.loads(article.content)
        article_slug = data['article']['slug']

        comments = self.client.post(
            self.post_get_url.format(article_slug=article_slug),
            data=self.create_comment,
            format='json'
        )

        self.assertEqual(comments.status_code,
                         status.HTTP_201_CREATED)

    def test_put_comment(self):
        article = self.create_article(self.article)
        data = json.loads(article.content)
        article_slug = data['article']['slug']

        comments = self.client.post(
            self.post_get_url.format(article_slug=article_slug),
            data=self.create_comment,
            format='json'
        )
        comm = json.loads(comments.content)
        comm_id = comm['id']

        update_comment = self.client.put(
            self.delete_put_url.format(article_slug=article_slug,
                                       comm_id=comm_id),
            data=self.edit_comment, format='json'
        )

        self.assertEqual(update_comment.status_code,
                         status.HTTP_200_OK)

    def test_delete_comment(self):
        article = self.create_article(
            self.article)
        data = json.loads(article.content)
        article_slug = data['article']['slug']

        comments = self.client.post(
            self.post_get_url.format(article_slug=article_slug),
            data=self.create_comment,
            format='json'
        )
        comm = json.loads(comments.content)
        comm_id = comm['id']

        delete_comment = self.client.delete(
            self.delete_put_url.format(article_slug=article_slug,
                                       comm_id=comm_id)
        )
        self.assertEqual(delete_comment.status_code,
                         status.HTTP_200_OK)

    def test_get_comment(self):
        article = self.create_article(
            self.article)
        data = json.loads(article.content)
        article_slug = data['article']['slug']

        self.client.post(
            self.post_get_url.format(article_slug=article_slug),
            data=self.create_comment,
            format='json'
            )

        get_comments = self.client.get(
            self.post_get_url.format(article_slug=article_slug))

        self.assertEqual(get_comments.status_code,
                         status.HTTP_200_OK)

    def test_get_non_eixisting_article(self):

        get_comments = self.client.get(
            self.post_get_url.format(article_slug=self.fasle_slug))

        self.assertEqual(get_comments.status_code,
                         status.HTTP_404_NOT_FOUND)

    def test_post_to_non_existing_article(self):

        comments = self.client.post(
            self.post_get_url.format(article_slug=self.fasle_slug),
            data=self.create_comment,
            format='json'
        )

        self.assertEqual(comments.status_code,
                         status.HTTP_404_NOT_FOUND)

    def test_delete_non_existing_article(self):

        delete_comment = self.client.delete(
            self.delete_put_url.format(article_slug=self.fasle_slug,
                                       comm_id='1')
        )
        self.assertEqual(delete_comment.status_code,
                         status.HTTP_404_NOT_FOUND)

    def test_edit_non_existing_article(self):
        update_comment = self.client.put(
            self.delete_put_url.format(article_slug=self.fasle_slug,
                                       comm_id='1'),
            data=self.edit_comment, format='json'
        )

        self.assertEqual(update_comment.status_code,
                         status.HTTP_404_NOT_FOUND)

    def test_create_comment_with_highlighted_text(self):
        article = self.client.post(
            self.post_article_url,
            data=self.article,
            format='json', follow=True
        )
        data = json.loads(article.content)
        article_slug = data['article']['slug']
        self.create_comment['comment']['highlighted_text'] = "article body"
        comments = self.client.post(
            self.post_get_url.format(article_slug=article_slug),
            data=self.create_comment,
            format='json'
        )

        self.assertEqual(comments.status_code,
                         status.HTTP_201_CREATED)

    def test_create_comment_with_wrong_highlighted_text(self):
        article = self.client.post(
            self.post_article_url,
            data=self.article,
            format='json', follow=True
        )
        data = json.loads(article.content)
        article_slug = data['article']['slug']
        self.create_comment['comment']['highlighted_text'] = "This text is not on the body"
        comments = self.client.post(
            self.post_get_url.format(article_slug=article_slug),
            data=self.create_comment,
            format='json'
        )

        self.assertEqual(comments.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_update_comment_with_highlighted_text(self):
        article = self.create_article(self.article)
        data = json.loads(article.content)
        article_slug = data['article']['slug']

        comments = self.client.post(
            self.post_get_url.format(article_slug=article_slug),
            data=self.create_comment,
            format='json'
        )
        comm = json.loads(comments.content)
        comm_id = comm['id']
        self.edit_comment['comment']['highlighted_text'] = "article body"
        update_comment = self.client.put(
            self.delete_put_url.format(article_slug=article_slug,
                                       comm_id=comm_id),
            data=self.edit_comment, format='json'
        )

        self.assertEqual(update_comment.status_code,
                         status.HTTP_200_OK)

    def test_update_comment_with_wrong_highlighted_text(self):
        article = self.create_article(self.article)
        data = json.loads(article.content)
        article_slug = data['article']['slug']

        comments = self.client.post(
            self.post_get_url.format(article_slug=article_slug),
            data=self.create_comment,
            format='json'
        )
        comm = json.loads(comments.content)
        comm_id = comm['id']
        self.edit_comment['comment']['highlighted_text'] = "wrong highlight"
        update_comment = self.client.put(
            self.delete_put_url.format(article_slug=article_slug,
                                       comm_id=comm_id),
            data=self.edit_comment, format='json'
        )

        self.assertEqual(update_comment.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_checking_comment_history(self):
        article = self.create_article(self.article)
        data = json.loads(article.content)
        article_slug = data['article']['slug']

        comments = self.client.post(
            self.post_get_url.format(article_slug=article_slug),
            data=self.create_comment,
            format='json'
        )
        comm = json.loads(comments.content)
        comm_id = comm['id']

        self.client.put(self.delete_put_url.format(
                                       article_slug=article_slug,
                                       comm_id=comm_id),
                        data=self.edit_comment, format='json'
                        )

        history = self.client.get(
            self.history_url.format(id=comm_id))

        self.assertEqual(history.status_code,
                         status.HTTP_200_OK)

    def test_check_history_of_nonexisting_comment(self):
        history = self.client.get(
            self.history_url.format(id=1))

        self.assertEqual(history.status_code,
                         status.HTTP_404_NOT_FOUND)
