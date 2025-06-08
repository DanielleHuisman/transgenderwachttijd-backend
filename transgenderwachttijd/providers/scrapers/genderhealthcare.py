import re

from ..util import soup_find_string
from .base import Scraper, ScraperServiceTime, TF, TM, ADULTS

WEEKS_REGEX = re.compile(r'(\d+)\+? weken', re.IGNORECASE)


class ScraperGenderhealthcare(Scraper):

    def get_provider_handle(self) -> str:
        return 'genderhealthcare'

    def get_source_url(self) -> str:
        return 'https://genderhealthcare.com/wachttijd-transgenderzorg-genderzorg-nederland-genderhealthcare/'

    def scrape(self) -> list[ScraperServiceTime]:
        soup = self.fetch_html_page(self.get_source_url())

        posts = soup.find_all('article', class_='post')

        for post in posts:
            content = post.find(class_='recent-posts-content')

            texts = content.find_all('p')
            if len(texts) == 0:
                continue

            text = soup_find_string(texts[-1])
            result = WEEKS_REGEX.search(text)
            weeks = int(result.group(1))
            print(f'{weeks} weeks')

            return [{
                'service': 'Intake',
                'types': [TF, TM],
                'age_groups': [ADULTS],
                'days': int(weeks * 7),
                'is_individual': False,
                'has_stop': False
            }]
        else:
            print('no match')

        return []
