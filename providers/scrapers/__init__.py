from typing import List

from providers.scrapers.base import Scraper
from providers.scrapers.devaart import ScraperDeVaart
from providers.scrapers.jonx import ScraperJonx
from providers.scrapers.oog import ScraperOOG
from providers.scrapers.psytrans import ScraperPsyTrans
from providers.scrapers.radboudumc import ScraperRadboudumc
from providers.scrapers.stepwork import ScraperStepwork
from providers.scrapers.umcg import ScraperUMCG
from providers.scrapers.vumc import ScraperVUmc

scrapers: List[Scraper] = [
    ScraperDeVaart(),
    ScraperJonx(),
    ScraperOOG(),
    ScraperPsyTrans(),
    ScraperRadboudumc(),
    ScraperStepwork(),
    ScraperUMCG(),
    ScraperVUmc()
]
