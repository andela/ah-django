"""
this file contains all tests pertaining bookmarking of articles.
"""
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
import json


class BookmarkTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_1 = {
            "user": {
                "email": "premiermember@gmail.com",
                "username": "premiermember",
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

    def test_normal_article_bookmark(self):
        """
        test a normal bookmark article procedure
        """
        onsignup = self.signup()
        usertoken = json.loads(onsignup.content)["user"]["token"]
        article = self.create_article(usertoken=usertoken)
        articleslug = json.loads(article.content)["article"]["slug"]
        articletitle = json.loads(article.content)["article"]["title"]

        bookmark = self.client.post(
            self.get_bookmark_url.format(articleslug),
            {},
            format="json",
            HTTP_AUTHORIZATION='bearer {}'.format(usertoken))
        self.assertEqual(bookmark.status_code,
                         status.HTTP_201_CREATED)
        self.assertEqual(
            json.loads(bookmark.content)["data"],
            "You have successfully bookmarked {}".format(articletitle))

    def test_unauthorized_user_bookmark_article(self):
        """
        test incognito user bookmark article procedure
        """
        onsignup = self.signup()
        usertoken = json.loads(onsignup.content)["user"]["token"]
        article = self.create_article(usertoken=usertoken)
        articleslug = json.loads(article.content)["article"]["slug"]
        bookmark = self.client.post(
            self.get_bookmark_url.format(articleslug),
            {},
            format="json",
        )
        self.assertEqual(bookmark.status_code,
                         status.HTTP_403_FORBIDDEN)

    def test_bookmarking_article_that_dont_exist(self):
        """
        test user bookmarking article that dont exist.
        """
        onsignup = self.signup()
        usertoken = json.loads(onsignup.content)["user"]["token"]
        bookmark = self.client.post(
            self.get_bookmark_url.format("idontexist"),
            {},
            format="json",
            HTTP_AUTHORIZATION='bearer {}'.format(usertoken))
        self.assertEqual(bookmark.status_code,
                         status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(bookmark.content)["error"],
                         "Article ({}) does not exist.".format("idontexist"))

    def test_bookmarking_article_twice(self):
        """
        test a normal bookmark article twice.
        """
        onsignup = self.signup()
        usertoken = json.loads(onsignup.content)["user"]["token"]
        article = self.create_article(usertoken=usertoken)
        articletitle = json.loads(article.content)["article"]["title"]
        articleslug = json.loads(article.content)["article"]["slug"]
        # bookmark the first time.
        self.client.post(
            self.get_bookmark_url.format(articleslug),
            {},
            format="json",
            HTTP_AUTHORIZATION='bearer {}'.format(usertoken))
        # bookmark the second time
        bookmark = self.client.post(
            self.get_bookmark_url.format(articleslug),
            {},
            format="json",
            HTTP_AUTHORIZATION='bearer {}'.format(usertoken))
        self.assertEqual(bookmark.status_code,
                         status.HTTP_409_CONFLICT)
        self.assertEqual(json.loads(bookmark.content)["error"],
                         "You already bookmarked {}".format(articletitle))
