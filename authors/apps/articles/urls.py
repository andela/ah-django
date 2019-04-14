from django.conf.urls import url
from django.urls.conf import path

from .views import (
    ArticleList, ArticleDetails, NewArticle, RateArticle,
    SearchArticlesList, ReadArticleView, ShareArticlesApiView,
    ReportArticleView, ReportList, ReportAPIViews
)


app_name = 'articles'

urlpatterns = [
    url(r'^articles/search',
        SearchArticlesList.as_view(), name='article_title'),
    url(r'^articles/(?P<slug>.+)/report/$', ReportArticleView.as_view(),
        name='report_article'),
    url(r'^articles/reports/$', ReportList.as_view(),
        name='view_reports'),
    url(r'^articles/(?P<pk>.+)/action/$', ReportAPIViews.as_view(),
        name='report_actions'),
    url(r'^articles/$', NewArticle.as_view(), name='new_article'),
    url(r'^articles/feed/$', ArticleList.as_view(), name='articles_feed'),
    url(r'^articles/(?P<slug>.+)/share/(?P<platform>.+)/$',
        ShareArticlesApiView.as_view(), name='share'),
    url(r'^articles/(?P<slug>.+)/rate/$', RateArticle.as_view(),
        name='rate_article'),
    url(r'^articles/(?P<slug>.+)/$', ArticleDetails.as_view(),
        name='article_details'),
    path('articles/<slug:slug>/read', ReadArticleView.as_view(),
         name='read_article'),
]
