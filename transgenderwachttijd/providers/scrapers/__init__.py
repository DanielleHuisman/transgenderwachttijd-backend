from typing import List

from transgenderwachttijd.providers.scrapers.base import Scraper
from transgenderwachttijd.providers.scrapers.amc import ScraperAMC
from transgenderwachttijd.providers.scrapers.devaart import ScraperDeVaart
from transgenderwachttijd.providers.scrapers.jonx import ScraperJonx
from transgenderwachttijd.providers.scrapers.oog import ScraperOOG
from transgenderwachttijd.providers.scrapers.psytrans import ScraperPsyTrans
from transgenderwachttijd.providers.scrapers.radboudumc import ScraperRadboudumc
from transgenderwachttijd.providers.scrapers.umcg import ScraperUMCG

scrapers: List[Scraper] = [
    ScraperAMC(),
    ScraperDeVaart(),
    ScraperJonx(),
    ScraperOOG(),
    ScraperPsyTrans(),
    ScraperRadboudumc(),
    ScraperUMCG(),
]
