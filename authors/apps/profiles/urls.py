from django.urls import path
from .views import (ProfileView, ViewAllProfiles)


app_name = "profiles"
urlpatterns = [
    path("profiles/list/", ViewAllProfiles.as_view(), name="all-profiles"),
    path('profiles/<username>/', ProfileView.as_view(), name='put-profile'),
]
