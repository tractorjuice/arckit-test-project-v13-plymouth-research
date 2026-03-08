# Vendor Profile: Scrapy

> **Template Origin**: Official | **ArcKit Version**: 4.0.1

## Document Control

| Field | Value |
|-------|-------|
| **Document ID** | scrapy-profile |
| **Document Type** | Vendor Profile |
| **Project** | Plymouth Research Restaurant Menu Analytics (Project 001) |
| **Classification** | PUBLIC |
| **Status** | PUBLISHED |
| **Version** | 1.2 |
| **Created Date** | 2026-02-20 |
| **Last Modified** | 2026-03-08 |
| **Review Cycle** | On-Demand |
| **Next Review Date** | 2027-03-08 |
| **Owner** | Lead Developer |
| **Reviewed By** | PENDING |
| **Approved By** | PENDING |
| **Distribution** | Development Team |
| **Source Research** | ARC-001-RSCH-v1.0, ARC-001-RSCH-v2.0, ARC-001-RSCH-v2.1 |
| **Confidence** | High |

## Revision History

| Version | Date | Author | Changes | Approved By | Approval Date |
|---------|------|--------|---------|-------------|---------------|
| 1.0 | 2026-02-20 | AI Agent | Initial creation from `/arckit:research` command. | PENDING | PENDING |
| 1.1 | 2026-03-08 | AI Agent | Updated and validated against `ARC-001-RSCH-v2.0`. Emphasized compliance benefits. | PENDING | PENDING |
| 1.2 | 2026-03-08 | AI Agent | Refreshed against `ARC-001-RSCH-v2.1`. Reconfirmed Scrapy as the preferred collection framework for compliance-sensitive workloads. | PENDING | PENDING |

---

## Overview

Scrapy is an open-source, high-performance web crawling and scraping framework for Python. It provides a complete, asynchronous framework for writing "spiders" (scrapers), handling concurrency, managing requests, and processing extracted data through configurable pipelines. It is the industry standard for large-scale and production Python web scraping, maintained primarily by Zyte (formerly Scrapinghub) and the community.

## Products and Services

- **Scrapy OSS**: The full web scraping framework (BSD-3 licence).
- **scrapy-playwright plugin**: A plugin for rendering JavaScript-heavy pages.
- **Zyte API / Scrapy Cloud**: Commercial managed services offered by Scrapy's primary maintainer, Zyte. These are separate, paid products.

For this project, only the Scrapy Open Source Software (OSS) is relevant.

## Pricing Model

| Tier | Price | Notes |
|------|-------|-------|
| Scrapy OSS | Free (BSD-3) | Full framework with no limitations. |
| scrapy-playwright | Free (MIT) | Plugin for JavaScript rendering. |
| Zyte API / Scrapy Cloud | From $25/month | Managed services, not required for this project. |

*The recommended use of Scrapy for this project is zero-cost.*

## GitHub Statistics

- **Stars**: 59,800+
- **Licence**: BSD-3-Clause
- **Contributors**: 594+
- **Status**: Actively maintained.
- **URL**: https://github.com/scrapy/scrapy

## Key Features

- **Built-in Ethical Scraping**: Provides framework-level enforcement of `robots.txt` rules and automatic rate limiting (`AutoThrottle`).
- **Asynchronous**: Built on Twisted, it handles thousands of concurrent requests efficiently.
- **Middleware Architecture**: Extensible pipeline for handling requests, responses, and items.
- **JavaScript Rendering**: Can integrate with Playwright or Selenium to scrape dynamic, client-side rendered websites.
- **Data Pipelines**: Process and store scraped data cleanly (e.g., validate, deduplicate, write to SQLite).

## UK Government Presence

Not applicable. Scrapy is an open-source library, not a hosted service.

## Strengths

- **Production-Grade**: Battle-tested and used by major organizations at massive scale.
- **Compliance Focused**: Its built-in support for `robots.txt` and rate limiting is the most effective way to mitigate the project's critical compliance risks (R-001, R-004) and meet non-negotiable ethical requirements (NFR-C-003).
- **Performance**: Asynchronous architecture is significantly faster than sequential requests for large jobs.
- **Extensibility**: The middleware and pipeline system is highly customizable.
- **Community**: Has the largest and most active community of all Python scraping frameworks.

## Weaknesses

- Steeper learning curve compared to simple libraries like BeautifulSoup.
- The framework adds some boilerplate/overhead for very small, one-off tasks.
- Asynchronous nature can make debugging more complex for developers new to the paradigm.

## Compliance Relevance

Scrapy is critical for mitigating compliance risks in Project 001:
- **`ROBOTSTXT_OBEY = True`**: A simple setting in Scrapy enforces `robots.txt` rules at the framework level, which is far more robust than manual checks.
- **`AUTOTHROTTLE_ENABLED = True`**: Automatically adjusts scraping speed based on server load, ensuring the scraper is not aggressive.
- **`DOWNLOAD_DELAY`**: A fallback setting to enforce a fixed delay between requests.
- **`USER_AGENT`**: Easily configurable to provide a transparent and honest user agent.

## Competitive Alternatives

| Alternative | Price | Key Difference |
|-------------|-------|----------------|
| BeautifulSoup4 + Requests | Free | Simpler for static sites, but requires manual implementation of all compliance features. |
| Playwright (standalone) | Free | Excellent for JS-heavy sites, but lacks the scraping framework features of Scrapy (e.g., pipelines, automatic rate-limiting). |
| Apify / Bright Data | $49+/month | Managed services that are powerful but far exceed the project's budget. |

## Projects Referenced In

- **Project 001 — Plymouth Research Restaurant Menu Analytics** (Evaluated in `ARC-001-RSCH-v1.0` and `ARC-001-RSCH-v2.0`)

## Decision Notes

**Recommended**: While the current implementation uses BeautifulSoup, it is strongly recommended to **adopt Scrapy** for all new scraping tasks and to progressively migrate existing scrapers. Scrapy's built-in support for ethical scraping rules is the single most effective technical control for the project's highest-rated compliance risks. It provides a robust, framework-level guarantee of compliance that manual implementations cannot match.
