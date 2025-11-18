# Plymouth Research - Web Scraping Results

## Summary

Successfully scraped real menu data from 129 Plymouth restaurants using Firecrawl API with a two-phase restartable architecture. Data quality validated and corrected to remove erroneous third-party aggregator data.

## Final Database Statistics (Corrected)

**Total Data:**
- **219 restaurants** in database
- **3,577 menu items** total (after data quality corrections)

**Real Scraped Data:**
- **129 restaurants** (59%) with real menu data from actual websites
- **3,061 menu items** extracted from live websites
- **Success rate**: 59% of target restaurants successfully scraped

**Synthetic/Placeholder Data:**
- **85 restaurants** (41%) with placeholder data
  - Failed scraping attempts (DNS errors, blocked sites, no structured data)
  - Restaurants without accessible menus
- **5 restaurants** marked as scraped but with 0 items (extraction failures)

**Data Quality Corrections:**
- **Changs Chinese Restaurant**: Removed 984 incorrect items (scraped TripAdvisor aggregator instead of restaurant site)
- **Sutton Snax**: Removed 22 incorrect items (scraped TripAdvisor aggregator instead of restaurant site)
- **Total removed**: 1,006 erroneous items from aggregator contamination
- **Lesson**: Importance of URL validation and aggregator filtering in production scraping

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

## Dashboard Visualization Improvements

**Problem**: Restaurants with unusually high menu item counts (e.g., Revolution Plymouth with 167 items) were distorting visualizations, making it difficult to compare typical restaurants.

**Solution Implemented**:

1. **Outlier Detection** (IQR Method):
   - Calculates Q1, Q3, and Interquartile Range (IQR)
   - Identifies outliers as restaurants with > Q3 + 1.5×IQR items
   - Displays outlier count and threshold in dashboard

2. **Statistical Metrics**:
   - Shows median (robust against outliers), min, max menu item counts
   - Median provides better central tendency than mean for skewed data

3. **Visualization Options**:
   - **Logarithmic scale toggle**: For datasets with extreme outliers
   - **Exclude outliers toggle**: Hides outliers to focus on typical restaurants
   - **Percentage view**: Shows category distribution as percentages (0-100%) instead of absolute counts
   - **Color coding**: Outliers shown in red (#FF6B6B), typical restaurants in teal (#4ECDC4)

4. **Reference Lines**:
   - Green dashed line shows median value across all restaurants
   - Helps identify restaurants above/below typical menu size

5. **Outlier Details**:
   - Expandable section lists all outlier restaurants with item counts
   - Transparency about which data points are excluded

**Impact**:
- Better comparison of typical restaurants
- Clear identification of unusual data patterns
- Flexible visualization for different analysis needs
- User control over data presentation

## Files

- `phase1_discover_menus.py` - Menu URL discovery script
- `phase2_extract_menus.py` - Menu extraction script
- `restaurant_menu_urls.json` - Discovered menu URLs (gitignored)
- `restaurants_extracted.json` - Extracted menu data (gitignored)
- `plymouth_research.db` - SQLite database (gitignored)
- `import_from_json.py` - Import script for database
- `dashboard_app.py` - Streamlit dashboard with real data badges, outlier handling, and advanced visualizations

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
