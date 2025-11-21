#!/usr/bin/env python3
"""
Import Plymouth licensing data from JSON into database.

Reads restaurant_licensing_data.json and updates the restaurants table
with licensing information for matched restaurants.
"""

import sqlite3
import json
from datetime import datetime

def import_licensing_data():
    """Import licensing data from JSON into database."""

    print("=" * 80)
    print("IMPORTING LICENSING DATA")
    print("=" * 80)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Load JSON data
    with open('restaurant_licensing_data.json', 'r', encoding='utf-8') as f:
        restaurants = json.load(f)

    print(f"Loaded {len(restaurants)} restaurants from JSON\n")

    # Connect to database
    conn = sqlite3.connect('plymouth_research.db')
    cursor = conn.cursor()

    updated_count = 0
    skipped_count = 0

    for restaurant in restaurants:
        restaurant_id = restaurant['restaurant_id']
        restaurant_name = restaurant['name']
        licensing = restaurant.get('licensing')

        # Skip if no licensing data found
        if not licensing:
            print(f"[{restaurant_id}] {restaurant_name}: No licensing data - SKIP")
            skipped_count += 1
            continue

        # Extract licensing details
        premises_id = licensing.get('premises_id')
        premises_name = licensing.get('licensing_name')
        premises_address = licensing.get('licensing_address')
        license_number = licensing.get('license_number')
        license_url = licensing.get('license_url')
        dps_name = licensing.get('dps_name')
        scraped_at = licensing.get('scraped_at')

        # Convert arrays to JSON strings for storage
        activities = json.dumps(licensing.get('licensable_activities', []))
        opening_hours = json.dumps(licensing.get('opening_hours', []))

        # Calculate match confidence (simple: 1.0 if names match exactly, 0.8 otherwise)
        if restaurant_name.lower() == premises_name.lower():
            match_confidence = 1.0
        else:
            match_confidence = 0.8

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
            premises_id,
            premises_name,
            premises_address,
            license_number,
            license_url,
            dps_name,
            activities,
            opening_hours,
            scraped_at,
            match_confidence,
            restaurant_id
        ))

        # Show what was updated
        activities_list = licensing.get('licensable_activities', [])
        hours_list = licensing.get('opening_hours', [])

        print(f"[{restaurant_id}] {restaurant_name}:")
        print(f"  ✓ License: {license_number}")
        print(f"  ✓ Premises ID: {premises_id}")
        print(f"  ✓ Opening hours: {len(hours_list)} time periods")
        print(f"  ✓ Activities: {', '.join(activities_list[:2]) if activities_list else 'None'}")
        print(f"  ✓ Match confidence: {match_confidence:.1%}")
        print()

        updated_count += 1

    # Commit changes
    conn.commit()
    conn.close()

    # Summary
    print("=" * 80)
    print("IMPORT COMPLETE")
    print("=" * 80)
    print(f"Total restaurants: {len(restaurants)}")
    print(f"Updated with licensing data: {updated_count}")
    print(f"Skipped (no licensing data): {skipped_count}")
    print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

if __name__ == "__main__":
    import_licensing_data()
