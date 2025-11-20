#!/usr/bin/env python3
"""
Targeted Restaurant Licensing Scraper

Scrapes licensing data ONLY for the 98 restaurants already in our database.
Much faster than scraping all 2,232 Plymouth premises.
"""

import sqlite3
import json
import time
from datetime import datetime
from scrape_plymouth_licensing import scrape_license_details, SEARCH_URL
import requests
from bs4 import BeautifulSoup
import re

def search_licensing_database(restaurant_name: str, address: str = None):
    """
    Search Plymouth licensing database for a restaurant by name.
    Returns list of matching premises with their IDs.
    """
    search_url = f"{SEARCH_URL}?SYS_ID=1&SearchOperatorName={restaurant_name}"

    try:
        time.sleep(2)  # Rate limiting
        response = requests.get(search_url, timeout=30)
        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', class_='grid')
        if not table:
            return []

        results = []
        rows = table.find('tbody').find_all('tr') if table.find('tbody') else []

        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 2:
                name_link = cols[0].find('a')
                if name_link:
                    premises_name = name_link.text.strip()
                    premises_url = name_link.get('href', '')
                    premises_id_match = re.search(r'/Search/(\d+)$', premises_url)
                    premises_id = premises_id_match.group(1) if premises_id_match else None
                    premises_address = cols[1].text.strip()

                    if premises_id:
                        results.append({
                            'premises_id': premises_id,
                            'name': premises_name,
                            'address': premises_address
                        })

        return results

    except Exception as e:
        print(f"  Error searching for {restaurant_name}: {e}")
        return []

def get_restaurants_from_db():
    """Get all restaurant names from our database."""
    conn = sqlite3.connect('plymouth_research.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT restaurant_id, name, address, cuisine_type, price_range
        FROM restaurants
        WHERE is_active = 1
        ORDER BY name
    """)

    restaurants = []
    for row in cursor.fetchall():
        restaurants.append({
            'restaurant_id': row[0],
            'name': row[1],
            'address': row[2],
            'cuisine_type': row[3],
            'price_range': row[4]
        })

    conn.close()
    return restaurants

def main():
    print("=" * 80)
    print("TARGETED RESTAURANT LICENSING SCRAPER")
    print("=" * 80)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Get restaurants from our database
    restaurants = get_restaurants_from_db()
    print(f"Found {len(restaurants)} restaurants in database\n")

    results = []
    matched_count = 0
    unmatched = []

    for idx, restaurant in enumerate(restaurants, 1):
        name = restaurant['name']
        address = restaurant.get('address', '')

        print(f"[{idx}/{len(restaurants)}] Searching for: {name}")

        # Search licensing database
        search_results = search_licensing_database(name, address)

        if search_results:
            print(f"  ✓ Found {len(search_results)} match(es)")

            # Get details for first match (most relevant)
            premises = search_results[0]
            print(f"  → Using: {premises['name']} (ID: {premises['premises_id']})")

            # Scrape detailed license info
            details = scrape_license_details(premises['premises_id'])

            # Combine all data
            result = {
                **restaurant,  # Our database info
                'licensing': {
                    'premises_id': premises['premises_id'],
                    'licensing_name': premises['name'],
                    'licensing_address': premises['address'],
                    'scraped_at': datetime.utcnow().isoformat(),
                    **details  # License details
                },
                'all_matches': search_results  # All search results for reference
            }

            results.append(result)
            matched_count += 1

            # Show key extracted info
            if details.get('opening_hours'):
                print(f"  → Opening hours: {len(details['opening_hours'])} time periods")
            if details.get('licensable_activities'):
                print(f"  → Activities: {', '.join(details['licensable_activities'][:2])}")

        else:
            print(f"  ✗ No match found")
            unmatched.append(restaurant)
            results.append({
                **restaurant,
                'licensing': None,
                'all_matches': []
            })

        print()

    # Save results
    output_file = 'restaurant_licensing_data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # Save unmatched for manual review
    if unmatched:
        with open('unmatched_licensing.json', 'w', encoding='utf-8') as f:
            json.dump(unmatched, f, indent=2, ensure_ascii=False)

    # Summary
    print("=" * 80)
    print("SCRAPING COMPLETE")
    print("=" * 80)
    print(f"Total restaurants: {len(restaurants)}")
    print(f"Matched with licensing data: {matched_count} ({matched_count/len(restaurants)*100:.1f}%)")
    print(f"Unmatched: {len(unmatched)} ({len(unmatched)/len(restaurants)*100:.1f}%)")
    print(f"\nOutput files:")
    print(f"  - {output_file} (all results)")
    if unmatched:
        print(f"  - unmatched_licensing.json (needs manual review)")
    print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

if __name__ == "__main__":
    main()
