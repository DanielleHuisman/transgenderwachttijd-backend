import re

from .base import Scraper

WEEKS_REGEX = re.compile('(\d+) weken', re.IGNORECASE)


class ScraperStepwork(Scraper):

    def source_url(self):
        return 'https://stepwork.nl/wachttijden/'

    def scrape(self):
        soup = self.fetch_html_page(self.source_url())

        link = soup.find(id='cl_text_6071be4d219e5').p.a['href']

        reader = self.fetch_pdf_document(link)
        text = reader.find('stepwork transgenderzorg', 'de behandeling')

        result = WEEKS_REGEX.search(text)
        weeks = int(result.group(1))
        print(f'{weeks} weken')
