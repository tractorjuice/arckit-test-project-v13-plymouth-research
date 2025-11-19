#!/usr/bin/env python3
"""
Google Places Restaurant Discovery Script for Plymouth Research

This script uses the Google Places API to discover all restaurants in Plymouth, UK
and add them to the database.

Features:
- Text search for "restaurants in Plymouth UK"
- Pagination to get all results (up to 60 per search)
- Multiple search strategies (general, by cuisine type)
- Automatic deduplication using Google Place ID
- Extracts comprehensive restaurant data

Setup:
1. Set GOOGLE_PLACES_API_KEY environment variable
   export GOOGLE_PLACES_API_KEY="your-api-key-here"

Usage:
    # Discover all restaurants (general search)
    python discover_restaurants_google.py --discover-all

    # Discover by cuisine types (more comprehensive)
    python discover_restaurants_google.py --discover-by-cuisine

    # Dry run (show what would be added without adding)
    python discover_restaurants_google.py --discover-all --dry-run

API Costs:
- Text Search: $32 per 1,000 requests
- Pagination: Each page is a separate request
- Estimate: 5-10 requests for comprehensive discovery (~$0.32)

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
from typing import Dict, List, Optional
import os

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

# Plymouth center coordinates
PLYMOUTH_LAT = 50.3755
PLYMOUTH_LNG = -4.1427


class RestaurantDiscovery:
    """Discovers restaurants in Plymouth using Google Places API"""

    def __init__(self, api_key: str = None, db_path: str = DB_PATH):
        """
        Initialize the discovery tool

        Args:
            api_key: Google Places API key (falls back to env var)
            db_path: Path to SQLite database
        """
        self.api_key = api_key or GOOGLE_API_KEY
        if not self.api_key:
            raise ValueError(
                "Google Places API key is required. "
                "Set GOOGLE_PLACES_API_KEY environment variable or pass api_key parameter."
            )

        self.db_path = db_path
        self.session = requests.Session()
        self.session.headers.update({
            'X-Goog-Api-Key': self.api_key,
            'X-Goog-FieldMask': '*'
        })

    def search_restaurants(self, query: str, location_bias: bool = True) -> List[Dict]:
        """
        Search for restaurants using Google Places Text Search

        Args:
            query: Search query (e.g., "restaurants in Plymouth UK")
            location_bias: Whether to bias results to Plymouth area

        Returns:
            List of restaurant dictionaries
        """
        url = f"{PLACES_API_BASE}/places:searchText"

        payload = {
            "textQuery": query,
            "maxResultCount": 20  # Max per request
        }

        # Add location bias for Plymouth
        if location_bias:
            payload["locationBias"] = {
                "circle": {
                    "center": {
                        "latitude": PLYMOUTH_LAT,
                        "longitude": PLYMOUTH_LNG
                    },
                    "radius": 5000.0  # 5km radius from city center
                }
            }

        all_places = []
        next_page_token = None

        while True:
            if next_page_token:
                payload["pageToken"] = next_page_token

            try:
                response = self.session.post(url, json=payload, timeout=10)
                response.raise_for_status()
                data = response.json()

                places = data.get('places', [])
                all_places.extend(places)

                logger.info(f"Found {len(places)} restaurants (total: {len(all_places)})")

                # Check for next page
                next_page_token = data.get('nextPageToken')
                if not next_page_token:
                    break

                # Rate limiting between pages
                time.sleep(2)

            except requests.exceptions.RequestException as e:
                logger.error(f"Error searching for restaurants: {e}")
                break

        return all_places

    def parse_restaurant_data(self, place_data: Dict) -> Dict:
        """
        Parse restaurant data from Google Places API response

        Args:
            place_data: Raw place data from API

        Returns:
            Parsed restaurant dictionary
        """
        location = place_data.get('location', {})
        display_name = place_data.get('displayName', {})

        # Extract primary cuisine type from types array
        types = place_data.get('types', [])
        cuisine_keywords = ['restaurant', 'cafe', 'bar', 'food', 'meal']
        cuisine_type = None
        for t in types:
            if t not in cuisine_keywords and t != 'point_of_interest' and t != 'establishment':
                cuisine_type = t.replace('_', ' ').title()
                break
        if not cuisine_type:
            cuisine_type = 'Restaurant'

        return {
            'name': display_name.get('text', 'Unknown'),
            'google_place_id': place_data.get('id'),
            'cuisine_type': cuisine_type,
            'address': place_data.get('formattedAddress'),
            'google_formatted_address': place_data.get('formattedAddress'),
            'google_rating': place_data.get('rating'),
            'google_user_ratings_total': place_data.get('userRatingCount', 0),
            'google_price_level': place_data.get('priceLevel'),
            'google_latitude': location.get('latitude'),
            'google_longitude': location.get('longitude'),
            'google_maps_url': place_data.get('googleMapsUri'),
            'google_phone_national': place_data.get('nationalPhoneNumber'),
            'google_phone_international': place_data.get('internationalPhoneNumber'),
            'google_website_url': place_data.get('websiteUri'),
            'google_business_status': place_data.get('businessStatus'),

            # Service options
            'google_dine_in': 1 if place_data.get('dineIn') else 0,
            'google_takeout': 1 if place_data.get('takeout') else 0,
            'google_delivery': 1 if place_data.get('delivery') else 0,
            'google_reservable': 1 if place_data.get('reservable') else 0,

            # Meal services
            'google_serves_breakfast': 1 if place_data.get('servesBreakfast') else 0,
            'google_serves_lunch': 1 if place_data.get('servesLunch') else 0,
            'google_serves_dinner': 1 if place_data.get('servesDinner') else 0,

            # Beverages
            'google_serves_beer': 1 if place_data.get('servesBeer') else 0,
            'google_serves_wine': 1 if place_data.get('servesWine') else 0,
            'google_serves_vegetarian': 1 if place_data.get('servesVegetarianFood') else 0,

            # Metadata
            'google_last_fetched_at': datetime.now().isoformat(),
            'data_source': 'google_discovered',
            'scraped_at': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat()
        }

    def check_existing_restaurant(self, place_id: str) -> Optional[int]:
        """
        Check if restaurant already exists in database

        Args:
            place_id: Google Place ID

        Returns:
            restaurant_id if exists, None otherwise
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT restaurant_id FROM restaurants
            WHERE google_place_id = ?
        """, (place_id,))

        result = cursor.fetchone()
        conn.close()

        return result[0] if result else None

    def add_restaurant_to_db(self, restaurant_data: Dict) -> int:
        """
        Add a new restaurant to the database

        Args:
            restaurant_data: Parsed restaurant data

        Returns:
            restaurant_id of inserted restaurant
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Determine price range from price_level
        price_level = restaurant_data.get('google_price_level')
        if price_level == 0:
            price_range = 'Free'
        elif price_level == 1:
            price_range = '£'
        elif price_level == 2:
            price_range = '££'
        elif price_level == 3:
            price_range = '£££'
        elif price_level == 4:
            price_range = '££££'
        else:
            price_range = None

        # Use google_website_url, fallback to google_maps_url, or generate placeholder
        # website_url must be unique and not null
        website_url = (restaurant_data['google_website_url'] or
                      restaurant_data['google_maps_url'] or
                      f"https://www.google.com/maps/place/?q=place_id:{restaurant_data['google_place_id']}")

        cursor.execute("""
            INSERT INTO restaurants (
                name, cuisine_type, price_range, address, website_url,
                google_place_id, google_rating, google_user_ratings_total,
                google_price_level, google_latitude, google_longitude,
                google_formatted_address, google_maps_url,
                google_phone_national, google_phone_international,
                google_website_url, google_business_status,
                google_dine_in, google_takeout, google_delivery, google_reservable,
                google_serves_breakfast, google_serves_lunch, google_serves_dinner,
                google_serves_beer, google_serves_wine, google_serves_vegetarian,
                google_last_fetched_at, data_source, scraped_at, last_updated,
                is_active
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1
            )
        """, (
            restaurant_data['name'],
            restaurant_data['cuisine_type'],
            price_range,
            restaurant_data['address'],
            website_url,
            restaurant_data['google_place_id'],
            restaurant_data['google_rating'],
            restaurant_data['google_user_ratings_total'],
            restaurant_data['google_price_level'],
            restaurant_data['google_latitude'],
            restaurant_data['google_longitude'],
            restaurant_data['google_formatted_address'],
            restaurant_data['google_maps_url'],
            restaurant_data['google_phone_national'],
            restaurant_data['google_phone_international'],
            restaurant_data['google_website_url'],
            restaurant_data['google_business_status'],
            restaurant_data['google_dine_in'],
            restaurant_data['google_takeout'],
            restaurant_data['google_delivery'],
            restaurant_data['google_reservable'],
            restaurant_data['google_serves_breakfast'],
            restaurant_data['google_serves_lunch'],
            restaurant_data['google_serves_dinner'],
            restaurant_data['google_serves_beer'],
            restaurant_data['google_serves_wine'],
            restaurant_data['google_serves_vegetarian'],
            restaurant_data['google_last_fetched_at'],
            restaurant_data['data_source'],
            restaurant_data['scraped_at'],
            restaurant_data['last_updated']
        ))

        restaurant_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return restaurant_id

    def discover_and_add_restaurants(self, queries: List[str], dry_run: bool = False) -> Dict:
        """
        Discover restaurants and add them to database

        Args:
            queries: List of search queries to run
            dry_run: If True, don't actually add to database

        Returns:
            Dictionary with statistics
        """
        stats = {
            'total_found': 0,
            'already_exist': 0,
            'newly_added': 0,
            'new_restaurants': []
        }

        all_places = []
        seen_place_ids = set()

        # Run all queries
        for query in queries:
            logger.info(f"\n{'='*60}")
            logger.info(f"Searching: {query}")
            logger.info(f"{'='*60}")

            places = self.search_restaurants(query)

            # Deduplicate based on place_id
            for place in places:
                place_id = place.get('id')
                if place_id and place_id not in seen_place_ids:
                    all_places.append(place)
                    seen_place_ids.add(place_id)

            time.sleep(1)  # Rate limiting between queries

        stats['total_found'] = len(all_places)
        logger.info(f"\n{'='*60}")
        logger.info(f"Total unique restaurants found: {len(all_places)}")
        logger.info(f"{'='*60}\n")

        # Process each restaurant
        for i, place in enumerate(all_places, 1):
            place_id = place.get('id')
            name = place.get('displayName', {}).get('text', 'Unknown')

            logger.info(f"[{i}/{len(all_places)}] Processing: {name}")

            # Check if already exists
            existing_id = self.check_existing_restaurant(place_id)
            if existing_id:
                logger.info(f"  ✓ Already in database (ID: {existing_id})")
                stats['already_exist'] += 1
                continue

            # Parse restaurant data
            restaurant_data = self.parse_restaurant_data(place)

            if dry_run:
                logger.info(f"  [DRY RUN] Would add: {name}")
                logger.info(f"    Address: {restaurant_data.get('address')}")
                logger.info(f"    Rating: {restaurant_data.get('google_rating')}/5 ({restaurant_data.get('google_user_ratings_total')} reviews)")
                stats['new_restaurants'].append(restaurant_data)
            else:
                # Add to database
                restaurant_id = self.add_restaurant_to_db(restaurant_data)
                logger.info(f"  ✓ Added to database (ID: {restaurant_id})")
                stats['new_restaurants'].append(restaurant_data)

            stats['newly_added'] += 1

        return stats


