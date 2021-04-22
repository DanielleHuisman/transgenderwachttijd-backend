from django_q.tasks import schedule, Schedule

from transgenderwachttijd.logging import logger

from .scrapers import scrapers


def initialize_tasks():
    if not Schedule.objects.filter(name='scrape').first():
        schedule('providers.tasks.scrape', name='scrape', schedule_type=Schedule.CRON, cron='00 12 * * *')


def scrape():
    for scraper in scrapers:
        try:
            scraper.scrape()
        except Exception as err:
            logger.error(f'Failed to scrape using scraper "{type(scraper).__name__}":')
            logger.exception(err)
