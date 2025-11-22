# Interactive Data Matcher - User Guide

**Tool**: `interactive_matcher.py`
**Purpose**: Manually review and select matches for restaurants with missing data
**Created**: 2025-11-22

---

## Overview

The Interactive Matcher helps you manually match restaurants to external datasets when automated matching fails. It shows you each unmatched restaurant alongside the top 5 most likely matches, allowing you to select the correct one or skip.

**Current Gaps** (as of 2025-11-22):
- **Licensing**: 170 unmatched restaurants (70%)
- **Business Rates**: 179 unmatched restaurants (73.7%)
- **FSA Hygiene**: 56 unmatched restaurants (23%)

---

## Quick Start

```bash
# Run the interactive matcher
python interactive_matcher.py

# Select data source:
# 1. Licensing data (170 unmatched)
# 2. Business Rates (179 unmatched)
# 3. FSA Hygiene (56 unmatched)
```

---

## How It Works

### 1. Restaurant Display

For each unmatched restaurant, you'll see:
```
================================================================================
Restaurant 1/170
================================================================================
ID: 2
Name: Fletcher's Restaurant
Address: 3 The Barbican, Plymouth
Postcode: PL1 2LR
```

### 2. Top 5 Matches

The tool shows 5 potential matches ranked by similarity score:
```
Top 5 Potential Matches:
--------------------------------------------------------------------------------

[1] Score: 85.5
    Name: Fletcher's
    Address: 3 The Barbican Plymouth PL1 2LR
    Match: name=95%, postcode=✓, address=20
    License: PA0256
    Activities: sale and supply of alcohol, live music

[2] Score: 62.3
    Name: Fletcher & Sons Ltd
    Address: 12 High Street Plymouth PL4 8AA
    Match: name=78%, postcode=✗, address=10
    License: PA1234
    Activities: sale and supply of alcohol

[3] Score: 45.0
    ...
```

**Score Components**:
- **Name Similarity**: 0-50 points (normalized name matching)
- **Postcode Match**: 30 points (exact match)
- **Address Similarity**: 0-20 points (word overlap)
- **Total Score**: Sum of components (0-100)

**Score Interpretation**:
- ≥90: Very High confidence (likely correct)
- 80-89: High confidence (probable match)
- 70-79: Medium confidence (possible match)
- 60-69: Low confidence (review carefully)
- <60: Very low confidence (unlikely match)

### 3. Make Your Choice

```
================================================================================
Options:
  1-5: Select match
  s: Skip this restaurant
  q: Quit and save progress
  n: None of these match

Your choice:
```

**Controls**:
- **1-5**: Select the corresponding match (saves to verified matches)
- **s** or **n**: Skip this restaurant (saves to skipped list)
- **q**: Quit and save current progress (can resume later)

---

## Output Files

After each session, the tool creates timestamped CSV files:

### Verified Matches

**Licensing**:
- `licensing_manual_matches_YYYYMMDD_HHMMSS.csv`
- Contains: restaurant_id, premises_id, license_number, opening_hours, etc.

**Business Rates**:
- `business_rates_manual_matches_YYYYMMDD_HHMMSS.csv`
- Contains: restaurant_id, rateable_value, category, etc.

**FSA Hygiene**:
- `fsa_manual_matches_YYYYMMDD_HHMMSS.csv`
- Contains: restaurant_id, hygiene_rating, inspection_date, etc.

### Skipped Restaurants

- `{data_source}_manual_skipped_YYYYMMDD_HHMMSS.csv`
- Restaurants you skipped (for future review)

---

## Importing Verified Matches

After verifying matches, import them to the database:

### Licensing Matches

```bash
# Option 1: Use existing import script (modify to accept CSV path)
python import_licensing_matches.py

# Option 2: Create custom import script
python import_manual_licensing_matches.py licensing_manual_matches_20251122_120000.csv
```

### Business Rates Matches

```bash
# Import business rates matches
python import_manual_business_rates.py business_rates_manual_matches_20251122_120000.csv
```

### FSA Hygiene Matches

```bash
# Import FSA hygiene matches
python import_manual_fsa_matches.py fsa_manual_matches_20251122_120000.csv
```

---

## Tips for Effective Matching

### 1. Name Variations to Watch For

**Corporate Entities**:
- "The Rockfish" vs "Rockfish (Plymouth) Limited"
- "Zizzi Plymouth" vs "Azzurri Central Limited"
- "Wagamama" vs "Wagamama Limited"

**Location Suffixes**:
- "Nando's Plymouth" vs "Nando's Restaurant"
- "Costa Plymouth Drake Circus" vs "Costa Coffee"

**Abbreviations**:
- "Wetherspoons - The Gipsy Moth" vs "J D Wetherspoon PLC"
- "ASK Italian" vs "ASK"

### 2. Using Additional Context

Beyond the similarity score, consider:

**Address Matches**:
- Street name matches are strong indicators
- Building numbers should align
- Postcode is most reliable (when available)

**Business Type**:
- Licensing activities should match restaurant type
  - Restaurant → "sale and supply of alcohol"
  - Pub → "sale of alcohol", "live music", "late night"
  - Cafe → may have no license or basic license
- Business rates category should match
  - "Restaurant and Premises" (correct)
  - "Office and Premises" (wrong)

**Rateable Value**:
- Should be reasonable for restaurant size
- Chain restaurants: £30,000-£100,000
- Independent restaurants: £15,000-£50,000
- Small cafes: £5,000-£20,000

