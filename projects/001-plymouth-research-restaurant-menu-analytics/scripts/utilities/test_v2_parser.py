#!/usr/bin/env python3
"""Quick test of v2 parser on Honky Tonks"""

import sqlite3
import requests
import base64
from pathlib import Path
from fetch_balance_sheets_v2 import get_latest_filing, download_ixbrl, parse_balance_sheet_both_years, calculate_financial_performance

DB_PATH = Path(__file__).parent / "plymouth_research.db"

# Get Honky Tonks
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("SELECT restaurant_id, name, company_number FROM restaurants WHERE name = 'Honky Tonk Wine Library'")
result = cursor.fetchone()
conn.close()

if result:
    restaurant_id, name, company_number = result
    print(f"Testing: {name} ({company_number})")
    print("-" * 80)

    # Get filing
    filing = get_latest_filing(company_number)
    if filing:
        print(f"Filing: {filing['date']} (period end: {filing['period_end']})")

        # Download iXBRL
        ixbrl = download_ixbrl(filing['document_url'])
        if ixbrl:
            print(f"Downloaded: {len(ixbrl)} bytes")

            # Parse both years
            current, prior = parse_balance_sheet_both_years(ixbrl)

            print(f"\nCurrent Year Data ({len(current)} metrics):")
            for key, value in sorted(current.items()):
                print(f"  {key}: £{value:,}")

            print(f"\nPrior Year Data ({len(prior)} metrics):")
            for key, value in sorted(prior.items()):
                print(f"  {key}: £{value:,}")

            # Calculate performance
            if current and prior:
                performance = calculate_financial_performance(current, prior)
                print(f"\nPerformance Metrics:")
                print(f"  Rating: {performance['financial_rating']} ({performance['rating_description']})")
                print(f"  Score: {performance['financial_health_score']}/100")
                print(f"  Net Assets Change: £{performance['net_assets_change_gbp']:,} ({performance['net_assets_change_pct']:+.1f}%)")
