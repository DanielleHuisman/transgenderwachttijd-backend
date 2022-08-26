from typing import List

import strawberry

from .types import ArticleCategory, ArticleSource, ArticleSourceFeed, Article


@strawberry.type
class Query:
    article_category: ArticleCategory = strawberry.django.field()
    article_categories: List[ArticleCategory] = strawberry.django.field()

    article_source: ArticleSource = strawberry.django.field()
    article_sources: List[ArticleSource] = strawberry.django.field()

    article_source_feed: ArticleSourceFeed = strawberry.django.field()
    article_source_feeds: List[ArticleSourceFeed] = strawberry.django.field()

    article: Article = strawberry.django.field()
    articles: List[Article] = strawberry.django.field()
