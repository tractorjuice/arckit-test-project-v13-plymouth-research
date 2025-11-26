"""
Fuzzy Matching Utilities
========================

Common fuzzy matching functionality used across data sources
(FSA hygiene, licensing, business rates, etc.)

Author: Plymouth Research Team
Date: 2025-11-26
"""

import re
import logging
from typing import Optional, List, Dict, Any, Tuple
from difflib import SequenceMatcher
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class MatchResult:
    """Result of a fuzzy match operation."""
    source_id: Any
    target_id: Optional[int]
    confidence: float
    name_similarity: float
    address_similarity: float
    postcode_match: bool
    match_type: str
    match_reason: str

    @property
    def is_matched(self) -> bool:
        return self.target_id is not None


class FuzzyMatcher:
    """
    Fuzzy string matching for data reconciliation.

    Provides consistent matching logic across different data sources
    with configurable thresholds and scoring weights.
    """

    # Default configuration
    DEFAULT_CONFIG = {
        'name_weight': 50.0,
        'postcode_bonus': 30.0,
        'address_weight': 20.0,
        'confidence_threshold': 60.0,
        'high_confidence_threshold': 95.0,
    }

    # Corporate suffixes to remove during normalization
    CORPORATE_SUFFIXES = [
        'LIMITED', 'LTD', 'PLC', 'HOLDINGS', 'GROUP', 'UK', 'INC',
        'COMPANY', 'CO', 'CORP', 'CORPORATION'
    ]

    # Location suffixes to remove
    LOCATION_SUFFIXES = [
        'PLYMOUTH', '(PLYMOUTH)', '- PLYMOUTH', ', PLYMOUTH',
        'ROYAL WILLIAM YARD', 'BARBICAN', 'SUTTON HARBOUR'
    ]

    def __init__(self, config: Optional[Dict[str, float]] = None):
        """
        Initialize fuzzy matcher.

        Args:
            config: Optional configuration overrides
        """
        self.config = {**self.DEFAULT_CONFIG, **(config or {})}
        logger.info(f"FuzzyMatcher initialized with config: {self.config}")

    def match_records(
        self,
        source_records: List[Dict[str, Any]],
        target_records: List[Dict[str, Any]],
        source_name_key: str = 'name',
        source_address_key: str = 'address',
        target_name_key: str = 'name',
        target_address_key: str = 'address',
        target_id_key: str = 'restaurant_id',
    ) -> List[MatchResult]:
        """
        Match source records to target records.

        Args:
            source_records: Records to match (e.g., FSA establishments)
            target_records: Records to match against (e.g., restaurants)
            source_name_key: Key for name in source records
            source_address_key: Key for address in source records
            target_name_key: Key for name in target records
            target_address_key: Key for address in target records
            target_id_key: Key for ID in target records

        Returns:
            List of MatchResult objects
        """
        results = []

        for source in source_records:
            source_name = source.get(source_name_key, '')
            source_address = source.get(source_address_key, '')

            best_match = self.find_best_match(
                source_name,
                source_address,
                target_records,
                target_name_key,
                target_address_key,
                target_id_key,
            )

            if best_match:
                target_id, confidence, name_sim, addr_sim, postcode, match_type = best_match
                result = MatchResult(
                    source_id=source.get('id', source.get(source_name_key)),
                    target_id=target_id if confidence >= self.config['confidence_threshold'] else None,
                    confidence=confidence,
                    name_similarity=name_sim,
                    address_similarity=addr_sim,
                    postcode_match=postcode,
                    match_type=match_type,
                    match_reason=self._build_reason(match_type, postcode),
                )
            else:
                result = MatchResult(
                    source_id=source.get('id', source.get(source_name_key)),
                    target_id=None,
                    confidence=0.0,
                    name_similarity=0.0,
                    address_similarity=0.0,
                    postcode_match=False,
                    match_type='unmatched',
                    match_reason='No matches found',
                )

            results.append(result)

        return results

    def find_best_match(
        self,
        source_name: str,
        source_address: str,
        targets: List[Dict[str, Any]],
        target_name_key: str = 'name',
        target_address_key: str = 'address',
        target_id_key: str = 'restaurant_id',
    ) -> Optional[Tuple[int, float, float, float, bool, str]]:
        """
        Find best matching target for a source record.

        Args:
            source_name: Source record name
            source_address: Source record address
            targets: List of target records
            target_name_key: Key for name in target records
            target_address_key: Key for address in target records
            target_id_key: Key for ID in target records

        Returns:
            Tuple of (target_id, confidence, name_sim, addr_sim, postcode_match, match_type)
            or None if no match found
        """
        normalized_source_name = self.normalize_name(source_name)
        source_postcode = self.extract_postcode(source_address)

        best_result = None
        best_score = 0.0

        for target in targets:
            target_name = target.get(target_name_key, '')
            target_address = target.get(target_address_key, '') or ''
            target_id = target.get(target_id_key)

            if not target_name:
                continue

            normalized_target_name = self.normalize_name(target_name)
            target_postcode = self.extract_postcode(target_address)

            # Calculate name similarity
            name_similarity = self.string_similarity(normalized_source_name, normalized_target_name) * 100

            # Start with weighted name similarity
            score = name_similarity * (self.config['name_weight'] / 100)

            # Postcode match bonus
            postcode_match = False
            if source_postcode and target_postcode:
                if source_postcode == target_postcode:
                    score += self.config['postcode_bonus']
                    postcode_match = True

            # Address similarity bonus
            address_similarity = 0.0
            if source_address and target_address:
                address_similarity = self.string_similarity(
                    source_address.lower(),
                    target_address.lower()
                )
                score += address_similarity * self.config['address_weight']

            # Determine match type
            if name_similarity >= 95:
                match_type = 'exact_name'
            elif name_similarity >= 80:
                match_type = 'similar_name'
            elif name_similarity >= 60:
                match_type = 'partial_name'
            else:
                match_type = 'low_similarity'

            # Update best match
            if score > best_score:
                best_score = score
                best_result = (
                    target_id,
                    score,
                    name_similarity,
                    address_similarity * 100,
                    postcode_match,
                    match_type,
                )

        return best_result

    def normalize_name(self, name: str) -> str:
        """
        Normalize a business name for matching.

        Removes:
        - Corporate suffixes (Ltd, Limited, etc.)
        - Location suffixes (Plymouth, etc.)
        - Special characters
        - Extra whitespace

        Args:
            name: Raw business name

        Returns:
            Normalized name (uppercase)
        """
        if not name:
            return ""

        result = name.upper()

        # Remove corporate suffixes
        for suffix in self.CORPORATE_SUFFIXES:
            result = re.sub(rf'\b{suffix}\b', '', result)

        # Remove location suffixes
        for location in self.LOCATION_SUFFIXES:
            result = result.replace(location, '')

        # Remove special characters (keep alphanumeric and spaces)
        result = re.sub(r'[^\w\s]', '', result)

        # Collapse whitespace
        result = re.sub(r'\s+', ' ', result).strip()

        return result

    def extract_postcode(self, address: str) -> str:
        """
        Extract UK postcode from address string.

        Args:
            address: Full address string

        Returns:
            Normalized postcode or empty string
        """
        if not address:
            return ""

        # UK postcode pattern
        pattern = r'\b([A-Z]{1,2}\d{1,2}[A-Z]?\s?\d[A-Z]{2})\b'
        match = re.search(pattern, address.upper())

        if match:
            postcode = match.group(1).replace(' ', '')
            # Add standard space before last 3 characters
            if len(postcode) >= 5:
                return postcode[:-3] + ' ' + postcode[-3:]

        return ""

    @staticmethod
    def string_similarity(s1: str, s2: str) -> float:
        """
        Calculate string similarity ratio.

        Args:
            s1: First string
            s2: Second string

        Returns:
            Similarity ratio (0.0 to 1.0)
        """
        if not s1 or not s2:
            return 0.0
        return SequenceMatcher(None, s1, s2).ratio()

    @staticmethod
    def _build_reason(match_type: str, postcode_match: bool) -> str:
        """Build human-readable match reason."""
        reason = match_type
        if postcode_match:
            reason += '+postcode'
        return reason


