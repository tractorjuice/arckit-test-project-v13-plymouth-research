"""
Data Processing Layer for Plymouth Research
============================================

This package contains all data processing components:
- Database operations (connection, CRUD)
- Data matchers (fuzzy matching for FSA, licensing, business rates)
- Data importers (CSV/JSON to database)
- Data parsers (restaurant-specific HTML parsing)
"""

from .database import Database
from .matchers import FuzzyMatcher

__all__ = [
    'Database',
    'FuzzyMatcher',
]
