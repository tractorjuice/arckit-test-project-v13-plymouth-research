#!/usr/bin/env python3
"""
Code Organization Script
Organizes all Python scripts into proper directory structure:
- scripts/fetchers/ - Data fetching and scraping scripts
- scripts/matchers/ - Data matching scripts
- scripts/importers/ - Data import scripts
- scripts/utilities/ - Utility and one-off scripts
- scripts/scrapers/ - Menu scraping scripts
- archive/obsolete_scripts/ - Old/obsolete versions

Author: Claude Code
Date: 2025-11-22
"""

import os
import shutil
from pathlib import Path
from collections import defaultdict

def organize_code():
    """Organize all Python scripts into proper directory structure."""

    base_dir = Path("/workspaces/arckit-test-project-v13-plymouth-research/projects/001-plymouth-research-restaurant-menu-analytics")
    scripts_dir = base_dir / "scripts"

    # Define directory structure
    directories = {
        'fetchers': scripts_dir / 'fetchers',
        'matchers': scripts_dir / 'matchers',
        'importers': scripts_dir / 'importers',
        'utilities': scripts_dir / 'utilities',
        'scrapers': scripts_dir / 'scrapers',
        'obsolete': base_dir / 'archive' / 'obsolete_scripts'
    }

    # Create directories
    print("=" * 80)
    print("CODE ORGANIZATION - CREATING DIRECTORY STRUCTURE")
    print("=" * 80)
    for name, path in directories.items():
        path.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created: {path}")

    print()

    # Files to keep in root (main applications)
    keep_in_root = [
        'dashboard_app.py',
        'interactive_matcher_app.py',
        'organize_data.py',
        'organize_code.py',  # This script itself
    ]

    # Categorize files
    file_categories = {
        'fetchers': [
            # Active fetchers (v2/latest versions)
            'fetch_hygiene_ratings_v2.py',
            'fetch_trustpilot_reviews.py',
            'fetch_google_reviews.py',
            'fetch_companies_house_data.py',
            'fetch_balance_sheets_v2.py',
            'fetch_directors.py',
            'discover_trustpilot_urls.py',
            'discover_restaurants_google.py',
            'scrape_plymouth_licensing_fixed.py',
        ],

        'matchers': [
            # Active matchers (v3/v2/latest versions)
            'match_business_rates_v3.py',
            'match_fsa_hygiene_v2.py',
            'match_licensing_data.py',
            'interactive_matcher.py',  # Old CLI version
        ],

        'importers': [
            # Import scripts
            'import_fsa_manual_matches.py',
            'import_licensing_matches.py',
            'import_manual_matches_comprehensive.py',
            'import_business_rates.py',
            'import_companies_house_data.py',
            'import_licensing_data.py',
            'import_from_json.py',
        ],

        'utilities': [
            # Utility scripts
            'check_address_consistency.py',
            'calculate_price_ranges.py',
            'apply_optimizations.py',
            'deduplicate_restaurants.py',
            'remove_synthetic_data.py',
            'reorder_tabs.py',
            'debug_contexts.py',
            'test_v2_parser.py',
        ],

        'scrapers': [
            # Menu scraping scripts
            'phase1_discover_menus.py',
            'phase2_extract_menus.py',
        ],

        'obsolete': [
            # Old/obsolete versions
            'dashboard_app_backup.py',
            'fetch_balance_sheets.py',  # v1
            'match_business_rates.py',  # v1
            'match_business_rates_v2.py',  # v2
            'scrape_plymouth_licensing.py',  # old version
            'scrape_restaurant_licensing.py',  # old version
            'poc_download_accounts.py',
            'poc_financial_data.py',
            'poc_parse_ixbrl.py',
        ]
    }

    # Track moved files
    moved = defaultdict(list)
    kept = []

    # Move files
    print("=" * 80)
    print("MOVING FILES")
    print("=" * 80)

    for category, files in file_categories.items():
        dest_dir = directories[category]
        print(f"\n{category.upper()} → {dest_dir}")
        print("-" * 80)

        for filename in files:
            src = base_dir / filename
            dest = dest_dir / filename

            if src.exists():
                shutil.move(str(src), str(dest))
                moved[category].append(filename)
                print(f"  ✓ {filename}")
            else:
                print(f"  ⚠ Not found: {filename}")

    # Report files kept in root
    print(f"\nKEPT IN ROOT (main applications)")
    print("-" * 80)
    for filename in keep_in_root:
        src = base_dir / filename
        if src.exists():
            kept.append(filename)
            print(f"  ✓ {filename}")

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    total = 0
    for category, files in moved.items():
        count = len(files)
        total += count
        print(f"{category:20s}: {count:3d} files")
    print(f"{'kept in root':20s}: {len(kept):3d} files")
    print(f"{'TOTAL organized':20s}: {total:3d} files")

    # Create README files
    create_readmes(directories)

    print("\n" + "=" * 80)
    print("CODE ORGANIZATION COMPLETE")
    print("=" * 80)
    print("\n✅ All scripts organized into:")
    for name, path in directories.items():
        print(f"   - {path}")
    print(f"\n✅ Main applications kept in root:")
    for filename in keep_in_root:
        print(f"   - {filename}")
    print("\n" + "=" * 80)

