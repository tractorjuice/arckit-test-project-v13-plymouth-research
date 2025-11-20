-- Add Extended FSA Food Hygiene Rating Fields
-- Date: 2025-11-20
-- Purpose: Add additional FSA fields for complete hygiene data capture
--
-- Fields being added:
-- - FSA Business Name (their official name)
-- - Full address (4 address lines + postcode)
-- - GPS coordinates (latitude, longitude)
-- - Local authority reference ID
-- - Rating key (full rating identifier)
-- - Scheme type (FHRS)
-- - Local authority website
-- - New rating pending flag

-- Business Name
ALTER TABLE restaurants ADD COLUMN fsa_business_name TEXT;

-- Address Fields
ALTER TABLE restaurants ADD COLUMN fsa_address_line1 TEXT;
ALTER TABLE restaurants ADD COLUMN fsa_address_line2 TEXT;
ALTER TABLE restaurants ADD COLUMN fsa_address_line3 TEXT;
ALTER TABLE restaurants ADD COLUMN fsa_address_line4 TEXT;
ALTER TABLE restaurants ADD COLUMN fsa_postcode TEXT;

-- GPS Coordinates
ALTER TABLE restaurants ADD COLUMN fsa_latitude REAL;
ALTER TABLE restaurants ADD COLUMN fsa_longitude REAL;

-- Reference & Metadata
ALTER TABLE restaurants ADD COLUMN fsa_local_authority_business_id TEXT;
ALTER TABLE restaurants ADD COLUMN fsa_rating_key TEXT;
ALTER TABLE restaurants ADD COLUMN fsa_scheme_type TEXT;
ALTER TABLE restaurants ADD COLUMN fsa_local_authority_website TEXT;
ALTER TABLE restaurants ADD COLUMN fsa_new_rating_pending TEXT;

-- Create indexes for commonly searched fields
CREATE INDEX IF NOT EXISTS idx_fsa_postcode ON restaurants(fsa_postcode);
CREATE INDEX IF NOT EXISTS idx_fsa_business_name ON restaurants(fsa_business_name);
