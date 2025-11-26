"""
FSA Food Hygiene Rating Fetcher
================================

Fetches and matches FSA Food Hygiene Rating data from XML.

Data Source: Food Standards Agency Open Data
URL: https://ratings.food.gov.uk/api/open-data-files/FHRS891en-GB.xml
License: Open Government License v3.0

Author: Plymouth Research Team
Date: 2025-11-26
"""

import logging
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional, Dict, List, Any, Tuple
from difflib import SequenceMatcher
from datetime import datetime

from .base_fetcher import BaseFetcher

logger = logging.getLogger(__name__)


class HygieneFetcher(BaseFetcher):
    """
    Fetcher for FSA Food Hygiene Rating data.

    Parses FSA XML files and matches establishments to restaurants
    using fuzzy name matching with postcode and address verification.
    """

    # Business types to include (restaurants, cafes, pubs, etc.)
    INCLUDED_BUSINESS_TYPES = [
        "Restaurant/Cafe/Canteen",
        "Pub/bar/nightclub",
        "Takeaway/sandwich shop",
        "Hotel/bed & breakfast/guest house",
        "Other catering premises",
    ]

    # Matching thresholds
    CONFIDENCE_THRESHOLD = 60.0  # Minimum score for auto-match
    HIGH_CONFIDENCE_THRESHOLD = 95.0  # Score for "exact match"

    def __init__(self, db_path: Optional[Path] = None, xml_path: Optional[Path] = None):
        """
        Initialize hygiene fetcher.

        Args:
            db_path: Path to SQLite database
            xml_path: Path to FSA XML file
        """
        super().__init__(db_path)

        if xml_path is None:
            from shared.config import get_config
            config = get_config()
            xml_path = config.raw_data_dir / "plymouth_fsa_data.xml"

        self.xml_path = xml_path

    def fetch(self, **kwargs) -> List[Dict[str, Any]]:
        """
        Parse FSA XML file and extract establishment data.

        Returns:
            List of establishment dictionaries
        """
        xml_path = kwargs.get('xml_path', self.xml_path)

        if not Path(xml_path).exists():
            raise FileNotFoundError(f"FSA XML file not found: {xml_path}")

        logger.info(f"Parsing FSA XML from: {xml_path}")

        tree = ET.parse(xml_path)
        root = tree.getroot()

        establishments = []

        for est in root.findall('.//EstablishmentDetail'):
            business_type = est.findtext('BusinessType', '')

            # Filter to relevant business types
            if business_type not in self.INCLUDED_BUSINESS_TYPES:
                continue

            establishment = {
                'fsa_id': est.findtext('FHRSID'),
                'business_name': est.findtext('BusinessName', ''),
                'business_type': business_type,
                'address_line1': est.findtext('AddressLine1', ''),
                'address_line2': est.findtext('AddressLine2', ''),
                'address_line3': est.findtext('AddressLine3', ''),
                'address_line4': est.findtext('AddressLine4', ''),
                'postcode': est.findtext('PostCode', ''),
                'rating_value': est.findtext('RatingValue', ''),
                'rating_date': est.findtext('RatingDate', ''),
                'latitude': est.findtext('.//Geocode/Latitude', ''),
                'longitude': est.findtext('.//Geocode/Longitude', ''),
                'local_authority_business_id': est.findtext('LocalAuthorityBusinessID', ''),
                'rating_key': est.findtext('RatingKey', ''),
                'scheme_type': est.findtext('SchemeType', ''),
                'new_rating_pending': est.findtext('NewRatingPending', ''),
            }

            # Parse scores
            scores = est.find('Scores')
            if scores is not None:
                establishment['score_hygiene'] = scores.findtext('Hygiene', '')
                establishment['score_structural'] = scores.findtext('Structural', '')
                establishment['score_confidence'] = scores.findtext('ConfidenceInManagement', '')

            establishments.append(establishment)

        logger.info(f"Parsed {len(establishments)} establishments from FSA XML")
        return establishments

    def process(self, data: List[Dict[str, Any]]) -> int:
        """
        Match FSA establishments to restaurants and update database.

        Args:
            data: List of FSA establishment dictionaries

        Returns:
            Number of restaurants successfully matched
        """
        restaurants = self.get_restaurants(active_only=True)
        logger.info(f"Matching {len(data)} FSA establishments to {len(restaurants)} restaurants")

        matched_count = 0
        matches = []
        unmatched = []

        for fsa in data:
            best_match = self._find_best_match(fsa, restaurants)

            if best_match:
                restaurant_id, confidence, match_reason = best_match

                if confidence >= self.CONFIDENCE_THRESHOLD:
                    # Update database
                    updates = self._build_updates(fsa)
                    if self.update_restaurant(restaurant_id, updates):
                        matched_count += 1
                        matches.append({
                            'fsa_id': fsa['fsa_id'],
                            'restaurant_id': restaurant_id,
                            'confidence': confidence,
                            'reason': match_reason,
                        })
                        logger.debug(f"Matched: {fsa['business_name']} -> restaurant_id={restaurant_id} ({confidence:.1f}%)")
                else:
                    unmatched.append(fsa)
            else:
                unmatched.append(fsa)

        # Log summary
        logger.info(f"Matched: {matched_count}/{len(data)} establishments")
        logger.info(f"Unmatched: {len(unmatched)} establishments")

        return matched_count

    def _find_best_match(
        self,
        fsa: Dict[str, Any],
        restaurants: List[Dict[str, Any]]
    ) -> Optional[Tuple[int, float, str]]:
        """
        Find best matching restaurant for an FSA establishment.

        Args:
            fsa: FSA establishment dictionary
            restaurants: List of restaurant dictionaries

        Returns:
            Tuple of (restaurant_id, confidence_score, match_reason) or None
        """
        fsa_name = self._normalize_name(fsa['business_name'])
        fsa_postcode = self._normalize_postcode(fsa['postcode'])
        fsa_address = self._build_address(fsa)

        best_match = None
        best_score = 0.0
        best_reason = ""

        for restaurant in restaurants:
            rest_name = self._normalize_name(restaurant['name'])
            rest_address = restaurant.get('address', '') or ''
            rest_postcode = self._extract_postcode(rest_address)

            # Calculate name similarity (0-100)
            name_similarity = SequenceMatcher(None, fsa_name, rest_name).ratio() * 100

            # Start with name similarity as base score
            score = name_similarity * 0.5  # 50% weight

            # Postcode match bonus (30 points)
            postcode_match = False
            if fsa_postcode and rest_postcode:
                if fsa_postcode == rest_postcode:
                    score += 30
                    postcode_match = True

            # Address similarity bonus (0-20 points)
            if fsa_address and rest_address:
                address_similarity = SequenceMatcher(
                    None,
                    fsa_address.lower(),
                    rest_address.lower()
                ).ratio()
                score += address_similarity * 20

            # Determine match reason
            if name_similarity >= 95:
                reason = "exact_name"
            elif name_similarity >= 80:
                reason = "similar_name"
            elif name_similarity >= 60:
                reason = "partial_name"
            else:
                reason = "low_similarity"

            if postcode_match:
                reason += "+postcode"

            # Update best match
            if score > best_score:
                best_score = score
                best_match = restaurant['restaurant_id']
                best_reason = reason

        if best_match and best_score >= self.CONFIDENCE_THRESHOLD:
            return (best_match, best_score, best_reason)

        return None

    def _build_updates(self, fsa: Dict[str, Any]) -> Dict[str, Any]:
        """Build database update dictionary from FSA data."""
        updates = {
            'fsa_id': int(fsa['fsa_id']) if fsa['fsa_id'] else None,
            'fsa_business_name': fsa['business_name'],
            'fsa_business_type': fsa['business_type'],
            'fsa_address_line1': fsa['address_line1'],
            'fsa_address_line2': fsa['address_line2'],
            'fsa_address_line3': fsa['address_line3'],
            'fsa_address_line4': fsa['address_line4'],
            'fsa_postcode': fsa['postcode'],
            'hygiene_rating_date': fsa['rating_date'],
            'fsa_local_authority_business_id': fsa['local_authority_business_id'],
            'fsa_rating_key': fsa['rating_key'],
            'fsa_scheme_type': fsa['scheme_type'],
            'fsa_new_rating_pending': fsa['new_rating_pending'],
            'hygiene_rating_fetched_at': datetime.now().isoformat(),
        }

        # Parse rating value
        rating_value = fsa['rating_value']
        if rating_value and rating_value.isdigit():
            updates['hygiene_rating'] = int(rating_value)
        elif rating_value == 'Exempt':
            updates['hygiene_rating'] = None
        elif rating_value == 'AwaitingInspection':
            updates['hygiene_rating'] = None

        # Parse scores
        if fsa.get('score_hygiene'):
            try:
                updates['hygiene_score_hygiene'] = int(fsa['score_hygiene'])
            except ValueError:
                pass

        if fsa.get('score_structural'):
            try:
                updates['hygiene_score_structural'] = int(fsa['score_structural'])
            except ValueError:
                pass

        if fsa.get('score_confidence'):
            try:
                updates['hygiene_score_confidence'] = int(fsa['score_confidence'])
            except ValueError:
                pass

        # Parse coordinates
        if fsa['latitude'] and fsa['longitude']:
            try:
                updates['fsa_latitude'] = float(fsa['latitude'])
                updates['fsa_longitude'] = float(fsa['longitude'])
            except ValueError:
                pass

        return updates

    @staticmethod
    def _normalize_name(name: str) -> str:
        """Normalize business name for matching."""
        if not name:
            return ""

        name = name.upper()

        # Remove corporate suffixes
        for suffix in ['LIMITED', 'LTD', 'PLC', 'HOLDINGS', 'GROUP', 'UK', 'INC']:
            name = re.sub(rf'\b{suffix}\b', '', name)

        # Remove location suffixes
        for location in ['PLYMOUTH', '(PLYMOUTH)', '- PLYMOUTH']:
            name = name.replace(location, '')

        # Remove special characters
        name = re.sub(r'[^\w\s]', '', name)

        # Collapse whitespace
        name = re.sub(r'\s+', ' ', name).strip()

        return name

    @staticmethod
    def _normalize_postcode(postcode: str) -> str:
        """Normalize UK postcode for matching."""
        if not postcode:
            return ""

        # Uppercase and remove spaces
        postcode = postcode.upper().replace(' ', '')

        # Add standard space before last 3 characters
        if len(postcode) >= 5:
            postcode = postcode[:-3] + ' ' + postcode[-3:]

        return postcode

    @staticmethod
    def _extract_postcode(address: str) -> str:
        """Extract UK postcode from address string."""
        if not address:
            return ""

        # UK postcode pattern
        pattern = r'\b([A-Z]{1,2}\d{1,2}[A-Z]?\s?\d[A-Z]{2})\b'
        match = re.search(pattern, address.upper())

        if match:
            postcode = match.group(1).replace(' ', '')
            if len(postcode) >= 5:
                return postcode[:-3] + ' ' + postcode[-3:]

        return ""

    @staticmethod
    def _build_address(fsa: Dict[str, Any]) -> str:
        """Build full address from FSA address lines."""
        parts = [
            fsa.get('address_line1', ''),
            fsa.get('address_line2', ''),
            fsa.get('address_line3', ''),
            fsa.get('address_line4', ''),
            fsa.get('postcode', ''),
        ]
        return ', '.join(p for p in parts if p)


# ============================================================================
# CLI Entry Point
# ============================================================================

if __name__ == "__main__":
    import argparse

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    parser = argparse.ArgumentParser(description="Fetch and match FSA hygiene ratings")
    parser.add_argument('--xml', type=str, help="Path to FSA XML file")
    parser.add_argument('--db', type=str, help="Path to database file")

    args = parser.parse_args()

    fetcher = HygieneFetcher(
        db_path=Path(args.db) if args.db else None,
        xml_path=Path(args.xml) if args.xml else None,
    )

    stats = fetcher.run()
    print(f"\nResults:")
    print(f"  Fetched: {stats['fetched']}")
    print(f"  Matched: {stats['matched']}")
    print(f"  Errors: {stats['errors']}")
