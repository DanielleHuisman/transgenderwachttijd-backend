import re
from typing import TypedDict

from ..util import search_last
from .base import Scraper, ScraperServiceOffering, ScraperServiceTime, TF, TM, CHILDREN, ADOLESCENTS, ADULTS

HREF_REGEX = re.compile(r'wachtlijst', re.IGNORECASE)
TIME_REGEX = re.compile(r'(\d+(?:[,.]\d+)?)\s?(dagen|week|weken|maand|maanden|jaar)', re.IGNORECASE)
INDIVIDUAL_TEXT = 'individueel'


class ScraperServiceAMC(TypedDict):
    match: tuple[str, str, str]
    offering: ScraperServiceOffering


SERVICES: list[ScraperServiceAMC] = [{
    'match': ('Eerste consult kinderen', 'kinderen/adolescenten: eerste consult', 'volwassen'),
    'offering': {
        'service': 'Intake',
        'types': [TF, TM],
        'age_groups': [CHILDREN, ADOLESCENTS]
    }
}, {
    'match': ('Eerste consult volwassenen', 'volwassenen: eerste consult', 'kinderen/ adolescenten'),
    'offering': {
        'service': 'Intake',
        'types': [TF, TM],
        'age_groups': [ADULTS]
    }
}, {
    'match': ('Start diagnostiek kinderen', 'kinderen/ adolescenten: start diagnostiek', 'volwassenen'),
    'offering': {
        'service': 'Diagnostics',
        'types': [TF, TM],
        'age_groups': [CHILDREN, ADOLESCENTS]
    }
}, {
    'match': ('Start diagnostiek volwassenen', 'volwassenen: start diagnostiek', 'hormoonbehandeling'),
    'offering': {
        'service': 'Diagnostics',
        'types': [TF, TM],
        'age_groups': [ADULTS]
    }
}, {
    'match': ('Hormoonbehandeling', 'hormoonbehandeling', 'chirurgie'),
    'offering': {
        'service': 'Hormone therapy',
        'types': [TF, TM],
        'age_groups': [CHILDREN, ADOLESCENTS, ADULTS]
    }
}, {
    'match': ('Vaginaplastiek', 'vaginaplastiek', 'darm vagina plastiek'),
    'offering': {
        'service': 'Vaginaplasty',
        'types': [TF],
        'age_groups': [ADULTS]
    }
}, {
    'match': ('Darm vagina plastiek', 'darm vagina plastiek', 'borstvergroting'),
    'offering': {
        'service': 'Colovaginaplasty',
        'types': [TF],
        'age_groups': [ADULTS]
    }
}, {
    'match': ('Borstvergroting', 'borstvergroting', 'secundaire correcties'),
    'offering': {
        'service': 'Breast augmentation',
        'types': [TF],
        'age_groups': [ADULTS]
    }
}, {
    'match': ('Secundaire correcties genitale chirurgie', 'secundaire correcties', 'adamsappel correctie'),
    'offering': {
        'service': 'Secondary corrections',
        'types': [TF, TM],
        'age_groups': [ADULTS]
    }
}, {
    'match': ('Adamsappel', 'adamsappel correctie', 'stem verhogende'),
    'offering': {
        'service': 'Tracheal shave',
        'types': [TF],
        'age_groups': [ADULTS]
    }
}, {
    'match': ('Stem verhogende operaties', 'stem verhogende operaties', 'aangezichtschirurgie'),
    'offering': {
        'service': 'Voice altering surgery',
        'types': [TF],
        'age_groups': [ADULTS]
    }
}, {
    'match': ('Aangezichtschirurgie', 'aangezichtschirurgie', 'borstverwijdering'),
    'offering': {
        'service': 'Facial surgery',
        'types': [TF],
        'age_groups': [ADULTS]
    }
}, {
    'match': ('Borstverwijdering', 'borstverwijdering (mastectomie)', 'borstverwijdering'),
    'offering': {
        'service': 'Mastectomy',
        'types': [TM],
        'age_groups': [ADULTS]
    }
}, {
    'match': ('Verwijdering baarmoeder en eierstokken', 'verwijdering baarmoeder en eierstokken', 'vagina (colpectomie)'),
    'offering': {
        'service': 'Hysterectomy',
        'types': [TM],
        'age_groups': [ADULTS]
    }
}, {
    'match': ('Verwijdering vagina', 'vagina (colpectomie)', 'verwijdering'),
    'offering': {
        'service': 'Colpectomy',
        'types': [TM],
        'age_groups': [ADULTS],
    }
}, {
    'match': ('Metaïdoioplastiek', 'metaïdoioplastiek', 'phalloplastiek'),
    'offering': {
        'service': 'Metaidoioplasty',
        'types': [TM],
        'age_groups': [ADULTS]
    }
}, {
    'match': ('Phalloplastiek', 'phalloplastiek', 'uitleg wachttijden'),
    'offering': {
        'service': 'Phalloplasty',
        'types': [TM],
        'age_groups': [ADULTS]
    }
}]

# NOTE: Combinations surgeries are currently not supported
# ('Borstverwijdering i.c.m. verwijdering baarmoeder en eierstokken', 'borstverwijdering i.c.m. het verwijderen', 'verwijdering baarmoeder en eierstokken')
# ('Verwijdering baarmoeder i.c.m. verwijdering vagina', 'verwijdering baarmoeder en', 'metaïdoioplastiek')


class ScraperAMC(Scraper):

    def get_provider_handle(self) -> str:
        return 'amsterdam-umc'

    def get_source_url(self) -> str:
        return 'https://www.amsterdamumc.nl/nl/genderdysforie/wachttijden.htm'

    def scrape(self) -> list[ScraperServiceTime]:
        soup = self.fetch_html_page(self.get_source_url())

        link = soup.find(class_='download', href=HREF_REGEX)['href']
        if link.startswith('/'):
            link = f'https://www.amsterdamumc.nl/{link}'

        reader = self.fetch_pdf_document(link)

        # month = reader.lines[0]
        # year = reader.lines[1]
        # print(f'{month} {year}')

        service_times: list[ScraperServiceTime] = []

        for service in SERVICES:
            (name, start, end) = service['match']

            result = reader.find(start, end)
            print(name)
            if result:
                print(result)
                is_individual = INDIVIDUAL_TEXT in result
                times = search_last(TIME_REGEX, result)
                if times:
                    unit = times.group(2)
                    if unit == 'jaar':
                        days = round(float(times.group(1).replace(',', '.')) * 365.25)
                    elif unit == 'maand' or unit == 'maanden':
                        days = round(float(times.group(1).replace(',', '.')) * 30)
                    elif unit == 'week' or unit == 'weken':
                        days = round(float(times.group(1).replace(',', '.')) * 7)
                    elif unit == 'dagen':
                        days = int(times.group(1))
                    else:
                        print('unknown unit', unit)
                        days = None
                else:
                    print('no match')
                    days = None

                print(days, 'days')
                print('individual',  is_individual)

                # NOTE: the object spread operator would be nicer here, but Python's typing is terrible
                service_time: ScraperServiceTime = service['offering'].copy()
                service_time['days'] = None if is_individual else days
                service_time['is_individual'] = is_individual
                service_time['has_stop'] = False
                service_times.append(service_time)
            else:
                print('no result')
            print()

        return service_times
