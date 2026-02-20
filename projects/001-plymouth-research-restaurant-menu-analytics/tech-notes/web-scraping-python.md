# Tech Note: Web Scraping in Python

| Field | Value |
|-------|-------|
| **Topic** | Python Web Scraping: Frameworks, Ethics, and Tools |
| **Category** | Data Collection / Web Scraping |
| **Last Updated** | 2026-02-20 |
| **Relevance to Projects** | Project 001 — Plymouth Research Restaurant Menu Analytics |

## Summary

Python web scraping involves programmatically extracting data from websites. The three primary tools are BeautifulSoup4 (HTML parsing), Scrapy (full scraping framework), and Playwright (browser automation for JavaScript-heavy sites). For ethical research scraping, enforcing robots.txt compliance and rate limiting is critical — both are non-negotiable for Plymouth Research (Principle #3, NFR-C-003).

## Key Findings

1. **BeautifulSoup4 + Requests**: Best for simple, static HTML sites. Requests (~52,900 GitHub stars) handles HTTP; BeautifulSoup parses HTML. No built-in rate limiting or robots.txt handling — must be implemented manually. Ideal for 1–50 restaurant scraping tasks.

2. **Scrapy**: Production-grade framework (BSD-3, 59,800+ GitHub stars, 594 contributors, maintained by Zyte). Built-in `RobotsTxtMiddleware` (set `ROBOTSTXT_OBEY = True`), AutoThrottle for automatic rate limiting, configurable User-Agent, SQLite/CSV export pipelines. Best for 50+ restaurant scale.

3. **Playwright (Python)**: Browser automation by Microsoft (Apache-2.0, 14,200 GitHub stars). Handles JavaScript-rendered menus (React/Angular/Vue). Slower than HTTP-only scrapers (~150 MB browser download). Rate limiting must be implemented manually (`asyncio.sleep()`). Integration with Scrapy via `scrapy-playwright` plugin.

4. **Scrapy + scrapy-playwright hybrid**: Industry best practice for mixed static/dynamic sites. Scrapy handles static pages; Playwright handles JS-heavy pages within same scraping pipeline. Maintains Scrapy's robots.txt and AutoThrottle enforcement.

5. **Managed scraping services** (Apify, Bright Data): Enterprise pricing ($49–$499+/month) far exceeds Plymouth Research £100/month budget. Not viable for this project.

6. **68% of production scraping implementations** use at least two tools, choosing based on target site characteristics.

## Ethical Scraping Requirements (Plymouth Research)

Critical constraints (NON-NEGOTIABLE per Principle #3):

| Requirement | Implementation | Tool Support |
|-------------|----------------|-------------|
| Robots.txt compliance | Parse before any request | Scrapy: `ROBOTSTXT_OBEY = True`; BS4: `urllib.robotparser` |
| Rate limiting (5s minimum) | Delay between requests per domain | Scrapy AutoThrottle; manual `time.sleep(5)` for BS4 |
| Honest User-Agent | Identify bot with contact info | Scrapy: `USER_AGENT` setting; Requests: `headers` |
| Scraping audit trail | Log all requests | Scrapy stats; DR-007 scraping_audit_log table |

## Relevance to Projects

**Project 001**: BeautifulSoup4 + Requests currently used for menu scraping, Trustpilot scraping, Plymouth licensing scraper. Migration to Scrapy recommended for Phase 2 (500+ restaurants) to provide framework-level robots.txt and rate limiting enforcement.

## Related Technologies

- `urllib.robotparser`: Python stdlib robots.txt parser
- `httpx`: Modern async HTTP client (Apache-2.0) — alternative to Requests with HTTP/2 support
- `lxml`: Fast HTML/XML parser (BSD-3) — backend for BeautifulSoup
- `parsel`: CSS/XPath selector library used by Scrapy

## References

- Scrapy: https://github.com/scrapy/scrapy
- Playwright Python: https://github.com/microsoft/playwright-python
- scrapy-playwright: https://github.com/scrapy-plugins/scrapy-playwright
- BeautifulSoup comparison: https://www.firecrawl.dev/blog/beautifulsoup4-vs-scrapy-comparison
