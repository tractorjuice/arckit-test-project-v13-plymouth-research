#!/usr/bin/env python3
"""
Import Companies House Data to Database
========================================

Imports Companies House company data from CSV into the database.

Author: Plymouth Research Team
Date: 2025-11-19
"""

import sqlite3
import csv
from pathlib import Path
from datetime import datetime
import argparse


def create_companies_house_columns(cursor):
    """Add Companies House columns to restaurants table if they don't exist."""

    # Check if columns already exist
    cursor.execute("PRAGMA table_info(restaurants)")
    existing_columns = {row[1] for row in cursor.fetchall()}

    new_columns = [
        ("company_number", "TEXT"),
        ("company_name", "TEXT"),
        ("company_status", "TEXT"),
        ("company_type", "TEXT"),
        ("incorporation_date", "TEXT"),
        ("company_registered_address", "TEXT"),
        ("company_sic_codes", "TEXT"),
        ("company_match_confidence", "REAL"),
        ("company_match_reason", "TEXT"),
        ("companies_house_fetched_at", "TEXT")
    ]

    columns_added = []
    for col_name, col_type in new_columns:
        if col_name not in existing_columns:
            cursor.execute(f"ALTER TABLE restaurants ADD COLUMN {col_name} {col_type}")
            columns_added.append(col_name)

    return columns_added


