from rest_framework import serializers
from .models import Review, ReviewRequest
from apps.accounts.serializers import UserSerializer


class ReviewRequestSerializer(serializers.ModelSerializer):
    reviewer = UserSerializer(read_only=True)
    assigned_by = UserSerializer(read_only=True)

    class Meta:
        model = ReviewRequest
        fields = ['id', 'reviewer', 'assigned_by', 'status', 'message', 'created_at']
        read_only_fields = ['status']


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'reviewer', 'status', 'feedback', 'rating', 'is_anonymous', 'created_at']
        read_only_fields = ['status']