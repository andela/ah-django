from django.urls import path
from .views import (ProfileView, ViewAllProfiles,
                    FollowersView, FollowView, FollowingView)


app_name = "profiles"
urlpatterns = [
    path("profiles/list/", ViewAllProfiles.as_view(), name="all-profiles"),
    path('profiles/<username>/', ProfileView.as_view(), name='put-profile'),
    path("users/<username>/followers/",
         FollowersView.as_view(), name="view-followers"),
    path("users/<username>/following/",
         FollowingView.as_view(), name="view following"),
    path("users/<username>/follow/", FollowView.as_view(), name="follow-user"),
    path("users/<username>/unfollow/",
         FollowView.as_view(), name="unfollow-user")
]
