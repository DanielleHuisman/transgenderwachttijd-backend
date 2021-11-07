import re

from ..util import soup_find_string
from .base import Scraper, ScraperServiceTime, TF, TM, CHILDREN, ADOLESCENTS, ADULTS

YEARS_REGEX = re.compile(r'(\d+)\+? jaar', re.IGNORECASE)


class ScraperOOG(Scraper):

    def get_provider_handle(self) -> str:
        return 'oog'

    def get_source_url(self) -> str:
        return 'https://oogpsychologen.nl/wachttijden/'

    def scrape(self) -> list[ScraperServiceTime]:
        soup = self.fetch_html_page(self.get_source_url())

        headers = soup.find_all('div', class_='elementor-price-list-header')

        for header in headers:
            name = soup_find_string(header.find(class_='elementor-price-list-title'))

            if name.startswith('Genderteam Zuid-Nederland'):
                result = YEARS_REGEX.search(soup_find_string(header.find(class_='elementor-price-list-price')))
                years = int(result.group(1))
                print(name)
                print(f'{years} years')

                return [{
                    'service': 'Intake',
                    'types': [TF, TM],
                    'age_groups': [CHILDREN, ADOLESCENTS, ADULTS],
                    'days': int(years * 365.25),
                    'is_individual': False,
                    'has_stop': False
                }]
        else:
            print('no match')

        return []
