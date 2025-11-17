"""
Plymouth Research Menu Scraper
================================

Main scraper orchestration integrating ethical compliance controls.

This module coordinates:
- Robots.txt compliance checking (BEFORE every request)
- Rate limiting (5 seconds per domain minimum)
- Database logging (comprehensive audit trail)
- HTML parsing and data extraction

Requirements:
- FR-011: Web scraping with robots.txt compliance
- NFR-C-001: 100% robots.txt compliance
- NFR-C-003: Rate limiting (5 seconds per domain)
- Principle 3: Ethical web scraping (NON-NEGOTIABLE)
- Goal G-3: Zero legal violations

Author: Plymouth Research Team
Date: 2025-11-17
"""

import logging
import time
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from .robots_parser import RobotsParser
from .rate_limiter import DomainRateLimiter

logger = logging.getLogger(__name__)


class MenuScraper:
    """
    Ethical menu scraper with robots.txt compliance and rate limiting.

    This is the main scraping class that coordinates all ethical controls.
    """

    # User-Agent identifying Plymouth Research with contact URL
    USER_AGENT = "PlymouthResearchMenuScraper/1.0 (+https://plymouthresearch.uk; contact@plymouthresearch.uk)"

    def __init__(self, db_connection=None):
        """
        Initialize menu scraper with ethical compliance controls.

        Args:
            db_connection: Database connection for logging (optional for testing)
        """
        self.robots_parser = RobotsParser(user_agent=self.USER_AGENT)
        self.rate_limiter = DomainRateLimiter(min_delay_seconds=5.0)
        self.db_connection = db_connection

        logger.info("="*80)
        logger.info("MenuScraper initialized")
        logger.info(f"User-Agent: {self.USER_AGENT}")
        logger.info(f"Rate limit: {self.rate_limiter.min_delay_seconds}s per domain")
        logger.info(f"Robots.txt: ENFORCED")
        logger.info("="*80)

    def scrape_restaurant(self, restaurant_id: int, website_url: str) -> Tuple[bool, str, Optional[List[Dict]]]:
        """
        Scrape a single restaurant's menu with full ethical compliance.

        This method is the MAIN ENTRY POINT for scraping a restaurant.
        It enforces ALL ethical controls in the correct order:

        1. Check robots.txt (BEFORE making request)
        2. Apply rate limiting (wait if needed)
        3. Make HTTP request
        4. Parse menu data
        5. Log to database (success or failure)

        Args:
            restaurant_id: Database ID of restaurant
            website_url: Restaurant's website URL to scrape

        Returns:
            Tuple of (success: bool, message: str, menu_items: Optional[List[Dict]])
            - success: True if scraping succeeded, False if failed
            - message: Human-readable status message
            - menu_items: List of extracted menu items (if success), None otherwise

        Example:
            >>> scraper = MenuScraper(db_connection)
            >>> success, message, items = scraper.scrape_restaurant(1, "https://restaurant.com/menu")
            >>> if success:
            >>>     print(f"Extracted {len(items)} menu items")
            >>> else:
            >>>     print(f"Scraping failed: {message}")
        """
        scrape_start_time = time.time()
        log_data = {
            "restaurant_id": restaurant_id,
            "url": website_url,
            "scraped_at": datetime.now(),
            "user_agent": self.USER_AGENT,
        }

        try:
            # STEP 1: Check robots.txt (CRITICAL - MUST check BEFORE request)
            logger.info(f"🔍 STEP 1: Checking robots.txt for {website_url}")
            robots_allowed, robots_reason = self.robots_parser.can_fetch(website_url)
            log_data["robots_txt_allowed"] = robots_allowed

            if not robots_allowed:
                # BLOCKED by robots.txt - MUST NOT proceed
                message = f"🚫 BLOCKED by robots.txt: {robots_reason}"
                logger.warning(message)
                log_data["success"] = False
                log_data["http_status_code"] = None
                log_data["error_message"] = "Blocked by robots.txt"
                log_data["rate_limit_delay_seconds"] = 0

                # Log compliance violation (this should NEVER happen in production)
                self._log_to_database(log_data)

                return False, message, None

            logger.info(f"✅ robots.txt allows scraping: {website_url}")

            # STEP 2: Get crawl delay from robots.txt (if specified)
            crawl_delay = self.robots_parser.get_crawl_delay(website_url)

            # STEP 3: Apply rate limiting (wait if needed)
            logger.info(f"⏱️  STEP 2: Applying rate limiting")
            delay_waited = self.rate_limiter.wait_if_needed(website_url, crawl_delay=crawl_delay)
            log_data["rate_limit_delay_seconds"] = int(delay_waited)

            if delay_waited > 0:
                logger.info(f"⏸️  Waited {delay_waited:.2f}s for rate limiting")

            # STEP 4: Make HTTP request
            logger.info(f"🌐 STEP 3: Making HTTP request to {website_url}")
            response = requests.get(
                website_url,
                headers={"User-Agent": self.USER_AGENT},
                timeout=30  # 30 second timeout
            )

            log_data["http_status_code"] = response.status_code

            if response.status_code != 200:
                message = f"❌ HTTP {response.status_code}: {website_url}"
                logger.warning(message)
                log_data["success"] = False
                log_data["error_message"] = f"HTTP {response.status_code}"
                self._log_to_database(log_data)
                return False, message, None

            logger.info(f"✅ HTTP 200 OK: {website_url}")

            # STEP 5: Parse menu data
            logger.info(f"📄 STEP 4: Parsing HTML content")
            menu_items = self._parse_menu_html(response.text, website_url)

            if not menu_items:
                message = f"⚠️  No menu items found at {website_url}"
                logger.warning(message)
                log_data["success"] = False
                log_data["error_message"] = "No menu items extracted"
                self._log_to_database(log_data)
                return False, message, None

            # Success!
            scrape_duration = time.time() - scrape_start_time
            message = f"✅ SUCCESS: Extracted {len(menu_items)} menu items from {website_url} in {scrape_duration:.2f}s"
            logger.info(message)

            log_data["success"] = True
            log_data["error_message"] = None
            self._log_to_database(log_data)

            return True, message, menu_items

        except requests.exceptions.Timeout:
            message = f"⏱️  TIMEOUT: {website_url} (30s timeout exceeded)"
            logger.error(message)
            log_data["success"] = False
            log_data["http_status_code"] = None
            log_data["error_message"] = "Request timeout (30s)"
            log_data["rate_limit_delay_seconds"] = int(delay_waited) if 'delay_waited' in locals() else 0
            self._log_to_database(log_data)
            return False, message, None

        except requests.exceptions.RequestException as e:
            message = f"❌ REQUEST ERROR: {website_url} - {str(e)}"
            logger.error(message)
            log_data["success"] = False
            log_data["http_status_code"] = None
            log_data["error_message"] = f"Request error: {str(e)}"
            log_data["rate_limit_delay_seconds"] = int(delay_waited) if 'delay_waited' in locals() else 0
            self._log_to_database(log_data)
            return False, message, None

        except Exception as e:
            message = f"❌ UNEXPECTED ERROR: {website_url} - {str(e)}"
            logger.exception(message)
            log_data["success"] = False
            log_data["http_status_code"] = None
            log_data["error_message"] = f"Unexpected error: {str(e)}"
            log_data["rate_limit_delay_seconds"] = int(delay_waited) if 'delay_waited' in locals() else 0
            self._log_to_database(log_data)
            return False, message, None

    def _parse_menu_html(self, html: str, source_url: str) -> List[Dict]:
        """
        Parse HTML to extract menu items.

        NOTE: This is a PLACEHOLDER implementation.
        Sprint 2 will implement restaurant-specific parsing logic.

        Args:
            html: Raw HTML content
            source_url: Source URL for data lineage

        Returns:
            List of menu item dictionaries with keys:
            - name: str
            - description: Optional[str]
            - price_gbp: Optional[float]
            - category: Optional[str]
            - source_url: str
            - scraped_at: datetime
        """
        soup = BeautifulSoup(html, 'lxml')

        # PLACEHOLDER: Basic extraction (will be enhanced in Sprint 2)
        # This extracts ANY text that looks like a menu item
        menu_items = []

        # Example: Look for elements that might be menu items
        # (This is very basic - real implementation will be restaurant-specific)
        potential_items = soup.find_all(['div', 'li', 'p'], class_=lambda x: x and ('menu' in x.lower() or 'item' in x.lower()))

        for element in potential_items[:10]:  # Limit to 10 for now
            text = element.get_text(strip=True)
            if text and len(text) > 5:  # Basic filter
                menu_items.append({
                    "name": text[:255],  # Truncate to DB column limit
                    "description": None,  # TODO: Extract description
                    "price_gbp": None,   # TODO: Extract and normalize price
                    "category": None,    # TODO: Categorize
                    "source_url": source_url,
                    "scraped_at": datetime.now(),
                    "source_html": str(element)[:1000]  # Store snippet for debugging
                })

        logger.info(f"📊 Extracted {len(menu_items)} potential menu items (placeholder extraction)")
        return menu_items

    def _log_to_database(self, log_data: Dict):
        """
        Log scraping attempt to database (E-006: Scraping Logs).

        This creates a comprehensive audit trail for:
        - Ethical compliance monitoring (robots.txt, rate limiting)
        - Debugging scraping failures
        - Legal compliance demonstration

        Args:
            log_data: Dictionary with scraping log fields
        """
        if not self.db_connection:
            logger.warning("⚠️  No database connection - skipping log write")
            return

        try:
            # TODO: Implement database INSERT in Sprint 1
            # INSERT INTO scraping_logs (...)
            logger.debug(f"📝 Would log to database: {log_data}")

        except Exception as e:
            logger.error(f"❌ Failed to log to database: {e}")


# ============================================================================
# Usage Example
# ============================================================================

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Initialize scraper (no DB connection for testing)
    scraper = MenuScraper(db_connection=None)

    # Test scraping
    test_restaurants = [
        (1, "https://example.com/"),
        (2, "https://httpbin.org/html"),
    ]

    print("\n" + "="*80)
    print("Menu Scraper - Test Run")
    print("="*80 + "\n")

    for restaurant_id, url in test_restaurants:
        print(f"\nScraping Restaurant ID {restaurant_id}: {url}")
        print("-" * 80)

        success, message, items = scraper.scrape_restaurant(restaurant_id, url)

        print(f"Result: {message}")
        if success and items:
            print(f"Extracted {len(items)} items:")
            for item in items[:3]:  # Show first 3
                print(f"  - {item['name'][:50]}")
        print()
