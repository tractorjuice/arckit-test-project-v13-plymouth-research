#!/usr/bin/env python3
"""
Data Organization Script
Organizes all project data files into proper directory structure:
- data/raw/ - Original source data
- data/processed/ - Generated/transformed data
- data/sample/ - Test/demo data
- data/manual_matches/ - Manual verification outputs

Author: Claude Code
Date: 2025-11-22
"""

import os
import shutil
from pathlib import Path
from collections import defaultdict

def organize_data():
    """Organize all data files into proper directory structure."""

    # Define directory structure
    base_dir = Path("/workspaces/arckit-test-project-v13-plymouth-research/projects/001-plymouth-research-restaurant-menu-analytics")
    data_dir = base_dir / "data"

    directories = {
        'raw': data_dir / 'raw',
        'processed': data_dir / 'processed',
        'sample': data_dir / 'sample',
        'manual_matches': data_dir / 'manual_matches'
    }

    # Create directories
    print("=" * 80)
    print("DATA ORGANIZATION - CREATING DIRECTORY STRUCTURE")
    print("=" * 80)
    for name, path in directories.items():
        path.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created: {path}")

    print()

    # Categorize files
    file_categories = {
        'raw': [
            # FSA raw data
            'plymouth_fsa_data.xml',

            # Licensing raw data (all partials and complete files)
            'plymouth_licensing_complete.json',
            'plymouth_licensing_complete_fixed.json',
            'plymouth_licensing_premises_list.json',
            'restaurant_licensing_data.json',

            # Business rates source
            'plymouth_business_rates_source.csv',
        ],

        'processed': [
            # Business rates matches
            'business_rates_matches_all.csv',
            'business_rates_matches_all_v2.csv',
            'business_rates_matches_all_v3.csv',
            'business_rates_matches_confident.csv',
            'business_rates_matches_confident_v2.csv',
            'business_rates_matches_confident_v3.csv',
            'business_rates_matches_verified_v2.csv',
            'business_rates_matches_verified_v2_final.csv',
            'business_rates_matches_verified_v3.csv',
            'business_rates_unmatched.csv',
            'business_rates_unmatched_v2.csv',
            'business_rates_unmatched_v3.csv',

            # FSA hygiene matches
            'fsa_hygiene_matches_all_v2.csv',
            'fsa_hygiene_matches_confident_v2.csv',
            'fsa_hygiene_matches_verified_v2.csv',
            'fsa_hygiene_unmatched.csv',
            'fsa_hygiene_unmatched_v2.csv',
            'matched_hygiene_ratings.csv',
            'unmatched_hygiene_ratings.csv',
            'google_without_fsa.csv',

            # Licensing matches
            'licensing_matches_all.csv',
            'licensing_matches_confident.csv',
            'licensing_matches_verified.csv',
            'licensing_unmatched.csv',
            'unmatched_licensing.json',

            # Companies House data
            'companies_high_confidence.csv',
            'companies_medium_confidence.csv',
            'companies_low_confidence.csv',
            'balance_sheet_results.csv',

            # Trustpilot data
            'discovered_trustpilot_urls.csv',
            'trustpilot_urls_for_verification.csv',

            # Analysis reports
            'address_consistency_report.csv',

            # Menu extraction
            'restaurant_menu_urls.json',
            'restaurants_extracted.json',
            'failed_restaurants_for_retry.csv',
        ],

        'sample': [
            'synthetic_restaurants_unique.csv',
        ]
    }

    # Add all licensing partial files (both original and fixed)
    for i in range(50, 2251, 50):
        file_categories['raw'].append(f'plymouth_licensing_partial_{i}.json')
        file_categories['raw'].append(f'plymouth_licensing_fixed_partial_{i}.json')

    # Move manual match files from parent directory
    parent_dir = Path("/workspaces/arckit-test-project-v13-plymouth-research")
    manual_match_files = list(parent_dir.glob("*manual_matches*.csv"))

    # Track moved files
    moved = defaultdict(list)

    # Move files
    print("=" * 80)
    print("MOVING FILES")
    print("=" * 80)

    for category, files in file_categories.items():
        dest_dir = directories[category]
        print(f"\n{category.upper()} FILES → {dest_dir}")
        print("-" * 80)

        for filename in files:
            src = base_dir / filename
            dest = dest_dir / filename

            if src.exists():
                shutil.move(str(src), str(dest))
                moved[category].append(filename)
                print(f"  ✓ {filename}")
            elif src.name.startswith('plymouth_licensing'):
                # Skip missing partial files (we may not have all)
                pass
            else:
                print(f"  ⚠ Not found: {filename}")

    # Move manual match files
    if manual_match_files:
        print(f"\nMANUAL MATCH FILES → {directories['manual_matches']}")
        print("-" * 80)
        for src in manual_match_files:
            dest = directories['manual_matches'] / src.name
            shutil.move(str(src), str(dest))
            moved['manual_matches'].append(src.name)
            print(f"  ✓ {src.name}")

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    total = 0
    for category, files in moved.items():
        count = len(files)
        total += count
        print(f"{category:20s}: {count:3d} files")
    print(f"{'TOTAL':20s}: {total:3d} files")

    # Create README
    readme_path = data_dir / 'README.md'
    readme_content = """# Data Directory Structure

This directory contains all data files organized by type:

## raw/
Original source data downloaded or scraped from external sources:
- `plymouth_fsa_data.xml` - FSA Food Hygiene Rating Scheme data (1.8MB)
- `plymouth_licensing_*.json` - Plymouth City Council licensing data (complete + partials)
- `plymouth_business_rates_source.csv` - Plymouth business rates data

## processed/
Generated files from data matching, processing, and analysis:
- `*_matches_*.csv` - Automated matching results (business rates, FSA, licensing)
- `*_unmatched*.csv` - Unmatched restaurants requiring manual review
- `*_verified*.csv` - Manually verified matches
- `companies_*.csv` - Companies House data with confidence scores
- `discovered_trustpilot_urls.csv` - Trustpilot URL discovery results
- `address_consistency_report.csv` - Address quality analysis
- `restaurant_menu_urls.json` - Extracted menu page URLs
- `restaurants_extracted.json` - Scraped restaurant data

## sample/
Test and synthetic data for development:
- `synthetic_restaurants_unique.csv` - Generated test restaurant data

## manual_matches/
Manual verification outputs from interactive matching sessions:
- `licensing_manual_matches_*.csv` - Manually verified licensing matches
- `fsa_manual_matches_*.csv` - Manually verified FSA hygiene matches

---

**Note**: The main database `plymouth_research.db` remains in the project root directory for easy access by all scripts.

**Last Updated**: 2025-11-22
"""

    with open(readme_path, 'w') as f:
        f.write(readme_content)

    print(f"\n✓ Created: {readme_path}")

    print("\n" + "=" * 80)
    print("DATA ORGANIZATION COMPLETE")
    print("=" * 80)
    print("\n✅ All data files organized into:")
    print(f"   - {directories['raw']}")
    print(f"   - {directories['processed']}")
    print(f"   - {directories['sample']}")
    print(f"   - {directories['manual_matches']}")
    print("\n✅ Database remains in project root: plymouth_research.db")
    print("\n" + "=" * 80)

if __name__ == "__main__":
    organize_data()
