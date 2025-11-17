-- Plymouth Research Restaurant Menu Analytics
-- Database Schema v1.0
-- PostgreSQL 15+
-- Generated: 2025-11-17

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS pg_trgm;  -- For fuzzy text search

-- ============================================================================
-- E-001: Restaurant Entity
-- ============================================================================
CREATE TABLE restaurants (
    restaurant_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT,
    postcode VARCHAR(10),
    website_url TEXT NOT NULL UNIQUE,
    cuisine_type VARCHAR(50),  -- British, Italian, Chinese, etc.
    price_range VARCHAR(20),   -- Budget, Mid-Range, Premium
    avg_main_price NUMERIC(10,2),  -- Calculated from menu items
    latitude NUMERIC(9,6),     -- For future map features
    longitude NUMERIC(9,6),
    scraped_at TIMESTAMP NOT NULL,  -- First scrape timestamp
    last_updated TIMESTAMP NOT NULL,  -- Most recent scrape timestamp
    is_active BOOLEAN DEFAULT TRUE,  -- False if opted out or permanently offline
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_restaurants_name ON restaurants(name);
CREATE INDEX idx_restaurants_cuisine ON restaurants(cuisine_type);
CREATE INDEX idx_restaurants_postcode ON restaurants(postcode);
CREATE INDEX idx_restaurants_active ON restaurants(is_active);

COMMENT ON TABLE restaurants IS 'E-001: Restaurant business entities (150+ Plymouth restaurants)';
COMMENT ON COLUMN restaurants.website_url IS 'Source of truth for scraping (must be unique)';
COMMENT ON COLUMN restaurants.is_active IS 'FALSE if opted out or permanently closed';

-- ============================================================================
-- E-003: Category Reference Data
-- ============================================================================
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL UNIQUE,
    display_order INTEGER,  -- Order in dropdown filters
    created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO categories (category_name, display_order) VALUES
    ('Starters', 1),
    ('Mains', 2),
    ('Desserts', 3),
    ('Drinks', 4),
    ('Sides', 5),
    ('Specials', 6),
    ('Other', 7);

COMMENT ON TABLE categories IS 'E-003: Controlled vocabulary for menu item categories';

-- ============================================================================
-- E-002: Menu Item Entity
-- ============================================================================
CREATE TABLE menu_items (
    item_id SERIAL PRIMARY KEY,
    restaurant_id INTEGER NOT NULL REFERENCES restaurants(restaurant_id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price_gbp NUMERIC(10,2),  -- Normalized to decimal GBP
    category VARCHAR(50),  -- Starters, Mains, Desserts, Drinks, etc.
    scraped_at TIMESTAMP NOT NULL,
    last_updated TIMESTAMP NOT NULL,
    source_html TEXT,  -- Raw HTML snippet for debugging extraction issues
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_menu_items_restaurant ON menu_items(restaurant_id);
CREATE INDEX idx_menu_items_name ON menu_items(name);
CREATE INDEX idx_menu_items_category ON menu_items(category);
CREATE INDEX idx_menu_items_price ON menu_items(price_gbp);
CREATE INDEX idx_menu_items_last_updated ON menu_items(last_updated);

COMMENT ON TABLE menu_items IS 'E-002: Menu item entities with prices and descriptions (10,000+ items)';
COMMENT ON COLUMN menu_items.source_html IS 'Raw HTML for data lineage and debugging';
COMMENT ON COLUMN menu_items.price_gbp IS 'Normalized price (validation: 0.50-150.00 GBP)';

-- ============================================================================
-- E-004: Dietary Tags Reference Data
-- ============================================================================
CREATE TABLE dietary_tags (
    tag_id SERIAL PRIMARY KEY,
    tag_name VARCHAR(50) NOT NULL UNIQUE,  -- vegan, vegetarian, gluten-free, dairy-free, nut-free
    created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO dietary_tags (tag_name) VALUES
    ('vegan'),
    ('vegetarian'),
    ('gluten-free'),
    ('dairy-free'),
    ('nut-free');

COMMENT ON TABLE dietary_tags IS 'E-004: Controlled vocabulary for dietary tags';

-- ============================================================================
-- E-005: Menu Item Dietary Tags (Junction Table)
-- ============================================================================
CREATE TABLE menu_item_dietary_tags (
    item_id INTEGER NOT NULL REFERENCES menu_items(item_id) ON DELETE CASCADE,
    tag_id INTEGER NOT NULL REFERENCES dietary_tags(tag_id) ON DELETE CASCADE,
    confidence NUMERIC(3,2) DEFAULT 1.0,  -- ML confidence score (0.0-1.0)
    created_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (item_id, tag_id)
);

CREATE INDEX idx_menu_item_dietary_tags_item ON menu_item_dietary_tags(item_id);
CREATE INDEX idx_menu_item_dietary_tags_tag ON menu_item_dietary_tags(tag_id);

COMMENT ON TABLE menu_item_dietary_tags IS 'E-005: Many-to-many relationship between menu items and dietary tags';
COMMENT ON COLUMN menu_item_dietary_tags.confidence IS 'ML confidence score for auto-tagged items (1.0 = human verified)';

-- ============================================================================
-- E-006: Scraping Logs (Audit Trail)
-- ============================================================================
CREATE TABLE scraping_logs (
    log_id SERIAL PRIMARY KEY,
    restaurant_id INTEGER REFERENCES restaurants(restaurant_id) ON DELETE SET NULL,
    url TEXT NOT NULL,
    http_status_code INTEGER,  -- 200, 404, 500, etc.
    robots_txt_allowed BOOLEAN,  -- TRUE if robots.txt permitted, FALSE if blocked
    rate_limit_delay_seconds INTEGER,  -- Actual delay before this request (should be ≥5)
    user_agent TEXT,
    success BOOLEAN,  -- TRUE if menu data extracted, FALSE if failed
    error_message TEXT,  -- If failed, what went wrong
    scraped_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_scraping_logs_restaurant ON scraping_logs(restaurant_id);
CREATE INDEX idx_scraping_logs_scraped_at ON scraping_logs(scraped_at);
CREATE INDEX idx_scraping_logs_success ON scraping_logs(success);

COMMENT ON TABLE scraping_logs IS 'E-006: Comprehensive audit trail for ethical scraping compliance';
COMMENT ON COLUMN scraping_logs.robots_txt_allowed IS 'Critical: FALSE indicates compliance violation';
COMMENT ON COLUMN scraping_logs.rate_limit_delay_seconds IS 'Must be ≥5 seconds per Principle 3';

-- ============================================================================
-- E-007: Data Quality Metrics
-- ============================================================================
CREATE TABLE data_quality_metrics (
    metric_id SERIAL PRIMARY KEY,
    metric_date DATE NOT NULL UNIQUE,
    total_restaurants INTEGER,
    total_menu_items INTEGER,
    completeness_pct NUMERIC(5,2),  -- % of items with all required fields populated
    accuracy_pct NUMERIC(5,2),  -- % of items passing manual validation (sampled)
    freshness_avg_days NUMERIC(5,1),  -- Average age of menu data in days
    scraping_success_rate_pct NUMERIC(5,2),  -- % of restaurants successfully scraped
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_data_quality_metrics_date ON data_quality_metrics(metric_date);

COMMENT ON TABLE data_quality_metrics IS 'E-007: Daily data quality snapshots for Goal G-1 (95% accuracy)';

-- ============================================================================
-- E-008: User Feedback (Error Reporting)
-- ============================================================================
CREATE TABLE user_feedback (
    feedback_id SERIAL PRIMARY KEY,
    item_id INTEGER REFERENCES menu_items(item_id) ON DELETE SET NULL,
    restaurant_id INTEGER REFERENCES restaurants(restaurant_id) ON DELETE SET NULL,
    feedback_type VARCHAR(50),  -- "incorrect_price", "wrong_dietary_tag", "stale_data", "other"
    description TEXT,
    user_email VARCHAR(255),  -- Optional if user wants follow-up
    resolved BOOLEAN DEFAULT FALSE,
    resolved_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_user_feedback_resolved ON user_feedback(resolved);
CREATE INDEX idx_user_feedback_created_at ON user_feedback(created_at);
CREATE INDEX idx_user_feedback_type ON user_feedback(feedback_type);

COMMENT ON TABLE user_feedback IS 'E-008: Crowdsourced error reporting for data quality improvement';

-- ============================================================================
-- E-009: Opt-Out Exclusion List
-- ============================================================================
CREATE TABLE opt_out_exclusions (
    exclusion_id SERIAL PRIMARY KEY,
    restaurant_name VARCHAR(255),
    website_url TEXT NOT NULL UNIQUE,
    contact_email VARCHAR(255),
    opt_out_reason TEXT,
    opted_out_at TIMESTAMP DEFAULT NOW()
);

CREATE UNIQUE INDEX idx_opt_out_exclusions_url ON opt_out_exclusions(website_url);

COMMENT ON TABLE opt_out_exclusions IS 'E-009: Permanent exclusion list for restaurants exercising Right to Object';
COMMENT ON COLUMN opt_out_exclusions.website_url IS 'Unique constraint prevents duplicate opt-outs';

-- ============================================================================
-- Triggers for Updated Timestamps
-- ============================================================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_restaurants_updated_at BEFORE UPDATE ON restaurants
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_menu_items_updated_at BEFORE UPDATE ON menu_items
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- Initial Data Quality Metrics Record
-- ============================================================================
INSERT INTO data_quality_metrics (
    metric_date,
    total_restaurants,
    total_menu_items,
    completeness_pct,
    accuracy_pct,
    freshness_avg_days,
    scraping_success_rate_pct
) VALUES (
    CURRENT_DATE,
    0,
    0,
    0.00,
    0.00,
    0.0,
    0.00
);

-- ============================================================================
-- Views for Common Queries
-- ============================================================================

-- Active restaurants with recent menu data
CREATE VIEW active_restaurants_with_menus AS
SELECT
    r.restaurant_id,
    r.name,
    r.cuisine_type,
    r.price_range,
    r.postcode,
    COUNT(mi.item_id) as menu_item_count,
    MAX(mi.last_updated) as latest_menu_update,
    EXTRACT(DAY FROM NOW() - MAX(mi.last_updated)) as days_since_update
FROM restaurants r
LEFT JOIN menu_items mi ON r.restaurant_id = mi.restaurant_id
WHERE r.is_active = TRUE
GROUP BY r.restaurant_id;

COMMENT ON VIEW active_restaurants_with_menus IS 'Active restaurants with menu freshness metrics';

-- ============================================================================
-- Database Setup Complete
-- ============================================================================
COMMENT ON SCHEMA public IS 'Plymouth Research Restaurant Menu Analytics - Schema v1.0';
