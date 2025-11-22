#!/usr/bin/env python3
"""
Fetch Balance Sheet Data for All Companies - Version 2
=======================================================

Downloads and parses iXBRL accounts to extract financial metrics for BOTH
current and prior years, calculates year-over-year changes, and assigns
financial performance ratings.

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

def parse_balance_sheet_both_years(ixbrl_content):
    """Parse balance sheet data from iXBRL for BOTH current and prior years."""
    if not ixbrl_content:
        return {}, {}

    soup = BeautifulSoup(ixbrl_content, 'html.parser')

    # Step 1: Parse all context definitions to build date mappings
    context_dates = {}
    contexts = soup.find_all('xbrli:context')

    for ctx in contexts:
        ctx_id = ctx.get('id', '')

        # Get instant date (for balance sheet items) - represents a point in time
        instant = ctx.find('xbrli:instant')
        if instant:
            date_str = instant.get_text(strip=True)
            try:
                context_dates[ctx_id] = {'instant': datetime.fromisoformat(date_str.replace('Z', '+00:00')), 'type': 'instant'}
            except:
                pass

        # Get period end date (for P&L items) - represents end of a duration
        period_end = ctx.find('xbrli:enddate')
        if period_end:
            date_str = period_end.get_text(strip=True)
            try:
                context_dates[ctx_id] = {'endDate': datetime.fromisoformat(date_str.replace('Z', '+00:00')), 'type': 'period'}
            except:
                pass

    # Step 2: Identify current and prior year contexts by finding the two most recent dates
    if not context_dates:
        return {}, {}

    # Get all unique dates (both instant and endDate)
    all_dates = []
    for ctx_id, date_info in context_dates.items():
        if 'instant' in date_info:
            all_dates.append((date_info['instant'], ctx_id))
        elif 'endDate' in date_info:
            all_dates.append((date_info['endDate'], ctx_id))

    if not all_dates:
        return {}, {}

    # Sort by date (most recent first)
    all_dates.sort(reverse=True)

    # Group contexts by date
    date_groups = {}
    for date, ctx_id in all_dates:
        date_key = date.strftime('%Y-%m-%d')
        if date_key not in date_groups:
            date_groups[date_key] = []
        date_groups[date_key].append(ctx_id)

    # Get the two most recent dates (current year and prior year)
    sorted_dates = sorted(date_groups.keys(), reverse=True)

    current_year_contexts = set()
    prior_year_contexts = set()

    if len(sorted_dates) >= 1:
        current_year_contexts = set(date_groups[sorted_dates[0]])
    if len(sorted_dates) >= 2:
        prior_year_contexts = set(date_groups[sorted_dates[1]])

    # Step 3: Parse financial data tags using context mappings
    xbrl_tags = soup.find_all(['ix:nonfraction', 'ix:nonnumeric'])

    current_year_data = {}
    prior_year_data = {}

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
        context_ref = tag.get('contextref', '')
        value_text = tag.get_text(strip=True)
        sign_attr = tag.get('sign', '')

        # Determine if this is current or prior year based on context date mapping
        is_current_year = context_ref in current_year_contexts
        is_prior_year = context_ref in prior_year_contexts

        if not (is_current_year or is_prior_year):
            continue

        # Try to match field names
        for xbrl_name, our_name in field_mapping.items():
            if xbrl_name in name:
                # Parse numeric value
                try:
                    # Remove commas and convert to int
                    if value_text and value_text != '-':
                        clean_value = value_text.replace(',', '').replace('£', '').strip()
                        if clean_value:
                            value = int(clean_value)

                            # Handle sign attribute (e.g., sign="-" means negate the value)
                            if sign_attr == '-':
                                value = -value

                            if is_current_year:
                                current_year_data[our_name] = value
                            elif is_prior_year:
                                prior_year_data[our_name] = value
                except (ValueError, AttributeError):
                    pass

    return current_year_data, prior_year_data

def calculate_financial_performance(current, prior):
    """
    Calculate financial performance score and rating.

    Returns dict with:
    - net_assets_change: absolute change
    - net_assets_change_pct: percentage change
    - employee_change: absolute change
    - financial_health_score: 0-100 score
    - financial_rating: A-F rating
    - rating_description: text description
    """
    metrics = {}

    # Calculate net assets change
    current_net_assets = current.get('net_assets', 0)
    prior_net_assets = prior.get('net_assets', 0)

    if prior_net_assets != 0:
        metrics['net_assets_change_gbp'] = current_net_assets - prior_net_assets
        metrics['net_assets_change_pct'] = ((current_net_assets - prior_net_assets) / abs(prior_net_assets)) * 100
    else:
        metrics['net_assets_change_gbp'] = current_net_assets
        metrics['net_assets_change_pct'] = None

    # Calculate employee change
    current_employees = current.get('employees', 0) or 0
    prior_employees = prior.get('employees', 0) or 0
    metrics['employee_change'] = current_employees - prior_employees

    # Calculate financial health score (0-100)
    score = 50  # Start at neutral

    # Factor 1: Net assets position (40 points)
    if current_net_assets > 0:
        score += 20  # Positive net assets
        if current_net_assets > 100000:
            score += 10  # Strong assets
        if current_net_assets > 500000:
            score += 10  # Very strong assets
    else:
        score -= 20  # Negative net assets (liabilities)
        if current_net_assets < -100000:
            score -= 10  # Significant debt

    # Factor 2: Year-over-year improvement (30 points)
    if metrics['net_assets_change_gbp']:
        if metrics['net_assets_change_gbp'] > 0:
            score += 15  # Improved
            if metrics['net_assets_change_pct'] and metrics['net_assets_change_pct'] > 20:
                score += 15  # Significant improvement (>20%)
        else:
            score -= 15  # Declined
            if metrics['net_assets_change_pct'] and metrics['net_assets_change_pct'] < -20:
                score -= 15  # Significant decline (>20%)

    # Factor 3: Employee growth (10 points)
    if metrics['employee_change'] > 0:
        score += 10  # Growing workforce
    elif metrics['employee_change'] < 0:
        score -= 5  # Shrinking workforce

    # Factor 4: Asset composition (10 points)
    total_assets = current.get('total_assets', 0) or current_net_assets
    if total_assets > 0 and current_net_assets > 0:
        asset_ratio = current_net_assets / total_assets
        if asset_ratio > 0.5:
            score += 10  # Strong asset base
        elif asset_ratio > 0.3:
            score += 5  # Decent asset base

    # Normalize score to 0-100
    score = max(0, min(100, score))
    metrics['financial_health_score'] = score

    # Assign letter grade
    if score >= 90:
        metrics['financial_rating'] = 'A'
        metrics['rating_description'] = 'Excellent'
    elif score >= 80:
        metrics['financial_rating'] = 'B'
        metrics['rating_description'] = 'Very Good'
    elif score >= 70:
        metrics['financial_rating'] = 'C'
        metrics['rating_description'] = 'Good'
    elif score >= 60:
        metrics['financial_rating'] = 'D'
        metrics['rating_description'] = 'Fair'
    elif score >= 50:
        metrics['financial_rating'] = 'E'
        metrics['rating_description'] = 'Weak'
    else:
        metrics['financial_rating'] = 'F'
        metrics['rating_description'] = 'Poor'

    return metrics

def create_financial_columns(cursor):
    """Add financial data columns to restaurants table."""
    new_columns = [
        # Current year
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

        # Prior year
        ("fixed_assets_gbp_prior", "INTEGER"),
        ("current_assets_gbp_prior", "INTEGER"),
        ("net_current_assets_gbp_prior", "INTEGER"),
        ("total_assets_gbp_prior", "INTEGER"),
        ("net_assets_gbp_prior", "INTEGER"),
        ("shareholders_equity_gbp_prior", "INTEGER"),
        ("turnover_gbp_prior", "INTEGER"),
        ("gross_profit_gbp_prior", "INTEGER"),
        ("operating_profit_gbp_prior", "INTEGER"),
        ("profit_loss_gbp_prior", "INTEGER"),
        ("employees_prior", "INTEGER"),

        # Calculated metrics
        ("net_assets_change_gbp", "INTEGER"),
        ("net_assets_change_pct", "REAL"),
        ("employee_change", "INTEGER"),
        ("financial_health_score", "INTEGER"),
        ("financial_rating", "TEXT"),
        ("rating_description", "TEXT"),
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
    print("FETCH BALANCE SHEET DATA (BOTH YEARS) FOR ALL COMPANIES")
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
    success_count = 0
    error_count = 0

    # Process each company
    for idx, (restaurant_id, name, company_number, company_name) in enumerate(companies, 1):
        print(f"[{idx}/{len(companies)}] {name}")
        print(f"  Company: {company_name} ({company_number})")

        try:
            # Get latest filing
            time.sleep(RATE_LIMIT_DELAY)
            filing = get_latest_filing(company_number)

            if not filing:
                print("  ⚠️  No accounts filings found")
                error_count += 1
                print()
                continue

            print(f"  📄 Latest filing: {filing['date']} (period end: {filing['period_end']})")

            # Download iXBRL
            time.sleep(RATE_LIMIT_DELAY)
            ixbrl_content = download_ixbrl(filing['document_url'])

            if not ixbrl_content:
                print("  ⚠️  Could not download iXBRL document")
                error_count += 1
                print()
                continue

            # Parse balance sheet for BOTH years
            current_data, prior_data = parse_balance_sheet_both_years(ixbrl_content)

            if not current_data:
                print("  ⚠️  No current year financial data found in document")
                error_count += 1
                print()
                continue

            # Display what we found
            print(f"  ✅ Found {len(current_data)} current year metrics")
            if prior_data:
                print(f"  ✅ Found {len(prior_data)} prior year metrics")

            # Calculate performance metrics
            performance = calculate_financial_performance(current_data, prior_data)

            print(f"  📊 Financial Rating: {performance['financial_rating']} ({performance['rating_description']}) - Score: {performance['financial_health_score']}/100")
            if performance['net_assets_change_gbp'] is not None:
                change_symbol = "📈" if performance['net_assets_change_gbp'] > 0 else "📉"
                print(f"  {change_symbol} Net Assets Change: £{performance['net_assets_change_gbp']:,}", end="")
                if performance['net_assets_change_pct'] is not None:
                    print(f" ({performance['net_assets_change_pct']:+.1f}%)")
                else:
                    print()

            # Update database
            update_fields = []
            update_values = []

            # Current year
            for key, value in current_data.items():
                col_name = f"{key}_gbp" if key != 'employees' else key
                update_fields.append(f"{col_name} = ?")
                update_values.append(value)

            # Prior year
            for key, value in prior_data.items():
                col_name = f"{key}_gbp_prior" if key != 'employees' else f"{key}_prior"
                update_fields.append(f"{col_name} = ?")
                update_values.append(value)

            # Performance metrics
            for key, value in performance.items():
                col_name = key if key.endswith(('_gbp', '_pct', '_change', '_score', '_rating', '_description')) else f"{key}"
                update_fields.append(f"{col_name} = ?")
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

            success_count += 1
            print(f"  ✅ Updated database")

        except Exception as e:
            print(f"  ❌ Error: {e}")
            error_count += 1

        print()

    conn.close()

    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()
    print(f"📊 Total companies processed: {len(companies)}")
    print(f"✅ Successful: {success_count} ({success_count/len(companies)*100:.1f}%)")
    print(f"❌ Errors: {error_count} ({error_count/len(companies)*100:.1f}%)")
    print()
    print("=" * 80)

if __name__ == "__main__":
    main()
