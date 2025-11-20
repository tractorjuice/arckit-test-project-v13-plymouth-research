#!/usr/bin/env python3
"""
Fetch Balance Sheet Data for All Companies
==========================================

Downloads and parses iXBRL accounts to extract financial metrics.

Author: Plymouth Research Team
Date: 2025-11-20
"""

import sqlite3
import requests
import base64
import time
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup
import re
import csv

# Configuration
DB_PATH = Path(__file__).parent / "plymouth_research.db"
API_KEY = "8aca0fb0-82ea-4cc0-b0c3-ae3c859a7dfa"
RATE_LIMIT_DELAY = 1.0  # 1 second between requests

# Encode API key
auth_string = f"{API_KEY}:"
auth_base64 = base64.b64encode(auth_string.encode('ascii')).decode('ascii')

headers = {
    "Authorization": f"Basic {auth_base64}",
    "Accept": "application/json"
}

def get_companies():
    """Get all companies with company numbers from database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT restaurant_id, name, company_number, company_name
        FROM restaurants
        WHERE company_number IS NOT NULL
        ORDER BY name
    """)

    companies = cursor.fetchall()
    conn.close()

    return companies

def get_latest_filing(company_number):
    """Get latest accounts filing for a company."""
    url = f"https://api.company-information.service.gov.uk/company/{company_number}/filing-history"

    try:
        response = requests.get(url, headers=headers, params={"category": "accounts"}, timeout=10)

        if response.status_code == 200:
            filing_history = response.json()
            items = filing_history.get('items', [])

            if items:
                latest = items[0]
                return {
                    'transaction_id': latest.get('transaction_id'),
                    'date': latest.get('date'),
                    'type': latest.get('type'),
                    'description': latest.get('description'),
                    'period_end': latest.get('description_values', {}).get('made_up_date'),
                    'document_url': latest.get('links', {}).get('document_metadata')
                }

        return None

    except Exception as e:
        print(f"  ⚠️  Error fetching filing history: {e}")
        return None

def download_ixbrl(document_url):
    """Download iXBRL document."""
    if not document_url:
        return None

    # Get content URL
    content_url = document_url + "/content"

    ixbrl_headers = {
        "Authorization": f"Basic {auth_base64}",
        "Accept": "application/xhtml+xml"
    }

    try:
        response = requests.get(content_url, headers=ixbrl_headers, timeout=15)

        if response.status_code == 200:
            return response.content

        return None

    except Exception as e:
        print(f"  ⚠️  Error downloading iXBRL: {e}")
        return None

def parse_balance_sheet(ixbrl_content):
    """Parse balance sheet data from iXBRL."""
    if not ixbrl_content:
        return {}

    soup = BeautifulSoup(ixbrl_content, 'html.parser')

    # Find all XBRL tags
    xbrl_tags = soup.find_all(['ix:nonfraction', 'ix:nonnumeric'])

    financial_data = {}

    # Map of XBRL tag names to our field names
    field_mapping = {
        'FixedAssets': 'fixed_assets',
        'CurrentAssets': 'current_assets',
        'NetCurrentAssetsLiabilities': 'net_current_assets',
        'TotalAssetsLessCurrentLiabilities': 'total_assets',
        'NetAssetsLiabilities': 'net_assets',
        'Equity': 'shareholders_equity',
        'Turnover': 'turnover',
        'GrossProfit': 'gross_profit',
        'OperatingProfit': 'operating_profit',
        'ProfitLoss': 'profit_loss',
        'AverageNumberEmployeesDuringPeriod': 'employees',
    }

    for tag in xbrl_tags:
        name = tag.get('name', '')
        value_text = tag.get_text(strip=True)

        # Try to match field names
        for xbrl_name, our_name in field_mapping.items():
            if xbrl_name in name:
                # Parse numeric value
                try:
                    # Remove commas and convert to int
                    if value_text and value_text != '-':
                        clean_value = value_text.replace(',', '').replace('£', '').strip()
                        if clean_value:
                            financial_data[our_name] = int(clean_value)
                except (ValueError, AttributeError):
                    pass

    return financial_data

def create_financial_columns(cursor):
    """Add financial data columns to restaurants table."""
    new_columns = [
        ("fixed_assets_gbp", "INTEGER"),
        ("current_assets_gbp", "INTEGER"),
        ("net_current_assets_gbp", "INTEGER"),
        ("total_assets_gbp", "INTEGER"),
        ("net_assets_gbp", "INTEGER"),
        ("shareholders_equity_gbp", "INTEGER"),
        ("turnover_gbp", "INTEGER"),
        ("gross_profit_gbp", "INTEGER"),
        ("operating_profit_gbp", "INTEGER"),
        ("profit_loss_gbp", "INTEGER"),
        ("employees", "INTEGER"),
        ("accounts_period_end", "TEXT"),
        ("financial_data_fetched_at", "TEXT"),
    ]

    for col_name, col_type in new_columns:
        try:
            cursor.execute(f"ALTER TABLE restaurants ADD COLUMN {col_name} {col_type}")
            print(f"  ✅ Added column: {col_name}")
        except sqlite3.OperationalError as e:
            if "duplicate column" in str(e).lower():
                pass  # Column already exists
            else:
                raise

