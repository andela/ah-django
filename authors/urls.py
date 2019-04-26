"""authors URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .apidocs import docs_description


schema_view = get_schema_view(
    openapi.Info(
        title="Authors Haven API",
        default_version='v1',
        description=docs_description,
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@authorshaven.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    # url(r'^docs/', schema_view),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('authors.apps.authentication.urls')),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^oauth/', include('rest_framework_social_oauth2.urls')),
    url(r'^api/', include('authors.apps.articles.urls')),
    url(r'^api/', include('authors.apps.comments.urls')),
    url(r'^api/', include('authors.apps.profiles.urls')),
    url(r'^api/', include('authors.apps.bookmarks.urls')),
    url(r'^api/', include('authors.apps.reports.urls')),
    url(r'^api/', include('authors.apps.notifications.urls')),
    url(r'^api/', include('authors.apps.readstats.urls')),
    url(r'^api/docs/(?P<format>.json|.yaml)$', schema_view.without_ui(
        cache_timeout=None), name='schema-json'),
    url(r'^api/docs/$', schema_view.with_ui('swagger',
                                            cache_timeout=None),
        name='schema-swagger-ui'),
    url(r'^api/redoc/$', schema_view.with_ui('redoc',
                                             cache_timeout=None),
        name='schema-redoc'),
]
