-- Add hygiene rating columns to restaurants table
-- Food Standards Agency (FSA) Food Hygiene Rating Scheme (FHRS)

-- Main hygiene rating (0-5 stars)
ALTER TABLE restaurants ADD COLUMN hygiene_rating INTEGER;

-- Date the rating was given by FSA
ALTER TABLE restaurants ADD COLUMN hygiene_rating_date TEXT;

-- FSA establishment ID for tracking
ALTER TABLE restaurants ADD COLUMN fsa_id INTEGER;

-- When we fetched the data from FSA API
ALTER TABLE restaurants ADD COLUMN hygiene_rating_fetched_at TEXT;

-- Detailed breakdown scores (lower is better: 0 = excellent)
ALTER TABLE restaurants ADD COLUMN hygiene_score_hygiene INTEGER;
ALTER TABLE restaurants ADD COLUMN hygiene_score_structural INTEGER;
ALTER TABLE restaurants ADD COLUMN hygiene_score_confidence INTEGER;

-- FSA business type (e.g., "Restaurant/Cafe/Canteen")
ALTER TABLE restaurants ADD COLUMN fsa_business_type TEXT;

-- Local authority details
ALTER TABLE restaurants ADD COLUMN fsa_local_authority TEXT;

-- Create index for faster hygiene rating queries
CREATE INDEX IF NOT EXISTS idx_restaurants_hygiene_rating ON restaurants(hygiene_rating);
