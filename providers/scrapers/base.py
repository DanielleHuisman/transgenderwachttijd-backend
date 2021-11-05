from io import BytesIO
from typing import Optional, TypedDict

import requests
from bs4 import BeautifulSoup

from ..util import PDFReader

TF = 'Transfeminine'
TM = 'Transmasculine'
CHILDREN = 'Children'
ADOLESCENTS = 'Adolescents'
ADULTS = 'Adults'


class ScraperServiceTime(TypedDict):
    service: str
    types: list[str]
    age_groups: list[str]
    days: Optional[int]


class Scraper:

    def get_provider_handle(self) -> str:
        raise NotImplementedError()

    def get_source_url(self) -> str:
        raise NotImplementedError()

    def scrape(self) -> list[ScraperServiceTime]:
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
