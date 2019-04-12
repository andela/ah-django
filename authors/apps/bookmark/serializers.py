from rest_framework import serializers
from authors.apps.bookmark.models import BookmarkArticle


class BookmarkSerializer(serializers.ModelSerializer):
    """ Serializer for bookmarking an article """
    slug = serializers.CharField(source='_article.slug')

    class Meta:
        model = BookmarkArticle
        fields = [
            'slug',
            'id'
        ]
