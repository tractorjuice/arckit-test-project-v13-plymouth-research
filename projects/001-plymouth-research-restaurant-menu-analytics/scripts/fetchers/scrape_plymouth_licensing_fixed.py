#!/usr/bin/env python3
"""
Plymouth Licensing Database Scraper - FIXED VERSION

Fixes the DPS name extraction bug where footer text was being captured
instead of the actual Designated Premises Supervisor name.

Key improvements:
- Multiple extraction strategies for DPS and license holder
- Footer text filtering
- Better table row parsing
- More robust error handling
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

# Footer text patterns to filter out
FOOTER_PATTERNS = [
    r'Copyright.*Idox',
    r'Terms and Conditions',
    r'Version \d+\.\d+',
    r'Privacy Policy',
    r'© \d{4}'
]

def is_footer_text(text: str) -> bool:
    """Check if text is likely from page footer."""
    if not text:
        return True

    text_clean = text.strip()

    # Too long to be a name
    if len(text_clean) > 200:
        return True

    # Check for footer patterns
    for pattern in FOOTER_PATTERNS:
        if re.search(pattern, text_clean, re.IGNORECASE):
            return True

    # Empty or just whitespace
    if not text_clean or text_clean.isspace():
        return True

    return False

def extract_text_from_label(soup, label_pattern: str) -> Optional[str]:
    """
    Extract text associated with a label using multiple strategies.

    Strategies:
    1. Look for label in table row, get next cell value
    2. Look for label in div, get next sibling (with footer filtering)
    3. Look for label followed by colon, extract text after it
    """
    # Strategy 1: Table row structure
    label_text = soup.find(string=re.compile(label_pattern))
    if label_text:
        # Check if it's in a table row
        tr = label_text.find_parent('tr')
        if tr:
            tds = tr.find_all('td')
            if len(tds) >= 2:
                # First td is label, second is value
                for i, td in enumerate(tds):
                    if re.search(label_pattern, td.get_text(), re.IGNORECASE):
                        if i + 1 < len(tds):
                            value = tds[i + 1].get_text().strip()
                            if not is_footer_text(value):
                                return value

        # Strategy 2: Div/TD with next sibling (with footer filtering)
        parent = label_text.find_parent('div') or label_text.find_parent('td')
        if parent:
            next_elem = parent.find_next_sibling()
            if next_elem:
                value = next_elem.get_text().strip()
                if not is_footer_text(value):
                    return value

        # Strategy 3: Look for text pattern like "Label: Value"
        # Find parent block and extract text after the label
        parent_block = label_text.find_parent(['div', 'p', 'section'])
        if parent_block:
            full_text = parent_block.get_text()
            match = re.search(rf'{label_pattern}\s*:\s*(.+?)(?:\n|$)', full_text, re.IGNORECASE)
            if match:
                value = match.group(1).strip()
                if not is_footer_text(value):
                    return value

    return None

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

    # Extract license holder - FIXED VERSION
    holder = extract_text_from_label(soup, r'Licence Holder')
    if holder:
        details['license_holder'] = holder

    # Extract DPS - FIXED VERSION
    dps = extract_text_from_label(soup, r'Designated Premises Supervisor')
    if dps:
        details['dps_name'] = dps

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
    checkpoint_files = glob.glob('plymouth_licensing_fixed_partial_*.json')

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
            'scraped_at': datetime.now().isoformat(),
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
            save_to_json(results, f'plymouth_licensing_fixed_partial_{idx}.json')
            print(f"  ✓ Checkpoint saved: plymouth_licensing_fixed_partial_{idx}.json")

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
    print("PLYMOUTH LICENSING DATABASE SCRAPER - FIXED VERSION")
    print("=" * 80)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    print("🔧 IMPROVEMENTS:")
    print("   - Fixed DPS name extraction (filters out footer text)")
    print("   - Fixed license holder extraction")
    print("   - Multiple extraction strategies for robustness")
    print("   - Better error handling and validation")
    print()
    print("ℹ️  CHECKPOINT SYSTEM:")
    print("   - Saves every 50 premises to plymouth_licensing_fixed_partial_N.json")
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
    save_to_json(all_data, 'plymouth_licensing_complete_fixed.json')

    # Print summary statistics
    print("\n" + "=" * 80)
    print("SCRAPING COMPLETE - SUMMARY")
    print("=" * 80)
    print(f"Total premises scraped: {len(all_data)}")

    with_license = sum(1 for p in all_data if 'license_number' in p.get('details', {}))
    with_dps = sum(1 for p in all_data if 'dps_name' in p.get('details', {}))
    with_holder = sum(1 for p in all_data if 'license_holder' in p.get('details', {}))

    print(f"With license details: {with_license}")
    print(f"With DPS name: {with_dps}")
    print(f"With license holder: {with_holder}")
    print(f"Without license details: {sum(1 for p in all_data if 'error' in p.get('details', {}))}")
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
