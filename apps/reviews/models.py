from django.db import models
from apps.accounts.models import User
from apps.articles.models import Article


class Review(models.Model):

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        IN_PROGRESS = 'in_progress', 'In Progress'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'
        REVISION = 'revision', 'Needs Revision'

    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    feedback = models.TextField(blank=True)
    rating = models.PositiveIntegerField(default=0)
    is_anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['article', 'reviewer']

    def __str__(self):
        return f"{self.reviewer} - {self.article}"