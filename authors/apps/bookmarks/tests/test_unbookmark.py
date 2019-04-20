"""
    this tests cover unbookmarking of an article.
"""
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
import json


class UnBookmarkTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_1 = {
            "user": {
                "email": "premiermember@gmail.com",
                "username": "PremierMember",
                "password": "premiermember2019"
            }
        }
        self.get_bookmark_url = '/api/articles/{}/bookmarks/'

    def signup(self):
        return self.client.post(
            "/api/users", self.user_1, format="json")

    def create_article(self, usertoken=None):
        """ method for creating an article """
        data = {
            "article": {
                "title": "Article to be bookmaked",
                "description": "This is the article description",
                "body": "This is the article body",
                "image_url": "https://imageurl.com",
                "tags": []
            }
        }

        return self.client.post(
            '/api/articles/',
            data,
            format='json',
            HTTP_AUTHORIZATION='bearer {}'.format(usertoken))

    def bookmark_article(self):
        """
        bookmark an article
        """
        onsignup = self.signup()
        usertoken = json.loads(onsignup.content)["user"]["token"]
        article = self.create_article(usertoken=usertoken)
        articleslug = json.loads(article.content)["article"]["slug"]

        self.client.post(
            self.get_bookmark_url.format(articleslug),
            {},
            format="json",
            HTTP_AUTHORIZATION='bearer {}'.format(usertoken))
        return (articleslug, usertoken)

    def test_normal_article_unbookmark(self):
        """
        test a normal unbookmark of an article
        """
        (articleslug, usertoken) = self.bookmark_article()
        title = "Article to be bookmaked"
        bookmark = self.client.delete(
            self.get_bookmark_url.format(articleslug),
            {},
            format="json",
            HTTP_AUTHORIZATION='bearer {}'.format(usertoken))
        self.assertEqual(bookmark.status_code,
                         status.HTTP_200_OK)
        self.assertEqual(
            json.loads(bookmark.content)["data"],
            "You have successfully unbookmarked {}".format(title))

    def test_incognito_article_unbookmark(self):
        """
        test a incognito unbookmark of an article
        """
        (articleslug, usertoken) = self.bookmark_article()
        bookmark = self.client.delete(
            self.get_bookmark_url.format(articleslug),
            {},
            format="json",
        )
        self.assertEqual(bookmark.status_code,
                         status.HTTP_403_FORBIDDEN)

    def test_unbookmark_article_twice(self):
        """
            test unbookmark twice.
        """
        (articleslug, usertoken) = self.bookmark_article()
        title = "Article to be bookmaked"
        self.client.delete(
            self.get_bookmark_url.format(articleslug),
            {},
            format="json",
            HTTP_AUTHORIZATION='bearer {}'.format(usertoken))
        bookmark = self.client.delete(
            self.get_bookmark_url.format(articleslug),
            {},
            format="json",
            HTTP_AUTHORIZATION='bearer {}'.format(usertoken))
        self.assertEqual(bookmark.status_code,
                         status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            json.loads(bookmark.content)["error"],
            "You had not bookmarked {}".format(title))

    def test_unbookmark_unexistent_article(self):
        """
            test unbookmarking a non existent article
        """
        (articleslug, usertoken) = self.bookmark_article()

        bookmark = self.client.delete(
            self.get_bookmark_url.format("idontexist"),
            {},
            format="json",
            HTTP_AUTHORIZATION='bearer {}'.format(usertoken))
        self.assertEqual(bookmark.status_code,
                         status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(bookmark.content)["error"],
                         "Article ({}) does not exist.".format("idontexist"))
