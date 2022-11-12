from typing import List

import strawberry
from strawberry import auto

from . import models


@strawberry.django.filters.filter(models.ArticleCategory, lookups=True)
class ArticleCategoryFilter:
    id: auto

    name: auto
    slug: auto

    feeds: 'ArticleSourceFeedFilter'


@strawberry.django.ordering.order(models.ArticleCategory)
class ArticleCategoryOrder:
    id: auto

    name: auto
    slug: auto

    feeds: 'ArticleSourceFeedOrder'


@strawberry.django.type(models.ArticleCategory, filters=ArticleCategoryFilter, order=ArticleCategoryOrder)
class ArticleCategory:
    id: auto

    name: auto
    slug: auto

    feeds: List['ArticleSourceFeed']


@strawberry.django.filters.filter(models.ArticleSource, lookups=True)
class ArticleSourceFilter:
    id: auto

    name: auto
    slug: auto
    website: auto

    feeds: 'ArticleSourceFeedFilter'
    articles: 'ArticleFilter'


@strawberry.django.ordering.order(models.ArticleSource)
class ArticleSourceOrder:
    id: auto

    name: auto
    slug: auto
    website: auto

    feeds: 'ArticleSourceFeedOrder'
    articles: 'ArticleOrder'


@strawberry.django.type(models.ArticleSource, filters=ArticleSourceFilter, order=ArticleSourceOrder)
class ArticleSource:
    id: auto

    name: auto
    slug: auto
    website: auto

    feeds: List['ArticleSourceFeed']
    articles: List['Article']


@strawberry.django.filters.filter(models.ArticleSourceFeed, lookups=True)
class ArticleSourceFeedFilter:
    id: auto

    name: auto
    url: auto
    scraped_at: auto

    source: 'ArticleSourceFilter'
    category: 'ArticleCategoryFilter'
    articles: 'ArticleFilter'


@strawberry.django.ordering.order(models.ArticleSourceFeed)
class ArticleSourceFeedOrder:
    id: auto

    name: auto
    url: auto
    scraped_at: auto

    source: 'ArticleSourceOrder'
    category: 'ArticleCategoryOrder'
    articles: 'ArticleOrder'


@strawberry.django.type(models.ArticleSourceFeed, filters=ArticleSourceFeedFilter, order=ArticleSourceFeedOrder)
class ArticleSourceFeed:
    id: auto

    name: auto
    url: auto
    scraped_at: auto

    source: 'ArticleSource'
    category: 'ArticleCategory'
    articles: List['Article']


@strawberry.django.filters.filter(models.Article, lookups=True)
class ArticleFilter:
    id: auto

    url: auto
    title: auto
    content: auto
    published_at: auto
    image_url: auto
    keyword_count: auto

    source: 'ArticleSourceFilter'
    feed: 'ArticleSourceFeedFilter'


@strawberry.django.ordering.order(models.Article)
class ArticleOrder:
    id: auto

    url: auto
    title: auto
    content: auto
    published_at: auto
    image_url: auto
    keyword_count: auto

    source: 'ArticleSourceOrder'
    feed: 'ArticleSourceFeedOrder'


@strawberry.django.type(models.Article, filters=ArticleFilter, order=ArticleOrder)
class Article:
    id: auto

    url: auto
    title: auto
    content: auto
    published_at: auto
    image_url: auto
    keyword_count: auto

    source: 'ArticleSource'
    feed: 'ArticleSourceFeed'
