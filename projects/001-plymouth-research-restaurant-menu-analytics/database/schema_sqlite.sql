-- Plymouth Research Restaurant Menu Analytics
-- SQLite Schema v1.0 (Development/Demo Version)
-- Generated: 2025-11-17

-- ============================================================================
-- E-001: Restaurant Entity
-- ============================================================================
CREATE TABLE restaurants (
    restaurant_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT,
    postcode TEXT,
    website_url TEXT NOT NULL UNIQUE,
    cuisine_type TEXT,
    price_range TEXT,
    avg_main_price REAL,
    latitude REAL,
    longitude REAL,
    scraped_at TEXT NOT NULL,
    last_updated TEXT NOT NULL,
    is_active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_restaurants_name ON restaurants(name);
CREATE INDEX idx_restaurants_cuisine ON restaurants(cuisine_type);
CREATE INDEX idx_restaurants_postcode ON restaurants(postcode);

-- ============================================================================
-- E-003: Category Reference Data
-- ============================================================================
CREATE TABLE categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT NOT NULL UNIQUE,
    display_order INTEGER,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO categories (category_name, display_order) VALUES
    ('Starters', 1),
    ('Mains', 2),
    ('Desserts', 3),
    ('Drinks', 4),
    ('Sides', 5),
    ('Specials', 6),
    ('Other', 7);

-- ============================================================================
-- E-002: Menu Item Entity
-- ============================================================================
CREATE TABLE menu_items (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    restaurant_id INTEGER NOT NULL REFERENCES restaurants(restaurant_id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    price_gbp REAL,
    category TEXT,
    scraped_at TEXT NOT NULL,
    last_updated TEXT NOT NULL,
    source_html TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_menu_items_restaurant ON menu_items(restaurant_id);
CREATE INDEX idx_menu_items_name ON menu_items(name);
CREATE INDEX idx_menu_items_category ON menu_items(category);
CREATE INDEX idx_menu_items_price ON menu_items(price_gbp);

-- ============================================================================
-- E-004: Dietary Tags Reference Data
-- ============================================================================
CREATE TABLE dietary_tags (
    tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
    tag_name TEXT NOT NULL UNIQUE,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO dietary_tags (tag_name) VALUES
    ('vegan'),
    ('vegetarian'),
    ('gluten-free'),
    ('dairy-free'),
    ('nut-free');

-- ============================================================================
-- E-005: Menu Item Dietary Tags (Junction Table)
-- ============================================================================
CREATE TABLE menu_item_dietary_tags (
    item_id INTEGER NOT NULL REFERENCES menu_items(item_id) ON DELETE CASCADE,
    tag_id INTEGER NOT NULL REFERENCES dietary_tags(tag_id) ON DELETE CASCADE,
    confidence REAL DEFAULT 1.0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (item_id, tag_id)
);

CREATE INDEX idx_menu_item_dietary_tags_item ON menu_item_dietary_tags(item_id);
CREATE INDEX idx_menu_item_dietary_tags_tag ON menu_item_dietary_tags(tag_id);

-- ============================================================================
-- E-006: Scraping Logs (Audit Trail)
-- ============================================================================
CREATE TABLE scraping_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    restaurant_id INTEGER REFERENCES restaurants(restaurant_id) ON DELETE SET NULL,
    url TEXT NOT NULL,
    http_status_code INTEGER,
    robots_txt_allowed INTEGER,
    rate_limit_delay_seconds INTEGER,
    user_agent TEXT,
    success INTEGER,
    error_message TEXT,
    scraped_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_scraping_logs_restaurant ON scraping_logs(restaurant_id);
CREATE INDEX idx_scraping_logs_scraped_at ON scraping_logs(scraped_at);

-- ============================================================================
-- E-009: Opt-Out Exclusion List
-- ============================================================================
CREATE TABLE opt_out_exclusions (
    exclusion_id INTEGER PRIMARY KEY AUTOINCREMENT,
    restaurant_name TEXT,
    website_url TEXT NOT NULL UNIQUE,
    contact_email TEXT,
    opt_out_reason TEXT,
    opted_out_at TEXT DEFAULT CURRENT_TIMESTAMP
);
