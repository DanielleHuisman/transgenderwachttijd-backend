from typing import Optional

from ..util import soup_find_string
from .base import Scraper


class ScraperUMCG(Scraper):

    def get_provider_handle(self) -> str:
        return 'umcg'

    def get_source_url(self) -> str:
        return 'https://www.umcg.nl/NL/Zorg/Volwassenen/Wachttijden/Paginas/Genderteam.aspx'

    def scrape(self):
        soup = self.fetch_html_page(self.get_source_url())

        table = soup.find('table', class_='ms-rteTable-UMCG')
        table_body = table.tbody
        last_header: Optional[str] = None

        for table_row in table_body.children:
            title = soup_find_string(table_row.th)
            if not title:
                continue

            is_header = table_row.th.strong is not None
            if is_header:
                last_header = title
                continue

            title = title.split('(')[0].strip()

            weeks: Optional[int] = None
            for table_column in table_row.children:
                content = soup_find_string(table_column)
                if content:
                    try:
                        weeks = int(content.replace('>', ''))
                    except ValueError:
                        continue

                    if weeks:
                        break

            if weeks:
                print(f'{last_header} - {title}')
                print(f'{weeks} weeks')
