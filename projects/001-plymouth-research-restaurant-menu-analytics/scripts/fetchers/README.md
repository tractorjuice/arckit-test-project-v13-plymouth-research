# Data Fetchers

Scripts for fetching and scraping data from external sources.

## Active Scripts

- **fetch_hygiene_ratings_v2.py** - FSA Food Hygiene Rating Scheme data fetcher (XML-based)
- **fetch_trustpilot_reviews.py** - Scrape Trustpilot reviews
- **fetch_google_reviews.py** - Fetch Google Places reviews via API
- **fetch_companies_house_data.py** - Companies House API data fetcher
- **fetch_balance_sheets_v2.py** - Financial data fetcher (v2)
- **fetch_directors.py** - Company directors data fetcher
- **discover_trustpilot_urls.py** - Multi-strategy Trustpilot URL discovery
- **discover_restaurants_google.py** - Google Places API restaurant discovery
- **scrape_plymouth_licensing_fixed.py** - Plymouth licensing data scraper (fixed version)

## Usage

All fetchers output to `data/raw/` or `data/processed/` directories.

Example:
```bash
python fetch_hygiene_ratings_v2.py
```
