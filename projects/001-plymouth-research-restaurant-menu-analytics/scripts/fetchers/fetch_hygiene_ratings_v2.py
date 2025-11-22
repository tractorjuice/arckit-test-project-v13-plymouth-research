#!/usr/bin/env python3
"""
Fetch Hygiene Ratings Script (XML Version)
===========================================

Fetches Food Standards Agency (FSA) Food Hygiene Rating Scheme (FHRS) data
from the Plymouth XML data file.

Faster and more complete than API approach - processes all 1800+ establishments
from local XML file.

Author: Plymouth Research Team
Date: 2025-11-18
"""

import sqlite3
import xml.etree.ElementTree as ET
import re
import csv
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from datetime import datetime
from difflib import SequenceMatcher


def normalize_name(name: str) -> str:
    """Normalize restaurant name for matching."""
    normalized = name.lower()
    # Remove common location suffixes
    normalized = re.sub(r'\s+(plymouth|barbican|royal william yard|drake circus|city centre)$', '', normalized)
    # Remove special characters
    normalized = re.sub(r'[^\w\s&]', '', normalized)
    # Normalize whitespace
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    return normalized


def extract_postcode(address: str) -> Optional[str]:
    """Extract UK postcode from address string."""
    if not address:
        return None

    # UK postcode pattern
    postcode_pattern = r'\b([A-Z]{1,2}\d{1,2}[A-Z]?\s?\d[A-Z]{2})\b'
    match = re.search(postcode_pattern, address.upper())

    if match:
        postcode = match.group(1)
        # Ensure space before final 3 characters
        if len(postcode) >= 5 and postcode[-4] != ' ':
            postcode = postcode[:-3] + ' ' + postcode[-3:]
        return postcode

    return None


def calculate_similarity(str1: str, str2: str) -> float:
    """Calculate similarity ratio between two strings."""
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()


def parse_fsa_xml(xml_path: Path) -> List[Dict]:
    """
    Parse FSA XML file and extract restaurant/cafe establishments.

    Returns:
        List of establishment dictionaries
    """
    print("📄 Parsing FSA XML file...")

    tree = ET.parse(str(xml_path))
    root = tree.getroot()

    # Get header info
    header = root.find('Header')
    total_count = int(header.find('ItemCount').text)
    extract_date = header.find('ExtractDate').text

    print(f"  Extract Date: {extract_date}")
    print(f"  Total Establishments: {total_count:,}")

    establishments = []

    # Parse all establishments
    for est_elem in root.findall('.//EstablishmentDetail'):
        # Get business type
        business_type = est_elem.find('BusinessType')
        business_type_text = business_type.text if business_type is not None else ''

        # Filter for restaurants/cafes/canteens/pubs/bars
        if 'restaurant' not in business_type_text.lower() and \
           'cafe' not in business_type_text.lower() and \
           'canteen' not in business_type_text.lower() and \
           'pub' not in business_type_text.lower() and \
           'bar' not in business_type_text.lower() and \
           'nightclub' not in business_type_text.lower():
            continue

        # Extract data
        def get_text(elem, tag):
            """Safely get text from XML element."""
            node = elem.find(tag)
            return node.text if node is not None and node.text else ''

        # Get rating value
        rating_value = get_text(est_elem, 'RatingValue')
        if rating_value in ['AwaitingInspection', 'Awaiting Inspection', 'Exempt']:
            rating_numeric = None
        else:
            try:
                rating_numeric = int(rating_value) if rating_value else None
            except ValueError:
                rating_numeric = None

        # Get scores
        scores_elem = est_elem.find('Scores')
        if scores_elem is not None:
            hygiene_score = get_text(scores_elem, 'Hygiene')
            structural_score = get_text(scores_elem, 'Structural')
            confidence_score = get_text(scores_elem, 'ConfidenceInManagement')
        else:
            hygiene_score = structural_score = confidence_score = None

        # Build address (both combined and individual lines)
        address_line1 = get_text(est_elem, 'AddressLine1')
        address_line2 = get_text(est_elem, 'AddressLine2')
        address_line3 = get_text(est_elem, 'AddressLine3')
        address_line4 = get_text(est_elem, 'AddressLine4')
        address_parts = [address_line1, address_line2, address_line3, address_line4]
        full_address = ', '.join([p for p in address_parts if p])

        # Get GPS coordinates
        geocode_elem = est_elem.find('Geocode')
        if geocode_elem is not None:
            latitude_text = get_text(geocode_elem, 'Latitude')
            longitude_text = get_text(geocode_elem, 'Longitude')
            latitude = float(latitude_text) if latitude_text else None
            longitude = float(longitude_text) if longitude_text else None
        else:
            latitude = None
            longitude = None

        establishment = {
            'fsa_id': int(get_text(est_elem, 'FHRSID')),
            'business_name': get_text(est_elem, 'BusinessName'),
            'business_type': business_type_text,
            'address': full_address,
            'address_line1': address_line1,
            'address_line2': address_line2,
            'address_line3': address_line3,
            'address_line4': address_line4,
            'postcode': get_text(est_elem, 'PostCode'),
            'latitude': latitude,
            'longitude': longitude,
            'rating': rating_numeric,
            'rating_date': get_text(est_elem, 'RatingDate'),
            'rating_key': get_text(est_elem, 'RatingKey'),
            'hygiene_score': int(hygiene_score) if hygiene_score else None,
            'structural_score': int(structural_score) if structural_score else None,
            'confidence_score': int(confidence_score) if confidence_score else None,
            'local_authority': get_text(est_elem, 'LocalAuthorityName'),
            'local_authority_business_id': get_text(est_elem, 'LocalAuthorityBusinessID'),
            'local_authority_website': get_text(est_elem, 'LocalAuthorityWebSite'),
            'scheme_type': get_text(est_elem, 'SchemeType'),
            'new_rating_pending': get_text(est_elem, 'NewRatingPending')
        }

        establishments.append(establishment)

    print(f"  Found {len(establishments):,} restaurants/cafes/canteens/pubs/bars")
    print()

    return establishments


