from django_filters import FilterSet, DateFilter, BooleanFilter, CharFilter
from django.utils import timezone
from datetime import timedelta
from .models import Article


class ArticleFilter(FilterSet):
    date_from = DateFilter(field_name='published_at', lookup_expr='gte')
    date_to = DateFilter(field_name='published_at', lookup_expr='lte')
    author = CharFilter(field_name='author__username', lookup_expr='iexact')
    tag = CharFilter(field_name='tags__name', lookup_expr='iexact')

    class Meta:
        model = Article
        fields = ['category__slug', 'status', 'access_level', 'is_featured', 'date_from', 'date_to', 'author', 'tag']