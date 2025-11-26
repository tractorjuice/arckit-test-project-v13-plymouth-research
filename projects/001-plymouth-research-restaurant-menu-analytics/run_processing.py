#!/usr/bin/env python3
"""
Data Processing Entry Point
===========================

Run data processing tasks (matching, importing) from the command line.

Usage:
    python run_processing.py --help
    python run_processing.py stats
    python run_processing.py match --source fsa --file data/raw/fsa.xml
    python run_processing.py import --file data/processed/matches.csv

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


def run_stats(args):
    """Show database statistics."""
    from processing.database import Database

    db = Database()
    stats = db.get_stats()

    print("\n📊 Database Statistics")
    print("=" * 40)
    print(f"Total Restaurants:      {stats['total_restaurants']}")
    print(f"  - Real Data:          {stats['real_restaurants']}")
    print(f"  - With Hygiene:       {stats['restaurants_with_hygiene']}")
    print(f"Menu Items:             {stats['total_menu_items']}")
    print(f"Trustpilot Reviews:     {stats['trustpilot_reviews']}")
    print(f"Google Reviews:         {stats['google_reviews']}")
    print("=" * 40)


def run_match(args):
    """Run fuzzy matching."""
    from processing.matchers.fuzzy_matcher import FuzzyMatcher

    matcher = FuzzyMatcher()

    # Demo matching
    print("\n🔍 Fuzzy Matcher Demo")
    print("=" * 40)

    test_names = [
        ("Rockfish Plymouth Limited", "ROCKFISH"),
        ("The Boathouse Cafe (Plymouth)", "BOATHOUSE CAFE"),
        ("McDonald's Restaurants Ltd", "MCDONALDS"),
    ]

    for raw, _ in test_names:
        normalized = matcher.normalize_name(raw)
        print(f"'{raw}' -> '{normalized}'")

    print("\nTo perform actual matching, use collection commands.")


def run_import(args):
    """Import data from file."""
    print(f"\n📥 Import from: {args.file}")
    print("Import functionality available through scripts/importers/")


def main():
    parser = argparse.ArgumentParser(
        description="Plymouth Research Data Processing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_processing.py stats
  python run_processing.py match --demo
  python run_processing.py import --file data/processed/matches.csv
        """
    )

    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose logging')

    subparsers = parser.add_subparsers(dest='command', help='Processing commands')

    # Stats subcommand
    subparsers.add_parser('stats', help='Show database statistics')

    # Match subcommand
    match_parser = subparsers.add_parser('match', help='Run fuzzy matching')
    match_parser.add_argument('--source', type=str, choices=['fsa', 'licensing', 'rates'], help='Data source')
    match_parser.add_argument('--file', type=str, help='Input file path')
    match_parser.add_argument('--demo', action='store_true', help='Run demo matching')

    # Import subcommand
    import_parser = subparsers.add_parser('import', help='Import matched data')
    import_parser.add_argument('--file', type=str, required=True, help='CSV file to import')

    args = parser.parse_args()
    setup_logging(args.verbose)

    if args.command == 'stats':
        run_stats(args)
    elif args.command == 'match':
        run_match(args)
    elif args.command == 'import':
        run_import(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
