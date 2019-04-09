from django_filters import rest_framework as filters
from .models import Articles


class ArticleFilter(filters.FilterSet):
    author = filters.CharFilter(field_name='author__username', lookup_expr='iexact')
    title = filters.CharFilter(lookup_expr='icontains')
    tag = filters.CharFilter(field_name='tags', lookup_expr='icontains')

    class Meta:
        model = Articles
        fields = ['author', 'title', 'tag']
