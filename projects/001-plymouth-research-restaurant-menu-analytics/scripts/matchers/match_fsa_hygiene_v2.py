#!/usr/bin/env python3
"""
FSA Hygiene Matcher V2 - Improved with Name Normalization

Improvements over V1:
- Strips corporate suffixes (LTD, LIMITED, PLC, HOLDINGS)
- Strips location suffixes (Plymouth, UK)
- Removes special characters and punctuation
- Lowered confidence threshold from 70% to 60%
- Better handling of name variations

Usage:
    python match_fsa_hygiene_v2.py
"""

import sqlite3
import pandas as pd
import re
import xml.etree.ElementTree as ET
from difflib import SequenceMatcher
from typing import Tuple
from datetime import datetime

# Configuration
DB_PATH = 'plymouth_research.db'
FSA_XML_PATH = 'plymouth_fsa_data.xml'
OUTPUT_CSV_CONFIDENT = 'fsa_hygiene_matches_confident_v2.csv'
OUTPUT_CSV_ALL = 'fsa_hygiene_matches_all_v2.csv'
OUTPUT_CSV_UNMATCHED = 'fsa_hygiene_unmatched_v2.csv'

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
        r'\s+,\s+PLYMOUTH\s*$',
    ]

    for pattern in location_patterns:
        name = re.sub(pattern, '', name, flags=re.IGNORECASE)

    # Remove special characters but keep spaces, ampersands, and numbers
    name = re.sub(r'[^\w\s&#]', '', name)

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
    fsa_business_name: str,
    fsa_address: str,
    fsa_postcode: str
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
    fsa_name_norm = normalize_business_name(fsa_business_name)

    # 1. Name similarity (0-50 points)
    name_sim = similarity_score(rest_name_norm, fsa_name_norm)
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
    fsa_post_norm = normalize_postcode(fsa_postcode)

    if rest_post_norm and fsa_post_norm:
        if rest_post_norm == fsa_post_norm:
            score += POSTCODE_MATCH_BONUS
            reasons.append("exact_postcode")
        elif len(rest_post_norm) >= 4 and len(fsa_post_norm) >= 4:
            if rest_post_norm[:4] == fsa_post_norm[:4]:  # First 4 chars (area)
                score += 15  # Half points for area match
                reasons.append("postcode_area")

    # 3. Address similarity (0-20 points)
    if restaurant_address and fsa_address and not pd.isna(restaurant_address) and not pd.isna(fsa_address):
        rest_addr_norm = str(restaurant_address).upper()
        fsa_addr_norm = str(fsa_address).upper()

        # Word-based matching
        rest_words = set(re.findall(r'\w+', rest_addr_norm))
        fsa_words = set(re.findall(r'\w+', fsa_addr_norm))

        if rest_words and fsa_words:
            common_words = rest_words & fsa_words
            # Remove common stop words
            stop_words = {'THE', 'AT', 'IN', 'ON', 'A', 'AN', 'AND', 'OR', 'PLYMOUTH', 'UK', 'DEVON', 'STREET', 'ROAD'}
            common_words = common_words - stop_words

            if common_words:
                addr_points = min(len(common_words) * 5, ADDRESS_SIMILARITY_WEIGHT)
                score += addr_points
                if len(common_words) >= 3:
                    reasons.append(f"address_match({len(common_words)}_words)")

    reason_str = "+".join(reasons) if reasons else "low_confidence"
    return round(score, 2), reason_str


def parse_fsa_xml(xml_path: str) -> pd.DataFrame:
    """Parse FSA XML file and return DataFrame."""
    print(f"  Parsing XML: {xml_path}")

    tree = ET.parse(xml_path)
    root = tree.getroot()

    establishments = []

    for establishment in root.findall('.//EstablishmentDetail'):
        # Extract data
        fsa_id = establishment.find('FHRSID')
        business_name = establishment.find('BusinessName')
        business_type = establishment.find('BusinessType')
        address_line1 = establishment.find('AddressLine1')
        address_line2 = establishment.find('AddressLine2')
        address_line3 = establishment.find('AddressLine3')
        postcode = establishment.find('PostCode')
        rating_value = establishment.find('RatingValue')
        rating_date = establishment.find('RatingDate')

        # Hygiene scores
        hygiene = establishment.find('.//Hygiene')
        structural = establishment.find('.//Structural')
        confidence = establishment.find('.//ConfidenceInManagement')

        establishments.append({
            'fsa_id': int(fsa_id.text) if fsa_id is not None and fsa_id.text else None,
            'fsa_business_name': business_name.text if business_name is not None else '',
            'fsa_business_type': business_type.text if business_type is not None else '',
            'fsa_address_line1': address_line1.text if address_line1 is not None else '',
            'fsa_address_line2': address_line2.text if address_line2 is not None else '',
            'fsa_address_line3': address_line3.text if address_line3 is not None else '',
            'fsa_postcode': postcode.text if postcode is not None else '',
            'hygiene_rating': int(rating_value.text) if rating_value is not None and rating_value.text.isdigit() else None,
            'hygiene_rating_date': rating_date.text if rating_date is not None else '',
            'hygiene_score_hygiene': int(hygiene.text) if hygiene is not None and hygiene.text and hygiene.text.isdigit() else None,
            'hygiene_score_structural': int(structural.text) if structural is not None and structural.text and structural.text.isdigit() else None,
            'hygiene_score_confidence': int(confidence.text) if confidence is not None and confidence.text and confidence.text.isdigit() else None,
        })

    df = pd.DataFrame(establishments)

    # Filter to restaurants/cafes
    restaurant_types = ['Restaurant/Cafe/Canteen', 'Takeaway/sandwich shop']
    df = df[df['fsa_business_type'].isin(restaurant_types)]

    print(f"  Loaded {len(df)} restaurants/cafes from FSA data")

    return df


