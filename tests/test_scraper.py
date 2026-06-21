import json
import pathlib
import tempfile
import unittest

from web_scrapper.scraper import scrape_url


class ScraperTests(unittest.TestCase):
    def test_scrape_url_returns_clear_structure(self) -> None:
        html = """
        <html>
          <head><title>Sample Page</title></head>
          <body>
            <h1>Welcome</h1>
            <p>First paragraph.</p>
            <a href="docs">Read docs</a>
          </body>
        </html>
        """

        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = pathlib.Path(temp_dir) / "sample.html"
            file_path.write_text(html, encoding="utf-8")
            result = scrape_url(file_path.as_uri())

        self.assertEqual(result["title"], "Sample Page")
        self.assertEqual(result["headings"], ["Welcome"])
        self.assertEqual(result["paragraphs"], ["First paragraph."])
        self.assertEqual(result["links"], [file_path.as_uri().replace("sample.html", "docs")])

    def test_result_is_json_serializable(self) -> None:
        data = {
            "url": "https://example.com",
            "title": "Example",
            "headings": ["Hello"],
            "paragraphs": ["World"],
            "links": ["https://example.com/path"],
        }
        encoded = json.dumps(data)
        decoded = json.loads(encoded)
        self.assertEqual(decoded["title"], "Example")


if __name__ == "__main__":
    unittest.main()
