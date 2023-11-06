import re

from .base import Scraper, ScraperServiceTime, TF, TM, CHILDREN, ADOLESCENTS, ADULTS

WEEKS_REGEX = re.compile(r'(\d+) weken', re.IGNORECASE)


class ScraperRadboudumc(Scraper):

    def get_provider_handle(self) -> str:
        return 'radboudumc'

    def get_source_url(self) -> str:
        return 'https://www.radboudumc.nl/expertisecentra/geslacht-en-gender/waarvoor-kunt-u-bij-ons-terecht/transgenderzorg'

    def scrape(self) -> list[ScraperServiceTime]:
        text = self.fetch_page(self.get_source_url())

        result = WEEKS_REGEX.search(text)
        weeks = int(result.group(1))
        print(f'{weeks} weken')

        return [{
            'service': 'Intake',
            'types': [TF, TM],
            'age_groups': [CHILDREN, ADOLESCENTS, ADULTS],
            'days': weeks * 7,
            'is_individual': False,
            'has_stop': False
        }]
