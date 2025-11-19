-- Google Reviews Integration Schema
-- Created: 2025-11-19
-- Purpose: Add Google Reviews/Google Places API integration to restaurant database

-- ============================================================================
-- PART 1: Add Google Reviews columns to restaurants table
-- ============================================================================

-- Add Google Places metadata columns
ALTER TABLE restaurants ADD COLUMN google_place_id TEXT;
ALTER TABLE restaurants ADD COLUMN google_rating REAL;
ALTER TABLE restaurants ADD COLUMN google_user_ratings_total INTEGER DEFAULT 0;
ALTER TABLE restaurants ADD COLUMN google_price_level INTEGER; -- 0-4 (Free to Very Expensive)
ALTER TABLE restaurants ADD COLUMN google_last_fetched_at TEXT;

-- Add computed aggregate columns (updated by triggers)
ALTER TABLE restaurants ADD COLUMN google_review_count INTEGER DEFAULT 0;
ALTER TABLE restaurants ADD COLUMN google_avg_rating REAL;

-- ============================================================================
-- PART 2: Create google_reviews table
-- ============================================================================

CREATE TABLE IF NOT EXISTS google_reviews (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    restaurant_id INTEGER NOT NULL,

    -- Review content
    review_date TEXT NOT NULL,           -- ISO8601 datetime (converted from Unix timestamp)
    author_name TEXT,
    review_text TEXT,
    rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),

    -- Google-specific metadata
    google_author_url TEXT,              -- Google Maps profile URL
    google_profile_photo_url TEXT,       -- Author's profile photo
    language TEXT,                       -- Language code (e.g., 'en', 'es')
    relative_time_description TEXT,      -- e.g., "2 weeks ago"

    -- Scraping metadata
    fetched_at TEXT NOT NULL,

    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id) ON DELETE CASCADE
);

-- ============================================================================
-- PART 3: Create indexes for performance
-- ============================================================================

-- Index on restaurant_id for fast lookups
CREATE INDEX IF NOT EXISTS idx_google_reviews_restaurant
ON google_reviews(restaurant_id);

-- Index on review_date for date-based queries
CREATE INDEX IF NOT EXISTS idx_google_reviews_date
ON google_reviews(review_date);

-- Index on rating for rating-based filters
CREATE INDEX IF NOT EXISTS idx_google_reviews_rating
ON google_reviews(rating);

-- Composite index for restaurant + date queries
CREATE INDEX IF NOT EXISTS idx_google_reviews_restaurant_date
ON google_reviews(restaurant_id, review_date DESC);

-- Unique constraint to prevent duplicate reviews (by restaurant + author + date)
CREATE UNIQUE INDEX IF NOT EXISTS idx_google_reviews_unique
ON google_reviews(restaurant_id, author_name, review_date, review_text);

-- ============================================================================
-- PART 4: Create view for aggregated statistics
-- ============================================================================

CREATE VIEW IF NOT EXISTS restaurant_google_summary AS
SELECT
    r.restaurant_id,
    r.name,
    r.google_place_id,
    r.google_rating,
    r.google_user_ratings_total,
    r.google_review_count,
    r.google_avg_rating,

    -- Calculated statistics from our stored reviews
    COUNT(gr.review_id) as actual_review_count,
    ROUND(AVG(gr.rating), 2) as calculated_avg_rating,
    MIN(gr.review_date) as oldest_review_date,
    MAX(gr.review_date) as newest_review_date,

    -- Rating distribution
    SUM(CASE WHEN gr.rating = 5 THEN 1 ELSE 0 END) as five_star_count,
    SUM(CASE WHEN gr.rating = 4 THEN 1 ELSE 0 END) as four_star_count,
    SUM(CASE WHEN gr.rating = 3 THEN 1 ELSE 0 END) as three_star_count,
    SUM(CASE WHEN gr.rating = 2 THEN 1 ELSE 0 END) as two_star_count,
    SUM(CASE WHEN gr.rating = 1 THEN 1 ELSE 0 END) as one_star_count

FROM restaurants r
LEFT JOIN google_reviews gr ON r.restaurant_id = gr.restaurant_id
GROUP BY r.restaurant_id;

-- ============================================================================
-- PART 5: Create triggers for automatic statistics updates
-- ============================================================================

-- Trigger to update restaurant stats when new review is inserted
CREATE TRIGGER IF NOT EXISTS update_restaurant_google_stats_insert
AFTER INSERT ON google_reviews
BEGIN
    UPDATE restaurants
    SET
        google_review_count = (
            SELECT COUNT(*)
            FROM google_reviews
            WHERE restaurant_id = NEW.restaurant_id
        ),
        google_avg_rating = (
            SELECT ROUND(AVG(rating), 2)
            FROM google_reviews
            WHERE restaurant_id = NEW.restaurant_id
        )
    WHERE restaurant_id = NEW.restaurant_id;
END;

-- Trigger to update restaurant stats when review is deleted
CREATE TRIGGER IF NOT EXISTS update_restaurant_google_stats_delete
AFTER DELETE ON google_reviews
BEGIN
    UPDATE restaurants
    SET
        google_review_count = (
            SELECT COUNT(*)
            FROM google_reviews
            WHERE restaurant_id = OLD.restaurant_id
        ),
        google_avg_rating = (
            SELECT ROUND(AVG(rating), 2)
            FROM google_reviews
            WHERE restaurant_id = OLD.restaurant_id
        )
    WHERE restaurant_id = OLD.restaurant_id;
END;

-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================

-- Check schema was created successfully
-- SELECT name FROM sqlite_master WHERE type='table' AND name='google_reviews';
-- SELECT name FROM sqlite_master WHERE type='view' AND name='restaurant_google_summary';
-- SELECT name FROM sqlite_master WHERE type='trigger' AND name LIKE '%google%';

-- Sample query to test the view
-- SELECT * FROM restaurant_google_summary WHERE google_review_count > 0 LIMIT 5;

-- ============================================================================
-- NOTES
-- ============================================================================

/*
Google Places API Limitations:
- Only returns 5 most recent reviews per location (API limitation)
- Reviews are filtered by Google (may not show all reviews)
- Requires API key with Places API enabled
- Free tier: 25,000 requests/month
- Cost after free tier: $17 per 1,000 additional requests

Data Freshness:
- Run `fetch_google_reviews.py --all` to fetch all restaurants
- Run `fetch_google_reviews.py --update` for incremental updates
- Recommended frequency: Weekly

Attribution:
- Display "Reviews from Google" in dashboard
- Include Google logo/branding as per Google's guidelines
- Link back to Google Maps listing

Comparison with Trustpilot:
- Google: 5 reviews per restaurant (API limit) but higher coverage (98% expected)
- Trustpilot: Unlimited reviews but lower coverage (64% achieved)
- Together: Comprehensive review coverage
*/
