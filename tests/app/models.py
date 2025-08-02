# For test purposes

from django.db import models
from django.utils import timezone

from django_page_resolver.models import PageResolverModel


class TimeStampedModelMixin(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False, null=True)

    class Meta:
        abstract = True


class Post(TimeStampedModelMixin, PageResolverModel):
    title = models.CharField(max_length=100)

    class Meta:
        ordering = ('created_at',)


class Comment(TimeStampedModelMixin, PageResolverModel):
    title = models.CharField(max_length=100)
    post = models.ForeignKey('app.Post', on_delete=models.CASCADE, related_name='comments')

    class Meta:
        ordering = ('created_at',)