def import_companies_from_csv(cursor, csv_path: Path, dry_run: bool = False):
    """Import company data from CSV file."""

    if not csv_path.exists():
        print(f"❌ CSV file not found: {csv_path}")
        return 0

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"📄 Found {len(rows)} companies in CSV")
    print()

    updated_count = 0
    skipped_count = 0

    for row in rows:
        restaurant_id = int(row['restaurant_id'])
        restaurant_name = row['restaurant_name']
        company_number = row['company_number']
        company_name = row['company_name']
        confidence = float(row['confidence'])

        # Check if restaurant exists
        cursor.execute("SELECT name FROM restaurants WHERE restaurant_id = ?", (restaurant_id,))
        result = cursor.fetchone()

        if not result:
            print(f"⚠️  Restaurant ID {restaurant_id} not found in database, skipping")
            skipped_count += 1
            continue

        if dry_run:
            print(f"[DRY RUN] Would update: {restaurant_name}")
            print(f"          Company: {company_name} ({company_number})")
            print(f"          Status: {row['company_status']}, Confidence: {confidence:.1f}%")
            print()
            updated_count += 1
        else:
            # Update restaurant with company data
            cursor.execute("""
                UPDATE restaurants
                SET
                    company_number = ?,
                    company_name = ?,
                    company_status = ?,
                    company_type = ?,
                    incorporation_date = ?,
                    company_registered_address = ?,
                    company_sic_codes = ?,
                    company_match_confidence = ?,
                    company_match_reason = ?,
                    companies_house_fetched_at = ?
                WHERE restaurant_id = ?
            """, (
                company_number,
                company_name,
                row['company_status'],
                row['company_type'],
                row['incorporation_date'],
                row['registered_address'],
                row['sic_codes'],
                confidence,
                row['match_reason'],
                datetime.now().isoformat(),
                restaurant_id
            ))

            print(f"✅ Updated: {restaurant_name}")
            print(f"   Company: {company_name} ({company_number})")
            print(f"   Status: {row['company_status']}, Confidence: {confidence:.1f}%")
            print()
            updated_count += 1

    return updated_count


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description='Import Companies House data to database')
    parser.add_argument('--file', type=str, default='companies_high_confidence.csv',
                        help='CSV file to import (default: companies_high_confidence.csv)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be imported without actually updating database')
    parser.add_argument('--include-dissolved', action='store_true',
                        help='Include dissolved companies (default: skip them)')

    args = parser.parse_args()

    print("=" * 70)
    print("Import Companies House Data to Database")
    print("=" * 70)
    print()

    if args.dry_run:
        print("🔍 DRY RUN MODE - No changes will be made to the database")
        print()

    # Connect to database
    db_path = Path(__file__).parent / "plymouth_research.db"
    if not db_path.exists():
        print(f"❌ Database not found: {db_path}")
        return

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    # Create Companies House columns if they don't exist
    print("📊 Checking database schema...")
    columns_added = create_companies_house_columns(cursor)

    if columns_added:
        print(f"✅ Added {len(columns_added)} new columns to restaurants table:")
        for col in columns_added:
            print(f"   • {col}")
    else:
        print("✅ All columns already exist")
    print()

    # Import data from CSV
    csv_path = Path(__file__).parent / args.file

    if not args.include_dissolved:
        print("⚠️  Filtering out dissolved companies...")
        print("   (Use --include-dissolved to include them)")
        print()

        # Filter CSV to exclude dissolved companies
        temp_path = Path(__file__).parent / "temp_filtered.csv"
        with open(csv_path, 'r', encoding='utf-8') as f_in:
            reader = csv.DictReader(f_in)
            rows = [row for row in reader if row['company_status'] != 'dissolved']

            with open(temp_path, 'w', newline='', encoding='utf-8') as f_out:
                if rows:
                    writer = csv.DictWriter(f_out, fieldnames=reader.fieldnames)
                    writer.writeheader()
                    writer.writerows(rows)

        print(f"📄 Filtered: {len(rows)} active companies (excluded dissolved)")
        print()
        csv_path = temp_path

    updated_count = import_companies_from_csv(cursor, csv_path, dry_run=args.dry_run)

    if not args.dry_run:
        conn.commit()
        print("=" * 70)
        print("✅ Import Complete!")
        print("=" * 70)
        print()
        print(f"📊 Updated {updated_count} restaurants with Companies House data")
        print()

        # Show statistics
        cursor.execute("""
            SELECT
                COUNT(*) as total,
                COUNT(company_number) as with_company,
                COUNT(CASE WHEN company_status = 'active' THEN 1 END) as active,
                COUNT(CASE WHEN company_status = 'dissolved' THEN 1 END) as dissolved
            FROM restaurants
            WHERE is_active = 1
        """)

        total, with_company, active, dissolved = cursor.fetchone()

        print("📈 Database Statistics:")
        print(f"   • Total active restaurants: {total}")
        print(f"   • With Companies House data: {with_company} ({with_company/total*100:.1f}%)")
        print(f"   • Active companies: {active}")
        print(f"   • Dissolved companies: {dissolved}")
        print()

        # Show company type distribution
        cursor.execute("""
            SELECT company_type, COUNT(*) as count
            FROM restaurants
            WHERE company_number IS NOT NULL
            GROUP BY company_type
            ORDER BY count DESC
        """)

        print("📊 Company Type Distribution:")
        for company_type, count in cursor.fetchall():
            if company_type:
                print(f"   • {company_type}: {count}")
        print()

        # Show average incorporation date
        cursor.execute("""
            SELECT
                AVG(CAST(strftime('%Y', incorporation_date) AS INTEGER)) as avg_year,
                MIN(incorporation_date) as oldest,
                MAX(incorporation_date) as newest
            FROM restaurants
            WHERE incorporation_date IS NOT NULL
        """)

        avg_year, oldest, newest = cursor.fetchone()
        if avg_year:
            current_year = datetime.now().year
            avg_age = current_year - int(avg_year)
            print("📅 Business Age Statistics:")
            print(f"   • Average incorporation year: {int(avg_year)} ({avg_age} years ago)")
            print(f"   • Oldest company: {oldest}")
            print(f"   • Newest company: {newest}")
            print()
    else:
        print("=" * 70)
        print("🔍 DRY RUN Complete!")
        print("=" * 70)
        print()
        print(f"📊 Would update {updated_count} restaurants")
        print()
        print("To actually import the data, run without --dry-run:")
        print(f"   python import_companies_house_data.py --file {args.file}")
        print()

    # Cleanup temp file
    temp_path = Path(__file__).parent / "temp_filtered.csv"
    if temp_path.exists():
        temp_path.unlink()

    conn.close()


if __name__ == "__main__":
    main()