def find_best_match(
    restaurant_name: str,
    restaurant_address: Optional[str],
    fsa_establishments: List[Dict]
) -> Tuple[Optional[Dict], str, float]:
    """
    Find the best matching establishment from FSA data.

    Returns:
        Tuple of (best_match_dict, match_reason, confidence_score)
    """
    our_postcode = extract_postcode(restaurant_address) if restaurant_address else None
    normalized_name = normalize_name(restaurant_name)

    # Scoring system
    best_match = None
    best_score = 0
    match_reason = ""

    for est in fsa_establishments:
        score = 0
        reasons = []

        # Name similarity (0-100 points)
        fsa_name = normalize_name(est['business_name'])
        name_similarity = calculate_similarity(normalized_name, fsa_name)
        score += name_similarity * 100

        if name_similarity >= 0.95:
            reasons.append("exact_name")
        elif name_similarity >= 0.8:
            reasons.append("similar_name")
        elif name_similarity >= 0.6:
            reasons.append("partial_name")

        # Postcode match (50 bonus points)
        fsa_postcode = est['postcode']
        if our_postcode and fsa_postcode:
            if our_postcode.replace(' ', '').upper() == fsa_postcode.replace(' ', '').upper():
                score += 50
                reasons.append("postcode_match")

        # Address similarity (0-30 bonus points)
        if restaurant_address and est['address']:
            our_words = set(re.findall(r'\w+', restaurant_address.lower()))
            fsa_words = set(re.findall(r'\w+', est['address'].lower()))
            common_words = our_words & fsa_words

            if len(common_words) >= 3:
                score += min(len(common_words) * 5, 30)
                reasons.append("address_match")

        if score > best_score:
            best_score = score
            best_match = est
            match_reason = ", ".join(reasons) if reasons else "low_confidence"

    # Confidence threshold
    if best_score >= 70:
        return best_match, match_reason, best_score
    else:
        return None, "low_confidence", best_score


