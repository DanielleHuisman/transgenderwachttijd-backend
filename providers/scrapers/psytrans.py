import re

from .base import Scraper

WEEKS_REGEX = re.compile(r'(\d+) weken', re.IGNORECASE)

SERVICES = [
    ('Intake', 'intake na aanmelding', '</p>'),
    ('Behandeling', 'behandeling na intake', '</p>')
]


class ScraperPsyTrans(Scraper):

    def source_url(self):
        return 'https://psytrans.nl/werkwijze/'

    def scrape(self):
        text = self.fetch_page(self.source_url())

        waiting_times = []

        for (name, start, end) in SERVICES:
            start_index = text.find(start)
            end_index = text.find(end, start_index)

            if start_index < 0 or end_index < 0:
                raise Exception(f'Match not found for start "{start}" and end "{end}"')

            result = WEEKS_REGEX.search(text[start_index:end_index])
            weeks = int(result.group(1))
            print(name)
            print(f'{weeks} weken')

            waiting_times.append({
                'name': name,
                'weeks': weeks
            })

        print(waiting_times)
