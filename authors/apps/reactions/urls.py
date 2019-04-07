from django.urls import path

from .views import UserReactionView
from .models import UserReaction
from authors.apps.articles.models import Article

app_name = 'user_reactions'

urlpatterns = [
    path('articles/<slug>/like', UserReactionView.as_view(
        reaction=UserReaction.like, model=Article),
        name='reaction-like'),
    path('articles/<slug>/dislike', UserReactionView.as_view(
        reaction=UserReaction.dislike, model=Article),
        name='reaction-dislike')
]
