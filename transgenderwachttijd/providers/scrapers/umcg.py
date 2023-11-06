from typing import Optional, TypedDict

from ..util import soup_find_string
from .base import Scraper, ScraperServiceOffering, ScraperServiceTime, TF, TM, ADOLESCENTS, ADULTS

INDIVIDUAL_TEXT = 'individueel'


class ScraperServiceUMCG(TypedDict):
    match: str
    offering: ScraperServiceOffering


SERVICES: list[ScraperServiceUMCG] = [{
    'match': 'Psychiatrie - Intake Genderteam',
    'offering': {
        'service': 'Intake',
        'types': [TF, TM],
        'age_groups': [ADOLESCENTS, ADULTS]
    }
}, {
    'match': 'Gynaecologie - Hysterectomie',
    'offering': {
        'service': 'Hysterectomy',
        'types': [TM],
        'age_groups': [ADULTS]
    }
}, {
    'match': 'Plastische chirurgie - Mastectomie',
    'offering': {
        'service': 'Mastectomy',
        'types': [TM],
        'age_groups': [ADULTS]
    }
}, {
    'match': 'Plastische chirurgie - Vaginaplastiek',
    'offering': {
        'service': 'Vaginaplasty',
        'types': [TF],
        'age_groups': [ADULTS]
    }
}, {
    'match': 'Plastische chirurgie - Secundaire genitale correcties',
    'offering': {
        'service': 'Secondary corrections',
        'types': [TF],
        'age_groups': [ADULTS]
    }
}, {
    'match': 'Plastische chirurgie - Mamma-augmentatie',
    'offering': {
        'service': 'Breast augmentation',
        'types': [TF],
        'age_groups': [ADULTS]
    }
}, {
    'match': 'Plastische chirurgie - Feminisatieoperaties',
    'offering': {
        'service': 'Facial surgery',
        'types': [TF],
        'age_groups': [ADULTS]
    }
}, {
    'match': 'Plastische chirurgie - Phalloplastiek',
    'offering': {
        'service': 'Phalloplasty',
        'types': [TM],
        'age_groups': [ADULTS]
    }
}, {
    'match': 'KNO - Intake Logopedist',
    'offering': {
        'service': 'Speech therapy',
        'types': [TF, TM],
        'age_groups': [ADOLESCENTS, ADULTS]
    }
}]


class ScraperUMCG(Scraper):

    def get_provider_handle(self) -> str:
        return 'umcg'

    def get_source_url(self) -> str:
        return 'https://www.umcg.nl/w/wachttijden-genderteam'

    def scrape(self) -> list[ScraperServiceTime]:
        soup = self.fetch_html_page(self.get_source_url())

        table = soup.find('table', {'data-wachttijden-articleid': True})
        table_body = table.tbody
        last_header: Optional[str] = None

        service_times: list[ScraperServiceTime] = []

        for table_row in table_body.find_all('tr'):
            title = soup_find_string(table_row.th)
            if not title:
                continue

            is_header = table_row.th.em is None
            if is_header:
                last_header = title
                continue

            title = title.split('(')[0].strip()
            name = f'{last_header} - {title}'

            days: Optional[int] = None
            is_individual: bool = False
            for table_column in table_row.find_all('td'):
                content = soup_find_string(table_column)
                if content:
                    if INDIVIDUAL_TEXT in content:
                        is_individual = True
                        break

                    try:
                        days = int(content.replace('>', ''))
                    except ValueError:
                        continue

                    if days:
                        break

            if days or is_individual:
                print(name)
                print(f'{days} days')
                print('individual', is_individual)

                for service in SERVICES:
                    if service['match'] == name:
                        # NOTE: the object spread operator would be nicer here, but Python's typing is terrible
                        service_time: ScraperServiceTime = service['offering'].copy()
                        service_time['days'] = None if is_individual else days
                        service_time['is_individual'] = is_individual
                        service_time['has_stop'] = False
                        service_times.append(service_time)
                        break
                else:
                    print('no match')

        return service_times
