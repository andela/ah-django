from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
import json


class CURDArticlesTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.postlist_article_url = '/api/articles/'
        self.get_article_url = '/api/articles/{article_slug}/'
        self.user_signup = {
            "user": {
                "email": "testuser@gmail.com",
                "username": "testuser",
                "password": "testuserpass123"
            }
        }

        self.user_signup2 = {
            "user": {
                "email": "testuser2@gmail.com",
                "username": "testuser2",
                "password": "testuser2pass123"
            }
        }

        self.article = {
            "article": {
                "title": "This is the article title",
                "description": "This is the article description",
                "body": "This is the article body",
                "image_url": "https://imageurl.com"
            }

        }

        self.edit_article = {
            "title": "This article title is edited",
            "body": "This article body is edited"
        }

        self.signup = self.client.post(
            "/api/users",
            self.user_signup,
            format="json"
        )

        self.signup2 = self.client.post(
            "/api/users",
            self.user_signup2,
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
            self.postlist_article_url,
            data,
            format='json', follow=True
        )

    def test_create_article(self):
        article = self.create_article(self.article)

        self.assertEqual(article.status_code,
                         status.HTTP_201_CREATED)

    def test_list_articles(self):
        self.create_article(self.article)
        list_articles = self.client.get(
            self.postlist_article_url, follow=True
        )
        self.assertEqual(list_articles.status_code,
                         status.HTTP_200_OK)

    def test_get_article(self):
        article = self.create_article(self.article)
        data = json.loads(article.content)
        article_slug = data['slug']
        get_articles = self.client.get(
            self.get_article_url.format(article_slug=article_slug)
        )

        self.assertEqual(get_articles.status_code,
                         status.HTTP_200_OK)

    def test_put_article(self):
        article = self.create_article(
            self.article)
        data = json.loads(article.content)
        article_slug = data['slug']
        edit_article = self.client.put(
            self.get_article_url.format(article_slug=article_slug),
            data=self.edit_article, formart='json'
        )

        self.assertEqual(edit_article.status_code,
                         status.HTTP_200_OK)

    def test_delete_article(self):
        article = self.create_article(
            self.article)
        data = json.loads(article.content)
        article_slug = data['slug']
        delete_article = self.client.delete(
            self.get_article_url.format(article_slug=article_slug)
        )
        self.assertEqual(delete_article.status_code,
                         status.HTTP_204_NO_CONTENT)

    def test_invalid_user(self):
        """
        Test post without login
        """
        self.client.credentials()
        article = self.create_article(self.article)
        self.assertEqual(article.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthrosed_user_delete(self):
        """
        Test unauthorised user
        deleting an article
        """
        article = self.create_article(
            self.article)
        self.client.credentials()
        credentials2 = json.loads(self.signup2.content)[
            "user"]["token"]
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + credentials2)
        data = json.loads(article.content)
        article_slug = data['slug']
        delete_article = self.client.delete(
            self.get_article_url.format(article_slug=article_slug)
        )
        self.assertEqual(delete_article.status_code,
                         status.HTTP_401_UNAUTHORIZED)

    def test_unauthrosed_user_patch(self):
        """
        Test unauthorised user
        deleting an article
        """
        article = self.create_article(
            self.article)
        self.client.credentials()
        credentials2 = json.loads(self.signup2.content)[
            "user"]["token"]
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + credentials2)
        data = json.loads(article.content)
        article_slug = data['slug']
        edit_article = self.client.put(
            self.get_article_url.format(article_slug=article_slug),
            data=self.edit_article, formart='json'
        )

        self.assertEqual(edit_article.status_code,
                         status.HTTP_401_UNAUTHORIZED)