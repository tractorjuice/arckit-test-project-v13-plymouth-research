-- Business Rates Schema for Plymouth Research
-- Adds business rates columns to restaurants table
-- Date: 2025-11-21

-- Add business rates columns
ALTER TABLE restaurants ADD COLUMN business_rates_propref TEXT;
ALTER TABLE restaurants ADD COLUMN business_rates_account_holder TEXT;
ALTER TABLE restaurants ADD COLUMN business_rates_address TEXT;
ALTER TABLE restaurants ADD COLUMN business_rates_postcode TEXT;
ALTER TABLE restaurants ADD COLUMN business_rates_rateable_value INTEGER;
ALTER TABLE restaurants ADD COLUMN business_rates_net_charge REAL;
ALTER TABLE restaurants ADD COLUMN business_rates_category TEXT;
ALTER TABLE restaurants ADD COLUMN business_rates_vo_description TEXT;
ALTER TABLE restaurants ADD COLUMN business_rates_match_score REAL;
ALTER TABLE restaurants ADD COLUMN business_rates_match_reason TEXT;
ALTER TABLE restaurants ADD COLUMN business_rates_matched_at TEXT;

-- Create index for queries
CREATE INDEX IF NOT EXISTS idx_restaurants_business_rates_propref
ON restaurants(business_rates_propref);

CREATE INDEX IF NOT EXISTS idx_restaurants_rateable_value
ON restaurants(business_rates_rateable_value);

-- Comments (stored as table metadata)
-- business_rates_propref: Unique property reference from business rates register
-- business_rates_account_holder: Business name from rates register
-- business_rates_address: Full address from rates register
-- business_rates_postcode: Postcode from rates register
-- business_rates_rateable_value: Rateable value (property valuation for business rates calculation)
-- business_rates_net_charge: Annual business rates charge for 2025-26
-- business_rates_category: Standard Classification of Assessee Type (Scat)
-- business_rates_vo_description: Valuation Office description of property
-- business_rates_match_score: Confidence score for matching (0-100)
-- business_rates_match_reason: Explanation of matching logic
-- business_rates_matched_at: ISO8601 timestamp when match was made
