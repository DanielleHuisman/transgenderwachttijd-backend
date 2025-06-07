import re
from typing import TypedDict

from .base import Scraper, ScraperServiceOffering, ScraperServiceTime, TF, TM, CHILDREN, ADOLESCENTS, ADULTS

STOP_REGEXES = [
    re.compile(r'aanmeldstop hanteren', re.IGNORECASE),
    re.compile(r'hanteren (?:momenteel )?een aanmeldstop', re.IGNORECASE)
]
WEEKS_REGEX = re.compile(r'(\d+) weken', re.IGNORECASE)


class ScraperServicePsyTrans(TypedDict):
    match: tuple[str, str, str]
    offering: ScraperServiceOffering


SERVICES: list[ScraperServicePsyTrans] = [{
    'match': ('Intake', 'intake na aanmelding', '</p>'),
    'offering': {
        'service': 'Intake',
        'types': [TF, TM],
        'age_groups': [CHILDREN, ADOLESCENTS, ADULTS]
    }
}, {
    'match': ('Behandeling', 'behandeling na intake', '</p>'),
    'offering': {
        'service': 'Diagnostics',
        'types': [TF, TM],
        'age_groups': [CHILDREN, ADOLESCENTS, ADULTS]
    }
}]


class ScraperPsyTrans(Scraper):

    def get_provider_handle(self) -> str:
        return 'psytrans'

    def get_source_url(self):
        return 'https://psytrans.nl/'

    def scrape(self) -> list[ScraperServiceTime]:
        text = self.fetch_page(self.get_source_url())

        has_stop = False
        for stop_regex in STOP_REGEXES:
            has_stop = stop_regex.search(text) is not None
            if has_stop:
                break

        service_times: list[ScraperServiceTime] = []

        for service in SERVICES:
            (name, start, end) = service['match']

            start_index = text.find(start)
            end_index = text.find(end, start_index)

            if start_index < 0 or end_index < 0:
                raise Exception(f'Match not found for start "{start}" and end "{end}"')

            result = WEEKS_REGEX.search(text[start_index:end_index])
            weeks = int(result.group(1))
            print(name)
            print(f'{weeks} weken')

            # NOTE: the object spread operator would be nicer here, but Python's typing is terrible
            service_time: ScraperServiceTime = service['offering'].copy()
            service_time['days'] = weeks * 7
            service_time['is_individual'] = False
            service_time['has_stop'] = has_stop
            service_times.append(service_time)

        return service_times
