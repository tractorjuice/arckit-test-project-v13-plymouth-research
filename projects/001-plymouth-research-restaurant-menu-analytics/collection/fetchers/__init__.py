"""
Data Fetchers for Plymouth Research
====================================

Modules for fetching data from external sources:
- FSA (Food Standards Agency) hygiene ratings
- Trustpilot reviews
- Google Places API
- Companies House API
- Plymouth licensing data
"""

from .base_fetcher import BaseFetcher
from .hygiene_fetcher import HygieneFetcher
from .trustpilot_fetcher import TrustpilotFetcher
from .google_fetcher import GooglePlacesFetcher

__all__ = [
    'BaseFetcher',
    'HygieneFetcher',
    'TrustpilotFetcher',
    'GooglePlacesFetcher',
]
