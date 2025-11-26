"""
Web Scraping Components
=======================

Core scraping infrastructure with ethical compliance controls.
"""

from .menu_scraper import MenuScraper
from .robots_parser import RobotsParser
from .rate_limiter import DomainRateLimiter

__all__ = [
    'MenuScraper',
    'RobotsParser',
    'DomainRateLimiter',
]
