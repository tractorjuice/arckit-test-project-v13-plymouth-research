"""
Rate Limiter for Ethical Web Scraping
======================================

CRITICAL: Enforces 5-second minimum delay between requests to same domain

Requirements:
- NFR-C-003: Rate limiting (5 seconds per domain minimum)
- Principle 3: Ethical web scraping (rate limits respect server capacity)
- Goal G-3: Zero legal violations

Author: Plymouth Research Team
Date: 2025-11-17
"""

import logging
import time
from collections import defaultdict
from threading import Lock
from typing import Dict
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class DomainRateLimiter:
    """
    Per-domain rate limiter enforcing minimum delays between requests.

    This ensures we don't burden restaurant servers with rapid requests.
    Principle 3 requires MINIMUM 5 seconds per domain, but can be longer
    if robots.txt specifies a Crawl-delay.

    Thread-safe for concurrent scraping.
    """

    def __init__(self, min_delay_seconds: float = 5.0):
        """
        Initialize rate limiter with minimum delay.

        Args:
            min_delay_seconds: Minimum seconds between requests to same domain
                              (default 5.0 per Principle 3)
        """
        self.min_delay_seconds = min_delay_seconds
        self.last_request_time: Dict[str, float] = defaultdict(float)
        self.lock = Lock()  # Thread-safe access to last_request_time
        logger.info(f"RateLimiter initialized with {min_delay_seconds}s minimum delay per domain")

    def wait_if_needed(self, url: str, crawl_delay: float = None) -> float:
        """
        Wait if needed to respect rate limits, then record this request.

        CRITICAL: Call this BEFORE every HTTP request to a restaurant website.

        Args:
            url: The URL being requested
            crawl_delay: Optional crawl delay from robots.txt (if specified)

        Returns:
            Actual delay waited in seconds (for logging)

        Examples:
            >>> limiter = DomainRateLimiter(min_delay_seconds=5.0)
            >>> actual_delay = limiter.wait_if_needed("https://restaurant.com/menu")
            >>> # Makes HTTP request after delay
            >>> logger.info(f"Waited {actual_delay:.2f} seconds before request")
        """
        domain = self._extract_domain(url)

        with self.lock:
            current_time = time.time()
            last_time = self.last_request_time[domain]

            # Determine required delay (max of min_delay and crawl_delay)
            required_delay = self.min_delay_seconds
            if crawl_delay and crawl_delay > required_delay:
                required_delay = crawl_delay
                logger.info(f"⏱️  Using crawl_delay {crawl_delay}s for {domain} (> min {self.min_delay_seconds}s)")

            # Calculate elapsed time since last request to this domain
            elapsed = current_time - last_time

            if elapsed < required_delay:
                # Need to wait
                wait_time = required_delay - elapsed
                logger.info(f"⏸️  Rate limiting: waiting {wait_time:.2f}s before requesting {domain}")
                time.sleep(wait_time)
                actual_delay = wait_time
            else:
                # Enough time has passed, no wait needed
                actual_delay = 0.0
                logger.debug(f"✅ Rate limit OK: {elapsed:.2f}s elapsed since last request to {domain}")

            # Record this request time
            self.last_request_time[domain] = time.time()

            return actual_delay

    def _extract_domain(self, url: str) -> str:
        """
        Extract domain from URL for rate limiting key.

        Args:
            url: Full URL

        Returns:
            Domain (scheme://netloc) for rate limiting

        Examples:
            >>> limiter._extract_domain("https://restaurant.com/menu")
            'https://restaurant.com'
        """
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"

    def reset(self):
        """
        Reset all rate limit timers.

        Useful for testing or when restarting scraper.
        """
        with self.lock:
            self.last_request_time.clear()
            logger.info("🗑️  Rate limiter reset - all timers cleared")

    def get_stats(self) -> Dict[str, any]:
        """
        Get rate limiter statistics for monitoring.

        Returns:
            Dictionary with stats:
            - domains_tracked: Number of domains with rate limit state
            - min_delay_seconds: Configured minimum delay
            - last_request_times: Dict of domain -> last request timestamp
        """
        with self.lock:
            return {
                "domains_tracked": len(self.last_request_time),
                "min_delay_seconds": self.min_delay_seconds,
                "last_request_times": dict(self.last_request_time)
            }


# ============================================================================
# Usage Example
# ============================================================================

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # Initialize rate limiter
    limiter = DomainRateLimiter(min_delay_seconds=5.0)

    # Simulate scraping requests
    test_urls = [
        "https://restaurant1.com/menu",
        "https://restaurant2.com/menu",  # Different domain, no delay needed
        "https://restaurant1.com/about",  # Same domain as first, should delay 5s
    ]

    print("\n" + "="*80)
    print("Rate Limiter - Test Run")
    print("="*80 + "\n")

    for i, url in enumerate(test_urls, 1):
        print(f"Request {i}: {url}")
        start_time = time.time()

        delay_waited = limiter.wait_if_needed(url)

        elapsed = time.time() - start_time
        print(f"  Waited: {delay_waited:.2f}s")
        print(f"  Total elapsed: {elapsed:.2f}s")
        print()

    # Show stats
    print("\nRate Limiter Stats:")
    stats = limiter.get_stats()
    print(f"  Domains tracked: {stats['domains_tracked']}")
    print(f"  Min delay: {stats['min_delay_seconds']}s")
