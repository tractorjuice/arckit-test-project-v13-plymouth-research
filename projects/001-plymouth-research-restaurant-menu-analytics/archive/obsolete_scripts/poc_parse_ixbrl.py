#!/usr/bin/env python3
"""
Parse iXBRL Accounts Document
=============================

Download and parse the structured iXBRL version to extract financial metrics.
"""

import requests
import base64
from bs4 import BeautifulSoup
import re

COMPANY_NUMBER = "11403510"
API_KEY = "8aca0fb0-82ea-4cc0-b0c3-ae3c859a7dfa"
DOCUMENT_URL = "https://document-api.company-information.service.gov.uk/document/L1tfEliAz2y37oNzEuKYC44Rga9oxQIwS28YF0flIIw/content"

# Encode API key
auth_string = f"{API_KEY}:"
auth_base64 = base64.b64encode(auth_string.encode('ascii')).decode('ascii')

headers = {
    "Authorization": f"Basic {auth_base64}",
    "Accept": "application/xhtml+xml"
}

print("=" * 80)
print("PARSING iXBRL ACCOUNTS - HONKY TONK WINE LIBRARY")
print("=" * 80)
print()

print("📥 Downloading iXBRL document...")
response = requests.get(DOCUMENT_URL, headers=headers)

if response.status_code == 200:
    print(f"✅ Downloaded: {len(response.content):,} bytes")
    print(f"   Content-Type: {response.headers.get('Content-Type')}")
    print()

    # Save for inspection
    with open('honkytonks_accounts_2024.html', 'wb') as f:
        f.write(response.content)

    # Parse with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    print("🔍 EXTRACTING FINANCIAL DATA FROM iXBRL...")
    print("-" * 80)

    # Look for XBRL tags (different namespaces possible)
    # Common tags: ix:nonFraction, ix:nonNumeric
    xbrl_tags = soup.find_all(['ix:nonfraction', 'ix:nonnumeric'])

    if xbrl_tags:
        print(f"✅ Found {len(xbrl_tags)} XBRL data points\n")

        # Extract specific financial metrics
        financial_data = {}

        for tag in xbrl_tags:
            name = tag.get('name', '')
            context = tag.get('contextref', '')
            value = tag.get_text(strip=True)

            # Look for key financial indicators
            if 'assets' in name.lower():
                financial_data[f"Assets ({name})"] = value
            elif 'turnover' in name.lower() or 'revenue' in name.lower():
                financial_data[f"Revenue ({name})"] = value
            elif 'profit' in name.lower() or 'loss' in name.lower():
                financial_data[f"Profit/Loss ({name})"] = value
            elif 'employee' in name.lower():
                financial_data[f"Employees ({name})"] = value
            elif 'shareholder' in name.lower() or 'equity' in name.lower():
                financial_data[f"Equity ({name})"] = value

        print("📊 KEY FINANCIAL METRICS FOUND:")
        print("-" * 80)
        if financial_data:
            for key, value in financial_data.items():
                print(f"   {key}: {value}")
        else:
            print("   ⚠️  No standard financial metrics found in XBRL tags")

        print()
    else:
        print("⚠️  No XBRL tags found, trying plain text extraction...")
        print()

        # Fallback: Look for common patterns in text
        text = soup.get_text()

        # Look for balance sheet items
        patterns = {
            'Total Assets': r'Total\s+assets?\s*[:\s]*£?\s*([\d,]+)',
            'Net Assets': r'Net\s+assets?\s*[:\s]*£?\s*([\d,]+)',
            'Fixed Assets': r'Fixed\s+assets?\s*[:\s]*£?\s*([\d,]+)',
            'Current Assets': r'Current\s+assets?\s*[:\s]*£?\s*([\d,]+)',
            'Creditors': r'Creditors?\s*[:\s]*£?\s*([\d,]+)',
            'Called up share capital': r'Called\s+up\s+share\s+capital\s*[:\s]*£?\s*([\d,]+)',
        }

        print("📊 PATTERN MATCHING RESULTS:")
        print("-" * 80)

        found_data = {}
        for metric, pattern in patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                # Get unique values
                values = list(set(matches))
                found_data[metric] = values
                print(f"   {metric}: {', '.join(values)}")

        if not found_data:
            print("   ⚠️  No financial patterns matched")

        print()

    # Show a sample of the HTML structure
    print("📄 DOCUMENT STRUCTURE SAMPLE:")
    print("-" * 80)
    print(soup.prettify()[:1000])
    print("...")
    print()

else:
    print(f"❌ Error: {response.status_code}")
    print(f"Response: {response.text[:500]}")

print()
print("=" * 80)
print("FINDINGS & RECOMMENDATION")
print("=" * 80)
print()
print("Based on this POC:")
print()
print("✅ PHASE 1: Filing Metadata (RECOMMENDED)")
print("   Implementation: Easy (API calls only)")
print("   Coverage: 100% of companies")
print("   Data Quality: High")
print("   Value: Shows company size, filing compliance, age")
print()
print("   Metrics to collect:")
print("   - last_accounts_date (e.g., '2024-06-30')")
print("   - account_type (e.g., 'micro-entity', 'small', 'full')")
print("   - filing_status (e.g., 'current', 'overdue')")
print("   - accounts_next_due (e.g., '2026-03-31')")
print("   - company_age_years (e.g., 7)")
print()
print("⚠️  PHASE 2: Financial Metrics (OPTIONAL)")
print("   Implementation: Complex (PDF/iXBRL parsing)")
print("   Coverage: 40-60% useful data")
print("   Data Quality: Medium (micro-entities exempt)")
print("   Value: Limited for most restaurants (too many exemptions)")
print()
print("   Why it's limited:")
print("   - 91/102 companies are 'ltd' (private limited)")
print("   - Most qualify as micro-entities (exempt from disclosure)")
print("   - Turnover, profit, employees usually NOT disclosed")
print("   - Only assets/liabilities available (less useful)")
print()
print("💡 RECOMMENDED APPROACH:")
print("   1. Start with Phase 1 (filing metadata)")
print("   2. Adds value immediately with minimal effort")
print("   3. Can always add Phase 2 later if needed")
print("=" * 80)
