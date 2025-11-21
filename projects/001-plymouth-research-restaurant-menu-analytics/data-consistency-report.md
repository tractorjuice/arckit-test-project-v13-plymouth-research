# Plymouth Research Data Consistency Report

**Generated**: 2025-11-21
**Total Active Restaurants**: 243

---

## Executive Summary

### Current Data Coverage

| Data Source | Coverage | Count | Status |
|-------------|----------|-------|--------|
| **Google Places** | 100.0% | 243/243 | ✅ Complete |
| **FSA Hygiene** | 75.3% | 183/243 | 🟡 Good |
| **Trustpilot Reviews** | 26.7% | 65/243 | 🟠 Moderate |
| **Licensing Data** | 17.3% | 42/243 | 🔴 Low |
| **Business Rates** | 16.9% | 41/243 | 🔴 Low |

### Key Findings

✅ **Good News**:
- All postcodes are **100% consistent** across datasets (no conflicts)
- Google Places has complete 100% coverage (all 243 restaurants)
- FSA Hygiene coverage is strong at 75% (183 restaurants)
- Zero restaurants have zero external data (all have at least Google)

⚠️ **Challenges**:
- **No restaurants** have all 5 data sources
- Business Rates and Licensing coverage is low (~17%)
- 157 restaurants (65%) have name variations across datasets
- Name matching failures due to corporate names (LTD, PLC) vs brand names

🎯 **Opportunities**:
- **15 restaurants** have 4/5 data sources (easy wins!)
- **151 restaurants** with FSA postcodes but no business rates
- **77 restaurants** with 3/5 data sources (good candidates)

---

## 1. Data Completeness Matrix

### Distribution by Data Source Count

| Sources | Restaurants | Percentage |
|---------|-------------|------------|
| 4/5 | 15 | 6.2% |
| 3/5 | 77 | 31.7% |
| 2/5 | 132 | 54.3% |
| 1/5 | 19 | 7.8% |
| 0/5 | 0 | 0.0% |

### Most Common Combinations

| FSA | Business Rates | Licensing | Trustpilot | Google | Count |
|-----|----------------|-----------|------------|--------|-------|
| ✓ | ✗ | ✗ | ✗ | ✓ | 95 |
| ✗ | ✗ | ✗ | ✓ | ✓ | 32 |
| ✓ | ✗ | ✓ | ✗ | ✓ | 29 |
| ✓ | ✓ | ✗ | ✗ | ✓ | 23 |
| ✓ | ✗ | ✗ | ✓ | ✓ | 21 |

---

## 2. High-Value Matching Opportunities

### Restaurants with 4/5 Data Sources (15 total)

These are **golden opportunities** - only 1 data source missing:

#### Missing Licensing Only (6 restaurants)
1. **Rockfish Plymouth** (ID 4) - Postcode: PL4 0LB
   - Has: FSA (5★), Business Rates (£55k), Trustpilot (75 reviews), Google ✓

2. **Honky Tonk Wine Library** (ID 7) - Postcode: PL4 0BJ
   - Has: FSA (N/A), Business Rates (£19k), Trustpilot (4 reviews), Google ✓

3. **Wagamama Plymouth** (ID 16) - Postcode: PL1 3QQ
   - Has: FSA (5★), Business Rates (£111k), Trustpilot (336 reviews), Google ✓

4. **Pizza Express Plymouth** (ID 46) - Postcode: PL1 2SW
   - Has: FSA (5★), Business Rates (£48k), Trustpilot (71 reviews), Google ✓

5. **Turtle Bay Plymouth** (ID 80) - Postcode: PL1 1AB
   - Has: FSA (5★), Business Rates (£97k), Trustpilot (296 reviews), Google ✓

6. **Five Guys Plymouth** (ID 194) - Postcode: PL4 0FE
   - Has: FSA (5★), Business Rates (£71k), Trustpilot (54 reviews), Google ✓

#### Missing Business Rates Only (2 restaurants)
7. **Subway Plymouth** (ID 34) - Postcode: PL1 2SN
   - Has: FSA (5★), Licensing (✓), Trustpilot (9 reviews), Google ✓

8. **Seco Lounge** (ID 157) - Postcode: PL1 3RP
   - Has: FSA (5★), Licensing (✓), Trustpilot (210 reviews), Google ✓

#### Missing Trustpilot Only (7 restaurants)
9. **Cosmic Kitchen** (ID 231) - Postcode: PL1 2AY
   - Has: FSA (5★), Business Rates (£16k), Licensing (✓), Google ✓

