from providers.scrapers.base import Scraper
from providers.scrapers.radboudumc import ScraperRadboudumc
from providers.scrapers.umcg import ScraperUMCG
from providers.scrapers.vumc import ScraperVUmc


def test(scraper_name: str):
    scraper: Scraper

    if scraper_name == 'vumc':
        scraper = ScraperVUmc()
    elif scraper_name == 'umcg':
        scraper = ScraperUMCG()
    elif scraper_name == 'radboudumc':
        scraper = ScraperRadboudumc()
    else:
        raise Exception(f'Unknown scraper "{scraper_name}"')

    scraper.scrape()


test('radboudumc')
