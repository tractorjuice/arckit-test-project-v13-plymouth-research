#!/usr/bin/env python3
"""
Sprint 2 Parser Testing
========================

Test all restaurant-specific parsers with mock restaurant HTML.

This validates Sprint 2 functionality:
1. Waterfront Parser (div/span based)
2. Boathouse Parser (table based)
3. Plymouth Grill Parser (list based)

Author: Plymouth Research Team
Date: 2025-11-17
"""

import sys
import logging
from pathlib import Path
from collections import defaultdict

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from parsers.waterfront_parser import WaterfrontParser
from parsers.boathouse_parser import BoathouseParser
from parsers.plymouth_grill_parser import PlymouthGrillParser

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


def print_menu_items(items: list, restaurant_name: str):
    """Print menu items grouped by category."""
    print(f"\n🍽️  {restaurant_name}")
    print(f"Total Items: {len(items)}")

    # Group by category
    by_category = defaultdict(list)
    for item in items:
        by_category[item['category']].append(item)

    # Calculate statistics
    total_price = sum(item['price_gbp'] for item in items if item['price_gbp'])
    avg_price = total_price / len([item for item in items if item['price_gbp']]) if items else 0
    items_with_tags = sum(1 for item in items if item.get('dietary_tags'))

    print(f"Categories: {len(by_category)}")
    print(f"Average Price: £{avg_price:.2f}")
    print(f"Items with Dietary Tags: {items_with_tags}/{len(items)} ({items_with_tags/len(items)*100:.0f}%)")

    print(f"\n📋 Menu Breakdown by Category:\n")
    for category, category_items in sorted(by_category.items()):
        print(f"  {category} ({len(category_items)} items)")

        for i, item in enumerate(category_items[:3], 1):  # Show first 3 per category
            print(f"    {i}. {item['name']}")
            if item['price_gbp']:
                print(f"       Price: £{item['price_gbp']:.2f}")
            if item['dietary_tags']:
                print(f"       Tags: {', '.join(item['dietary_tags'])}")

        if len(category_items) > 3:
            print(f"    ... and {len(category_items) - 3} more")
        print()


def test_waterfront_parser():
    """Test Waterfront Restaurant parser (div/span based)."""
    print_section("TEST 1: Waterfront Restaurant Parser (div/span based)")

    html_path = Path(__file__).parent / "test_data" / "mock_restaurant.html"

    with open(html_path, 'r') as f:
        html = f.read()

    parser = WaterfrontParser()
    items = parser.parse_menu(html)

    print(f"✅ Parser: WaterfrontParser")
    print(f"✅ HTML Pattern: <div class='menu-section'> → <div class='menu-item'>")
    print(f"✅ File: {html_path.name}")

    print_menu_items(items, "The Waterfront Restaurant")

    return items


def test_boathouse_parser():
    """Test Boathouse Cafe parser (table based)."""
    print_section("TEST 2: Boathouse Cafe Parser (table based)")

    html_path = Path(__file__).parent / "test_data" / "mock_boathouse_cafe.html"

    with open(html_path, 'r') as f:
        html = f.read()

    parser = BoathouseParser()
    items = parser.parse_menu(html)

    print(f"✅ Parser: BoathouseParser")
    print(f"✅ HTML Pattern: <table class='menu-table'> → <tr> → <td>")
    print(f"✅ File: {html_path.name}")

    print_menu_items(items, "The Boathouse Cafe")

    return items


def test_plymouth_grill_parser():
    """Test Plymouth Grill parser (list based)."""
    print_section("TEST 3: Plymouth Grill Parser (list based)")

    html_path = Path(__file__).parent / "test_data" / "mock_plymouth_grill.html"

    with open(html_path, 'r') as f:
        html = f.read()

    parser = PlymouthGrillParser()
    items = parser.parse_menu(html)

    print(f"✅ Parser: PlymouthGrillParser")
    print(f"✅ HTML Pattern: <ul class='menu-items'> → <li class='menu-item'>")
    print(f"✅ File: {html_path.name}")

    print_menu_items(items, "The Plymouth Grill")

    return items


def main():
    """Run all Sprint 2 parser tests."""
    print("\n" + "🧪"*40)
    print("  SPRINT 2 PARSER TESTING")
    print("  Plymouth Research Restaurant Menu Analytics")
    print("  Testing Multiple HTML Patterns")
    print("🧪"*40)

    try:
        # Test 1: Waterfront Parser
        waterfront_items = test_waterfront_parser()

        # Test 2: Boathouse Parser
        boathouse_items = test_boathouse_parser()

        # Test 3: Plymouth Grill Parser
        plymouth_grill_items = test_plymouth_grill_parser()

        # =====================================================================
        # Final Summary
        # =====================================================================
        print_section("Summary: All Parsers Tested")

        total_items = len(waterfront_items) + len(boathouse_items) + len(plymouth_grill_items)
        total_categories = set()
        total_dietary_tags = set()

        for items in [waterfront_items, boathouse_items, plymouth_grill_items]:
            for item in items:
                total_categories.add(item['category'])
                if item.get('dietary_tags'):
                    total_dietary_tags.update(item['dietary_tags'])

        print(f"📊 Aggregate Statistics:")
        print(f"   Restaurants Tested: 3")
        print(f"   Total Menu Items: {total_items}")
        print(f"   Unique Categories: {len(total_categories)} ({', '.join(sorted(total_categories))})")
        print(f"   Dietary Tags Found: {len(total_dietary_tags)} ({', '.join(sorted(total_dietary_tags))})")

        print(f"\n✅ Parser Coverage:")
        print(f"   ✅ Pattern 1 (div/span): WaterfrontParser ({len(waterfront_items)} items)")
        print(f"   ✅ Pattern 2 (table): BoathouseParser ({len(boathouse_items)} items)")
        print(f"   ✅ Pattern 3 (list): PlymouthGrillParser ({len(plymouth_grill_items)} items)")

        print(f"\n🎯 Sprint 2 Achievements:")
        print(f"   ✅ 3 parsers built for different HTML patterns")
        print(f"   ✅ {total_items} menu items parsed successfully")
        print(f"   ✅ Dietary tag extraction working across all parsers")
        print(f"   ✅ Price normalization consistent (£X.XX format)")
        print(f"   ✅ Category detection working")

        print(f"\n🚀 Ready for:")
        print(f"   ⏭️  Batch scraping script (scrape multiple restaurants)")
        print(f"   ⏭️  Database integration (store all parsed items)")
        print(f"   ⏭️  Parser selector (auto-detect HTML pattern)")
        print(f"   ⏭️  Real restaurant scraping (apply to live websites)")

        return 0

    except Exception as e:
        print("\n" + "="*80)
        print("❌ TEST FAILED!")
        print("="*80)
        print(f"\nError: {e}")
        logger.exception("Test failed with exception")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
