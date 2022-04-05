from calendar import timegm
from datetime import datetime

import feedparser
import pytz
from django.db import transaction
from django.utils import timezone
from django_q.tasks import schedule, Schedule

from transgenderwachttijd.logging import logger

from .models import ArticleSourceFeed, Article

KEYWORDS = ['transgender']


def initialize_tasks():
    if not Schedule.objects.filter(name='scrape_rss_feeds').first():
        schedule('articles.tasks.scrape_rss_feeds', name='scrape_rss_feeds', schedule_type=Schedule.CRON, cron='00 * * * *')


def scrape_rss_feeds():
    feeds = ArticleSourceFeed.objects.all()

    for feed in feeds:
        try:
            with transaction.atomic():
                data = feedparser.parse(feed.url)

                for entry in data.entries:
                    if not hasattr(entry, 'published_parsed'):
                        logger.warn(f'Entry "{entry.link}" of feed "{feed.url}" has no publication date, skipping.')
                        continue

                    published_at = timezone.make_aware(datetime.utcfromtimestamp(timegm(entry.published_parsed)), timezone=pytz.utc)

                    # Check if the current and following entries can be skipped
                    if feed.scraped_at and published_at <= feed.scraped_at:
                        break

                    # Check if this article already exists
                    article = Article.objects.filter(url=entry.link).first()
                    if article:
                        article.feeds.add(feed)
                        break

                    # Sanitize article title and description
                    title = entry.title.lower()
                    description = entry.description.lower() if entry.description else ''

                    # Count keywords in article title and description
                    keyword_count = 0
                    for keyword in KEYWORDS:
                        keyword_count += title.count(keyword)
                        keyword_count += description.count(keyword)

                    # Check if this article contains any keywords
                    if keyword_count == 0:
                        continue

                    # Create article
                    article = Article(
                        url=entry.link,
                        title=entry.title,
                        content=entry.description,
                        published_at=published_at,
                        keyword_count=keyword_count,
                        source=feed.source
                    )

                    # Find an image for this article if available
                    for enclosure in entry.enclosures:
                        if enclosure.type.startswith('image/'):
                            article.image_url = enclosure.href
                            break

                    # Save article and add article feed relation
                    article.save()
                    article.feeds.add(feed)

                # Update feed
                feed.scraped_at = timezone.now()
                feed.save()
        except Exception as err:
            logger.error(f'Failed to scrape RSS feed "{feed.url}":')
            logger.exception(err)
