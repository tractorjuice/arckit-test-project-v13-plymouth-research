#!/usr/bin/env python3
"""
Trustpilot Review Scraper for Plymouth Research Restaurants
============================================================

Scrapes Trustpilot reviews for restaurants in the Plymouth Research database
and stores them in SQLite.

Features:
- Multi-restaurant batch processing
- Rate limiting and ethical scraping
- Incremental updates (only fetch new reviews)
- Deduplication and data validation
- Progress tracking and error handling

Usage:
    # Scrape all restaurants with Trustpilot URLs
    python fetch_trustpilot_reviews.py --all

    # Scrape specific restaurant
    python fetch_trustpilot_reviews.py --restaurant-id 5

    # Incremental update (only new reviews)
    python fetch_trustpilot_reviews.py --update

    # Test with single restaurant
    python fetch_trustpilot_reviews.py --test
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import re
import argparse
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TrustpilotRestaurantScraper:
    """Scraper for Trustpilot reviews adapted for restaurant use case"""

    def __init__(self, db_path: str = "plymouth_research.db", rate_limit: float = 2.5):
        """
        Initialize scraper

        Args:
            db_path: Path to SQLite database
            rate_limit: Seconds to wait between requests (default 2.5s)
        """
        self.db_path = db_path
        self.rate_limit = rate_limit
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5"
        })

    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def get_reviews_from_page(self, url: str, page_number: int = 1) -> Tuple[List[Dict], Optional[Dict]]:
        """
        Get reviews from a specific Trustpilot page URL

        Args:
            url: Trustpilot page URL
            page_number: Page number being fetched

        Returns:
            Tuple of (reviews list, pagination info dict)
        """
        try:
            logger.info(f"Fetching page {page_number}: {url}")
            response = self.session.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the __NEXT_DATA__ script tag
            reviews_raw = soup.find("script", id="__NEXT_DATA__")
            if not reviews_raw:
                logger.warning(f"Could not find __NEXT_DATA__ script on page {url}")
                return [], None

            data = json.loads(reviews_raw.string)

            # Navigate to reviews in the JSON structure
            if not (data.get("props") and
                    data["props"].get("pageProps") and
                    data["props"]["pageProps"].get("reviews")):
                logger.warning(f"Unexpected data structure on page {url}")
                return [], None

            reviews = data["props"]["pageProps"]["reviews"]
            pagination = data["props"]["pageProps"].get("pagination", {})

            # Add page number to each review
            for review in reviews:
                review['_page_number'] = page_number

            logger.info(f"Found {len(reviews)} reviews on page {page_number}")

            return reviews, pagination

        except Exception as e:
            logger.error(f"Error fetching page {url}: {e}")
            return [], None

    def parse_review(self, review_data: Dict, restaurant_id: int) -> Dict:
        """
        Parse raw review data from Trustpilot JSON

        Args:
            review_data: Raw review dict from Trustpilot
            restaurant_id: Database ID of the restaurant

        Returns:
            Parsed review dict ready for database insertion
        """
        try:
            # Parse date
            review_date = review_data.get("dates", {}).get("publishedDate")
            if review_date:
                review_date = pd.to_datetime(review_date).strftime("%Y-%m-%d")

            # Extract consumer info
            consumer = review_data.get("consumer", {})

            parsed = {
                'restaurant_id': restaurant_id,
                'review_date': review_date,
                'author_name': consumer.get("displayName", "Anonymous"),
                'review_title': review_data.get("title", ""),
                'review_body': review_data.get("text", ""),
                'rating': review_data.get("rating"),
                'author_location': consumer.get("countryCode", ""),
                'author_review_count': consumer.get("numberOfReviews", 0),
                'page_number': review_data.get('_page_number', 1),
                'scraped_at': datetime.now().isoformat(),
                'is_verified_purchase': 1 if review_data.get("isVerified") else 0,
                'reply_count': len(review_data.get("reply", [])) if review_data.get("reply") else 0,
                'helpful_count': review_data.get("likes", 0)
            }

            return parsed

        except Exception as e:
            logger.error(f"Error parsing review: {e}")
            return None

    def save_reviews_to_db(self, reviews: List[Dict]) -> int:
        """
        Save reviews to database with deduplication

        Args:
            reviews: List of parsed review dicts

        Returns:
            Number of new reviews inserted
        """
        if not reviews:
            return 0

        conn = self._get_connection()
        cursor = conn.cursor()

        inserted_count = 0

        for review in reviews:
            try:
                # Check if review already exists (deduplication)
                cursor.execute("""
                    SELECT review_id FROM trustpilot_reviews
                    WHERE restaurant_id = ?
                    AND review_date = ?
                    AND author_name = ?
                    AND review_body = ?
                """, (review['restaurant_id'], review['review_date'],
                      review['author_name'], review['review_body']))

                if cursor.fetchone():
                    logger.debug(f"Skipping duplicate review from {review['author_name']}")
                    continue

                # Insert new review
                cursor.execute("""
                    INSERT INTO trustpilot_reviews (
                        restaurant_id, review_date, author_name, review_title,
                        review_body, rating, author_location, author_review_count,
                        page_number, scraped_at, is_verified_purchase,
                        reply_count, helpful_count
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    review['restaurant_id'], review['review_date'], review['author_name'],
                    review['review_title'], review['review_body'], review['rating'],
                    review['author_location'], review['author_review_count'],
                    review['page_number'], review['scraped_at'], review['is_verified_purchase'],
                    review['reply_count'], review['helpful_count']
                ))

                inserted_count += 1

            except sqlite3.Error as e:
                logger.error(f"Database error inserting review: {e}")
                continue

        conn.commit()
        conn.close()

        logger.info(f"Inserted {inserted_count} new reviews (skipped {len(reviews) - inserted_count} duplicates)")
        return inserted_count

    def update_restaurant_metadata(self, restaurant_id: int):
        """
        Update restaurant's Trustpilot metadata after scraping

        Args:
            restaurant_id: Database ID of restaurant
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE restaurants
            SET trustpilot_last_scraped_at = ?
            WHERE restaurant_id = ?
        """, (datetime.now().isoformat(), restaurant_id))

        conn.commit()
        conn.close()

    def scrape_restaurant_reviews(self, restaurant_id: int, max_pages: int = 50,
                                   incremental: bool = False) -> Dict:
        """
        Scrape all reviews for a single restaurant

        Args:
            restaurant_id: Database ID of restaurant
            max_pages: Maximum number of pages to scrape
            incremental: If True, only fetch recent reviews since last scrape

        Returns:
            Dict with scraping statistics
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        # Get restaurant info
        cursor.execute("""
            SELECT restaurant_id, name, trustpilot_url, trustpilot_last_scraped_at
            FROM restaurants
            WHERE restaurant_id = ?
        """, (restaurant_id,))

        restaurant = cursor.fetchone()
        conn.close()

        if not restaurant:
            logger.error(f"Restaurant {restaurant_id} not found")
            return {'error': 'Restaurant not found'}

        if not restaurant['trustpilot_url']:
            logger.error(f"Restaurant {restaurant['name']} has no Trustpilot URL")
            return {'error': 'No Trustpilot URL'}

        logger.info(f"\n{'='*60}")
        logger.info(f"Scraping: {restaurant['name']}")
        logger.info(f"URL: {restaurant['trustpilot_url']}")
        logger.info(f"{'='*60}")

        all_reviews = []
        page_number = 1
        total_inserted = 0

        # For incremental updates, only fetch first few pages
        if incremental and restaurant['trustpilot_last_scraped_at']:
            max_pages = min(5, max_pages)  # Only check first 5 pages
            logger.info(f"Incremental mode: checking only first {max_pages} pages")

        while page_number <= max_pages:
            url = f"{restaurant['trustpilot_url']}?page={page_number}"

            reviews, pagination = self.get_reviews_from_page(url, page_number)

            if not reviews:
                logger.info(f"No more reviews found at page {page_number}")
                break

            # Parse reviews
            parsed_reviews = []
            for review in reviews:
                parsed = self.parse_review(review, restaurant_id)
                if parsed:
                    parsed_reviews.append(parsed)

            # Save to database
            inserted = self.save_reviews_to_db(parsed_reviews)
            total_inserted += inserted
            all_reviews.extend(parsed_reviews)

            # For incremental, stop if we're seeing old reviews
            if incremental and inserted == 0:
                logger.info("No new reviews found, stopping incremental update")
                break

            # Check if there are more pages
            if pagination:
                current_page = pagination.get("page", page_number)
                total_pages = pagination.get("totalPages", 0)
                logger.info(f"Progress: page {current_page}/{total_pages}")

                if current_page >= total_pages:
                    logger.info("Reached last page")
                    break

            page_number += 1

            # Rate limiting
            time.sleep(self.rate_limit)

        # Update restaurant metadata
        self.update_restaurant_metadata(restaurant_id)

        stats = {
            'restaurant_id': restaurant_id,
            'restaurant_name': restaurant['name'],
            'pages_scraped': page_number - 1,
            'reviews_found': len(all_reviews),
            'reviews_inserted': total_inserted,
            'reviews_duplicates': len(all_reviews) - total_inserted
        }

        logger.info(f"\n{'='*60}")
        logger.info(f"RESULTS for {restaurant['name']}:")
        logger.info(f"  Pages scraped: {stats['pages_scraped']}")
        logger.info(f"  Reviews found: {stats['reviews_found']}")
        logger.info(f"  New reviews inserted: {stats['reviews_inserted']}")
        logger.info(f"  Duplicates skipped: {stats['reviews_duplicates']}")
        logger.info(f"{'='*60}\n")

        return stats

    def scrape_all_restaurants(self, max_pages_per_restaurant: int = 50) -> List[Dict]:
        """
        Scrape reviews for all restaurants with Trustpilot URLs

        Args:
            max_pages_per_restaurant: Max pages to scrape per restaurant

        Returns:
            List of statistics dicts for each restaurant
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT restaurant_id, name, trustpilot_url
            FROM restaurants
            WHERE is_active = 1
            AND trustpilot_url IS NOT NULL
            AND trustpilot_url != ''
            ORDER BY name
        """)

        restaurants = cursor.fetchall()
        conn.close()

        logger.info(f"\n{'='*60}")
        logger.info(f"Found {len(restaurants)} restaurants with Trustpilot URLs")
        logger.info(f"{'='*60}\n")

        all_stats = []

        for i, restaurant in enumerate(restaurants, 1):
            logger.info(f"\n[{i}/{len(restaurants)}] Processing: {restaurant['name']}")

            stats = self.scrape_restaurant_reviews(
                restaurant['restaurant_id'],
                max_pages=max_pages_per_restaurant
            )
            all_stats.append(stats)

            # Longer pause between restaurants
            if i < len(restaurants):
                logger.info(f"Pausing 5 seconds before next restaurant...")
                time.sleep(5)

        return all_stats

    def incremental_update_all(self) -> List[Dict]:
        """
        Incremental update: fetch only new reviews for all restaurants

        Returns:
            List of statistics dicts for each restaurant
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        # Get restaurants scraped in last 30 days
        thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat()

        cursor.execute("""
            SELECT restaurant_id, name, trustpilot_url, trustpilot_last_scraped_at
            FROM restaurants
            WHERE is_active = 1
            AND trustpilot_url IS NOT NULL
            AND trustpilot_url != ''
            AND trustpilot_last_scraped_at >= ?
            ORDER BY trustpilot_last_scraped_at ASC
        """, (thirty_days_ago,))

        restaurants = cursor.fetchall()
        conn.close()

        logger.info(f"\n{'='*60}")
        logger.info(f"Incremental update for {len(restaurants)} restaurants")
        logger.info(f"{'='*60}\n")

        all_stats = []

        for i, restaurant in enumerate(restaurants, 1):
            logger.info(f"\n[{i}/{len(restaurants)}] Updating: {restaurant['name']}")

            stats = self.scrape_restaurant_reviews(
                restaurant['restaurant_id'],
                max_pages=5,  # Only check first 5 pages
                incremental=True
            )
            all_stats.append(stats)

            if i < len(restaurants):
                time.sleep(3)

        return all_stats


