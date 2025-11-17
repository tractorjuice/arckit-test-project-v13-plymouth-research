#!/usr/bin/env python3
"""
Add Nice Slice Cheesecake to Honky Tonk Wine Library Menu
==========================================================

Add the missing cheesecake dessert item to Honky Tonk Wine Library.

Author: Plymouth Research Team
Date: 2025-11-17
"""

import sys
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from database.connection import Database

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


NEW_MENU_ITEM = {
    'name': 'Nice Slice Cheesecake',
    'description': 'Creamy cheesecake with fruit compote',
    'price_gbp': 7.50,
    'category': 'Desserts',
    'dietary_tags': ['vegetarian']
}


def main():
    """Add Nice Slice Cheesecake to Honky Tonk menu."""
    print("\n" + "🍰 "*40)
    print("  ADDING NICE SLICE CHEESECAKE TO HONKY TONK")
    print("🍰 "*40)

    try:
        # Initialize database
        db = Database("plymouth_research.db")
        db.connect()

        # Find Honky Tonk Wine Library
        all_data = db.get_all_data()
        honky_tonk = None

        for restaurant in all_data['restaurants']:
            if restaurant['name'] == 'Honky Tonk Wine Library':
                honky_tonk = restaurant
                break

        if not honky_tonk:
            logger.error("❌ Honky Tonk Wine Library not found in database")
            return 1

        print(f"\n📍 Restaurant: {honky_tonk['name']}")
        print(f"   Restaurant ID: {honky_tonk['restaurant_id']}")

        # Add the missing cheesecake item
        print(f"\n🍰 Adding: {NEW_MENU_ITEM['name']}")
        print(f"   Description: {NEW_MENU_ITEM['description']}")
        print(f"   Price: £{NEW_MENU_ITEM['price_gbp']:.2f}")
        print(f"   Category: {NEW_MENU_ITEM['category']}")

        inserted_count = db.insert_menu_items(honky_tonk['restaurant_id'], [NEW_MENU_ITEM])

        if inserted_count > 0:
            print(f"✅ Successfully added Nice Slice Cheesecake!")
        else:
            logger.error("❌ Failed to add menu item")
            return 1

        # Get updated statistics
        all_data = db.get_all_data()
        honky_tonk_items = [
            item for item in all_data['menu_items']
            if item['restaurant_name'] == 'Honky Tonk Wine Library'
        ]

        print("\n" + "="*80)
        print("📊 HONKY TONK WINE LIBRARY UPDATED")
        print("="*80)
        print(f"\nTotal Menu Items: {len(honky_tonk_items)}")

        # Show desserts
        desserts = [item for item in honky_tonk_items if item['category'] == 'Desserts']
        print(f"\n🍰 Desserts ({len(desserts)} items):")
        for dessert in desserts:
            print(f"   • {dessert['name']} - £{dessert['price_gbp']:.2f}")

        # Close database
        db.close()

        print(f"\n✅ Menu item successfully added!")
        print(f"\n🚀 Next Steps:")
        print(f"   1. Refresh dashboard to see Nice Slice Cheesecake")
        print(f"   2. Verify it appears in Honky Tonk's desserts section")

        return 0

    except Exception as e:
        logger.exception(f"❌ Failed to add cheesecake: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
