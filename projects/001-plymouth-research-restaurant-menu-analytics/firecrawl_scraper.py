#!/usr/bin/env python3
"""
Firecrawl-Powered Restaurant Menu Scraper
==========================================

Uses Firecrawl API to scrape restaurant menus from complex websites
including JavaScript-rendered content and PDFs.

Author: Plymouth Research Team
Date: 2025-11-17
"""

import json
import logging
from typing import Dict, List, Optional
from firecrawl import Firecrawl

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FirecrawlMenuScraper:
    """Restaurant menu scraper using Firecrawl API."""

    def __init__(self, api_key: str):
        """
        Initialize Firecrawl scraper.

        Args:
            api_key: Firecrawl API key
        """
        self.firecrawl = Firecrawl(api_key=api_key)
        logger.info("Firecrawl scraper initialized")

    def scrape_restaurant_menu(
        self,
        url: str,
        restaurant_name: str,
        cuisine_type: str = "Unknown"
    ) -> Optional[Dict]:
        """
        Scrape restaurant menu using Firecrawl with structured extraction.

        Args:
            url: Restaurant website URL
            restaurant_name: Name of the restaurant
            cuisine_type: Type of cuisine

        Returns:
            Dictionary with restaurant info and menu items, or None if failed
        """
        logger.info(f"Scraping {restaurant_name} from {url}")

        try:
            # Use Firecrawl to extract structured menu data
            result = self.firecrawl.scrape(
                url,
                formats=[{
                    "type": "json",
                    "prompt": """Extract the restaurant menu with ALL items. For each menu item, extract:
                    - name: dish name
                    - description: dish description (if available)
                    - price_gbp: price in GBP as a number (remove £ symbol, convert to float)
                    - category: category like Starters, Mains, Desserts, Sides, Drinks, Pizza, Pasta, etc.
                    - dietary_tags: array of dietary tags like vegan, vegetarian, gluten-free, dairy-free, nut-free

                    Also extract:
                    - address: full restaurant address
                    - price_range: general price range (e.g., £10-25)

                    Return JSON in this format:
                    {
                        "restaurant": {
                            "address": "full address",
                            "price_range": "price range"
                        },
                        "menu_items": [
                            {
                                "name": "dish name",
                                "description": "description",
                                "price_gbp": 12.95,
                                "category": "Mains",
                                "dietary_tags": ["vegetarian"]
                            }
                        ]
                    }

                    Extract ALL menu items you can find on the page. Include everything.
                    """
                }]
            )

            # Extract the JSON data from result
            if hasattr(result, 'extract') and result.extract:
                extracted_data = result.extract
            elif hasattr(result, 'json') and result.json:
                extracted_data = result.json
            elif isinstance(result, dict) and 'extract' in result:
                extracted_data = result['extract']
            else:
                logger.warning(f"Unexpected result format for {restaurant_name}")
                return None

            # Validate and structure the data
            if not isinstance(extracted_data, dict):
                logger.warning(f"Extracted data is not a dict for {restaurant_name}")
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
            logger.info(f"✅ Successfully scraped {restaurant_name}: {item_count} items")

            return restaurant_data

        except Exception as e:
            logger.error(f"❌ Failed to scrape {restaurant_name}: {str(e)}")
            return None

    def scrape_multiple_restaurants(
        self,
        restaurants: List[Dict[str, str]]
    ) -> List[Dict]:
        """
        Scrape multiple restaurants.

        Args:
            restaurants: List of dicts with 'url', 'name', and 'cuisine_type'

        Returns:
            List of successfully scraped restaurant data
        """
        results = []

        for resto in restaurants:
            data = self.scrape_restaurant_menu(
                url=resto['url'],
                restaurant_name=resto['name'],
                cuisine_type=resto.get('cuisine_type', 'Unknown')
            )

            if data:
                results.append(data)

        logger.info(f"\n✅ Successfully scraped {len(results)}/{len(restaurants)} restaurants")
        return results

    def save_to_json(self, data: List[Dict], filename: str):
        """Save scraped data to JSON file."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"💾 Saved data to {filename}")


def main():
    """Main scraping function."""
    # API Key
    API_KEY = "fc-5e88426ea5584be080853dfe03cb2b1a"

    # Initialize scraper
    scraper = FirecrawlMenuScraper(api_key=API_KEY)

    # Plymouth restaurants to scrape
    restaurants = [
        {
            "url": "https://www.bostonteaparty.co.uk/cafes/plymouth/",
            "name": "Boston Tea Party Plymouth",
            "cuisine_type": "Cafe/Brunch"
        },
        {
            "url": "https://www.pieminister.co.uk/restaurants/plymouth",
            "name": "Pieminister Plymouth",
            "cuisine_type": "British Pies"
        },
        {
            "url": "https://www.bills-website.co.uk/restaurants/plymouth",
            "name": "Bill's Plymouth",
            "cuisine_type": "British/International"
        },
        {
            "url": "https://www.zizzi.co.uk/restaurants/plymouth/plymouth-barbican",
            "name": "Zizzi Plymouth",
            "cuisine_type": "Italian"
        },
        {
            "url": "https://www.askitalian.co.uk/restaurants/plymouth-barbican/",
            "name": "ASK Italian Plymouth",
            "cuisine_type": "Italian"
        },
        {
            "url": "https://www.pizzaexpress.com/plymouth-barbican-leisure-park",
            "name": "Pizza Express Plymouth",
            "cuisine_type": "Italian Pizza"
        },
        {
            "url": "https://www.nandos.co.uk/restaurants/plymouth-barbican",
            "name": "Nando's Plymouth",
            "cuisine_type": "Portuguese Chicken"
        },
        {
            "url": "https://thelounges.co.uk/armado",
            "name": "Armado Lounge Plymouth",
            "cuisine_type": "British/International"
        },
        {
            "url": "https://thelounges.co.uk/seco",
            "name": "Seco Lounge Plymouth",
            "cuisine_type": "British/International"
        },
        {
            "url": "https://www.socialpubandkitchen.co.uk/roundabout-plymouth",
            "name": "Roundabout Plymouth",
            "cuisine_type": "Pub Food"
        }
    ]

    # Scrape all restaurants
    results = scraper.scrape_multiple_restaurants(restaurants)

    # Save results
    if results:
        scraper.save_to_json(results, "restaurants_firecrawl_batch_1.json")
        print(f"\n🎉 Scraped {len(results)} restaurants successfully!")
        print("📁 Data saved to: restaurants_firecrawl_batch_1.json")
    else:
        print("\n❌ No restaurants were successfully scraped")


if __name__ == "__main__":
    main()
