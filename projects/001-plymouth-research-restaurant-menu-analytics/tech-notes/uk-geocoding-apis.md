# Tech Note: UK Geocoding and Geography APIs

| Field | Value |
|-------|-------|
| **Topic** | UK Geocoding, Postcode Lookup, and Geographic Enrichment APIs |
| **Category** | Geographic Data / APIs |
| **Last Updated** | 2026-03-08 |
| **Relevance to Projects** | Project 001 — Plymouth Research Restaurant Menu Analytics |

## Summary

UK geocoding and geography enrichment is well served by free, authoritative government open data sources. The ONS Postcode Directory, Postcodes.io, and Google Places API together cover all geographic enrichment needs for Plymouth Research at zero cost. Google Places API pricing changed significantly in March 2025 — migration from legacy API to Places API (New) is required.

## Key Findings

1. **ONS Postcode Directory**: Official ONS quarterly release. Maps all 2.5 million UK postcodes to ward, LSOA, MSOA, parliamentary constituency, IMD deprivation data. OGL v3.0. Free bulk CSV download from https://geoportal.statistics.gov.uk. The authoritative source for UK geographic enrichment.

2. **Postcodes.io**: Free open-source REST API (MIT, 1,400+ GitHub stars) serving ONS data. No API key required. Bulk endpoint for 100 postcodes per request. Self-hostable via Docker. v18.0.1 released February 2026 — actively maintained. Ideal for on-demand geocoding validation (INT-006).

3. **Google Places API pricing change (March 2025)**: Google replaced the $200/month recurring credit with per-SKU free thresholds. Place Details Pro (which includes service options and business hours) now has 5,000 free requests/month. Plymouth Research usage: 243 requests/month (Phase 1) and ~1,500 requests/month (Phase 2, weekly refresh) — both within the 5,000 free threshold. No cost change expected.

4. **Places API (New) migration**: Google designated the legacy Places API as "Legacy" in 2025. Migration to Places API (New) provides better free tier (10K Essentials, 5K Pro/month), improved data quality, and better volume discounts. Required for long-term API stability.

5. **Ordnance Survey APIs**: OS Places API provides authoritative UK addresses. Free for PSGA (Public Sector Geospatial Agreement) members (25K transactions/month). Commercial: £100/month. Not cost-effective compared to Postcodes.io for Plymouth Research's use case (postcode-to-geography mapping only).

6. **OpenCage Geocoder**: Alternative to Google Places for address geocoding. 2,500 free requests/day. €50/month for Small plan. Provides global geocoding but lacks the business-specific data (service options, opening hours, reviews) provided by Google Places.

## UK Geography Data Hierarchy

For Plymouth Research restaurant enrichment:
```
UK → England → South West → Devon → Plymouth
├── Ward (e.g., "Drake", "Ham")
├── LSOA (Lower Super Output Area, ~1,500 people)
├── MSOA (Middle Super Output Area, ~7,500 people)
├── Parliamentary Constituency (e.g., "Plymouth Sutton and Devonport")
└── IMD Decile (1=most deprived, 10=least deprived)
```

## API Comparison for Plymouth Research

| API | Use Case | Auth | Cost | Data |
|-----|----------|------|------|------|
| Postcodes.io | Postcode → ward, LSOA, IMD | None | Free | ONS |
| ONS Postcode Directory | Bulk batch enrichment | None | Free | ONS |
| Google Places (New) | Business data, service options | API key | Free (within tier) | Google |
| OS Places API | Authoritative UK addresses | API key | Free (PSGA) / £100/mo | OS |
| OpenCage | Generic geocoding | API key | 2,500/day free | Multiple |

## Implementation Pattern for Plymouth Research

```python
# Postcodes.io — batch enrichment of 100 restaurants per request
import requests

postcodes = ["PL1 2NQ", "PL4 8AA", "PL1 1AE"]  # Up to 100

response = requests.post(
    "https://api.postcodes.io/postcodes",
    json={"postcodes": postcodes}
)

for result in response.json()["result"]:
    if result["result"]:
        data = result["result"]
        ward = data["admin_ward"]
        lsoa = data["lsoa"]
        constituency = data["parliamentary_constituency"]
        imd_decile = data["codes"]["admin_ward"]  # via supplementary lookup
```

## Compliance Notes

- ONS data: OGL v3.0 — attribution required: "Contains OS data © Crown copyright and database right"
- Google Places: "Powered by Google" attribution required; data caching limited by ToS
- Postcodes.io: MIT licence — no specific attribution requirements

## Relevance to Projects

**Project 001**: Implements INT-005 (ONS Postcode Directory), INT-006 (Postcodes.io), FR-011 (ONS geography enrichment), BR-008 (geographic intelligence). All implemented as of commit e08ca94. The v2.1 research reconfirms that this mixed model remains the best economic fit and still requires Google Places API migration to the newer endpoints.

## References

- ONS Postcode Directory: https://geoportal.statistics.gov.uk/
- Postcodes.io: https://postcodes.io/ and https://github.com/ideal-postcodes/postcodes.io
- Google Places API (New): https://developers.google.com/maps/documentation/places/web-service
- Google Maps billing (March 2025): https://developers.google.com/maps/billing-and-pricing/march-2025
