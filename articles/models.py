from uuid import uuid4

from django.db import models


class ArticleSource(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    name = models.CharField(max_length=255, unique=True)
    slug = models.CharField(max_length=255, unique=True)
    website = models.URLField(max_length=255)

    def __str__(self):
        return self.name


class ArticleSourceFeed(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    name = models.CharField(max_length=255)
    url = models.URLField(max_length=255, unique=True)
    scraped_at = models.DateTimeField(blank=True, null=True)

    source = models.ForeignKey(ArticleSource, related_name='feeds', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.source.name} - {self.name}'


class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    url = models.URLField(max_length=255, unique=True)
    title = models.TextField()
    content = models.TextField(blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)
    image_url = models.URLField(max_length=255, blank=True, null=True)

    source = models.ForeignKey(ArticleSource, related_name='articles', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.source.name} - {self.title}'
