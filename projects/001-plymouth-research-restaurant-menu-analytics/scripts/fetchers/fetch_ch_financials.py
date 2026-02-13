#!/usr/bin/env python3
"""
Fetch Companies House financial data for matched restaurants.

For each restaurant with a company_number, fetches:
- Company profile (SIC codes, accounts dates, status)
- Filing history to find latest accounts
- Accounts document data where available

Uses the free Companies House REST API.
Rate limit: 600 requests per 5 minutes (we use 0.6s delay).
"""

import sqlite3
import requests
import time
import json
import sys
from datetime import datetime, timezone

DB_PATH = "plymouth_research.db"
API_BASE = "https://api.company-information.service.gov.uk"
RATE_DELAY = 0.6  # seconds between requests


class CHClient:
    def __init__(self, api_key):
        self.session = requests.Session()
        self.session.auth = (api_key, '')
        self.session.headers['Accept'] = 'application/json'
        self.request_count = 0

    def get(self, path):
        time.sleep(RATE_DELAY)
        self.request_count += 1
        try:
            r = self.session.get(f"{API_BASE}{path}", timeout=15)
            if r.status_code == 200:
                return r.json()
            elif r.status_code == 429:
                print("    Rate limited, waiting 60s...")
                time.sleep(60)
                return self.get(path)
            else:
                return None
        except requests.RequestException as e:
            print(f"    Error: {e}")
            return None


def get_latest_accounts_filing(client, company_number):
    """Find the most recent accounts filing."""
    data = client.get(f"/company/{company_number}/filing-history?category=accounts&items_per_page=5")
    if not data or not data.get('items'):
        return None

    for item in data['items']:
        if item.get('category') == 'accounts':
            return item
    return None


def parse_accounts_type(description):
    """Determine accounts type from filing description."""
    if not description:
        return 'unknown'
    desc = description.lower()
    if 'micro' in desc:
        return 'micro'
    elif 'small' in desc or 'abbreviated' in desc:
        return 'small'
    elif 'full' in desc or 'total exemption' in desc:
        return 'total_exemption'
    elif 'dormant' in desc:
        return 'dormant'
    elif 'group' in desc:
        return 'group'
    return 'other'


