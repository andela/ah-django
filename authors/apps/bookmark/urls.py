from django.conf.urls import url
from .views import BookmarkAPIView, BookmarkListAPIView

app_name = "bookmark"

urlpatterns = [
    url(r'^articles/?(?P<slug>[a-zA-Z0-9_\.-]{3,255})?/bookmark/?$',
        BookmarkAPIView.as_view(), name='bookmark-article'),
    url(r'^bookmark/all/$',
        BookmarkListAPIView.as_view(), name='get-bookmark'),
]
