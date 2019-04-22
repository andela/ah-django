from rest_framework import serializers
from .models import ReportArticle


class ReportArticleSerializer(serializers.ModelSerializer):
    """ Report article serializer """
    article = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ReportArticle
        fields = (
            'id', 'article', 'user', 'report', 'viewed',
            'action_taken', 'created_at', 'updated_at',
        )
        read_only_fields = ['id', 'article', 'user', 'action_taken']

    def get_article(self, obj):
        return obj.article.slug
