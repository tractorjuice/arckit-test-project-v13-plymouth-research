# Data Organization Summary

**Date**: 2025-11-22
**Organized by**: Claude Code
**Total Files Moved**: 125 files

## Overview

All data files have been organized into a proper directory structure following data science best practices. The project root is now clean with only scripts and the database, while all data files are organized by type.

## Directory Structure

```
data/
├── README.md                    # Documentation of data structure
├── raw/                         # Original source data (246 MB)
│   ├── plymouth_fsa_data.xml                    # FSA hygiene data (1.8 MB)
│   ├── plymouth_licensing_complete.json         # Complete licensing data (6.2 MB)
│   ├── plymouth_licensing_complete_fixed.json   # Fixed licensing data (3.1 MB)
│   ├── plymouth_licensing_partial_*.json        # 44 checkpoint files
│   ├── plymouth_licensing_fixed_partial_*.json  # 39 fixed checkpoint files
│   ├── plymouth_licensing_premises_list.json    # Premises list
│   ├── plymouth_business_rates_source.csv       # Business rates source (18 KB)
│   └── restaurant_licensing_data.json           # Restaurant licensing subset
├── processed/                   # Generated/transformed data (1.3 MB)
│   ├── business_rates_matches_all*.csv          # All business rates matches (3 versions)
│   ├── business_rates_matches_confident*.csv    # High-confidence matches (3 versions)
│   ├── business_rates_matches_verified*.csv     # Manually verified (3 versions)
│   ├── business_rates_unmatched*.csv            # Unmatched restaurants (3 versions)
│   ├── fsa_hygiene_matches_all_v2.csv           # All FSA matches v2
│   ├── fsa_hygiene_matches_confident_v2.csv     # High-confidence FSA matches
│   ├── fsa_hygiene_matches_verified_v2.csv      # Manually verified FSA matches
│   ├── fsa_hygiene_unmatched*.csv               # Unmatched FSA (2 versions)
│   ├── licensing_matches_all.csv                # All licensing matches
│   ├── licensing_matches_confident.csv          # High-confidence licensing
│   ├── licensing_matches_verified.csv           # Manually verified licensing
│   ├── licensing_unmatched.csv                  # Unmatched licensing
│   ├── matched_hygiene_ratings.csv              # Matched hygiene summary
│   ├── unmatched_hygiene_ratings.csv            # Unmatched hygiene summary
│   ├── google_without_fsa.csv                   # Google Places without FSA data
│   ├── companies_*.csv                          # Companies House data (3 files)
│   ├── discovered_trustpilot_urls.csv           # Trustpilot URL discovery
│   ├── trustpilot_urls_for_verification.csv     # Trustpilot URLs to verify
│   ├── address_consistency_report.csv           # Address quality analysis
│   ├── balance_sheet_results.csv                # Financial data
│   ├── restaurant_menu_urls.json                # Extracted menu URLs
│   ├── restaurants_extracted.json               # Scraped restaurant data
│   ├── failed_restaurants_for_retry.csv         # Failed scrapes
│   └── unmatched_licensing.json                 # Unmatched licensing (JSON)
├── sample/                      # Test/synthetic data (20 KB)
│   └── synthetic_restaurants_unique.csv         # Generated test data
└── manual_matches/              # Manual verification outputs (144 KB)
    ├── licensing_manual_matches_20251122_130316.csv  # Session 1 (3 matches)
    ├── licensing_manual_matches_20251122_133104.csv  # Session 2
    └── fsa_manual_matches_20251122_134550.csv        # FSA session (10 matches)
```

## File Count by Category

