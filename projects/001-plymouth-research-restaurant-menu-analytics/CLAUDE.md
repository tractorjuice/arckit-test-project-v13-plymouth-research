# Plymouth Research Restaurant Menu Analytics - Implementation Guide

This file provides guidance for working with the Plymouth Research Restaurant Menu Analytics dashboard implementation.

## Project Status

**Implementation Phase**: Dashboard MVP with Food Hygiene Ratings + Trustpilot Reviews integration

**Current Capabilities**:
- 98 restaurants with scraped menu data
- 2,625 menu items with prices, descriptions, dietary tags
- FSA Food Hygiene Rating Scheme integration (49/98 restaurants rated)
- Trustpilot Reviews integration (63/98 restaurants, 9,410 reviews)
- Interactive Streamlit dashboard with 8 tabs
- SQLite database with full-text search
- Hygiene vs Customer Satisfaction correlation analysis

## Quick Start

### Running the Dashboard

```bash
# Activate environment (if using venv)
# source venv/bin/activate

# Run dashboard
streamlit run dashboard_app.py

# Dashboard will open at http://localhost:8501
```

### Refreshing Hygiene Ratings

```bash
# Download latest FSA Plymouth data
curl -o plymouth_fsa_data.xml https://ratings.food.gov.uk/api/open-data-files/FHRS891en-GB.xml

# Run matcher
python fetch_hygiene_ratings_v2.py

# Review unmatched restaurants
cat unmatched_hygiene_ratings.csv
```

### Refreshing Trustpilot Reviews

```bash
# Incremental update (fetch only new reviews)
python fetch_trustpilot_reviews.py --update

# Full refresh of specific restaurant
python fetch_trustpilot_reviews.py --restaurant-id 4 --max-pages 50

# Discover Trustpilot URLs for new restaurants
python discover_trustpilot_urls.py --discover-all --auto-update
```

## Key Files

### Core Application
- **dashboard_app.py** (2,053 lines) - Main Streamlit dashboard application
  - 8 tabs: Overview, Browse Menus, Price Analysis, Cuisine Comparison, Dietary Options, Hygiene Ratings, Reviews, About
  - Caches data with 5-minute TTL
  - Full-text search with filtering
  - Hygiene rating filters and badges
  - Trustpilot review display and correlation analysis

### Database
- **plymouth_research.db** - SQLite database (excluded from git)
  - `restaurants` table: 98 rows, 29 columns (inc. 9 hygiene + 5 Trustpilot columns)
  - `menu_items` table: 2,625 rows, 13 columns
  - `drinks` table: Beverage data with categories
  - `trustpilot_reviews` table: 9,410 rows, 13 columns
  - `restaurant_trustpilot_summary` view: Pre-aggregated review statistics
  - Full-text search indexes

### Schema Management
- **add_hygiene_columns.sql** - Database schema for FSA hygiene ratings
  - 9 new columns added to `restaurants` table
  - Indexed for performance
- **add_trustpilot_schema.sql** - Database schema for Trustpilot reviews
  - 5 new columns added to `restaurants` table
  - New `trustpilot_reviews` table with 13 columns
  - New `restaurant_trustpilot_summary` view
  - 5 indexes for query performance
  - 2 triggers for automatic stat updates

### Data Fetching
- **fetch_hygiene_ratings_v2.py** - FSA data matcher (XML-based)
  - Parses 1,841 establishments from FSA Plymouth XML
  - Multi-factor matching: name similarity + postcode + address
  - 70+ confidence threshold for auto-matching
  - Exports matched/unmatched CSVs
- **fetch_trustpilot_reviews.py** (591 lines) - Trustpilot review scraper
  - Scrapes Trustpilot's __NEXT_DATA__ JSON structure
  - Rate limiting: 2.5s between pages, 5s between restaurants
  - Incremental updates (only fetch new reviews)
  - Automatic deduplication
  - Batch processing support
- **discover_trustpilot_urls.py** (533 lines) - Trustpilot URL discovery
  - Multi-strategy: domain-based + direct search
  - Confidence scoring with SequenceMatcher
  - CSV export for manual verification
  - Auto-update for high-confidence matches (95%+)

### Documentation
- **HYGIENE_RATINGS_GUIDE.md** - Complete FSA rating system documentation
  - Scoring methodology (0-25 in 3 categories)
  - Final rating calculation (0-5 stars)
  - Plymouth data analysis (49 restaurants)
  - Dashboard display guidelines
