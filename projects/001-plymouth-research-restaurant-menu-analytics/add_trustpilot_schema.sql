-- ============================================================================
-- Trustpilot Reviews Schema Migration
-- ============================================================================
-- Purpose: Add Trustpilot review functionality to Plymouth Research database
-- Date: 2025-11-18
--
-- This migration adds:
-- 1. Trustpilot metadata columns to restaurants table
-- 2. New trustpilot_reviews table for storing review data
-- 3. Indexes for performance
-- ============================================================================

-- Step 1: Add Trustpilot metadata columns to restaurants table
-- ============================================================================

ALTER TABLE restaurants ADD COLUMN trustpilot_url TEXT;
ALTER TABLE restaurants ADD COLUMN trustpilot_business_id TEXT;
ALTER TABLE restaurants ADD COLUMN trustpilot_last_scraped_at TEXT;
ALTER TABLE restaurants ADD COLUMN trustpilot_review_count INTEGER DEFAULT 0;
ALTER TABLE restaurants ADD COLUMN trustpilot_avg_rating REAL;

-- Create index for Trustpilot lookups
CREATE INDEX IF NOT EXISTS idx_restaurants_trustpilot_id
    ON restaurants(trustpilot_business_id);

-- Step 2: Create trustpilot_reviews table
-- ============================================================================

CREATE TABLE IF NOT EXISTS trustpilot_reviews (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    restaurant_id INTEGER NOT NULL,

    -- Review content
    review_date TEXT NOT NULL,              -- ISO8601 date (YYYY-MM-DD)
    author_name TEXT,                       -- Reviewer display name
    review_title TEXT,                      -- Review heading/title
    review_body TEXT,                       -- Full review text
    rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),

    -- Metadata
    author_location TEXT,                   -- Country code (GB, US, etc.)
    author_review_count INTEGER,            -- How many reviews this author has written
    page_number INTEGER,                    -- Which page this review was on
    scraped_at TEXT NOT NULL,               -- When we fetched this (ISO8601)

    -- Trustpilot-specific fields
    is_verified_purchase INTEGER DEFAULT 0, -- If Trustpilot marked as verified
    reply_count INTEGER DEFAULT 0,          -- Number of business replies
    helpful_count INTEGER DEFAULT 0,        -- "Helpful" votes on Trustpilot

    -- Relationships
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id) ON DELETE CASCADE
);

-- Step 3: Create indexes for performance
-- ============================================================================

-- Index for getting all reviews for a restaurant
CREATE INDEX IF NOT EXISTS idx_reviews_restaurant
    ON trustpilot_reviews(restaurant_id);

-- Index for sorting by date (most recent first)
CREATE INDEX IF NOT EXISTS idx_reviews_date
    ON trustpilot_reviews(review_date DESC);

-- Index for filtering by rating
CREATE INDEX IF NOT EXISTS idx_reviews_rating
    ON trustpilot_reviews(rating);

-- Composite index for restaurant + date queries
CREATE INDEX IF NOT EXISTS idx_reviews_restaurant_date
    ON trustpilot_reviews(restaurant_id, review_date DESC);

-- Index for deduplication (prevent duplicate reviews)
CREATE INDEX IF NOT EXISTS idx_reviews_dedup
    ON trustpilot_reviews(restaurant_id, review_date, author_name, review_body);

-- Step 4: Create aggregate view for dashboard queries
-- ============================================================================

CREATE VIEW IF NOT EXISTS restaurant_trustpilot_summary AS
SELECT
    r.restaurant_id,
    r.name,
    r.trustpilot_url,
    r.trustpilot_avg_rating,
    r.trustpilot_review_count,
    r.trustpilot_last_scraped_at,
    COUNT(tr.review_id) AS actual_review_count,
    AVG(tr.rating) AS calculated_avg_rating,
    MIN(tr.review_date) AS oldest_review_date,
    MAX(tr.review_date) AS newest_review_date,
    SUM(CASE WHEN tr.rating = 5 THEN 1 ELSE 0 END) AS five_star_count,
    SUM(CASE WHEN tr.rating = 4 THEN 1 ELSE 0 END) AS four_star_count,
    SUM(CASE WHEN tr.rating = 3 THEN 1 ELSE 0 END) AS three_star_count,
    SUM(CASE WHEN tr.rating = 2 THEN 1 ELSE 0 END) AS two_star_count,
    SUM(CASE WHEN tr.rating = 1 THEN 1 ELSE 0 END) AS one_star_count
FROM restaurants r
LEFT JOIN trustpilot_reviews tr ON r.restaurant_id = tr.restaurant_id
WHERE r.is_active = 1
GROUP BY r.restaurant_id;

-- Step 5: Create helper functions via triggers
-- ============================================================================

-- Trigger to update restaurant aggregate stats when reviews are inserted
CREATE TRIGGER IF NOT EXISTS update_restaurant_trustpilot_stats_insert
AFTER INSERT ON trustpilot_reviews
BEGIN
    UPDATE restaurants
    SET
        trustpilot_review_count = (
            SELECT COUNT(*)
            FROM trustpilot_reviews
            WHERE restaurant_id = NEW.restaurant_id
        ),
        trustpilot_avg_rating = (
            SELECT ROUND(AVG(rating), 2)
            FROM trustpilot_reviews
            WHERE restaurant_id = NEW.restaurant_id
        )
    WHERE restaurant_id = NEW.restaurant_id;
END;

-- Trigger to update restaurant aggregate stats when reviews are deleted
CREATE TRIGGER IF NOT EXISTS update_restaurant_trustpilot_stats_delete
AFTER DELETE ON trustpilot_reviews
BEGIN
    UPDATE restaurants
    SET
        trustpilot_review_count = (
            SELECT COUNT(*)
            FROM trustpilot_reviews
            WHERE restaurant_id = OLD.restaurant_id
        ),
        trustpilot_avg_rating = (
            SELECT ROUND(AVG(rating), 2)
            FROM trustpilot_reviews
            WHERE restaurant_id = OLD.restaurant_id
        )
    WHERE restaurant_id = OLD.restaurant_id;
END;

-- ============================================================================
-- Verification Queries (run after migration)
-- ============================================================================

-- Check new columns exist
-- SELECT * FROM pragma_table_info('restaurants') WHERE name LIKE 'trustpilot%';

-- Check new table exists
-- SELECT name FROM sqlite_master WHERE type='table' AND name='trustpilot_reviews';

-- Check indexes were created
-- SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='trustpilot_reviews';

-- Check view exists
-- SELECT name FROM sqlite_master WHERE type='view' AND name='restaurant_trustpilot_summary';

-- ============================================================================
-- Rollback Script (if needed)
-- ============================================================================

-- DROP TRIGGER IF EXISTS update_restaurant_trustpilot_stats_insert;
-- DROP TRIGGER IF EXISTS update_restaurant_trustpilot_stats_delete;
-- DROP VIEW IF EXISTS restaurant_trustpilot_summary;
-- DROP INDEX IF EXISTS idx_reviews_dedup;
-- DROP INDEX IF EXISTS idx_reviews_restaurant_date;
-- DROP INDEX IF EXISTS idx_reviews_rating;
-- DROP INDEX IF EXISTS idx_reviews_date;
-- DROP INDEX IF EXISTS idx_reviews_restaurant;
-- DROP TABLE IF EXISTS trustpilot_reviews;
-- DROP INDEX IF EXISTS idx_restaurants_trustpilot_id;
--
-- -- Note: SQLite doesn't support DROP COLUMN, so removing columns requires recreating table
-- -- For development, can just delete the database and recreate from schema.sql
