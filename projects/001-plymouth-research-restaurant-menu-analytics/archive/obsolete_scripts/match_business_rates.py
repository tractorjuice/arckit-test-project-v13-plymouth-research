#!/usr/bin/env python3
"""
Business Rates Matcher for Plymouth Research

Matches Plymouth restaurants with their business rates data from the
Monthly Business Rates November 2025 dataset.

Features:
- Multi-factor matching: address + postcode + name similarity
- Confidence scoring (0-100)
- Focuses on hospitality categories (restaurants, cafes, pubs, takeaways)
- Exports matched and unmatched results

Usage:
    python match_business_rates.py
"""

import sqlite3
import pandas as pd
from difflib import SequenceMatcher
import re
from typing import Tuple, Optional

# Database configuration
DB_PATH = 'plymouth_research.db'
EXCEL_PATH = '/workspaces/arckit-test-project-v13-plymouth-research/Monthly-Business-Rates-November-2025.xlsx'

# Matching thresholds
AUTO_MATCH_THRESHOLD = 70  # Auto-match if confidence >= 70
NAME_SIMILARITY_WEIGHT = 50
POSTCODE_MATCH_BONUS = 30
ADDRESS_SIMILARITY_WEIGHT = 20

# Hospitality categories to match
HOSPITALITY_CATEGORIES = [
    'restaurant', 'cafe', 'takeaway', 'pub', 'bar', 'hotel', 'inn',
    'food', 'club', 'licensed'
]


