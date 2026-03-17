from rest_framework import generics, status, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.utils import timezone
from apps.articles.models import Article
from apps.articles.serializers import ArticleListSerializer, ArticleDetailSerializer
from common.permissions import IsAuthorOrReadOnly
from common.pagination import StandardPagination


class ArticleListView(generics.ListCreateAPIView):
    serializer_class = ArticleListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__slug', 'status', 'access_level', 'is_featured']
    search_fields = ['title', 'description', 'content', 'author__username']
    ordering_fields = ['created_at', 'views_count', 'likes_count']
    ordering = ['-created_at']

    def get_queryset(self):
        return Article.objects.filter(status='published').select_related('author', 'category')

    def perform_create(self, serializer):
        status_value = self.request.data.get('status', 'draft')
        published_at = timezone.now() if status_value == 'published' else None
        serializer.save(author=self.request.user, published_at=published_at)


class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer
    permission_classes = [IsAuthorOrReadOnly]
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views_count += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ArticleLikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        if request.user in article.liked_by.all():
            article.liked_by.remove(request.user)
            article.likes_count -= 1
            article.save()
            return Response({'message': 'Unliked.', 'likes_count': article.likes_count})
        article.liked_by.add(request.user)
        article.likes_count += 1
        article.save()
        return Response({'message': 'Liked.', 'likes_count': article.likes_count})


class MyArticlesView(generics.ListAPIView):
    serializer_class = ArticleListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardPagination

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user).order_by('-created_at')
    