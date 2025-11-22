# Plymouth Licensing Database Scraper - Usage Guide

## Overview

Two scrapers available:

1. **`scrape_restaurant_licensing.py`** - Targeted scraper (✅ COMPLETED)
   - Scrapes only the 243 restaurants in our database
   - Fast: ~13 minutes total
   - Result: 42/243 matched (17.3%)

2. **`scrape_plymouth_licensing.py`** - Full scraper (⏳ READY TO RUN)
   - Scrapes ALL 2,232 licensed premises in Plymouth
   - Slow: ~2.5-3.5 hours total
   - Checkpoint system: saves every 50 premises
   - Resume capability: can run in chunks

## Running the Full Scraper

### Quick Start

```bash
# Run the full scraper
python3 scrape_plymouth_licensing.py

# The scraper will:
# 1. Load existing premises list (or scrape it if missing)
# 2. Resume from last checkpoint (or start fresh)
# 3. Save checkpoints every 50 premises
# 4. Save final complete dataset
```

### Checkpoint System

**Automatic Checkpoints**:
- Saves to `plymouth_licensing_partial_50.json`, `plymouth_licensing_partial_100.json`, etc.
- Created every 50 premises (~3-4 minutes)
- Allows safe interruption and resumption

**Resume Behavior**:
- Automatically detects the latest checkpoint file
- Resumes from where it left off
- No need to manually specify resume point

**Example Output**:
```
✓ Found checkpoint: plymouth_licensing_partial_150.json
  Loaded 150 previously scraped premises
  Resuming from index 151/2232
```

### Running in Codespaces

**Problem**: Codespaces times out after ~60 minutes of inactivity

**Solution**: Run in ~45-minute chunks

**How**:
1. Start the scraper: `python3 scrape_plymouth_licensing.py`
2. Let it run for 45 minutes (~600-750 premises)
3. Press `Ctrl+C` to stop gracefully
4. Wait a few minutes (or continue working in another tab)
5. Restart: `python3 scrape_plymouth_licensing.py` (auto-resumes)
6. Repeat until complete (2,232 premises)

**Progress Tracking**:
```
[151/2232] Himalayan Spice (ID: 644)
  → Opening hours: 3 time periods
  → Activities: sale and supply of alcohol

================================================================================
Progress: 200/2232 (9.0%) - 200 premises processed
================================================================================

  ✓ Checkpoint saved: plymouth_licensing_partial_200.json
```

### File Structure

**Input**:
- None (scrapes from Plymouth Council website)

**Intermediate Files** (created during scraping):
- `plymouth_licensing_premises_list.json` - All 2,232 premises (ID, name, address)
- `plymouth_licensing_partial_50.json` - First 50 premises with details
- `plymouth_licensing_partial_100.json` - First 100 premises with details
- ... (continues every 50)

**Final Output**:
- `plymouth_licensing_complete.json` - All 2,232 premises with full details

### Data Structure

Each premises record includes:

```json
{
  "premises_id": "644",
  "name": "Himalayan Spice",
  "address": "31 New Street, Plymouth, Devon, PL1 2NA",
  "scraped_at": "2025-11-20T23:40:15.123456",
  "details": {
    "license_number": "PA0518",
    "license_url": "https://licensing.plymouth.gov.uk/...",
    "license_holder": "Mr Narayan Gautam",
    "dps_name": "Mr Narayan Gautam",
    "licensable_activities": [
      "sale and supply of alcohol"
    ],
    "opening_hours": [
      {
        "days": "Monday to Saturday",
        "time_from": "10:00",
        "time_to": "00:00"
      },
      {
        "days": "Sunday",
        "time_from": "12:00",
        "time_to": "23:30"
      }
    ],
    "activity_hours": [...],
    "conditions": {
      "mandatory": [...],
      "operational": [...],
      "post_hearing": [...]
    },
    "validity_from": "01/01/2005",
    "validity_to": "Indefinite"
  }
}
```

## Estimating Completion Time

**Rate Limiting**: 2 seconds between requests