def create_readmes(directories):
    """Create README files for each script category."""

    readmes = {
        'fetchers': """# Data Fetchers

Scripts for fetching and scraping data from external sources.

## Active Scripts

- **fetch_hygiene_ratings_v2.py** - FSA Food Hygiene Rating Scheme data fetcher (XML-based)
- **fetch_trustpilot_reviews.py** - Scrape Trustpilot reviews
- **fetch_google_reviews.py** - Fetch Google Places reviews via API
- **fetch_companies_house_data.py** - Companies House API data fetcher
- **fetch_balance_sheets_v2.py** - Financial data fetcher (v2)
- **fetch_directors.py** - Company directors data fetcher
- **discover_trustpilot_urls.py** - Multi-strategy Trustpilot URL discovery
- **discover_restaurants_google.py** - Google Places API restaurant discovery
- **scrape_plymouth_licensing_fixed.py** - Plymouth licensing data scraper (fixed version)

## Usage

All fetchers output to `data/raw/` or `data/processed/` directories.

Example:
```bash
python fetch_hygiene_ratings_v2.py
```
""",

        'matchers': """# Data Matchers

Scripts for matching restaurant records across different data sources.

## Active Scripts

- **match_business_rates_v3.py** - Business rates matching (v3 - latest)
- **match_fsa_hygiene_v2.py** - FSA hygiene data matching (v2)
- **match_licensing_data.py** - Licensing data matching
- **interactive_matcher.py** - Old CLI interactive matcher (deprecated - use interactive_matcher_app.py)

## Usage

Matchers read from `data/raw/` and output matches to `data/processed/`.

Example:
```bash
python match_business_rates_v3.py
```
""",

        'importers': """# Data Importers

Scripts for importing matched data into the database.

## Active Scripts

- **import_fsa_manual_matches.py** - Import manual FSA hygiene matches
- **import_licensing_matches.py** - Import licensing matches
- **import_manual_matches_comprehensive.py** - Comprehensive manual match importer
- **import_business_rates.py** - Import business rates data
- **import_companies_house_data.py** - Import Companies House data
- **import_licensing_data.py** - Import licensing data
- **import_from_json.py** - Generic JSON importer

## Usage

All importers read from `data/manual_matches/` or `data/processed/` and update `plymouth_research.db`.

Example:
```bash
python import_fsa_manual_matches.py data/manual_matches/fsa_manual_matches_20251122_134550.csv
```
""",

        'utilities': """# Utilities

Utility scripts for data analysis, cleanup, and maintenance.

## Scripts

- **check_address_consistency.py** - Analyze address consistency across data sources
- **calculate_price_ranges.py** - Calculate restaurant price ranges
- **apply_optimizations.py** - Database optimization script
- **deduplicate_restaurants.py** - Remove duplicate restaurant records
- **remove_synthetic_data.py** - Remove synthetic/test data
- **reorder_tabs.py** - Dashboard tab reordering utility
- **debug_contexts.py** - Debug script for context issues
- **test_v2_parser.py** - Test script for v2 parsers

## Usage

Run as needed for maintenance and analysis tasks.
""",

        'scrapers': """# Menu Scrapers

Scripts for discovering and extracting restaurant menu data.

## Scripts

- **phase1_discover_menus.py** - Discover menu page URLs
- **phase2_extract_menus.py** - Extract menu items from discovered URLs

## Usage

Run in sequence:
```bash
python phase1_discover_menus.py  # Discover menu URLs
python phase2_extract_menus.py   # Extract menu items
```
""",

        'obsolete': """# Obsolete Scripts

Old versions and proof-of-concept scripts kept for reference.

## Contents

- **dashboard_app_backup.py** - Old dashboard backup
- **fetch_balance_sheets.py** - Old balance sheet fetcher (v1)
- **match_business_rates.py** - Old business rates matcher (v1)
- **match_business_rates_v2.py** - Old business rates matcher (v2)
- **scrape_plymouth_licensing.py** - Old licensing scraper
- **scrape_restaurant_licensing.py** - Old restaurant licensing scraper
- **poc_download_accounts.py** - Proof of concept: download accounts
- **poc_financial_data.py** - Proof of concept: financial data
- **poc_parse_ixbrl.py** - Proof of concept: parse iXBRL

## Note

These scripts are archived and not actively maintained. Use newer versions in parent directories.
"""
    }

    # Write README files
    for category, content in readmes.items():
        readme_path = directories[category] / 'README.md'
        with open(readme_path, 'w') as f:
            f.write(content)
        print(f"✓ Created: {readme_path}")

if __name__ == "__main__":
    organize_code()
