from typing import List

import strawberry

from .types import ArticleCategory, ArticleCategoryOrder, ArticleSource, ArticleSourceOrder, ArticleSourceFeed, ArticleSourceFeedOrder, Article, ArticleOrder


@strawberry.type
class Query:
    article_category: ArticleCategory = strawberry.django.field()
    article_categories: List[ArticleCategory] = strawberry.django.field(order=ArticleCategoryOrder)

    article_source: ArticleSource = strawberry.django.field()
    article_sources: List[ArticleSource] = strawberry.django.field(order=ArticleSourceOrder)

    article_source_feed: ArticleSourceFeed = strawberry.django.field()
    article_source_feeds: List[ArticleSourceFeed] = strawberry.django.field(order=ArticleSourceFeedOrder)

    article: Article = strawberry.django.field()
    articles: List[Article] = strawberry.django.field(order=ArticleOrder)
