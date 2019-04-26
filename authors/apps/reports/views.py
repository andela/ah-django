from rest_framework.generics import (CreateAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     DestroyAPIView)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

from authors.apps.articles.models import Articles
from authors.apps.articles.serializers import ArticlesSerializer
from .serializers import ReportArticleSerializer
from .models import ReportArticle

from django.template.loader import render_to_string
from ..utils.mailer import Email


from datetime import datetime


class ReportArticleView(CreateAPIView):
    """ Report Article View """

    permission_classes = (IsAuthenticated, )
    serializer_class = ReportArticleSerializer

    def post(self, request, article_slug):
        report = request.data.get('report', {})
        serializer = self.serializer_class(
            data=report
        )
        article = get_object_or_404(Articles, slug=article_slug)
        serializer.is_valid(raise_exception=True)
        serializer.save(article=article, user=self.request.user)
        return Response({'report': serializer.data},
                        status=status.HTTP_201_CREATED)


class ListReportView(ListAPIView):
    """ List Article Reports View """

    permission_classes = (IsAdminUser, )
    serializer_class = ReportArticleSerializer

    def list(self, request):
        reports = ReportArticle.objects.all()
        serializer = ReportArticleSerializer(reports, many=True)
        return Response({"reports": serializer.data},
                        status=status.HTTP_200_OK)


class ReportsView(RetrieveAPIView):
    permission_classes = (IsAdminUser, )
    serializer_class = ReportArticleSerializer

    def get(self, request, id):
        report = get_object_or_404(ReportArticle, id=id)
        serializer = self.serializer_class(report)
        report.viewed = True
        report.save()
        return Response(
            {"report": serializer.data}, status=status.HTTP_200_OK
        )


class FlagArticleView(APIView):

    permission_classes = (IsAdminUser, )
    serializer_class = ArticlesSerializer

    def post(self, request, id):
        """ Flag article view """

        flag = request.data.get('flag', {})
        report = get_object_or_404(ReportArticle, id=id)
        article = report.article
        article.flag = flag['flag']
        article.save()
        report.action_taken = 'flagged'
        report.updated_at = datetime.now()
        report.save()

        message = {
            'message': "Article {article} has been flagged as {flag}".format(
                article=article.slug, flag=flag['flag'])
        }
        self.send_mail(request=request, message=message['message'],
                       article=article)

        return Response(message, status=status.HTTP_200_OK)

    def send_mail(self, request, message, article):

        subject = 'Your article has been flagged'
        title = article.title
        article_slug = article.slug
        to_email = [article.author.email]
        host = request.get_host()
        protocol = request.scheme
        shared_link = protocol + '://' + host + '/api/articles/' + article_slug

        message = render_to_string(
            'request_update.html', {
                'title': title,
                'link': shared_link,
                'report': message
            })

        email = Email(to_email=to_email, message=message,
                      subject=subject, html_message=message)
        email.send()

    def delete(self, request, id):
        """ Unflag article view """

        report = get_object_or_404(ReportArticle, id=id)
        article = report.article
        flag = article.flag
        if flag == "":
            message = "This article was not flagged"
        else:
            article.flag = ""
            article.save()
            report.action_taken = 'resolved'
            report.save()
            message = "Article {} has been unflagged".format(article.slug)

        return Response(
            {"message": message}, status=status.HTTP_200_OK
        )


class ReportActionView(CreateAPIView, DestroyAPIView):
    serializer_class = ReportArticleSerializer

    def delete(self, request, id):
        """ Delete report """
        return Response(
            {"detail": "You are not allowed to perform this action."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


class FlaggedArticlesView(ListAPIView):
    serializer_class = ArticlesSerializer
    permission_classes = (IsAdminUser, )

    def get_queryset(self):
        queryset = Articles.objects.exclude(flag="")
        return queryset
