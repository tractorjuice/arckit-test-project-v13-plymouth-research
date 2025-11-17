#!/usr/bin/env python3
"""
Add Multiple Plymouth Restaurants to Database
=============================================

Add 2 more restaurants to demonstrate scalability:
1. The Ocean Room - Fine dining seafood
2. Harbour Bistro - Casual European bistro

This brings total to 6 restaurants with diverse cuisines and price points.

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


RESTAURANTS_DATA = [
    # Restaurant 1: The Ocean Room (Fine Dining)
    {
        'restaurant': {
            'name': 'The Ocean Room',
            'address': 'Royal William Yard, Plymouth, PL1 3RP',
            'website_url': 'https://oceanroom-plymouth.co.uk',
            'cuisine_type': 'Fine Dining Seafood',
            'price_range': '£30-50',
        },
        'menu_items': [
            # Starters
            {'name': 'Oysters Rockefeller', 'description': '6 oysters with spinach, garlic butter', 'price_gbp': 16.50, 'category': 'Starters', 'dietary_tags': ['gluten-free']},
            {'name': 'Seared Scallops', 'description': 'Diver scallops with cauliflower puree', 'price_gbp': 18.95, 'category': 'Starters', 'dietary_tags': ['gluten-free']},
            {'name': 'Smoked Salmon Carpaccio', 'description': 'Thinly sliced salmon with lemon dressing', 'price_gbp': 14.50, 'category': 'Starters', 'dietary_tags': ['gluten-free', 'dairy-free']},
            {'name': 'Heritage Tomato Salad', 'description': 'Heirloom tomatoes with basil oil', 'price_gbp': 12.00, 'category': 'Starters', 'dietary_tags': ['vegan', 'gluten-free']},

            # Mains
            {'name': 'Lobster Thermidor', 'description': 'Whole lobster with cream sauce', 'price_gbp': 48.00, 'category': 'Mains', 'dietary_tags': ['gluten-free']},
            {'name': 'Dover Sole (Whole)', 'description': 'Grilled whole Dover sole with herb butter', 'price_gbp': 42.00, 'category': 'Mains', 'dietary_tags': ['gluten-free']},
            {'name': 'Sea Bass en Papillote', 'description': 'Baked sea bass with fennel and tomatoes', 'price_gbp': 36.00, 'category': 'Mains', 'dietary_tags': ['gluten-free', 'dairy-free']},
            {'name': 'Fillet of Beef Wellington', 'description': 'Prime beef fillet in puff pastry', 'price_gbp': 45.00, 'category': 'Mains', 'dietary_tags': []},
            {'name': 'Wild Mushroom Risotto', 'description': 'Arborio rice with seasonal mushrooms', 'price_gbp': 28.00, 'category': 'Mains', 'dietary_tags': ['vegetarian', 'gluten-free']},
            {'name': 'Truffle Gnocchi', 'description': 'Homemade gnocchi with black truffle', 'price_gbp': 32.00, 'category': 'Mains', 'dietary_tags': ['vegetarian']},

            # Sides
            {'name': 'Triple-Cooked Chips', 'description': 'Hand-cut triple-cooked chips', 'price_gbp': 5.50, 'category': 'Sides', 'dietary_tags': ['vegan', 'gluten-free']},
            {'name': 'Grilled Asparagus', 'description': 'British asparagus with lemon', 'price_gbp': 6.00, 'category': 'Sides', 'dietary_tags': ['vegan', 'gluten-free']},
            {'name': 'Creamed Spinach', 'description': 'Wilted spinach in cream', 'price_gbp': 5.00, 'category': 'Sides', 'dietary_tags': ['vegetarian', 'gluten-free']},

            # Desserts
            {'name': 'Lemon Posset', 'description': 'Light lemon dessert with shortbread', 'price_gbp': 9.50, 'category': 'Desserts', 'dietary_tags': ['vegetarian']},
            {'name': 'Dark Chocolate Mousse', 'description': '70% chocolate mousse with raspberry', 'price_gbp': 10.00, 'category': 'Desserts', 'dietary_tags': ['vegetarian', 'gluten-free']},
            {'name': 'Cheese Selection', 'description': '5 British cheeses with crackers', 'price_gbp': 14.00, 'category': 'Desserts', 'dietary_tags': ['vegetarian']},
        ]
    },

    # Restaurant 2: Harbour Bistro (Casual European)
    {
        'restaurant': {
            'name': 'Harbour Bistro',
            'address': 'Sutton Harbour, Plymouth, PL4 0DW',
            'website_url': 'https://harbourbistro-plymouth.co.uk',
            'cuisine_type': 'European Bistro',
            'price_range': '£12-25',
        },
        'menu_items': [
            # Starters
            {'name': 'French Onion Soup', 'description': 'Classic soup with gruyere crouton', 'price_gbp': 7.50, 'category': 'Starters', 'dietary_tags': ['vegetarian']},
            {'name': 'Chicken Liver Pâté', 'description': 'Smooth pâté with toasted brioche', 'price_gbp': 8.50, 'category': 'Starters', 'dietary_tags': []},
            {'name': 'Burrata & Tomatoes', 'description': 'Fresh burrata with heritage tomatoes', 'price_gbp': 9.50, 'category': 'Starters', 'dietary_tags': ['vegetarian', 'gluten-free']},
            {'name': 'Crispy Calamari', 'description': 'Lightly fried squid with aioli', 'price_gbp': 8.95, 'category': 'Starters', 'dietary_tags': []},

            # Mains
            {'name': 'Moules Marinière', 'description': 'Fresh mussels in white wine sauce', 'price_gbp': 16.50, 'category': 'Mains', 'dietary_tags': ['gluten-free']},
            {'name': 'Steak Frites', 'description': '8oz sirloin with frites and sauce', 'price_gbp': 24.00, 'category': 'Mains', 'dietary_tags': ['gluten-free']},
            {'name': 'Confit Duck Leg', 'description': 'Slow-cooked duck with dauphinoise', 'price_gbp': 22.50, 'category': 'Mains', 'dietary_tags': ['gluten-free']},
            {'name': 'Pan-Fried Sea Bream', 'description': 'Sea bream with ratatouille', 'price_gbp': 20.00, 'category': 'Mains', 'dietary_tags': ['gluten-free', 'dairy-free']},
            {'name': 'Vegetable Tart', 'description': 'Roasted vegetable tart with salad', 'price_gbp': 15.50, 'category': 'Mains', 'dietary_tags': ['vegetarian']},
            {'name': 'Coq au Vin', 'description': 'Chicken braised in red wine', 'price_gbp': 18.50, 'category': 'Mains', 'dietary_tags': ['gluten-free']},

            # Sides
            {'name': 'Frites', 'description': 'Thin-cut French fries', 'price_gbp': 4.00, 'category': 'Sides', 'dietary_tags': ['vegan', 'gluten-free']},
            {'name': 'Mixed Salad', 'description': 'Dressed mixed leaves', 'price_gbp': 3.50, 'category': 'Sides', 'dietary_tags': ['vegan', 'gluten-free']},
            {'name': 'Garlic Bread', 'description': 'Toasted baguette with garlic butter', 'price_gbp': 4.50, 'category': 'Sides', 'dietary_tags': ['vegetarian']},

            # Desserts
            {'name': 'Crème Caramel', 'description': 'Classic French custard', 'price_gbp': 6.50, 'category': 'Desserts', 'dietary_tags': ['vegetarian', 'gluten-free']},
            {'name': 'Tarte Tatin', 'description': 'Upside-down apple tart with cream', 'price_gbp': 7.50, 'category': 'Desserts', 'dietary_tags': ['vegetarian']},
            {'name': 'Chocolate Profiteroles', 'description': 'Choux pastry with chocolate sauce', 'price_gbp': 7.95, 'category': 'Desserts', 'dietary_tags': ['vegetarian']},
        ]
    },
]


def main():
    """Add multiple restaurants to database."""
    print("\n" + "🍽️ "*40)
    print("  ADDING MULTIPLE PLYMOUTH RESTAURANTS")
    print("  Scaling to 6 Total Restaurants")
    print("🍽️ "*40)

    try:
        # Initialize database
        db = Database("plymouth_research.db")
        db.connect()

        total_items = 0

        for i, restaurant_data in enumerate(RESTAURANTS_DATA, 1):
            restaurant_info = restaurant_data['restaurant']
            menu_items = restaurant_data['menu_items']

            print(f"\n{'─'*80}")
            print(f"Restaurant {i}/{len(RESTAURANTS_DATA)}")
            print(f"{'─'*80}")
            print(f"📍 {restaurant_info['name']}")
            print(f"   Address: {restaurant_info['address']}")
            print(f"   Cuisine: {restaurant_info['cuisine_type']}")
            print(f"   Price Range: {restaurant_info['price_range']}")

            # Insert restaurant
            restaurant_id = db.insert_restaurant(restaurant_info)

            if not restaurant_id:
                logger.error(f"❌ Failed to insert {restaurant_info['name']}")
                continue

            print(f"✅ Restaurant inserted (ID: {restaurant_id})")

            # Insert menu items
            inserted_count = db.insert_menu_items(restaurant_id, menu_items)
            total_items += inserted_count
            print(f"✅ Inserted {inserted_count} menu items")

            # Log scraping attempt
            log_data = {
                'restaurant_id': restaurant_id,
                'url': restaurant_info['website_url'],
                'http_status_code': 200,
                'robots_txt_allowed': True,
                'rate_limit_delay_seconds': 0,
                'user_agent': 'Manual Curation (Demonstration Data)',
                'success': True,
                'error_message': None,
            }

            db.log_scraping_attempt(log_data)

        # Get final statistics
        all_data = db.get_all_data()

        print("\n" + "="*80)
        print("📊 DATABASE FULLY UPDATED")
        print("="*80)
        print(f"\nTotal Restaurants: {len(all_data['restaurants'])}")
        print(f"Total Menu Items: {len(all_data['menu_items'])}")
        print(f"Menu Items Added: {total_items}")

        print(f"\n🍽️  All Restaurants:")
        for restaurant in sorted(all_data['restaurants'], key=lambda x: x['name']):
            # Count items for this restaurant
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

        print(f"\n✅ Successfully added {len(RESTAURANTS_DATA)} restaurants!")
        print(f"\n🚀 Next Steps:")
        print(f"   1. Refresh dashboard: streamlit run dashboard_app.py")
        print(f"   2. Compare 6 different restaurants across price ranges")
        print(f"   3. Test filtering by cuisine type (Seafood, Bistro, Fine Dining, etc.)")
        print(f"   4. Analyze price distribution across {len(all_data['menu_items'])} menu items")

        return 0

    except Exception as e:
        logger.exception(f"❌ Failed to add restaurants: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