- **TRUSTPILOT_INTEGRATION_GUIDE.md** (632 lines) - Comprehensive Trustpilot integration guide
  - Implementation overview (Phases 1-4)
  - Database schema documentation
  - Tool usage examples and workflows
  - Data quality checks
  - Legal & ethical compliance notes
  - Troubleshooting guide

## Database Schema

### restaurants table (29 columns)

**Core Fields**:
- `restaurant_id` INTEGER PRIMARY KEY
- `name` TEXT NOT NULL
- `cuisine_type` TEXT
- `price_range` TEXT (£, ££, £££, ££££)
- `address` TEXT
- `website_url` TEXT
- `data_source` TEXT ('real_scraped', 'synthetic')
- `is_active` INTEGER (0/1)

**Hygiene Rating Fields** (added 2025-11-18):
- `hygiene_rating` INTEGER (0-5 stars)
- `hygiene_rating_date` TEXT (ISO8601 datetime)
- `fsa_id` INTEGER (FSA unique ID)
- `hygiene_score_hygiene` INTEGER (0-25, lower is better)
- `hygiene_score_structural` INTEGER (0-25, lower is better)
- `hygiene_score_confidence` INTEGER (0-30, lower is better)
- `fsa_business_type` TEXT
- `fsa_local_authority` TEXT
- `hygiene_rating_fetched_at` TEXT (ISO8601 timestamp)

**Trustpilot Fields** (added 2025-11-19):
- `trustpilot_url` TEXT (Full Trustpilot page URL)
- `trustpilot_business_id` TEXT (Business slug, e.g., "therockfish.co.uk")
- `trustpilot_last_scraped_at` TEXT (ISO8601 timestamp)
- `trustpilot_review_count` INTEGER (Auto-updated by trigger)
- `trustpilot_avg_rating` REAL (Auto-updated by trigger)

### menu_items table (13 columns)
- `item_id` INTEGER PRIMARY KEY
- `restaurant_id` INTEGER FOREIGN KEY
- `item_name` TEXT NOT NULL
- `category` TEXT
- `description` TEXT
- `price` REAL
- `currency` TEXT (default 'GBP')
- `is_vegetarian` INTEGER (0/1)
- `is_vegan` INTEGER (0/1)
- `is_gluten_free` INTEGER (0/1)
- `allergen_info` TEXT
- `scraped_at` TEXT
- `last_updated` TEXT

### trustpilot_reviews table (13 columns, added 2025-11-19)
- `review_id` INTEGER PRIMARY KEY AUTOINCREMENT
- `restaurant_id` INTEGER FOREIGN KEY (CASCADE DELETE)
- `review_date` TEXT NOT NULL (ISO8601 date)
- `author_name` TEXT
- `review_title` TEXT
- `review_body` TEXT
- `rating` INTEGER CHECK(rating BETWEEN 1 AND 5)
- `author_location` TEXT (Country code)
- `author_review_count` INTEGER
- `page_number` INTEGER
- `scraped_at` TEXT NOT NULL
- `is_verified_purchase` INTEGER DEFAULT 0
- `reply_count` INTEGER DEFAULT 0
- `helpful_count` INTEGER DEFAULT 0

## FSA Food Hygiene Rating System

### Rating Scale
- **5★ (Very Good)**: 0-15 total points
- **4★ (Good)**: 20 total points
- **3★ (Satisfactory)**: 25-30 total points
- **2★ (Improvement Necessary)**: 35-40 total points
- **1★ (Major Improvement)**: 45-50 total points
- **0★ (Urgent Improvement)**: 50+ total points

### Override Rules
- If ANY category scores ≥15, maximum rating is 3★
- If ANY category scores ≥20, rating is further reduced

### Plymouth Data (49/98 restaurants rated)
- **Average Rating**: 4.51/5
- **Distribution**: 67.3% (5★), 24.5% (4★), 2.0% (3★), 4.1% (2★), 2.0% (1★)
- **Data Source**: FSA Plymouth XML (Authority Code 891)
- **Extract Date**: 2025-11-15
- **Total Establishments in XML**: 1,841 (443 restaurants/cafes)

## Matching Algorithm (fetch_hygiene_ratings_v2.py)

### Scoring System
1. **Name Similarity** (0-100 points)
   - Uses `difflib.SequenceMatcher`
   - ≥95% = "exact_name"
   - ≥80% = "similar_name"
   - ≥60% = "partial_name"

2. **Postcode Match** (50 bonus points)
   - Exact match on normalized UK postcode
   - Extracted using regex pattern

