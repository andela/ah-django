from django.urls import path
from .views import (ReportArticleView, ListReportView,
                    ReportsView, ReportActionView, FlagArticleView,
                    FlaggedArticlesView)

urlpatterns = [
    path('articles/<article_slug>/report/',
         ReportArticleView.as_view(), name="report-article"),

    path('articles/report/flag/',
         FlaggedArticlesView.as_view(), name="flagged-articles"),

    path('articles/report/<int:id>/',
         ReportsView.as_view(), name="single-report"),

    path('articles/report/list/',
         ListReportView.as_view(), name="list-reports"),

    path('articles/report/<int:id>/action/',
         ReportActionView.as_view(), name="take-action-reports"),

    path('articles/report/<int:id>/flag/',
         FlagArticleView.as_view(), name="flag-article"),

]
