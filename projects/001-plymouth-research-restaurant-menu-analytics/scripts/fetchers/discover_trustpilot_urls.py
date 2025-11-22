#!/usr/bin/env python3
"""
Trustpilot URL Discovery Tool for Plymouth Research Restaurants
================================================================

Discovers Trustpilot URLs for restaurants in the database using multiple strategies:
1. Domain-based lookup (if restaurant has website)
2. Google search scraping
3. Direct Trustpilot search
4. Manual verification export

Usage:
    # Discover URLs for all restaurants
    python discover_trustpilot_urls.py --discover-all

    # Update database with verified URLs from CSV
    python discover_trustpilot_urls.py --import-csv verified_trustpilot_urls.csv

    # Export restaurants for manual verification
    python discover_trustpilot_urls.py --export-for-verification
"""

import requests
from bs4 import BeautifulSoup
import sqlite3
import pandas as pd
from typing import List, Dict, Optional, Tuple
import re
import time
import argparse
from urllib.parse import urlparse, quote_plus
import logging
from difflib import SequenceMatcher

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TrustpilotURLDiscoverer:
    """Discover Trustpilot URLs for restaurants"""

    def __init__(self, db_path: str = "plymouth_research.db"):
        self.db_path = db_path
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })

    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def extract_domain_from_website(self, website_url: str) -> Optional[str]:
        """
        Extract domain from restaurant website URL

        Args:
            website_url: Restaurant website URL

        Returns:
            Domain without www (e.g., 'rockfish.co.uk')
        """
        if not website_url:
            return None

        try:
            parsed = urlparse(website_url)
            domain = parsed.netloc or parsed.path
            # Remove www.
            domain = re.sub(r'^www\.', '', domain)
            return domain
        except Exception as e:
            logger.error(f"Error parsing URL {website_url}: {e}")
            return None

    def check_domain_based_url(self, website_url: str) -> Optional[Tuple[str, str, float]]:
        """
        Check if Trustpilot page exists for restaurant's domain

        Args:
            website_url: Restaurant website URL

        Returns:
            Tuple of (trustpilot_url, business_id, confidence) or None
        """
        domain = self.extract_domain_from_website(website_url)
        if not domain:
            return None

        # Common Trustpilot URL patterns
        patterns = [
            f"https://www.trustpilot.com/review/{domain}",
            f"https://www.trustpilot.com/review/www.{domain}",
        ]

        for url in patterns:
            try:
                logger.info(f"Checking: {url}")
                response = self.session.get(url, timeout=10, allow_redirects=True)

                if response.status_code == 200:
                    # Verify it's actually a business page, not a 404
                    soup = BeautifulSoup(response.text, 'html.parser')

                    # Check for business name in page
                    business_name_elem = soup.find('h1')
                    if business_name_elem:
                        # Extract business ID from URL
                        business_id = url.split('/review/')[-1]
                        logger.info(f"✓ Found Trustpilot page: {url}")
                        return (url, business_id, 1.0)  # High confidence

                time.sleep(1)  # Rate limiting

            except requests.RequestException as e:
                logger.debug(f"Error checking {url}: {e}")
                continue

        return None

    def search_trustpilot_directly(self, restaurant_name: str, location: str = "Plymouth") -> List[Tuple[str, str, float]]:
        """
        Search Trustpilot's own search for restaurant

        Args:
            restaurant_name: Name of restaurant
            location: Location to help narrow search

        Returns:
            List of (trustpilot_url, business_id, confidence_score) tuples
        """
        try:
            # Trustpilot search URL
            query = f"{restaurant_name} {location}"
            search_url = f"https://www.trustpilot.com/search?query={quote_plus(query)}"

            logger.info(f"Searching Trustpilot for: {query}")
            response = self.session.get(search_url, timeout=10)

            if response.status_code != 200:
                return []

            soup = BeautifulSoup(response.text, 'html.parser')

            # Find search results (Trustpilot's structure may vary)
            results = []

            # Look for business unit links
            for link in soup.find_all('a', href=re.compile(r'/review/')):
                href = link.get('href')
                if not href.startswith('http'):
                    href = f"https://www.trustpilot.com{href}"

                # Extract business name from link text
                business_name_elem = link.find('h3') or link.find('span') or link
                business_name = business_name_elem.get_text(strip=True) if business_name_elem else ""

                # Calculate confidence based on name similarity
                similarity = SequenceMatcher(None, restaurant_name.lower(), business_name.lower()).ratio()

                if similarity > 0.6:  # At least 60% match
                    business_id = href.split('/review/')[-1].split('?')[0]
                    results.append((href, business_id, similarity))
                    logger.info(f"  Found: {business_name} ({similarity:.2f} match) - {href}")

            # Sort by confidence
            results.sort(key=lambda x: x[2], reverse=True)
            return results[:5]  # Top 5 results

        except Exception as e:
            logger.error(f"Error searching Trustpilot: {e}")
            return []

    def search_google(self, restaurant_name: str, location: str = "Plymouth") -> Optional[Tuple[str, str, float]]:
        """
        Search Google for restaurant's Trustpilot page

        Args:
            restaurant_name: Name of restaurant
            location: Location to help narrow search

        Returns:
            Tuple of (trustpilot_url, business_id, confidence) or None

        Note: This may be blocked by Google's bot detection. Use sparingly.
        """
        try:
            query = f"{restaurant_name} {location} site:trustpilot.com"
            search_url = f"https://www.google.com/search?q={quote_plus(query)}"

            logger.info(f"Googling: {query}")
            response = self.session.get(search_url, timeout=10)

            if response.status_code != 200:
                logger.warning("Google search failed (may be blocked)")
                return None

            soup = BeautifulSoup(response.text, 'html.parser')

            # Find first Trustpilot link in results
            for link in soup.find_all('a', href=re.compile(r'trustpilot\.com/review/')):
                href = link.get('href')

                # Extract actual URL from Google redirect
                match = re.search(r'(https://[^&]+trustpilot\.com/review/[^&]+)', href)
                if match:
                    url = match.group(1)
                    business_id = url.split('/review/')[-1].split('?')[0]
                    logger.info(f"✓ Found via Google: {url}")
                    return (url, business_id, 0.8)  # Medium confidence

            time.sleep(2)  # Rate limiting for Google

        except Exception as e:
            logger.error(f"Error searching Google: {e}")
            return None

    def discover_url_for_restaurant(self, restaurant_id: int) -> Optional[Dict]:
        """
        Discover Trustpilot URL for a single restaurant using multiple strategies

        Args:
            restaurant_id: Database ID of restaurant

        Returns:
            Dict with discovery results or None
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT restaurant_id, name, address, website_url
            FROM restaurants
            WHERE restaurant_id = ?
        """, (restaurant_id,))

        restaurant = cursor.fetchone()
        conn.close()

        if not restaurant:
            logger.error(f"Restaurant {restaurant_id} not found")
            return None

        logger.info(f"\n{'='*60}")
        logger.info(f"Discovering Trustpilot URL for: {restaurant['name']}")
        logger.info(f"{'='*60}")

        candidates = []

        # Strategy 1: Domain-based lookup (if has website)
        if restaurant['website_url']:
            logger.info("\n[Strategy 1] Checking domain-based URL...")
            result = self.check_domain_based_url(restaurant['website_url'])
            if result:
                candidates.append({
                    'url': result[0],
                    'business_id': result[1],
                    'confidence': result[2],
                    'method': 'domain_based'
                })

        # Strategy 2: Trustpilot direct search
        logger.info("\n[Strategy 2] Searching Trustpilot...")
        trustpilot_results = self.search_trustpilot_directly(restaurant['name'])
        for url, business_id, confidence in trustpilot_results:
            candidates.append({
                'url': url,
                'business_id': business_id,
                'confidence': confidence,
                'method': 'trustpilot_search'
            })

        # Strategy 3: Google search (use sparingly)
        # Commented out to avoid Google blocking - enable if needed
        # logger.info("\n[Strategy 3] Searching Google...")
        # google_result = self.search_google(restaurant['name'])
        # if google_result:
        #     candidates.append({
        #         'url': google_result[0],
        #         'business_id': google_result[1],
        #         'confidence': google_result[2],
        #         'method': 'google_search'
        #     })

        if not candidates:
            logger.info("✗ No Trustpilot URL found")
            return None

        # Sort by confidence and return best match
        candidates.sort(key=lambda x: x['confidence'], reverse=True)
        best_match = candidates[0]

        result = {
            'restaurant_id': restaurant_id,
            'restaurant_name': restaurant['name'],
            'trustpilot_url': best_match['url'],
            'trustpilot_business_id': best_match['business_id'],
            'confidence': best_match['confidence'],
            'method': best_match['method'],
            'all_candidates': candidates
        }

        logger.info(f"\n✓ Best match:")
        logger.info(f"  URL: {best_match['url']}")
        logger.info(f"  Confidence: {best_match['confidence']:.2f}")
        logger.info(f"  Method: {best_match['method']}")

        if len(candidates) > 1:
            logger.info(f"\n  Other candidates found: {len(candidates) - 1}")

        return result

    def discover_all_restaurants(self, update_db: bool = False) -> pd.DataFrame:
        """
        Discover Trustpilot URLs for all restaurants without URLs

        Args:
            update_db: If True, automatically update database with high-confidence matches

        Returns:
            DataFrame with discovery results
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT restaurant_id, name, website_url
            FROM restaurants
            WHERE is_active = 1
            AND (trustpilot_url IS NULL OR trustpilot_url = '')
            ORDER BY name
        """)

        restaurants = cursor.fetchall()
        conn.close()

        logger.info(f"\n{'='*60}")
        logger.info(f"Discovering Trustpilot URLs for {len(restaurants)} restaurants")
        logger.info(f"{'='*60}\n")

        results = []

        for i, restaurant in enumerate(restaurants, 1):
            logger.info(f"\n[{i}/{len(restaurants)}] {restaurant['name']}")

            result = self.discover_url_for_restaurant(restaurant['restaurant_id'])

            if result:
                results.append(result)

                # Auto-update database if high confidence (95%+) and update_db=True
                if update_db and result['confidence'] >= 0.95:
                    self.update_restaurant_url(
                        result['restaurant_id'],
                        result['trustpilot_url'],
                        result['trustpilot_business_id']
                    )
                    logger.info("  → Updated database (high confidence)")

            # Rate limiting
            time.sleep(3)

        # Create DataFrame
        if results:
            df = pd.DataFrame(results)
            df = df[['restaurant_id', 'restaurant_name', 'trustpilot_url',
                     'trustpilot_business_id', 'confidence', 'method']]
            return df
        else:
            return pd.DataFrame()

    def update_restaurant_url(self, restaurant_id: int, trustpilot_url: str,
                               trustpilot_business_id: str) -> bool:
        """
        Update restaurant's Trustpilot URL in database

        Args:
            restaurant_id: Database ID
            trustpilot_url: Trustpilot page URL
            trustpilot_business_id: Business ID (slug)

        Returns:
            True if successful
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE restaurants
                SET trustpilot_url = ?,
                    trustpilot_business_id = ?
                WHERE restaurant_id = ?
            """, (trustpilot_url, trustpilot_business_id, restaurant_id))

            conn.commit()
            conn.close()

            logger.info(f"✓ Updated database for restaurant {restaurant_id}")
            return True

        except Exception as e:
            logger.error(f"Error updating database: {e}")
            return False

    def export_for_manual_verification(self, filename: str = "trustpilot_urls_for_verification.csv"):
        """
        Export all restaurants with their current Trustpilot status for manual verification

        Args:
            filename: Output CSV filename
        """
        conn = self._get_connection()

        df = pd.read_sql_query("""
            SELECT
                restaurant_id,
                name,
                address,
                website_url,
                trustpilot_url,
                trustpilot_business_id,
                CASE
                    WHEN trustpilot_url IS NOT NULL THEN 'verified'
                    ELSE 'needs_review'
                END as status,
                '' as manual_trustpilot_url,
                '' as notes
            FROM restaurants
            WHERE is_active = 1
            ORDER BY
                CASE WHEN trustpilot_url IS NULL THEN 1 ELSE 0 END,
                name
        """, conn)

        conn.close()

        df.to_csv(filename, index=False)
        logger.info(f"✓ Exported {len(df)} restaurants to {filename}")
        logger.info(f"  - {len(df[df['status'] == 'verified'])} already have Trustpilot URLs")
        logger.info(f"  - {len(df[df['status'] == 'needs_review'])} need manual verification")

        return filename

    def import_verified_urls(self, csv_filename: str) -> int:
        """
        Import manually verified Trustpilot URLs from CSV

        CSV should have columns: restaurant_id, manual_trustpilot_url
        Updates database with non-empty manual_trustpilot_url values

        Args:
            csv_filename: Path to CSV with verified URLs

        Returns:
            Number of restaurants updated
        """
        df = pd.read_csv(csv_filename)

        # Filter to rows with manual URLs
        df = df[df['manual_trustpilot_url'].notna() & (df['manual_trustpilot_url'] != '')]

        updated_count = 0

        for _, row in df.iterrows():
            url = row['manual_trustpilot_url'].strip()
            if not url:
                continue

            # Extract business ID from URL
            match = re.search(r'trustpilot\.com/review/([^/?]+)', url)
            if match:
                business_id = match.group(1)

                if self.update_restaurant_url(row['restaurant_id'], url, business_id):
                    updated_count += 1

        logger.info(f"✓ Updated {updated_count} restaurants from {csv_filename}")
        return updated_count