**Premises Scrape Rate**:
- ~2-3 seconds per premises (includes parsing)
- 50 premises ≈ 2-3 minutes
- 2,232 premises ≈ 2.5-3.5 hours total

**Checkpoint Schedule**:
- Checkpoint 1 (50 premises): ~3 minutes
- Checkpoint 2 (100 premises): ~6 minutes
- Checkpoint 3 (150 premises): ~9 minutes
- ...
- Checkpoint 45 (2,232 premises): ~2.5-3.5 hours

**Codespaces Chunks** (45-minute sessions):
- Chunk 1: Premises 1-750 (45 min)
- Chunk 2: Premises 751-1500 (45 min)
- Chunk 3: Premises 1501-2232 (35 min)

Total: ~2 hours of active runtime across 3 sessions

## Troubleshooting

### Scraper Crashes

**Problem**: Script crashes mid-run

**Solution**: Just restart - it auto-resumes from last checkpoint
```bash
python3 scrape_plymouth_licensing.py
```

### Network Errors

**Problem**: Timeout or connection errors

**Solution**: The scraper has retry logic (3 attempts per request)

If it still fails:
```bash
# Check the last checkpoint
ls -lh plymouth_licensing_partial_*.json | tail -1

# Restart - it will resume
python3 scrape_plymouth_licensing.py
```

### Corrupted Checkpoint

**Problem**: Checkpoint file is corrupted (invalid JSON)

**Solution**: Delete the corrupted checkpoint and restart
```bash
# Delete the last checkpoint
rm plymouth_licensing_partial_2000.json

# Restart - will resume from previous checkpoint (1950)
python3 scrape_plymouth_licensing.py
```

### Fresh Start

**Problem**: Want to start completely fresh

**Solution**: Delete all checkpoint files
```bash
# Delete all checkpoints
rm plymouth_licensing_partial_*.json

# Delete premises list (optional)
rm plymouth_licensing_premises_list.json

# Start fresh
python3 scrape_plymouth_licensing.py
```

## After Scraping Complete

### Step 1: Verify Data
```bash
# Check final file size
ls -lh plymouth_licensing_complete.json

# Count premises
cat plymouth_licensing_complete.json | jq '. | length'

# Should output: 2232
```

### Step 2: Analyze Results
```bash
# Count successful scrapes (with license details)
cat plymouth_licensing_complete.json | jq '[.[] | select(.details.license_number)] | length'

# Count failed scrapes
cat plymouth_licensing_complete.json | jq '[.[] | select(.details.error)] | length'
```

### Step 3: Import to Database

Option 1: Match all 2,232 premises to our restaurants
Option 2: Use existing `import_licensing_data.py` with the targeted data

You'll likely want to create a new import script for the full dataset.

## Data Quality Notes

**Success Rates** (estimated):
- ~95% of premises have current licenses
- ~5% may have errors (closed businesses, license expired, etc.)

**Common Issues**:
- DPS names may contain footer text ("Copyright © Idox...")
- Some premises have no opening hours (24-hour or not specified)
- Activity hours may differ from opening hours

**Data Validation**:
- License numbers follow pattern: PA####
- Premises IDs are integers (1-5000 range)
- Dates are in DD/MM/YYYY format

## Legal & Ethical Notes

**Data Source**: Plymouth City Council Licensing Register (public data)

**Legal**:
- Public sector information licensed under OGL v3.0
- Attribution required: "Data from Plymouth City Council"

**Rate Limiting**:
- 2 seconds between requests (respectful scraping)
- No DDoS risk at this rate
- Total load: ~1-2 requests per second

**Permitted Use**:
- Research and analytics
- Internal business intelligence
- Non-commercial use

## Next Steps After Full Scrape

1. **Match to Restaurants**: Create enhanced matching algorithm
2. **Dashboard Integration**: Add licensing data for all matched restaurants
3. **Coverage Analysis**: Identify restaurant types requiring licenses
4. **Trend Analysis**: Track license renewals, new openings, closures
5. **Compliance Monitoring**: Alert for expired or suspended licenses

---

*Last Updated: 2025-11-20*
*Full Scraper Version: 2.0 (with 50-premise checkpoints)*
