#!/usr/bin/env python3
"""
Business Rates Matcher V2 - Improved with Name Normalization

Improvements:
- Strips corporate suffixes (LTD, LIMITED, PLC, HOLDINGS)
- Strips location suffixes (Plymouth, UK)
- Removes special characters and punctuation
- Lowered confidence threshold from 70% to 60%
- Better handling of name variations

Usage:
    python match_business_rates_v2.py
"""

import sqlite3
import pandas as pd
import re
from difflib import SequenceMatcher
from typing import Tuple
from datetime import datetime

# Configuration
DB_PATH = 'plymouth_research.db'
EXCEL_PATH = '/workspaces/arckit-test-project-v13-plymouth-research/Monthly-Business-Rates-November-2025.xlsx'
OUTPUT_CSV_CONFIDENT = 'business_rates_matches_confident_v2.csv'
OUTPUT_CSV_ALL = 'business_rates_matches_all_v2.csv'
OUTPUT_CSV_UNMATCHED = 'business_rates_unmatched_v2.csv'

# Matching weights
NAME_SIMILARITY_WEIGHT = 50  # 0-50 points
POSTCODE_MATCH_BONUS = 30    # 30 bonus points for exact postcode
ADDRESS_SIMILARITY_WEIGHT = 20  # 0-20 points

# Confidence threshold (LOWERED from 70 to 60)
CONFIDENCE_THRESHOLD = 60


def normalize_business_name(name: str) -> str:
    """
    Normalize business name for better matching.

    Removes:
    - Corporate suffixes (LTD, LIMITED, PLC, HOLDINGS, etc.)
    - Location suffixes (Plymouth, UK)
    - Special characters and punctuation
    - Extra whitespace
    """
    if not name or pd.isna(name):
        return ""

    name = str(name).upper().strip()

    # Remove corporate suffixes (at end of string)
    corporate_patterns = [
        r'\s+LIMITED\s*$',
        r'\s+LTD\.?\s*$',
        r'\s+PLC\.?\s*$',
        r'\s+HOLDINGS?\s*$',
        r'\s+GROUP\s*$',
        r'\s+UK\s*$',
        r'\s+\(UK\)\s*$',
    ]

    for pattern in corporate_patterns:
        name = re.sub(pattern, '', name, flags=re.IGNORECASE)

    # Remove location suffixes
    location_patterns = [
        r'\s+PLYMOUTH\s*$',
        r'\s+\(PLYMOUTH\)\s*$',
        r'\s+-\s+PLYMOUTH\s*$',
    ]

    for pattern in location_patterns:
        name = re.sub(pattern, '', name, flags=re.IGNORECASE)

    # Remove special characters but keep spaces and alphanumeric
    name = re.sub(r'[^\w\s&]', '', name)

    # Normalize whitespace
    name = re.sub(r'\s+', ' ', name).strip()

    return name


def normalize_postcode(postcode: str) -> str:
    """Normalize UK postcode."""
    if not postcode or pd.isna(postcode):
        return ""

    postcode = str(postcode).upper().strip()
    # Remove all spaces
    postcode = re.sub(r'\s+', '', postcode)
    return postcode


def similarity_score(str1: str, str2: str) -> float:
    """Calculate similarity score between two strings (0-100)."""
    if not str1 or not str2:
        return 0.0
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio() * 100


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

    # Normalize names for comparison
    rest_name_norm = normalize_business_name(restaurant_name)
    rates_holder_norm = normalize_business_name(rates_account_holder)

    # 1. Name similarity (0-50 points)
    name_sim = similarity_score(rest_name_norm, rates_holder_norm)
    name_points = (name_sim / 100) * NAME_SIMILARITY_WEIGHT
    score += name_points

    if name_sim >= 95:
        reasons.append(f"exact_name({name_sim:.0f}%)")
    elif name_sim >= 80:
        reasons.append(f"similar_name({name_sim:.0f}%)")
    elif name_sim >= 60:
        reasons.append(f"partial_name({name_sim:.0f}%)")

    # 2. Postcode match (30 bonus points)
    rest_post_norm = normalize_postcode(restaurant_postcode)
    rates_post_norm = normalize_postcode(rates_postcode)

    if rest_post_norm and rates_post_norm:
        if rest_post_norm == rates_post_norm:
            score += POSTCODE_MATCH_BONUS
            reasons.append("exact_postcode")
        elif rest_post_norm[:4] == rates_post_norm[:4]:  # First 4 chars (area)
            score += 15  # Half points for area match
            reasons.append("postcode_area")

    # 3. Address similarity (0-20 points)
    if restaurant_address and rates_address and not pd.isna(restaurant_address) and not pd.isna(rates_address):
        rest_addr_norm = str(restaurant_address).upper()
        rates_addr_norm = str(rates_address).upper()

        # Word-based matching
        rest_words = set(re.findall(r'\w+', rest_addr_norm))
        rates_words = set(re.findall(r'\w+', rates_addr_norm))

        if rest_words and rates_words:
            common_words = rest_words & rates_words
            # Remove common stop words
            stop_words = {'THE', 'AT', 'IN', 'ON', 'A', 'AN', 'AND', 'OR', 'PLYMOUTH', 'UK'}
            common_words = common_words - stop_words

            if common_words:
                addr_points = min(len(common_words) * 5, ADDRESS_SIMILARITY_WEIGHT)
                score += addr_points
                if len(common_words) >= 3:
                    reasons.append(f"address_match({len(common_words)}_words)")

    reason_str = "+".join(reasons) if reasons else "low_confidence"
    return round(score, 2), reason_str


