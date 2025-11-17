#!/usr/bin/env python3
"""
Targeted scraper for Rockfish Plymouth
Extracts real menu data from their website
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scrape_rockfish_plymouth():
    """Scrape real menu data from Rockfish Plymouth"""

    url = "https://www.therockfish.co.uk/restaurants/plymouth/"

    logger.info(f"Fetching {url}")
    time.sleep(2)  # Rate limiting

    headers = {
        'User-Agent': 'PlymouthResearchBot/1.0 (Educational project)'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        restaurant = {
            "restaurant": {
                "name": "Rockfish Plymouth",
                "address": "3-4 Rope Walk, Coxside, Plymouth, PL4 0LB",
                "website_url": url,
                "cuisine_type": "Seafood",
                "price_range": "£8-26"
            },
            "menu_items": []
        }

        # Find all text content
        page_text = soup.get_text()

        # Pattern to find menu items with prices
        # Looking for pattern: Item Name: £X.XX or Item Name £X.XX
        price_pattern = r'([A-Z][A-Za-z\s\-&,]+?)[\s:]+£(\d+\.?\d*)'

        matches = re.finditer(price_pattern, page_text)

        menu_items_found = []

        for match in matches:
            dish_name = match.group(1).strip()
            price_str = match.group(2)

            # Filter out obviously wrong matches
            if len(dish_name) < 3 or len(dish_name) > 80:
                continue
            if 'Copyright' in dish_name or 'Menu' in dish_name:
                continue

            try:
                price = float(price_str)
                if price < 1 or price > 100:  # Reasonable price range
                    continue

                # Determine category based on price
                if price < 7:
                    category = "Sides"
                elif price < 13:
                    category = "Starters"
                else:
                    category = "Mains"

                # Check for dietary info
                dietary_tags = []
                if any(word in dish_name.lower() for word in ['vegan', 'vegetable', 'salad']):
                    dietary_tags.append("vegetarian")

                item = {
                    "name": dish_name,
                    "description": f"Fresh seafood from Rockfish Plymouth",
                    "price_gbp": price,
                    "category": category,
                    "dietary_tags": dietary_tags
                }

                # Avoid duplicates
                if dish_name not in [i['name'] for i in menu_items_found]:
                    menu_items_found.append(item)
                    logger.info(f"Found: {dish_name} - £{price}")

            except ValueError:
                continue

        # Take best items (remove near-duplicates, limit to reasonable number)
        unique_items = []
        seen_names = set()

        for item in menu_items_found[:20]:  # Limit to 20 items
            name_lower = item['name'].lower()

            # Skip if very similar to existing
            is_duplicate = False
            for seen in seen_names:
                if seen in name_lower or name_lower in seen:
                    is_duplicate = True
                    break

            if not is_duplicate:
                unique_items.append(item)
                seen_names.add(name_lower)

        restaurant["menu_items"] = unique_items[:12]  # Limit to 12 best items

        logger.info(f"\nExtracted {len(restaurant['menu_items'])} unique items from Rockfish")

        return restaurant

    except Exception as e:
        logger.error(f"Error scraping Rockfish: {e}")
        return None


def main():
    """Main function"""
    logger.info("="*60)
    logger.info("Scraping Rockfish Plymouth - Real Menu Data")
    logger.info("="*60)

    restaurant_data = scrape_rockfish_plymouth()

    if restaurant_data:
        # Save to JSON
        output_file = "restaurant_rockfish_real.json"
        with open(output_file, 'w') as f:
            json.dump([restaurant_data], f, indent=2)

        logger.info(f"\n{'='*60}")
        logger.info(f"Success! Real menu data saved to: {output_file}")
        logger.info(f"Total items: {len(restaurant_data['menu_items'])}")
        logger.info(f"{'='*60}\n")

        # Display items
        print("\nMenu Items Found:")
        print("-" * 60)
        for item in restaurant_data['menu_items']:
            print(f"{item['name']:<40} £{item['price_gbp']:<6.2f} {item['category']}")
        print("-" * 60)

    else:
        logger.error("Failed to scrape Rockfish")


if __name__ == "__main__":
    main()
