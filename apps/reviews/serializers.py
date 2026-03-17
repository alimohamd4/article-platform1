from rest_framework import serializers
from .models import Review
from apps.accounts.serializers import UserSerializer


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'reviewer', 'status', 'feedback', 'rating', 'is_anonymous', 'created_at']
        read_only_fields = ['status']