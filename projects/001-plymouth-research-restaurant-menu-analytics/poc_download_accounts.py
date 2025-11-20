#!/usr/bin/env python3
"""
Download and Analyze Accounts Document
======================================

Download Honky Tonks' latest accounts and see what financial data is inside.
"""

import requests
import base64
import json

COMPANY_NUMBER = "11403510"
API_KEY = "8aca0fb0-82ea-4cc0-b0c3-ae3c859a7dfa"

# Document URL from previous POC
DOCUMENT_URL = "https://document-api.company-information.service.gov.uk/document/L1tfEliAz2y37oNzEuKYC44Rga9oxQIwS28YF0flIIw"

# Encode API key
auth_string = f"{API_KEY}:"
auth_base64 = base64.b64encode(auth_string.encode('ascii')).decode('ascii')

headers = {
    "Authorization": f"Basic {auth_base64}",
    "Accept": "application/pdf"  # Try PDF first
}

print("=" * 80)
print("DOWNLOADING ACCOUNTS DOCUMENT")
print("=" * 80)
print()

# Try to get document metadata first
metadata_headers = {
    "Authorization": f"Basic {auth_base64}",
    "Accept": "application/json"
}

print("📋 Getting document metadata...")
response = requests.get(DOCUMENT_URL, headers=metadata_headers)

if response.status_code == 200:
    metadata = response.json()
    print("✅ Document metadata:")
    print(json.dumps(metadata, indent=2))
    print()
else:
    print(f"⚠️  Could not get metadata: {response.status_code}")
    print(f"Response: {response.text[:200]}")
    print()

# Now try to download the actual document
print("📥 Downloading PDF document...")
response = requests.get(DOCUMENT_URL + "/content", headers=headers)

if response.status_code == 200:
    # Save to file
    filename = f"honkytonks_accounts_2024.pdf"
    with open(filename, 'wb') as f:
        f.write(response.content)

    print(f"✅ Downloaded: {filename}")
    print(f"   Size: {len(response.content):,} bytes")
    print(f"   Content-Type: {response.headers.get('Content-Type')}")
    print()

    # Check if it's actually a PDF
    if response.content[:4] == b'%PDF':
        print("✅ Valid PDF file")
        print()
        print("📄 To view the accounts:")
        print(f"   open {filename}")
        print()
        print("💡 What to look for in micro-entity accounts:")
        print("   - Balance Sheet: Total assets, Net assets")
        print("   - May have: Turnover (optional for micro-entities)")
        print("   - Directors' statement")
        print("   - Abbreviated information (minimal detail)")
        print()
        print("⚠️  Micro-entity accounts often exclude:")
        print("   - Detailed profit/loss")
        print("   - Employee numbers")
        print("   - Detailed turnover breakdown")
    else:
        print("⚠️  Not a PDF file, content type:", response.headers.get('Content-Type'))
        print("First 200 bytes:", response.content[:200])

else:
    print(f"❌ Error downloading document: {response.status_code}")
    print(f"Response: {response.text[:500]}")

print()
print("=" * 80)
print("WHAT WE CAN EXTRACT FROM MICRO-ENTITY ACCOUNTS")
print("=" * 80)
print()
print("✅ Always Available (from API metadata):")
print("   - Filing date")
print("   - Account period end date")
print("   - Account type (micro-entity)")
print("   - Company age at filing")
print()
print("📊 Sometimes Available (from document parsing):")
print("   - Total assets")
print("   - Net worth (called 'net assets' or 'shareholders funds')")
print("   - Fixed assets vs current assets")
print()
print("❌ Usually NOT Available in Micro-Entity Accounts:")
print("   - Turnover (exempt from disclosure)")
print("   - Profit/loss (exempt from disclosure)")
print("   - Number of employees (exempt from disclosure)")
print("   - Detailed breakdown of income/expenses")
print()
print("💡 RECOMMENDATION:")
print("   Phase 1: Filing metadata (100% coverage, easy)")
print("   - Last accounts date")
print("   - Account type")
print("   - Filing compliance status")
print("   - Company age")
print()
print("   Phase 2: Asset data (requires PDF parsing, ~40% useful data)")
print("   - Total assets")
print("   - Net worth")
print("   - Asset breakdown (if full accounts)")
print()
print("=" * 80)