def main():
    parser = argparse.ArgumentParser(
        description='Discover restaurants in Plymouth using Google Places API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Discover all restaurants (general search)
  python discover_restaurants_google.py --discover-all

  # Discover by cuisine types (more comprehensive)
  python discover_restaurants_google.py --discover-by-cuisine

  # Dry run (show what would be added)
  python discover_restaurants_google.py --discover-all --dry-run

Environment:
  Requires GOOGLE_PLACES_API_KEY environment variable.
        """
    )

    parser.add_argument('--discover-all', action='store_true', help='Discover all restaurants (general search)')
    parser.add_argument('--discover-by-cuisine', action='store_true', help='Discover restaurants by cuisine type (more comprehensive)')
    parser.add_argument('--dry-run', action='store_true', help='Dry run - show what would be added without adding')

    args = parser.parse_args()

    # Validate API key
    if not GOOGLE_API_KEY:
        logger.error("GOOGLE_PLACES_API_KEY environment variable is not set!")
        logger.error("Get API key at: https://console.cloud.google.com/")
        sys.exit(1)

    try:
        discovery = RestaurantDiscovery()

        # Build query list
        queries = []

        if args.discover_all:
            queries = [
                "restaurants in Plymouth UK",
                "cafes in Plymouth UK",
                "bars in Plymouth UK",
                "pubs in Plymouth UK"
            ]

        elif args.discover_by_cuisine:
            queries = [
                "restaurants in Plymouth UK",
                "Italian restaurants in Plymouth UK",
                "Indian restaurants in Plymouth UK",
                "Chinese restaurants in Plymouth UK",
                "Thai restaurants in Plymouth UK",
                "Mexican restaurants in Plymouth UK",
                "Japanese restaurants in Plymouth UK",
                "French restaurants in Plymouth UK",
                "American restaurants in Plymouth UK",
                "British restaurants in Plymouth UK",
                "fish and chips in Plymouth UK",
                "pizza restaurants in Plymouth UK",
                "burger restaurants in Plymouth UK",
                "cafes in Plymouth UK",
                "bars in Plymouth UK",
                "pubs in Plymouth UK"
            ]

        else:
            parser.print_help()
            sys.exit(0)

        # Run discovery
        logger.info(f"\n{'='*60}")
        logger.info(f"GOOGLE PLACES RESTAURANT DISCOVERY")
        logger.info(f"Plymouth, UK")
        logger.info(f"Queries: {len(queries)}")
        if args.dry_run:
            logger.info(f"Mode: DRY RUN (no database changes)")
        logger.info(f"{'='*60}\n")

        stats = discovery.discover_and_add_restaurants(queries, dry_run=args.dry_run)

        # Final summary
        logger.info(f"\n{'='*60}")
        logger.info(f"DISCOVERY COMPLETE")
        logger.info(f"{'='*60}")
        logger.info(f"Total restaurants found: {stats['total_found']}")
        logger.info(f"Already in database: {stats['already_exist']}")
        logger.info(f"Newly discovered: {stats['newly_added']}")

        if args.dry_run:
            logger.info(f"\n[DRY RUN] No changes were made to the database.")
            logger.info(f"Run without --dry-run to add {stats['newly_added']} new restaurants.")

        if stats['newly_added'] > 0:
            logger.info(f"\n📋 New Restaurants:")
            for r in stats['new_restaurants'][:10]:  # Show first 10
                logger.info(f"  - {r['name']}")
                logger.info(f"    {r['address']}")
                logger.info(f"    Rating: {r['google_rating']}/5 ({r['google_user_ratings_total']} reviews)")

            if len(stats['new_restaurants']) > 10:
                logger.info(f"  ... and {len(stats['new_restaurants']) - 10} more")

        logger.info(f"{'='*60}\n")

    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
