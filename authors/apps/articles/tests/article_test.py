import cloudinary

from rest_framework import status
from django.urls import reverse
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
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_new(self):
        """
        create new article successfuly
        """
        new_article = {
            "article": {
                "title": "test",
                "description": "Ever wonder how?",
                "body": "It takes a Jacobian",
                "image": "andela.png",
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
        cloudinary.uploader.destroy('ah-django/test_testguy99')

        # run again to test duplicate returns 409
        response = self.client.post(self.new_article_path,
                                    new_article, HTTP_AUTHORIZATION=auth,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_create_new_with_invalid_image(self):
        """
        create new article successfuly
        """
        new_article = {
            "article": {
                "title": "How to train your dragon",
                "description": "Ever wonder how?",
                "body": "It takes a Jacobian",
                "image": "no-such-image.png",
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
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ArticleDetails(BaseTestCase):
    """
        Test getting, updating, deleting articles
    """

    def test_get_all_articles(self):
        """
        test get all articles
        """
        response = self.client.get(self.articles_feed)
        # articles = Article.objects.all()
        # serializer = ArticleSerializer(articles, many=True)
        # self.assertEqual(response.data, serializer.data)
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
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

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
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_rate_article(self):
        """
        test rate article
        """
        rating = {
            "rating": {
                "rating": 4
            }
        }

        payload = utils.jwt_payload_handler(self.testuser)
        token = utils.jwt_encode_handler(payload)
        auth = 'Bearer {0}'.format(token)
        response = self.client.post(self.article_rating,
                                    rating, HTTP_AUTHORIZATION=auth,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_rate_article(self):
        """
        test rate article invalid
        """
        rating = {
            "rating": {
                "rating": 23
            }
        }

        payload = utils.jwt_payload_handler(self.testuser)
        token = utils.jwt_encode_handler(payload)
        auth = 'Bearer {0}'.format(token)
        response = self.client.post(self.article_rating,
                                    rating, HTTP_AUTHORIZATION=auth,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sharing_on_twitter(self):
        """
        test the sharing of an article on twitter
         """
        payload = utils.jwt_payload_handler(self.testuser)
        token = utils.jwt_encode_handler(payload)
        auth = 'Bearer {0}'.format(token)
        response = self.client.get(reverse('articles:share', kwargs={
            'slug': 'test-slug', 'platform': 'twitter'
        }),
            HTTP_AUTHORIZATION=auth,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sharing_on_facebook(self):
        """
        test the sharing of an article on facebook
         """
        payload = utils.jwt_payload_handler(self.testuser)
        token = utils.jwt_encode_handler(payload)
        auth = 'Bearer {0}'.format(token)
        response = self.client.get(reverse('articles:share', kwargs={
            'slug': 'test-slug', 'platform': 'facebook'
        }),
            HTTP_AUTHORIZATION=auth,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sharing_on_reddit(self):
        """
        test the sharing of an article on reddit
         """
        payload = utils.jwt_payload_handler(self.testuser)
        token = utils.jwt_encode_handler(payload)
        auth = 'Bearer {0}'.format(token)
        response = self.client.get(reverse('articles:share', kwargs={
            'slug': 'test-slug', 'platform': 'reddit'
        }),
            HTTP_AUTHORIZATION=auth,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sharing_on_linkedin(self):
        """
        test the sharing of an article on linkedin
         """

        payload = utils.jwt_payload_handler(self.testuser)
        token = utils.jwt_encode_handler(payload)
        auth = 'Bearer {0}'.format(token)
        response = self.client.get(reverse('articles:share', kwargs={
            'slug': 'test-slug', 'platform': 'linkedin'
        }),
            HTTP_AUTHORIZATION=auth,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def search_article_title_success(self):
        """ test for a successful search for article by title"""
        response = self.test_client.get(
            "/api/articles/search?title={}".format(self.title),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
