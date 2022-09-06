from typing import List

import strawberry
from strawberry import auto

from . import models


@strawberry.django.type(models.ArticleCategory)
class ArticleCategory:
    id: auto

    name: auto
    slug: auto

    feeds: List['ArticleSourceFeed']


@strawberry.django.ordering.order(models.ArticleCategory)
class ArticleCategoryOrder:
    name: auto
    slug: auto


@strawberry.django.type(models.ArticleSource)
class ArticleSource:
    id: auto

    name: auto
    slug: auto
    website: auto

    feeds: List['ArticleSourceFeed']
    articles: List['Article']


@strawberry.django.ordering.order(models.ArticleSource)
class ArticleSourceOrder:
    name: auto
    slug: auto


@strawberry.django.type(models.ArticleSourceFeed)
class ArticleSourceFeed:
    id: auto

    name: auto
    url: auto
    scraped_at: auto

    source: 'ArticleSource'
    category: 'ArticleCategory'
    articles: List['Article']


@strawberry.django.ordering.order(models.ArticleSourceFeed)
class ArticleSourceFeedOrder:
    name: auto
    scraped_at: auto


@strawberry.django.type(models.Article)
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


@strawberry.django.ordering.order(models.Article)
class ArticleOrder:
    title: auto
    published_at: auto
