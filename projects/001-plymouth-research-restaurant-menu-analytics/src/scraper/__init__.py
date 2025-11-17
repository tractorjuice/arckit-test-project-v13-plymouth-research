"""
Plymouth Research Menu Scraper Package
========================================

Ethical web scraping with robots.txt compliance and rate limiting.

Modules:
- robots_parser: Robots.txt compliance checking
- rate_limiter: Per-domain rate limiting (5 seconds minimum)
- menu_scraper: Main scraper orchestration

Author: Plymouth Research Team
Date: 2025-11-17
"""

from .robots_parser import RobotsParser, validate_user_agent
from .rate_limiter import DomainRateLimiter
from .menu_scraper import MenuScraper

__all__ = [
    "RobotsParser",
    "DomainRateLimiter",
    "MenuScraper",
    "validate_user_agent",
]

__version__ = "1.0.0"
