import re
from typing import TypedDict

from ..util import soup_find_string
from .base import Scraper, ScraperServiceOffering, ScraperServiceTime, TF, TM, CHILDREN, ADOLESCENTS, ADULTS

WEEKS_REGEX = re.compile(r'(\d+) (wk|weken)', re.IGNORECASE)


class ScraperServiceDeVaart(TypedDict):
    match: tuple[str, str]
    offering: ScraperServiceOffering


SERVICES: list[ScraperServiceDeVaart] = [{
    'match': ('Intake', 'Jeugd'),
    'offering': {
        'service': 'Intake',
        'types': [TF, TM],
        'age_groups': [CHILDREN, ADOLESCENTS]
    }
}, {
    'match': ('Intake', 'Volwassen'),
    'offering': {
        'service': 'Intake',
        'types': [TF, TM],
        'age_groups': [ADULTS]
    }
}, {
    'match': ('Behandeling', 'Jeugd'),
    'offering': {
        'service': 'Diagnostics',
        'types': [TF, TM],
        'age_groups': [CHILDREN, ADOLESCENTS]
    }
}, {
    'match': ('Behandeling', 'Volwassen'),
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

        service_times: dict[tuple[str, str], ScraperServiceTime] = {}

        for table in soup.find_all('table'):
            service_name = None

            for table_row in table.tbody.find_all('tr'):
                columns = [column for column in table_row.find_all('td')]
                if len(columns) < 2:
                    continue

                if columns[1].strong:
                    service_name = soup_find_string(columns[1].strong).strip()
                    continue

                name = soup_find_string(columns[0])
                time = soup_find_string(columns[1])
                if not name or 'gender' not in name or not time:
                    continue

                name = name.replace('gender', '').strip()
                result = WEEKS_REGEX.search(time)
                weeks = int(result.group(1))

                if service_name:
                    print(f'{service_name} - {name}')
                    print(f'{weeks} weken')
                else:
                    print('no match')
                    continue

                match = (service_name, name)
                days = weeks * 7

                for service in SERVICES:
                    if service['match'] != match:
                        continue

                    if match not in service_times or days < service_times[match]['days']:
                        # NOTE: the object spread operator would be nicer here, but Python's typing is terrible
                        service_time: ScraperServiceTime = service['offering'].copy()
                        service_time['days'] = days
                        service_time['is_individual'] = False
                        service_time['has_stop'] = False
                        service_times[match] = service_time
                        break

        return list(service_times.values())
