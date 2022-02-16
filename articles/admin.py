from django.contrib.admin import register, ModelAdmin

from .models import ArticleSource, ArticleSourceFeed, Article


@register(ArticleSource)
class ArticleSourceAdmin(ModelAdmin):
    list_display = ['id', 'name', 'slug', 'website']
    list_filter = []


@register(ArticleSourceFeed)
class ArticleSourceFeedAdmin(ModelAdmin):
    list_display = ['id', 'source', 'name', 'url', 'scraped_at']
    list_filter = ['source', 'scraped_at']


@register(Article)
class ArticleAdmin(ModelAdmin):
    list_display = ['id', 'source', 'title', 'published_at', 'url']
    list_filter = ['source', 'published_at']
