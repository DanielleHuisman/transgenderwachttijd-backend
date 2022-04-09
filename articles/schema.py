import graphene
from graphene_django import DjangoObjectType

from . import models


class ArticleCategory(DjangoObjectType):
    class Meta:
        model = models.ArticleCategory


class ArticleSource(DjangoObjectType):
    class Meta:
        model = models.ArticleSource


class ArticleSourceFeed(DjangoObjectType):
    class Meta:
        model = models.ArticleSourceFeed


class Article(DjangoObjectType):
    class Meta:
        model = models.Article


class Query(graphene.ObjectType):
    article_category = graphene.Field(ArticleCategory, id=graphene.UUID())
    article_categories = graphene.NonNull(graphene.List(graphene.NonNull(ArticleCategory)))

    article_source = graphene.Field(ArticleSource, id=graphene.UUID())
    article_sources = graphene.NonNull(graphene.List(graphene.NonNull(ArticleSource)))

    article_source_feed = graphene.Field(ArticleSourceFeed, id=graphene.UUID())
    article_source_feeds = graphene.NonNull(graphene.List(graphene.NonNull(ArticleSourceFeed)))

    article = graphene.Field(Article, id=graphene.UUID())
    articles = graphene.NonNull(graphene.List(graphene.NonNull(Article)))

    def resolve_article_category(self, _info, **kwargs):
        return models.ArticleCategory.objects.get(id=kwargs['id'])

    def resolve_article_categories(self, _info):
        return models.ArticleCategory.objects.all()

    def resolve_article_source(self, _info, **kwargs):
        return models.ArticleSource.objects.get(id=kwargs['id'])

    def resolve_article_sources(self, _info):
        return models.ArticleSource.objects.all()

    def resolve_article_source_feed(self, _info, **kwargs):
        return models.ArticleSourceFeed.objects.get(id=kwargs['id'])

    def resolve_article_source_feeds(self, _info):
        return models.ArticleSourceFeed.objects.all()

    def resolve_article(self, _info, **kwargs):
        return models.Article.objects.get(id=kwargs['id'])

    def resolve_articles(self, _info):
        return models.Article.objects.all()
