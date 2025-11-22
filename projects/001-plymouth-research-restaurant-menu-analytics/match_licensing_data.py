#!/usr/bin/env python3
"""
Plymouth Licensing Data Matcher

Matches restaurants in plymouth_research.db with licensing premises from
plymouth_licensing_complete_fixed.json using name normalization, postcode,
and address similarity scoring.

Scoring System:
- Name similarity: 0-50 points (difflib.SequenceMatcher)
- Postcode match: 30 bonus points (exact match)
- Address similarity: 0-20 bonus points (word matching)
- Confidence threshold: 60 points for auto-match

Author: Claude Code
Date: 2025-11-22
"""

import sqlite3
import json
import re
import difflib
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import pandas as pd

def normalize_business_name(name: str) -> str:
    """
    Normalize business name for better matching.
    Removes corporate suffixes, location suffixes, special characters.
    """
    if not name or pd.isna(name):
        return ""

    name = str(name).upper().strip()

    # Remove corporate suffixes
    corporate_patterns = [
        r'\s+LIMITED\s*$',
        r'\s+LTD\.?\s*$',
        r'\s+PLC\.?\s*$',
        r'\s+HOLDINGS?\s*$',
        r'\s+\(UK\)\s*$',
        r'\s+UK\s*$',
        r'\s+GROUP\s*$',
        r'\s+RESTAURANTS?\s*$',
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

    # Remove special characters except &
    name = re.sub(r'[^\w\s&#]', '', name)
    name = re.sub(r'\s+', ' ', name).strip()

    return name

def extract_postcode(text: str) -> Optional[str]:
    """Extract UK postcode from text."""
    if not text:
        return None

    # UK postcode pattern
    pattern = r'[A-Z]{1,2}\d{1,2}\s?\d[A-Z]{2}'
    match = re.search(pattern, text.upper())

    if match:
        postcode = match.group(0).replace(' ', '')
        # Normalize: "PL12AB" -> "PL1 2AB"
        return f"{postcode[:-3]} {postcode[-3:]}"

    return None

def calculate_name_similarity(name1: str, name2: str) -> float:
    """Calculate similarity between two names (0-100)."""
    norm1 = normalize_business_name(name1)
    norm2 = normalize_business_name(name2)

    if not norm1 or not norm2:
        return 0.0

    return difflib.SequenceMatcher(None, norm1, norm2).ratio() * 100

def calculate_address_similarity(addr1: str, addr2: str) -> int:
    """Calculate address similarity score (0-20 points)."""
    if not addr1 or not addr2:
        return 0

    # Normalize addresses
    words1 = set(normalize_business_name(addr1).split())
    words2 = set(normalize_business_name(addr2).split())

    # Count common words (excluding very common ones)
    common_words = words1 & words2
    stop_words = {'THE', 'A', 'AN', 'OF', 'AT', 'IN', 'ON', 'FOR', 'WITH'}
    meaningful_common = common_words - stop_words

    # 5 points per meaningful common word, max 20
    return min(len(meaningful_common) * 5, 20)

def calculate_match_confidence(
    rest_name: str,
    rest_address: str,
    rest_postcode: str,
    premises_name: str,
    premises_address: str,
) -> Tuple[float, str, Dict[str, any]]:
    """
    Calculate overall match confidence score.

    Returns:
        (confidence_score, match_reason, components)
    """
    components = {}

    # 1. Name similarity (0-50 points)
    name_sim = calculate_name_similarity(rest_name, premises_name)
    name_score = (name_sim / 100) * 50
    components['name_similarity'] = name_sim
    components['name_score'] = name_score

    # 2. Postcode match (30 bonus points)
    premises_postcode = extract_postcode(premises_address)
    postcode_match = False
    postcode_score = 0

    if rest_postcode and premises_postcode:
        # Normalize both postcodes for comparison
        norm_rest_pc = rest_postcode.replace(' ', '').upper()
        norm_prem_pc = premises_postcode.replace(' ', '').upper()
        if norm_rest_pc == norm_prem_pc:
            postcode_match = True
            postcode_score = 30

    components['postcode_match'] = postcode_match
    components['postcode_score'] = postcode_score
    components['rest_postcode'] = rest_postcode
    components['premises_postcode'] = premises_postcode

    # 3. Address similarity (0-20 points)
    address_score = calculate_address_similarity(rest_address, premises_address)
    components['address_score'] = address_score

    # Total confidence
    total_confidence = name_score + postcode_score + address_score
    components['total_confidence'] = total_confidence

    # Match reason
    reasons = []
    if name_sim >= 95:
        reasons.append("exact_name")
    elif name_sim >= 80:
        reasons.append("similar_name")
    elif name_sim >= 60:
        reasons.append("partial_name")
    else:
        reasons.append("weak_name")

    if postcode_match:
        reasons.append("postcode_match")

    if address_score >= 15:
        reasons.append("strong_address")
    elif address_score >= 10:
        reasons.append("good_address")

    match_reason = " + ".join(reasons)

    return total_confidence, match_reason, components

def load_restaurants_from_db() -> pd.DataFrame:
    """Load all active restaurants from database."""
    conn = sqlite3.connect('plymouth_research.db')

    query = """
        SELECT
            restaurant_id,
            name,
            address,
            postcode
        FROM restaurants
        WHERE is_active = 1
        ORDER BY restaurant_id
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    return df

def load_licensing_premises() -> List[Dict]:
    """Load all licensing premises from JSON."""
    json_path = Path('plymouth_licensing_complete_fixed.json')

    if not json_path.exists():
        raise FileNotFoundError(f"{json_path} not found")

    with open(json_path, 'r', encoding='utf-8') as f:
        premises = json.load(f)

    return premises

def find_best_match(
    rest_name: str,
    rest_address: str,
    rest_postcode: str,
    premises_list: List[Dict],
    confidence_threshold: float = 60.0
) -> Optional[Dict]:
    """Find best matching premises for a restaurant."""
    best_match = None
    best_confidence = 0.0

    for premises in premises_list:
        premises_name = premises.get('name', '')
        premises_address = premises.get('address', '')

        confidence, reason, components = calculate_match_confidence(
            rest_name,
            rest_address,
            rest_postcode,
            premises_name,
            premises_address
        )

        if confidence >= confidence_threshold and confidence > best_confidence:
            best_confidence = confidence
            best_match = {
                'premises': premises,
                'confidence': confidence,
                'reason': reason,
                'components': components
            }

    return best_match

def match_all_restaurants(
    restaurants_df: pd.DataFrame,
    premises_list: List[Dict],
    confidence_threshold: float = 60.0
) -> Tuple[List[Dict], List[Dict]]:
    """
    Match all restaurants against licensing premises.

    Returns:
        (matched_restaurants, unmatched_restaurants)
    """
    matched = []
    unmatched = []

    total = len(restaurants_df)

    print(f"\nMatching {total} restaurants against {len(premises_list)} licensing premises...")
    print(f"Confidence threshold: {confidence_threshold}")
    print("=" * 80)

    for idx, row in restaurants_df.iterrows():
        rest_id = row['restaurant_id']
        rest_name = row['name']
        rest_address = row.get('address', '')
        rest_postcode = row.get('postcode', '')

        print(f"\n[{idx + 1}/{total}] {rest_name}")

        match = find_best_match(
            rest_name,
            rest_address,
            rest_postcode,
            premises_list,
            confidence_threshold
        )

        if match:
            premises = match['premises']
            confidence = match['confidence']
            reason = match['reason']
            components = match['components']

            print(f"  ✓ MATCH: {premises['name']}")
            print(f"    Confidence: {confidence:.1f} ({reason})")
            print(f"    Components: name={components['name_similarity']:.0f}%, "
                  f"postcode={'✓' if components['postcode_match'] else '✗'}, "
                  f"address={components['address_score']}")

            # Extract license details
            details = premises.get('details', {})

            matched.append({
                'restaurant_id': rest_id,
                'restaurant_name': rest_name,
                'restaurant_address': rest_address,
                'restaurant_postcode': rest_postcode,
                'premises_id': premises.get('premises_id'),
                'premises_name': premises.get('name'),
                'premises_address': premises.get('address'),
                'license_number': details.get('license_number'),
                'license_url': details.get('license_url'),
                'dps_name': details.get('dps_name'),
                'license_holder': details.get('license_holder'),
                'licensable_activities': details.get('licensable_activities', []),
                'opening_hours': details.get('opening_hours', []),
                'activity_hours': details.get('activity_hours', []),
                'conditions': details.get('conditions', {}),
                'validity_from': details.get('validity_from'),
                'validity_to': details.get('validity_to'),
                'match_confidence': confidence,
                'match_reason': reason,
                'scraped_at': premises.get('scraped_at')
            })
        else:
            print(f"  ✗ NO MATCH")
            unmatched.append({
                'restaurant_id': rest_id,
                'restaurant_name': rest_name,
                'restaurant_address': rest_address,
                'restaurant_postcode': rest_postcode
            })

    return matched, unmatched

def export_to_csv(matched: List[Dict], unmatched: List[Dict]):
    """Export matches and unmatched to CSV files."""
    # Export all matches
    matched_df = pd.DataFrame(matched)
    matched_df.to_csv('licensing_matches_all.csv', index=False)
    print(f"\n✓ Exported {len(matched)} matches to licensing_matches_all.csv")

    # Export high-confidence matches (80+)
    if len(matched) > 0:
        confident_df = matched_df[matched_df['match_confidence'] >= 80]
        confident_df.to_csv('licensing_matches_confident.csv', index=False)
        print(f"✓ Exported {len(confident_df)} confident matches (≥80%) to licensing_matches_confident.csv")

    # Export unmatched
    unmatched_df = pd.DataFrame(unmatched)
    unmatched_df.to_csv('licensing_unmatched.csv', index=False)
    print(f"✓ Exported {len(unmatched)} unmatched to licensing_unmatched.csv")

def main():
    """Main matching workflow."""
    print("=" * 80)
    print("PLYMOUTH LICENSING DATA MATCHER")
    print("=" * 80)
    print("Matches restaurants in database with scraped licensing premises")
    print("Using name normalization + postcode + address similarity scoring")
    print("=" * 80)

    # Configuration
    CONFIDENCE_THRESHOLD = 60.0  # Same as successful FSA matcher

    # Load data
    print("\n1. Loading data...")
    restaurants_df = load_restaurants_from_db()
    print(f"   ✓ Loaded {len(restaurants_df)} restaurants from database")

    premises_list = load_licensing_premises()
    print(f"   ✓ Loaded {len(premises_list)} licensing premises from JSON")

    # Match restaurants
    print("\n2. Matching restaurants...")
    matched, unmatched = match_all_restaurants(
        restaurants_df,
        premises_list,
        CONFIDENCE_THRESHOLD
    )

    # Summary
    print("\n" + "=" * 80)
    print("MATCHING COMPLETE - SUMMARY")
    print("=" * 80)
    print(f"Total restaurants: {len(restaurants_df)}")
    print(f"Matched: {len(matched)} ({len(matched)/len(restaurants_df)*100:.1f}%)")
    print(f"Unmatched: {len(unmatched)} ({len(unmatched)/len(restaurants_df)*100:.1f}%)")

    if len(matched) > 0:
        confidences = [m['match_confidence'] for m in matched]
        print(f"\nConfidence range: {min(confidences):.1f} - {max(confidences):.1f}")
        print(f"Average confidence: {sum(confidences)/len(confidences):.1f}")

        # Confidence breakdown
        very_high = sum(1 for c in confidences if c >= 90)
        high = sum(1 for c in confidences if 80 <= c < 90)
        medium = sum(1 for c in confidences if 70 <= c < 80)
        low = sum(1 for c in confidences if 60 <= c < 70)

        print(f"\nConfidence breakdown:")
        print(f"  ≥90 (Very High): {very_high} ({very_high/len(matched)*100:.0f}%)")
        print(f"  80-89 (High): {high} ({high/len(matched)*100:.0f}%)")
        print(f"  70-79 (Medium): {medium} ({medium/len(matched)*100:.0f}%)")
        print(f"  60-69 (Low): {low} ({low/len(matched)*100:.0f}%)")

    # Export results
    print("\n3. Exporting results...")
    export_to_csv(matched, unmatched)

    print("\n" + "=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print("1. Review licensing_matches_all.csv")
    print("2. Check licensing_matches_confident.csv for high-confidence matches")
    print("3. Manually verify questionable matches (confidence 60-80)")
    print("4. Create licensing_matches_verified.csv with approved matches")
    print("5. Run import script to update database")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
