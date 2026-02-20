# Vendor Profile: Scrapy

| Field | Value |
|-------|-------|
| **Vendor Name** | Scrapy Project (maintained by Zyte) |
| **Category** | Web Scraping Framework |
| **Website** | https://scrapy.org |
| **Confidence** | High |
| **Last Researched** | 2026-02-20 |
| **Projects Referenced In** | Project 001 — Plymouth Research Restaurant Menu Analytics |

## Overview

Scrapy is an open-source, high-performance web crawling and scraping framework for Python. It provides a complete framework for writing spiders (scrapers), handling concurrency, managing requests, and processing extracted data through configurable pipelines. It is the industry standard for large-scale Python web scraping. Maintained primarily by Zyte (formerly Scrapinghub) and a wide community.

## Products and Services

- **Scrapy OSS**: Full web scraping framework (BSD-3 licence)
- **scrapy-playwright plugin**: JavaScript rendering via Playwright (https://github.com/scrapy-plugins/scrapy-playwright)
- **Zyte API**: Commercial managed scraping service by same maintainer (paid, separate product)
- **Scrapy Cloud**: Zyte's hosted scraping platform (paid, separate product)

Note: Scrapy OSS is the relevant component for Plymouth Research. Zyte's paid services are separate.

## Pricing Model

| Tier | Price | Notes |
|------|-------|-------|
| Scrapy OSS | Free (BSD-3) | Full framework, no limitations |
| scrapy-playwright | Free (MIT) | Playwright integration plugin |
| Zyte API | From $25/month | Managed scraping — not required |
| Scrapy Cloud | From $29/month | Hosted execution — not required |

*Plymouth Research recommendation: OSS only, zero cost.*

## GitHub Statistics

- **Stars**: 59,800+
- **Licence**: BSD-3-Clause
- **Contributors**: 594
- **Status**: Actively maintained (Zyte + community)
- **URL**: https://github.com/scrapy/scrapy
- **Python requirement**: Python 3.10+

## Key Features

- **robots.txt middleware**: Built-in `RobotsTxtMiddleware` enforces disallow rules automatically
- **AutoThrottle**: Automatic rate limiting based on server response times
- **Custom User-Agent**: Per-spider User-Agent configuration
- **Concurrent requests**: Configurable parallel requests with delay
- **Download handlers**: Extensible for HTTP, HTTPS, FTP
- **Item pipelines**: Process scraped data (validate, deduplicate, store to SQLite/CSV/JSON)
- **Spider middleware**: Custom request/response processing
- **scrapy-playwright**: Drop-in JavaScript rendering via Playwright for dynamic sites
- **Telnet console**: Real-time debugging and monitoring

## UK Government Presence

Not applicable — OSS library. No hosted component.

## Strengths

- Production-grade: used by enterprise organisations at massive scale
- Built-in ethical scraping: robots.txt middleware is framework-level (not manual)
- AutoThrottle enforces rate limiting without manual `time.sleep()` calls
- 59,800+ stars — largest web scraping framework community
- scrapy-playwright enables JS rendering without changing scraping logic
- Configurable retry logic, redirect handling, deduplication middleware
- BSD-3 licence: permissive for commercial use

## Weaknesses

- Steeper learning curve than BeautifulSoup + Requests (spiders, middlewares, pipelines paradigm)
- Framework overhead for simple, one-off scraping tasks
- Async architecture (Twisted-based) can complicate debugging
- scrapy-playwright adds ~150 MB browser download per environment

## Compliance Relevance

Critical for Plymouth Research:
- **RobotsTxtMiddleware**: Set `ROBOTSTXT_OBEY = True` — enforces NFR-C-003 at framework level, reducing R-004 (robots.txt violation) risk
- **AutoThrottle**: Enforces 5-second minimum delay (NFR-C-003) automatically
- **DOWNLOAD_DELAY**: Fallback fixed delay configuration
- **User-Agent**: `USER_AGENT = 'PlymouthResearchBot/1.0 (+https://plymouthresearch.co.uk/about)'`
- Audit trail via Scrapy stats exporter (supports DR-007 scraping audit log)

## Competitive Alternatives

| Alternative | Price | Key Difference |
|-------------|-------|----------------|
| BeautifulSoup4 + Requests | Free (MIT) | Simpler, manual rate limiting, no built-in robots.txt |
| Playwright Python | Free (Apache-2.0) | JS-native, but slower, more memory, manual rate limiting |
| Mechanize | Free (BSD) | Older, no JS support, limited maintenance |
| Apify | $49–$499/month | Managed service, exceeds £100/month budget |

## Decision Notes

**Recommended**: Adopt Scrapy for Phase 2 scale (500+ restaurants). Continue with BeautifulSoup4 + Requests for current Phase 1 (150 restaurants). When transitioning to Scrapy, the RobotsTxtMiddleware and AutoThrottle provide the strongest available enforcement of NFR-C-003 (ethical scraping — NON-NEGOTIABLE) and reduce R-004 risk from Medium to Low.
