from django.conf.urls import url
from .views import (HighlightApiList, HighlightApiView,)

urlpatterns = [
    url(r'^highlights/(?P<slug>.+)/(?P<highlight_id>\d+)/$',
        HighlightApiView.as_view(), name='get-highlights'),
    url(r'^highlights/(?P<slug>.+)/$',
        HighlightApiList.as_view(), name='create-highlight'),
]
