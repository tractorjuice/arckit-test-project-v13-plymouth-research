#!/usr/bin/env python3
"""
Import Business Rates Data into Database

Reads matched business rates CSV and updates the restaurants table.

Usage:
    python import_business_rates.py
"""

import sqlite3
import pandas as pd
from datetime import datetime

DB_PATH = 'plymouth_research.db'
MATCHES_CSV = 'business_rates_matches_confident.csv'


def add_schema():
    """Add business rates columns to database."""
    print("Adding business rates schema to database...")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Read and execute schema file
    with open('add_business_rates_schema.sql', 'r') as f:
        schema_sql = f.read()

    # Execute each statement separately
    for statement in schema_sql.split(';'):
        statement = statement.strip()
        if statement and not statement.startswith('--'):
            try:
                cursor.execute(statement)
            except sqlite3.OperationalError as e:
                if 'duplicate column name' in str(e).lower():
                    print(f"  ⚠ Column already exists (skipping): {statement[:50]}...")
                else:
                    raise

    conn.commit()
    conn.close()
    print("  ✓ Schema added")


def import_matches():
    """Import matched business rates data."""
    print("\nImporting business rates matches...")

    # Load matches
    df = pd.read_csv(MATCHES_CSV)
    print(f"  Found {len(df)} matched restaurants")

    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get current timestamp
    matched_at = datetime.utcnow().isoformat()

    # Update each restaurant
    updated_count = 0
    for _, row in df.iterrows():
        cursor.execute("""
            UPDATE restaurants
            SET
                business_rates_propref = ?,
                business_rates_account_holder = ?,
                business_rates_address = ?,
                business_rates_postcode = ?,
                business_rates_rateable_value = ?,
                business_rates_net_charge = ?,
                business_rates_category = ?,
                business_rates_vo_description = ?,
                business_rates_match_score = ?,
                business_rates_match_reason = ?,
                business_rates_matched_at = ?
            WHERE restaurant_id = ?
        """, (
            row['rates_propref'],
            row['rates_account_holder'],
            row['rates_address'],
            row['rates_postcode'],
            int(row['rates_rateable_value']) if pd.notna(row['rates_rateable_value']) else None,
            float(row['rates_net_charge']) if pd.notna(row['rates_net_charge']) else None,
            row['rates_category'],
            row['rates_vo_description'],
            float(row['match_score']) if pd.notna(row['match_score']) else None,
            row['match_reason'],
            matched_at,
            int(row['restaurant_id'])
        ))

        if cursor.rowcount > 0:
            updated_count += 1

    conn.commit()
    conn.close()

    print(f"  ✓ Updated {updated_count} restaurants")


def verify_import():
    """Verify the import was successful."""
    print("\nVerifying import...")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Count restaurants with business rates
    cursor.execute("""
        SELECT COUNT(*) FROM restaurants
        WHERE business_rates_propref IS NOT NULL
    """)
    count = cursor.fetchone()[0]

    # Get statistics
    cursor.execute("""
        SELECT
            COUNT(*) as total,
            AVG(business_rates_rateable_value) as avg_rv,
            MIN(business_rates_rateable_value) as min_rv,
            MAX(business_rates_rateable_value) as max_rv,
            AVG(business_rates_net_charge) as avg_charge,
            MIN(business_rates_net_charge) as min_charge,
            MAX(business_rates_net_charge) as max_charge
        FROM restaurants
        WHERE business_rates_propref IS NOT NULL
    """)
    stats = cursor.fetchone()

    conn.close()

    print(f"  Restaurants with business rates: {count}")
    print(f"  Rateable Value - Avg: £{stats[1]:,.0f}, Min: £{stats[2]:,.0f}, Max: £{stats[3]:,.0f}")
    print(f"  Annual Charge - Avg: £{stats[4]:,.0f}, Min: £{stats[5]:,.0f}, Max: £{stats[6]:,.0f}")


def main():
    """Main execution."""
    print("=" * 80)
    print("BUSINESS RATES DATA IMPORT")
    print("=" * 80)
    print()

    try:
        # Add schema
        add_schema()

        # Import data
        import_matches()

        # Verify
        verify_import()

        print("\n" + "=" * 80)
        print("✓ Business rates data imported successfully!")
        print("=" * 80)
        print("\nNext steps:")
        print("  1. Restart dashboard: streamlit run dashboard_app.py")
        print("  2. View business rates in restaurant profiles")
        print("  3. Use filters and analysis features")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
