from django.urls import path

from .views import (CommentAPIView, ListCommentsView,
                    ReplyList, ReplyAPIView, CommentHistoryAPIView)

app_name = 'comments'

urlpatterns = [
    path('articles/<slug:slug>/comments',
         ListCommentsView.as_view(),
         name='all-comments'),
    path('articles/<slug:slug>/comments/<int:key>/history',
         CommentHistoryAPIView.as_view(),
         name='comment_history'),
    path('articles/<slug:slug>/comments/<int:id>',
         CommentAPIView.as_view(),
         name='single-comment'),
    path('articles/<slug:slug>/comments/<int:id>/reply',
         ReplyList.as_view(),
         name='comment-reply'),
    path('articles/<slug:slug>/comments/<int:id>/reply/<int:key>',
         ReplyAPIView.as_view(),
         name='comment-reply'),

]
