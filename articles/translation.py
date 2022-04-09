from modeltranslation.translator import register, TranslationOptions

from .models import ArticleCategory


@register(ArticleCategory)
class ArticleCategoryOptions(TranslationOptions):
    fields = ('name', 'slug')
