from typing import List

from providers.scrapers.base import Scraper
from providers.scrapers.psytrans import ScraperPsyTrans
from providers.scrapers.radboudumc import ScraperRadboudumc
from providers.scrapers.stepwork import ScraperStepwork
from providers.scrapers.umcg import ScraperUMCG
from providers.scrapers.vumc import ScraperVUmc

scrapers: List[Scraper] = [
    ScraperPsyTrans(),
    ScraperRadboudumc(),
    ScraperStepwork(),
    ScraperUMCG(),
    ScraperVUmc()
]
