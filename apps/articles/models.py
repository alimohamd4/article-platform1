from django.db import models
from django.utils.text import slugify
from taggit.managers import TaggableManager
from apps.accounts.models import User
from apps.categories.models import Category


class Article(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'
        UNDER_REVIEW = 'under_review', 'Under Review'
        REJECTED = 'rejected', 'Rejected'

    class AccessLevel(models.TextChoices):
        PUBLIC = 'public', 'Public'
        PRIVATE = 'private', 'Private'
        INSTITUTIONAL = 'institutional', 'Institutional'

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='articles')
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500, unique=True, blank=True)
    description = models.TextField()
    content = models.TextField()
    cover_image = models.ImageField(upload_to='articles/covers/', null=True, blank=True)
    pdf_file = models.FileField(upload_to='articles/pdfs/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    access_level = models.CharField(max_length=20, choices=AccessLevel.choices, default=AccessLevel.PUBLIC)
    tags = TaggableManager(blank=True)
    location = models.CharField(max_length=255, blank=True)
    read_time = models.PositiveIntegerField(default=0)
    views_count = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    citations_count = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    liked_by = models.ManyToManyField(User, related_name='liked_articles', blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)