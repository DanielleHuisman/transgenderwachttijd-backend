import re

from ..util import soup_find_string
from .base import Scraper

WEEKS_REGEX = re.compile(r'(\d+) wk', re.IGNORECASE)


class ScraperDeVaart(Scraper):

    def source_url(self):
        return 'https://psychologenpraktijkdevaart.nl/praktijkinfo/wachtlijst-bggz-en-sggz/'

    def scrape(self):
        soup = self.fetch_html_page(self.source_url())

        tables = soup.find_all('table')
        table = tables[2]
        table_body = table.tbody

        waiting_times = []

        for table_row in table_body.children:
            columns = [column for column in table_row.children]

            if columns[1].strong:
                continue

            name = soup_find_string(columns[0])
            result = WEEKS_REGEX.search(soup_find_string(columns[1]))
            weeks = int(result.group(1))
            print(name)
            print(f'{weeks} weken')

            waiting_times.append({
                'name': name,
                'weeks': weeks
            })

        print(waiting_times)
