from rest_framework import status
from ...authentication.tests.base_test import BaseTestCase
from rest_framework_jwt import utils
from ..serializers import ArticleSerializer
from ..models import Article


class TestNewArticle(BaseTestCase):
    """
        New article tests
    """

    def test_auth_required(self):
        """
            auth required to post article
        """
        new_article = {
            "article": {
                "title": "How to train your dragon",
                "description": "Ever wonder how?",
                "body": "It takes a Jacobian",
                "tagList": [
                    "dragons",
                    "training"
                ]
            }
        }

        response = self.client.post(self.new_article_path,
                                    new_article, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_new(self):
        """
        create new article successfuly
        """
        new_article = {
            "article": {
                "title": "How to train your dragon",
                "description": "Ever wonder how?",
                "body": "It takes a Jacobian",
                "tagList": [
                    "dragons",
                    "training"
                ]
            }
        }

        payload = utils.jwt_payload_handler(self.testuser)
        token = utils.jwt_encode_handler(payload)
        auth = 'Bearer {0}'.format(token)
        response = self.client.post(self.new_article_path,
                                    new_article, HTTP_AUTHORIZATION=auth,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ArticleDetails(BaseTestCase):
    """
        Test getting, updating, deleting articles
    """

    def test_get_all_articles(self):
        """
        test get all articles
        """
        response = self.client.get(self.articles_feed)
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_article(self):
        """
        test get one article
        """
        response = self.client.get(self.article_details)
        articles = Article.objects.get(slug='test-slug')
        serializer = ArticleSerializer(articles)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_article(self):
        """
        test update article
        """
        update_article = {
            "title": "How to train your dragon -- update",
            "description": "Ever wonder how?",
            "body": "It takes a Jacobian",
            "tagList": [
                "dragons",
                "training"
            ]
        }

        payload = utils.jwt_payload_handler(self.testuser)
        token = utils.jwt_encode_handler(payload)
        auth = 'Bearer {0}'.format(token)
        response = self.client.put(self.article_details,
                                   update_article, HTTP_AUTHORIZATION=auth,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_article(self):
        """
        test update article unauthorized
        """
        update_article = {
            "title": "How to train your dragon -- update",
            "description": "Ever wonder how?",
            "body": "It takes a Jacobian",
            "tagList": [
                "dragons",
                "training"
            ]
        }
        response = self.client.put(self.article_details,
                                   update_article, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_article(self):
        """
        test delete article
        """
        payload = utils.jwt_payload_handler(self.testuser)
        token = utils.jwt_encode_handler(payload)
        auth = 'Bearer {0}'.format(token)
        response = self.client.put(self.article_details,
                                   HTTP_AUTHORIZATION=auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_delete_article(self):
        """
        test delete article unauthorized
        """
        response = self.client.put(self.article_details)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