def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(
        description='Scrape Trustpilot reviews for Plymouth restaurants'
    )
    parser.add_argument('--all', action='store_true',
                        help='Scrape all restaurants with Trustpilot URLs')
    parser.add_argument('--update', action='store_true',
                        help='Incremental update: only fetch new reviews')
    parser.add_argument('--restaurant-id', type=int,
                        help='Scrape specific restaurant by ID')
    parser.add_argument('--test', action='store_true',
                        help='Test mode: scrape first restaurant only')
    parser.add_argument('--max-pages', type=int, default=50,
                        help='Maximum pages per restaurant (default: 50)')
    parser.add_argument('--db', type=str, default='plymouth_research.db',
                        help='Database path (default: plymouth_research.db)')
    parser.add_argument('--rate-limit', type=float, default=2.5,
                        help='Seconds between requests (default: 2.5)')

    args = parser.parse_args()

    scraper = TrustpilotRestaurantScraper(
        db_path=args.db,
        rate_limit=args.rate_limit
    )

    if args.test:
        # Test with first restaurant
        conn = scraper._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT restaurant_id FROM restaurants
            WHERE trustpilot_url IS NOT NULL
            LIMIT 1
        """)
        result = cursor.fetchone()
        conn.close()

        if result:
            stats = scraper.scrape_restaurant_reviews(result['restaurant_id'], max_pages=3)
            print(json.dumps(stats, indent=2))
        else:
            print("No restaurants with Trustpilot URLs found")

    elif args.restaurant_id:
        stats = scraper.scrape_restaurant_reviews(args.restaurant_id, max_pages=args.max_pages)
        print(json.dumps(stats, indent=2))

    elif args.update:
        all_stats = scraper.incremental_update_all()
        print(f"\nProcessed {len(all_stats)} restaurants")
        print(json.dumps(all_stats, indent=2))

    elif args.all:
        all_stats = scraper.scrape_all_restaurants(max_pages_per_restaurant=args.max_pages)
        print(f"\nProcessed {len(all_stats)} restaurants")
        print(json.dumps(all_stats, indent=2))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
