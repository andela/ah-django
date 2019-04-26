from django.conf.urls import url

from authors.apps.favorites import views

app_name = "favorites"

urlpatterns = [
    url(r'^favorites/', views.ListAllFavorites.as_view(),
        name='user-favorites'),
    url(r'^articles/?(?P<slug>[a-zA-Z0-9_\.-]{3,255})?/favorite',
        views.FavouritesView.as_view(), name="user-favorite"),
]