def normalize_string(s: str) -> str:
    """Normalize string for matching."""
    if pd.isna(s) or s == '0':
        return ''
    s = str(s).lower()
    s = re.sub(r'[^a-z0-9\s]', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def normalize_postcode(postcode: str) -> str:
    """Normalize UK postcode."""
    if pd.isna(postcode):
        return ''
    postcode = str(postcode).upper().replace(' ', '')
    # Extract PL1 2AB format
    match = re.search(r'([A-Z]+\d+\s*\d+[A-Z]+)', postcode)
    return match.group(1).replace(' ', '') if match else postcode


def extract_postcode_from_address(address: str) -> str:
    """Extract postcode from address string."""
    if pd.isna(address):
        return ''
    # Look for PL postcode pattern
    match = re.search(r'(PL\d+\s*\d+[A-Z]+)', str(address).upper())
    return match.group(1).replace(' ', '') if match else ''


def similarity_score(str1: str, str2: str) -> float:
    """Calculate similarity score between two strings (0-100)."""
    if not str1 or not str2:
        return 0.0
    return SequenceMatcher(None, str1, str2).ratio() * 100


def calculate_match_score(
    restaurant_name: str,
    restaurant_address: str,
    restaurant_postcode: str,
    rates_account_holder: str,
    rates_address: str,
    rates_postcode: str
) -> Tuple[float, str]:
    """
    Calculate match confidence score and reason.

    Returns:
        (score, reason) where score is 0-100 and reason explains the match
    """
    score = 0
    reasons = []

    # Normalize inputs
    rest_name_norm = normalize_string(restaurant_name)
    rest_addr_norm = normalize_string(restaurant_address)
    rest_post_norm = normalize_postcode(restaurant_postcode)

    rates_holder_norm = normalize_string(rates_account_holder)
    rates_addr_norm = normalize_string(rates_address)
    rates_post_norm = normalize_postcode(rates_postcode)

    # 1. Name similarity (50 points max)
    name_sim = similarity_score(rest_name_norm, rates_holder_norm)
    score += (name_sim / 100) * NAME_SIMILARITY_WEIGHT

    if name_sim >= 95:
        reasons.append(f"exact_name({name_sim:.0f}%)")
    elif name_sim >= 80:
        reasons.append(f"similar_name({name_sim:.0f}%)")
    elif name_sim >= 60:
        reasons.append(f"partial_name({name_sim:.0f}%)")

    # 2. Postcode match (30 bonus points)
    if rest_post_norm and rates_post_norm:
        if rest_post_norm == rates_post_norm:
            score += POSTCODE_MATCH_BONUS
            reasons.append("exact_postcode")
        elif rest_post_norm[:4] == rates_post_norm[:4]:  # Outward code match
            score += POSTCODE_MATCH_BONUS * 0.5
            reasons.append("postcode_area")

    # 3. Address similarity (20 points max)
    if rest_addr_norm and rates_addr_norm:
        # Word-based matching
        rest_words = set(rest_addr_norm.split())
        rates_words = set(rates_addr_norm.split())

        if rest_words and rates_words:
            common_words = rest_words & rates_words
            addr_score = (len(common_words) / max(len(rest_words), len(rates_words))) * ADDRESS_SIMILARITY_WEIGHT
            score += addr_score

            if addr_score > 15:
                reasons.append(f"address_match({len(common_words)}_words)")

    reason_str = "+".join(reasons) if reasons else "no_match"
    return round(score, 2), reason_str


def load_business_rates() -> pd.DataFrame:
    """Load and filter business rates data."""
    print("Loading business rates data...")

    # Read Excel file
    df_raw = pd.read_excel(EXCEL_PATH, sheet_name='website', header=None)

    # Use row 5 as column names, data starts from row 6
    df = df_raw.iloc[6:].copy()
    df.columns = df_raw.iloc[5].tolist()
    df = df.iloc[:, 1:]  # Drop first empty column
    df = df.reset_index(drop=True)

    # Convert numeric columns
    df['Current 2023 Rv'] = pd.to_numeric(df['Current 2023 Rv'], errors='coerce')
    df['2025-26 Net Charge'] = pd.to_numeric(df['2025-26 Net Charge'], errors='coerce')

    # Create full address
    df['Full Address'] = (df['Addr1'].astype(str) + ', ' +
                          df['Addr2'].astype(str).replace('0', '').replace('nan', '') + ', ' +
                          df['Postcode'].astype(str)).str.replace(', ,', ',').str.strip(', ')

    # Filter to hospitality properties
    hospitality_mask = df['Scat Description'].astype(str).str.lower().str.contains(
        '|'.join(HOSPITALITY_CATEGORIES), na=False, regex=True
    )

    df_hospitality = df[hospitality_mask].copy()

    print(f"  Total properties: {len(df):,}")
    print(f"  Hospitality properties: {len(df_hospitality):,}")

    return df_hospitality


def load_restaurants() -> pd.DataFrame:
    """Load restaurants from database."""
    print("Loading restaurants from database...")

    conn = sqlite3.connect(DB_PATH)
    query = """
        SELECT
            restaurant_id,
            name,
            address,
            fsa_address_line1,
            fsa_address_line2,
            fsa_postcode,
            google_formatted_address
        FROM restaurants
        WHERE is_active = 1
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Create composite address field
    df['composite_address'] = df.apply(lambda row:
        row['address'] or row['fsa_address_line1'] or row['google_formatted_address'] or '',
        axis=1
    )

    # Extract postcode
    df['composite_postcode'] = df.apply(lambda row:
        row['fsa_postcode'] or extract_postcode_from_address(row['composite_address']),
        axis=1
    )

    print(f"  Found {len(df)} active restaurants")

    return df


def match_restaurants(restaurants_df: pd.DataFrame, rates_df: pd.DataFrame) -> pd.DataFrame:
    """Match restaurants with business rates data."""
    print("\nMatching restaurants with business rates...")

    matches = []

    for _, restaurant in restaurants_df.iterrows():
        best_match = None
        best_score = 0
        best_reason = ""

        # Try to match with each rates property
        for _, rates_prop in rates_df.iterrows():
            score, reason = calculate_match_score(
                restaurant['name'],
                restaurant['composite_address'],
                restaurant['composite_postcode'],
                rates_prop['Account Holder1'],
                rates_prop['Full Address'],
                rates_prop['Postcode']
            )

            if score > best_score:
                best_score = score
                best_reason = reason
                best_match = rates_prop

        # Record match
        match_result = {
            'restaurant_id': restaurant['restaurant_id'],
            'restaurant_name': restaurant['name'],
            'restaurant_address': restaurant['composite_address'],
            'restaurant_postcode': restaurant['composite_postcode'],
            'match_score': best_score,
            'match_reason': best_reason,
            'rates_propref': best_match['Propref'] if best_match is not None and best_score >= AUTO_MATCH_THRESHOLD else None,
            'rates_account_holder': best_match['Account Holder1'] if best_match is not None else None,
            'rates_address': best_match['Full Address'] if best_match is not None else None,
            'rates_postcode': best_match['Postcode'] if best_match is not None else None,
            'rates_rateable_value': best_match['Current 2023 Rv'] if best_match is not None else None,
            'rates_net_charge': best_match['2025-26 Net Charge'] if best_match is not None else None,
            'rates_category': best_match['Scat Description'] if best_match is not None else None,
            'rates_vo_description': best_match['VO Description'] if best_match is not None else None,
        }

        matches.append(match_result)

    return pd.DataFrame(matches)


def main():
    """Main execution."""
    print("=" * 80)
    print("PLYMOUTH RESTAURANT BUSINESS RATES MATCHER")
    print("=" * 80)
    print()

    # Load data
    rates_df = load_business_rates()
    restaurants_df = load_restaurants()

    # Match
    matches_df = match_restaurants(restaurants_df, rates_df)

    # Analyze results
    print("\n" + "=" * 80)
    print("MATCHING RESULTS")
    print("=" * 80)

    matched = matches_df[matches_df['match_score'] >= AUTO_MATCH_THRESHOLD]
    high_confidence = matched[matched['match_score'] >= 90]
    medium_confidence = matched[(matched['match_score'] >= 70) & (matched['match_score'] < 90)]
    unmatched = matches_df[matches_df['match_score'] < AUTO_MATCH_THRESHOLD]

    print(f"Total restaurants: {len(matches_df)}")
    print(f"Matched: {len(matched)} ({len(matched)/len(matches_df)*100:.1f}%)")
    print(f"  - High confidence (≥90): {len(high_confidence)}")
    print(f"  - Medium confidence (70-89): {len(medium_confidence)}")
    print(f"Unmatched: {len(unmatched)} ({len(unmatched)/len(matches_df)*100:.1f}%)")
    print()

    # Show statistics
    if len(matched) > 0:
        print("Rateable Value Statistics (matched restaurants):")
        print(f"  Mean: £{matched['rates_rateable_value'].mean():,.0f}")
        print(f"  Median: £{matched['rates_rateable_value'].median():,.0f}")
        print(f"  Min: £{matched['rates_rateable_value'].min():,.0f}")
        print(f"  Max: £{matched['rates_rateable_value'].max():,.0f}")
        print()

        print("Annual Business Rates Statistics (matched restaurants):")
        print(f"  Mean: £{matched['rates_net_charge'].mean():,.0f}")
        print(f"  Median: £{matched['rates_net_charge'].median():,.0f}")
        print(f"  Min: £{matched['rates_net_charge'].min():,.0f}")
        print(f"  Max: £{matched['rates_net_charge'].max():,.0f}")

    # Export results
    print("\n" + "=" * 80)
    print("EXPORTING RESULTS")
    print("=" * 80)

    # Export all matches
    matches_df.to_csv('business_rates_matches_all.csv', index=False)
    print(f"✓ Saved all matches to: business_rates_matches_all.csv")

    # Export matched only
    matched.to_csv('business_rates_matches_confident.csv', index=False)
    print(f"✓ Saved confident matches (≥{AUTO_MATCH_THRESHOLD}%) to: business_rates_matches_confident.csv")

    # Export unmatched
    unmatched.to_csv('business_rates_unmatched.csv', index=False)
    print(f"✓ Saved unmatched restaurants to: business_rates_unmatched.csv")

    print("\n" + "=" * 80)
    print("Next steps:")
    print("  1. Review: business_rates_matches_confident.csv")
    print("  2. Manual review: business_rates_unmatched.csv")
    print("  3. Run: python import_business_rates.py (to import into database)")
    print("=" * 80)


if __name__ == '__main__':
    main()
