""" This module defines test cases for highlights """
from django.urls import reverse
from rest_framework import status
from authors.apps.authentication.tests.base_test import BaseTestCase


class TestCasesHighlights(BaseTestCase):
    """ This class defines test methods for higlights """

    def test_create_highlight(self):
        response = self.client.post(
            reverse('highlights:create-highlight',
                    kwargs={"slug": "test-slug"}), {
                        "highlight_object":
                        {"highlight": "about",
                         "comment": "This quote is innacurate."}
            },
            HTTP_AUTHORIZATION=self.hauth,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_highlights(self):
        """ Tests the successfult retirieve of a highlight """
        response = self.client.get(
            reverse('highlights:create-highlight',
                    kwargs={
                        "slug": "test-slug"
                    }),
            HTTP_AUTHORIZATION=self.hauth
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_invalid_highlight(self):
        """ Tests non-existant highlight """

        response = self.client.post(
            reverse('highlights:create-highlight',
                    kwargs={"slug": "test-slug"}), {
                        "highlight_object":
                        {"highlight": "inexistence highlight",
                         "comment": "This quote is innacurate."}
            },
            HTTP_AUTHORIZATION=self.hauth,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_highlight_for_no_article(self):
        """ Tests highlight a non existant article """

        response = self.client.post(
            reverse('highlights:create-highlight',
                    kwargs={"slug": "test-slug-not-real"}), {
                        "highlight_object":
                        {"highlight": "inexistence highlight",
                         "comment": "This quote is innacurate."}
            },
            HTTP_AUTHORIZATION=self.hauth,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_not_unauthorized_highlight(self):
        """ Tests unauthorized highlight """

        response = self.client.post(
            reverse('highlights:create-highlight',
                    kwargs={"slug": "test-slug"}), {
                        "highlight_object":
                        {"highlight": "inexistence highlight",
                         "comment": "This quote is innacurate."}
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_one_highlights(self):
        """ Tests the successfult retirieve of a highlight """

        response = self.client.get(
            reverse('highlights:get-highlights',
                    kwargs={
                        "slug": "test-slug",
                        "highlight_id": 1
                    }),
            HTTP_AUTHORIZATION=self.hauth,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_highlights(self):
        """ Tests the successfult delete of a highlight """

        response = self.client.delete(
            reverse('highlights:get-highlights',
                    kwargs={
                        "slug": "test-slug",
                        "highlight_id": 1
                    }),
            HTTP_AUTHORIZATION=self.hauth,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
