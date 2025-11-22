#!/usr/bin/env python3
"""
Import Manual FSA Hygiene Matches with Comprehensive Address Preservation

This script imports manually verified FSA hygiene matches while preserving ALL address data
from all sources (Google Places, licensing, business rates, FSA, etc.).

Shows before/after address comparison for each restaurant.

Author: Claude Code
Date: 2025-11-22
"""

import sqlite3
import pandas as pd
import json
from datetime import datetime
from pathlib import Path

def show_address_comparison(restaurant_id: int, conn: sqlite3.Connection):
    """Show all addresses for a restaurant from all sources."""
    query = """
        SELECT
            restaurant_id,
            name,
            address as basic_address,
            postcode as basic_postcode,
            google_formatted_address,
            google_latitude,
            google_longitude,
            licensing_premises_address,
            business_rates_address,
            business_rates_postcode,
            fsa_address_line1,
            fsa_address_line2,
            fsa_address_line3,
            fsa_postcode
        FROM restaurants
        WHERE restaurant_id = ?
    """

    df = pd.read_sql_query(query, conn, params=(restaurant_id,))

    if len(df) == 0:
        return None

    restaurant = df.iloc[0]

    addresses = {
        'Basic': f"{restaurant.get('basic_address', 'N/A')} {restaurant.get('basic_postcode', 'N/A')}",
        'Google Places': restaurant.get('google_formatted_address', 'N/A'),
        'Licensing': restaurant.get('licensing_premises_address', 'N/A'),
        'Business Rates': f"{restaurant.get('business_rates_address', 'N/A')} {restaurant.get('business_rates_postcode', 'N/A')}",
        'FSA': ' '.join(filter(pd.notna, [
            restaurant.get('fsa_address_line1'),
            restaurant.get('fsa_address_line2'),
            restaurant.get('fsa_address_line3'),
            restaurant.get('fsa_postcode')
        ])) or 'Not yet imported'
    }

    return addresses

