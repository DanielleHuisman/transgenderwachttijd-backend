from typing import List

from providers.scrapers.base import Scraper
from providers.scrapers.amc import ScraperAMC
from providers.scrapers.devaart import ScraperDeVaart
from providers.scrapers.jonx import ScraperJonx
from providers.scrapers.oog import ScraperOOG
from providers.scrapers.psytrans import ScraperPsyTrans
from providers.scrapers.radboudumc import ScraperRadboudumc
from providers.scrapers.umcg import ScraperUMCG

scrapers: List[Scraper] = [
    ScraperAMC(),
    ScraperDeVaart(),
    ScraperJonx(),
    ScraperOOG(),
    ScraperPsyTrans(),
    ScraperRadboudumc(),
    ScraperUMCG(),
]
