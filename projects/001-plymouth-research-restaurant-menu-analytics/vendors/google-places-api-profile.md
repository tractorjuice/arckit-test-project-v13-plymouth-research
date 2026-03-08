# Vendor Profile: Google Places API

| Field | Value |
|-------|-------|
| **Vendor Name** | Google (Alphabet Inc.) |
| **Category** | Geocoding / Location Data / Business Data API |
| **Website** | https://developers.google.com/maps/documentation/places |
| **Confidence** | High |
| **Last Researched** | 2026-03-08 |
| **Projects Referenced In** | Project 001 — Plymouth Research Restaurant Menu Analytics |

## Overview

Google Places API is a web service providing location information, business details, reviews, and service options for places worldwide. It is part of Google Maps Platform. In 2024–2025, Google launched "Places API (New)" as a successor to the legacy Places API, with improved data coverage, different pricing tiers, and updated billing models effective March 1, 2025.

## Products and Services

- **Places API (New)**: Current version with enhanced features, Essentials/Pro/Enterprise field tiers
- **Places API (Legacy)**: Deprecated, still operational but no new features
- **Nearby Search (New)**: Search places near a location
- **Text Search (New)**: Search places by text query
- **Place Details (New)**: Detailed information about a specific place

## Pricing Model (Effective March 2025)

Google replaced the $200/month recurring credit with per-SKU free monthly thresholds.

### Free Tiers (per SKU per month)
| SKU Level | Free Calls/Month |
|-----------|-----------------|
| Essentials | 10,000 |
| Pro | 5,000 |
| Enterprise | 1,000 |

### Place Details (New) Pricing
| Field Set | Free Threshold | Price per 1,000 (0–100K) |
|-----------|---------------|--------------------------|
| Essentials (IDs, names, addresses) | 10,000/month | $5.00 |
| Pro (hours, phone, service options) | 5,000/month | $17.00 |
| Enterprise (reviews, photos) | 1,000/month | $20.00 |

### Plymouth Research Usage Estimate
- Current: 243 restaurants × 1 request/month = 243 requests (Pro level fields)
- Within 5,000/month Pro free threshold: **£0/month**
- Phase 2 (1,500 restaurants × 1 request/month): 1,500 requests — still within 5,000 free threshold
- Phase 2 (1,500 restaurants × weekly refresh): 6,000 requests — slightly over Pro free threshold ($17/1,000 for excess 1,000 = $0.017 ≈ £0.013/month)

*Pricing verified February 2026 from https://developers.google.com/maps/billing-and-pricing/pricing*

## Key Features

- Place Details: name, address, phone, website, business hours, service options, price level
- Service options: dine_in, takeout, delivery, reservations (used in FR-007)
- Business status: OPERATIONAL, CLOSED_TEMPORARILY, CLOSED_PERMANENTLY
- Google rating and total review count
- Up to 5 reviews per place (via reviews field)
- GPS coordinates (latitude, longitude)
- Formatted address and Google Maps URL

## UK Government Presence

Not applicable — global commercial API. No G-Cloud listing or Crown Commercial Service agreement identified.

## Strengths

- Comprehensive business data (service options, hours, ratings)
- Highly accurate location data for UK businesses
- Free tier sufficient for Plymouth Research Phase 1 and Phase 2 usage
- Reliable uptime (Google SLA)
- Well-documented API with Python client library

## Weaknesses

- Google changed pricing model in March 2025 — requires migration from legacy to new Places API
- Enterprise-level fields (reviews) have lower free threshold (1,000/month)
- No UK data residency guarantee (US-hosted)
- Terms of service prohibit caching beyond stated limits
- Review data limited to 5 reviews per place in API response

## Compliance

- Terms of Service: attribute with "Powered by Google" text and Google Maps logo
- Data retention: Google ToS limits caching to 30 days for some data types
- No PII concerns: public business data only
- Plymouth Research current attribution: "Data from Google Places" — review and update to comply with new ToS

## Competitive Alternatives

| Alternative | Free Tier | Key Difference |
|-------------|-----------|----------------|
| OpenCage Geocoder | 2,500/day free | Geocoding only, no service options data |
| OpenStreetMap / Nominatim | Free | Community data, less accurate for businesses |
| HERE Maps | Free tier available | Competitive but less UK business data |
| TomTom Places | Free tier | Good location data, not as rich as Google |
| Ordnance Survey API | Free (25K/month for PSGA) | UK-authoritative addresses, no business hours |

## Decision Notes

**Recommended**: Retain Google Places API and migrate from legacy Places API to Places API (New) to ensure compatibility with the March 2025 pricing model and access to the current free usage caps. Current usage (243 requests/month) remains comfortably within the free monthly allowances relevant to Project 001.

**Action required**: Update `fetch_google_reviews.py` to use Places API (New) endpoints and field masks.

**Updated 2026-03-08**: Revalidated during `ARC-001-RSCH-v2.1`; no change to the recommendation.
