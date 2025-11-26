"""
Trustpilot Review Fetcher
=========================

Fetches reviews from Trustpilot for matched restaurants.

Data Source: Trustpilot.com (public reviews)
Method: Web scraping (__NEXT_DATA__ JSON extraction)
License: Public data for analytics (non-commercial, internal use)

Author: Plymouth Research Team
Date: 2025-11-26
"""

import logging
import json
import time
import re
from pathlib import Path
from typing import Optional, Dict, List, Any
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from .base_fetcher import BaseFetcher

logger = logging.getLogger(__name__)


class TrustpilotFetcher(BaseFetcher):
    """
    Fetcher for Trustpilot reviews.

    Scrapes Trustpilot's __NEXT_DATA__ JSON structure to extract
    reviews with rate limiting and incremental updates.
    """

    # Rate limiting
    PAGE_DELAY = 2.5  # Seconds between page requests
    RESTAURANT_DELAY = 5.0  # Seconds between restaurants

    # Request settings
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    MAX_PAGES = 50  # Maximum pages to fetch per restaurant

    def __init__(self, db_path: Optional[Path] = None):
        """
        Initialize Trustpilot fetcher.

        Args:
            db_path: Path to SQLite database
        """
        super().__init__(db_path)
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.USER_AGENT})

    def fetch(self, restaurant_id: Optional[int] = None, max_pages: int = None, **kwargs) -> List[Dict[str, Any]]:
        """
        Fetch Trustpilot reviews for restaurants.

        Args:
            restaurant_id: Specific restaurant ID (None for all)
            max_pages: Maximum pages per restaurant (default: MAX_PAGES)

        Returns:
            List of review dictionaries
        """
        if max_pages is None:
            max_pages = self.MAX_PAGES

        # Get restaurants with Trustpilot URLs
        restaurants = self._get_restaurants_with_trustpilot(restaurant_id)
        logger.info(f"Found {len(restaurants)} restaurants with Trustpilot URLs")

        all_reviews = []

        for i, restaurant in enumerate(restaurants):
            rest_id = restaurant['restaurant_id']
            url = restaurant['trustpilot_url']

            logger.info(f"[{i+1}/{len(restaurants)}] Fetching reviews for: {restaurant['name']}")

            try:
                reviews = self._fetch_restaurant_reviews(rest_id, url, max_pages)
                all_reviews.extend(reviews)
                logger.info(f"  Fetched {len(reviews)} reviews")

            except Exception as e:
                logger.error(f"  Error fetching reviews: {e}")
                self.stats["errors"] += 1

            # Rate limiting between restaurants
            if i < len(restaurants) - 1:
                time.sleep(self.RESTAURANT_DELAY)

        return all_reviews

    def process(self, data: List[Dict[str, Any]]) -> int:
        """
        Store reviews in database.

        Args:
            data: List of review dictionaries

        Returns:
            Number of reviews stored
        """
        if not data:
            return 0

        cursor = self.conn.cursor()
        stored = 0

        for review in data:
            try:
                # Check if review already exists
                cursor.execute(
                    "SELECT review_id FROM trustpilot_reviews WHERE restaurant_id = ? AND review_date = ? AND author_name = ?",
                    (review['restaurant_id'], review['review_date'], review['author_name'])
                )

                if cursor.fetchone():
                    continue  # Skip duplicate

                # Insert new review
                cursor.execute("""
                    INSERT INTO trustpilot_reviews (
                        restaurant_id, review_date, author_name, review_title,
                        review_body, rating, author_location, author_review_count,
                        page_number, scraped_at, is_verified_purchase, reply_count,
                        helpful_count
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    review['restaurant_id'],
                    review['review_date'],
                    review['author_name'],
                    review.get('review_title'),
                    review.get('review_body'),
                    review['rating'],
                    review.get('author_location'),
                    review.get('author_review_count', 0),
                    review.get('page_number', 1),
                    datetime.now().isoformat(),
                    review.get('is_verified_purchase', 0),
                    review.get('reply_count', 0),
                    review.get('helpful_count', 0),
                ))
                stored += 1

            except Exception as e:
                logger.error(f"Error storing review: {e}")
                self.stats["errors"] += 1

        self.conn.commit()

        # Update restaurant review counts
        self._update_restaurant_counts()

        logger.info(f"Stored {stored} new reviews")
        return stored

    def _get_restaurants_with_trustpilot(self, restaurant_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get restaurants that have Trustpilot URLs."""
        query = """
            SELECT restaurant_id, name, trustpilot_url
            FROM restaurants
            WHERE trustpilot_url IS NOT NULL
              AND trustpilot_url != ''
              AND is_active = 1
        """
        params = []

        if restaurant_id:
            query += " AND restaurant_id = ?"
            params.append(restaurant_id)

        query += " ORDER BY name"

        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

    def _fetch_restaurant_reviews(
        self,
        restaurant_id: int,
        trustpilot_url: str,
        max_pages: int
    ) -> List[Dict[str, Any]]:
        """
        Fetch all reviews for a single restaurant.

        Args:
            restaurant_id: Database restaurant ID
            trustpilot_url: Trustpilot page URL
            max_pages: Maximum pages to fetch

        Returns:
            List of review dictionaries
        """
        reviews = []

        for page_num in range(1, max_pages + 1):
            page_url = f"{trustpilot_url}?page={page_num}"

            try:
                page_reviews = self._fetch_page(restaurant_id, page_url, page_num)

                if not page_reviews:
                    logger.debug(f"  No more reviews at page {page_num}")
                    break

                reviews.extend(page_reviews)
                logger.debug(f"  Page {page_num}: {len(page_reviews)} reviews")

                # Rate limiting between pages
                time.sleep(self.PAGE_DELAY)

            except Exception as e:
                logger.error(f"  Error on page {page_num}: {e}")
                break

        return reviews

    def _fetch_page(
        self,
        restaurant_id: int,
        url: str,
        page_num: int
    ) -> List[Dict[str, Any]]:
        """
        Fetch reviews from a single Trustpilot page.

        Args:
            restaurant_id: Database restaurant ID
            url: Page URL
            page_num: Page number

        Returns:
            List of review dictionaries
        """
        response = self.session.get(url, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find __NEXT_DATA__ script tag
        script = soup.find('script', id='__NEXT_DATA__')
        if not script:
            logger.warning(f"No __NEXT_DATA__ found on page: {url}")
            return []

        try:
            data = json.loads(script.string)
            reviews_data = self._extract_reviews_from_json(data)
        except json.JSONDecodeError as e:
            logger.error(f"JSON parse error: {e}")
            return []

        # Convert to our format
        reviews = []
        for r in reviews_data:
            review = {
                'restaurant_id': restaurant_id,
                'review_date': r.get('dates', {}).get('publishedDate', r.get('createdAt', '')),
                'author_name': r.get('consumer', {}).get('displayName', 'Anonymous'),
                'review_title': r.get('title', ''),
                'review_body': r.get('text', ''),
                'rating': r.get('rating', 0),
                'author_location': r.get('consumer', {}).get('countryCode', ''),
                'author_review_count': r.get('consumer', {}).get('numberOfReviews', 0),
                'page_number': page_num,
                'is_verified_purchase': 1 if r.get('labels', {}).get('verification', {}).get('isVerified') else 0,
                'reply_count': len(r.get('reply', {}).get('message', '') or ''),
                'helpful_count': r.get('likes', 0),
            }
            reviews.append(review)

        return reviews

    def _extract_reviews_from_json(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract reviews array from __NEXT_DATA__ JSON structure."""
        try:
            # Navigate Trustpilot's nested structure
            page_props = data.get('props', {}).get('pageProps', {})
            reviews = page_props.get('reviews', [])
            return reviews
        except Exception as e:
            logger.error(f"Error extracting reviews from JSON: {e}")
            return []

    def _update_restaurant_counts(self):
        """Update restaurant review counts and averages."""
        cursor = self.conn.cursor()

        # Update counts
        cursor.execute("""
            UPDATE restaurants
            SET trustpilot_review_count = (
                SELECT COUNT(*) FROM trustpilot_reviews
                WHERE trustpilot_reviews.restaurant_id = restaurants.restaurant_id
            ),
            trustpilot_avg_rating = (
                SELECT AVG(rating) FROM trustpilot_reviews
                WHERE trustpilot_reviews.restaurant_id = restaurants.restaurant_id
            ),
            trustpilot_last_scraped_at = ?
            WHERE trustpilot_url IS NOT NULL
        """, (datetime.now().isoformat(),))

        self.conn.commit()
        logger.info("Updated restaurant review counts and averages")


# ============================================================================
# CLI Entry Point
# ============================================================================

if __name__ == "__main__":
    import argparse

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    parser = argparse.ArgumentParser(description="Fetch Trustpilot reviews")
    parser.add_argument('--restaurant-id', type=int, help="Specific restaurant ID")
    parser.add_argument('--max-pages', type=int, default=50, help="Max pages per restaurant")
    parser.add_argument('--db', type=str, help="Path to database file")

    args = parser.parse_args()

    fetcher = TrustpilotFetcher(
        db_path=Path(args.db) if args.db else None,
    )

    stats = fetcher.run(
        restaurant_id=args.restaurant_id,
        max_pages=args.max_pages,
    )

    print(f"\nResults:")
    print(f"  Fetched: {stats['fetched']}")
    print(f"  Stored: {stats['matched']}")
    print(f"  Errors: {stats['errors']}")
