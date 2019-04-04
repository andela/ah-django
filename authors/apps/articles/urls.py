from django.conf.urls import url

from .views import (
    ArticleList, ArticleDetails, NewArticle
)

app_name = 'articles'

urlpatterns = [
    url(r'^articles/$', NewArticle.as_view(), name='new_article'),
    url(r'^articles/feed/$', ArticleList.as_view(), name='articles_feed'),
    url(r'^articles/(?P<slug>.+)/$', ArticleDetails.as_view(),
        name='article_details')
]
