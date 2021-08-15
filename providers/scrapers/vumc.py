import re

from .base import Scraper

TIME_REGEX = re.compile(r'(\d+)\s?dagen.+?(\d+)\s?weken', re.IGNORECASE)

SERVICES = [
    ('Eerste consult kinderen', 'eerste consult', 'volwassen'),
    ('Eerste consult volwassenen', 'eerste consult', 'start diagnostiek kinderen'),
    ('Start diagnostiek kinderen', 'start diagnostiek kinderen', 'start diagnostiek volwassenen'),
    ('Start diagnostiek volwassenen', 'start diagnostiek volwassenen', 'hormoonbehandeling'),
    ('Hormoonbehandeling', 'hormoonbehandeling', 'chirurgie'),
    ('Vaginaplastiek', 'vaginaplastiek', 'darm vagina plastiek'),
    ('Darm vagina plastiek', 'darm vagina plastiek', 'borstvergroting'),
    ('Borstvergroting', 'borstvergroting', 'secundaire correcties'),
    ('Secundaire correcties genitale chirurgie', 'secundaire correcties', 'adamsappel correctie'),
    ('Adamsappel', 'adamsappel correctie', 'stem verhogende'),
    ('Stem verhogende operaties', 'stem verhogende operaties', 'aangezichtschirurgie'),
    ('Aangezichtschirurgie', 'aangezichtschirurgie', 'borstverwijdering'),
    ('Borstverwijdering', 'borstverwijdering (mastectomie)', 'borstverwijdering i.c.m. het verwijderen'),
    ('Borstverwijdering i.c.m. verwijdering baarmoeder en eierstokken', 'borstverwijdering i.c.m. het verwijderen',
     'verwijdering baarmoeder en eierstokken'),
    ('Verwijdering baarmoeder en eierstokken', 'verwijdering baarmoeder en eierstokken', 'vagina (colpectomie)'),
    ('Verwijdering vagina', 'vagina (colpectomie)', 'verwijdering baarmoeder en'),
    ('Verwijdering baarmoeder i.c.m. verwijdering vagina', 'verwijdering baarmoeder en', 'metaïdoioplastiek'),
    ('Metaïdoioplastiek', 'metaïdoioplastiek', 'phalloplastiek'),
    ('Phalloplastiek', 'phalloplastiek', '*door de grote toename'),
]


class ScraperVUmc(Scraper):

    def source_url(self):
        return 'https://www.vumc.nl/web/file?uuid=c04a8b57-c3f7-4f35-a71c-f1966c56293d'\
               '&owner=5ec2d559-9d3f-4285-8cbd-140abc921b69'\
               '&contentid=3013'\
               '&disposition=inline'

    def scrape(self):
        reader = self.fetch_pdf_document(self.source_url())
        # print(reader.content)

        month = reader.lines[0]
        year = reader.lines[1]

        print(f'{month} {year}')

        waiting_times = []

        for (name, start, end) in SERVICES:
            result = reader.find(start, end)
            print(name)
            if result:
                print(result)
                times = TIME_REGEX.search(result)
                if times:
                    days = int(times.group(1))
                    weeks = int(times.group(2))

                    waiting_times.append({
                        'name': name,
                        'days': days,
                        'weeks': weeks
                    })

                    print(days, 'days')
                    print(weeks, 'weeks')
                else:
                    print('no match')
            else:
                print('no result')
            print()

        print(waiting_times)
