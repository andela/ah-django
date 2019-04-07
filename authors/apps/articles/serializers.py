from . import models
from rest_framework import serializers


class ArticleSerializer(serializers.ModelSerializer):
    """Articles model serializer"""
    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()
    like_popularity = serializers.SerializerMethodField()
    description = serializers.CharField(required=False)
    tagList = serializers.ListField(
        required=False)

    class Meta:
        """Articles model meta fields"""
        fields = '__all__'
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
        read_only_fields = ('author',)
        model = models.Article

    def get_likes(self, inst):
        return inst.user_reaction.likes.count()

    def get_dislikes(self, inst):
        return inst.user_reaction.dislikes.count()

    def get_like_popularity(self, inst):
        return inst.user_reaction.fetch_popularity_status(avg=True)

    def __repr__(self):
        return self.body
