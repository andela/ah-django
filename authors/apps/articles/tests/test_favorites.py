from .base_test import BaseTestCase
from rest_framework.views import status
from ..models import Favorites
import json


class ArticleFavoritesTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.favorite_article_url = '/api/articles/{}/favorite'
        self.unfavorite_article_url = '/api/articles/{}/favorite'
        self.article = self.create_article(self.article).data
        self.slug = self.article['article']['slug']
        self.article_id = self.article['article']['id']
        self.list_favorites_url = '/api/favorite/articles'
        self.filter_articles_url = '/api/articles?favorited_by=testuser'

    def favorite_article(self, slug):
        """defines article unfavorite action"""

        return self.client.post(self.favorite_article_url.format(slug),
                                follow=True)

    def unfavorite_article(self, slug):
        """defines article unfavorite action"""
        return self.client.delete(self.unfavorite_article_url.format(slug))

    def test_authorized_user_can_favorite_an_article(self):
        """ tests that authenticated user can set an article as favorite"""

        favorite_response = self.favorite_article(self.slug)
        self.assertEqual(favorite_response.status_code,
                         status.HTTP_201_CREATED)
        count = Favorites.objects.filter(article=self.article_id).count()
        self.assertEqual(count, 1)

    def test_unauthorized_user_cannot_favorite_an_article(self):
        """ tests validation for unathorized user trying to favorite an article"""

        self.client.credentials()
        favorite_response = self.favorite_article(self.slug)
        self.assertEqual(favorite_response.status_code,
                         status.HTTP_403_FORBIDDEN)

    def test_article_favorite_exists(self):
        """ tests validations checks while favoriting an article that is arleady set as favorite by the user"""

        # favorite article
        self.favorite_article(self.slug)
        # favorite article again
        favorite_response = self.favorite_article(self.slug)
        self.assertEqual(favorite_response.status_code,
                         status.HTTP_403_FORBIDDEN)

    def test_article_favorite_not_found(self):
        """ tests validations checks while favoriting an article that does not exists"""

        self.slug = 'invalid_slug_name'
        favorite_response = self.favorite_article(self.slug)
        self.assertEqual(favorite_response.status_code,
                         status.HTTP_404_NOT_FOUND)

    def test_authorized_user_can_unfavorite_an_article(self):
        """ tests that authenticated user can set unfavorite an article"""

        self.favorite_article(self.slug)
        unfavorite_response = self.unfavorite_article(self.slug)
        self.assertEqual(unfavorite_response.status_code, status.HTTP_200_OK)
        count = Favorites.objects.filter(article=self.article_id).count()
        self.assertEqual(count, 0)

    def test_article_unfavorite_not_found(self):
        """ tests validations checks while unfavoriting an article that does not exists"""

        self.slug = 'invalid_slug_name'
        unfavorite_response = self.unfavorite_article(self.slug)
        self.assertEqual(unfavorite_response.status_code,
                         status.HTTP_404_NOT_FOUND)

    def test_unauthorized_user_cannot_unfavorite_an_article(self):
        """ tests validation for unathorized user trying to unfavorite an article"""

        self.client.credentials()
        self.favorite_article(self.slug)
        unfavorite_response = self.unfavorite_article(self.slug)
        self.assertEqual(unfavorite_response.status_code,
                         status.HTTP_403_FORBIDDEN)

    def test_authorized_user_view_article_favorites(self):
        """ tests article favorites list for user"""
        self.favorite_article(self.slug)
        response = self.client.get(self.list_favorites_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        count = Favorites.objects.filter(article=self.article_id).count()
        self.assertEqual(count, 1)

    def test_missing_articles_favorites_on_get(self):
        """ tests non existent favorites for user """
        response = self.client.get(self.list_favorites_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_article_with_unauthorized_user(self):
        """ tests validation for unathorized user trying to get favorite articles"""

        self.client.credentials()
        self.favorite_article(self.slug)
        response = self.client.get(self.list_favorites_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_favorited_aritcles(self):
        """test filter article by favorited by"""

        self.favorite_article(self.slug)
        response = self.client.get(self.filter_articles_url)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)
        self.assertEqual(len(data["articles"]), 1)

    def test_filter_articles_object_does_not_exist(self):
        """test filter article by favorited by when username does not exists"""

        self.url = '/api/articles?favorited_by=testssuser2'

        self.favorite_article(self.slug)

        response = self.client.get(self.url)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)
        self.assertEqual(len(data["articles"]), 0)
        self.assertEqual(data["articles"], [])
