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
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls import include, url
from django.contrib import admin

SchemaView = get_schema_view(
    openapi.Info(
        title="Authors Haven API, Team Deffered",
        default_version='v1',
        description="A Platform for the Creative at Heart",
        terms_of_service="https://www.andela.com",
        contact=openapi.Contact(email="deffered@andela.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^apidocs$',
        SchemaView.with_ui('swagger',
                           cache_timeout=0), name='schema-swagger-ui'),
    url(r'api/', include(('authors.apps.authentication.urls',
                          'authentication'),
                         namespace='authentication')),
    url(r'api/', include(('authors.apps.reactions.urls',
                          'reactions'),
                         namespace='reactions')),
    url('api/', include(('authors.apps.articles.urls',
                         'articles'),
                        namespace='articles')),
]
