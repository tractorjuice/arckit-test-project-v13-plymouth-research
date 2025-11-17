#!/usr/bin/env python3
"""
Phase 1: Discover Menu URLs
============================

Crawls all restaurant websites to find menu page URLs.
Saves results to JSON for Phase 2 extraction.

Restartable: Reads existing progress and continues from last checkpoint.

Author: Plymouth Research Team
Date: 2025-11-17
"""

import csv
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
from firecrawl import Firecrawl

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MenuURLDiscovery:
    """Discover menu URLs for all restaurants."""

    def __init__(self, api_key: str):
        """Initialize Firecrawl."""
        self.firecrawl = Firecrawl(api_key=api_key)
        self.discovered = 0
        self.failed = 0
        logger.info("Menu URL Discovery initialized")

    def find_menu_url(self, base_url: str, restaurant_name: str) -> Dict:
        """
        Find menu URL for a restaurant.

        Returns:
            Dict with restaurant info and menu_url
        """
        try:
            logger.info(f"  🔍 Discovering menu URL for {restaurant_name}")

            # Step 1: Map site structure
            try:
                map_result = self.firecrawl.map(url=base_url)
                links = map_result.links if hasattr(map_result, 'links') else []

                # Look for menu pages
                menu_keywords = ['menu', 'food', 'eat', 'dining', 'restaurant-menu', 'our-menu']

                for link in links:
                    link_url = link.url if hasattr(link, 'url') else str(link)
                    link_lower = link_url.lower()

                    # Check for menu pages (HTML or PDF)
                    if any(keyword in link_lower for keyword in menu_keywords):
                        logger.info(f"  ✅ Found in map: {link_url}")
                        self.discovered += 1
                        return {
                            'restaurant_name': restaurant_name,
                            'base_url': base_url,
                            'menu_url': link_url,
                            'discovery_method': 'map',
                            'status': 'found'
                        }

                    # Check for PDFs
                    if link_lower.endswith('.pdf') and any(keyword in link_lower for keyword in ['menu', 'food']):
                        logger.info(f"  ✅ Found PDF in map: {link_url}")
                        self.discovered += 1
                        return {
                            'restaurant_name': restaurant_name,
                            'base_url': base_url,
                            'menu_url': link_url,
                            'discovery_method': 'map_pdf',
                            'status': 'found'
                        }

            except Exception as e:
                logger.warning(f"  ⚠️ Map failed: {str(e)}")

            # Step 2: Try common paths
            logger.info(f"  🔍 Trying common menu paths...")
            common_paths = [
                '/menu', '/menus', '/food', '/our-menu', '/eat',
                '/restaurant-menu', '/food-menu', '/menu.html',
                '/menu.pdf', '/menus.pdf', '/food-menu.pdf'
            ]

            base_domain = base_url.rstrip('/')
            for path in common_paths:
                test_url = base_domain + path
                try:
                    # Quick test
                    test_result = self.firecrawl.scrape(test_url, formats=['markdown'])
                    if test_result and hasattr(test_result, 'markdown') and len(test_result.markdown) > 100:
                        logger.info(f"  ✅ Found via path test: {test_url}")
                        self.discovered += 1
                        return {
                            'restaurant_name': restaurant_name,
                            'base_url': base_url,
                            'menu_url': test_url,
                            'discovery_method': 'path_test',
                            'status': 'found'
                        }
                except:
                    pass

            # Not found - use base URL as fallback
            logger.warning(f"  ⚠️ No menu URL found, will use base URL")
            self.failed += 1
            return {
                'restaurant_name': restaurant_name,
                'base_url': base_url,
                'menu_url': base_url,
                'discovery_method': 'fallback',
                'status': 'not_found'
            }

        except Exception as e:
            logger.error(f"  ❌ Error: {str(e)}")
            self.failed += 1
            return {
                'restaurant_name': restaurant_name,
                'base_url': base_url,
                'menu_url': base_url,
                'discovery_method': 'error',
                'status': 'error',
                'error': str(e)
            }

    def discover_all(self, csv_file: str, output_file: str, checkpoint_every: int = 25):
        """
        Discover menu URLs for all restaurants.

        Args:
            csv_file: Input CSV with restaurants
            output_file: Output JSON file
            checkpoint_every: Save progress every N restaurants
        """
        # Load existing progress if available
        results = []
        processed_names = set()

        if Path(output_file).exists():
            logger.info(f"📂 Loading existing progress from {output_file}")
            with open(output_file, 'r', encoding='utf-8') as f:
                results = json.load(f)
                processed_names = {r['restaurant_name'] for r in results}
            logger.info(f"✅ Loaded {len(results)} previously discovered restaurants")

        # Load restaurants from CSV
        restaurants = []
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['name'] not in processed_names:
                    restaurants.append({
                        'name': row['name'],
                        'url': row['website_url'],
                        'cuisine_type': row['cuisine_type']
                    })

        total = len(restaurants)
        already_done = len(processed_names)

        logger.info(f"\n📊 Menu URL Discovery")
        logger.info(f"Already discovered: {already_done}")
        logger.info(f"Remaining: {total}")
        logger.info(f"Total: {already_done + total}\n")

        # Discover menu URLs
        for i, resto in enumerate(restaurants, 1):
            logger.info(f"\n[{already_done + i}/{already_done + total}] {resto['name']}")

            result = self.find_menu_url(resto['url'], resto['name'])
            result['cuisine_type'] = resto['cuisine_type']
            results.append(result)

            # Save checkpoint
            if i % checkpoint_every == 0 or i == total:
                self.save_results(results, output_file)
                logger.info(f"\n💾 Checkpoint saved: {already_done + i}/{already_done + total} restaurants")
                logger.info(f"📊 Found: {self.discovered} | Not found: {self.failed}\n")

        # Final save
        self.save_results(results, output_file)

        logger.info("\n" + "="*80)
        logger.info("🎉 PHASE 1 COMPLETE: Menu URL Discovery")
        logger.info("="*80)
        logger.info(f"Total restaurants: {len(results)}")
        logger.info(f"✅ Menu URLs found: {self.discovered}")
        logger.info(f"⚠️ Fallback to base URL: {self.failed}")
        logger.info(f"💾 Saved to: {output_file}")
        logger.info("="*80 + "\n")

        return results

    def save_results(self, results: List[Dict], filename: str):
        """Save results to JSON."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)


def main():
    """Main discovery function."""
    API_KEY = "fc-5e88426ea5584be080853dfe03cb2b1a"

    discoverer = MenuURLDiscovery(api_key=API_KEY)

    discoverer.discover_all(
        csv_file="synthetic_restaurants_unique.csv",
        output_file="restaurant_menu_urls.json",
        checkpoint_every=25
    )

    print(f"\n✅ Phase 1 complete!")
    print(f"📁 Menu URLs saved to: restaurant_menu_urls.json")
    print(f"\nNext step: Run phase2_extract_menus.py to extract menu data")


if __name__ == "__main__":
    main()
