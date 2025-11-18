#!/usr/bin/env python3
"""
Calculate Price Ranges Script
==============================

Calculates price_range for all restaurants based on their actual menu item prices.
Updates the restaurants table with formatted price ranges like "£5-15".

Author: Plymouth Research Team
Date: 2025-11-18
"""

import sqlite3
from pathlib import Path


def format_price_range(min_price: float, max_price: float) -> str:
    """Format price range as £X-Y."""
    # Round to nearest pound for cleaner display
    min_rounded = int(min_price) if min_price == int(min_price) else round(min_price, 2)
    max_rounded = int(max_price) if max_price == int(max_price) else round(max_price, 2)

    # Format without decimals if whole numbers
    if min_rounded == int(min_rounded) and max_rounded == int(max_rounded):
        return f"£{int(min_rounded)}-{int(max_rounded)}"
    else:
        return f"£{min_rounded:.2f}-{max_rounded:.2f}"


def calculate_price_ranges(db_path: Path):
    """Calculate and update price ranges for all restaurants."""
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    try:
        # Get all restaurants
        cursor.execute("SELECT restaurant_id, name FROM restaurants")
        restaurants = cursor.fetchall()

        print("=" * 60)
        print("Calculate Price Ranges from Menu Items")
        print("=" * 60)
        print(f"\nProcessing {len(restaurants)} restaurants...\n")

        updated = 0
        no_items = 0

        for restaurant_id, name in restaurants:
            # Get min/max prices for this restaurant
            cursor.execute("""
                SELECT MIN(price_gbp), MAX(price_gbp)
                FROM menu_items
                WHERE restaurant_id = ?
                AND price_gbp IS NOT NULL
                AND price_gbp > 0
            """, (restaurant_id,))

            result = cursor.fetchone()
            min_price, max_price = result if result else (None, None)

            if min_price and max_price:
                # Calculate price range
                price_range = format_price_range(min_price, max_price)

                # Update restaurant
                cursor.execute("""
                    UPDATE restaurants
                    SET price_range = ?
                    WHERE restaurant_id = ?
                """, (price_range, restaurant_id))

                updated += 1
                print(f"✓ {name}: {price_range}")
            else:
                no_items += 1
                print(f"⚠ {name}: No menu items with prices")

        # Commit changes
        conn.commit()

        print("\n" + "=" * 60)
        print("✅ Price Range Calculation Complete!")
        print("=" * 60)
        print(f"\n📊 Results:")
        print(f"   • Updated: {updated} restaurants")
        print(f"   • No prices: {no_items} restaurants")
        print(f"   • Total: {len(restaurants)} restaurants")

        # Show some examples
        print("\n📋 Sample Price Ranges:")
        cursor.execute("""
            SELECT name, price_range
            FROM restaurants
            WHERE price_range != '' AND price_range IS NOT NULL
            ORDER BY RANDOM()
            LIMIT 10
        """)

        for name, price_range in cursor.fetchall():
            print(f"   • {name}: {price_range}")

    except Exception as e:
        conn.rollback()
        print(f"\n❌ Error: {e}")
        raise

    finally:
        conn.close()


def main():
    """Main entry point."""
    db_path = Path(__file__).parent / "plymouth_research.db"

    if not db_path.exists():
        print(f"❌ Database not found: {db_path}")
        return

    calculate_price_ranges(db_path)


if __name__ == "__main__":
    main()
