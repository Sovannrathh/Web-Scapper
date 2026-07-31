from __future__ import annotations

from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Dict, List
from urllib.error import URLError
from urllib.parse import urljoin
from urllib.request import urlopen


@dataclass
class ScrapedData:
    url: str
    title: str
    headings: List[str]
    paragraphs: List[str]
    links: List[str]

    def to_dict(self) -> Dict[str, object]:
        return {
            "url": self.url,
            "title": self.title,
            "headings": self.headings,
            "paragraphs": self.paragraphs,
            "links": self.links,
        }


class _BasicHTMLParser(HTMLParser):
    def __init__(self, base_url: str) -> None:
        super().__init__()
        self.base_url = base_url
        self.title = ""
        self.headings: List[str] = []
        self.paragraphs: List[str] = []
        self.links: List[str] = []
        self._active_tag = ""
        self._buffer: List[str] = []

    def handle_starttag(self, tag: str, attrs: List[tuple[str, str | None]]) -> None:
        self._active_tag = tag
        self._buffer = []
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.links.append(urljoin(self.base_url, href))

    def handle_data(self, data: str) -> None:
        if self._active_tag:
            self._buffer.append(data)

    def handle_endtag(self, tag: str) -> None:
        text = " ".join(part.strip() for part in self._buffer if part.strip()).strip()
        if not text:
            self._active_tag = ""
            self._buffer = []
            return

        if tag == "title":
            self.title = text
        elif tag in {"h1", "h2", "h3"}:
            self.headings.append(text)
        elif tag == "p":
            self.paragraphs.append(text)

        self._active_tag = ""
        self._buffer = []


class BasicWebScraper:
    """Simple scraper that returns clear structured information from a page."""

    def __init__(self, timeout: int = 10) -> None:
        self.timeout = timeout

    def scrape(self, url: str) -> ScrapedData:
        try:
            with urlopen(url, timeout=self.timeout) as response:
                content_type = response.headers.get("Content-Type", "")
                if "text/html" not in content_type and content_type:
                    raise ValueError(f"URL does not point to HTML content: {content_type}")
                html = response.read().decode("utf-8", errors="replace")
        except URLError as exc:
            raise ValueError(f"Cannot fetch URL '{url}': {exc}") from exc

        parser = _BasicHTMLParser(base_url=url)
        parser.feed(html)

        return ScrapedData(
            url=url,
            title=parser.title,
            headings=parser.headings,
            paragraphs=parser.paragraphs,
            links=parser.links,
        )


def scrape_url(url: str, timeout: int = 10) -> Dict[str, object]:
    return BasicWebScraper(timeout=timeout).scrape(url).to_dict()
