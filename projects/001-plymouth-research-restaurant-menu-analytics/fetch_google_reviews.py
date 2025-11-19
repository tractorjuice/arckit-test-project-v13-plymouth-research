#!/usr/bin/env python3
"""
Google Reviews Fetcher for Plymouth Research Restaurant Menu Analytics

This script uses the official Google Places API to fetch reviews for restaurants.

Setup:
1. Get a Google Cloud API key:
   - Go to https://console.cloud.google.com/
   - Create a new project (or use existing)
   - Enable "Places API (New)"
   - Create credentials (API Key)
   - Restrict the key to Places API for security

2. Set environment variable:
   export GOOGLE_PLACES_API_KEY="your-api-key-here"

   OR create a .env file:
   GOOGLE_PLACES_API_KEY=your-api-key-here

Usage:
    # Fetch reviews for a specific restaurant
    python fetch_google_reviews.py --restaurant-id 4

    # Fetch for all restaurants
    python fetch_google_reviews.py --all

    # Test with first 5 restaurants
    python fetch_google_reviews.py --test

    # Incremental update (only restaurants without Google data)
    python fetch_google_reviews.py --update

API Costs:
- Find Place: $17 per 1,000 requests
- Place Details: $17 per 1,000 requests
- Free tier: $200 credit/month (~ 11,700 requests)
- For 98 restaurants: ~200 requests total (~$3.40 one-time)

Author: Claude Code
Date: 2025-11-19
"""

import sqlite3
import requests
import logging
import argparse
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import os
from urllib.parse import quote_plus

# Try to load dotenv for .env file support
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Database configuration
DB_PATH = 'plymouth_research.db'

# Google Places API configuration
GOOGLE_API_KEY = os.getenv('GOOGLE_PLACES_API_KEY')
PLACES_API_BASE = 'https://places.googleapis.com/v1'


