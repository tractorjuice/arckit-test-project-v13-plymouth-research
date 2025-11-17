-- Migration: Add Data Source Tracking
-- Date: 2025-11-17
-- Purpose: Track whether restaurant data is real (scraped) vs synthetic/test data

-- Add data_source column to restaurants table
-- Values: 'real_scraped', 'synthetic', 'test', 'manual_entry'
ALTER TABLE restaurants ADD COLUMN data_source TEXT DEFAULT 'synthetic';

-- Add scraping_method column to restaurants table
-- Values: 'web_fetch_manual', 'beautifulsoup', 'playwright', 'scrapy', 'manual_entry', 'synthetic_generation'
ALTER TABLE restaurants ADD COLUMN scraping_method TEXT DEFAULT 'synthetic_generation';

-- Update existing restaurants with default values
-- All existing data is synthetic unless proven otherwise
UPDATE restaurants SET data_source = 'synthetic', scraping_method = 'synthetic_generation';

-- Mark known real restaurants (based on scraping_logs)
UPDATE restaurants
SET data_source = 'real_scraped', scraping_method = 'web_fetch_manual'
WHERE restaurant_id IN (
    SELECT DISTINCT restaurant_id
    FROM scraping_logs
    WHERE success = 1 AND restaurant_id IS NOT NULL
);

-- Create index for filtering by data source
CREATE INDEX IF NOT EXISTS idx_restaurants_data_source ON restaurants(data_source);
