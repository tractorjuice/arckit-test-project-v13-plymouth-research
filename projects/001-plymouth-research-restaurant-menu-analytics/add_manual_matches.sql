-- Migration: Create manual_matches table (E-008 from data model ARC-001-DATA-v1.0)
-- Records of manual and automated matching between restaurants and external data sources

CREATE TABLE IF NOT EXISTS manual_matches (
    match_id INTEGER PRIMARY KEY AUTOINCREMENT,
    restaurant_id INTEGER NOT NULL REFERENCES restaurants(restaurant_id) ON DELETE CASCADE,
    match_type TEXT NOT NULL CHECK(match_type IN ('fsa_hygiene', 'licensing', 'business_rates', 'companies_house', 'trustpilot')),
    external_id TEXT,                    -- ID in external system
    external_name TEXT,                  -- Name in external system
    confidence_score REAL CHECK(confidence_score >= 0.0 AND confidence_score <= 100.0),
    matched_by TEXT NOT NULL CHECK(matched_by IN ('auto', 'manual', 'interactive')),
    matched_at TEXT NOT NULL,            -- ISO 8601 timestamp
    verified_by TEXT,                    -- Reviewer name
    notes TEXT                           -- Match notes
);

CREATE INDEX IF NOT EXISTS idx_mm_restaurant_id ON manual_matches(restaurant_id);
CREATE INDEX IF NOT EXISTS idx_mm_match_type ON manual_matches(match_type);
CREATE INDEX IF NOT EXISTS idx_mm_matched_by ON manual_matches(matched_by);