3. **Address Similarity** (0-30 bonus points)
   - Word-based matching
   - 5 points per common word (max 30)

4. **Confidence Threshold**: 70+ points for auto-match

### Results (as of 2025-11-18)
- **Matched**: 49 restaurants (50%)
- **Unmatched**: 49 restaurants (exported to CSV)
- **High Confidence Matches**: 23 exact names (100% confidence)
- **Low Confidence**: 5 matches between 70-80% (manual review recommended)

## Dashboard Features

### Tab 1: Overview
- 6 key metrics (restaurants, items, cuisines, avg price, price range, avg hygiene)
- Quick stats and navigation
- Data source breakdown

### Tab 2: Browse Menus
- Search across all menu items (full-text search)
- Filter by: cuisine, price range, dietary preferences, hygiene rating
- Color-coded data source badges
- Hygiene rating badges with inspection dates
- Menu item cards with prices and dietary tags

### Tab 3: Price Analysis
- Price distribution histogram
- Average prices by cuisine (bar chart)
- Price range distribution (pie chart)
- Statistical summary

### Tab 4: Cuisine Comparison
- Menu item counts by cuisine
- Vegetarian/Vegan options by cuisine
- Gluten-free availability
- Comparative analysis

### Tab 5: Dietary Options
- Vegetarian/Vegan/Gluten-free counts
- Dietary options by cuisine (grouped bar chart)
- Dietary option percentages (stacked bar chart)
- Restaurant-level dietary support

### Tab 6: Hygiene Ratings
- Overview metrics (rated count, average, distribution)
- Rating distribution chart (color-coded)
- Detailed scores breakdown table
- Restaurants requiring attention (≤2★)
- FSA attribution and links

### Tab 7: Reviews ⭐ NEW
- Overview metrics (restaurants reviewed, total reviews, avg rating, recent reviews)
- Recent reviews feed with filters (restaurant, rating, date range)
- Rating distribution charts (bar chart + pie chart)
- Hygiene vs Trustpilot correlation scatter plot
- Restaurants by reviews table (sortable)
- Trustpilot attribution

### Tab 8: About
- Project overview
- Data sources
- Statistics
- Technology stack
- Contact information

## Data Sources

### Restaurant Menu Data
- **Source**: Web scraping (98 restaurants)
- **Method**: BeautifulSoup, Selenium (for dynamic content)
- **Rate Limiting**: 1 request per 5 seconds per domain
- **Last Updated**: Varies by restaurant (see `last_updated` column)
- **Coverage**: 2,625 menu items

### FSA Food Hygiene Ratings
- **Source**: Food Standards Agency Open Data
- **URL**: https://ratings.food.gov.uk/api/open-data-files/FHRS891en-GB.xml
- **Authority**: Plymouth City (Code 891)
- **Extract Date**: 2025-11-15
- **Update Frequency**: Weekly (FSA updates XML files weekly)
- **License**: Open Government License (OGL)

### Trustpilot Reviews
- **Source**: Trustpilot.com (public reviews)
- **Method**: Web scraping (__NEXT_DATA__ JSON extraction)
- **Coverage**: 63/98 restaurants (96.9% of those with Trustpilot pages)
- **Total Reviews**: 9,410
- **Date Range**: 2013-12-04 to 2025-11-19 (12 years)
- **Average Rating**: 2.67/5
- **Update Frequency**: Manual (run --update for incremental)
- **Rate Limiting**: 2.5s between pages, 5s between restaurants
- **License**: Public data for analytics (non-commercial, internal use)

## Known Limitations

1. **Hygiene Rating Coverage**: Only 50% of restaurants matched
   - 49 unmatched restaurants need manual review
   - Missing addresses make matching difficult
   - Some restaurants may be new (not yet inspected)

2. **Trustpilot Review Coverage**: 64% of restaurants
   - 35 restaurants have no Trustpilot page
   - Chain restaurant reviews are company-wide (not location-specific)
   - Some reviews may be for different branches
   - Only 27% of restaurants have BOTH hygiene AND review data

3. **Menu Data Freshness**: Varies by restaurant
   - No automated refresh yet
   - Some menus may be outdated
   - Prices may have changed

4. **Data Quality**: Scraped data quality varies
   - Some descriptions missing
   - Dietary tags may be incomplete
   - Price extraction errors possible

5. **Search Performance**: Good for current scale (2,625 items, 9,410 reviews)
   - May need optimization at 10,000+ items
   - Full-text search is not indexed on all fields

## Future Enhancements

