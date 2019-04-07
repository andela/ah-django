from django.conf.urls import url
from .views import ListCreateFollow, DeleteFollower
from .views import FollowersView, RetrieveFollowing

app_name = 'followers'

urlpatterns = [
    url(r'^profiles/?(?P<username>[a-zA-Z0-9_\.-]{3,255})?/?/follow/?$',
        ListCreateFollow.as_view(), name='follow_url'),
    url(r'^profiles/?(?P<username>[a-zA-Z0-9_\.-]{3,255})?/?/unfollow',
        DeleteFollower.as_view(), name='delete_url'),
    url(r'^profiles/?(?P<username>[a-zA-Z0-9_\.-]{3,255})?/?/followers/',
        FollowersView.as_view(), name='followers_url'),
    url(r'^profiles/?(?P<username>[a-zA-Z0-9_\.-]{3,255})?/?/following/',
        RetrieveFollowing.as_view(), name='following_url'),
]
