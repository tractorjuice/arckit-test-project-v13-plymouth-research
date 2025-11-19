-- Google Places Extended Data Schema
-- Created: 2025-11-19
-- Purpose: Add service options, contact info, and business status from Google Places API

-- ============================================================================
-- PART 1: Add Service Options columns
-- ============================================================================

-- Service types
ALTER TABLE restaurants ADD COLUMN google_dine_in INTEGER DEFAULT 0;
ALTER TABLE restaurants ADD COLUMN google_takeout INTEGER DEFAULT 0;
ALTER TABLE restaurants ADD COLUMN google_delivery INTEGER DEFAULT 0;
ALTER TABLE restaurants ADD COLUMN google_reservable INTEGER DEFAULT 0;

-- Meal services
ALTER TABLE restaurants ADD COLUMN google_serves_breakfast INTEGER DEFAULT 0;
ALTER TABLE restaurants ADD COLUMN google_serves_lunch INTEGER DEFAULT 0;
ALTER TABLE restaurants ADD COLUMN google_serves_dinner INTEGER DEFAULT 0;

-- Beverage services
ALTER TABLE restaurants ADD COLUMN google_serves_beer INTEGER DEFAULT 0;
ALTER TABLE restaurants ADD COLUMN google_serves_wine INTEGER DEFAULT 0;

-- Dietary options
ALTER TABLE restaurants ADD COLUMN google_serves_vegetarian INTEGER DEFAULT 0;

-- ============================================================================
-- PART 2: Add Contact Information columns
-- ============================================================================

ALTER TABLE restaurants ADD COLUMN google_phone_national TEXT;
ALTER TABLE restaurants ADD COLUMN google_phone_international TEXT;
ALTER TABLE restaurants ADD COLUMN google_website_url TEXT;

-- ============================================================================
-- PART 3: Add Business Status column
-- ============================================================================

ALTER TABLE restaurants ADD COLUMN google_business_status TEXT; -- OPERATIONAL, CLOSED_TEMPORARILY, CLOSED_PERMANENTLY

-- ============================================================================
-- PART 4: Add Location Data columns (for future mapping)
-- ============================================================================

ALTER TABLE restaurants ADD COLUMN google_latitude REAL;
ALTER TABLE restaurants ADD COLUMN google_longitude REAL;
ALTER TABLE restaurants ADD COLUMN google_formatted_address TEXT;
ALTER TABLE restaurants ADD COLUMN google_maps_url TEXT;

-- ============================================================================
-- PART 5: Create indexes for common queries
-- ============================================================================

-- Index for filtering by service type
CREATE INDEX IF NOT EXISTS idx_google_service_options
ON restaurants(google_dine_in, google_takeout, google_delivery);

-- Index for filtering by meal service
CREATE INDEX IF NOT EXISTS idx_google_meal_services
ON restaurants(google_serves_breakfast, google_serves_lunch, google_serves_dinner);

-- Index for business status
CREATE INDEX IF NOT EXISTS idx_google_business_status
ON restaurants(google_business_status);

-- Index for location data (for geographic queries)
CREATE INDEX IF NOT EXISTS idx_google_location
ON restaurants(google_latitude, google_longitude);

-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================

-- Check new columns were added
-- PRAGMA table_info(restaurants);

-- Count restaurants by service options
-- SELECT
--     SUM(google_dine_in) as dine_in_count,
--     SUM(google_takeout) as takeout_count,
--     SUM(google_delivery) as delivery_count,
--     SUM(google_reservable) as reservable_count
-- FROM restaurants WHERE google_place_id IS NOT NULL;

-- Count by business status
-- SELECT google_business_status, COUNT(*)
-- FROM restaurants
-- WHERE google_place_id IS NOT NULL
-- GROUP BY google_business_status;

-- ============================================================================
-- NOTES
-- ============================================================================

/*
Service Options Usage:
- Filter restaurants by service type (dine-in, takeout, delivery)
- Find restaurants accepting reservations
- Filter by meal time (breakfast, lunch, dinner)
- Identify restaurants serving alcohol (beer, wine)
- Find vegetarian-friendly options

Contact Information Usage:
- Display phone numbers for reservations
- Link to official websites
- Validate existing website data

Business Status Usage:
- Filter out permanently closed restaurants
- Identify temporarily closed (useful during updates)
- Show only operational restaurants

Location Data Usage:
- Add interactive map to dashboard
- "Restaurants near me" feature
- Distance calculations
- Geographic filtering by area

Cost: $0 additional (all fields included in existing Place Details API calls)
*/
