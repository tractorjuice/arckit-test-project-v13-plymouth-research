# Gold Standard Progress Report - Option 1

**Date**: 2025-11-21
**Objective**: Complete 22 restaurants with 4/5 data sources to achieve 100% coverage

---

## Target Restaurants (22 total)

### Category 1: Missing Licensing Only (8 restaurants)

| ID | Restaurant | FSA | Business Rates | Trustpilot | Google | Status |
|----|------------|-----|----------------|------------|--------|--------|
| 4 | Rockfish Plymouth | 5★ | £55,000 | ✓ | ✓ | ⏳ Scraper at 42% |
| 7 | Honky Tonk Wine Library | 1★ | £19,250 | ✓ | ✓ | ⏳ Scraper at 42% |
| 16 | Wagamama Plymouth | 5★ | £111,000 | ✓ | ✓ | ⏳ Scraper at 42% |
| 46 | Pizza Express Plymouth | 5★ | £48,000 | ✓ | ✓ | ⏳ Scraper at 42% |
| 69 | Nando's Barbican | 5★ | £80,000 | ✓ | ✓ | ⏳ Scraper at 42% |
| 80 | Turtle Bay Plymouth | 5★ | £97,500 | ✓ | ✓ | ⏳ Scraper at 42% |
| 91 | Nando's Plymouth | 5★ | £80,000 | ✓ | ✓ | ⏳ Scraper at 42% |
| 194 | Five Guys Plymouth | 5★ | £71,000 | ✓ | ✓ | ✅ Found in scraper |

**Progress**: 1/8 found (12.5%)
**Issue**: Licensing scraper stopped at 42.6% (950/2,232 premises)
**Action Required**: Restart/continue scraper to 100%

---

### Category 2: Missing Business Rates Only (2 restaurants)

| ID | Restaurant | FSA | Licensing | Trustpilot | Google | Status |
|----|------------|-----|-----------|------------|--------|--------|
| 34 | Subway Plymouth | 5★ | ✓ | ✓ | ✓ | ❌ Not found |
| 157 | Seco Lounge | 4★ | ✓ | ✓ | ✓ | 🔍 Possible match |

**Subway Plymouth**:
- Searched by postcode PL1 2SN: No match
- Issue: May not be in business rates register or postcode incorrect

**Seco Lounge**:
- Found: LOUNGERS LIMITED at multiple Plymouth addresses
- Issue: Seco Lounge is a Loungers brand, but address doesn't match PL1 3RP
- Possible matches:
  - LOUNGERS UK LIMITED at PL1 3GE
  - LOUNGERS LIMITED at PL4 0FE
  - LOUNGERS UK LIMITED at PL1 2LS
  - LOUNGERS PLC at PL1 2JN

**Progress**: 0/2 confirmed
**Action Required**: Manual verification of addresses

---

### Category 3: Missing Trustpilot Only (12 restaurants)

| ID | Restaurant | FSA | Business Rates | Licensing | Google | Trustpilot Found |
|----|------------|-----|----------------|-----------|--------|------------------|
| 231 | Cosmic Kitchen | 5★ | £16,500 | ✓ | ✓ | ❌ No page |
| 239 | NORA'S | 5★ | £14,100 | ✓ | ✓ | ❌ No page |
| 256 | KYOWA | 5★ | £6,500 | ✓ | ✓ | ❌ No page |
| 276 | Cafe and Bistro Tio Leo | 4★ | £8,100 | ✓ | ✓ | ❌ No page |
| 301 | Coffee#1 Plymouth | 5★ | £65,000 | ✓ | ✓ | ⚠️ Company-wide only |
| 313 | Old Town Tiki Bar | 5★ | £32,250 | ✓ | ✓ | ❌ No page |
| 314 | Tigermilk | 5★ | £26,000 | ✓ | ✓ | ❌ No page |
| 318 | Brass Monkey | 5★ | £93,750 | ✓ | ✓ | ❌ No page |
| 339 | Minerva Inn | 5★ | £8,500 | ✓ | ✓ | ❌ No page |
| 340 | Dolphin Hotel | 5★ | £53,000 | ✓ | ✓ | ❌ No page |
| 348 | Lord High Admiral | 5★ | £11,100 | ✓ | ✓ | ❌ No page |
| 359 | Golden Hind | 5★ | £25,800 | ✓ | ✓ | ❌ No page |

