# Vendor Profile: Postcodes.io

| Field | Value |
|-------|-------|
| **Vendor Name** | Ideal Postcodes Ltd |
| **Category** | UK Geocoding / Postcode Lookup API |
| **Website** | https://postcodes.io |
| **Confidence** | High |
| **Last Researched** | 2026-02-20 |
| **Projects Referenced In** | Project 001 — Plymouth Research Restaurant Menu Analytics |

## Overview

Postcodes.io is a free, open-source UK postcode lookup API and geocoder. It regularly ingests and serves ONS Postcode Directory and Ordnance Survey Open Names datasets, making it the most comprehensive free UK geocoding resource available. No authentication is required. The project is maintained by Ideal Postcodes Ltd and released under the MIT licence.

## Products and Services

- **Public API**: Free REST API at https://api.postcodes.io — no API key required
- **Self-hosted**: Docker image available for deployment on own infrastructure
- **Batch endpoints**: Bulk lookup of up to 100 postcodes per request

## Pricing Model

| Tier | Price | Notes |
|------|-------|-------|
| Public API | Free | No rate limit stated; fair use expected |
| Self-hosted | Free (infra cost only) | Full control, no external dependency |

*No commercial pricing — fully open source and free to use.*

## GitHub Statistics

- **Stars**: 1,400+
- **Licence**: MIT
- **Last Release**: v18.0.1 (February 16, 2026) — actively maintained
- **URL**: https://github.com/ideal-postcodes/postcodes.io

## Data Coverage

Postcodes.io covers all UK postcodes mapped to:
- Ward name and code
- LSOA (Lower Super Output Area)
- MSOA (Middle Super Output Area)
- Parliamentary constituency
- County, district, admin area
- Latitude, longitude (WGS84)
- Index of Multiple Deprivation (IMD) decile and rank
- Country (England, Scotland, Wales, Northern Ireland)

Data is updated quarterly to align with ONS Postcode Directory release cycle.

## Key API Endpoints

- `GET /postcodes/{postcode}` — single postcode lookup
- `POST /postcodes` — bulk lookup (up to 100 postcodes)
- `GET /postcodes/{postcode}/validate` — validate postcode format
- `GET /postcodes/{postcode}/nearest` — find nearest postcodes
- `GET /outcodes/{outcode}` — outward code lookup (e.g., PL1)

## UK Government Presence

Postcodes.io serves ONS data under OGL v3.0. The underlying data (ONS Postcode Directory) is official UK Government open data. Postcodes.io is not a government service itself but an authoritative third-party wrapper around government data.

## Strengths

- Completely free, no API key, no rate limit issues
- Serves authoritative ONS data (same source as ONS Postcode Directory download)
- Covers all UK postcodes including Plymouth PL1–PL9
- IMD data enables deprivation-aware analysis (BR-008, FR-011)
- MIT licence: unrestricted use
- Bulk endpoint: enrich 100 restaurants per request
- Self-hostable via Docker for zero external dependencies
- Actively maintained (v18.0.1 released February 2026)

## Weaknesses

- No SLA for public API (fair use, community service)
- Rate limits not published (potential throttling at very high volume)
- Not a real-time API for newly created postcodes (quarterly updates)
- Relies on ONS data quality (generally excellent for UK)

## Compliance

- MIT licence: no restrictions
- Data: OGL v3.0 (same as ONS Postcode Directory)
- Attribution required: "Contains OS data © Crown copyright and database right"
- No PII involved (postcode-to-geography mapping only)

## Competitive Alternatives

| Alternative | Free Tier | Key Difference |
|-------------|-----------|----------------|
| Google Maps Geocoding API | 10,000/month free | Global coverage, richer data, API key required |
| OpenCage Geocoder | 2,500/day free | Global, structured address data |
| OS Places API | 25K/month for PSGA | Authoritative UK addresses, registration required |
| Mapcity | Paid | More features, UK-specific |

## Decision Notes

**Recommended**: Retain Postcodes.io as primary UK geocoding service for Plymouth Research Project 001. It directly implements INT-006 (Postcodes.io API requirement) and FR-011 (ONS geography enrichment) at zero cost. The self-hosted Docker option provides resilience if the public API becomes unavailable. No action required — already implemented.
