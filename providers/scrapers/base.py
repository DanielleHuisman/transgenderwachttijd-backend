from io import BytesIO

import requests
from bs4 import BeautifulSoup

from ..util import PDFReader


class Scraper:

    def source_url(self):
        raise NotImplementedError()

    def scrape(self):
        raise NotImplementedError()

    def fetch(self, url: str, **kwargs):
        response = requests.get(url, **kwargs)

        if 200 <= response.status_code <= 299:
            return response
        if 400 <= response.status_code <= 599:
            # TODO: improve error handling
            raise Exception('Failed to fetch page')
        else:
            raise Exception(f'Unable to handle status code {response.status_code}')

    def fetch_page(self, url: str, **kwargs):
        response = self.fetch(url, **kwargs)
        return response.text

    def fetch_html_page(self, url: str, **kwargs):
        text = self.fetch_page(url, **kwargs)
        return BeautifulSoup(text, 'html.parser')

    def fetch_document(self, url: str, **kwargs):
        response = self.fetch(url, **kwargs)
        return response.content

    def fetch_pdf_document(self, url: str, **kwargs):
        data = self.fetch_document(url, **kwargs)
        return PDFReader(BytesIO(data))
