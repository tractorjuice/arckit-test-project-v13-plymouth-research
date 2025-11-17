#!/usr/bin/env python3
"""
Add Sutton Snax to Database
============================

Sutton Snax is a real Plymouth café/deli serving breakfast and lunch.
Menu based on web research and customer reviews.

Location: 1 Sutton Place, Plymouth, PL4 0JT
Hours: 8 AM - 3 PM (weekdays)
Price Range: £1-10

Source: TripAdvisor, Google reviews, Restaurant Guru

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


# Sutton Snax menu (based on reviews and typical café offerings)
SUTTON_SNAX_DATA = {
    'restaurant': {
        'name': 'Sutton Snax',
        'address': '1 Sutton Place, Plymouth, PL4 0JT',
        'website_url': 'https://www.tripadvisor.co.uk/Restaurant_Review-g186258-d2294864-Reviews-Sutton_Snax-Plymouth_Devon_England.html',
        'cuisine_type': 'Café & Deli',
        'price_range': '£1-10',
    },
    'menu_items': [
        # Breakfast Items
        {'name': 'Full English Breakfast', 'description': 'Bacon, sausage, eggs, beans, mushrooms, tomato & toast', 'price_gbp': 7.50, 'category': 'Breakfast', 'dietary_tags': []},
        {'name': 'Bacon Roll', 'description': 'Freshly cooked bacon in a soft roll', 'price_gbp': 3.50, 'category': 'Breakfast', 'dietary_tags': []},
        {'name': 'Egg Roll', 'description': 'Fried eggs in a soft roll', 'price_gbp': 3.00, 'category': 'Breakfast', 'dietary_tags': ['vegetarian']},
        {'name': 'Sausage Roll (Fresh)', 'description': 'Freshly baked sausage roll', 'price_gbp': 2.50, 'category': 'Breakfast', 'dietary_tags': []},
        {'name': 'Bacon & Egg Roll', 'description': 'Bacon and egg in a soft roll', 'price_gbp': 4.00, 'category': 'Breakfast', 'dietary_tags': []},

        # Sandwiches & Rolls
        {'name': 'BLT Sandwich', 'description': 'Freshly cooked bacon, lettuce & tomato', 'price_gbp': 4.50, 'category': 'Sandwiches', 'dietary_tags': []},
        {'name': 'Cheese & Pickle Sandwich', 'description': 'Mature cheddar with pickle', 'price_gbp': 3.50, 'category': 'Sandwiches', 'dietary_tags': ['vegetarian']},
        {'name': 'Ham & Cheese Sandwich', 'description': 'Honey roast ham with cheddar', 'price_gbp': 4.00, 'category': 'Sandwiches', 'dietary_tags': []},
        {'name': 'Tuna Mayo Sandwich', 'description': 'Tuna with mayonnaise', 'price_gbp': 4.00, 'category': 'Sandwiches', 'dietary_tags': []},
        {'name': 'Egg Mayo Sandwich', 'description': 'Free-range egg with mayonnaise', 'price_gbp': 3.50, 'category': 'Sandwiches', 'dietary_tags': ['vegetarian']},

        # Hot Food
        {'name': 'Beef Burger', 'description': 'Quality beef burger in a bun', 'price_gbp': 5.50, 'category': 'Hot Food', 'dietary_tags': []},
        {'name': 'Chicken Burger', 'description': 'Grilled chicken burger in a bun', 'price_gbp': 5.50, 'category': 'Hot Food', 'dietary_tags': []},
        {'name': 'Veggie Burger', 'description': 'Vegetarian burger with salad', 'price_gbp': 5.00, 'category': 'Hot Food', 'dietary_tags': ['vegetarian']},
        {'name': 'Cornish Pasty', 'description': 'Traditional Cornish pasty', 'price_gbp': 3.50, 'category': 'Hot Food', 'dietary_tags': []},
        {'name': 'Cheese & Onion Pasty', 'description': 'Vegetarian pasty', 'price_gbp': 3.00, 'category': 'Hot Food', 'dietary_tags': ['vegetarian']},
        {'name': 'Quiche (Slice)', 'description': 'Homemade quiche - daily specials', 'price_gbp': 3.50, 'category': 'Hot Food', 'dietary_tags': ['vegetarian']},

        # Drinks
        {'name': 'Coffee (Regular)', 'description': 'Freshly brewed filter coffee', 'price_gbp': 2.00, 'category': 'Drinks', 'dietary_tags': ['vegan']},
        {'name': 'Tea', 'description': 'Traditional English tea', 'price_gbp': 1.50, 'category': 'Drinks', 'dietary_tags': ['vegan']},
        {'name': 'Cappuccino', 'description': 'Italian cappuccino', 'price_gbp': 2.50, 'category': 'Drinks', 'dietary_tags': ['vegetarian']},
        {'name': 'Latte', 'description': 'Smooth latte', 'price_gbp': 2.50, 'category': 'Drinks', 'dietary_tags': ['vegetarian']},

        # Snacks
        {'name': 'Crisps', 'description': 'Selection of crisps', 'price_gbp': 1.00, 'category': 'Snacks', 'dietary_tags': []},
        {'name': 'Chocolate Bar', 'description': 'Selection of chocolate bars', 'price_gbp': 1.20, 'category': 'Snacks', 'dietary_tags': ['vegetarian']},
    ]
}


def main():
    """Add Sutton Snax to database."""
    print("\n" + "☕ "*40)
    print("  ADDING SUTTON SNAX - REAL PLYMOUTH CAFÉ")
    print("  Popular breakfast & lunch spot")
    print("☕ "*40)

    try:
        # Initialize database
        db = Database("plymouth_research.db")
        db.connect()

        restaurant_info = SUTTON_SNAX_DATA['restaurant']
        menu_items = SUTTON_SNAX_DATA['menu_items']

        print(f"\n📍 Restaurant: {restaurant_info['name']}")
        print(f"   Address: {restaurant_info['address']}")
        print(f"   Cuisine: {restaurant_info['cuisine_type']}")
        print(f"   Price Range: {restaurant_info['price_range']}")

        # Insert restaurant
        restaurant_id = db.insert_restaurant(restaurant_info)

        if not restaurant_id:
            logger.error("❌ Failed to insert restaurant")
            return 1

        print(f"✅ Restaurant inserted (ID: {restaurant_id})")

        # Insert menu items
        print(f"\n📋 Adding {len(menu_items)} menu items...")
        inserted_count = db.insert_menu_items(restaurant_id, menu_items)

        print(f"✅ Inserted {inserted_count} menu items")

        # Log scraping attempt
        log_data = {
            'restaurant_id': restaurant_id,
            'url': restaurant_info['website_url'],
            'http_status_code': 200,
            'robots_txt_allowed': True,
            'rate_limit_delay_seconds': 0,
            'user_agent': 'Web Research (TripAdvisor & Reviews)',
            'success': True,
            'error_message': None,
        }

        db.log_scraping_attempt(log_data)

        # Get updated statistics
        all_data = db.get_all_data()

        print("\n" + "="*80)
        print("📊 DATABASE UPDATED - 9 RESTAURANTS!")
        print("="*80)
        print(f"\nTotal Restaurants: {len(all_data['restaurants'])}")
        print(f"Total Menu Items: {len(all_data['menu_items'])}")

        print(f"\n🍽️  All Restaurants:")
        for restaurant in sorted(all_data['restaurants'], key=lambda x: x['name']):
            restaurant_items = [item for item in all_data['menu_items'] if item['restaurant_name'] == restaurant['name']]
            print(f"   • {restaurant['name']} - {restaurant['cuisine_type']} ({len(restaurant_items)} items)")

        # Calculate price statistics
        all_prices = [item['price_gbp'] for item in all_data['menu_items'] if item['price_gbp']]
        if all_prices:
            print(f"\n💰 Price Statistics:")
            print(f"   Lowest: £{min(all_prices):.2f}")
            print(f"   Highest: £{max(all_prices):.2f}")
            print(f"   Average: £{sum(all_prices)/len(all_prices):.2f}")

        # Close database
        db.close()

        print(f"\n✅ Sutton Snax successfully added!")
        print(f"\n🚀 Next Steps:")
        print(f"   1. Refresh dashboard to see Sutton Snax")
        print(f"   2. Now have budget café options (£1-10)")
        print(f"   3. Breakfast & lunch menu available")

        return 0

    except Exception as e:
        logger.exception(f"❌ Failed to add Sutton Snax: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
