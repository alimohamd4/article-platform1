from rest_framework import serializers
from .models import Article
from apps.accounts.serializers import UserSerializer
from apps.categories.serializers import CategorySerializer
from apps.categories.models import Category


class ArticleListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        required=False
    )
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'slug', 'description', 'cover_image',
            'author', 'category', 'category_id', 'status',
            'access_level', 'read_time', 'views_count', 'likes_count',
            'comments_count', 'is_featured', 'published_at', 'created_at'
        ]
        read_only_fields = ['slug', 'views_count', 'likes_count', 'published_at']

    def get_comments_count(self, obj):
        return obj.comments.count()


class ArticleDetailSerializer(ArticleListSerializer):
    class Meta(ArticleListSerializer.Meta):
        fields = ArticleListSerializer.Meta.fields + [
            'content', 'pdf_file', 'location'
        ]
