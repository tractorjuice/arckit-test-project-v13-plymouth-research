#!/usr/bin/env python3
"""
Plymouth Licensing Database Scraper

Extracts all premises licensing data from Plymouth City Council's licensing register.
Saves comprehensive data including license holders, DPS, operating hours, and conditions.
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
import glob
from typing import Dict, List, Optional
from datetime import datetime

BASE_URL = "https://licensing.plymouth.gov.uk"
SEARCH_URL = f"{BASE_URL}/1/LicensingActPremises/Search"

def get_with_retry(url: str, max_retries: int = 3, delay: float = 2.0) -> Optional[requests.Response]:
    """Fetch URL with retry logic and rate limiting."""
    for attempt in range(max_retries):
        try:
            time.sleep(delay)  # Rate limiting
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                return response
            elif response.status_code == 500:
                print(f"  Server error 500 for {url}, skipping...")
                return None
            else:
                print(f"  Attempt {attempt + 1}: Status {response.status_code}")
        except requests.RequestException as e:
            print(f"  Attempt {attempt + 1}: Error {e}")
            if attempt < max_retries - 1:
                time.sleep(delay * (attempt + 1))
    return None

def scrape_all_premises_list() -> List[Dict]:
    """Scrape all premises IDs, names, and addresses from search results."""
    print("=" * 80)
    print("PHASE 1: Scraping all premises from search results")
    print("=" * 80)

    all_premises = []
    page = 1

    while True:
        url = f"{SEARCH_URL}?SYS_ID=1&page={page}"
        print(f"\nFetching page {page}...")

        response = get_with_retry(url)
        if not response:
            print(f"Failed to fetch page {page}, stopping.")
            break

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the results table
        table = soup.find('table', class_='grid')
        if not table:
            print("No table found, stopping.")
            break

        # Extract premises from table rows
        rows = table.find('tbody').find_all('tr') if table.find('tbody') else []

        if not rows:
            print("No more results, stopping.")
            break

        page_count = 0
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 2:
                # Extract premises name and ID from link
                name_link = cols[0].find('a')
                if name_link:
                    premises_name = name_link.text.strip()
                    premises_url = name_link.get('href', '')
                    # Extract premises ID from URL like /1/LicensingActPremises/Search/3492
                    premises_id_match = re.search(r'/Search/(\d+)$', premises_url)
                    premises_id = premises_id_match.group(1) if premises_id_match else None

                    # Extract address
                    address = cols[1].text.strip()

                    if premises_id:
                        all_premises.append({
                            'premises_id': premises_id,
                            'name': premises_name,
                            'address': address
                        })
                        page_count += 1

        print(f"  Found {page_count} premises on page {page} (Total: {len(all_premises)})")

        # Check if there's a next page by looking for page count info
        pager_div = soup.find('div', class_='clsIdoxPagerDiv')
        if pager_div:
            # Look for "Page X of Y" text
            summary_text = pager_div.find('span', class_='clsIdoxPagerSummarySpan')
            if summary_text:
                # Extract total pages from "Page 1 of 224 (2232 items)"
                match = re.search(r'Page \d+ of (\d+)', summary_text.text)
                if match:
                    total_pages = int(match.group(1))
                    if page < total_pages:
                        page += 1
                    else:
                        print(f"\nReached last page ({total_pages}).")
                        break
                else:
                    break
            else:
                break
        else:
            break

    print(f"\n{'=' * 80}")
    print(f"PHASE 1 COMPLETE: Found {len(all_premises)} total premises")
    print(f"{'=' * 80}\n")

    return all_premises

def parse_hours_table(table) -> List[Dict]:
    """Parse hours table from license page."""
    hours = []
    if not table:
        return hours

    # Look for rows with class="Data" which contain the actual hours
    data_rows = table.find_all('tr', class_='Data')
    for row in data_rows:
        cols = row.find_all('td')
        if len(cols) >= 3:
            hours.append({
                'days': cols[0].text.strip(),
                'time_from': cols[1].text.strip(),
                'time_to': cols[2].text.strip(),
                'non_standard': cols[3].text.strip() if len(cols) > 3 else ''
            })

    return hours

def parse_conditions(soup) -> Dict:
    """Parse all conditions sections from license page."""
    conditions = {
        'mandatory': [],
        'operational': [],
        'post_hearing': [],
        'cctv': []
    }

    # Find all annex sections
    text = soup.get_text()

    # Extract ANNEX 1 - Mandatory Conditions
    annex1_match = re.search(r'ANNEX 1.*?Mandatory Conditions(.*?)(?=ANNEX 2|$)', text, re.DOTALL)
    if annex1_match:
        conditions['mandatory'] = [line.strip() for line in annex1_match.group(1).split('\n') if line.strip()]

    # Extract ANNEX 2 - Operational Schedule
    annex2_match = re.search(r'ANNEX 2.*?Operating Schedule(.*?)(?=ANNEX 3|$)', text, re.DOTALL)
    if annex2_match:
        conditions['operational'] = [line.strip() for line in annex2_match.group(1).split('\n') if line.strip()]

    # Extract ANNEX 3 - Post-Hearing Conditions
    annex3_match = re.search(r'ANNEX 3.*?After Hearing(.*?)(?=ANNEX 4|$)', text, re.DOTALL)
    if annex3_match:
        conditions['post_hearing'] = [line.strip() for line in annex3_match.group(1).split('\n') if line.strip()]

    return conditions

def scrape_license_details(premises_id: str) -> Optional[Dict]:
    """Scrape detailed license information for a specific premises."""
    # Step 1: Get premises page to find current license
    premises_url = f"{SEARCH_URL}/{premises_id}"
    response = get_with_retry(premises_url)
    if not response:
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the most recent license link
    license_links = soup.find_all('a', href=re.compile(r'/Detail\?LIC_ID='))
    if not license_links:
        return {'error': 'No current license found'}

    # Get the first (most recent) license
    license_link = license_links[0]
    license_number = license_link.text.strip()
    license_url = BASE_URL + license_link.get('href')

    # Step 2: Get detailed license page
    response = get_with_retry(license_url)
    if not response:
        return {'error': 'Could not fetch license details'}

    soup = BeautifulSoup(response.text, 'html.parser')

    details = {
        'license_number': license_number,
        'license_url': license_url
    }

    # Extract license holder
    holder_text = soup.find(string=re.compile(r'Licence Holder'))
    if holder_text:
        holder_parent = holder_text.find_parent('div') or holder_text.find_parent('td')
        if holder_parent:
            # Find next sibling or table cell with the actual name
            next_elem = holder_parent.find_next_sibling()
            if next_elem:
                details['license_holder'] = next_elem.text.strip()

    # Extract DPS
    dps_text = soup.find(string=re.compile(r'Designated Premises Supervisor'))
    if dps_text:
        dps_parent = dps_text.find_parent('div') or dps_text.find_parent('td')
        if dps_parent:
            next_elem = dps_parent.find_next_sibling()
            if next_elem:
                details['dps_name'] = next_elem.text.strip()

    # Extract licensable activities - look for <ul class="Activities">
    activities_list = soup.find('ul', class_='Activities')
    if activities_list:
        activities = activities_list.find_all('li')
        details['licensable_activities'] = [act.text.strip() for act in activities]
    else:
        details['licensable_activities'] = []

    # Extract opening hours - look for <table class="OpenTimes">
    opening_hours_table = soup.find('table', class_='OpenTimes')
    details['opening_hours'] = parse_hours_table(opening_hours_table) if opening_hours_table else []

    # Extract activity hours (alcohol service times) - look for next table after "Times Granted" heading
    activity_heading = soup.find(string=re.compile(r'Activities.*Times Granted'))
    if activity_heading:
        # Find the table that follows this heading
        heading_parent = activity_heading.find_parent(['h3', 'th', 'div'])
        if heading_parent:
            activity_table = heading_parent.find_next('table')
            details['activity_hours'] = parse_hours_table(activity_table) if activity_table else []
        else:
            details['activity_hours'] = []
    else:
        details['activity_hours'] = []

    # Extract conditions
    details['conditions'] = parse_conditions(soup)

    # Extract validity dates
    validity_text = soup.find(string=re.compile(r'Validity:'))
    if validity_text:
        validity_match = re.search(r'(\d{2}/\d{2}/\d{4})\s+to\s+(.+)', validity_text)
        if validity_match:
            details['validity_from'] = validity_match.group(1)
            details['validity_to'] = validity_match.group(2).strip()

    return details

def load_checkpoint() -> Optional[List[Dict]]:
    """Load the most recent checkpoint file if it exists."""
    checkpoint_files = glob.glob('plymouth_licensing_partial_*.json')

    if not checkpoint_files:
        return None

    # Get the most recent checkpoint (highest number)
    checkpoint_files.sort(key=lambda x: int(re.search(r'partial_(\d+)', x).group(1)))
    latest_checkpoint = checkpoint_files[-1]

    print(f"\n✓ Found checkpoint: {latest_checkpoint}")

    with open(latest_checkpoint, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"  Loaded {len(data)} previously scraped premises")
    return data

def scrape_all_premises_details(premises_list: List[Dict], resume: bool = True) -> List[Dict]:
    """Scrape detailed license information for all premises."""
    print("=" * 80)
    print("PHASE 2: Scraping detailed license information")
    print("=" * 80)

    total = len(premises_list)
    results = []
    start_idx = 1

    # Try to resume from checkpoint
    if resume:
        checkpoint_data = load_checkpoint()
        if checkpoint_data:
            results = checkpoint_data
            start_idx = len(results) + 1
            print(f"  Resuming from index {start_idx}/{total}")
            print("=" * 80)

    for idx in range(start_idx, total + 1):
        premises = premises_list[idx - 1]  # Convert to 0-indexed
        premises_id = premises['premises_id']
        name = premises['name']

        print(f"\n[{idx}/{total}] {name} (ID: {premises_id})")

        details = scrape_license_details(premises_id)

        # Combine basic info with detailed license info
        full_data = {
            **premises,
            'scraped_at': datetime.utcnow().isoformat(),
            'details': details if details else {'error': 'No data available'}
        }

        results.append(full_data)

        # Progress indicator
        if idx % 10 == 0:
            print(f"\n{'=' * 80}")
            print(f"Progress: {idx}/{total} ({idx/total*100:.1f}%) - {len(results)} premises processed")
            print(f"{'=' * 80}")

        # Save checkpoint every 50 premises
        if idx % 50 == 0:
            save_to_json(results, f'plymouth_licensing_partial_{idx}.json')
            print(f"  ✓ Checkpoint saved: plymouth_licensing_partial_{idx}.json")

    print(f"\n{'=' * 80}")
    print(f"PHASE 2 COMPLETE: Scraped {len(results)} premises with details")
    print(f"{'=' * 80}\n")

    return results

def save_to_json(data: List[Dict], filename: str):
    """Save data to JSON file with pretty formatting."""
    filepath = f'/workspaces/arckit-test-project-v13-plymouth-research/projects/001-plymouth-research-restaurant-menu-analytics/{filename}'
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\n✓ Saved {len(data)} records to {filename}")

def main():
    """Main scraping workflow."""
    print("\n" + "=" * 80)
    print("PLYMOUTH LICENSING DATABASE SCRAPER")
    print("=" * 80)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    print("ℹ️  CHECKPOINT SYSTEM:")
    print("   - Saves every 50 premises to plymouth_licensing_partial_N.json")
    print("   - Automatically resumes from last checkpoint if run is interrupted")
    print("   - Safe for Codespaces (run in ~45-minute chunks)")
    print("   - Estimated time per 50 premises: ~3-4 minutes")
    print("   - Total estimated time for 2,232 premises: ~2.5-3.5 hours")
    print("=" * 80 + "\n")

    # Phase 1: Get all premises from search results (or load existing)
    import os
    premises_file = 'plymouth_licensing_premises_list.json'

    if os.path.exists(premises_file):
        print(f"✓ Found existing premises list: {premises_file}")
        with open(premises_file, 'r', encoding='utf-8') as f:
            premises_list = json.load(f)
        print(f"  Loaded {len(premises_list)} premises (skipping Phase 1)\n")
    else:
        premises_list = scrape_all_premises_list()

        if not premises_list:
            print("ERROR: No premises found. Exiting.")
            return

        # Save premises list
        save_to_json(premises_list, premises_file)

    # Phase 2: Get detailed license information for each premises
    all_data = scrape_all_premises_details(premises_list)

    # Save final complete dataset
    save_to_json(all_data, 'plymouth_licensing_complete.json')

    # Print summary statistics
    print("\n" + "=" * 80)
    print("SCRAPING COMPLETE - SUMMARY")
    print("=" * 80)
    print(f"Total premises scraped: {len(all_data)}")
    print(f"With license details: {sum(1 for p in all_data if 'license_number' in p.get('details', {}))}")
    print(f"Without license details: {sum(1 for p in all_data if 'error' in p.get('details', {}))}")
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