10. **KYOWA** (ID 256) - Postcode: PL4 9AF
    - Has: FSA (5★), Business Rates (£6.5k), Licensing (✓), Google ✓

11. **Coffee#1 Plymouth** (ID 301) - Postcode: PL1 1NW
    - Has: FSA (5★), Business Rates (£65k), Licensing (✓), Google ✓

12. **Tigermilk** (ID 314) - Postcode: PL1 2SW
    - Has: FSA (4★), Business Rates (£26k), Licensing (✓), Google ✓

13. **Minerva Inn** (ID 339) - Postcode: PL4 0EA
    - Has: FSA (5★), Business Rates (£8.5k), Licensing (✓), Google ✓

14. **Dolphin Hotel** (ID 340) - Postcode: PL1 2LS
    - Has: FSA (5★), Business Rates (£53k), Licensing (✓), Google ✓

15. **Lord High Admiral** (ID 348) - Postcode: PL1 3PE
    - Has: FSA (5★), Business Rates (£11k), Licensing (✓), Google ✓

---

## 3. Name Variation Analysis

### Summary

- **157 restaurants (65%)** have different names across datasets
- **31 companies** use "LTD" or "LIMITED" suffix in business rates
- **4 companies** use "PLC" suffix
- **151 restaurants** have different FSA business names vs our database name

### Common Patterns

| Pattern | Count | Impact |
|---------|-------|--------|
| Corporate suffixes (LTD/LIMITED) | 31 | Match failures for business rates |
| Corporate suffixes (PLC) | 4 | Match failures for business rates |
| Location suffix (e.g., "Plymouth") | 49 | Inconsistent naming |
| FSA name variations | 151 | FSA matcher missing variations |
| Business rates name variations | 41 | Corporate vs brand names |
| Licensing name variations | 28 | Premises vs trading names |

### Example Name Variations

| Our Database | FSA Name | Business Rates Name |
|--------------|----------|---------------------|
| Rockfish Plymouth | Rockfish Plymouth | ROCKFISH (PLYMOUTH) LIMITED |
| Barbican Kitchen (Original) | Barbican Kitchen Brasserie | THE BARBICAN KITCHEN LTD |
| Honky Tonk Wine Library | HonkyTonk Wine Library | HONKYTONK WINE LIBRARY LIMITED |
| Wagamama Plymouth | Wagamama | WAGAMAMA LIMITED |
| Las Iguanas Plymouth | N/A | IGUANAS HOLDINGS LIMITED |
| Zizzi Plymouth | N/A | AZZURRI CENTRAL LIMITED |
| Boston Tea Party Plymouth | Boston Tea Party | BOSTON TEA PARTY GROUP LTD |
| Pizza Express Plymouth | Pizza Express | PIZZA EXPRESS PLC |
| Domino's Pizza Plymouth | N/A | DOMINO'S PIZZA WEST COUNTRY |
| Fletcher's Restaurant | Platters Restaurant | N/A |

**Key Issue**: Fletcher's Restaurant vs "Platters Restaurant" in FSA data suggests a business name change or different trading name.

---

## 4. Postcode Consistency

### Analysis Result: ✅ PERFECT

- **0 inconsistencies** found across all datasets
- FSA postcodes match business rates postcodes 100%
- No conflicts between licensing and other sources
- All postcodes are normalized correctly

**Conclusion**: Postcode can be trusted as a reliable matching key.

---

## 5. Matching Opportunities by Category

### A. Business Rates Matching (151 opportunities)

Restaurants with **FSA postcodes** but **no business rates data**:

**Top 10 Candidates**:
1. Knead Pizza Plymouth (PL1 2AE) - Has FSA 5★
2. Fletcher's Restaurant (PL1 2LS) - Has FSA 5★
3. Pier One (PL1 3DE) - Has FSA 5★
4. The Village Restaurant (PL1 2LE) - Has FSA 4★
5. Armado Lounge (PL1 2LS) - Has FSA 5★
6. Àclèaf at Boringdon Hall (PL7 4DP) - Has FSA 5★
7. Miller & Carter Plymouth (PL4 0DW) - Has FSA 5★
8. Jolly Jacks (PL1 4LS) - Has FSA 5★
9. McDonald's Plymouth (PL9 7BH) - Has FSA 5★
10. KFC Plymouth (PL4 6JG) - Has FSA 5★

**Action**: Re-run business rates matcher with:
- Lower confidence threshold (60% instead of 70%)
- Add corporate suffix removal (strip LTD, LIMITED, PLC)
- Add location suffix removal (strip "Plymouth", "UK")
- Manual review of top 20 candidates

