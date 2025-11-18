# Plymouth Research - Web Scraping Results

## Summary

Successfully scraped real menu data from 135 Plymouth restaurants using Firecrawl API with a two-phase restartable architecture.

## Final Database Statistics

**Total Data:**
- **219 restaurants** in database
- **4,583 menu items** total

**Real Scraped Data:**
- **135 restaurants** (62%) with real menu data from actual websites
- **4,045 menu items** extracted from live websites
- **Success rate**: 62% of target restaurants successfully scraped

**Synthetic/Placeholder Data:**
- **84 restaurants** (38%) with placeholder data
  - Failed scraping attempts (DNS errors, blocked sites, no structured data)
  - Restaurants without accessible menus

## Scraping Architecture

### Two-Phase Approach

**Phase 1: Menu URL Discovery**
- Processed: 211 restaurant URLs (including duplicates)
- Method: Firecrawl site mapping + common path testing
- Output: `restaurant_menu_urls.json`
- Features:
  - Intelligent menu page detection (HTML and PDF)
  - Common path testing (`/menu`, `/menus`, `/food`, `/menu.pdf`)
  - Checkpoint system (every 25 restaurants)
  - Fully restartable

**Phase 2: Menu Extraction**
- Processed: 211 discovered menu URLs
- Method: Firecrawl structured JSON extraction
- Output: `restaurants_extracted.json`
- Extracted data:
  - Menu item name, description, price (GBP)
  - Category (starters, mains, desserts, etc.)
  - Dietary tags (vegan, vegetarian, gluten-free)
  - Restaurant address and price range
- Features:
  - Checkpoint system (every 25 restaurants)
  - Fully restartable
  - Handles JavaScript-rendered pages and PDFs

## Top Restaurants by Menu Items

| Restaurant | Menu Items |
|-----------|------------|
| Revolution Plymouth | 167 items |
| McDonald's Plymouth | 121 items |
| Prezzo Plymouth | 109 items |
| Pret A Manger Plymouth | 104 items |
| The Village Restaurant | 98 items |
| Yukisan Ramen Bar | 94 items |
| Wildwood Plymouth | 92 items |
| Las Iguanas Plymouth | 88 items |
| Rockfish Plymouth | 65 items |
| Koishii Sushi Bar | 49 items |

## Scraping Technology

- **API**: Firecrawl (firecrawl.dev)
- **Language**: Python 3
- **Database**: SQLite
- **Rate Limiting**: Built into Firecrawl API
- **JavaScript Handling**: Automatic via Firecrawl
- **PDF Support**: Native Firecrawl PDF extraction

## Data Quality

**Successful Extractions:**
- Clean, structured JSON data
- Accurate price conversion (£ to GBP decimal)
- Proper categorization
- Dietary tag detection

**Common Failure Reasons:**
1. **DNS Errors** (35 restaurants): Domain no longer exists or unreachable
2. **No Structured Menu** (28 restaurants): Menu not in machine-readable format
3. **Blocked/Protected** (12 restaurants): Site blocking automated access
4. **Invalid URLs** (9 restaurants): Incorrect or outdated website URLs

## Compliance

- **robots.txt**: Respected via Firecrawl
- **Rate Limiting**: Managed by Firecrawl API
- **Data Usage**: Public menu information only
- **GDPR**: No personal data collected
- **Ethical**: Transformative use for analytics

## Files

- `phase1_discover_menus.py` - Menu URL discovery script
- `phase2_extract_menus.py` - Menu extraction script
- `restaurant_menu_urls.json` - Discovered menu URLs (gitignored)
- `restaurants_extracted.json` - Extracted menu data (gitignored)
- `plymouth_research.db` - SQLite database (gitignored)
- `import_from_json.py` - Import script for database
- `dashboard_app.py` - Streamlit dashboard with real data badges

## Next Steps

Potential improvements:
1. Re-scrape failed restaurants with fallback methods
2. Implement automated weekly refresh
3. Add menu change detection
4. Expand to more Plymouth restaurants
5. Add nutritional information extraction
6. Implement price tracking over time

---

Generated: 2025-11-18
Scraping Duration: Phase 1 (50 minutes) + Phase 2 (70 minutes) = ~2 hours total
