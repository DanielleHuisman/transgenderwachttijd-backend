import re

from .base import Scraper

HREF_REGEX = re.compile(r'wachttijden', re.IGNORECASE)
WEEKS_REGEX = re.compile(r'(\d+) weken', re.IGNORECASE)


class ScraperStepwork(Scraper):

    def get_provider_handle(self) -> str:
        return 'stepwork'

    def get_source_url(self) -> str:
        return 'https://stepwork.nl/wachttijden/'

    def scrape(self):
        soup = self.fetch_html_page(self.get_source_url())

        link = soup.find(class_='customize-unpreviewable', href=HREF_REGEX)['href']

        reader = self.fetch_pdf_document(link)
        text = reader.find('stepwork transgenderzorg', 'de behandeling')

        result = WEEKS_REGEX.search(text)
        weeks = int(result.group(1))
        print(f'{weeks} weken')
