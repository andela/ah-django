""" This module defines the url patters for profiles """

from django.conf.urls import url

from .views import (
    ProfileListApi, UpdateUserAPIView, UserProfileView
)

app_name = 'profiles'

urlpatterns = [
    url(r'^profiles/(?P<string>[\w\-]+)/?$',
        UserProfileView.as_view(), name='profile'),
    url(r'^profiles/(?P<string>[\w\-]+)/edit/?$',
        UpdateUserAPIView.as_view(), name='profile_update'),
    url(r'^profiles/?$',
        ProfileListApi.as_view(), name='list_profiles'),
]