class GooglePlacesReviewFetcher:
    """Fetches restaurant reviews from Google Places API"""

    def __init__(self, api_key: str = None, db_path: str = DB_PATH):
        """
        Initialize the fetcher

        Args:
            api_key: Google Places API key (falls back to env var)
            db_path: Path to SQLite database
        """
        self.api_key = api_key or GOOGLE_API_KEY
        if not self.api_key:
            raise ValueError(
                "Google Places API key is required. "
                "Set GOOGLE_PLACES_API_KEY environment variable or pass api_key parameter. "
                "Get key at: https://console.cloud.google.com/"
            )

        self.db_path = db_path
        self.session = requests.Session()
        self.session.headers.update({
            'X-Goog-Api-Key': self.api_key,
            'X-Goog-FieldMask': '*'  # Request all fields
        })

    def search_place(self, restaurant_name: str, address: str = None) -> Optional[str]:
        """
        Search for a place using Google Places Text Search

        Args:
            restaurant_name: Name of the restaurant
            address: Optional address for better accuracy

        Returns:
            place_id if found, None otherwise
        """
        # Build search query
        query = f"{restaurant_name} Plymouth UK"
        if address:
            query += f" {address}"

        url = f"{PLACES_API_BASE}/places:searchText"
        payload = {
            "textQuery": query,
            "maxResultCount": 1  # We only want the best match
        }

        try:
            response = self.session.post(url, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()

            if 'places' in data and len(data['places']) > 0:
                place = data['places'][0]
                place_id = place.get('id')
                display_name = place.get('displayName', {}).get('text', 'Unknown')

                logger.info(f"Found place: {display_name} (ID: {place_id})")
                return place_id
            else:
                logger.warning(f"No place found for: {restaurant_name}")
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Error searching for place '{restaurant_name}': {e}")
            return None

    def get_place_details(self, place_id: str) -> Optional[Dict]:
        """
        Get place details including reviews

        Args:
            place_id: Google Places ID

        Returns:
            Dictionary with place data or None
        """
        url = f"{PLACES_API_BASE}/places/{place_id}"

        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            return {
                'place_id': place_id,
                'rating': data.get('rating'),
                'user_ratings_total': data.get('userRatingCount', 0),
                'price_level': data.get('priceLevel'),
                'reviews': data.get('reviews', [])
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching place details for {place_id}: {e}")
            return None

    def parse_review(self, review_data: Dict, restaurant_id: int) -> Dict:
        """
        Parse a single review from Google Places API response

        Args:
            review_data: Raw review data from API
            restaurant_id: Database ID of the restaurant

        Returns:
            Parsed review dictionary
        """
        # Convert Unix timestamp to ISO8601
        publish_time = review_data.get('publishTime', '')
        try:
            if 'T' in publish_time:  # Already ISO format
                review_date = publish_time.split('T')[0]
            else:  # Unix timestamp
                dt = datetime.fromtimestamp(int(publish_time))
                review_date = dt.strftime('%Y-%m-%d')
        except:
            review_date = datetime.now().strftime('%Y-%m-%d')

        return {
            'restaurant_id': restaurant_id,
            'review_date': review_date,
            'author_name': review_data.get('authorAttribution', {}).get('displayName', 'Anonymous'),
            'review_text': review_data.get('text', {}).get('text', ''),
            'rating': review_data.get('rating', 0),
            'google_author_url': review_data.get('authorAttribution', {}).get('uri', ''),
            'google_profile_photo_url': review_data.get('authorAttribution', {}).get('photoUri', ''),
            'language': 'en',  # Google doesn't provide this in new API
            'relative_time_description': review_data.get('relativePublishTimeDescription', ''),
            'fetched_at': datetime.now().isoformat()
        }

    def save_reviews_to_db(self, reviews: List[Dict]) -> Tuple[int, int]:
        """
        Save reviews to database with deduplication

        Args:
            reviews: List of parsed review dictionaries

        Returns:
            Tuple of (inserted_count, duplicate_count)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        inserted = 0
        duplicates = 0

        for review in reviews:
            try:
                # Check for existing review
                cursor.execute("""
                    SELECT review_id FROM google_reviews
                    WHERE restaurant_id = ?
                    AND author_name = ?
                    AND review_date = ?
                    AND review_text = ?
                """, (
                    review['restaurant_id'],
                    review['author_name'],
                    review['review_date'],
                    review['review_text']
                ))

                if cursor.fetchone():
                    duplicates += 1
                    continue

                # Insert new review
                cursor.execute("""
                    INSERT INTO google_reviews (
                        restaurant_id, review_date, author_name, review_text, rating,
                        google_author_url, google_profile_photo_url,
                        language, relative_time_description, fetched_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    review['restaurant_id'],
                    review['review_date'],
                    review['author_name'],
                    review['review_text'],
                    review['rating'],
                    review['google_author_url'],
                    review['google_profile_photo_url'],
                    review['language'],
                    review['relative_time_description'],
                    review['fetched_at']
                ))
                inserted += 1

            except sqlite3.Error as e:
                logger.error(f"Database error inserting review: {e}")
                continue

        conn.commit()
        conn.close()

        return (inserted, duplicates)

    def update_restaurant_metadata(self, restaurant_id: int, place_data: Dict):
        """
        Update restaurant table with Google Places metadata

        Args:
            restaurant_id: Database ID of restaurant
            place_data: Dictionary with Google Places data
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE restaurants
            SET
                google_place_id = ?,
                google_rating = ?,
                google_user_ratings_total = ?,
                google_price_level = ?,
                google_last_fetched_at = ?
            WHERE restaurant_id = ?
        """, (
            place_data.get('place_id'),
            place_data.get('rating'),
            place_data.get('user_ratings_total', 0),
            place_data.get('price_level'),
            datetime.now().isoformat(),
            restaurant_id
        ))

        conn.commit()
        conn.close()

    def fetch_restaurant_reviews(self, restaurant_id: int) -> Dict:
        """
        Fetch reviews for a single restaurant

        Args:
            restaurant_id: Database ID of the restaurant

        Returns:
            Dictionary with statistics about the fetch
        """
        # Get restaurant info from database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT name, address, google_place_id
            FROM restaurants
            WHERE restaurant_id = ?
        """, (restaurant_id,))

        row = cursor.fetchone()
        conn.close()

        if not row:
            logger.error(f"Restaurant ID {restaurant_id} not found in database")
            return {'error': 'Restaurant not found'}

        name, address, existing_place_id = row

        logger.info(f"\n{'='*60}")
        logger.info(f"Fetching Google reviews for: {name}")
        logger.info(f"{'='*60}")

        # Step 1: Get or search for place_id
        place_id = existing_place_id
        if not place_id:
            logger.info(f"Searching for place...")
            place_id = self.search_place(name, address)
            if not place_id:
                logger.warning(f"Could not find Google Place for {name}")
                return {
                    'restaurant_id': restaurant_id,
                    'restaurant_name': name,
                    'reviews_inserted': 0,
                    'reviews_duplicates': 0,
                    'error': 'Place not found'
                }
            time.sleep(0.5)  # Rate limiting

        # Step 2: Get place details and reviews
        logger.info(f"Fetching place details and reviews...")
        place_data = self.get_place_details(place_id)
        if not place_data:
            return {
                'restaurant_id': restaurant_id,
                'restaurant_name': name,
                'reviews_inserted': 0,
                'reviews_duplicates': 0,
                'error': 'Could not fetch place details'
            }

        # Step 3: Update restaurant metadata
        self.update_restaurant_metadata(restaurant_id, place_data)
        logger.info(f"Google Rating: {place_data.get('rating', 'N/A')}/5")
        logger.info(f"Total user ratings: {place_data.get('user_ratings_total', 0)}")

        # Step 4: Parse and save reviews
        reviews = place_data.get('reviews', [])
        logger.info(f"Found {len(reviews)} reviews to process")

        if reviews:
            parsed_reviews = [self.parse_review(r, restaurant_id) for r in reviews]
            inserted, duplicates = self.save_reviews_to_db(parsed_reviews)

            logger.info(f"Inserted {inserted} new reviews (skipped {duplicates} duplicates)")
        else:
            inserted, duplicates = 0, 0
            logger.info("No reviews available for this place")

        logger.info(f"{'='*60}\n")

        return {
            'restaurant_id': restaurant_id,
            'restaurant_name': name,
            'place_id': place_id,
            'google_rating': place_data.get('rating'),
            'total_ratings': place_data.get('user_ratings_total', 0),
            'reviews_found': len(reviews),
            'reviews_inserted': inserted,
            'reviews_duplicates': duplicates
        }


def main():
    parser = argparse.ArgumentParser(
        description='Fetch Google Reviews for Plymouth restaurants',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Fetch reviews for restaurant ID 4
  python fetch_google_reviews.py --restaurant-id 4

  # Fetch for all restaurants
  python fetch_google_reviews.py --all

  # Test with first 5 restaurants
  python fetch_google_reviews.py --test

  # Update (only restaurants without Google data)
  python fetch_google_reviews.py --update

Environment:
  Requires GOOGLE_PLACES_API_KEY environment variable.
  Get API key at: https://console.cloud.google.com/
        """
    )

    parser.add_argument('--restaurant-id', type=int, help='Specific restaurant ID to fetch')
    parser.add_argument('--all', action='store_true', help='Fetch all restaurants')
    parser.add_argument('--test', action='store_true', help='Test mode (first 5 restaurants)')
    parser.add_argument('--update', action='store_true', help='Incremental update (only new restaurants)')

    args = parser.parse_args()

    # Validate API key
    if not GOOGLE_API_KEY:
        logger.error("GOOGLE_PLACES_API_KEY environment variable is not set!")
        logger.error("Get API key at: https://console.cloud.google.com/")
        logger.error("Then set it: export GOOGLE_PLACES_API_KEY='your-key-here'")
        sys.exit(1)

    try:
        fetcher = GooglePlacesReviewFetcher()

        # Get list of restaurants to process
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        if args.restaurant_id:
            restaurant_ids = [args.restaurant_id]
        elif args.test:
            cursor.execute("SELECT restaurant_id FROM restaurants WHERE is_active = 1 LIMIT 5")
            restaurant_ids = [row[0] for row in cursor.fetchall()]
        elif args.update:
            cursor.execute("SELECT restaurant_id FROM restaurants WHERE is_active = 1 AND google_place_id IS NULL")
            restaurant_ids = [row[0] for row in cursor.fetchall()]
        elif args.all:
            cursor.execute("SELECT restaurant_id FROM restaurants WHERE is_active = 1")
            restaurant_ids = [row[0] for row in cursor.fetchall()]
        else:
            parser.print_help()
            sys.exit(0)

        conn.close()

        logger.info(f"\n{'='*60}")
        logger.info(f"PROCESSING {len(restaurant_ids)} RESTAURANTS")
        logger.info(f"{'='*60}\n")

        all_stats = []
        for i, restaurant_id in enumerate(restaurant_ids, 1):
            logger.info(f"[{i}/{len(restaurant_ids)}] Processing restaurant ID {restaurant_id}")
            stats = fetcher.fetch_restaurant_reviews(restaurant_id)
            all_stats.append(stats)

            # Rate limiting between restaurants (Google recommends < 100 QPS)
            if i < len(restaurant_ids):
                time.sleep(1.0)  # 1 second between restaurants

        # Final summary
        logger.info(f"\n{'='*60}")
        logger.info(f"FINAL SUMMARY")
        logger.info(f"{'='*60}")

        successful = [s for s in all_stats if 'error' not in s]
        failed = [s for s in all_stats if 'error' in s]

        logger.info(f"Restaurants processed: {len(restaurant_ids)}")
        logger.info(f"Successful: {len(successful)}")
        logger.info(f"Failed: {len(failed)}")

        if successful:
            total_reviews = sum(s['reviews_inserted'] for s in successful)
            total_ratings = sum(s.get('total_ratings', 0) for s in successful)
            avg_rating = sum(s.get('google_rating', 0) for s in successful if s.get('google_rating')) / len([s for s in successful if s.get('google_rating')])

            logger.info(f"Total new reviews inserted: {total_reviews}")
            logger.info(f"Total ratings on Google: {total_ratings}")
            logger.info(f"Average Google rating: {avg_rating:.2f}/5")

        if failed:
            logger.warning(f"\nFailed restaurants:")
            for s in failed:
                logger.warning(f"  - {s.get('restaurant_name', 'Unknown')}: {s.get('error')}")

        logger.info(f"{'='*60}\n")

        # Note about API limitations
        logger.info("NOTE: Google Places API only returns up to 5 most recent reviews per location.")
        logger.info("This is an API limitation. Use Trustpilot for more comprehensive review history.")

    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
