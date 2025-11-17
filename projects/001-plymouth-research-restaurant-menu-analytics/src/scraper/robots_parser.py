"""
Robots.txt Parser for Ethical Web Scraping
===========================================

CRITICAL: This module enforces Principle 3 (Ethical Web Scraping) - NON-NEGOTIABLE

Legal Compliance:
- UK Computer Misuse Act 1990: Respect robots.txt to avoid unauthorized access
- Website Terms of Service: robots.txt is part of implicit contract
- GDPR: Ethical data collection demonstrates accountability

Requirements:
- NFR-C-001: 100% robots.txt compliance
- Principle 3: Ethical web scraping is non-negotiable
- Goal G-3: Zero legal violations

Author: Plymouth Research Team
Date: 2025-11-17
License: Proprietary
"""

import logging
from typing import Optional, Tuple
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser
import requests

logger = logging.getLogger(__name__)


class RobotsParser:
    """
    Parse and enforce robots.txt rules for ethical web scraping.

    This class is the FIRST LINE OF DEFENSE against unethical scraping.
    ALL scraping requests MUST pass through this parser.

    Attributes:
        user_agent (str): Our honest User-Agent identifying Plymouth Research
        cache (dict): Cache of RobotFileParser instances per domain
    """

    def __init__(self, user_agent: str = "PlymouthResearchMenuScraper/1.0 (+https://plymouthresearch.uk)"):
        """
        Initialize robots.txt parser with honest User-Agent.

        Args:
            user_agent: Honest User-Agent string identifying Plymouth Research
                       with contact URL for website owners
        """
        self.user_agent = user_agent
        self.cache = {}  # Domain -> RobotFileParser
        logger.info(f"RobotsParser initialized with User-Agent: {self.user_agent}")

    def can_fetch(self, url: str) -> Tuple[bool, str]:
        """
        Check if URL can be fetched according to robots.txt.

        CRITICAL: This method MUST be called before EVERY HTTP request.
        Failure to check robots.txt violates Principle 3 (non-negotiable).

        Args:
            url: The URL to check (e.g., "https://restaurant.com/menu")

        Returns:
            Tuple of (allowed: bool, reason: str)
            - allowed: True if robots.txt allows scraping, False if blocked
            - reason: Human-readable explanation for logging

        Examples:
            >>> parser = RobotsParser()
            >>> allowed, reason = parser.can_fetch("https://example.com/menu")
            >>> if not allowed:
            >>>     logger.warning(f"Blocked by robots.txt: {reason}")
            >>>     return  # MUST NOT proceed
        """
        try:
            parsed_url = urlparse(url)
            domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
            robots_url = f"{domain}/robots.txt"

            # Get or create RobotFileParser for this domain
            if domain not in self.cache:
                logger.info(f"Fetching robots.txt from {robots_url}")
                rp = RobotFileParser()
                rp.set_url(robots_url)

                try:
                    # Fetch robots.txt with timeout
                    response = requests.get(robots_url, timeout=10)

                    if response.status_code == 200:
                        rp.parse(response.text.splitlines())
                        logger.info(f"✅ robots.txt parsed successfully for {domain}")
                    elif response.status_code == 404:
                        # No robots.txt = allow all (per spec)
                        logger.info(f"ℹ️  No robots.txt found for {domain} (404) - allowing all")
                        rp.allow_all = True
                    else:
                        # Other errors: assume restrictive (safe default)
                        logger.warning(f"⚠️  robots.txt fetch failed for {domain} (HTTP {response.status_code}) - assuming restrictive")
                        rp.disallow_all = True

                except requests.exceptions.RequestException as e:
                    # Network error: assume restrictive (safe default)
                    logger.error(f"❌ Network error fetching robots.txt from {domain}: {e} - assuming restrictive")
                    rp.disallow_all = True

                self.cache[domain] = rp

            # Check if URL is allowed
            rp = self.cache[domain]
            allowed = rp.can_fetch(self.user_agent, url)

            if allowed:
                reason = f"✅ robots.txt ALLOWS scraping {url}"
                logger.debug(reason)
            else:
                reason = f"🚫 robots.txt BLOCKS scraping {url}"
                logger.warning(reason)

            return allowed, reason

        except Exception as e:
            # Critical failure: default to DENY (safe)
            reason = f"❌ robots.txt check FAILED for {url}: {e} - DENYING by default"
            logger.error(reason)
            return False, reason

    def get_crawl_delay(self, url: str) -> Optional[float]:
        """
        Get crawl delay specified in robots.txt (if any).

        Some robots.txt files specify a "Crawl-delay" directive.
        We MUST respect this in addition to our 5-second rate limit.
        Use max(5 seconds, crawl_delay) as the actual delay.

        Args:
            url: The URL to check

        Returns:
            Crawl delay in seconds, or None if not specified

        Examples:
            >>> parser = RobotsParser()
            >>> delay = parser.get_crawl_delay("https://example.com/menu")
            >>> actual_delay = max(5.0, delay or 5.0)  # Use max of 5s and robots.txt delay
        """
        try:
            parsed_url = urlparse(url)
            domain = f"{parsed_url.scheme}://{parsed_url.netloc}"

            if domain not in self.cache:
                # Trigger cache population
                self.can_fetch(url)

            rp = self.cache.get(domain)
            if rp and hasattr(rp, 'crawl_delay'):
                delay = rp.crawl_delay(self.user_agent)
                if delay:
                    logger.info(f"⏱️  robots.txt specifies Crawl-delay: {delay} seconds for {domain}")
                    return float(delay)

            return None

        except Exception as e:
            logger.error(f"Error getting crawl delay for {url}: {e}")
            return None

    def clear_cache(self):
        """
        Clear robots.txt cache.

        Call this periodically (e.g., daily) to refresh robots.txt rules
        in case website owners update their robots.txt file.
        """
        self.cache.clear()
        logger.info("🗑️  robots.txt cache cleared")


