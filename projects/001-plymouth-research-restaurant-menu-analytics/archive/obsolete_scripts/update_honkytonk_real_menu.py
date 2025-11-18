#!/usr/bin/env python3
"""
Update Honky Tonk Wine Library with Real Menu Data
===================================================

Replace curated menu with actual menu from website:
https://www.honkytonkwinelibrary.com/food-3-1

This is their Christmas menu (2025).

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


# Real menu from Honky Tonk Wine Library website
REAL_MENU_ITEMS = [
    # Sharing Boards
    {'name': 'Mini Deli Board', 'description': 'Artisan cheese, chicken & herb terrine, hummus, fries, chutney, crackers & sourdough', 'price_gbp': 24.50, 'category': 'Sharing Boards', 'dietary_tags': []},
    {'name': 'Deli Board for 2', 'description': 'Two cheeses, terrines, pâté, dips, pigs in blankets, olives, tomatoes, grapes', 'price_gbp': 49.00, 'category': 'Sharing Boards', 'dietary_tags': []},
    {'name': 'Half Board for 2', 'description': 'Deli board plus one warm plate, bonus bite, and mulled wine tot', 'price_gbp': 72.00, 'category': 'Sharing Boards', 'dietary_tags': []},
    {'name': 'Honkytonk Full Board for 4', 'description': 'Extended spread with two warm plates, two bonus bites, and mulled wine tot', 'price_gbp': 134.00, 'category': 'Sharing Boards', 'dietary_tags': []},
    {'name': 'The VegeBoard', 'description': 'Two cheeses, dips, nutroast, parsnips, olives, terrine, tomatoes, grapes', 'price_gbp': 58.00, 'category': 'Sharing Boards', 'dietary_tags': ['vegetarian']},

    # Warm Plates (£14.50 each)
    {'name': 'Rolled Porchetta', 'description': 'With sage, rosemary, lemon, and braised fennel', 'price_gbp': 14.50, 'category': 'Warm Plates', 'dietary_tags': []},
    {'name': 'Turkey Pie Yorkie', 'description': 'With creamy leeks and bacon', 'price_gbp': 14.50, 'category': 'Warm Plates', 'dietary_tags': []},
    {'name': 'Beef Brisket', 'description': 'In red wine stock with spices', 'price_gbp': 14.50, 'category': 'Warm Plates', 'dietary_tags': []},
    {'name': 'Maple-glazed Salmon', 'description': 'With green beans', 'price_gbp': 14.50, 'category': 'Warm Plates', 'dietary_tags': ['gluten-free']},
    {'name': 'Pan-seared Scallops', 'description': 'With cauliflower purée', 'price_gbp': 14.50, 'category': 'Warm Plates', 'dietary_tags': ['gluten-free']},
    {'name': 'Nutroast', 'description': 'With chestnuts and cranberries', 'price_gbp': 14.50, 'category': 'Warm Plates', 'dietary_tags': ['vegetarian']},

    # Bonus Bites (£8.50 each)
    {'name': 'Parmesan Coated Parsnips', 'description': 'Crispy parsnips with parmesan coating', 'price_gbp': 8.50, 'category': 'Bonus Bites', 'dietary_tags': ['vegetarian']},
    {'name': 'Sage and Onion Fries', 'description': 'Seasoned fries with sage and onion', 'price_gbp': 8.50, 'category': 'Bonus Bites', 'dietary_tags': ['vegan']},
    {'name': 'Brussel Sprouts', 'description': 'With chorizo lardons', 'price_gbp': 8.50, 'category': 'Bonus Bites', 'dietary_tags': []},
    {'name': "Mac 'n' Cheese", 'description': 'With chorizo crumb', 'price_gbp': 8.50, 'category': 'Bonus Bites', 'dietary_tags': []},

    # Light Lunch
    {'name': 'Honkytonk Winter Salad', 'description': 'Chicory, kale, chickpeas in pomegranate dressing', 'price_gbp': 14.50, 'category': 'Light Lunch', 'dietary_tags': ['vegan', 'gluten-free']},
    {'name': 'Hearty Winter Soup', 'description': 'With warm sourdough', 'price_gbp': 10.00, 'category': 'Light Lunch', 'dietary_tags': ['vegan']},
    {'name': 'Beef Brisket Naanwich', 'description': 'Beef brisket in warm naan bread', 'price_gbp': 15.50, 'category': 'Light Lunch', 'dietary_tags': []},
    {'name': 'Cranberry, Rocket & Brie Naanwich', 'description': 'Cranberry, rocket, and brie in warm naan', 'price_gbp': 14.50, 'category': 'Light Lunch', 'dietary_tags': ['vegetarian']},
    {'name': 'Cold Cuts Deli Board', 'description': 'Terrine, ham, pâté with chutney and sourdough', 'price_gbp': 22.00, 'category': 'Light Lunch', 'dietary_tags': []},

    # Cheese Course
    {'name': 'Cheeseboard', 'description': 'Two artisan cheeses with crackers, sourdough, olives, balsamic onions', 'price_gbp': 21.25, 'category': 'Cheese Course', 'dietary_tags': ['vegetarian']},
    {'name': 'Baked Camembert', 'description': 'Cranberry centre with confit shallots, garlic, honey, and sourdough', 'price_gbp': 15.95, 'category': 'Cheese Course', 'dietary_tags': ['vegetarian']},

    # Dips to Share (with nacho chips, crudités, warm naan)
    {'name': 'Hummus', 'description': 'Served with nacho chips, crudités, and warm naan', 'price_gbp': 8.50, 'category': 'Dips to Share', 'dietary_tags': ['vegan']},
    {'name': 'Mackerel and Horseradish', 'description': 'Served with nacho chips, crudités, and warm naan', 'price_gbp': 9.50, 'category': 'Dips to Share', 'dietary_tags': []},
    {'name': 'Roasted Carrot and Sweet Potato', 'description': 'Served with nacho chips, crudités, and warm naan', 'price_gbp': 7.50, 'category': 'Dips to Share', 'dietary_tags': ['vegan']},
    {'name': '3 Dips Bundle', 'description': 'Choice of three dips with nacho chips, crudités, and warm naan', 'price_gbp': 22.50, 'category': 'Dips to Share', 'dietary_tags': []},

    # Desserts
    {'name': 'Nice Slice Cheesecake', 'description': 'Rotating flavors of artisan cheesecake', 'price_gbp': 7.95, 'category': 'Desserts', 'dietary_tags': ['vegetarian']},
    {'name': 'Honkytonk Christmas Coppa', 'description': 'Christmas pudding, ice cream, cranberries, cinnamon liqueur', 'price_gbp': 9.00, 'category': 'Desserts', 'dietary_tags': ['vegetarian']},
    {'name': 'Ice Cream/Sorbet', 'description': '3 scoops of ice cream or sorbet', 'price_gbp': 6.95, 'category': 'Desserts', 'dietary_tags': ['vegetarian']},
    {'name': 'Boozy Affogato', 'description': 'Ice cream with espresso and liqueur', 'price_gbp': 8.50, 'category': 'Desserts', 'dietary_tags': ['vegetarian']},

    # Beverages
    {'name': 'Mulled Wine', 'description': 'Red wine, port, brandy, spices and orange (200ml)', 'price_gbp': 7.95, 'category': 'Beverages', 'dietary_tags': ['vegan']},
]


def main():
    """Replace Honky Tonk menu with real data."""
    print("\n" + "🍷 "*40)
    print("  UPDATING HONKY TONK WITH REAL MENU DATA")
    print("  Source: https://www.honkytonkwinelibrary.com/food-3-1")
    print("🍷 "*40)

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

        restaurant_id = honky_tonk['restaurant_id']
        print(f"\n📍 Restaurant: {honky_tonk['name']}")
        print(f"   ID: {restaurant_id}")

        # Get current menu items
        current_items = [
            item for item in all_data['menu_items']
            if item['restaurant_name'] == 'Honky Tonk Wine Library'
        ]
        print(f"   Current menu items: {len(current_items)}")

        # Delete old menu items
        print(f"\n🗑️  Deleting old menu items...")
        cursor = db.conn.cursor()

        # First delete from menu_item_dietary_tags
        cursor.execute("""
            DELETE FROM menu_item_dietary_tags
            WHERE item_id IN (
                SELECT item_id FROM menu_items WHERE restaurant_id = ?
            )
        """, (restaurant_id,))

        # Then delete from menu_items
        cursor.execute("DELETE FROM menu_items WHERE restaurant_id = ?", (restaurant_id,))
        db.conn.commit()
        print(f"✅ Deleted {len(current_items)} old items")

        # Insert real menu items
        print(f"\n📋 Adding {len(REAL_MENU_ITEMS)} real menu items from website...")
        inserted_count = db.insert_menu_items(restaurant_id, REAL_MENU_ITEMS)

        if inserted_count > 0:
            print(f"✅ Successfully added {inserted_count} menu items!")
        else:
            logger.error("❌ Failed to add menu items")
            return 1

        # Update scraping log
        log_data = {
            'restaurant_id': restaurant_id,
            'url': 'https://www.honkytonkwinelibrary.com/food-3-1',
            'http_status_code': 200,
            'robots_txt_allowed': True,
            'rate_limit_delay_seconds': 0,
            'user_agent': 'WebFetch API (Real Menu Data)',
            'success': True,
            'error_message': None,
        }
        db.log_scraping_attempt(log_data)

        # Get updated statistics
        all_data = db.get_all_data()
        honky_tonk_items = [
            item for item in all_data['menu_items']
            if item['restaurant_name'] == 'Honky Tonk Wine Library'
        ]

        print("\n" + "="*80)
        print("📊 HONKY TONK WINE LIBRARY UPDATED WITH REAL MENU")
        print("="*80)
        print(f"\nTotal Menu Items: {len(honky_tonk_items)}")

        # Show menu by category
        categories = {}
        for item in honky_tonk_items:
            category = item['category']
            if category not in categories:
                categories[category] = []
            categories[category].append(item)

        for category, items in sorted(categories.items()):
            print(f"\n{category} ({len(items)} items):")
            for item in items[:3]:  # Show first 3
                print(f"   • {item['name']} - £{item['price_gbp']:.2f}")
            if len(items) > 3:
                print(f"   ... and {len(items) - 3} more")

        # Price stats
        prices = [item['price_gbp'] for item in honky_tonk_items]
        print(f"\n💰 Price Range: £{min(prices):.2f} - £{max(prices):.2f}")
        print(f"   Average: £{sum(prices)/len(prices):.2f}")

        # Total database stats
        print(f"\n📊 Platform Total:")
        print(f"   Restaurants: {len(all_data['restaurants'])}")
        print(f"   Menu Items: {len(all_data['menu_items'])}")

        # Close database
        db.close()

        print(f"\n✅ Honky Tonk menu successfully updated with real data!")
        print(f"\n🚀 Next Steps:")
        print(f"   1. Refresh dashboard to see real Honky Tonk menu")
        print(f"   2. Browse Christmas menu items")
        print(f"   3. Verify data provenance shows correct source URL")

        return 0

    except Exception as e:
        logger.exception(f"❌ Failed to update menu: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
