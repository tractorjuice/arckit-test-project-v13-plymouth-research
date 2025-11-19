-- =================================================================
-- Database Performance Indexes
-- =================================================================
-- Adds indexes to speed up dashboard queries
-- Author: Plymouth Research Team
-- Date: 2025-11-19
-- =================================================================

-- Check existing indexes
SELECT name, tbl_name, sql FROM sqlite_master WHERE type = 'index' ORDER BY tbl_name, name;

-- ============================================================================
-- Restaurants Table Indexes
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_restaurants_name
ON restaurants(name);

CREATE INDEX IF NOT EXISTS idx_restaurants_cuisine
ON restaurants(cuisine_type);

CREATE INDEX IF NOT EXISTS idx_restaurants_price
ON restaurants(price_range);

CREATE INDEX IF NOT EXISTS idx_restaurants_active
ON restaurants(is_active);

CREATE INDEX IF NOT EXISTS idx_restaurants_company
ON restaurants(company_number);

CREATE INDEX IF NOT EXISTS idx_restaurants_hygiene
ON restaurants(hygiene_rating);

-- ============================================================================
-- Menu Items Table Indexes
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_menu_items_restaurant
ON menu_items(restaurant_id);

CREATE INDEX IF NOT EXISTS idx_menu_items_category
ON menu_items(category);

CREATE INDEX IF NOT EXISTS idx_menu_items_price
ON menu_items(price_gbp);

-- Composite index for common query pattern (restaurant + category)
CREATE INDEX IF NOT EXISTS idx_menu_items_restaurant_category
ON menu_items(restaurant_id, category);

-- ============================================================================
-- Reviews Table Indexes
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_trustpilot_reviews_restaurant
ON trustpilot_reviews(restaurant_id);

CREATE INDEX IF NOT EXISTS idx_trustpilot_reviews_date
ON trustpilot_reviews(review_date);

CREATE INDEX IF NOT EXISTS idx_trustpilot_reviews_rating
ON trustpilot_reviews(rating);

-- Composite index for common query pattern (restaurant + date)
CREATE INDEX IF NOT EXISTS idx_trustpilot_reviews_restaurant_date
ON trustpilot_reviews(restaurant_id, review_date DESC);

CREATE INDEX IF NOT EXISTS idx_google_reviews_restaurant
ON google_reviews(restaurant_id);

CREATE INDEX IF NOT EXISTS idx_google_reviews_date
ON google_reviews(review_date);

CREATE INDEX IF NOT EXISTS idx_google_reviews_rating
ON google_reviews(rating);

-- Composite index for common query pattern (restaurant + date)
CREATE INDEX IF NOT EXISTS idx_google_reviews_restaurant_date
ON google_reviews(restaurant_id, review_date DESC);

-- ============================================================================
-- Directors Table Indexes
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_directors_restaurant
ON company_directors(restaurant_id);

CREATE INDEX IF NOT EXISTS idx_directors_company
ON company_directors(company_number);

-- Composite index for active directors query
CREATE INDEX IF NOT EXISTS idx_directors_restaurant_active
ON company_directors(restaurant_id, resigned_date);

-- ============================================================================
-- Dietary Tags Indexes
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_dietary_tags_item
ON menu_item_dietary_tags(item_id);

CREATE INDEX IF NOT EXISTS idx_dietary_tags_tag
ON menu_item_dietary_tags(tag_id);

-- ============================================================================
-- Verify Indexes Created
-- ============================================================================

SELECT
    'Indexes created:' as status,
    COUNT(*) as total_indexes
FROM sqlite_master
WHERE type = 'index'
AND name LIKE 'idx_%';
