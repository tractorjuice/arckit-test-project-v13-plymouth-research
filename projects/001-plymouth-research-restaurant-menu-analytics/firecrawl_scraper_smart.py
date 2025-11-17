#!/usr/bin/env python3
"""
Smart Firecrawl Restaurant Scraper - Crawl Then Extract
========================================================

1. Crawls restaurant website to find menu pages
2. Extracts menu data from the actual menu page (not homepage)

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


class SmartFirecrawlScraper:
    """Smart restaurant scraper - crawls to find menu, then extracts."""

    def __init__(self, api_key: str):
        """Initialize Firecrawl scraper."""
        self.firecrawl = Firecrawl(api_key=api_key)
        self.success_count = 0
        self.failed_count = 0
        self.total_items = 0
        logger.info("Smart Firecrawl scraper initialized")

    def find_menu_page(self, base_url: str, restaurant_name: str) -> Optional[str]:
        """
        Crawl website to find the menu page.

        Args:
            base_url: Restaurant website base URL
            restaurant_name: Name of restaurant

        Returns:
            URL of menu page, or None if not found
        """
        try:
            # Use Firecrawl map to discover site structure
            logger.info(f"  🔍 Mapping site structure for {restaurant_name}")

            map_result = self.firecrawl.map(url=base_url)

            if not map_result or not hasattr(map_result, 'links'):
                logger.warning(f"  ⚠️ No site map returned for {restaurant_name}")
                return base_url  # Fall back to base URL

            links = map_result.links if hasattr(map_result, 'links') else []

            # Look for menu-related pages (HTML or PDF)
            menu_keywords = ['menu', 'food', 'eat', 'dining', 'restaurant-menu', 'our-menu']

            for link in links:
                # Handle LinkResult objects or strings
                link_url = link.url if hasattr(link, 'url') else str(link)
                link_lower = link_url.lower()

                # Check for menu pages (HTML or PDF)
                if any(keyword in link_lower for keyword in menu_keywords):
                    logger.info(f"  ✅ Found menu page: {link_url}")
                    return link_url

                # Also check for PDF links specifically
                if link_lower.endswith('.pdf') and any(keyword in link_lower for keyword in ['menu', 'food']):
                    logger.info(f"  ✅ Found PDF menu: {link_url}")
                    return link_url

            # No menu page found in map, try common paths
            logger.info(f"  🔍 No menu found in map, trying common paths...")

            # Try common menu URL patterns (HTML and PDF)
            common_paths = [
                '/menu', '/menus', '/food', '/our-menu', '/eat',
                '/restaurant-menu', '/food-menu', '/menu.html',
                '/menu.pdf', '/menus.pdf', '/food-menu.pdf', '/main-menu.pdf'
            ]

            base_domain = base_url.rstrip('/')
            for path in common_paths:
                test_url = base_domain + path
                logger.info(f"  🔗 Trying: {test_url}")

                # Quick test - try to scrape with markdown to see if page exists
                # Firecrawl can handle both HTML and PDF
                try:
                    test_result = self.firecrawl.scrape(test_url, formats=['markdown'])
                    if test_result and hasattr(test_result, 'markdown') and len(test_result.markdown) > 100:
                        logger.info(f"  ✅ Found menu at: {test_url} {'(PDF)' if path.endswith('.pdf') else '(HTML)'}")
                        return test_url
                except:
                    pass  # Page doesn't exist, try next

            logger.warning(f"  ⚠️ No menu page found, using base URL")
            return base_url

        except Exception as e:
            logger.warning(f"  ⚠️ Error mapping site for {restaurant_name}: {str(e)}")
            # Still try common paths even if map failed (including PDFs)
            base_domain = base_url.rstrip('/')
            for path in ['/menu', '/menus', '/food', '/menu.pdf', '/menus.pdf']:
                try:
                    test_url = base_domain + path
                    test_result = self.firecrawl.scrape(test_url, formats=['markdown'])
                    if test_result and hasattr(test_result, 'markdown') and len(test_result.markdown) > 100:
                        logger.info(f"  ✅ Found menu at: {test_url}")
                        return test_url
                except:
                    pass
            return base_url  # Final fallback

    def scrape_restaurant_menu(
        self,
        url: str,
        restaurant_name: str,
        cuisine_type: str = "Unknown"
    ) -> Optional[Dict]:
        """
        Smart scrape: Find menu page first, then extract.

        Args:
            url: Restaurant website URL
            restaurant_name: Name of the restaurant
            cuisine_type: Type of cuisine

        Returns:
            Dictionary with restaurant info and menu items, or None if failed
        """
        try:
            # Step 1: Find the menu page
            menu_url = self.find_menu_page(url, restaurant_name)

            # Step 2: Extract menu data from the menu page
            logger.info(f"  📋 Extracting menu from: {menu_url}")

            result = self.firecrawl.scrape(
                menu_url,
                formats=[{
                    "type": "json",
                    "prompt": """Extract the restaurant menu with ALL items you can find. For each menu item, extract:
                    - name: dish name (required)
                    - description: dish description (empty string if not available)
                    - price_gbp: price in GBP as a number - remove £ symbol and convert to float (e.g., "£12.95" becomes 12.95)
                    - category: category like Starters, Mains, Desserts, Sides, Drinks, Pizza, Pasta, Burgers (empty string if not clear)
                    - dietary_tags: array of dietary tags like ["vegan"], ["vegetarian"], ["gluten-free"] (empty array if none)

                    Also extract:
                    - address: full restaurant address (empty string if not found)
                    - price_range: general price range like "£10-25" (empty string if not found)

                    Return JSON in this exact format:
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

                    Extract EVERY menu item you can find on this page. Be thorough and include all dishes, drinks, sides, desserts.
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
                logger.warning(f"  ⚠️ Unexpected result format for {restaurant_name}")
                self.failed_count += 1
                return None

            # Validate
            if not isinstance(extracted_data, dict):
                logger.warning(f"  ⚠️ Invalid data structure for {restaurant_name}")
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
                    "scraping_method": "firecrawl_api_smart"
                },
                "menu_items": extracted_data.get("menu_items", [])
            }

            item_count = len(restaurant_data["menu_items"])
            self.total_items += item_count

            if item_count > 0:
                logger.info(f"  ✅ {restaurant_name}: {item_count} items")
                self.success_count += 1
            else:
                logger.info(f"  ⚠️ {restaurant_name}: 0 items (no menu extracted)")
                self.success_count += 1

            return restaurant_data

        except Exception as e:
            logger.error(f"  ❌ {restaurant_name}: {str(e)}")
            self.failed_count += 1
            return None

    def scrape_from_csv(self, csv_file: str, output_file: str, batch_size: int = 25):
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
        logger.info(f"\n📊 Starting SMART batch scrape of {total_restaurants} restaurants")
        logger.info(f"💡 Strategy: Crawl to find menu page → Extract from menu page")
        logger.info(f"💾 Results will be saved to {output_file}\n")

        results = []

        for i, resto in enumerate(restaurants, 1):
            logger.info(f"\n[{i}/{total_restaurants}] Scraping: {resto['name']}")

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
                logger.info(f"\n💾 Progress saved: {i}/{total_restaurants} restaurants processed")
                logger.info(f"📊 Success: {self.success_count} | Failed: {self.failed_count} | Items: {self.total_items}\n")

        # Final summary
        logger.info("\n" + "="*80)
        logger.info("🎉 SMART BATCH SCRAPING COMPLETED")
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
    scraper = SmartFirecrawlScraper(api_key=API_KEY)

    # Scrape all restaurants from CSV
    results = scraper.scrape_from_csv(
        csv_file="synthetic_restaurants_unique.csv",
        output_file="restaurants_firecrawl_smart.json",
        batch_size=25  # Save more frequently for smart scraping
    )

    print(f"\n🎉 Smart scraping complete!")
    print(f"✅ Successfully scraped {len(results)} restaurants")
    print(f"📁 Data saved to: restaurants_firecrawl_smart.json")


if __name__ == "__main__":
    main()
