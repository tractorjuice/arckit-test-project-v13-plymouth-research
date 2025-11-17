#!/usr/bin/env python3
"""
Automated Restaurant Menu Scraper
==================================

Automatically scrapes restaurant websites to update menu data.
Designed to run on a schedule (e.g., weekly via cron).

Features:
- Respects robots.txt
- Rate limiting (5 seconds between requests per domain)
- Error handling and logging
- Only updates when changes detected
- Tracks all scraping attempts in database

Author: Plymouth Research Team
Date: 2025-11-17
"""

import sys
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import requests
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.connection import Database

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class RestaurantScraper:
    """Automated scraper for restaurant menus."""

    def __init__(self, db_path: str = "plymouth_research.db"):
        """Initialize scraper with database connection."""
        self.db = Database(db_path)
        self.db.connect()
        self.user_agent = "PlymouthResearchBot/1.0 (Educational Research; respectful scraper)"
        self.rate_limit_seconds = 5  # Wait 5 seconds between requests per domain
        self.last_request_time = {}  # Track last request time per domain

    def check_robots_txt(self, url: str) -> bool:
        """Check if scraping is allowed by robots.txt."""
        try:
            parsed = urlparse(url)
            robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

            rp = RobotFileParser()
            rp.set_url(robots_url)
            rp.read()

            allowed = rp.can_fetch(self.user_agent, url)
            logger.info(f"robots.txt check for {parsed.netloc}: {'allowed' if allowed else 'disallowed'}")
            return allowed

        except Exception as e:
            logger.warning(f"Could not check robots.txt for {url}: {e}. Proceeding cautiously.")
            return True  # If we can't check, assume it's okay but log it

    def rate_limit(self, url: str):
        """Enforce rate limiting per domain."""
        parsed = urlparse(url)
        domain = parsed.netloc

        if domain in self.last_request_time:
            elapsed = time.time() - self.last_request_time[domain]
            if elapsed < self.rate_limit_seconds:
                sleep_time = self.rate_limit_seconds - elapsed
                logger.info(f"Rate limiting: sleeping {sleep_time:.2f}s for {domain}")
                time.sleep(sleep_time)

        self.last_request_time[domain] = time.time()

    def scrape_restaurant(self, restaurant: Dict) -> Optional[List[Dict]]:
        """
        Scrape a single restaurant's menu.

        Returns:
            List of menu items if successful, None otherwise
        """
        url = restaurant['website_url']
        restaurant_id = restaurant['restaurant_id']
        restaurant_name = restaurant['name']

        logger.info(f"Starting scrape for: {restaurant_name}")

        # Check robots.txt
        if not self.check_robots_txt(url):
            logger.warning(f"Scraping disallowed by robots.txt for {restaurant_name}")
            self.db.log_scraping_attempt({
                'restaurant_id': restaurant_id,
                'url': url,
                'http_status_code': None,
                'robots_txt_allowed': False,
                'rate_limit_delay_seconds': self.rate_limit_seconds,
                'user_agent': self.user_agent,
                'success': False,
                'error_message': 'Disallowed by robots.txt'
            })
            return None

        # Rate limiting
        self.rate_limit(url)

        try:
            # Attempt to fetch the webpage
            headers = {'User-Agent': self.user_agent}
            response = requests.get(url, headers=headers, timeout=10)

            logger.info(f"HTTP {response.status_code} for {restaurant_name}")

            if response.status_code != 200:
                self.db.log_scraping_attempt({
                    'restaurant_id': restaurant_id,
                    'url': url,
                    'http_status_code': response.status_code,
                    'robots_txt_allowed': True,
                    'rate_limit_delay_seconds': self.rate_limit_seconds,
                    'user_agent': self.user_agent,
                    'success': False,
                    'error_message': f'HTTP {response.status_code}'
                })
                return None

            # Parse menu items
            # NOTE: This is a placeholder - in production, you'd use BeautifulSoup
            # or a site-specific parser to extract menu items
            menu_items = self._parse_menu(response.text, restaurant_name)

            if menu_items:
                self.db.log_scraping_attempt({
                    'restaurant_id': restaurant_id,
                    'url': url,
                    'http_status_code': response.status_code,
                    'robots_txt_allowed': True,
                    'rate_limit_delay_seconds': self.rate_limit_seconds,
                    'user_agent': self.user_agent,
                    'success': True,
                    'error_message': None
                })
                logger.info(f"Successfully scraped {len(menu_items)} items from {restaurant_name}")
                return menu_items
            else:
                logger.warning(f"No menu items found for {restaurant_name}")
                return None

        except requests.Timeout:
            logger.error(f"Timeout scraping {restaurant_name}")
            self.db.log_scraping_attempt({
                'restaurant_id': restaurant_id,
                'url': url,
                'http_status_code': None,
                'robots_txt_allowed': True,
                'rate_limit_delay_seconds': self.rate_limit_seconds,
                'user_agent': self.user_agent,
                'success': False,
                'error_message': 'Request timeout'
            })
            return None

        except Exception as e:
            logger.exception(f"Error scraping {restaurant_name}: {e}")
            self.db.log_scraping_attempt({
                'restaurant_id': restaurant_id,
                'url': url,
                'http_status_code': None,
                'robots_txt_allowed': True,
                'rate_limit_delay_seconds': self.rate_limit_seconds,
                'user_agent': self.user_agent,
                'success': False,
                'error_message': str(e)
            })
            return None

    def _parse_menu(self, html: str, restaurant_name: str) -> Optional[List[Dict]]:
        """
        Parse menu items from HTML.

        NOTE: This is a placeholder implementation.
        In production, you would:
        1. Use BeautifulSoup to parse HTML
        2. Have restaurant-specific parsers
        3. Use ML/NLP to extract menu items
        4. Validate and normalize the data
        """
        # Placeholder - would need real implementation per restaurant
        logger.warning(f"Menu parsing not implemented for {restaurant_name}")
        return None

    def update_restaurant_menu(self, restaurant: Dict, new_menu_items: List[Dict]):
        """Update restaurant menu in database if changed."""
        restaurant_id = restaurant['restaurant_id']
        restaurant_name = restaurant['name']

        # Get current menu items
        current_items = self.db.get_menu_items_for_restaurant(restaurant_id)

        # Simple change detection - compare counts
        # In production, you'd do deep comparison
        if len(current_items) != len(new_menu_items):
            logger.info(f"Menu changed for {restaurant_name}: {len(current_items)} -> {len(new_menu_items)} items")

            # Delete old menu items
            cursor = self.db.conn.cursor()
            cursor.execute("""
                DELETE FROM menu_item_dietary_tags
                WHERE item_id IN (
                    SELECT item_id FROM menu_items WHERE restaurant_id = ?
                )
            """, (restaurant_id,))
            cursor.execute("DELETE FROM menu_items WHERE restaurant_id = ?", (restaurant_id,))
            self.db.conn.commit()

            # Insert new menu items
            self.db.insert_menu_items(restaurant_id, new_menu_items)
            logger.info(f"Updated menu for {restaurant_name}")
        else:
            logger.info(f"No menu changes detected for {restaurant_name}")

    def scrape_all(self):
        """Scrape all restaurants in the database."""
        logger.info("=" * 80)
        logger.info("Starting automated scraping run")
        logger.info("=" * 80)

        # Get all restaurants
        all_data = self.db.get_all_data()
        restaurants = all_data['restaurants']

        logger.info(f"Found {len(restaurants)} restaurants to scrape")

        success_count = 0
        failure_count = 0

        for restaurant in restaurants:
            try:
                menu_items = self.scrape_restaurant(restaurant)

                if menu_items:
                    self.update_restaurant_menu(restaurant, menu_items)
                    success_count += 1
                else:
                    failure_count += 1

            except Exception as e:
                logger.exception(f"Unexpected error processing {restaurant['name']}: {e}")
                failure_count += 1

        logger.info("=" * 80)
        logger.info(f"Scraping run completed: {success_count} successful, {failure_count} failed")
        logger.info("=" * 80)

        return success_count, failure_count

    def close(self):
        """Close database connection."""
        self.db.close()


def main():
    """Main entry point for automated scraper."""
    print("\n🤖 Plymouth Restaurant Menu Scraper")
    print("=" * 80)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    scraper = RestaurantScraper()

    try:
        success, failure = scraper.scrape_all()

        print("\n📊 Results:")
        print(f"   ✅ Successful: {success}")
        print(f"   ❌ Failed: {failure}")
        print(f"\n🕐 Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        return 0 if failure == 0 else 1

    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        return 1

    finally:
        scraper.close()


if __name__ == "__main__":
    sys.exit(main())