### B. FSA Hygiene Matching (60 opportunities)

Restaurants with **no hygiene rating** (60 total):

**Possible Causes**:
1. New restaurants not yet inspected
2. Name variations preventing match
3. Registered under different business name
4. Outside Plymouth city authority boundary
5. Not classified as food establishment

**Action**:
- Check if these are in FSA Plymouth XML under different names
- Cross-reference with licensing addresses
- Manual review of unmatched FSA establishments

### C. Licensing Matching (201 opportunities)

Restaurants with **no licensing data** (201 total):

**Note**: Licensing scraper is still running (1,350/2,232 premises scraped, 60% complete)

**Current Status**:
- 42 restaurants matched so far
- Estimated 50-100 more matches expected when scraping completes
- Known issue: DPS name extraction bug was fixed, needs re-scraping

**Action**:
- Wait for licensing scraper to complete (ETA: ~1 hour)
- Re-run matching with completed dataset
- Focus on high-value targets with 4/5 data sources first

### D. Trustpilot Discovery (178 opportunities)

Restaurants with **no Trustpilot data** (178 total):

**Analysis**:
- 65 restaurants currently have Trustpilot URLs (26.7%)
- Many restaurants may not have Trustpilot pages
- Small independent restaurants less likely to be reviewed

**Action**:
- Run Trustpilot URL discovery script for unmatched restaurants
- Focus on chains and popular restaurants first
- Accept that some restaurants genuinely have no Trustpilot presence

---

## 6. Recommendations

### Priority 1: Quick Wins (This Week)

1. **Complete 15 Restaurants with 4/5 Sources** 🎯
   - Run targeted licensing scraper for 6 specific restaurants
   - Search Trustpilot manually for 7 specific restaurants
   - Research business rates for 2 specific restaurants
   - **Impact**: Achieve 15 restaurants with complete data coverage

2. **Improve Business Rates Matcher** 📊
   - Add corporate suffix removal ("LTD", "LIMITED", "PLC")
   - Add location suffix removal ("Plymouth", "UK")
   - Lower confidence threshold from 70% to 60%
   - **Impact**: Expect +20-30 additional matches (from 41 to 60-70)

3. **Fix Name Variations** 📝
   - Create name normalization function (remove suffixes, trim)
   - Apply to all matchers (FSA, Business Rates, Licensing)
   - **Impact**: Improve match rates across all datasets by 10-15%

### Priority 2: Data Quality (Next 2 Weeks)

4. **Complete Licensing Scraper** ⏳
   - Wait for current scraper to finish (60% → 100%)
   - Re-run matching with full dataset
   - **Impact**: Expect 50-100 total licensing matches (from 42 to 90-140)

5. **Manual Review of Top 20 Mismatches** 🔍
   - Review Fletcher's Restaurant (FSA shows "Platters Restaurant")
   - Verify corporate name changes (Zizzi → Azzurri Central, etc.)
   - Update database with correct names
   - **Impact**: Fix data quality issues, improve future matching

6. **FSA Re-matching with Name Variations** 🏥
   - Re-run FSA matcher with improved name normalization
   - Cross-reference with licensing addresses for verification
   - **Impact**: Increase FSA coverage from 75% to 80-85%

### Priority 3: Long-Term Improvements (Next Month)

7. **Implement Fuzzy Matching Library** 🔧
   - Replace simple SequenceMatcher with RapidFuzz
   - Add phonetic matching (Soundex, Metaphone)
   - **Impact**: Better handling of typos and variations

8. **Create Master Name Registry** 📚
   - Document all known name variations per restaurant
   - Build alias table: restaurant_id → [alias1, alias2, ...]
   - Use for future matching operations
   - **Impact**: Prevent future match failures

9. **Automated Data Refresh Pipeline** 🔄
   - Schedule weekly FSA hygiene refresh
   - Schedule monthly business rates check
   - Schedule monthly Trustpilot review updates
   - **Impact**: Keep data fresh and up-to-date

### Priority 4: Advanced Analytics (Future)

10. **Cross-Dataset Validation** ✅
    - Flag restaurants with conflicting data (e.g., closed in Google, active in licensing)
    - Identify anomalies (e.g., high hygiene but terrible reviews)
    - **Impact**: Improve data trustworthiness

11. **Coverage Heatmap** 🗺️
    - Create geographic visualization of data coverage
    - Identify areas with poor coverage
    - Target scraping efforts geographically
    - **Impact**: Systematic approach to filling gaps

