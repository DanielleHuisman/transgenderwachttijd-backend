from transgenderwachttijd.providers.scrapers.base import Scraper
from transgenderwachttijd.providers.scrapers.amc import ScraperAMC
from transgenderwachttijd.providers.scrapers.devaart import ScraperDeVaart
from transgenderwachttijd.providers.scrapers.jonx import ScraperJonx
from transgenderwachttijd.providers.scrapers.oog import ScraperOOG
from transgenderwachttijd.providers.scrapers.psytrans import ScraperPsyTrans
from transgenderwachttijd.providers.scrapers.radboudumc import ScraperRadboudumc
from transgenderwachttijd.providers.scrapers.umcg import ScraperUMCG


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


test('devaart')
