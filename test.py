from providers.scrapers.base import Scraper
from providers.scrapers.devaart import ScraperDeVaart
from providers.scrapers.jonx import ScraperJonx
from providers.scrapers.oog import ScraperOOG
from providers.scrapers.psytrans import ScraperPsyTrans
from providers.scrapers.radboudumc import ScraperRadboudumc
from providers.scrapers.umcg import ScraperUMCG
from providers.scrapers.amc import ScraperAMC


def test(scraper_name: str):
    scraper: Scraper

    if scraper_name == 'amc':
        scraper = ScraperAMC()
    elif scraper_name == 'devaart':
        scraper = ScraperDeVaart()
    elif scraper_name == 'jonx':
        scraper = ScraperJonx()
    elif scraper_name == 'oog':
        scraper = ScraperOOG()
    elif scraper_name == 'psytrans':
        scraper = ScraperPsyTrans()
    elif scraper_name == 'radboudumc':
        scraper = ScraperRadboudumc()
    elif scraper_name == 'umcg':
        scraper = ScraperUMCG()
    else:
        raise Exception(f'Unknown scraper "{scraper_name}"')

    print(scraper.scrape())


test('oog')
