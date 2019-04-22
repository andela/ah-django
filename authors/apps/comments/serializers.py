from rest_framework import serializers
from .models import Comments


class CommentsSerializer(serializers.ModelSerializer):
    article = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    highlighted_text = serializers.CharField(
        allow_null=True, min_length=4, required=False)

    class Meta:
        model = Comments
        fields = [
            'id',
            'created_at',
            'updated_at',
            'body',
            'user',
            'highlighted_text',
            'article',

        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        return Comments.objects.create(**validated_data)

    def get_user(self, obj):
        return {"username": obj.user.username,
                "bio": obj.user.bio,
                "image": obj.user.image}

    def get_article(self, obj):
        return obj.article.slug

    def val_highlighted_text(self, text, article):

        if text is not None and text not in article.body:
            msg_d = ["Highlighted text not part of Article ({})".format(
                article.title)]
            msg = {'highlighted_text': msg_d}
            raise serializers.ValidationError(msg)
        else:
            return text
