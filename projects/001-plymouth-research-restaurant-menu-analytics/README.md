# Plymouth Research Restaurant Menu Analytics

**Project ID:** 001
**Status:** Operational
**Created:** 2025-11-15
**Last Updated:** 2025-11-18

## Overview

Plymouth Research is a restaurant menu scraping and analytics platform that aggregates menu data from 150+ restaurants in Plymouth, UK. The system provides an interactive dashboard for discovering dishes, comparing prices, and analyzing menu trends across the city's dining scene.

**Key Features:**
- Real menu data from 129+ Plymouth restaurants
- 3,577+ menu items with prices, descriptions, and dietary tags
- Interactive Streamlit dashboard with advanced analytics
- Two-phase restartable scraping architecture using Firecrawl API
- Data quality validation and outlier detection
- GDPR-compliant data collection (public business data only)

## Quick Start

### Prerequisites
```bash
pip install -r requirements.txt
```

**Required:**
- Python 3.9+
- SQLite 3
- Firecrawl API key (for scraping)

### Run Dashboard
```bash
streamlit run dashboard_app.py
```
Access at: http://localhost:8501

### Scrape New Restaurants

**Phase 1 - Discover Menu URLs:**
```bash
python phase1_discover_menus.py
```
Output: `restaurant_menu_urls.json`

**Phase 2 - Extract Menu Data:**
```bash
python phase2_extract_menus.py
```
Output: `restaurants_extracted.json`

**Import to Database:**
```bash
python import_from_json.py
```

## Project Structure

```
001-plymouth-research-restaurant-menu-analytics/
├── README.md                          # This file
├── SCRAPING_RESULTS.md               # Detailed scraping documentation
├── requirements.txt                   # Python dependencies
│
├── phase1_discover_menus.py          # Menu URL discovery (Firecrawl)
├── phase2_extract_menus.py           # Menu data extraction (Firecrawl)
├── import_from_json.py               # Import scraped data to database
├── dashboard_app.py                   # Interactive Streamlit dashboard
│
├── plymouth_research.db               # SQLite database (gitignored)
├── restaurant_menu_urls.json         # Phase 1 checkpoints (gitignored)
├── restaurants_extracted.json        # Phase 2 checkpoints (gitignored)
├── synthetic_restaurants_unique.csv  # Restaurant URL source list
│
├── src/                               # Source code modules
│   ├── database/                     # Database connection & operations
│   ├── parsers/                      # HTML/JSON parsers
│   ├── scraper/                      # Scraping utilities
│   └── scrapers/                     # Restaurant-specific scrapers
│
├── database/                          # Database schema & migrations
│   ├── schema.sql                    # PostgreSQL schema (reference)
│   ├── schema_sqlite.sql             # SQLite schema (active)
│   └── migrate_add_data_source.sql   # Data provenance migration
│
├── docs/governance/                   # Architecture governance artifacts
│   ├── requirements.md               # Business & technical requirements
│   ├── data-model.md                 # Data model with GDPR compliance
│   ├── dpia.md                       # Data Protection Impact Assessment
│   ├── stakeholder-drivers.md        # Stakeholder analysis
│   ├── risk-register.md              # Risk register
│   └── backlog.md                    # Product backlog
│
└── archive/                           # Archived obsolete files
    ├── obsolete_scripts/             # Old manual entry scripts
    ├── obsolete_json/                # Old batch generation files
    └── obsolete_docs/                # Superseded documentation
```

## Database Schema

**Tables:**
- `restaurants` - Restaurant metadata (name, address, cuisine, price range)
- `menu_items` - Menu items (name, description, price, category)
- `dietary_tags` - Dietary requirement tags (vegan, vegetarian, gluten-free)
- `menu_item_dietary_tags` - Many-to-many relationship

**Key Fields:**
- `data_source` - "real_scraped" or "synthetic" (data provenance)
- `scraping_method` - How data was obtained (e.g., "firecrawl_api_phase2")

## Dashboard Features

### Browse Menus
- View all menu items organized by restaurant and category
- Real data badges show which restaurants have actual scraped menus
- Dietary tag filtering (vegan, vegetarian, gluten-free)
- Price range filtering

### Price Analytics
- Price distribution by category (box plots)
- Price distribution by restaurant
- Histogram of menu item prices across all restaurants

