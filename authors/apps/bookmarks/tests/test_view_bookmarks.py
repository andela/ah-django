"""
this file contains all tests pertaining viewing all articles.
"""
# import json
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
import json


class BookmarkTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_1 = {
            "user": {
                "email": "premiermember@gmail.com",
                "username": "PremierMember",
                "password": "premiermember2019"
            }
        }

        self.articles_bookmark = "/api/articles/{}/bookmarks/"

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
        self.usertoken = usertoken
        self.client.post(
            "/api/articles/{}/bookmarks/".format(articleslug),
            {},
            format="json",
            HTTP_AUTHORIZATION='bearer {}'.format(usertoken))
        return articleslug

    def test_view_all_article_bookmarkers(self):
        """
            view all article bookmarks
        """
        articleslug = self.bookmark_article()
        res = self.client.get(
            self.articles_bookmark.format(articleslug))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('bookmarkers', res.data)
        self.assertEqual(json.loads(res.content)["bookmarkers"][0][
                         "profile"]["username"], "PremierMember")

    def test_view_bookmarkers_on_non_existent_article(self):
        res = self.client.get(
            self.articles_bookmark.format("idontexist"))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(res.content), {
            "error": "Article ({}) does not exist.".format("idontexist")
        })

    def test_view_my_bookmarked_articles(self):
        self.bookmark_article()
        res = self.client.get(
            "/api/bookmarks/articles/",
            HTTP_AUTHORIZATION='bearer {}'.format(self.usertoken))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_view_bookmarked_articles_incognito(self):
        self.bookmark_article()
        res = self.client.get(
            "/api/bookmarks/articles/")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
