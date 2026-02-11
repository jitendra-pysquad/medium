import uuid

from django.contrib.auth import get_user_model
from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from core.models import TimeStampedModel

User = get_user_model()


class Article(TimeStampedModel):
    class STATUS(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        PUBLISHED = 'PUBLISHED', 'Published'
        ARCHIVED = 'ARCHIVED', 'Archived'

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='articles'
    )
    title = models.CharField(max_length=255)
    text = RichTextField()
    image = models.ImageField(upload_to='articles/', null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS.choices,
        default=STATUS.DRAFT
    )
    published_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.author} - {self.title}"

    class Meta:
        ordering = ('-published_at',)
        verbose_name_plural = 'articles'

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'slug': self.slug})

    def generate_short_uuid(self):
        return uuid.uuid4().hex[:5]

    def is_author(self, user):
        return user.is_authenticated and self.author == user

    def can_edit(self, user):
        if not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        return self.author == user

    def can_delete(self, user):
        return user.is_superuser or self.can_edit(user)


    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            self.slug = f"{base_slug}-{self.generate_short_uuid()}"

        if self.status == self.STATUS.PUBLISHED and self.published_at is None:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)


class Comment(TimeStampedModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='replies',
        on_delete=models.CASCADE
    )
    text = models.TextField()
    image = models.ImageField(upload_to='comments/', null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.article}"

    class Meta:
        verbose_name_plural = 'comments'


class Like(TimeStampedModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='likes'
    )

    class Meta:
        unique_together = ('user', 'article')

    def __str__(self):
        return f"{self.user} - {self.article}"
