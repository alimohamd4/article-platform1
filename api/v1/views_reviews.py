from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404
from apps.reviews.models import Review
from apps.reviews.serializers import ReviewSerializer
from apps.articles.models import Article
from common.permissions import IsReviewerOrReadOnly


class ReviewListView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        slug = self.kwargs['slug']
        return Review.objects.filter(article__slug=slug).select_related('reviewer')

    def perform_create(self, serializer):
        article = get_object_or_404(Article, slug=self.kwargs['slug'])
        serializer.save(reviewer=self.request.user, article=article)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewerOrReadOnly]