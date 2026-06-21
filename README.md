# Web-Scapper

A basic web scraper with clear structure and clear output.

## Project structure

- `web_scrapper/scraper.py` - core scraping logic and structured result model.
- `web_scrapper/cli.py` - command-line entry point.
- `tests/test_scraper.py` - focused tests for core behavior.

## Usage

```bash
python3 -m web_scrapper.cli https://example.com
```

Example output:

```json
{
  "url": "https://example.com",
  "title": "Example Domain",
  "headings": ["Example Domain"],
  "paragraphs": ["This domain is for use in illustrative examples in documents."],
  "links": ["https://www.iana.org/domains/example"]
}
```
