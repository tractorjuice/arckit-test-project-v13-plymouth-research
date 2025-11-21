-- Add Plymouth Licensing Act columns to restaurants table
-- Data source: Plymouth City Council Licensing Register
-- https://licensing.plymouth.gov.uk

-- Add licensing columns
ALTER TABLE restaurants ADD COLUMN licensing_premises_id TEXT;
ALTER TABLE restaurants ADD COLUMN licensing_premises_name TEXT;
ALTER TABLE restaurants ADD COLUMN licensing_premises_address TEXT;
ALTER TABLE restaurants ADD COLUMN licensing_number TEXT;
ALTER TABLE restaurants ADD COLUMN licensing_url TEXT;
ALTER TABLE restaurants ADD COLUMN licensing_dps_name TEXT;
ALTER TABLE restaurants ADD COLUMN licensing_activities TEXT; -- JSON array of licensable activities
ALTER TABLE restaurants ADD COLUMN licensing_opening_hours TEXT; -- JSON array of opening hours
ALTER TABLE restaurants ADD COLUMN licensing_scraped_at TEXT; -- ISO8601 timestamp
ALTER TABLE restaurants ADD COLUMN licensing_match_confidence REAL; -- 0.0-1.0

-- Create index for faster lookups
CREATE INDEX IF NOT EXISTS idx_licensing_premises_id ON restaurants(licensing_premises_id);
CREATE INDEX IF NOT EXISTS idx_licensing_number ON restaurants(licensing_number);

-- Add comments (SQLite doesn't support COMMENT but we document here)
-- licensing_premises_id: Plymouth City Council premises ID (e.g., "644")
-- licensing_premises_name: Official name in licensing database
-- licensing_premises_address: Official address from licensing register
-- licensing_number: License number (e.g., "PA0518")
-- licensing_url: Full URL to license details page
-- licensing_dps_name: Designated Premises Supervisor name
-- licensing_activities: JSON array of licensable activities ["sale and supply of alcohol", ...]
-- licensing_opening_hours: JSON array of opening hours [{"days": "Monday to Saturday", "time_from": "10:00", "time_to": "00:00"}, ...]
-- licensing_scraped_at: When data was scraped (ISO8601)
-- licensing_match_confidence: How confident the automatic match was (1.0 = exact name match)
