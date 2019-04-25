from rest_framework.views import status
from ..models import ReadStats
from authors.apps.articles.tests.base_test import BaseTestCase
import json


class TestStatsOperations(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user_read_stat_url = "/api/user/stats/"
        self.article_read_stats = "/api/articles/{article_slug}/stats/"
        self.admin_view_user_stats = "/api/stats/"

    def test_read_status_for_anonynous_user(self):
        res = self.create_article(self.article)
        article = json.loads(res.content)["article"]
        self.client.credentials()
        self.client.get(
            self.get_article_url.format(
                article_id=article["slug"]), format="json")

        self.assertEqual(ReadStats.objects.count(), 0)

    def test_view_stats_of_user_with_no_stats(self):
        res = self.create_article(self.article)

        res = self.client.get(
            self.user_read_stat_url.format(
                username=self.user_signup["user"]["username"]),
            format="json"
        )

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(json.loads(res.content), {
            "status": 404,
            "error": "No stats available"
        })

    def test_read_status_for_authenticated_user(self):
        res = self.create_article(self.article)
        article = json.loads(res.content)["article"]
        self.client.get(
            self.get_article_url.format(
                article_id=article["slug"]), format="json")

        self.assertEqual(ReadStats.objects.count(), 1)

        res = self.client.get(
            self.user_read_stat_url.format(
                username=self.user_signup["user"]["username"]),
            format="json"
        )

        self.assertEqual(json.loads(res.content), {
            "total_reads": 1,
            "stats": [
                {
                    "views": 1,
                    "article": {
                        "title": "This is the article title",
                        "slug": "this-is-the-article-title",
                    }
                }
            ]
        })

    def test_read_status_for_multiple_views(self):
        res = self.create_article(self.article)
        self.create_article(self.article)
        article = json.loads(res.content)["article"]

        for x in [1, 2]:
            self.client.get(
                self.get_article_url.format(
                    article_id=article["slug"]), format="json")
            self.client.get(
                self.get_article_url.format(
                    article_id=article["slug"] + '-1'), format="json")

        res = self.client.get(
            self.user_read_stat_url.format(
                username=self.user_signup["user"]["username"]),
            format="json"
        )

        self.assertEqual(json.loads(res.content), {
            "total_reads": 2,
            "stats": [
                {
                    "views": 2,
                    "article": {
                        "title": "This is the article title",
                        "slug": "this-is-the-article-title",
                    }
                },
                {
                    "views": 2,
                    "article": {
                        "title": "This is the article title",
                        "slug": "this-is-the-article-title-1",
                    }
                }

            ]
        })

    def test_view_stats_of_article_with_no_stats(self):
        res = self.create_article(self.article)
        article = json.loads(res.content)["article"]

        res = self.client.get(self.article_read_stats.format(
            article_slug=article["slug"]),
            format="json")

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(res.content), {
            "status": 404,
            "error": "{} does not have any stats".format(article["title"])
        })

    def test_article_view_stats_for_unauthorized_author(self):
        res = self.create_article(self.article)
        article = json.loads(res.content)["article"]
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.credentials_2)
        self.client.get(
            self.get_article_url.format(
                article_id=article["slug"]), format="json")

        res = self.client.get(
            self.article_read_stats.format(
                article_slug=article["slug"]), format="json")

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(res.content), {
            "status": 403,
            "error": "Not allowed"
        })

    def test_view_stats_of_non_existent_article(self):
        res = self.client.get(self.article_read_stats.format(
            article_slug="idontexist"),
            format="json")

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(res.content), {
            "status": 404,
            "error": "Article not found"
        })

    def test_view_article_stats(self):
        res = self.create_article(self.article)
        article = json.loads(res.content)["article"]

        for x in [1, 2]:
            self.client.get(
                self.get_article_url.format(
                    article_id=article["slug"]), format="json")

        res = self.client.get(self.article_read_stats.format(
            article_slug=article["slug"]),
            format="json")

        data = json.loads(res.content)

        self.assertEqual(data["total_views"], 2)
        self.assertEqual(data["stats"][0]["user"]["username"], "testuser")
        self.assertEqual(data["stats"][0]["views"], 2)

    def test_non_admin_view_all_stats(self):
        # admin_view_user_stats
        res = self.create_article(self.article)
        article = json.loads(res.content)["article"]

        for x in [1, 2]:
            self.client.get(
                self.get_article_url.format(
                    article_id=article["slug"]), format="json")

        res = self.client.get(self.admin_view_user_stats, format="json")

        self.assertEqual((res.status_code), status.HTTP_403_FORBIDDEN)

    def test_admin_view_all_stats(self):
        # admin_view_user_stats
        res = self.create_article(self.article)
        article = json.loads(res.content)["article"]

        for x in [1, 2]:
            self.client.get(
                self.get_article_url.format(
                    article_id=article["slug"]), format="json")
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.admin_credentials)

        res = self.client.get(self.admin_view_user_stats, format="json")

        data = json.loads(res.content)

        self.assertEqual(data["stats"][0]["user"]["username"], "testuser")
        self.assertEqual(data["stats"][0]["article"]
                         ["slug"], "this-is-the-article-title")
        self.assertEqual(data["stats"][0]["views"], 2)

    def test_admin_view_stats_with_params_and_descending(self):
        res = self.create_article(self.article)
        self.create_article(self.article)
        article = json.loads(res.content)["article"]
        self.client.get(
            self.get_article_url.format(
                article_id=article["slug"]), format="json")
        for x in [1, 2]:
            self.client.get(
                self.get_article_url.format(
                    article_id=article["slug"] + '-1'), format="json")

        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.admin_credentials)

        res = self.client.get(self.admin_view_user_stats +
                              '?username=testuser&desc_views&article=this',
                              format="json")

        data = json.loads(res.content)

        self.assertEqual(data["stats"][0]["user"]["username"], "testuser")
        self.assertEqual(data["stats"][0]["article"]
                         ["slug"], "this-is-the-article-title-1")
        self.assertEqual(data["stats"][0]["views"], 2)
        self.assertEqual(data["stats"][1]["views"], 1)

    def test_admin_view_stats_with_params_and_ascending(self):
        res = self.create_article(self.article)
        self.create_article(self.article)
        article = json.loads(res.content)["article"]
        self.client.get(
            self.get_article_url.format(
                article_id=article["slug"]), format="json")
        for x in [1, 2]:
            self.client.get(
                self.get_article_url.format(
                    article_id=article["slug"] + '-1'), format="json")

        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.admin_credentials)

        res = self.client.get(self.admin_view_user_stats +
                              '?username=testuser&asc_views&article=this',
                              format="json")

        data = json.loads(res.content)

        self.assertEqual(data["stats"][0]["user"]["username"], "testuser")
        self.assertEqual(data["stats"][0]["article"]
                         ["slug"], "this-is-the-article-title")
        self.assertEqual(data["stats"][0]["views"], 1)
        self.assertEqual(data["stats"][1]["views"], 2)

    def test_non_available_stats(self):

        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.admin_credentials)

        res = self.client.get(self.admin_view_user_stats, format="json")

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(res.content), {
            "status": 404,
            "error": "No stats available"
        })
