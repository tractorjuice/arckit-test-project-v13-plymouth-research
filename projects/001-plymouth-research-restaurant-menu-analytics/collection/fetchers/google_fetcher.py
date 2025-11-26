"""
Google Places API Fetcher
=========================

Fetches restaurant data and reviews from Google Places API.

Data Source: Google Places API
URL: https://places.googleapis.com/v1
License: Google API Terms of Service

API Costs (as of 2025):
- Find Place: $17 per 1,000 requests
- Place Details: $17 per 1,000 requests
- Free tier: $200 credit/month (~11,700 requests)

Author: Plymouth Research Team
Date: 2025-11-26
"""

import logging
import os
import time
from pathlib import Path
from typing import Optional, Dict, List, Any
from datetime import datetime

import requests

from .base_fetcher import BaseFetcher

logger = logging.getLogger(__name__)


class GooglePlacesFetcher(BaseFetcher):
    """
    Fetcher for Google Places API data.

    Retrieves:
    - Place ID lookup by restaurant name/address
    - Place details (ratings, contact info, hours)
    - Reviews (up to 5 per place)
    - Service options (dine-in, takeout, delivery)
    """

    BASE_URL = "https://places.googleapis.com/v1"
    REQUEST_DELAY = 0.2  # 200ms between requests to avoid rate limits

    # Fields to request from Places API (New)
    PLACE_FIELDS = [
        "id",
        "displayName",
        "rating",
        "userRatingCount",
        "priceLevel",
        "formattedAddress",
        "nationalPhoneNumber",
        "internationalPhoneNumber",
        "websiteUri",
        "googleMapsUri",
        "location",
        "businessStatus",
        "dineIn",
        "takeout",
        "delivery",
        "reservable",
        "servesBreakfast",
        "servesLunch",
        "servesDinner",
        "servesBeer",
        "servesWine",
        "servesVegetarianFood",
        "reviews",
    ]

    def __init__(self, db_path: Optional[Path] = None, api_key: Optional[str] = None):
        """
        Initialize Google Places fetcher.

        Args:
            db_path: Path to SQLite database
            api_key: Google Places API key (or from GOOGLE_PLACES_API_KEY env)
        """
        super().__init__(db_path)

        self.api_key = api_key or os.environ.get('GOOGLE_PLACES_API_KEY')
        if not self.api_key:
            logger.warning("No Google Places API key found. Set GOOGLE_PLACES_API_KEY environment variable.")

        self.session = requests.Session()

    def fetch(self, restaurant_id: Optional[int] = None, **kwargs) -> List[Dict[str, Any]]:
        """
        Fetch Google Places data for restaurants.

        Args:
            restaurant_id: Specific restaurant ID (None for all without Google data)

        Returns:
            List of place detail dictionaries
        """
        if not self.api_key:
            raise ValueError("Google Places API key required")

        restaurants = self._get_restaurants_needing_google_data(restaurant_id)
        logger.info(f"Fetching Google data for {len(restaurants)} restaurants")

        results = []

        for i, restaurant in enumerate(restaurants):
            rest_id = restaurant['restaurant_id']
            name = restaurant['name']
            address = restaurant.get('address', '')

            logger.info(f"[{i+1}/{len(restaurants)}] Looking up: {name}")

            try:
                # Step 1: Find Place ID
                place_id = self._find_place_id(name, address)

                if not place_id:
                    logger.warning(f"  No place found for: {name}")
                    continue

                # Step 2: Get Place Details
                details = self._get_place_details(place_id)

                if details:
                    details['restaurant_id'] = rest_id
                    results.append(details)
                    logger.info(f"  Found: {details.get('displayName', {}).get('text', 'Unknown')}")

                time.sleep(self.REQUEST_DELAY)

            except Exception as e:
                logger.error(f"  Error: {e}")
                self.stats["errors"] += 1

        return results

    def process(self, data: List[Dict[str, Any]]) -> int:
        """
        Store Google Places data in database.

        Args:
            data: List of place detail dictionaries

        Returns:
            Number of restaurants updated
        """
        updated = 0

        for place in data:
            try:
                updates = self._build_updates(place)
                restaurant_id = place['restaurant_id']

                if self.update_restaurant(restaurant_id, updates):
                    # Store reviews
                    reviews = place.get('reviews', [])
                    if reviews:
                        self._store_reviews(restaurant_id, reviews)

                    updated += 1

            except Exception as e:
                logger.error(f"Error processing place data: {e}")
                self.stats["errors"] += 1

        logger.info(f"Updated {updated} restaurants with Google data")
        return updated

    def _get_restaurants_needing_google_data(self, restaurant_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get restaurants that need Google Places data."""
        query = """
            SELECT restaurant_id, name, address
            FROM restaurants
            WHERE is_active = 1
        """
        params = []

        if restaurant_id:
            query += " AND restaurant_id = ?"
            params.append(restaurant_id)
        else:
            # Only fetch for restaurants without Google data
            query += " AND google_place_id IS NULL"

        query += " ORDER BY name"

        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

    def _find_place_id(self, name: str, address: str = "") -> Optional[str]:
        """
        Find Google Place ID by restaurant name and address.

        Args:
            name: Restaurant name
            address: Restaurant address (optional)

        Returns:
            Google Place ID or None
        """
        search_text = f"{name} Plymouth UK"
        if address:
            search_text = f"{name} {address}"

        url = f"{self.BASE_URL}/places:searchText"
        headers = {
            "X-Goog-Api-Key": self.api_key,
            "X-Goog-FieldMask": "places.id,places.displayName",
            "Content-Type": "application/json",
        }
        payload = {
            "textQuery": search_text,
            "maxResultCount": 1,
        }

        response = self.session.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()

        data = response.json()
        places = data.get('places', [])

        if places:
            return places[0].get('id')

        return None

    def _get_place_details(self, place_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed place information.

        Args:
            place_id: Google Place ID

        Returns:
            Place details dictionary
        """
        url = f"{self.BASE_URL}/places/{place_id}"
        headers = {
            "X-Goog-Api-Key": self.api_key,
            "X-Goog-FieldMask": ",".join(self.PLACE_FIELDS),
        }

        response = self.session.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        return response.json()

    def _build_updates(self, place: Dict[str, Any]) -> Dict[str, Any]:
        """Build database update dictionary from place data."""
        updates = {
            'google_place_id': place.get('id'),
            'google_rating': place.get('rating'),
            'google_user_ratings_total': place.get('userRatingCount'),
            'google_price_level': place.get('priceLevel'),
            'google_formatted_address': place.get('formattedAddress'),
            'google_phone_national': place.get('nationalPhoneNumber'),
            'google_phone_international': place.get('internationalPhoneNumber'),
            'google_website_url': place.get('websiteUri'),
            'google_maps_url': place.get('googleMapsUri'),
            'google_business_status': place.get('businessStatus'),
            'google_last_fetched_at': datetime.now().isoformat(),
        }

        # Location
        location = place.get('location', {})
        if location:
            updates['google_latitude'] = location.get('latitude')
            updates['google_longitude'] = location.get('longitude')

        # Service options (booleans)
        updates['google_dine_in'] = 1 if place.get('dineIn') else 0
        updates['google_takeout'] = 1 if place.get('takeout') else 0
        updates['google_delivery'] = 1 if place.get('delivery') else 0
        updates['google_reservable'] = 1 if place.get('reservable') else 0
        updates['google_serves_breakfast'] = 1 if place.get('servesBreakfast') else 0
        updates['google_serves_lunch'] = 1 if place.get('servesLunch') else 0
        updates['google_serves_dinner'] = 1 if place.get('servesDinner') else 0
        updates['google_serves_beer'] = 1 if place.get('servesBeer') else 0
        updates['google_serves_wine'] = 1 if place.get('servesWine') else 0
        updates['google_serves_vegetarian'] = 1 if place.get('servesVegetarianFood') else 0

        return updates

    def _store_reviews(self, restaurant_id: int, reviews: List[Dict[str, Any]]):
        """Store Google reviews in database."""
        cursor = self.conn.cursor()

        for review in reviews:
            try:
                # Check for duplicate
                author_name = review.get('authorAttribution', {}).get('displayName', 'Anonymous')
                review_date = review.get('publishTime', '')[:10]  # Just date part

                cursor.execute(
                    "SELECT review_id FROM google_reviews WHERE restaurant_id = ? AND author_name = ? AND review_date = ?",
                    (restaurant_id, author_name, review_date)
                )

                if cursor.fetchone():
                    continue

                # Insert review
                cursor.execute("""
                    INSERT INTO google_reviews (
                        restaurant_id, review_date, author_name, review_text,
                        rating, google_author_url, google_profile_photo_url,
                        language, relative_time_description
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    restaurant_id,
                    review_date,
                    author_name,
                    review.get('text', {}).get('text', ''),
                    review.get('rating'),
                    review.get('authorAttribution', {}).get('uri'),
                    review.get('authorAttribution', {}).get('photoUri'),
                    review.get('text', {}).get('languageCode', 'en'),
                    review.get('relativePublishTimeDescription', ''),
                ))

            except Exception as e:
                logger.error(f"Error storing Google review: {e}")

        self.conn.commit()


# ============================================================================
# CLI Entry Point
# ============================================================================

if __name__ == "__main__":
    import argparse

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    parser = argparse.ArgumentParser(description="Fetch Google Places data")
    parser.add_argument('--restaurant-id', type=int, help="Specific restaurant ID")
    parser.add_argument('--db', type=str, help="Path to database file")

    args = parser.parse_args()

    fetcher = GooglePlacesFetcher(
        db_path=Path(args.db) if args.db else None,
    )

    stats = fetcher.run(restaurant_id=args.restaurant_id)

    print(f"\nResults:")
    print(f"  Fetched: {stats['fetched']}")
    print(f"  Updated: {stats['matched']}")
    print(f"  Errors: {stats['errors']}")
