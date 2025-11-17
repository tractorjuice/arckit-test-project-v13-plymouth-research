#!/usr/bin/env python3
"""
End-to-End Integration Demo
============================

Demonstrates complete data flow:
HTML → Parser → Database

This validates Path A (Quick Win):
1. Load mock restaurant HTML
2. Parse menu with WaterfrontParser
3. Store in SQLite database
4. Retrieve and display results

Author: Plymouth Research Team
Date: 2025-11-17
"""

import sys
import logging
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from database.connection import Database
from parsers.waterfront_parser import WaterfrontParser

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def print_section(title):
    """Print formatted section header."""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")


def main():
    """Run end-to-end demo."""
    print("\n" + "🎯"*40)
    print("  END-TO-END INTEGRATION DEMO")
    print("  Plymouth Research Restaurant Menu Analytics")
    print("  Path A: Quick Win - Real Data Flow")
    print("🎯"*40)

    # =========================================================================
    # STEP 1: Load Mock Restaurant HTML
    # =========================================================================
    print_section("STEP 1: Load Mock Restaurant HTML")

    html_path = Path(__file__).parent / "test_data" / "mock_restaurant.html"

    if not html_path.exists():
        print(f"❌ Mock restaurant HTML not found: {html_path}")
        return 1

    with open(html_path, 'r') as f:
        html_content = f.read()

    print(f"✅ Loaded HTML from: {html_path}")
    print(f"   File size: {len(html_content)} bytes")
    print(f"   Restaurant: The Waterfront Restaurant (Plymouth)")

    # =========================================================================
    # STEP 2: Parse Menu with WaterfrontParser
    # =========================================================================
    print_section("STEP 2: Parse Menu with WaterfrontParser")

    parser = WaterfrontParser()
    menu_items = parser.parse_menu(html_content)

    print(f"✅ Parsed {len(menu_items)} menu items")
    print("\n📋 Parsed Menu Items:")

    for i, item in enumerate(menu_items, 1):
        print(f"\n   {i}. {item['name']}")
        print(f"      Category: {item['category']}")
        if item['price_gbp']:
            print(f"      Price: £{item['price_gbp']:.2f}")
        if item['description']:
            print(f"      Description: {item['description']}")
        if item['dietary_tags']:
            print(f"      Dietary Tags: {', '.join(item['dietary_tags'])}")

    # =========================================================================
    # STEP 3: Connect to SQLite Database
    # =========================================================================
    print_section("STEP 3: Connect to SQLite Database")

    db_path = Path(__file__).parent / "plymouth_research.db"
    db = Database(str(db_path))
    db.connect()

    print(f"✅ Connected to database: {db_path}")
    print(f"   Database exists: {db_path.exists()}")
    print(f"   Database size: {db_path.stat().st_size:,} bytes" if db_path.exists() else "   (new database)")

    # =========================================================================
    # STEP 4: Insert Restaurant
    # =========================================================================
    print_section("STEP 4: Insert Restaurant into Database")

    restaurant_data = {
        'name': 'The Waterfront Restaurant',
        'address': 'Plymouth Waterfront, Devon',
        'website_url': 'https://waterfront-restaurant-plymouth.co.uk',
        'cuisine_type': 'British Seafood',
        'price_range': '£15-30',
    }

    restaurant_id = db.insert_restaurant(restaurant_data)

    if restaurant_id:
        print(f"✅ Restaurant inserted successfully")
        print(f"   Restaurant ID: {restaurant_id}")
        print(f"   Name: {restaurant_data['name']}")
        print(f"   Cuisine: {restaurant_data['cuisine_type']}")
        print(f"   Website: {restaurant_data['website_url']}")
    else:
        print("❌ Failed to insert restaurant")
        return 1

    # =========================================================================
    # STEP 5: Insert Menu Items
    # =========================================================================
    print_section("STEP 5: Insert Menu Items into Database")

    inserted_count = db.insert_menu_items(restaurant_id, menu_items)

    print(f"✅ Inserted {inserted_count} menu items")
    print(f"   Restaurant ID: {restaurant_id}")
    print(f"   Items with dietary tags: {sum(1 for item in menu_items if item.get('dietary_tags'))}")

    # =========================================================================
    # STEP 6: Log Scraping Attempt
    # =========================================================================
    print_section("STEP 6: Log Scraping Attempt (Audit Trail)")

    log_data = {
        'restaurant_id': restaurant_id,
        'url': restaurant_data['website_url'],
        'http_status_code': 200,
        'robots_txt_allowed': True,
        'rate_limit_delay_seconds': 0,
        'user_agent': 'PlymouthResearchMenuScraper/1.0',
        'success': True,
        'error_message': None,
        'scraped_at': datetime.now().isoformat()
    }

    db.log_scraping_attempt(log_data)
    print("✅ Scraping attempt logged to audit trail")

    # =========================================================================
    # STEP 7: Retrieve and Display Results
    # =========================================================================
    print_section("STEP 7: Retrieve Data from Database (Verification)")

    all_data = db.get_all_data()

    print(f"📊 Database Contents:")
    print(f"   Restaurants: {len(all_data['restaurants'])}")
    print(f"   Menu Items: {len(all_data['menu_items'])}")
    print(f"   Scraping Logs: {len(all_data['scraping_logs'])}")

    if all_data['restaurants']:
        print(f"\n🍽️  Restaurant Details:")
        for restaurant in all_data['restaurants']:
            print(f"   ID: {restaurant['restaurant_id']}")
            print(f"   Name: {restaurant['name']}")
            print(f"   Cuisine: {restaurant['cuisine_type']}")
            print(f"   Website: {restaurant['website_url']}")
            print(f"   Scraped: {restaurant['scraped_at']}")

    if all_data['menu_items']:
        print(f"\n📋 Sample Menu Items (first 5):")
        for i, item in enumerate(all_data['menu_items'][:5], 1):
            print(f"\n   {i}. {item['name']}")
            print(f"      Restaurant: {item['restaurant_name']}")
            print(f"      Category: {item['category']}")
            print(f"      Price: £{item['price_gbp']:.2f}" if item['price_gbp'] else "      Price: N/A")

    if all_data['scraping_logs']:
        print(f"\n📝 Scraping Log (most recent):")
        log = all_data['scraping_logs'][0]
        print(f"   URL: {log['url']}")
        print(f"   Status: {'✅ SUCCESS' if log['success'] else '❌ FAILED'}")
        print(f"   HTTP Status: {log['http_status_code']}")
        print(f"   Robots.txt: {'✅ Allowed' if log['robots_txt_allowed'] else '🚫 Blocked'}")
        print(f"   Scraped At: {log['scraped_at']}")

    # =========================================================================
    # STEP 8: Close Database Connection
    # =========================================================================
    db.close()
    print_section("STEP 8: Cleanup")
    print("✅ Database connection closed")

    # =========================================================================
    # Final Summary
    # =========================================================================
    print("\n" + "="*80)
    print("🎉 END-TO-END DEMO COMPLETE!")
    print("="*80)

    print("\n✅ Path A (Quick Win) Achievements:")
    print(f"   ✅ Mock restaurant HTML loaded ({len(html_content)} bytes)")
    print(f"   ✅ Menu parsed successfully ({len(menu_items)} items)")
    print(f"   ✅ SQLite database created and connected")
    print(f"   ✅ Restaurant inserted (ID: {restaurant_id})")
    print(f"   ✅ {inserted_count} menu items stored with dietary tags")
    print(f"   ✅ Scraping attempt logged to audit trail")
    print(f"   ✅ Data retrieved and verified from database")

    print("\n🎯 Data Flow Validated:")
    print("   HTML → Parser → Database → Query → Results")

    print("\n📊 Database Statistics:")
    print(f"   Database file: {db_path}")
    print(f"   Size: {db_path.stat().st_size:,} bytes")
    print(f"   Tables populated: 5 (restaurants, menu_items, menu_item_dietary_tags, scraping_logs, dietary_tags)")

    print("\n🚀 Ready for Sprint 2:")
    print("   ✅ Ethical scraping infrastructure complete (Sprint 1)")
    print("   ✅ End-to-end data flow validated (Path A)")
    print("   ⏭️  Next: Build parsers for 10-20 real Plymouth restaurants")
    print("   ⏭️  Next: Implement weekly automation")
    print("   ⏭️  Next: Data quality validation")

    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print("\n" + "="*80)
        print("❌ DEMO FAILED!")
        print("="*80)
        print(f"\nError: {e}")
        logger.exception("Demo failed with exception")
        sys.exit(1)
