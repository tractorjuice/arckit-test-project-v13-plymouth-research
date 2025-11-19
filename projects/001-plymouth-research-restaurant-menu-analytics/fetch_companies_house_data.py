#!/usr/bin/env python3
"""
Companies House Data Fetcher
============================

Matches restaurants to Companies House records to add business intelligence:
- Company registration details
- Company status (active, dissolved, etc.)
- Incorporation date
- Directors
- Company type (Ltd, PLC, etc.)

Uses the free Companies House API.

Author: Plymouth Research Team
Date: 2025-11-19
"""

import sqlite3
import requests
import base64
import time
import csv
import re
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from datetime import datetime
from difflib import SequenceMatcher
import os


# Plymouth postcode areas
PLYMOUTH_POSTCODES = ['PL1', 'PL2', 'PL3', 'PL4', 'PL5', 'PL6', 'PL7', 'PL8', 'PL9']

# API Configuration
API_BASE = "https://api.company-information.service.gov.uk"
RATE_LIMIT_DELAY = 0.5  # 500ms between requests (well under 600/5min limit)


class CompaniesHouseAPI:
    """Wrapper for Companies House API."""

    def __init__(self, api_key: str):
        """Initialize API client."""
        if not api_key:
            raise ValueError("Companies House API key is required")

        # API key is used as username, password is empty
        auth_string = f"{api_key}:"
        self.auth = base64.b64encode(auth_string.encode()).decode()
        self.headers = {
            "Authorization": f"Basic {self.auth}",
            "Accept": "application/json"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def search_companies(self, query: str, items_per_page: int = 20) -> List[Dict]:
        """Search for companies by name."""
        url = f"{API_BASE}/search/companies"
        params = {
            "q": query,
            "items_per_page": items_per_page
        }

        try:
            time.sleep(RATE_LIMIT_DELAY)
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get("items", [])
        except requests.exceptions.RequestException as e:
            print(f"    ⚠️  API Error: {e}")
            return []

    def get_company_details(self, company_number: str) -> Optional[Dict]:
        """Get detailed information for a company."""
        url = f"{API_BASE}/company/{company_number}"

        try:
            time.sleep(RATE_LIMIT_DELAY)
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"    ⚠️  API Error: {e}")
            return None

    def get_company_officers(self, company_number: str) -> List[Dict]:
        """Get directors/officers for a company."""
        url = f"{API_BASE}/company/{company_number}/officers"

        try:
            time.sleep(RATE_LIMIT_DELAY)
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get("items", [])
        except requests.exceptions.RequestException as e:
            print(f"    ⚠️  API Error: {e}")
            return []


def normalize_company_name(name: str) -> str:
    """Normalize company name for matching."""
    normalized = name.lower()

    # Remove location suffixes
    normalized = re.sub(r'\s+(plymouth|barbican|royal william yard|drake circus|city centre|uk)$', '', normalized)

    # Remove common company suffixes for matching
    normalized = re.sub(r'\s+(limited|ltd|plc|llp|llc|restaurant|restaurants|cafe|bar|pub)$', '', normalized)

    # Remove special characters except spaces and ampersands
    normalized = re.sub(r'[^\w\s&]', '', normalized)

    # Normalize whitespace
    normalized = re.sub(r'\s+', ' ', normalized).strip()

    return normalized


def extract_postcode_area(address: str) -> Optional[str]:
    """Extract postcode area (e.g., PL1, PL2) from address."""
    if not address:
        return None

    # UK postcode pattern - capture just the area
    match = re.search(r'\b(PL\d)\s?\d[A-Z]{2}\b', address.upper())
    if match:
        return match.group(1)

    return None


