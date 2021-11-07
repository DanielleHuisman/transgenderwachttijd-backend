import re

from ..util import soup_find_string
from .base import Scraper, ScraperServiceTime, TF, TM, CHILDREN, ADOLESCENTS

DAYS_REGEX = re.compile(r'(\d+) dagen', re.IGNORECASE)


class ScraperJonx(Scraper):

    def get_provider_handle(self) -> str:
        return 'jonx'

    def get_source_url(self) -> str:
        return 'https://www.jonx.nl/over-ons/wachttijden/'

    def scrape(self) -> list[ScraperServiceTime]:
        soup = self.fetch_html_page(self.get_source_url())

        table_rows = soup.select('figure > table > tbody > tr')

        for table_row in table_rows:
            table_columns = table_row.find_all('td')
            if len(table_columns) == 2:
                name = soup_find_string(table_columns[0])
                if name == 'Gender Poli':
                    result = DAYS_REGEX.search(soup_find_string(table_columns[1]))
                    days = int(result.group(1))
                    print(name)
                    print(f'{days} days')

                    return [{
                        'service': 'Intake',
                        'types': [TF, TM],
                        'age_groups': [CHILDREN, ADOLESCENTS],
                        'days': days,
                        'is_individual': False,
                        'has_stop': False
                    }]
        else:
            print('no match')

        return []
