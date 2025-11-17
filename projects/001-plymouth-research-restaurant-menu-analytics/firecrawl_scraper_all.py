#!/usr/bin/env python3
"""
Firecrawl Batch Scraper - Scrape ALL Plymouth Restaurants
===========================================================

Scrapes all synthetic restaurants using Firecrawl API.

Author: Plymouth Research Team
Date: 2025-11-17
"""

import csv
import json
import logging
import time
from typing import Dict, List, Optional
from firecrawl import Firecrawl

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FirecrawlBatchScraper:
    """Batch restaurant menu scraper using Firecrawl API."""

    def __init__(self, api_key: str):
        """Initialize Firecrawl scraper."""
        self.firecrawl = Firecrawl(api_key=api_key)
        self.success_count = 0
        self.failed_count = 0
        self.total_items = 0
        logger.info("Firecrawl batch scraper initialized")

    def scrape_restaurant_menu(
        self,
        url: str,
        restaurant_name: str,
        cuisine_type: str = "Unknown"
    ) -> Optional[Dict]:
        """
        Scrape restaurant menu using Firecrawl.

        Args:
            url: Restaurant website URL
            restaurant_name: Name of the restaurant
            cuisine_type: Type of cuisine

        Returns:
            Dictionary with restaurant info and menu items, or None if failed
        """
        try:
            # Use Firecrawl to extract structured menu data
            result = self.firecrawl.scrape(
                url,
                formats=[{
                    "type": "json",
                    "prompt": """Extract the restaurant menu with ALL items. For each menu item, extract:
                    - name: dish name
                    - description: dish description (if available, otherwise empty string)
                    - price_gbp: price in GBP as a number (remove £ symbol, convert to float)
                    - category: category like Starters, Mains, Desserts, Sides, Drinks, Pizza, Pasta, Burgers, etc.
                    - dietary_tags: array of dietary tags like vegan, vegetarian, gluten-free, dairy-free, nut-free (empty array if none)

                    Also extract:
                    - address: full restaurant address (or empty string if not found)
                    - price_range: general price range like £5-15 (or empty string if not found)

                    Return JSON in this exact format:
                    {
                        "restaurant": {
                            "address": "full address or empty",
                            "price_range": "price range or empty"
                        },
                        "menu_items": [
                            {
                                "name": "dish name",
                                "description": "description or empty",
                                "price_gbp": 12.95,
                                "category": "Mains",
                                "dietary_tags": []
                            }
                        ]
                    }

                    Extract EVERY menu item you can find. Be thorough.
                    """
                }]
            )

            # Extract the JSON data
            if hasattr(result, 'extract') and result.extract:
                extracted_data = result.extract
            elif hasattr(result, 'json') and result.json:
                extracted_data = result.json
            elif isinstance(result, dict) and 'extract' in result:
                extracted_data = result['extract']
            else:
                logger.warning(f"⚠️ Unexpected result format for {restaurant_name}")
                self.failed_count += 1
                return None

            # Validate
            if not isinstance(extracted_data, dict):
                logger.warning(f"⚠️ Invalid data structure for {restaurant_name}")
                self.failed_count += 1
                return None

            # Build restaurant JSON
            restaurant_data = {
                "restaurant": {
                    "name": restaurant_name,
                    "address": extracted_data.get("restaurant", {}).get("address", ""),
                    "website_url": url,
                    "cuisine_type": cuisine_type,
                    "price_range": extracted_data.get("restaurant", {}).get("price_range", ""),
                    "data_source": "real_scraped",
                    "scraping_method": "firecrawl_api"
                },
                "menu_items": extracted_data.get("menu_items", [])
            }

            item_count = len(restaurant_data["menu_items"])
            self.total_items += item_count

            if item_count > 0:
                logger.info(f"✅ {restaurant_name}: {item_count} items")
                self.success_count += 1
            else:
                logger.info(f"⚠️ {restaurant_name}: 0 items (no menu found)")
                self.success_count += 1  # Still count as success, just no menu

            return restaurant_data

        except Exception as e:
            logger.error(f"❌ {restaurant_name}: {str(e)}")
            self.failed_count += 1
            return None

    def scrape_from_csv(self, csv_file: str, output_file: str, batch_size: int = 50):
        """
        Scrape restaurants from CSV file in batches.

        Args:
            csv_file: Path to CSV with restaurant data
            output_file: Path to save JSON results
            batch_size: Number of restaurants per batch file
        """
        restaurants = []

        # Read CSV
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                restaurants.append({
                    'name': row['name'],
                    'url': row['website_url'],
                    'cuisine_type': row['cuisine_type']
                })

        total_restaurants = len(restaurants)
        logger.info(f"\n📊 Starting batch scrape of {total_restaurants} restaurants")
        logger.info(f"💾 Results will be saved to {output_file}\n")

        results = []

        for i, resto in enumerate(restaurants, 1):
            logger.info(f"[{i}/{total_restaurants}] Scraping: {resto['name']}")

            data = self.scrape_restaurant_menu(
                url=resto['url'],
                restaurant_name=resto['name'],
                cuisine_type=resto.get('cuisine_type', 'Unknown')
            )

            if data:
                results.append(data)

            # Save progress every batch_size restaurants
            if i % batch_size == 0 or i == total_restaurants:
                self.save_to_json(results, output_file)
                logger.info(f"\n💾 Progress saved: {i}/{total_restaurants} restaurants processed\n")

            # Firecrawl handles rate limiting internally, no delay needed

        # Final summary
        logger.info("\n" + "="*80)
        logger.info("🎉 BATCH SCRAPING COMPLETED")
        logger.info("="*80)
        logger.info(f"Total restaurants processed: {total_restaurants}")
        logger.info(f"✅ Successful: {self.success_count}")
        logger.info(f"❌ Failed: {self.failed_count}")
        logger.info(f"📋 Total menu items extracted: {self.total_items}")
        logger.info(f"💾 Results saved to: {output_file}")
        logger.info("="*80 + "\n")

        return results

    def save_to_json(self, data: List[Dict], filename: str):
        """Save scraped data to JSON file."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    """Main scraping function."""
    # API Key
    API_KEY = "fc-5e88426ea5584be080853dfe03cb2b1a"

    # Initialize scraper
    scraper = FirecrawlBatchScraper(api_key=API_KEY)

    # Scrape all restaurants from CSV
    results = scraper.scrape_from_csv(
        csv_file="synthetic_restaurants_unique.csv",
        output_file="restaurants_firecrawl_all.json",
        batch_size=50
    )

    print(f"\n🎉 Scraping complete!")
    print(f"✅ Successfully scraped {len(results)} restaurants")
    print(f"📁 Data saved to: restaurants_firecrawl_all.json")


if __name__ == "__main__":
    main()
