#!/usr/bin/env python3
"""
Address Consistency Checker
============================

Compares addresses across three data sources:
1. FSA (Food Standards Agency) - from hygiene ratings
2. Our scraped data - from restaurant websites
3. Companies House - from official company records

Identifies mismatches that may indicate incorrect data matching.

Author: Plymouth Research Team
Date: 2025-11-20
"""

import sqlite3
import csv
from pathlib import Path
from difflib import SequenceMatcher
from typing import Optional, Tuple


def normalize_address(address: str) -> str:
    """Normalize address for comparison."""
    if not address:
        return ""

    # Convert to lowercase
    normalized = address.lower()

    # Remove common variations
    normalized = normalized.replace("street", "st")
    normalized = normalized.replace("road", "rd")
    normalized = normalized.replace("avenue", "ave")
    normalized = normalized.replace("building", "bldg")
    normalized = normalized.replace("limited", "ltd")
    normalized = normalized.replace("plymouth", "")

    # Remove punctuation and extra whitespace
    normalized = ''.join(c if c.isalnum() or c.isspace() else ' ' for c in normalized)
    normalized = ' '.join(normalized.split())

    return normalized


def calculate_similarity(str1: str, str2: str) -> float:
    """Calculate similarity ratio between two strings."""
    norm1 = normalize_address(str1)
    norm2 = normalize_address(str2)

    if not norm1 or not norm2:
        return 0.0

    return SequenceMatcher(None, norm1, norm2).ratio()


def build_fsa_address(row) -> str:
    """Build full FSA address from components."""
    parts = []

    if row['fsa_address_line1']:
        parts.append(row['fsa_address_line1'])
    if row['fsa_address_line2']:
        parts.append(row['fsa_address_line2'])
    if row['fsa_address_line3']:
        parts.append(row['fsa_address_line3'])
    if row['fsa_address_line4']:
        parts.append(row['fsa_address_line4'])
    if row['fsa_postcode']:
        parts.append(row['fsa_postcode'])

    return ', '.join(parts)


