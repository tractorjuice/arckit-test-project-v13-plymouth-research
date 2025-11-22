#!/usr/bin/env python3
"""
Import verified licensing matches from CSV into database.

Reads licensing_matches_verified.csv and updates the restaurants table
with licensing information.

Author: Claude Code
Date: 2025-11-22
"""

import sqlite3
import pandas as pd
import json
from datetime import datetime

def import_licensing_matches():
    """Import verified licensing matches from CSV into database."""

    print("=" * 80)
    print("IMPORTING VERIFIED LICENSING MATCHES")
    print("=" * 80)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Load verified matches
    matches_df = pd.read_csv('licensing_matches_verified.csv')
    print(f"Loaded {len(matches_df)} verified matches from CSV\n")

    # Connect to database
    conn = sqlite3.connect('plymouth_research.db')
    cursor = conn.cursor()

    updated_count = 0
    errors = []

    for idx, row in matches_df.iterrows():
        restaurant_id = row['restaurant_id']
        restaurant_name = row['restaurant_name']

        try:
            # Parse JSON fields if they're strings
            licensable_activities = row.get('licensable_activities', '[]')
            if isinstance(licensable_activities, str):
                licensable_activities = json.loads(licensable_activities.replace("'", '"'))

            opening_hours = row.get('opening_hours', '[]')
            if isinstance(opening_hours, str):
                # Clean up the string representation
                opening_hours_str = opening_hours.replace("'", '"')
                opening_hours = json.loads(opening_hours_str)

            # Update database
            cursor.execute("""
                UPDATE restaurants
                SET
                    licensing_premises_id = ?,
                    licensing_premises_name = ?,
                    licensing_premises_address = ?,
                    licensing_number = ?,
                    licensing_url = ?,
                    licensing_dps_name = ?,
                    licensing_activities = ?,
                    licensing_opening_hours = ?,
                    licensing_scraped_at = ?,
                    licensing_match_confidence = ?
                WHERE restaurant_id = ?
            """, (
                str(row.get('premises_id', '')),
                row.get('premises_name', ''),
                row.get('premises_address', ''),
                row.get('license_number', ''),
                row.get('license_url', ''),
                row.get('dps_name', ''),
                json.dumps(licensable_activities),
                json.dumps(opening_hours),
                row.get('scraped_at', ''),
                float(row['match_confidence']),
                int(restaurant_id)
            ))

            updated_count += 1

            # Show progress
            activities_count = len(licensable_activities) if isinstance(licensable_activities, list) else 0
            hours_count = len(opening_hours) if isinstance(opening_hours, list) else 0

            print(f"[{idx + 1}/{len(matches_df)}] {restaurant_name}:")
            print(f"  ✓ License: {row.get('license_number', 'N/A')}")
            print(f"  ✓ Premises ID: {row.get('premises_id', 'N/A')}")
            print(f"  ✓ Activities: {activities_count} types")
            print(f"  ✓ Opening hours: {hours_count} periods")
            print(f"  ✓ Confidence: {row['match_confidence']:.1f}%")

        except Exception as e:
            error_msg = f"Error updating {restaurant_name} (ID: {restaurant_id}): {e}"
            errors.append(error_msg)
            print(f"  ✗ {error_msg}")

    # Commit changes
    conn.commit()
    conn.close()

    print("\n" + "=" * 80)
    print("IMPORT COMPLETE - SUMMARY")
    print("=" * 80)
    print(f"Total matches processed: {len(matches_df)}")
    print(f"Successfully updated: {updated_count}")
    print(f"Errors: {len(errors)}")

    if errors:
        print("\nErrors encountered:")
        for error in errors:
            print(f"  - {error}")

    # Verify update
    conn = sqlite3.connect('plymouth_research.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM restaurants
        WHERE is_active = 1 AND licensing_premises_id IS NOT NULL
    """)

    total_with_licensing = cursor.fetchone()[0]
    conn.close()

    print(f"\nTotal restaurants with licensing data: {total_with_licensing}/243")
    print(f"Coverage: {total_with_licensing/243*100:.1f}%")

    print("=" * 80 + "\n")

if __name__ == "__main__":
    import_licensing_matches()
