from django.contrib.admin import register, ModelAdmin
from modeltranslation.admin import TranslationAdmin

from .models import ArticleCategory, ArticleSource, ArticleSourceFeed, Article


@register(ArticleCategory)
class ArticleCategoryAdmin(TranslationAdmin):
    list_display = ['id', 'name', 'slug']
    list_filter = []


@register(ArticleSource)
class ArticleSourceAdmin(ModelAdmin):
    list_display = ['id', 'name', 'slug', 'website']
    list_filter = []


@register(ArticleSourceFeed)
class ArticleSourceFeedAdmin(ModelAdmin):
    list_display = ['id', 'source', 'name', 'category', 'url', 'scraped_at']
    list_filter = ['source', 'category', 'scraped_at']


@register(Article)
class ArticleAdmin(ModelAdmin):
    list_display = ['id', 'source', 'title', 'published_at', 'url']
    list_filter = ['source', 'published_at']
