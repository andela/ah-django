from rest_framework import serializers

from authors.apps.stats.models import ReadStats
from authors.apps.profiles.models import Profile
from authors.apps.profiles.serializers import ProfileSerializer
from authors.apps.articles.models import Article


import math


class ReaderStatsSerialer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField()
    read_ratio = serializers.SerializerMethodField()
    views_in_month = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        read_only_fields = ('views', 'reads')
        model = ReadStats

    def get_user(self, inst):
        user = Profile.objects.get(user_id=inst.user.id)
        return ProfileSerializer(user).data

    def get_read_ratio(self, inst):
        try:
            ratio = (inst.reads / inst.views) * 100
        except ArithmeticError:
            return 0
        else:
            return math.ceil(ratio)

    def get_views_in_month(self, inst):
        return Article.get_view_interval(self, author=inst.user, days=30)
