from authors.apps.articles.tests.base_test import BaseTestCase
from rest_framework.views import status
import json


class ReportArticleTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.report_article_url = '/api/articles/{article_slug}/report/'
        self.single_report_url = '/api/articles/report/{report_id}/'
        self.list_reports_url = '/api/articles/report/list/'
        self.flag_article_url = '/api/articles/report/{report_id}/flag/'
        self.report_action_url = '/api/articles/report/{report_id}/action/'
        self.flagged_articles_url = '/api/articles/report/flag/'
        self.report_article = {
            "report": {
                "report": "This is a sample report"
            }
        }

        self.flag_article = {
            "flag": {
                "flag": "plagirized"
            }
        }

    def post_report(self):
        """ method for posting a report """

        article = self.create_article(data=self.article)
        data = json.loads(article.content)
        article_slug = data['article']['slug']

        return self.client.post(
            self.report_article_url.format(article_slug=article_slug),
            self.report_article,
            format="json")

    def flag_report(self, report_id):
        self.client.credentials()
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.admin_credentials
        )
        return self.client.post(
            self.flag_article_url.format(report_id=report_id),
            data=self.flag_article,
            format='json'
        )

    def test_post_report(self):
        """ test for posting an article """

        report = self.post_report()

        self.assertEqual(report.status_code,
                         status.HTTP_201_CREATED)

    def test_list_reports(self):
        """ test for listing articles """
        self.post_report()
        self.client.credentials()
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.admin_credentials
        )
        list_article = self.client.get(
            self.list_reports_url
        )

        self.assertEqual(list_article.status_code,
                         status.HTTP_200_OK)

    def test_single_report(self):
        """ test for get single report """
        report = self.post_report()
        report_data = json.loads(report.content)
        report_id = report_data['report']['id']
        self.client.credentials()
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.admin_credentials
        )
        get_article = self.client.get(
            self.single_report_url.format(report_id=report_id)
        )

        self.assertEqual(get_article.status_code,
                         status.HTTP_200_OK)

    def test_delete_report(self):
        """ test delete report """

        report = self.post_report()
        report_data = json.loads(report.content)
        report_id = report_data['report']['id']
        self.client.credentials()
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.admin_credentials
        )
        delete_report = self.client.delete(
            self.report_action_url.format(report_id=report_id)
        )

        self.assertEqual(delete_report.status_code,
                         status.HTTP_200_OK)

    def test_flag_article(self):
        """ test flag article """

        report = self.post_report()
        report_data = json.loads(report.content)
        report_id = report_data['report']['id']
        flag_report = self.flag_report(report_id)

        self.assertEqual(flag_report.status_code,
                         status.HTTP_200_OK)

    def test_unflag_article(self):
        """ test unflag article """

        report = self.post_report()
        report_data = json.loads(report.content)
        report_id = report_data['report']['id']
        self.flag_report(report_id)
        unflag_article = self.client.delete(
            self.flag_article_url.format(report_id=report_id)
        )

        self.assertEqual(unflag_article.status_code, status.HTTP_200_OK)

    def test_flag_unathorized(self):
        """ test unauthorized user flag """

        report = self.post_report()
        report_data = json.loads(report.content)
        report_id = report_data['report']['id']
        self.client.credentials()
        flag = self.client.post(
            self.flag_article_url.format(report_id=report_id),
            data=self.flag_article,
            format='json'
        )

        self.assertEqual(flag.status_code,
                         status.HTTP_403_FORBIDDEN)

    def test_get_flagged_unauthorized(self):
        """
        test of get flagged
        article by unauthorized user
        """

        article = self.create_article(data=self.article)
        data = json.loads(article.content)
        article_slug = data['article']['slug']

        report = self.client.post(
            self.report_article_url.format(article_slug=article_slug),
            self.report_article,
            format="json")
        report_data = json.loads(report.content)
        report_id = report_data['report']['id']
        self.flag_report(report_id)
        self.client.credentials()

        get_article = self.client.get(
            self.get_article_url.format(article_id=article_slug))
        self.assertEqual(get_article.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_flagged_articles(self):

        article = self.create_article(data=self.article)
        data = json.loads(article.content)
        article_slug = data['article']['slug']

        report = self.client.post(
            self.report_article_url.format(article_slug=article_slug),
            self.report_article,
            format="json")
        report_data = json.loads(report.content)
        report_id = report_data['report']['id']
        self.flag_report(report_id)

        get_flagged_reports = self.client.get(
            self.flagged_articles_url
        )
        self.assertEqual(get_flagged_reports.status_code,
                         status.HTTP_200_OK)
