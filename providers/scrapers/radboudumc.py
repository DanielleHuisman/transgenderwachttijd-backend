import re

from .base import Scraper

WEEKS_REGEX = re.compile(r'(\d+) weken', re.IGNORECASE)


class ScraperRadboudumc(Scraper):

    def get_provider_handle(self) -> str:
        return 'radboudumc'

    def get_source_url(self) -> str:
        return 'https://www.radboudumc.nl/expertisecentra/geslacht-en-gender/waarvoor-kunt-u-bij-ons-terecht/transgenderzorg'

    def scrape(self):
        text = self.fetch_page(self.get_source_url())

        result = WEEKS_REGEX.search(text)
        weeks = int(result.group(1))
        print(f'{weeks} weken')
