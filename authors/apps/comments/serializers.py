from rest_framework import serializers

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from authors.apps.comments.models import Comment, CommentReply

import re


def validate_body(comment):
    """
        Checks the comment body does not
        contain numbers, or special characters ONLY
    """
    pattern = re.compile(r".*[a-zA-Z].*")

    if not pattern.match(comment):
        raise ValidationError(
            _(f'{comment} misses letters. Provide a readable comment, cool?'),
            params={'body': comment},
        )


class CommentSerializer(serializers.ModelSerializer):
    body = serializers.CharField(validators=[validate_body])
    author = serializers.SerializerMethodField()
    article = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('author', 'created_at', 'updated_at', 'article')

    def get_author(self, inst):
        return inst.author.username

    def get_article(self, inst):
        return inst.article.slug

    def get_replies(self, inst):
        return inst.replies

    def get_likes(self, inst):
        return inst.user_reaction.likes.count()

    def get_dislikes(self, inst):
        return inst.user_reaction.dislikes.count()


class CommentReplySerializer(serializers.ModelSerializer):
    body = serializers.CharField(validators=[validate_body])
    comment_to = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    article = serializers.SerializerMethodField()

    class Meta:
        model = CommentReply
        fields = '__all__'
        read_only_fields = ('author', 'comment_to', 'article',
                            'created_at', 'updated_at',)

    def get_comment_to(self, inst):
        return inst.comment_to.body

    def get_author(self, inst):
        return inst.author.username

    def get_article(self, inst):
        return inst.article.title