# ============================================================================
# Helper Functions
# ============================================================================

def validate_user_agent(user_agent: str) -> bool:
    """
    Validate that User-Agent string is honest and identifiable.

    Ethical Scraping Principle: User-Agent MUST identify Plymouth Research
    and provide contact information for website owners.

    Args:
        user_agent: User-Agent string to validate

    Returns:
        True if valid, False if deceptive/invalid

    Examples:
        >>> validate_user_agent("PlymouthResearchMenuScraper/1.0 (+https://plymouthresearch.uk)")
        True
        >>> validate_user_agent("Mozilla/5.0 (fake browser)")
        False
    """
    # Must contain identifying information
    required_keywords = ["plymouth", "research", "menu"]
    user_agent_lower = user_agent.lower()

    if not any(keyword in user_agent_lower for keyword in required_keywords):
        logger.error(f"❌ User-Agent is deceptive (missing identifying keywords): {user_agent}")
        return False

    # Should contain contact URL
    if "http" not in user_agent_lower:
        logger.warning(f"⚠️  User-Agent lacks contact URL: {user_agent}")

    return True


# ============================================================================
# Usage Example
# ============================================================================

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Initialize parser
    parser = RobotsParser()

    # Test URLs
    test_urls = [
        "https://example.com/menu",
        "https://example.com/admin",  # Often blocked
        "https://httpbin.org/html",
    ]

    print("\n" + "="*80)
    print("Robots.txt Parser - Test Run")
    print("="*80 + "\n")

    for url in test_urls:
        allowed, reason = parser.can_fetch(url)
        delay = parser.get_crawl_delay(url)

        print(f"URL: {url}")
        print(f"  Allowed: {'✅ YES' if allowed else '🚫 NO'}")
        print(f"  Reason: {reason}")
        if delay:
            print(f"  Crawl Delay: {delay} seconds")
        print()
