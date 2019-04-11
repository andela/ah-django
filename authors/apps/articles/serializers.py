from rest_framework import serializers
from .models import Articles, Rating, Likes, Comments, Favorites
from django.db.models import Avg
from authors.apps.authentication.serializers import UserSerializer
from authors.apps.profiles.serializers import ProfileSerializer


class ArticlesSerializer(serializers.ModelSerializer):
    rating_count = serializers.SerializerMethodField(read_only=True, default=0)
    avg_rating = serializers.SerializerMethodField(read_only=True, default=0)
    author = serializers.SerializerMethodField(read_only=True)
    favorited = serializers.SerializerMethodField(
        read_only=True, default=False)
    favoritesCount = serializers.SerializerMethodField(
        read_only=True, default=0)

    class Meta:
        model = Articles
        page_size = serializers.IntegerField()
        favorited_by = serializers.CharField()
        fields = [
            'id',
            'title',
            'description',
            'body',
            'image_url',
            'author',
            'created_at',
            'updated_at',
            'slug',
            'avg_rating',
            'rating_count',
            'tags',
            'favorited',
            'favoritesCount',
        ]
        read_only_fields = ["id", "author", "slug", "created_at", "avg_rating",
                            "rating_count"]

    def create(self, validated_data):
        return Articles.objects.create(**validated_data)

    def get_rating_count(self, obj):
        qs = Rating.objects.filter(article_id=obj.id).count()
        return qs

    def get_avg_rating(self, obj):
        qs = Rating.objects.filter(article_id=obj.id).aggregate(Avg('rating'))
        if qs['rating__avg'] is None:
            return 0
        return qs['rating__avg']

    def get_author(self, obj):

        return {
            "username": obj.author.username,
            "bio": obj.author.bio,
            "image": obj.author.image
        }

    def get_favoritesCount(self, obj):
        count = Favorites.objects.filter(article_id=obj.id).count()
        return count

    def get_favorited(self, obj):
        count = Favorites.objects.filter(article_id=obj.id).count()
        if count > 0:
            return True
        else:
            return False


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = [
            'id',
            'article_id',
            'user_id',
            'rating'
        ]
        read_only_fields = ["id", "author", "created_at"]


class LikesSerializer(serializers.ModelSerializer):
    like = serializers.IntegerField()
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Likes
        fields = ('id', 'article', 'user', 'like', 'created_at')
        read_only_fields = ("id", "article", "created_at", "user")

    def create(self, validated_data):
        return Articles.objects.create(**validated_data)


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = [
            'id',
            'article_slug',
            'created_at',
            'updated_at',
            'body',
            'author'
        ]
        read_only_fields = ["id"]


class TagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Articles
        page_size = serializers.IntegerField()
        fields = [
            'id',
            'tags'
        ]


class FavoritesSerializer(serializers.ModelSerializer):
    """ Define favourite model serializer"""
    article = ArticlesSerializer(many=False, read_only=True, required=False)

    class Meta:
        model = Favorites
        fields = ('id', 'article', 'user', 'created_at')
