import re
from typing import TypedDict

from .base import Scraper, ScraperServiceTime, TF, TM, CHILDREN, ADOLESCENTS, ADULTS

TIME_REGEX = re.compile(r'(\d+)\s?dagen.+?(\d+)\s?weken', re.IGNORECASE)


class ScraperServiceVUmc(TypedDict):
    match: tuple[str, str, str]
    offering: ScraperServiceTime


SERVICES: list[ScraperServiceVUmc] = [{
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
        'service': 'Vaginoplasty',
        'types': [TF],
        'age_groups': [ADULTS]
    }
}, {
    'match': ('Darm vagina plastiek', 'darm vagina plastiek', 'borstvergroting'),
    'offering': {
        'service': 'Colovaginoplasty',
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
    'match': ('Borstverwijdering', 'borstverwijdering (mastectomie)', 'borstverwijdering i.c.m. het verwijderen'),
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
    'match': ('Verwijdering vagina', 'vagina (colpectomie)', 'verwijdering baarmoeder en'),
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
    'match': ('Phalloplastiek', 'phalloplastiek', '*door de grote toename'),
    'offering': {
        'service': 'Phalloplasty',
        'types': [TM],
        'age_groups': [ADULTS]
    }
}]

# NOTE: Combinations surgeries are currently not supported
# ('Borstverwijdering i.c.m. verwijdering baarmoeder en eierstokken', 'borstverwijdering i.c.m. het verwijderen', 'verwijdering baarmoeder en eierstokken')
# ('Verwijdering baarmoeder i.c.m. verwijdering vagina', 'verwijdering baarmoeder en', 'metaïdoioplastiek')


class ScraperVUmc(Scraper):

    def get_provider_handle(self) -> str:
        return 'amsterdam-umc'

    def get_source_url(self) -> str:
        return 'https://www.vumc.nl/web/file?uuid=c04a8b57-c3f7-4f35-a71c-f1966c56293d'\
               '&owner=5ec2d559-9d3f-4285-8cbd-140abc921b69'\
               '&contentid=3013'\
               '&disposition=inline'

    def scrape(self) -> list[ScraperServiceTime]:
        reader = self.fetch_pdf_document(self.get_source_url())

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
                times = TIME_REGEX.search(result)
                if times:
                    days = int(times.group(1))
                    weeks = int(times.group(2))

                    print(days, 'days')
                    print(weeks, 'weeks')

                    # NOTE: the object spread operator would be nicer here, but Python's typing is terrible
                    service_time: ScraperServiceTime = service['offering'].copy()
                    service_time['days'] = days
                    service_times.append(service_time)
                else:
                    print('no match')
            else:
                print('no result')
            print()

        return service_times