def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(description='Discover Trustpilot URLs for restaurants')
    parser.add_argument('--discover-all', action='store_true',
                        help='Discover URLs for all restaurants without Trustpilot URLs')
    parser.add_argument('--auto-update', action='store_true',
                        help='Automatically update database with high-confidence matches (95%+)')
    parser.add_argument('--restaurant-id', type=int,
                        help='Discover URL for specific restaurant')
    parser.add_argument('--export-for-verification', action='store_true',
                        help='Export CSV for manual verification')
    parser.add_argument('--import-csv', type=str,
                        help='Import manually verified URLs from CSV')
    parser.add_argument('--output', type=str, default='discovered_trustpilot_urls.csv',
                        help='Output filename for discovery results')
    parser.add_argument('--db', type=str, default='plymouth_research.db',
                        help='Database path')

    args = parser.parse_args()

    discoverer = TrustpilotURLDiscoverer(db_path=args.db)

    if args.export_for_verification:
        filename = discoverer.export_for_manual_verification()
        print(f"\nExported to: {filename}")
        print("\nNext steps:")
        print("1. Open the CSV file")
        print("2. For restaurants needing review, manually search Trustpilot")
        print("3. Fill in the 'manual_trustpilot_url' column")
        print(f"4. Run: python discover_trustpilot_urls.py --import-csv {filename}")

    elif args.import_csv:
        count = discoverer.import_verified_urls(args.import_csv)
        print(f"\n✓ Imported {count} verified URLs")

    elif args.restaurant_id:
        result = discoverer.discover_url_for_restaurant(args.restaurant_id)
        if result:
            print("\nDiscovery Result:")
            print(f"  Restaurant: {result['restaurant_name']}")
            print(f"  URL: {result['trustpilot_url']}")
            print(f"  Confidence: {result['confidence']:.2%}")
            print(f"  Method: {result['method']}")

            # Ask if should update
            update = input("\nUpdate database with this URL? (y/n): ")
            if update.lower() == 'y':
                discoverer.update_restaurant_url(
                    result['restaurant_id'],
                    result['trustpilot_url'],
                    result['trustpilot_business_id']
                )
                print("✓ Database updated")

    elif args.discover_all:
        df = discoverer.discover_all_restaurants(update_db=args.auto_update)

        if not df.empty:
            df.to_csv(args.output, index=False)
            print(f"\n✓ Saved results to: {args.output}")
            print(f"\nSummary:")
            print(f"  Total discovered: {len(df)}")
            print(f"  High confidence (90%+): {len(df[df['confidence'] >= 0.9])}")
            print(f"  Medium confidence (70-90%): {len(df[(df['confidence'] >= 0.7) & (df['confidence'] < 0.9)])}")
            print(f"  Low confidence (<70%): {len(df[df['confidence'] < 0.7])}")

            if args.auto_update:
                print(f"\n  Auto-updated (95%+): {len(df[df['confidence'] >= 0.95])}")
        else:
            print("\nNo Trustpilot URLs discovered")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
