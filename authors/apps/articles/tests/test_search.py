from rest_framework import status
from ...authentication.tests.base_test import BaseTestCase
from rest_framework_jwt import utils


class SearchArticles(BaseTestCase):
    """
        Test getting, updating, deleting articles
    """

    def createArticle(self):
        """
        Create article to be used for testing
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
        res = self.client.post(
            self.new_article_path,
            new_article,
            HTTP_AUTHORIZATION=auth,
            format='json')
        return res

    def test_search_article_title_success(self):
        """ test for a successful search for article by title"""

        self.createArticle()
        url = self.new_article_path + "search?title=How"
        response = self.client.get(
            url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_article_tag_success(self):
        """ test for a successful search for article by tag"""

        self.createArticle()
        url = self.new_article_path + "search?tag=dragons"
        response = self.client.get(
            url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_article_author_success(self):
        """ test for a successful search for article by title"""

        self.createArticle()
        url = self.new_article_path + "search?author=testguy99"
        response = self.client.get(
            url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_article_title_unsuccessful(self):
        """ test for an unsuccessful search for article by title"""

        self.createArticle()
        url = self.new_article_path + "search?title=tree"
        response = self.client.get(
            url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_search_wrong_input(self):
        """ test for wrong url input"""

        self.createArticle()
        url = self.new_article_path + "search?tree=tree"
        response = self.client.get(
            url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_search_tag_unsuccessful(self):
        """ test for an unsuccessful search for article by tag"""

        self.createArticle()
        url = self.new_article_path + "search?tag=tree"
        response = self.client.get(
            url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_search_article_author_unsuccess(self):
        """ test for an unsuccessful search for article by author"""

        self.createArticle()
        url = self.new_article_path + "search?author=lincoln"
        response = self.client.get(
            url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