def main():
    print("=" * 80)
    print("BUSINESS RATES MATCHER V2 - IMPROVED WITH NAME NORMALIZATION")
    print("=" * 80)
    print()
    print("Improvements:")
    print("  ✓ Corporate suffix removal (LTD, LIMITED, PLC, HOLDINGS)")
    print("  ✓ Location suffix removal (Plymouth, UK)")
    print("  ✓ Special character normalization")
    print("  ✓ Lowered confidence threshold: 60% (was 70%)")
    print()

    # 1. Load restaurants from database (only those WITHOUT business rates)
    print("Step 1: Loading unmatched restaurants from database...")
    conn = sqlite3.connect(DB_PATH)

    restaurants_query = """
    SELECT
        restaurant_id,
        name,
        address,
        fsa_address_line1,
        fsa_postcode,
        google_formatted_address
    FROM restaurants
    WHERE is_active = 1
    AND business_rates_rateable_value IS NULL
    ORDER BY restaurant_id
    """

    restaurants_df = pd.read_sql_query(restaurants_query, conn)
    conn.close()

    print(f"  Found {len(restaurants_df)} unmatched restaurants")

    # 2. Load business rates from Excel
    print("\nStep 2: Loading business rates from Excel...")
    df = pd.read_excel(EXCEL_PATH, sheet_name='website', header=None)

    # Use row 5 (index 5) as column names
    df_data = df.iloc[6:].copy()
    df_data.columns = df.iloc[5].tolist()

    # Drop the first column (empty)
    df_data = df_data.iloc[:, 1:]

    print(f"  Loaded {len(df_data)} properties from business rates register")

    # Filter to hospitality sector
    hospitality_categories = [
        'Restaurants',
        'Cafes',
        'Public Houses',
        'Hotel',
        'Cafe',
        'Restaurant',
        'Drive-In Restaurants',
        'Licensed Restaurants',
    ]

    hospitality_df = df_data[
        df_data['Scat Description'].str.contains('|'.join(hospitality_categories), case=False, na=False)
    ].copy()

    print(f"  Filtered to {len(hospitality_df)} hospitality properties")

    # 3. Match restaurants to business rates
    print(f"\nStep 3: Matching restaurants (threshold: {CONFIDENCE_THRESHOLD}%)...")

    matches = []

    for idx, restaurant in restaurants_df.iterrows():
        best_match = None
        best_score = 0
        best_reason = ""

        restaurant_name = restaurant['name']
        restaurant_address = restaurant['fsa_address_line1'] or restaurant['address'] or restaurant['google_formatted_address']
        restaurant_postcode = restaurant['fsa_postcode']

        # Try to match against all hospitality properties
        for _, rates_row in hospitality_df.iterrows():
            rates_account_holder = rates_row['Account Holder1']
            rates_address = f"{rates_row['Addr1']}, {rates_row['Addr2']}"
            rates_postcode = rates_row['Postcode']

            score, reason = calculate_match_score(
                restaurant_name,
                restaurant_address,
                restaurant_postcode,
                rates_account_holder,
                rates_address,
                rates_postcode
            )

            if score > best_score:
                best_score = score
                best_reason = reason
                best_match = rates_row

        # Record the best match (even if below threshold)
        if best_match is not None:
            matches.append({
                'restaurant_id': restaurant['restaurant_id'],
                'restaurant_name': restaurant_name,
                'restaurant_address': restaurant_address,
                'restaurant_postcode': restaurant_postcode,
                'match_score': best_score,
                'match_reason': best_reason,
                'rates_propref': best_match['Propref'],
                'rates_account_holder': best_match['Account Holder1'],
                'rates_address': f"{best_match['Addr1']}, {best_match['Addr2']}",
                'rates_postcode': best_match['Postcode'],
                'rates_rateable_value': best_match['Current 2023 Rv'],
                'rates_net_charge': best_match['2025-26 Net Charge'],
                'rates_category': best_match['Scat Description'],
                'rates_vo_description': best_match['VO Description'],
            })

        if (idx + 1) % 10 == 0:
            print(f"  Processed {idx + 1}/{len(restaurants_df)} restaurants...")

    print(f"  Completed matching all {len(restaurants_df)} restaurants")

    # 4. Create DataFrames
    matches_df = pd.DataFrame(matches)

    # Confident matches (>= threshold)
    confident_matches = matches_df[matches_df['match_score'] >= CONFIDENCE_THRESHOLD].copy()

    # Unmatched (below threshold)
    unmatched = matches_df[matches_df['match_score'] < CONFIDENCE_THRESHOLD].copy()

    # 5. Save results
    print("\nStep 4: Saving results...")

    matches_df.to_csv(OUTPUT_CSV_ALL, index=False)
    print(f"  ✓ All matches saved to {OUTPUT_CSV_ALL}")

    confident_matches.to_csv(OUTPUT_CSV_CONFIDENT, index=False)
    print(f"  ✓ Confident matches saved to {OUTPUT_CSV_CONFIDENT}")

    unmatched.to_csv(OUTPUT_CSV_UNMATCHED, index=False)
    print(f"  ✓ Unmatched saved to {OUTPUT_CSV_UNMATCHED}")

    # 6. Summary statistics
    print("\n" + "=" * 80)
    print("RESULTS SUMMARY")
    print("=" * 80)

    print(f"\nTotal restaurants analyzed: {len(restaurants_df)}")
    print(f"Confident matches (≥{CONFIDENCE_THRESHOLD}%): {len(confident_matches)}")
    print(f"Below threshold (<{CONFIDENCE_THRESHOLD}%): {len(unmatched)}")

    if len(confident_matches) > 0:
        print(f"\nConfidence distribution:")
        print(f"  90-100%: {len(confident_matches[confident_matches['match_score'] >= 90])}")
        print(f"  80-89%:  {len(confident_matches[(confident_matches['match_score'] >= 80) & (confident_matches['match_score'] < 90)])}")
        print(f"  70-79%:  {len(confident_matches[(confident_matches['match_score'] >= 70) & (confident_matches['match_score'] < 80)])}")
        print(f"  60-69%:  {len(confident_matches[(confident_matches['match_score'] >= 60) & (confident_matches['match_score'] < 70)])}")

        print(f"\nTop 10 matches by rateable value:")
        top_matches = confident_matches.nlargest(10, 'rates_rateable_value')
        for idx, row in top_matches.iterrows():
            rv = int(row['rates_rateable_value']) if pd.notna(row['rates_rateable_value']) else 0
            print(f"  {row['restaurant_name']}: £{rv:,} ({row['match_score']:.0f}% confidence)")

        print(f"\nNEW matches in 60-69% range (lowered threshold):")
        new_matches = confident_matches[
            (confident_matches['match_score'] >= 60) &
            (confident_matches['match_score'] < 70)
        ].sort_values('match_score', ascending=False)

        if len(new_matches) > 0:
            for idx, row in new_matches.head(15).iterrows():
                rv = int(row['rates_rateable_value']) if pd.notna(row['rates_rateable_value']) else 0
                print(f"  {row['restaurant_name']}: £{rv:,} ({row['match_score']:.0f}%)")
                print(f"    → {row['rates_account_holder']}")
                print(f"    Reason: {row['match_reason']}")
        else:
            print("  (None)")

    print("\n" + "=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print(f"1. Review confident matches in {OUTPUT_CSV_CONFIDENT}")
    print(f"2. Manually review matches with 60-69% confidence")
    print(f"3. Run import script to update database")
    print()


if __name__ == '__main__':
    main()
