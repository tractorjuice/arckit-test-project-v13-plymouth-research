#!/usr/bin/env python3
"""
Proof of Concept: Financial Data for Honky Tonk Wine Library
=============================================================

Fetch and display all available financial data from Companies House.
"""

import requests
import json
import base64
from datetime import datetime

# Company details
COMPANY_NUMBER = "11403510"
COMPANY_NAME = "HONKYTONK WINE LIBRARY LIMITED"
API_KEY = "8aca0fb0-82ea-4cc0-b0c3-ae3c859a7dfa"

# Encode API key for Basic Auth
auth_string = f"{API_KEY}:"
auth_bytes = auth_string.encode('ascii')
auth_base64 = base64.b64encode(auth_bytes).decode('ascii')

headers = {
    "Authorization": f"Basic {auth_base64}",
    "Accept": "application/json"
}

print("=" * 80)
print(f"FINANCIAL DATA POC: {COMPANY_NAME}")
print(f"Company Number: {COMPANY_NUMBER}")
print("=" * 80)
print()

# ============================================================================
# 1. Company Profile
# ============================================================================
print("📋 FETCHING COMPANY PROFILE...")
print("-" * 80)

url = f"https://api.company-information.service.gov.uk/company/{COMPANY_NUMBER}"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    profile = response.json()

    print(f"✅ Company Status: {profile.get('company_status', 'N/A').upper()}")
    print(f"   Incorporation Date: {profile.get('date_of_creation', 'N/A')}")
    print(f"   Company Type: {profile.get('type', 'N/A')}")
    print(f"   SIC Codes: {', '.join(profile.get('sic_codes', []))}")

    # Accounts info
    accounts = profile.get('accounts', {})
    print(f"\n📊 Accounts Information:")
    print(f"   Last Made Up To: {accounts.get('last_accounts', {}).get('made_up_to', 'N/A')}")
    print(f"   Account Type: {accounts.get('last_accounts', {}).get('type', 'N/A')}")
    print(f"   Next Due: {accounts.get('next_due', 'N/A')}")
    print(f"   Overdue: {accounts.get('overdue', False)}")

    # Company age and filing status
    if 'date_of_creation' in profile:
        inc_date = datetime.strptime(profile['date_of_creation'], '%Y-%m-%d')
        years_old = (datetime.now() - inc_date).days // 365
        print(f"   Company Age: {years_old} years")
else:
    print(f"❌ Error fetching profile: {response.status_code}")

print()

# ============================================================================
# 2. Filing History
# ============================================================================
print("📁 FETCHING FILING HISTORY...")
print("-" * 80)

url = f"https://api.company-information.service.gov.uk/company/{COMPANY_NUMBER}/filing-history"
response = requests.get(url, headers=headers, params={"category": "accounts"})

if response.status_code == 200:
    filing_history = response.json()
    items = filing_history.get('items', [])

    print(f"✅ Found {len(items)} account filings\n")

    for idx, item in enumerate(items[:5], 1):  # Show last 5 filings
        print(f"Filing {idx}:")
        print(f"   Date: {item.get('date', 'N/A')}")
        print(f"   Description: {item.get('description', 'N/A')}")
        print(f"   Type: {item.get('type', 'N/A')}")

        # Extract period end date
        description = item.get('description', '')
        if 'made up to' in description.lower():
            period_end = description.split('made up to')[-1].strip().split()[0]
            print(f"   Period End: {period_end}")

        # Check if document is available
        links = item.get('links', {})
        if 'document_metadata' in links:
            doc_url = links['document_metadata']
            print(f"   Document Available: YES")
            print(f"   Document URL: {doc_url}")

        print()
else:
    print(f"❌ Error fetching filing history: {response.status_code}")

print()

# ============================================================================
# 3. Check for Accounts Data (iXBRL)
# ============================================================================
print("💰 CHECKING FOR DETAILED FINANCIAL DATA...")
print("-" * 80)

# Get latest filing transaction ID for document fetch
if response.status_code == 200 and items:
    latest_filing = items[0]
    transaction_id = latest_filing.get('transaction_id', '')

    if transaction_id:
        # Get document metadata
        doc_url = f"https://api.company-information.service.gov.uk/company/{COMPANY_NUMBER}/filing-history/{transaction_id}"
        doc_response = requests.get(doc_url, headers=headers)

        if doc_response.status_code == 200:
            doc_data = doc_response.json()
            print("✅ Latest filing details:")
            print(json.dumps(doc_data, indent=2))
        else:
            print(f"❌ Could not fetch document metadata: {doc_response.status_code}")
    else:
        print("⚠️  No transaction ID available")
else:
    print("⚠️  No filings available")

print()

# ============================================================================
# 4. Officers (for context)
# ============================================================================
print("👥 FETCHING OFFICERS (for context)...")
print("-" * 80)

url = f"https://api.company-information.service.gov.uk/company/{COMPANY_NUMBER}/officers"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    officers_data = response.json()
    items = officers_data.get('items', [])

    print(f"✅ Found {len(items)} active officers\n")

    for officer in items:
        if not officer.get('resigned_on'):
            print(f"   • {officer.get('name', 'N/A')} - {officer.get('officer_role', 'N/A')}")
else:
    print(f"❌ Error fetching officers: {response.status_code}")

print()
print("=" * 80)
print("POC COMPLETE")
print("=" * 80)
print()

print("📝 SUMMARY:")
print("-" * 80)
print("Available Data:")
print("  ✅ Company status and age")
print("  ✅ Filing history (dates, types)")
print("  ✅ Last accounts date and type")
print("  ✅ Next due date and overdue status")
print("  ✅ Officers and roles")
print()
print("Financial Metrics:")
print("  ⚠️  Requires parsing account documents (iXBRL or PDF)")
print("  📊 Available fields (if accounts are detailed):")
print("     - Turnover")
print("     - Total assets")
print("     - Net worth")
print("     - Profit/loss")
print("     - Number of employees")
print()
print("Next Steps:")
print("  1. Phase 1: Store filing metadata (easy win)")
print("  2. Phase 2: Parse account documents for financial metrics")
print("=" * 80)
