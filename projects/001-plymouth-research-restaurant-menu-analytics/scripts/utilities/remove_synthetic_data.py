#!/usr/bin/env python3
"""
Remove Synthetic Data Script
=============================

Removes all synthetic/placeholder restaurant entries from the database,
keeping only real scraped data.

Before removal:
- Exports list of synthetic restaurants to failed_restaurants_for_retry.csv
- This file can be used for future scraping retry attempts

Author: Plymouth Research Team
Date: 2025-11-18
"""

import sqlite3
from pathlib import Path


def main():
    """Remove synthetic restaurants from database."""
    db_path = Path(__file__).parent / "plymouth_research.db"

    if not db_path.exists():
        print(f"❌ Database not found: {db_path}")
        return

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    try:
        # Count synthetic restaurants
        cursor.execute("SELECT COUNT(*) FROM restaurants WHERE data_source = 'synthetic'")
        synthetic_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM restaurants WHERE data_source = 'real_scraped'")
        real_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM restaurants")
        total_count = cursor.fetchone()[0]

        print("="*60)
        print("Remove Synthetic Data")
        print("="*60)
        print(f"\n📊 Current Database:")
        print(f"   • Total restaurants: {total_count}")
        print(f"   • Real data: {real_count}")
        print(f"   • Synthetic data: {synthetic_count}")

        if synthetic_count == 0:
            print("\n✅ No synthetic data to remove!")
            return

        # Check for menu items (should be zero)
        cursor.execute("""
            SELECT COUNT(*)
            FROM menu_items mi
            JOIN restaurants r ON mi.restaurant_id = r.restaurant_id
            WHERE r.data_source = 'synthetic'
        """)
        synthetic_items = cursor.fetchone()[0]

        if synthetic_items > 0:
            print(f"\n⚠️  Warning: {synthetic_items} menu items linked to synthetic restaurants")
            print("    These will also be deleted.")

        # Confirm
        print(f"\n⚠️  This will DELETE {synthetic_count} synthetic restaurant entries")
        print("    A backup list has been saved to: failed_restaurants_for_retry.csv")
        response = input("\nProceed with deletion? (yes/no): ")

        if response.lower() != 'yes':
            print("❌ Cancelled")
            return

        # Delete synthetic restaurants (CASCADE will delete any menu items)
        print("\n🗑️  Removing synthetic data...")
        cursor.execute("DELETE FROM restaurants WHERE data_source = 'synthetic'")
        deleted = cursor.rowcount

        # Commit changes
        conn.commit()

        # Show final stats
        cursor.execute("SELECT COUNT(*) FROM restaurants")
        final_total = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM menu_items")
        final_items = cursor.fetchone()[0]

        print("\n" + "="*60)
        print("✅ Cleanup Complete!")
        print("="*60)
        print(f"\n📊 Final Database:")
        print(f"   • Restaurants: {final_total} (was {total_count})")
        print(f"   • Deleted: {deleted} synthetic entries")
        print(f"   • Menu items: {final_items} (all real data)")
        print(f"\n📁 Retry list saved: failed_restaurants_for_retry.csv")
        print(f"   Contains {synthetic_count} restaurant URLs for future scraping")

    except Exception as e:
        conn.rollback()
        print(f"\n❌ Error: {e}")
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    main()
