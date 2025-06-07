import re
from io import BytesIO
from typing import List, Optional

from pdfreader import SimplePDFViewer


class PDFReader:

    viewer: SimplePDFViewer
    content: str
    lines: List[str]

    def __init__(self, stream: BytesIO):
        self.viewer = SimplePDFViewer(stream)
        self.viewer.render()

        joined = ''
        spaces = 0
        for canvas in self.viewer:
            for string in canvas.strings:
                if string == ' ':
                    spaces += 1
                else:
                    if spaces >= 2:
                        joined += '\n'
                    elif spaces == 1:
                        joined += ' '

                    spaces = 0
                    joined += string.lower()

        self.content = joined
        self.lines = joined.split('\n')

    def find(self, start_text: str, end_text: str) -> Optional[str]:
        start = self.content.find(start_text)
        if start == -1:
            return None

        end = self.content.find(end_text, start + len(start_text))
        if end == -1:
            return None

        return self.content[start:end]

def soup_find_string(soup) -> Optional[str]:
    length = len(soup.contents)
    if length == 0:
        return soup.string
    else:
        for child in soup.contents:
            text = child.string
            if not text:
                continue
            text = text.strip(' \u200b\u00a0')
            if len(text) > 0:
                return text

    return None

def search_last(pattern: re.Pattern, value: str) -> Optional[re.Match]:
    pos = 0
    last_match = None

    while True:
        match = pattern.search(value, pos)
        if not match:
            break

        pos = match.end()
        last_match = match

    return last_match