**Progress**: 0/12 found
**Findings**:
- Coffee#1: Has company-wide Trustpilot (www.coffee1.co.uk) but not location-specific
- Pubs (Minerva Inn, Dolphin Hotel, Golden Hind, Lord High Admiral, Brass Monkey): Not on Trustpilot, reviewed on TripAdvisor/pub sites instead
- Small independent restaurants: Generally no Trustpilot presence

**Why This Happened**:
- Traditional pubs don't use Trustpilot
- Small independent venues rely on Google/TripAdvisor
- Only 26.7% of our restaurants have Trustpilot pages overall
- Trustpilot is more common for chains, retail, services (not pubs/small restaurants)

---

## Overall Results

| Category | Target | Achieved | Success Rate |
|----------|--------|----------|--------------|
| Licensing data | 8 | 1 | 12.5% |
| Business rates | 2 | 0 | 0% |
| Trustpilot URLs | 12 | 0 | 0% |
| **TOTAL** | **22** | **1** | **4.5%** |

---

## Key Learnings

### 1. Licensing Scraper Incomplete
- Stopped at 42.6% (950/2,232 premises)
- Not running in background
- Only found 2/8 target restaurants so far (Five Guys, Pizza Express)
- **Blocking factor**: Need to complete scraper to 100%

### 2. Business Rates Postcode Issues
- Subway: Postcode PL1 2SN not in register
- Seco Lounge: Brand name (Loungers) vs trading name mismatch
- **Blocking factor**: Need manual address verification

### 3. Trustpilot Presence is Rare for This Restaurant Type
- 0/12 restaurants have location-specific Trustpilot pages
- Pubs and small independents prefer TripAdvisor/Google
- Only chains have Trustpilot presence (and usually company-wide)
- **Fundamental issue**: Wrong data source for these restaurant types

---

## Revised Strategy

### Short-Term (Achievable)
1. ✅ **Achieved**: Business rates matcher improvements (+19 restaurants, 16.9% → 24.7%)
2. ⏳ **In Progress**: Licensing scraper (42.6% complete)
3. ❌ **Not Feasible**: Trustpilot for pubs/small independents

### Realistic Goal Adjustment
**Instead of 22 → 22 with 100% coverage:**
- Focus on 8 restaurants missing licensing (if scraper completes)
- Accept that pubs/small venues won't have Trustpilot
- **Revised target**: 9 restaurants with 4/5 → 5/5 (8 licensing + 1 already found)

### Alternative Metrics
**"Gold Standard" should be redefined as:**
- 4/5 data sources for pubs/independents (Trustpilot not expected)
- 5/5 data sources only for chains/larger venues

**Current State**:
- 22 restaurants with 4/5 sources (9.1% of 243)
- 1 restaurant can achieve 5/5 if we complete licensing
- Realistically: 8-9 restaurants could achieve 5/5 with licensing data

---

## Recommendations

### Priority 1: Complete Licensing Scraper
- Restart scraper from checkpoint 950
- Target completion: 100% (2,232 premises)
- Expected gain: 7 more gold standard restaurants

### Priority 2: Focus on Realistic Targets
- Don't chase Trustpilot for pubs (not their platform)
- Accept TripAdvisor/Google as alternatives
- Consider "Gold Standard" = 4/5 for most restaurant types

### Priority 3: Alternative Approach
Instead of completing 22 restaurants:
1. Complete licensing scraper (get to 8 restaurants with 5/5)
2. Improve FSA matcher (add +10-15 hygiene ratings)
3. Run business rates matcher v3 (potential +10-20 more)

**Impact**: Broader coverage improvement vs narrow "100%" achievement

---

## Conclusion

**Option 1 Results**: Partially successful

✅ **Wins**:
- Identified 22 restaurants with 4/5 sources (up from 15!)
- Business rates matcher improvements added 7 to this list
- Found 1 restaurant can achieve 5/5 (Five Guys)

❌ **Challenges**:
- Licensing scraper incomplete (blocking 7/8 targets)
- Trustpilot not viable for pubs/small independents (0/12 found)
- Business rates postcode mismatches (0/2 resolved)

🎯 **Realistic Outcome**:
- 1-2 restaurants achievable to 5/5 now
- 8-9 restaurants achievable if licensing scraper completes
- 12 restaurants will remain at 4/5 (Trustpilot not their platform)

**Recommendation**: Pivot to broader coverage improvements (FSA matcher v2, business rates v3) rather than narrow "100%" pursuit.