def main():
    """Main execution."""
    print("=" * 80)
    print("FETCH BALANCE SHEET DATA FOR ALL COMPANIES")
    print("=" * 80)
    print()

    # Get companies
    companies = get_companies()
    print(f"📊 Found {len(companies)} companies with company numbers\n")

    # Create database columns
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("🔧 Creating database columns...")
    create_financial_columns(cursor)
    conn.commit()
    print()

    # Results tracking
    results = []
    success_count = 0
    error_count = 0

    # Process each company
    for idx, (restaurant_id, name, company_number, company_name) in enumerate(companies, 1):
        print(f"[{idx}/{len(companies)}] {name}")
        print(f"  Company: {company_name} ({company_number})")

        result = {
            'restaurant_id': restaurant_id,
            'name': name,
            'company_number': company_number,
            'status': 'error',
            'error': None
        }

        try:
            # Get latest filing
            time.sleep(RATE_LIMIT_DELAY)
            filing = get_latest_filing(company_number)

            if not filing:
                result['error'] = 'No filings found'
                print("  ⚠️  No accounts filings found")
                error_count += 1
                results.append(result)
                print()
                continue

            print(f"  📄 Latest filing: {filing['date']} (period end: {filing['period_end']})")

            # Download iXBRL
            time.sleep(RATE_LIMIT_DELAY)
            ixbrl_content = download_ixbrl(filing['document_url'])

            if not ixbrl_content:
                result['error'] = 'Could not download iXBRL'
                print("  ⚠️  Could not download iXBRL document")
                error_count += 1
                results.append(result)
                print()
                continue

            # Parse balance sheet
            financial_data = parse_balance_sheet(ixbrl_content)

            if not financial_data:
                result['error'] = 'No financial data found'
                print("  ⚠️  No financial data found in document")
                error_count += 1
                results.append(result)
                print()
                continue

            # Display what we found
            print(f"  ✅ Found {len(financial_data)} financial metrics:")
            for key, value in financial_data.items():
                print(f"     {key}: £{value:,}")

            # Update database
            update_fields = []
            update_values = []

            for key, value in financial_data.items():
                update_fields.append(f"{key}_gbp = ?" if key != 'employees' else f"{key} = ?")
                update_values.append(value)

            # Add period end and fetch timestamp
            update_fields.append("accounts_period_end = ?")
            update_values.append(filing['period_end'])

            update_fields.append("financial_data_fetched_at = ?")
            update_values.append(datetime.now().isoformat())

            # Add restaurant_id for WHERE clause
            update_values.append(restaurant_id)

            sql = f"""
                UPDATE restaurants
                SET {', '.join(update_fields)}
                WHERE restaurant_id = ?
            """

            cursor.execute(sql, update_values)
            conn.commit()

            result['status'] = 'success'
            result.update(financial_data)
            result['period_end'] = filing['period_end']

            success_count += 1
            print(f"  ✅ Updated database")

        except Exception as e:
            result['error'] = str(e)
            print(f"  ❌ Error: {e}")
            error_count += 1

        results.append(result)
        print()

    conn.close()

    # Export results to CSV
    print("=" * 80)
    print("EXPORTING RESULTS")
    print("=" * 80)
    print()

    csv_file = "balance_sheet_results.csv"

    with open(csv_file, 'w', newline='') as f:
        fieldnames = ['restaurant_id', 'name', 'company_number', 'status',
                     'fixed_assets', 'current_assets', 'net_assets',
                     'shareholders_equity', 'turnover', 'profit_loss',
                     'employees', 'period_end', 'error']

        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for result in results:
            writer.writerow(result)

    print(f"✅ Exported results to: {csv_file}")
    print()

    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()
    print(f"📊 Total companies processed: {len(companies)}")
    print(f"✅ Successful: {success_count} ({success_count/len(companies)*100:.1f}%)")
    print(f"❌ Errors: {error_count} ({error_count/len(companies)*100:.1f}%)")
    print()

    # Breakdown by data availability
    has_turnover = sum(1 for r in results if r.get('turnover'))
    has_profit = sum(1 for r in results if r.get('profit_loss'))
    has_employees = sum(1 for r in results if r.get('employees'))
    has_assets = sum(1 for r in results if r.get('net_assets'))

    print("📈 Data Coverage:")
    print(f"  Net Assets: {has_assets}/{len(companies)} ({has_assets/len(companies)*100:.1f}%)")
    print(f"  Turnover: {has_turnover}/{len(companies)} ({has_turnover/len(companies)*100:.1f}%)")
    print(f"  Profit/Loss: {has_profit}/{len(companies)} ({has_profit/len(companies)*100:.1f}%)")
    print(f"  Employees: {has_employees}/{len(companies)} ({has_employees/len(companies)*100:.1f}%)")
    print()
    print("=" * 80)

if __name__ == "__main__":
    main()