def import_fsa_manual_matches(csv_path: str):
    """Import FSA manual matches with comprehensive address preservation."""

    print("=" * 80)
    print("IMPORT FSA MANUAL MATCHES - COMPREHENSIVE ADDRESS PRESERVATION")
    print("=" * 80)
    print(f"CSV File: {csv_path}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Load CSV
    if not Path(csv_path).exists():
        print(f"❌ Error: File not found: {csv_path}")
        return

    matches_df = pd.read_csv(csv_path)
    print(f"Loaded {len(matches_df)} manual matches from CSV\n")

    # Connect to database
    conn = sqlite3.connect('plymouth_research.db')
    cursor = conn.cursor()

    imported_count = 0
    errors = []

    print("=" * 80)
    print("IMPORTING AND SHOWING ADDRESS PRESERVATION")
    print("=" * 80)

    for idx, row in matches_df.iterrows():
        restaurant_id = int(row['restaurant_id'])
        restaurant_name = row['restaurant_name']

        print(f"\n[{idx + 1}/{len(matches_df)}] {restaurant_name} (ID: {restaurant_id})")
        print("-" * 80)

        # Show addresses BEFORE import
        addresses_before = show_address_comparison(restaurant_id, conn)

        if addresses_before:
            print("\n📍 ADDRESSES BEFORE IMPORT:")
            for source, address in addresses_before.items():
                print(f"  {source:20s}: {address}")

        try:
            # Update database - ONLY FSA fields, preserving all other addresses
            cursor.execute("""
                UPDATE restaurants
                SET
                    fsa_id = ?,
                    fsa_business_name = ?,
                    fsa_address_line1 = ?,
                    fsa_address_line2 = ?,
                    fsa_address_line3 = ?,
                    fsa_address_line4 = ?,
                    fsa_postcode = ?,
                    hygiene_rating = ?,
                    hygiene_rating_date = ?,
                    hygiene_score_hygiene = ?,
                    hygiene_score_structural = ?,
                    hygiene_score_confidence = ?,
                    fsa_business_type = ?,
                    fsa_local_authority = ?,
                    hygiene_rating_fetched_at = ?
                WHERE restaurant_id = ?
            """, (
                int(row.get('fsa_id')) if pd.notna(row.get('fsa_id')) else None,
                row.get('fsa_business_name', ''),
                row.get('fsa_address_line1', ''),
                row.get('fsa_address_line2', ''),
                row.get('fsa_address_line3', ''),
                row.get('fsa_address_line4', ''),
                row.get('fsa_postcode', ''),
                int(row.get('hygiene_rating')) if pd.notna(row.get('hygiene_rating')) else None,
                row.get('hygiene_rating_date', ''),
                int(row.get('hygiene_score_hygiene')) if pd.notna(row.get('hygiene_score_hygiene')) else None,
                int(row.get('hygiene_score_structural')) if pd.notna(row.get('hygiene_score_structural')) else None,
                int(row.get('hygiene_score_confidence')) if pd.notna(row.get('hygiene_score_confidence')) else None,
                row.get('fsa_business_type', ''),
                row.get('fsa_local_authority', ''),
                row.get('matched_at', datetime.now().isoformat()),
                restaurant_id
            ))

            imported_count += 1

            # Show addresses AFTER import
            conn.commit()  # Commit so we can see the update
            addresses_after = show_address_comparison(restaurant_id, conn)

            if addresses_after:
                print("\n📍 ADDRESSES AFTER IMPORT:")
                for source, address in addresses_after.items():
                    # Highlight what changed
                    if source == 'FSA' and addresses_before and addresses_before.get(source) != address:
                        print(f"  {source:20s}: {address} ✅ UPDATED")
                    else:
                        print(f"  {source:20s}: {address}")

            # Show import details
            rating = row.get('hygiene_rating')
            if pd.notna(rating):
                stars = '⭐' * int(rating)
                print(f"\n✓ Imported:")
                print(f"  - Hygiene Rating: {stars} ({int(rating)}/5)")
                print(f"  - FSA ID: {row.get('fsa_id', 'N/A')}")
                print(f"  - Business Type: {row.get('fsa_business_type', 'N/A')}")
                print(f"  - Confidence: {row.get('match_confidence', 'N/A'):.1f}")
            else:
                print(f"\n✓ Imported: Awaiting Inspection")

        except Exception as e:
            error_msg = f"Error importing {restaurant_name} (ID: {restaurant_id}): {e}"
            errors.append(error_msg)
            print(f"  ❌ {error_msg}")

    # Final summary
    print("\n" + "=" * 80)
    print("IMPORT COMPLETE - SUMMARY")
    print("=" * 80)
    print(f"Total matches processed: {len(matches_df)}")
    print(f"Successfully imported: {imported_count}")
    print(f"Errors: {len(errors)}")

    if errors:
        print("\n❌ Errors encountered:")
        for error in errors:
            print(f"  - {error}")

    # Verify total coverage
    cursor.execute("""
        SELECT COUNT(*)
        FROM restaurants
        WHERE is_active = 1 AND hygiene_rating IS NOT NULL
    """)
    total_with_fsa = cursor.fetchone()[0]
    print(f"\n✓ Total restaurants with FSA hygiene data: {total_with_fsa}/243 ({total_with_fsa/243*100:.1f}%)")

    conn.close()

    print("\n" + "=" * 80)
    print("ADDRESS PRESERVATION CONFIRMED")
    print("=" * 80)
    print("✅ Google Places addresses: PRESERVED (never modified)")
    print("✅ Licensing addresses: PRESERVED (never modified)")
    print("✅ Business Rates addresses: PRESERVED (never modified)")
    print("✅ FSA addresses: ADDED to dedicated fields")
    print("\nAll address sources remain intact and queryable!")
    print("=" * 80 + "\n")

def main():
    """Main entry point."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python import_fsa_manual_matches.py <csv_file>")
        print("\nExample:")
        print("  python import_fsa_manual_matches.py fsa_manual_matches_20251122_130316.csv")
        sys.exit(1)

    csv_path = sys.argv[1]
    import_fsa_manual_matches(csv_path)

if __name__ == "__main__":
    main()
