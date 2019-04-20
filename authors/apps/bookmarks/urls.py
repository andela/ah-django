from django.urls import path

from .views import (Bookmarkarticle,
                    ListBookmarkedArticles)
app_name = "bookmarks"


urlpatterns = [
    path("bookmarks/articles/",
         ListBookmarkedArticles.as_view(),
         name="view_bookmarked_articles"),
    path('articles/<slug>/bookmarks/',
         Bookmarkarticle.as_view(), name='bookmark&unbookmark')
]