def main():
    """Main execution function."""
    db_path = Path(__file__).parent / "plymouth_research.db"

    if not db_path.exists():
        print(f"❌ Database not found: {db_path}")
        return

    print("=" * 80)
    print("Address Consistency Check")
    print("=" * 80)
    print()

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get all restaurants with FSA data
    cursor.execute("""
        SELECT
            restaurant_id,
            name,
            address as scraped_address,
            company_number,
            company_name,
            company_registered_address,
            fsa_id,
            fsa_business_name,
            fsa_address_line1,
            fsa_address_line2,
            fsa_address_line3,
            fsa_address_line4,
            fsa_postcode,
            hygiene_rating
        FROM restaurants
        WHERE fsa_id IS NOT NULL
        AND is_active = 1
        ORDER BY name
    """)

    restaurants = cursor.fetchall()
    total = len(restaurants)

    print(f"📊 Checking {total} restaurants with FSA data")
    print()

    # Track results
    perfect_matches = []
    good_matches = []
    poor_matches = []
    mismatches = []

    results_data = []

    for resto in restaurants:
        # Build addresses
        fsa_address = build_fsa_address(resto)
        scraped_address = resto['scraped_address'] or ""
        ch_address = resto['company_registered_address'] or ""

        # Calculate similarities
        fsa_vs_scraped = calculate_similarity(fsa_address, scraped_address) if fsa_address and scraped_address else 0.0
        fsa_vs_ch = calculate_similarity(fsa_address, ch_address) if fsa_address and ch_address else 0.0
        scraped_vs_ch = calculate_similarity(scraped_address, ch_address) if scraped_address and ch_address else 0.0

        # Average similarity
        valid_similarities = [s for s in [fsa_vs_scraped, fsa_vs_ch, scraped_vs_ch] if s > 0]
        avg_similarity = sum(valid_similarities) / len(valid_similarities) if valid_similarities else 0.0

        # Categorize
        if avg_similarity >= 0.9:
            perfect_matches.append(resto['name'])
            category = "Perfect"
            emoji = "✅"
        elif avg_similarity >= 0.7:
            good_matches.append(resto['name'])
            category = "Good"
            emoji = "✓"
        elif avg_similarity >= 0.5:
            poor_matches.append(resto['name'])
            category = "Poor"
            emoji = "⚠️"
        else:
            mismatches.append(resto['name'])
            category = "Mismatch"
            emoji = "❌"

        # Store result
        results_data.append({
            'restaurant_id': resto['restaurant_id'],
            'name': resto['name'],
            'fsa_business_name': resto['fsa_business_name'] or 'N/A',
            'company_name': resto['company_name'] or 'N/A',
            'fsa_address': fsa_address,
            'scraped_address': scraped_address,
            'ch_address': ch_address,
            'fsa_vs_scraped': f"{fsa_vs_scraped:.1%}",
            'fsa_vs_ch': f"{fsa_vs_ch:.1%}",
            'scraped_vs_ch': f"{scraped_vs_ch:.1%}",
            'avg_similarity': f"{avg_similarity:.1%}",
            'category': category,
            'hygiene_rating': resto['hygiene_rating']
        })

        # Print if mismatch or poor match
        if avg_similarity < 0.7:
            print(f"{emoji} {resto['name']}")
            print(f"  Category: {category} (Avg: {avg_similarity:.1%})")
            print(f"  FSA Name: {resto['fsa_business_name']}")
            print(f"  Company: {resto['company_name']}")
            print()
            print(f"  FSA Address:")
            print(f"    {fsa_address}")
            print()
            print(f"  Scraped Address:")
            print(f"    {scraped_address}")
            print()
            if ch_address:
                print(f"  Companies House Address:")
                print(f"    {ch_address}")
                print()
            print(f"  Similarities:")
            print(f"    FSA ↔ Scraped: {fsa_vs_scraped:.1%}")
            print(f"    FSA ↔ CH: {fsa_vs_ch:.1%}")
            print(f"    Scraped ↔ CH: {scraped_vs_ch:.1%}")
            print()
            print("-" * 80)
            print()

    # Export results
    output_file = Path(__file__).parent / "address_consistency_report.csv"
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['restaurant_id', 'name', 'fsa_business_name', 'company_name',
                     'fsa_address', 'scraped_address', 'ch_address',
                     'fsa_vs_scraped', 'fsa_vs_ch', 'scraped_vs_ch',
                     'avg_similarity', 'category', 'hygiene_rating']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results_data)

    print(f"📄 Exported full report to: {output_file.name}")
    print()

    # Summary
    print("=" * 80)
    print("Summary")
    print("=" * 80)
    print()

    print(f"✅ Perfect Matches (≥90%): {len(perfect_matches)} ({len(perfect_matches)/total*100:.1f}%)")
    print(f"✓  Good Matches (70-89%): {len(good_matches)} ({len(good_matches)/total*100:.1f}%)")
    print(f"⚠️  Poor Matches (50-69%): {len(poor_matches)} ({len(poor_matches)/total*100:.1f}%)")
    print(f"❌ Mismatches (<50%): {len(mismatches)} ({len(mismatches)/total*100:.1f}%)")
    print()

    if poor_matches or mismatches:
        print("🔍 Restaurants Requiring Manual Review:")
        print()

        if poor_matches:
            print("⚠️  Poor Matches:")
            for name in poor_matches[:10]:  # Show first 10
                print(f"  - {name}")
            if len(poor_matches) > 10:
                print(f"  ... and {len(poor_matches) - 10} more")
            print()

        if mismatches:
            print("❌ Mismatches:")
            for name in mismatches[:10]:  # Show first 10
                print(f"  - {name}")
            if len(mismatches) > 10:
                print(f"  ... and {len(mismatches) - 10} more")
            print()

    print("💡 Recommendation:")
    if len(mismatches) > 0:
        print(f"  Review {len(mismatches)} mismatched restaurants in {output_file.name}")
        print("  These may have incorrect FSA matches or address data issues")
    else:
        print("  All addresses have reasonable similarity - no critical issues found")

    conn.close()


if __name__ == "__main__":
    main()
