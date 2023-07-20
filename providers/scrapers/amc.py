import re
from typing import TypedDict

from .base import Scraper, ScraperServiceOffering, ScraperServiceTime, TF, TM, CHILDREN, ADOLESCENTS, ADULTS

TITLE_REGEX = re.compile(r'wachtlijst', re.IGNORECASE)
TIME_REGEX = re.compile(r'(\d+(?:[,.]\d+)?)\s?(dagen|jaar).+?(\d+(?:[,.]\d+)?)\s?(weken|jaar)', re.IGNORECASE)
INDIVIDUAL_TEXT = 'individueel'


class ScraperServiceAMC(TypedDict):
    match: tuple[str, str, str]
    offering: ScraperServiceOffering


SERVICES: list[ScraperServiceAMC] = [{
    'match': ('Eerste consult kinderen', 'eerste consult', 'volwassen'),
    'offering': {
        'service': 'Intake',
        'types': [TF, TM],
        'age_groups': [CHILDREN, ADOLESCENTS]
    }
}, {
    'match': ('Eerste consult volwassenen', 'eerste consult', 'start diagnostiek kinderen'),
    'offering': {
        'service': 'Intake',
        'types': [TF, TM],
        'age_groups': [ADULTS]
    }
}, {
    'match': ('Start diagnostiek kinderen', 'start diagnostiek kinderen', 'start diagnostiek volwassenen'),
    'offering': {
        'service': 'Diagnostics',
        'types': [TF, TM],
        'age_groups': [CHILDREN, ADOLESCENTS]
    }
}, {
    'match': ('Start diagnostiek volwassenen', 'start diagnostiek volwassenen', 'hormoonbehandeling'),
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
    'match': ('Phalloplastiek', 'phalloplastiek', 'disclaimer'),
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
        return 'https://www.amc.nl/web/specialismen/genderdysforie/wachttijden.htm'

    def scrape(self) -> list[ScraperServiceTime]:
        soup = self.fetch_html_page(self.get_source_url())

        link = soup.find(class_='pdf', title=TITLE_REGEX)['href']
        if link.startswith('/'):
            link = f'https://www.amc.nl{link}'

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
                times = TIME_REGEX.search(result)
                if times:
                    if times.group(2) == 'jaar':
                        days = round(float(times.group(1).replace(',', '.')) * 365.25)
                    else:
                        days = int(times.group(1))

                    if times.group(4) == 'jaar':
                        weeks = round(float(times.group(3).replace(',', '.')) * 52)
                    else:
                        weeks = int(times.group(3))
                else:
                    print('no match')
                    days = None
                    weeks = None

                print(days, 'days')
                print(weeks, 'weeks')
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