### Restaurant Comparison
- **Outlier Detection:** IQR-based statistical outlier identification
- **Visualization Controls:**
  - Logarithmic scale toggle for extreme outliers
  - Exclude outliers option to focus on typical restaurants
  - Percentage view for category distribution
- **Statistical Metrics:** Median, min, max, outlier count
- **Color Coding:** Outliers (red), typical restaurants (teal)

### Statistics
- Real vs synthetic data breakdown
- Data provenance tracking
- Data freshness indicators

## Scraping Architecture

### Two-Phase Approach

**Phase 1: Menu URL Discovery**
- Uses Firecrawl `map()` to discover site structure
- Tests common menu paths (/menu, /menus, /food, /menu.pdf)
- Supports both HTML and PDF menus
- Checkpoint every 25 restaurants for restartability

**Phase 2: Menu Data Extraction**
- Structured JSON extraction with custom prompts
- Extracts: name, description, price, category, dietary tags
- Restaurant metadata: address, price range
- Checkpoint every 25 restaurants

### Data Quality Features
- **Outlier Detection:** IQR-based statistical analysis
- **Aggregator Filtering:** Prevents scraping TripAdvisor/Yelp data
- **Category Validation:** Default "Uncategorized" for missing categories
- **Data Provenance:** Tracks real vs synthetic data sources

## Current Statistics

**As of 2025-11-18:**
- **219 restaurants** in database
- **129 restaurants** (59%) with real scraped menu data
- **3,577 menu items** total
- **3,061 real menu items** from live websites
- **85 restaurants** with synthetic/placeholder data (failed scrapes)
- **5 restaurants** scraped but with 0 items (extraction failures)

**Data Quality Corrections:**
- Removed 1,006 erroneous items from TripAdvisor aggregator contamination
- Fixed 342 menu items with missing categories

## Legal & Ethical Compliance

- **robots.txt Compliance:** Respects website scraping policies
- **Rate Limiting:** Max 1 request per 5 seconds per domain
- **GDPR (UK):** Only public business data, no personal information
- **Copyright:** Transformative use for analytics, not republication
- **Attribution:** Clear source links to original restaurant websites

## Technology Stack

**Backend:**
- Python 3.9+
- SQLite 3 (file-based database)
- Firecrawl API (web scraping with JS rendering)

**Frontend:**
- Streamlit (interactive dashboard)
- Plotly (data visualizations)
- Pandas (data manipulation)

**Data Sources:**
- Restaurant websites (direct scraping)
- Firecrawl API (500 free credits used)

## Development Status

**Completed:**
- ✅ Two-phase scraping architecture with checkpoints
- ✅ Database schema with data provenance tracking
- ✅ Interactive Streamlit dashboard with outlier handling
- ✅ Data quality validation and corrections
- ✅ GDPR compliance assessment
- ✅ 129 restaurants successfully scraped

**Known Limitations:**
- 5 restaurants marked as scraped but have 0 items (extraction failures)
- Some restaurants lack category structure (marked as "Uncategorized")
- Chain restaurants (McDonald's, Pret) have less structured menu data
- Free Firecrawl credits exhausted (500 used)

## Future Enhancements

**Scraping Improvements:**
1. Add URL validation to filter aggregator sites (TripAdvisor, Yelp)
2. Implement retry logic for failed extractions
3. Add support for dynamic menu sections (seasonal, specials)
4. Scheduled weekly refresh of menu data

**Dashboard Enhancements:**
1. Search functionality for dishes across all restaurants
2. Map view showing restaurant locations
3. Trend analysis (price changes over time)
4. Recommendation engine based on preferences

**Data Quality:**
1. Re-extract restaurants with empty categories
2. Validate prices against reasonable ranges
3. Standardize cuisine type taxonomy
4. Add restaurant ratings/reviews integration

## Contributing

This is an ArcKit v0.9.1 test project for architecture governance workflows. The focus is on demonstrating enterprise architecture best practices rather than production-ready implementation.

## Documentation

- `SCRAPING_RESULTS.md` - Detailed scraping process, statistics, and lessons learned
- `docs/governance/requirements.md` - Comprehensive business and technical requirements
- `docs/governance/dpia.md` - Data Protection Impact Assessment (UK GDPR)
- `docs/governance/data-model.md` - Database schema with GDPR annotations

## License

This is a demonstration project for Plymouth Research. All restaurant data is publicly available business information scraped ethically and legally.

## Contact

For questions about this ArcKit test project, refer to the project documentation or CLAUDE.md in the repository root.
