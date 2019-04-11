from django.urls.conf import path

from .views import ReaderStatsApiView

app_name = 'reader_stats'


urlpatterns = [
    path('profiles/<str:username>/stats/',
         ReaderStatsApiView.as_view(),
         name='reader_stats'),
]