def calculate_match_confidence(
    restaurant_name: str,
    restaurant_address: str,
    company: Dict
) -> Tuple[float, str]:
    """
    Calculate confidence score for a company match.

    Returns: (confidence_score, match_reason)
    """
    confidence = 0.0
    reasons = []

    # Normalize names
    rest_name_norm = normalize_company_name(restaurant_name)
    company_name = company.get("title", "")
    company_name_norm = normalize_company_name(company_name)

    # Name similarity (0-70 points)
    name_similarity = SequenceMatcher(None, rest_name_norm, company_name_norm).ratio()
    name_score = name_similarity * 70
    confidence += name_score

    if name_similarity >= 0.95:
        reasons.append("exact_name")
    elif name_similarity >= 0.80:
        reasons.append("similar_name")
    elif name_similarity >= 0.60:
        reasons.append("partial_name")

    # Postcode area match (30 points)
    rest_postcode = extract_postcode_area(restaurant_address)
    company_address = company.get("address_snippet", "")
    company_postcode = extract_postcode_area(company_address)

    if rest_postcode and company_postcode:
        if rest_postcode == company_postcode:
            confidence += 30
            reasons.append("postcode_match")
        elif rest_postcode[:-1] == company_postcode[:-1]:  # PL1 vs PL2
            confidence += 15
            reasons.append("postcode_nearby")

    # Plymouth area check (10 points if company is in Plymouth)
    if any(pc in company_address.upper() for pc in PLYMOUTH_POSTCODES):
        confidence += 10
        reasons.append("plymouth_area")
    elif "PLYMOUTH" in company_address.upper():
        confidence += 5
        reasons.append("plymouth_mention")

    # Company status (bonus/penalty)
    status = company.get("company_status", "").lower()
    if status == "active":
        confidence += 5
        reasons.append("active")
    elif status in ["dissolved", "liquidation", "administration"]:
        confidence -= 20
        reasons.append(f"status_{status}")

    # SIC codes - restaurants (56101, 56102, 56103, 56210)
    sic_codes = company.get("sic_codes", [])
    if sic_codes:
        restaurant_sic = any(str(code).startswith('561') or str(code).startswith('562') for code in sic_codes)
        if restaurant_sic:
            confidence += 10
            reasons.append("restaurant_sic")

    match_reason = ", ".join(reasons) if reasons else "no_match"

    return confidence, match_reason


def find_best_company_match(
    api: CompaniesHouseAPI,
    restaurant_name: str,
    restaurant_address: str
) -> Tuple[Optional[Dict], float, str]:
    """
    Find the best Companies House match for a restaurant.

    Returns: (best_company, confidence_score, match_reason)
    """
    # Strategy 1: Search with full restaurant name
    search_queries = [
        restaurant_name,
        normalize_company_name(restaurant_name),
    ]

    # Strategy 2: Try without location suffixes
    name_without_location = re.sub(
        r'\s+(plymouth|barbican|royal william yard|drake circus)$',
        '',
        restaurant_name,
        flags=re.IGNORECASE
    ).strip()
    if name_without_location != restaurant_name:
        search_queries.append(name_without_location)

    all_candidates = []

    for query in search_queries:
        if not query:
            continue

        companies = api.search_companies(query, items_per_page=10)

        for company in companies:
            confidence, reason = calculate_match_confidence(
                restaurant_name,
                restaurant_address,
                company
            )

            all_candidates.append({
                "company": company,
                "confidence": confidence,
                "reason": reason,
                "search_query": query
            })

    if not all_candidates:
        return None, 0.0, "no_results"

    # Sort by confidence
    all_candidates.sort(key=lambda x: x["confidence"], reverse=True)
    best = all_candidates[0]

    return best["company"], best["confidence"], best["reason"]