def main():
    """Main execution function."""
    db_path = Path(__file__).parent / "plymouth_research.db"
    xml_path = Path(__file__).parent / "data" / "raw" / "plymouth_fsa_data.xml"

    if not db_path.exists():
        print(f"❌ Database not found: {db_path}")
        return

    if not xml_path.exists():
        print(f"❌ FSA XML file not found: {xml_path}")
        print("Download from: https://ratings.food.gov.uk/api/open-data-files/FHRS891en-GB.xml")
        return

    print("=" * 70)
    print("Fetch Food Hygiene Ratings from FSA XML Data")
    print("=" * 70)
    print()

    # Parse FSA XML data
    fsa_establishments = parse_fsa_xml(xml_path)

    # Connect to database
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    # Get all restaurants without hygiene ratings
    cursor.execute("""
        SELECT restaurant_id, name, address
        FROM restaurants
        WHERE data_source IN ('real_scraped', 'google_discovered')
        AND is_active = 1
        ORDER BY name
    """)

    restaurants = cursor.fetchall()
    total = len(restaurants)

    print(f"📊 Processing {total} restaurants")
    print()

    # Track results
    success_count = 0
    not_found_count = 0
    low_confidence_count = 0
    unmatched = []
    matched_details = []

    for idx, (restaurant_id, name, address) in enumerate(restaurants, 1):
        print(f"[{idx}/{total}] {name}")

        # Find best match
        best_match, match_reason, confidence = find_best_match(name, address, fsa_establishments)

        if best_match:
            # Update database
            cursor.execute("""
                UPDATE restaurants
                SET
                    hygiene_rating = ?,
                    hygiene_rating_date = ?,
                    fsa_id = ?,
                    hygiene_rating_fetched_at = ?,
                    hygiene_score_hygiene = ?,
                    hygiene_score_structural = ?,
                    hygiene_score_confidence = ?,
                    fsa_business_type = ?,
                    fsa_local_authority = ?,
                    fsa_business_name = ?,
                    fsa_address_line1 = ?,
                    fsa_address_line2 = ?,
                    fsa_address_line3 = ?,
                    fsa_address_line4 = ?,
                    fsa_postcode = ?,
                    fsa_latitude = ?,
                    fsa_longitude = ?,
                    fsa_local_authority_business_id = ?,
                    fsa_rating_key = ?,
                    fsa_scheme_type = ?,
                    fsa_local_authority_website = ?,
                    fsa_new_rating_pending = ?
                WHERE restaurant_id = ?
            """, (
                best_match['rating'],
                best_match['rating_date'],
                best_match['fsa_id'],
                datetime.now().isoformat(),
                best_match['hygiene_score'],
                best_match['structural_score'],
                best_match['confidence_score'],
                best_match['business_type'],
                best_match['local_authority'],
                best_match['business_name'],
                best_match['address_line1'],
                best_match['address_line2'],
                best_match['address_line3'],
                best_match['address_line4'],
                best_match['postcode'],
                best_match['latitude'],
                best_match['longitude'],
                best_match['local_authority_business_id'],
                best_match['rating_key'],
                best_match['scheme_type'],
                best_match['local_authority_website'],
                best_match['new_rating_pending'],
                restaurant_id
            ))

            conn.commit()

            rating = best_match['rating']
            stars = "⭐" * rating if rating else "⏳"
            print(f"  ✅ Matched: {best_match['business_name']}")
            print(f"  Rating: {stars} ({rating if rating else 'Awaiting'})")
            print(f"  Date: {best_match['rating_date'][:10] if best_match['rating_date'] else 'N/A'}")
            print(f"  Confidence: {confidence:.1f}% ({match_reason})")

            success_count += 1
            matched_details.append({
                'our_name': name,
                'fsa_name': best_match['business_name'],
                'rating': rating,
                'confidence': f"{confidence:.1f}%",
                'match_reason': match_reason
            })
        else:
            print(f"  ⚠ No confident match found (best: {confidence:.1f}%)")
            not_found_count += 1
            unmatched.append({
                'restaurant_id': restaurant_id,
                'name': name,
                'address': address if address else 'No address',
                'best_confidence': f"{confidence:.1f}%"
            })

        print()

    # Export unmatched restaurants
    if unmatched:
        unmatched_file = Path(__file__).parent / "data" / "processed" / "unmatched_hygiene_ratings.csv"
        with open(unmatched_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['restaurant_id', 'name', 'address', 'best_confidence'])
            writer.writeheader()
            writer.writerows(unmatched)

        print(f"📄 Exported {len(unmatched)} unmatched to: {unmatched_file.name}")
        print()

    # Export matched details
    if matched_details:
        matched_file = Path(__file__).parent / "data" / "processed" / "matched_hygiene_ratings.csv"
        with open(matched_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['our_name', 'fsa_name', 'rating', 'confidence', 'match_reason'])
            writer.writeheader()
            writer.writerows(matched_details)

        print(f"📄 Exported {len(matched_details)} matches to: {matched_file.name}")
        print()

    # Summary
    print("=" * 70)
    print("✅ Hygiene Rating Fetch Complete!")
    print("=" * 70)
    print()
    print(f"📊 Results:")
    print(f"   • Successfully matched: {success_count} ({success_count/total*100:.1f}%)")
    print(f"   • Not matched: {not_found_count} ({not_found_count/total*100:.1f}%)")
    print(f"   • Total processed: {total}")
    print()

    if success_count > 0:
        # Show rating distribution
        cursor.execute("""
            SELECT hygiene_rating, COUNT(*) as count
            FROM restaurants
            WHERE hygiene_rating IS NOT NULL AND data_source IN ('real_scraped', 'google_discovered')
            GROUP BY hygiene_rating
            ORDER BY hygiene_rating DESC
        """)

        print("⭐ Rating Distribution:")
        rating_data = cursor.fetchall()
        for rating, count in rating_data:
            stars = "⭐" * rating
            print(f"   {stars} ({rating}): {count} restaurants")

        print()

        # Calculate average rating
        cursor.execute("""
            SELECT AVG(hygiene_rating) as avg_rating
            FROM restaurants
            WHERE hygiene_rating IS NOT NULL AND data_source IN ('real_scraped', 'google_discovered')
        """)
        avg_rating = cursor.fetchone()[0]
        print(f"📈 Average hygiene rating: {avg_rating:.2f}/5")

    conn.close()


if __name__ == "__main__":
    main()