def main():
    print("=" * 80)
    print("FSA HYGIENE MATCHER V2 - IMPROVED WITH NAME NORMALIZATION")
    print("=" * 80)
    print()
    print("Improvements:")
    print("  ✓ Corporate suffix removal (LTD, LIMITED, PLC, HOLDINGS)")
    print("  ✓ Location suffix removal (Plymouth, UK)")
    print("  ✓ Special character normalization")
    print("  ✓ Lowered confidence threshold: 60% (was 70%)")
    print()

    # 1. Load restaurants from database (only those WITHOUT hygiene ratings)
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
    AND hygiene_rating IS NULL
    ORDER BY restaurant_id
    """

    restaurants_df = pd.read_sql_query(restaurants_query, conn)
    conn.close()

    print(f"  Found {len(restaurants_df)} unmatched restaurants")

    # 2. Load FSA data from XML
    print("\nStep 2: Loading FSA hygiene data from XML...")
    fsa_df = parse_fsa_xml(FSA_XML_PATH)

    # 3. Match restaurants to FSA establishments
    print(f"\nStep 3: Matching restaurants (threshold: {CONFIDENCE_THRESHOLD}%)...")

    matches = []

    for idx, restaurant in restaurants_df.iterrows():
        best_match = None
        best_score = 0
        best_reason = ""

        restaurant_name = restaurant['name']
        restaurant_address = restaurant['fsa_address_line1'] or restaurant['address'] or restaurant['google_formatted_address']
        restaurant_postcode = restaurant['fsa_postcode']

        # Try to match against all FSA establishments
        for _, fsa_row in fsa_df.iterrows():
            fsa_business_name = fsa_row['fsa_business_name']
            fsa_address = fsa_row['fsa_address_line1']
            fsa_postcode = fsa_row['fsa_postcode']

            score, reason = calculate_match_score(
                restaurant_name,
                restaurant_address,
                restaurant_postcode,
                fsa_business_name,
                fsa_address,
                fsa_postcode
            )

            if score > best_score:
                best_score = score
                best_reason = reason
                best_match = fsa_row

        # Record the best match (even if below threshold)
        if best_match is not None:
            matches.append({
                'restaurant_id': restaurant['restaurant_id'],
                'restaurant_name': restaurant_name,
                'restaurant_address': restaurant_address,
                'restaurant_postcode': restaurant_postcode,
                'match_score': best_score,
                'match_reason': best_reason,
                'fsa_id': best_match['fsa_id'],
                'fsa_business_name': best_match['fsa_business_name'],
                'fsa_business_type': best_match['fsa_business_type'],
                'fsa_address_line1': best_match['fsa_address_line1'],
                'fsa_address_line2': best_match['fsa_address_line2'],
                'fsa_postcode': best_match['fsa_postcode'],
                'hygiene_rating': best_match['hygiene_rating'],
                'hygiene_rating_date': best_match['hygiene_rating_date'],
                'hygiene_score_hygiene': best_match['hygiene_score_hygiene'],
                'hygiene_score_structural': best_match['hygiene_score_structural'],
                'hygiene_score_confidence': best_match['hygiene_score_confidence'],
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

        print(f"\nHygiene rating distribution:")
        for rating in sorted(confident_matches['hygiene_rating'].dropna().unique()):
            count = len(confident_matches[confident_matches['hygiene_rating'] == rating])
            print(f"  {int(rating)}★: {count} restaurants")

        print(f"\nNEW matches in 60-69% range (lowered threshold):")
        new_matches = confident_matches[
            (confident_matches['match_score'] >= 60) &
            (confident_matches['match_score'] < 70)
        ].sort_values('match_score', ascending=False)

        if len(new_matches) > 0:
            for idx, row in new_matches.head(15).iterrows():
                rating = int(row['hygiene_rating']) if pd.notna(row['hygiene_rating']) else 0
                print(f"  {row['restaurant_name']}: {rating}★ ({row['match_score']:.0f}%)")
                print(f"    → FSA: {row['fsa_business_name']}")
                print(f"    Reason: {row['match_reason']}")
        else:
            print("  (None)")

    print("\n" + "=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print(f"1. Review confident matches in {OUTPUT_CSV_CONFIDENT}")
    print(f"2. Manually verify matches with 60-69% confidence")
    print(f"3. Run import script to update database")
    print()


if __name__ == '__main__':
    main()