# ============================================================================
# Convenience Functions
# ============================================================================

def normalize_business_name(name: str) -> str:
    """Convenience function for name normalization."""
    return FuzzyMatcher().normalize_name(name)


def extract_uk_postcode(address: str) -> str:
    """Convenience function for postcode extraction."""
    return FuzzyMatcher().extract_postcode(address)


def calculate_similarity(s1: str, s2: str) -> float:
    """Convenience function for string similarity."""
    return FuzzyMatcher.string_similarity(s1, s2)


# ============================================================================
# CLI Entry Point
# ============================================================================

if __name__ == "__main__":
    import argparse

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # Demo usage
    matcher = FuzzyMatcher()

    test_names = [
        ("Rockfish Plymouth Limited", "Rockfish"),
        ("The Boathouse Cafe (Plymouth)", "Boathouse Cafe"),
        ("McDonald's Restaurants Ltd", "McDonalds"),
    ]

    print("Name Normalization Demo:")
    print("-" * 60)
    for raw, expected in test_names:
        normalized = matcher.normalize_name(raw)
        print(f"  '{raw}' -> '{normalized}'")
        print(f"    (expected similar to: '{expected}')")
    print()

    test_addresses = [
        "123 High Street, Plymouth, PL1 2AB",
        "Sutton Harbour PL4 0DW",
        "Royal William Yard Plymouth PL1 3RP",
    ]

    print("Postcode Extraction Demo:")
    print("-" * 60)
    for addr in test_addresses:
        postcode = matcher.extract_postcode(addr)
        print(f"  '{addr}' -> '{postcode}'")
