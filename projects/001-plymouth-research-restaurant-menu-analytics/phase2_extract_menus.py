#!/usr/bin/env python3
"""
Phase 2: Extract Menu Data
===========================

Extracts menu data from discovered menu URLs (from Phase 1).
Saves results to JSON for database import.

Restartable: Reads existing progress and continues from last checkpoint.

Author: Plymouth Research Team
Date: 2025-11-17
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
from firecrawl import Firecrawl

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MenuExtractor:
    """Extract menu data from menu URLs."""

    def __init__(self, api_key: str):
        """Initialize Firecrawl."""
        self.firecrawl = Firecrawl(api_key=api_key)
        self.success_count = 0
        self.failed_count = 0
        self.total_items = 0
        logger.info("Menu Extractor initialized")

    def extract_menu(self, restaurant_info: Dict) -> Optional[Dict]:
        """
        Extract menu from a menu URL.

        Args:
            restaurant_info: Dict with restaurant_name, menu_url, base_url, cuisine_type

        Returns:
            Dict with restaurant data and menu_items
        """
        restaurant_name = restaurant_info['restaurant_name']
        menu_url = restaurant_info['menu_url']

        try:
            logger.info(f"  📋 Extracting from: {menu_url}")

            result = self.firecrawl.scrape(
                menu_url,
                formats=[{
                    "type": "json",
                    "prompt": """Extract the restaurant menu with ALL items. For each menu item, extract:
                    - name: dish name (required)
                    - description: dish description (empty string if not available)
                    - price_gbp: price in GBP as a number - remove £ symbol (e.g., "£12.95" becomes 12.95)
                    - category: category like Starters, Mains, Desserts, Sides, Drinks, Pizza, Pasta (empty string if not clear)
                    - dietary_tags: array like ["vegan"], ["vegetarian"], ["gluten-free"] (empty array if none)

                    Also extract:
                    - address: full restaurant address (empty string if not found)
                    - price_range: general price range like "£10-25" (empty string if not found)

                    Return JSON in this format:
                    {
                        "restaurant": {
                            "address": "full address or empty",
                            "price_range": "price range or empty"
                        },
                        "menu_items": [
                            {
                                "name": "Margherita Pizza",
                                "description": "Tomato, mozzarella, basil",
                                "price_gbp": 12.95,
                                "category": "Pizza",
                                "dietary_tags": ["vegetarian"]
                            }
                        ]
                    }

                    Extract EVERY menu item. Be thorough.
                    """
                }]
            )

            # Extract JSON data
            if hasattr(result, 'extract') and result.extract:
                extracted_data = result.extract
            elif hasattr(result, 'json') and result.json:
                extracted_data = result.json
            elif isinstance(result, dict) and 'extract' in result:
                extracted_data = result['extract']
            else:
                logger.warning(f"  ⚠️ Unexpected result format")
                self.failed_count += 1
                return None

            if not isinstance(extracted_data, dict):
                logger.warning(f"  ⚠️ Invalid data structure")
                self.failed_count += 1
                return None

            # Build restaurant JSON
            restaurant_data = {
                "restaurant": {
                    "name": restaurant_name,
                    "address": extracted_data.get("restaurant", {}).get("address", ""),
                    "website_url": restaurant_info['base_url'],
                    "cuisine_type": restaurant_info.get('cuisine_type', 'Unknown'),
                    "price_range": extracted_data.get("restaurant", {}).get("price_range", ""),
                    "data_source": "real_scraped",
                    "scraping_method": "firecrawl_api_phase2"
                },
                "menu_items": extracted_data.get("menu_items", []),
                "menu_url": menu_url
            }

            item_count = len(restaurant_data["menu_items"])
            self.total_items += item_count

            if item_count > 0:
                logger.info(f"  ✅ {restaurant_name}: {item_count} items")
                self.success_count += 1
            else:
                logger.info(f"  ⚠️ {restaurant_name}: 0 items")
                self.success_count += 1

            return restaurant_data

        except Exception as e:
            logger.error(f"  ❌ {restaurant_name}: {str(e)}")
            self.failed_count += 1
            return None

    def extract_all(self, input_file: str, output_file: str, checkpoint_every: int = 25):
        """
        Extract menus for all discovered URLs.

        Args:
            input_file: JSON file from Phase 1 with menu URLs
            output_file: Output JSON file with extracted menus
            checkpoint_every: Save progress every N restaurants
        """
        # Load menu URLs from Phase 1
        logger.info(f"📂 Loading menu URLs from {input_file}")
        with open(input_file, 'r', encoding='utf-8') as f:
            discovered_restaurants = json.load(f)

        logger.info(f"✅ Loaded {len(discovered_restaurants)} restaurants")

        # Load existing extraction progress if available
        results = []
        extracted_names = set()

        if Path(output_file).exists():
            logger.info(f"📂 Loading existing extraction progress from {output_file}")
            with open(output_file, 'r', encoding='utf-8') as f:
                results = json.load(f)
                extracted_names = {r['restaurant']['name'] for r in results}
            logger.info(f"✅ Loaded {len(results)} previously extracted restaurants")

        # Filter out already extracted
        to_extract = [r for r in discovered_restaurants if r['restaurant_name'] not in extracted_names]

        total = len(to_extract)
        already_done = len(extracted_names)

        logger.info(f"\n📊 Menu Extraction")
        logger.info(f"Already extracted: {already_done}")
        logger.info(f"Remaining: {total}")
        logger.info(f"Total: {already_done + total}\n")

        # Extract menus
        for i, resto in enumerate(to_extract, 1):
            logger.info(f"\n[{already_done + i}/{already_done + total}] {resto['restaurant_name']}")

            data = self.extract_menu(resto)

            if data:
                results.append(data)

            # Save checkpoint
            if i % checkpoint_every == 0 or i == total:
                self.save_results(results, output_file)
                logger.info(f"\n💾 Checkpoint saved: {already_done + i}/{already_done + total} restaurants")
                logger.info(f"📊 Success: {self.success_count} | Failed: {self.failed_count} | Items: {self.total_items}\n")

        # Final save
        self.save_results(results, output_file)

        logger.info("\n" + "="*80)
        logger.info("🎉 PHASE 2 COMPLETE: Menu Extraction")
        logger.info("="*80)
        logger.info(f"Total restaurants: {len(results)}")
        logger.info(f"✅ Successful extractions: {self.success_count}")
        logger.info(f"❌ Failed extractions: {self.failed_count}")
        logger.info(f"📋 Total menu items: {self.total_items}")
        logger.info(f"💾 Saved to: {output_file}")
        logger.info("="*80 + "\n")

        return results

    def save_results(self, results: List[Dict], filename: str):
        """Save results to JSON."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)


def main():
    """Main extraction function."""
    API_KEY = "fc-5e88426ea5584be080853dfe03cb2b1a"

    extractor = MenuExtractor(api_key=API_KEY)

    extractor.extract_all(
        input_file="restaurant_menu_urls.json",
        output_file="restaurants_extracted.json",
        checkpoint_every=25
    )

    print(f"\n✅ Phase 2 complete!")
    print(f"📁 Menu data saved to: restaurants_extracted.json")
    print(f"\nNext step: Run 'python import_from_json.py restaurants_extracted.json' to import into database")


if __name__ == "__main__":
    main()