### 3. When to Skip

Skip a restaurant if:
- **No clear match**: All scores <60 with no address alignment
- **Conflicting data**: Name matches but address completely different
- **Wrong business type**: Office/retail matched to restaurant
- **Temporary closure**: Restaurant closed but license still active
- **Uncertainty**: Not confident enough to commit

You can always come back to skipped restaurants in a later session.

### 4. Batch Processing Strategy

**Prioritize by Value**:
1. Start with high-traffic restaurants (chains, popular venues)
2. Focus on restaurants with multiple missing datasets
3. Leave difficult matches for last

**Session Length**:
- Aim for 20-30 matches per session (~15-20 minutes)
- Use `q` to save progress and take breaks
- Resume with same data source to continue

---

## Workflow Example

### Session 1: Licensing Data (30 restaurants)

```bash
$ python interactive_matcher.py
Select data source: 1 (Licensing)

# Review 30 restaurants
# Select 18 matches
# Skip 12 uncertain matches
# Press 'q' to quit

✓ Saved 18 verified matches to licensing_manual_matches_20251122_100000.csv
✓ Saved 12 skipped restaurants to licensing_manual_skipped_20251122_100000.csv
```

### Session 2: Review and Import

```bash
# Review the CSV in Excel/VSCode
$ code licensing_manual_matches_20251122_100000.csv

# Import verified matches
$ python import_manual_licensing_matches.py licensing_manual_matches_20251122_100000.csv

✓ Imported 18 matches successfully
Total restaurants with licensing data: 102/243 (42.0%)
```

### Session 3: Continue Matching

```bash
$ python interactive_matcher.py
Select data source: 1 (Licensing)

# Continue from restaurant 31
# Review another 30 restaurants...
```

---

## Expected Impact

### Licensing Data

**Current**: 84/243 (34.6%)
**Remaining**: 170 unmatched (potential +70%)

**If you manually match 50 restaurants**:
- New coverage: 134/243 (55.1%)
- Improvement: +20.5% coverage

**If you manually match 100 restaurants**:
- New coverage: 184/243 (75.7%)
- Improvement: +41.1% coverage

### Business Rates

**Current**: 64/243 (26.3%)
**Remaining**: 179 unmatched (potential +73.7%)

**If you manually match 50 restaurants**:
- New coverage: 114/243 (46.9%)
- Improvement: +20.6% coverage

**If you manually match 100 restaurants**:
- New coverage: 164/243 (67.5%)
- Improvement: +41.2% coverage

### FSA Hygiene

**Current**: 187/243 (77.0%)
**Remaining**: 56 unmatched (potential +23%)

**If you manually match all 56 restaurants**:
- New coverage: 243/243 (100%!)
- Improvement: +23% coverage

---

## Advanced Features

### Custom Filtering

Modify the script to filter by:
- Cuisine type (focus on specific cuisines)
- Price range (prioritize premium restaurants)
- Review count (high-traffic venues first)

### Batch Import

Process multiple manual match files at once:
```bash
for file in licensing_manual_matches_*.csv; do
    python import_manual_licensing_matches.py "$file"
done
```

### Quality Control

After importing, verify matches:
```sql
-- Check manual matches
SELECT
    restaurant_id,
    name,
    licensing_match_confidence,
    licensing_premises_name
FROM restaurants
WHERE licensing_match_confidence BETWEEN 0 AND 100
  AND licensing_premises_id IS NOT NULL
ORDER BY licensing_match_confidence DESC;
```

---

## Troubleshooting

### Issue: Tool crashes on startup

**Cause**: Missing CSV files
**Fix**: Ensure all required CSV files exist:
- `licensing_unmatched.csv`
- `business_rates_unmatched_v3.csv`
- `fsa_hygiene_unmatched_v2.csv`
- `plymouth_licensing_complete_fixed.json`
- `plymouth_business_rates_2025.csv`

### Issue: No matches showing

**Cause**: Data source file missing or empty
**Fix**: Check that source data files are populated

### Issue: Can't resume session

**Current Limitation**: Each session starts from the beginning
**Workaround**:
1. Import your verified matches
2. Re-run the matcher (will only show remaining unmatched)

---

## Future Enhancements

Potential improvements:
1. **Web UI**: Streamlit-based interface with better UX
2. **Resume Support**: Save progress mid-session, resume exactly where you left off
3. **Bulk Operations**: Mark multiple restaurants at once
4. **AI Suggestions**: Use LLM to recommend matches based on context
5. **Photo Verification**: Show Google Maps photos for visual confirmation
6. **Undo/Edit**: Go back and change previous selections

---

## Summary

The Interactive Matcher is a powerful tool for closing data gaps through manual verification:

✅ **Shows top 5 matches** with similarity scoring
✅ **Easy controls** (1-5 to select, s to skip, q to quit)
✅ **Saves progress** to timestamped CSV files
✅ **Supports 3 data sources** (licensing, business rates, FSA hygiene)
✅ **Resumable workflow** (import and continue)

**Estimated time**:
- ~30 seconds per restaurant
- 20 restaurants in ~10 minutes
- 100 restaurants in ~50 minutes

**Recommended workflow**:
1. Start with **FSA Hygiene** (only 56 unmatched, can achieve 100%!)
2. Then **Licensing** (170 unmatched, aim for 50-100)
3. Finally **Business Rates** (179 unmatched, focus on high-value targets)

---

*Guide Created: 2025-11-22*
*Tool Version: 1.0*