| Category | Files | Size |
|----------|-------|------|
| **raw/** | 86 | 246 MB |
| **processed/** | 35 | 1.3 MB |
| **sample/** | 1 | 20 KB |
| **manual_matches/** | 3 | 144 KB |
| **TOTAL** | **125** | **247 MB** |

## Scripts Updated

The following scripts have been updated to reference the new data paths:

### 1. `interactive_matcher_app.py`
**Changes**:
- Line 86: `licensing_unmatched.csv` → `data/processed/licensing_unmatched.csv`
- Line 88: `business_rates_unmatched.csv` → `data/processed/business_rates_unmatched.csv`
- Line 90: `fsa_hygiene_unmatched.csv` → `data/processed/fsa_hygiene_unmatched.csv`
- Line 123: `plymouth_licensing_complete_fixed.json` → `data/raw/plymouth_licensing_complete_fixed.json`
- Line 126: `plymouth_business_rates_source.csv` → `data/raw/plymouth_business_rates_source.csv`
- Line 132: `plymouth_fsa_data.xml` → `data/raw/plymouth_fsa_data.xml`

**Status**: ✅ Updated, currently running on port 8502

### 2. `fetch_hygiene_ratings_v2.py`
**Changes**:
- Line 243: `plymouth_fsa_data.xml` → `data/raw/plymouth_fsa_data.xml`
- Line 379: `unmatched_hygiene_ratings.csv` → `data/processed/unmatched_hygiene_ratings.csv`
- Line 390: `matched_hygiene_ratings.csv` → `data/processed/matched_hygiene_ratings.csv`

**Status**: ✅ Updated, ready to use

### 3. `.gitignore`
**Changes**:
- Replaced individual file exclusions with directory-level exclusion
- Added `data/` to exclude all data files
- Added `!data/README.md` to keep the README in git

**Status**: ✅ Updated

## Git Status

The `data/` directory is now excluded from git (except for README.md), keeping the repository size manageable while maintaining documentation of the data structure.

### What's Tracked:
- `data/README.md` - Documentation
- All Python scripts
- Database schema files
- Documentation files

### What's Excluded:
- `data/raw/` - Large source files (246 MB)
- `data/processed/` - Generated files (1.3 MB)
- `data/sample/` - Test data
- `data/manual_matches/` - Manual verification outputs

## Benefits

### Before Organization:
- 125 CSV/JSON/XML files scattered in project root
- Difficult to distinguish raw vs processed data
- No clear separation of source vs derived data
- Hard to find specific file types
- Cluttered project root

### After Organization:
- Clean project root with only scripts and database
- Clear separation: `raw/` → `processed/` → `sample/` → `manual_matches/`
- Easy to find source data vs generated data
- Proper data science project structure
- Git-friendly (excludes large data files)
- Easy to backup specific data types
- Clear data lineage and provenance

## Verification

### Project Root Status:
```bash
$ ls -1 *.csv *.json *.xml 2>/dev/null | wc -l
0
```
✅ **Project root is clean** - No loose data files

### Data Directory Status:
```bash
$ tree -L 1 data/
data/
├── README.md
├── manual_matches
├── processed
├── raw
└── sample

5 directories, 1 file
```
✅ **Data organized into 4 categories**

### Script Compatibility:
- `interactive_matcher_app.py` - ✅ Running successfully on port 8502
- `dashboard_app.py` - ✅ Running successfully on port 8501
- `fetch_hygiene_ratings_v2.py` - ✅ Updated, ready to run

## Usage Examples

### Running the Interactive Matcher:
```bash
# The app now loads data from organized directories automatically
streamlit run interactive_matcher_app.py --server.port 8502
```

### Refreshing FSA Hygiene Data:
```bash
# Downloads new data to data/raw/, exports matches to data/processed/
python fetch_hygiene_ratings_v2.py
```

### Accessing Manual Match Files:
```bash
# Import manual matches from organized location
python import_fsa_manual_matches.py data/manual_matches/fsa_manual_matches_20251122_134550.csv
```

### Finding Source Data:
```bash
# All raw source data in one place
ls -lh data/raw/

# All generated matches in one place
ls -lh data/processed/*_matches*.csv

# All unmatched lists in one place
ls -lh data/processed/*_unmatched*.csv
```

## Next Steps

1. **Backup Strategy**: Consider backing up `data/raw/` separately (246 MB of irreplaceable source data)
2. **Archival**: Old versions (v1, v2, etc.) in `data/processed/` can be archived or removed
3. **Documentation**: Update `CLAUDE.md` with references to new data paths
4. **Monitoring**: Set up automated data freshness checks for source files

## Files Created

1. `organize_data.py` - Python script that performed the organization (keeps for future use)
2. `data/README.md` - Documentation of data directory structure
3. `DATA_ORGANIZATION_SUMMARY.md` - This summary document

---

**Organization Script**: `organize_data.py`
**Execution Time**: ~2 seconds
**Errors**: 0
**Status**: ✅ **Complete and Verified**
