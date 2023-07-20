import re
from typing import TypedDict

from ..util import soup_find_string
from .base import Scraper, ScraperServiceOffering, ScraperServiceTime, TF, TM, CHILDREN, ADOLESCENTS, ADULTS

WEEKS_REGEX = re.compile(r'(\d+) wk', re.IGNORECASE)


class ScraperServiceDeVaart(TypedDict):
    match: str
    offering: ScraperServiceOffering


SERVICES: list[ScraperServiceDeVaart] = [{
    'match': 'Intake jeugd',
    'offering': {
        'service': 'Intake',
        'types': [TF, TM],
        'age_groups': [CHILDREN, ADOLESCENTS]
    }
}, {
    'match': 'Intake volwassenen',
    'offering': {
        'service': 'Intake',
        'types': [TF, TM],
        'age_groups': [ADULTS]
    }
}, {
    'match': 'Behandeling jeugd',
    'offering': {
        'service': 'Diagnostics',
        'types': [TF, TM],
        'age_groups': [CHILDREN, ADOLESCENTS]
    }
}, {
    'match': 'Behandeling volwassenen',
    'offering': {
        'service': 'Diagnostics',
        'types': [TF, TM],
        'age_groups': [ADULTS]
    }
}]


class ScraperDeVaart(Scraper):

    def get_provider_handle(self) -> str:
        return 'de-vaart'

    def get_source_url(self) -> str:
        return 'https://psychologenpraktijkdevaart.nl/praktijkinfo/wachtlijst-bggz-en-sggz/'

    def scrape(self) -> list[ScraperServiceTime]:
        soup = self.fetch_html_page(self.get_source_url())

        tables = soup.find_all('table')
        table = tables[2]
        table_body = table.tbody

        service_times: list[ScraperServiceTime] = []

        for table_row in table_body.children:
            columns = [column for column in table_row.children]

            if columns[1].strong:
                continue

            name = soup_find_string(columns[0])
            result = WEEKS_REGEX.search(soup_find_string(columns[1]))
            weeks = int(result.group(1))
            print(name)
            print(f'{weeks} weken')

            for service in SERVICES:
                if service['match'] == name:
                    # NOTE: the object spread operator would be nicer here, but Python's typing is terrible
                    service_time: ScraperServiceTime = service['offering'].copy()
                    service_time['days'] = weeks * 7
                    service_time['is_individual'] = False
                    service_time['has_stop'] = False
                    service_times.append(service_time)
                    break
            else:
                print('no match')

        return service_times