def main():
    """Main execution function."""
    print("=" * 70)
    print("Companies House Data Fetcher")
    print("=" * 70)
    print()

    # Get API key from environment or prompt
    api_key = os.getenv("COMPANIES_HOUSE_API_KEY")
    if not api_key:
        print("⚠️  No API key found in COMPANIES_HOUSE_API_KEY environment variable")
        print()
        print("To get an API key:")
        print("1. Visit: https://developer.company-information.service.gov.uk/")
        print("2. Register for a free account")
        print("3. Create an API key (it's your application's 'API Key')")
        print()
        api_key = input("Enter your Companies House API key: ").strip()

        if not api_key:
            print("❌ API key is required. Exiting.")
            return

    # Initialize API client
    try:
        api = CompaniesHouseAPI(api_key)
        print("✅ Connected to Companies House API")
    except Exception as e:
        print(f"❌ Failed to initialize API: {e}")
        return

    # Connect to database
    db_path = Path(__file__).parent / "plymouth_research.db"
    if not db_path.exists():
        print(f"❌ Database not found: {db_path}")
        return

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    # Get all restaurants
    cursor.execute("""
        SELECT restaurant_id, name, address, google_formatted_address
        FROM restaurants
        WHERE is_active = 1
        ORDER BY name
    """)

    restaurants = cursor.fetchall()
    total = len(restaurants)

    print(f"📊 Processing {total} restaurants")
    print()

    # Results tracking
    high_confidence_matches = []  # >= 70
    medium_confidence_matches = []  # 50-69
    low_confidence_matches = []  # 30-49
    no_matches = []  # < 30

    for i, (rest_id, name, address, google_address) in enumerate(restaurants, 1):
        print(f"[{i}/{total}] {name}")

        # Use google address if available, fallback to address
        search_address = google_address or address or ""

        # Find best match
        company, confidence, reason = find_best_company_match(api, name, search_address)

        result = {
            "restaurant_id": rest_id,
            "restaurant_name": name,
            "restaurant_address": search_address,
            "confidence": confidence,
            "match_reason": reason
        }

        if company:
            result.update({
                "company_number": company.get("company_number"),
                "company_name": company.get("title"),
                "company_status": company.get("company_status"),
                "company_type": company.get("company_type"),
                "incorporation_date": company.get("date_of_creation"),
                "registered_address": company.get("address_snippet"),
                "sic_codes": ", ".join(company.get("sic_codes", []))
            })

            print(f"  ✅ Matched: {company.get('title')}")
            print(f"     Company #: {company.get('company_number')}")
            print(f"     Status: {company.get('company_status')}")
            print(f"     Confidence: {confidence:.1f}% ({reason})")

            if confidence >= 70:
                high_confidence_matches.append(result)
            elif confidence >= 50:
                medium_confidence_matches.append(result)
            else:
                low_confidence_matches.append(result)
        else:
            result.update({
                "company_number": None,
                "company_name": None,
                "company_status": None,
                "company_type": None,
                "incorporation_date": None,
                "registered_address": None,
                "sic_codes": None
            })
            print(f"  ⚠️  No confident match found (best: {confidence:.1f}%)")
            no_matches.append(result)

        print()

    # Export results to CSV
    print()
    print("=" * 70)
    print("📄 Exporting results...")
    print("=" * 70)
    print()

    fieldnames = [
        "restaurant_id", "restaurant_name", "restaurant_address",
        "company_number", "company_name", "company_status", "company_type",
        "incorporation_date", "registered_address", "sic_codes",
        "confidence", "match_reason"
    ]

    if high_confidence_matches:
        with open("companies_high_confidence.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(high_confidence_matches)
        print(f"✅ Exported {len(high_confidence_matches)} high confidence matches to: companies_high_confidence.csv")

    if medium_confidence_matches:
        with open("companies_medium_confidence.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(medium_confidence_matches)
        print(f"⚠️  Exported {len(medium_confidence_matches)} medium confidence matches to: companies_medium_confidence.csv")

    if low_confidence_matches:
        with open("companies_low_confidence.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(low_confidence_matches)
        print(f"⚠️  Exported {len(low_confidence_matches)} low confidence matches to: companies_low_confidence.csv")

    if no_matches:
        with open("companies_no_match.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(no_matches)
        print(f"❌ Exported {len(no_matches)} no matches to: companies_no_match.csv")

    print()
    print("=" * 70)
    print("✅ Companies House Fetch Complete!")
    print("=" * 70)
    print()
    print("📊 Results Summary:")
    print(f"   • High confidence (≥70%): {len(high_confidence_matches)} ({len(high_confidence_matches)/total*100:.1f}%)")
    print(f"   • Medium confidence (50-69%): {len(medium_confidence_matches)} ({len(medium_confidence_matches)/total*100:.1f}%)")
    print(f"   • Low confidence (30-49%): {len(low_confidence_matches)} ({len(low_confidence_matches)/total*100:.1f}%)")
    print(f"   • No match (<30%): {len(no_matches)} ({len(no_matches)/total*100:.1f}%)")
    print()
    print("📝 Next Steps:")
    print("   1. Review companies_high_confidence.csv - safe to import")
    print("   2. Review companies_medium_confidence.csv - manual verification recommended")
    print("   3. Review companies_low_confidence.csv - likely incorrect matches")
    print("   4. companies_no_match.csv - may be sole traders or trading names")
    print()
    print("To import high confidence matches to database, run:")
    print("   python import_companies_house_data.py")

    conn.close()


if __name__ == "__main__":
    main()
