from django.conf.urls import url
from django.urls import path
from .views import (CreateCommentView, UpdateDeleteCommentView,
                    CommentHistoryView)

urlpatterns = [
    url(r'^articles/(?P<article_slug>[-\w]+)/comments/?$',
        CreateCommentView.as_view(),
        name="create-get-comment"),

    path('articles/<article_slug>/comments/<int:id>',
         UpdateDeleteCommentView.as_view(),
         name="update-delete-comment"),

    path('comments/<int:id>/history',
         CommentHistoryView.as_view(),
         name="comment-history")
]
