#!/usr/bin/env python3
"""
Fetch Directors from Companies House
=====================================

Fetches director information for companies in the database.

Author: Plymouth Research Team
Date: 2025-11-19
"""

import sqlite3
import requests
import base64
import time
import os
from pathlib import Path
from typing import List, Dict
import json


# API Configuration
API_BASE = "https://api.company-information.service.gov.uk"
RATE_LIMIT_DELAY = 0.5  # 500ms between requests


class CompaniesHouseAPI:
    """Wrapper for Companies House API."""

    def __init__(self, api_key: str):
        """Initialize API client."""
        if not api_key:
            raise ValueError("Companies House API key is required")

        auth_string = f"{api_key}:"
        self.auth = base64.b64encode(auth_string.encode()).decode()
        self.headers = {
            "Authorization": f"Basic {self.auth}",
            "Accept": "application/json"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

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


def create_directors_table(cursor):
    """Create directors table if it doesn't exist."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS company_directors (
            director_id INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurant_id INTEGER NOT NULL,
            company_number TEXT NOT NULL,
            director_name TEXT NOT NULL,
            officer_role TEXT,
            appointed_date TEXT,
            resigned_date TEXT,
            nationality TEXT,
            occupation TEXT,
            date_of_birth TEXT,
            fetched_at TEXT NOT NULL,
            FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id)
        )
    """)

    # Create index for faster lookups
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_directors_restaurant
        ON company_directors(restaurant_id)
    """)


def main():
    """Main execution function."""
    print("=" * 70)
    print("Fetch Directors from Companies House")
    print("=" * 70)
    print()

    # Get API key
    api_key = os.getenv("COMPANIES_HOUSE_API_KEY")
    if not api_key:
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
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    # Create directors table
    print("📊 Creating directors table...")
    create_directors_table(cursor)
    conn.commit()
    print("✅ Directors table ready")
    print()

    # Get all restaurants with company numbers
    cursor.execute("""
        SELECT restaurant_id, name, company_number, company_name
        FROM restaurants
        WHERE company_number IS NOT NULL
        ORDER BY name
    """)

    restaurants = cursor.fetchall()
    total = len(restaurants)

    print(f"📊 Processing {total} companies")
    print()

    total_directors = 0
    companies_with_directors = 0

    for i, (rest_id, name, company_number, company_name) in enumerate(restaurants, 1):
        print(f"[{i}/{total}] {name}")
        print(f"  Company: {company_name} ({company_number})")

        # Check if we already have directors for this company
        cursor.execute("""
            SELECT COUNT(*) FROM company_directors
            WHERE restaurant_id = ?
        """, (rest_id,))

        existing_count = cursor.fetchone()[0]
        if existing_count > 0:
            print(f"  ✓ Already have {existing_count} directors")
            print()
            total_directors += existing_count
            companies_with_directors += 1
            continue

        # Fetch directors
        officers = api.get_company_officers(company_number)

        if officers:
            # Filter to active directors only
            active_officers = [
                o for o in officers
                if o.get('resigned_on') is None
            ]

            print(f"  ✅ Found {len(active_officers)} active directors")

            for officer in active_officers:
                # Extract date of birth (year and month only for privacy)
                dob = officer.get('date_of_birth', {})
                dob_str = None
                if dob:
                    year = dob.get('year')
                    month = dob.get('month')
                    if year and month:
                        dob_str = f"{year}-{month:02d}"

                cursor.execute("""
                    INSERT INTO company_directors (
                        restaurant_id, company_number, director_name,
                        officer_role, appointed_date, resigned_date,
                        nationality, occupation, date_of_birth, fetched_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
                """, (
                    rest_id,
                    company_number,
                    officer.get('name', 'Unknown'),
                    officer.get('officer_role', ''),
                    officer.get('appointed_on', ''),
                    officer.get('resigned_on', ''),
                    officer.get('nationality', ''),
                    officer.get('occupation', ''),
                    dob_str
                ))

                director_name = officer.get('name', 'Unknown')
                role = officer.get('officer_role', 'Director')
                print(f"    • {director_name} ({role})")

            total_directors += len(active_officers)
            companies_with_directors += 1
        else:
            print(f"  ⚠️  No directors found")

        print()

    conn.commit()

    print()
    print("=" * 70)
    print("✅ Directors Fetch Complete!")
    print("=" * 70)
    print()
    print("📊 Results:")
    print(f"   • Companies processed: {total}")
    print(f"   • Companies with directors: {companies_with_directors}")
    print(f"   • Total directors found: {total_directors}")
    print(f"   • Average directors per company: {total_directors/companies_with_directors:.1f}")
    print()

    conn.close()


if __name__ == "__main__":
    main()
