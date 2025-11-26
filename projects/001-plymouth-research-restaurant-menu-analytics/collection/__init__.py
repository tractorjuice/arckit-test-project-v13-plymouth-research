"""
Data Collection Layer for Plymouth Research
============================================

This package contains all data collection components:
- Web scrapers (menu scraping with robots.txt compliance)
- Data fetchers (FSA, Trustpilot, Google Places, Companies House)

All collection operations respect ethical scraping principles:
- robots.txt compliance (checked BEFORE every request)
- Rate limiting (5 seconds minimum per domain)
- Honest User-Agent identification
- Comprehensive audit logging
"""

from .scrapers import MenuScraper, RobotsParser, DomainRateLimiter

__all__ = [
    'MenuScraper',
    'RobotsParser',
    'DomainRateLimiter',
]
