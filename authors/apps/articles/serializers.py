from rest_framework import serializers
from . import models


class ArticleSerializer(serializers.ModelSerializer):
    """Articles model serializer"""
    class Meta:
        """Articles model meta fields"""
        fields = ('id',
                  'title',
                  'description',
                  'body',
                  'tagList',
                  'createdAt',
                  'updatedAt',
                  'author',
                  'slug',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
        read_only_fields = ('author',)
        model = models.Article
