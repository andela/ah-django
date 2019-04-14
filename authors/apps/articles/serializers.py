from rest_framework import serializers
from . import models
from .models import Report
from ..comments.models import Comment
from ..comments.serializers import CommentSerializer
from django.db.models import Avg


class RateArticleSerializer(serializers.ModelSerializer):
    """Rate articles serializer"""

    class Meta:
        """Rate articles model meta fields"""
        model = models.ArticleRating
        fields = ('id',
                  'rater',
                  'article',
                  'rating')
        unique_together = ('rater', 'rating',)
        read_only_fields = ('article', 'rater')


class ArticleSerializer(serializers.ModelSerializer):
    """Articles model serializer"""
    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()
    like_popularity = serializers.SerializerMethodField()
    description = serializers.CharField(required=False)
    tagList = serializers.ListField(
        required=False)
    rating = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        """Articles model meta fields"""
        fields = '__all__'
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
        read_only_fields = ('author', 'rating')
        model = models.Article

    def get_rating(self, slug):
        rating = models.ArticleRating.objects.filter(article=slug) \
            .aggregate(Avg('rating'))
        if not rating['rating__avg']:
            rating = 0
            return rating
        return rating['rating__avg']

    def get_likes(self, inst):
        return inst.user_reaction.likes.count()

    def get_dislikes(self, inst):
        return inst.user_reaction.dislikes.count()

    def get_like_popularity(self, inst):
        return inst.user_reaction.fetch_popularity_status(avg=True)

    def get_comments(self, inst):

        query = Comment.objects.filter(article=inst)
        return CommentSerializer(query, many=True).data

    def __repr__(self):
        return self.body


class ReportSerializer(serializers.ModelSerializer):
    """
    Report article class.
    """

    class Meta:
        model = Report
        fields = ("id", "article_id", "viewed", "action", "violation",
                  "message", "create_at")
