#!/usr/bin/env python3
"""
Debug Context Names in iXBRL Documents
======================================

Analyzes what context names are actually used in iXBRL documents
to understand why parsing is failing.
"""

import requests
import base64
from bs4 import BeautifulSoup
from collections import Counter

API_KEY = "8aca0fb0-82ea-4cc0-b0c3-ae3c859a7dfa"
auth_string = f"{API_KEY}:"
auth_base64 = base64.b64encode(auth_string.encode('ascii')).decode('ascii')

headers = {
    "Authorization": f"Basic {auth_base64}",
    "Accept": "application/json"
}

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
                return latest.get('links', {}).get('document_metadata')

        return None

    except Exception as e:
        print(f"Error: {e}")
        return None

def download_ixbrl(document_url):
    """Download iXBRL document."""
    if not document_url:
        return None

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
        print(f"Error: {e}")
        return None

def analyze_contexts(ixbrl_content):
    """Analyze all context references in iXBRL."""
    if not ixbrl_content:
        return None

    soup = BeautifulSoup(ixbrl_content, 'html.parser')

    # Find all XBRL tags
    xbrl_tags = soup.find_all(['ix:nonfraction', 'ix:nonnumeric'])

    # Count context references
    contexts = Counter()
    context_by_field = {}

    for tag in xbrl_tags:
        name = tag.get('name', '')
        context_ref = tag.get('contextref', '')

        if context_ref:
            contexts[context_ref] += 1

            # Track which fields use which contexts
            for field in ['NetAssets', 'FixedAssets', 'CurrentAssets', 'Employees']:
                if field in name:
                    if field not in context_by_field:
                        context_by_field[field] = set()
                    context_by_field[field].add(context_ref)

    return contexts, context_by_field

# Test companies that failed in v2
test_companies = [
    ("Stoke Village Cafe", "04050856"),
    ("Barbican Kitchen", "06925358"),
    ("Cafe Local", "08313022"),
]

print("=" * 80)
print("ANALYZING iXBRL CONTEXT NAMES")
print("=" * 80)
print()

for name, company_number in test_companies:
    print(f"📊 {name} ({company_number})")
    print("-" * 80)

    # Get filing
    doc_url = get_latest_filing(company_number)
    if not doc_url:
        print("  ⚠️  No filing found")
        print()
        continue

    # Download iXBRL
    ixbrl = download_ixbrl(doc_url)
    if not ixbrl:
        print("  ⚠️  Could not download")
        print()
        continue

    # Analyze contexts
    contexts, fields = analyze_contexts(ixbrl)

    print(f"  Total XBRL tags: {sum(contexts.values())}")
    print(f"  Unique contexts: {len(contexts)}")
    print()

    print("  Top 10 Context Names:")
    for ctx, count in contexts.most_common(10):
        print(f"    {ctx}: {count} tags")
    print()

    print("  Context Names by Financial Field:")
    for field, ctxs in sorted(fields.items()):
        print(f"    {field}:")
        for ctx in sorted(ctxs):
            print(f"      - {ctx}")
    print()
    print("=" * 80)
    print()
