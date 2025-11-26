#!/usr/bin/env python3
"""
Data Collection Entry Point
===========================

Run data collection tasks (scraping, fetching) from the command line.

Usage:
    python run_collection.py --help
    python run_collection.py hygiene --xml data/raw/plymouth_fsa_data.xml
    python run_collection.py trustpilot --restaurant-id 4 --max-pages 10
    python run_collection.py google
    python run_collection.py scrape --url https://example.com/menu

Author: Plymouth Research Team
Date: 2025-11-26
"""

import argparse
import logging
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from shared.config import get_config


def setup_logging(verbose: bool = False):
    """Configure logging."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def run_hygiene(args):
    """Run hygiene ratings fetch."""
    from collection.fetchers.hygiene_fetcher import HygieneFetcher

    config = get_config()
    xml_path = Path(args.xml) if args.xml else config.raw_data_dir / "plymouth_fsa_data.xml"

    fetcher = HygieneFetcher(xml_path=xml_path)
    stats = fetcher.run()

    print(f"\n✅ Hygiene Fetch Complete")
    print(f"   Fetched: {stats['fetched']} establishments")
    print(f"   Matched: {stats['matched']} restaurants")
    print(f"   Errors: {stats['errors']}")


def run_trustpilot(args):
    """Run Trustpilot reviews fetch."""
    from collection.fetchers.trustpilot_fetcher import TrustpilotFetcher

    fetcher = TrustpilotFetcher()
    stats = fetcher.run(
        restaurant_id=args.restaurant_id,
        max_pages=args.max_pages,
    )

    print(f"\n✅ Trustpilot Fetch Complete")
    print(f"   Fetched: {stats['fetched']} reviews")
    print(f"   Stored: {stats['matched']} new reviews")
    print(f"   Errors: {stats['errors']}")


def run_google(args):
    """Run Google Places fetch."""
    from collection.fetchers.google_fetcher import GooglePlacesFetcher

    fetcher = GooglePlacesFetcher()
    stats = fetcher.run(restaurant_id=args.restaurant_id)

    print(f"\n✅ Google Places Fetch Complete")
    print(f"   Fetched: {stats['fetched']} places")
    print(f"   Updated: {stats['matched']} restaurants")
    print(f"   Errors: {stats['errors']}")


def run_scrape(args):
    """Run menu scraper."""
    from collection.scrapers.menu_scraper import MenuScraper
    from processing.database import Database

    db = Database()
    scraper = MenuScraper(db_connection=db)

    success, message, items = scraper.scrape_restaurant(
        restaurant_id=args.restaurant_id or 0,
        website_url=args.url
    )

    print(f"\n{'✅' if success else '❌'} Scrape Complete")
    print(f"   {message}")
    if items:
        print(f"   Items extracted: {len(items)}")


def main():
    parser = argparse.ArgumentParser(
        description="Plymouth Research Data Collection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_collection.py hygiene
  python run_collection.py trustpilot --max-pages 10
  python run_collection.py google --restaurant-id 5
  python run_collection.py scrape --url https://example.com/menu
        """
    )

    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose logging')

    subparsers = parser.add_subparsers(dest='command', help='Collection commands')

    # Hygiene subcommand
    hygiene_parser = subparsers.add_parser('hygiene', help='Fetch FSA hygiene ratings')
    hygiene_parser.add_argument('--xml', type=str, help='Path to FSA XML file')

    # Trustpilot subcommand
    trustpilot_parser = subparsers.add_parser('trustpilot', help='Fetch Trustpilot reviews')
    trustpilot_parser.add_argument('--restaurant-id', type=int, help='Specific restaurant ID')
    trustpilot_parser.add_argument('--max-pages', type=int, default=50, help='Max pages per restaurant')

    # Google subcommand
    google_parser = subparsers.add_parser('google', help='Fetch Google Places data')
    google_parser.add_argument('--restaurant-id', type=int, help='Specific restaurant ID')

    # Scrape subcommand
    scrape_parser = subparsers.add_parser('scrape', help='Scrape a restaurant menu')
    scrape_parser.add_argument('--url', type=str, required=True, help='URL to scrape')
    scrape_parser.add_argument('--restaurant-id', type=int, help='Restaurant ID to associate with')

    args = parser.parse_args()
    setup_logging(args.verbose)

    if args.command == 'hygiene':
        run_hygiene(args)
    elif args.command == 'trustpilot':
        run_trustpilot(args)
    elif args.command == 'google':
        run_google(args)
    elif args.command == 'scrape':
        run_scrape(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
