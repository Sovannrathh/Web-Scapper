from __future__ import annotations

import argparse
import json

from web_scrapper.scraper import scrape_url


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Basic web scraper")
    parser.add_argument("url", help="Target URL to scrape")
    parser.add_argument("--timeout", type=int, default=10, help="Request timeout in seconds")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    result = scrape_url(args.url, timeout=args.timeout)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
