from django.urls import path

from .views import UserReactionView, CommentsLikeReactionAPIView
from .models import UserReaction
from authors.apps.articles.models import Article
from authors.apps.comments.models import Comment

app_name = 'user_reactions'

urlpatterns = [
    path('articles/<slug>/like', UserReactionView.as_view(
        reaction=UserReaction.like, model=Article),
        name='reaction-like'),
    path('articles/<slug>/dislike', UserReactionView.as_view(
        reaction=UserReaction.dislike, model=Article),
        name='reaction-dislike'),
    path('articles/<slug>/comments/<int:id>/dislike',
         CommentsLikeReactionAPIView.as_view(
             reaction=UserReaction.dislike, model=Comment),
         name='reaction-dislike'),
    path('articles/<slug>/comments/<int:id>/like',
         CommentsLikeReactionAPIView.as_view(
             reaction=UserReaction.like, model=Comment),
         name='reaction-dislike')
]