### High Priority
1. Manual review and matching of 49 unmatched restaurants
2. Automated weekly refresh of FSA hygiene ratings
3. Automated menu scraping schedule (weekly/monthly)
4. Data quality validation and cleanup

### Medium Priority
1. Historical trend analysis (hygiene rating + review changes over time)
2. Geographic mapping (restaurant locations on map)
3. Export functionality (CSV, PDF reports)
4. API endpoint for programmatic access
5. Sentiment analysis on review text
6. Weekly automated refresh of Trustpilot reviews

### Low Priority
1. User accounts and favorites
2. Additional review sources (Google, TripAdvisor)
3. Reservation system integration
4. Mobile app

## Troubleshooting

### Dashboard Won't Start
```bash
# Check Python version (need 3.8+)
python --version

# Install dependencies
pip install streamlit pandas plotly sqlite3

# Check database exists
ls -lh plymouth_research.db
```

### Hygiene Ratings Not Showing
```bash
# Check if data exists
sqlite3 plymouth_research.db "SELECT COUNT(*) FROM restaurants WHERE hygiene_rating IS NOT NULL;"

# Should return: 49

# If 0, re-run fetch script
python fetch_hygiene_ratings_v2.py
```

### Date Parsing Errors
- FSA dates are ISO8601 format with time component
- Use `pd.to_datetime(date, format='ISO8601')` not `format="%Y-%m-%d"`

### Matching Issues
- Edit matching thresholds in `fetch_hygiene_ratings_v2.py`
- Lower confidence threshold from 70 to 60 for more matches
- Review `unmatched_hygiene_ratings.csv` for manual matching

## Legal & Ethical Notes

### Web Scraping
- **Respect robots.txt**: Check before scraping new restaurants
- **Rate Limiting**: 1 request per 5 seconds minimum
- **Terms of Service**: Review each website's ToS
- **Copyright**: Transformative use (analytics) not republication

### GDPR Compliance
- **Data Type**: Public business data only (no personal data)
- **Legal Basis**: Legitimate interest (market research)
- **Retention**: 12 months for trend analysis
- **Rights**: Restaurants can request removal

### FSA Data
- **License**: Open Government License v3.0
- **Attribution**: Required (displayed in dashboard)
- **Permitted Use**: Free to use, share, adapt
- **Updates**: FSA updates weekly, use latest data

### Trustpilot Data
- **License**: Public data scraping for analytics
- **Attribution**: Required ("Reviews from Trustpilot.com")
- **Permitted Use**: Internal analytics only, not republication
- **Rate Limiting**: Respectful scraping (2.5s between requests)
- **Compliance**: Robots.txt compliant, User-Agent header included
- **Ethics**: Transformative use (analytics), not commercial redistribution

## Key Insights

### Hygiene vs Customer Satisfaction Disconnect

Analysis of the 26 restaurants with BOTH hygiene ratings AND Trustpilot reviews reveals:

**Average Ratings by Hygiene Category**:
- 5★ Hygiene (Excellent) → 2.72★ Trustpilot
- 4★ Hygiene (Good) → 2.15★ Trustpilot

**Finding**: Food safety does NOT predict customer satisfaction

**Biggest Gaps** (all have 5★ FSA hygiene but poor reviews):
- Taco Bell: 5★ hygiene, 1.66★ Trustpilot (-3.34 gap)
- McDonald's: 5★ hygiene, 1.89★ Trustpilot (-3.11 gap)
- Burger King: 5★ hygiene, 2.04★ Trustpilot (-2.96 gap)

**Interpretation**: Fast food chains maintain excellent food safety but receive poor customer reviews driven by service quality, food taste, value, and speed - not hygiene.

**Top Overall** (high in both metrics):
- Rockfish Plymouth: 5★ hygiene, 3.75★ Trustpilot
- Armado Lounge: 5★ hygiene, 3.45★ Trustpilot

## References

- **FSA FHRS Homepage**: https://www.food.gov.uk/safety-hygiene/food-hygiene-rating-scheme
- **FSA API Documentation**: https://api.ratings.food.gov.uk/help
- **Plymouth FSA Data**: https://ratings.food.gov.uk/api/open-data-files/FHRS891en-GB.xml
- **OGL License**: https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/
- **Trustpilot Integration Guide**: TRUSTPILOT_INTEGRATION_GUIDE.md

---

*Last Updated: 2025-11-19*
*Dashboard Version: 1.2.0 (with FSA hygiene ratings + Trustpilot reviews)*
