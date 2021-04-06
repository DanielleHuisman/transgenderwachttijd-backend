from io import BytesIO

import requests

from ..util import PDFReader


class Scraper:

    def source_url(self):
        raise NotImplementedError()

    def scrape(self):
        raise NotImplementedError()

    def fetch_document(self, url: str):
        response = requests.get(url)

        if 200 <= response.status_code <= 299:
            return response.content

        # TODO: error handling

        raise Exception('Failed to fetch document')

    def fetch_pdf_document(self, url: str):
        data = self.fetch_document(url)
        return PDFReader(BytesIO(data))
