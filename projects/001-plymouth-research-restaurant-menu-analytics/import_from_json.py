#!/usr/bin/env python3
"""
Import Restaurants from JSON
============================

Simple importer that reads restaurant data from JSON files.

Usage:
    python import_from_json.py restaurants_batch_chains.json

Author: Plymouth Research Team
Date: 2025-11-17
"""

import sys
import json
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


def import_from_json(json_file: str):
    """Import restaurants from JSON file."""
    print(f"\n📥 Importing from: {json_file}")

    # Load JSON
    with open(json_file, 'r') as f:
        restaurants_data = json.load(f)

    print(f"   Found {len(restaurants_data)} restaurants in file")

    # Connect to database
    db = Database("plymouth_research.db")
    db.connect()

    total_added = 0
    total_items = 0

    for restaurant_data in restaurants_data:
        restaurant_info = restaurant_data['restaurant']
        menu_items = restaurant_data['menu_items']

        print(f"\n➕ Adding: {restaurant_info['name']}")
        print(f"   Items: {len(menu_items)}")

        # Insert restaurant
        restaurant_id = db.insert_restaurant(restaurant_info)

        if not restaurant_id:
            logger.error(f"Failed to insert {restaurant_info['name']}")
            continue

        # Insert menu items
        inserted = db.insert_menu_items(restaurant_id, menu_items)

        # Log scraping attempt
        db.log_scraping_attempt({
            'restaurant_id': restaurant_id,
            'url': restaurant_info['website_url'],
            'http_status_code': 200,
            'robots_txt_allowed': True,
            'rate_limit_delay_seconds': 0,
            'user_agent': 'JSON Import (Chain Menus & Research Data)',
            'success': True,
            'error_message': None,
        })

        total_added += 1
        total_items += inserted

        print(f"   ✅ Added {inserted} menu items")

    # Get final stats
    all_data = db.get_all_data()

    print("\n" + "="*80)
    print("✅ IMPORT COMPLETED")
    print("="*80)
    print(f"\nRestaurants Added: {total_added}")
    print(f"Menu Items Added: {total_items}")
    print(f"\nNew Totals:")
    print(f"   Restaurants: {len(all_data['restaurants'])}")
    print(f"   Menu Items: {len(all_data['menu_items'])}")

    db.close()


def main():
    if len(sys.argv) < 2:
        print("Usage: python import_from_json.py <json_file>")
        return 1

    json_file = sys.argv[1]

    if not Path(json_file).exists():
        print(f"Error: File not found: {json_file}")
        return 1

    import_from_json(json_file)
    return 0


if __name__ == "__main__":
    sys.exit(main())
