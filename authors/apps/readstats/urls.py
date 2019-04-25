from django.urls import path
from .views import (UserStatsView, ArticStatsView, AdminStatsView)


app_name = "readstats"
urlpatterns = [
    path("user/stats/",
         UserStatsView.as_view(), name="user-stats"),
    path("articles/<slug>/stats/",
         ArticStatsView.as_view(), name="article-stats"),
    path("stats/",
         AdminStatsView.as_view(), name="stats"),

]