12. **Predictive Matching** 🤖
    - Use ML to predict which unmatched restaurants are likely the same
    - Train on verified matches
    - **Impact**: Reduce manual review effort

---

## 7. Success Metrics

### Current State
- **Gold Standard (5/5 sources)**: 0 restaurants (0%)
- **Near-Complete (4/5 sources)**: 15 restaurants (6.2%)
- **Partial (3/5 sources)**: 77 restaurants (31.7%)
- **Minimal (1-2/5 sources)**: 151 restaurants (62.1%)

### Target State (1 Month)
- **Gold Standard (5/5 sources)**: 15+ restaurants (6%+)
- **Near-Complete (4/5 sources)**: 50+ restaurants (20%+)
- **Partial (3/5 sources)**: 100+ restaurants (40%+)
- **Minimal (1-2/5 sources)**: <80 restaurants (<35%)

### Coverage Targets
| Data Source | Current | 1 Month Target | 3 Month Target |
|-------------|---------|----------------|----------------|
| Google Places | 100% | 100% | 100% |
| FSA Hygiene | 75% | 85% | 90% |
| Business Rates | 17% | 30% | 40% |
| Licensing | 17% | 50% | 75% |
| Trustpilot | 27% | 35% | 45% |

---

## 8. Technical Implementation Notes

### Name Normalization Function

```python
import re

def normalize_business_name(name):
    """Normalize business name for matching."""
    if not name:
        return ""

    name = str(name).upper().strip()

    # Remove corporate suffixes
    name = re.sub(r'\s+(LTD|LIMITED|PLC|HOLDINGS?)\s*$', '', name)

    # Remove location suffixes
    name = re.sub(r'\s+\(PLYMOUTH\)|\s+PLYMOUTH\s*$', '', name)

    # Remove punctuation
    name = re.sub(r'[^\w\s]', '', name)

    # Normalize whitespace
    name = re.sub(r'\s+', ' ', name).strip()

    return name
```

### Improved Matcher Pseudocode

```
FOR each unmatched restaurant:
    normalized_name = normalize_business_name(restaurant.name)
    postcode = normalize_postcode(restaurant.postcode)

    FOR each external_record:
        external_name = normalize_business_name(external_record.name)
        external_postcode = normalize_postcode(external_record.postcode)

        # Calculate match score
        name_score = fuzzy_match(normalized_name, external_name)  # 0-100
        postcode_bonus = 30 if postcode == external_postcode else 0
        address_bonus = count_common_words(addresses) * 5  # 0-30

        total_score = name_score + postcode_bonus + address_bonus

        IF total_score >= 60:  # Lowered from 70
            record_as_potential_match(restaurant, external_record, total_score)
```

---

## 9. Appendix: Data Source Details

### FSA Food Hygiene Rating Scheme
- **Source**: https://ratings.food.gov.uk/
- **Format**: XML (Plymouth: FHRS891en-GB.xml)
- **Update Frequency**: Weekly
- **Authority**: Plymouth City Council (Code 891)
- **Current Extract**: 2025-11-15
- **Coverage**: 1,841 establishments (443 restaurants/cafes)

### Plymouth Business Rates Register
- **Source**: Monthly-Business-Rates-November-2025.xlsx
- **Format**: Excel spreadsheet
- **Update Frequency**: Monthly (from Plymouth City Council)
- **Year**: 2025-26 financial year
- **Coverage**: 5,605 properties (536 hospitality sector)

### Plymouth Licensing Register
- **Source**: https://licensing.plymouth.gov.uk/
- **Format**: HTML web scraping
- **Update Frequency**: Real-time (one-time scrape)
- **Coverage**: 2,232 licensed premises (restaurants, bars, clubs)
- **Status**: 60% complete (1,350/2,232 scraped)

### Trustpilot Reviews
- **Source**: https://www.trustpilot.com/
- **Format**: JSON (__NEXT_DATA__ extraction)
- **Update Frequency**: Manual/on-demand
- **Coverage**: 65 restaurants (9,410 reviews, 2013-2025)
- **Limitation**: Company-wide reviews, not location-specific

### Google Places API
- **Source**: Google Places API (places.googleapis.com)
- **Format**: JSON API responses
- **Update Frequency**: API calls (cached)
- **Coverage**: 100% (243 restaurants)
- **Features**: Ratings, reviews (max 5), service options, contact info

---

**Report Generated**: 2025-11-21
**Next Review**: 2025-12-21
**Owner**: Plymouth Research Project Team
