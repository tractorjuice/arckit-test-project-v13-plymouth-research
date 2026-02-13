-- Migration: Create drinks table (E-005 from data model ARC-001-DATA-v1.0)
-- Beverage menu items stored separately for distinct categorization

CREATE TABLE IF NOT EXISTS drinks (
    drink_id INTEGER PRIMARY KEY AUTOINCREMENT,
    restaurant_id INTEGER NOT NULL REFERENCES restaurants(restaurant_id) ON DELETE CASCADE,
    drink_name TEXT NOT NULL CHECK(length(drink_name) >= 2),
    category TEXT,  -- Beer, Wine, Cocktails, Spirits, Soft Drinks, Hot Drinks
    price REAL,     -- Price in GBP
    description TEXT,
    scraped_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_drinks_restaurant_id ON drinks(restaurant_id);
CREATE INDEX IF NOT EXISTS idx_drinks_category ON drinks(category);