def main():
    if len(sys.argv) < 2:
        print("Usage: python fetch_ch_financials.py <API_KEY>")
        sys.exit(1)

    api_key = sys.argv[1]
    client = CHClient(api_key)

    # Test connectivity
    test = client.get("/company/10384298")
    if not test:
        print("API connection failed")
        sys.exit(1)
    print("API connected successfully\n")

    conn = sqlite3.connect(DB_PATH)

    # Get all restaurants with company numbers
    rows = conn.execute("""
        SELECT restaurant_id, name, company_number, company_name
        FROM restaurants
        WHERE company_number IS NOT NULL AND company_number != ''
        ORDER BY restaurant_id
    """).fetchall()

    print(f"{'=' * 60}")
    print(f"Companies House Financial Data Fetch")
    print(f"{'=' * 60}")
    print(f"Restaurants with company numbers: {len(rows)}")
    print(f"Estimated time: ~{len(rows) * 1.5 / 60:.1f} minutes")
    print(f"{'=' * 60}\n")

    updated = 0
    skipped = 0
    no_accounts = 0
    errors = 0

    for i, (rid, name, co_num, co_name) in enumerate(rows, 1):
        print(f"[{i}/{len(rows)}] {name} ({co_num})")

        # Fetch company profile
        profile = client.get(f"/company/{co_num}")
        if not profile:
            print("    No profile found")
            errors += 1
            continue

        # Extract profile data
        sic_codes = ', '.join(profile.get('sic_codes', []))
        company_status = profile.get('company_status', '')
        company_type = profile.get('company_type', '')
        incorporation_date = profile.get('date_of_creation', '')
        registered_address = profile.get('registered_office_address', {})
        addr_parts = [
            registered_address.get('address_line_1', ''),
            registered_address.get('address_line_2', ''),
            registered_address.get('locality', ''),
            registered_address.get('postal_code', ''),
        ]
        reg_addr = ', '.join(p for p in addr_parts if p)

        accounts_info = profile.get('accounts', {})
        next_due = accounts_info.get('next_due', '')
        last_accounts = accounts_info.get('last_accounts', {})
        accounts_made_up_to = last_accounts.get('made_up_to', '')
        accounts_type = last_accounts.get('type', '')

        has_charges = profile.get('has_charges', False)
        has_insolvency = profile.get('has_insolvency_history', False)

        # Update basic profile data
        conn.execute("""
            UPDATE restaurants SET
                company_status = ?,
                company_type = ?,
                incorporation_date = ?,
                company_registered_address = ?,
                company_sic_codes = ?,
                financial_data_fetched_at = ?
            WHERE restaurant_id = ?
        """, (
            company_status, company_type, incorporation_date,
            reg_addr, sic_codes,
            datetime.now(timezone.utc).isoformat(),
            rid
        ))

        # Try to update accounts_period_end if we have it
        if accounts_made_up_to:
            conn.execute("""
                UPDATE restaurants SET accounts_period_end = ?
                WHERE restaurant_id = ?
            """, (accounts_made_up_to, rid))

        print(f"    Status: {company_status} | SIC: {sic_codes} | Accounts to: {accounts_made_up_to}")

        # Fetch latest accounts filing for more detail
        filing = get_latest_accounts_filing(client, co_num)
        if filing:
            filing_type = parse_accounts_type(filing.get('description', ''))
            filing_date = filing.get('date', '')
            print(f"    Latest filing: {filing_date} ({filing_type})")
        else:
            no_accounts += 1
            print("    No accounts filings found")

        # Check for insolvency/charges flags
        if has_insolvency:
            print(f"    WARNING: Has insolvency history")
        if has_charges:
            pass  # Common for companies with loans, not noteworthy

        updated += 1

    conn.commit()

    # Now calculate financial health scores based on available data
    print(f"\n{'=' * 60}")
    print("Calculating financial health scores...")
    print(f"{'=' * 60}\n")

    # Score based on: active status, has accounts, not dissolved, not insolvent
    restaurants = conn.execute("""
        SELECT restaurant_id, company_status, company_type, accounts_period_end,
               turnover_gbp, net_assets_gbp, profit_loss_gbp
        FROM restaurants
        WHERE company_number IS NOT NULL AND company_number != ''
    """).fetchall()

    scored = 0
    for row in restaurants:
        rid, status, co_type, acct_end, turnover, net_assets, profit = row
        score = 50  # Base score

        # Status scoring
        if status == 'active':
            score += 20
        elif status == 'dissolved':
            score -= 30
        elif status in ('liquidation', 'administration'):
            score -= 40

        # Has recent accounts
        if acct_end:
            try:
                acct_date = datetime.strptime(acct_end, '%Y-%m-%d')
                months_old = (datetime.now() - acct_date).days / 30
                if months_old < 18:
                    score += 15  # Recent accounts
                elif months_old < 30:
                    score += 5
                else:
                    score -= 10  # Very old accounts
            except ValueError:
                pass

        # Financial data (if available)
        if net_assets and net_assets > 0:
            score += 10
        elif net_assets and net_assets < 0:
            score -= 15  # Negative net assets

        if profit and profit > 0:
            score += 5

        # Clamp to 0-100
        score = max(0, min(100, score))

        # Rating
        if score >= 80:
            rating = 'Strong'
        elif score >= 60:
            rating = 'Good'
        elif score >= 40:
            rating = 'Fair'
        elif score >= 20:
            rating = 'Weak'
        else:
            rating = 'Critical'

        conn.execute("""
            UPDATE restaurants SET financial_health_score = ?, financial_rating = ?
            WHERE restaurant_id = ?
        """, (score, rating, rid))
        scored += 1

    conn.commit()

    # Summary
    print(f"\n{'=' * 60}")
    print(f"RESULTS")
    print(f"{'=' * 60}")
    print(f"Profiles fetched:  {updated}/{len(rows)}")
    print(f"No accounts:       {no_accounts}")
    print(f"Errors:            {errors}")
    print(f"Health scores:     {scored}")
    print(f"API requests:      {client.request_count}")

    # Show status breakdown
    cursor = conn.execute("""
        SELECT company_status, COUNT(*) FROM restaurants
        WHERE company_number IS NOT NULL AND company_number != ''
        GROUP BY company_status ORDER BY COUNT(*) DESC
    """)
    print(f"\nCompany status breakdown:")
    for row in cursor:
        print(f"  {row[0] or 'unknown'}: {row[1]}")

    # Show health score breakdown
    cursor = conn.execute("""
        SELECT financial_rating, COUNT(*), ROUND(AVG(financial_health_score), 1)
        FROM restaurants
        WHERE financial_health_score IS NOT NULL
        GROUP BY financial_rating ORDER BY AVG(financial_health_score) DESC
    """)
    print(f"\nFinancial health distribution:")
    for row in cursor:
        print(f"  {row[0]}: {row[1]} restaurants (avg score: {row[2]})")

    # Show SIC code breakdown
    cursor = conn.execute("""
        SELECT company_sic_codes, COUNT(*) FROM restaurants
        WHERE company_sic_codes IS NOT NULL AND company_sic_codes != ''
        GROUP BY company_sic_codes ORDER BY COUNT(*) DESC LIMIT 10
    """)
    print(f"\nTop SIC codes:")
    for row in cursor:
        print(f"  {row[0]}: {row[1]}")

    conn.close()
    print(f"\nDone.")


if __name__ == "__main__":
    main()
