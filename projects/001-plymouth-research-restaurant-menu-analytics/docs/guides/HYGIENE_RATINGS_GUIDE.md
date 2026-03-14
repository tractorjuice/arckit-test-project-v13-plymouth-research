# Food Hygiene Rating Scheme (FHRS) - Understanding the System

## Overview

The Food Hygiene Rating Scheme (FHRS) is the UK's official food safety rating system operated by the Food Standards Agency (FSA). It helps consumers make informed choices about where to eat or shop for food.

## Rating Scale (0-5 Stars)

| Rating | Meaning | Description |
|--------|---------|-------------|
| ⭐⭐⭐⭐⭐ (5) | **Very Good** | Hygiene standards are very good |
| ⭐⭐⭐⭐ (4) | **Good** | Hygiene standards are good |
| ⭐⭐⭐ (3) | **Satisfactory** | Hygiene standards are generally satisfactory |
| ⭐⭐ (2) | **Improvement Necessary** | Some improvement is necessary |
| ⭐ (1) | **Major Improvement** | Major improvement is necessary |
| ❌ (0) | **Urgent Improvement** | Urgent improvement is required |

## How the Scoring Works

### Three Assessment Categories

Food safety officers inspect and score establishments in three areas (lower scores are better):

1. **Hygiene** - Food handling, preparation, cooking, reheating, cooling, storage
2. **Structural** - Cleanliness, layout, lighting, ventilation, pest control, facilities
3. **Confidence in Management** - Food safety systems, staff training, protocols

### Score Values (Lower is Better!)

| Score | Meaning |
|-------|---------|
| 0 | Excellent compliance - no issues found |
| 5 | Very good compliance - very minor issues |
| 10 | Good compliance - minor issues |
| 15 | Satisfactory - some issues requiring attention |
| 20 | Improvement needed - significant issues |
| 25 | Major improvement needed - serious issues |
| 30 | Critical issues (Confidence in Management only) |

### How Scores Translate to Final Rating

**Based on TOTAL score (Hygiene + Structural + Confidence):**

| Total Score | Final Rating |
|-------------|--------------|
| 0-15 | 5★ (Very Good) |
| 20 | 4★ (Good) |
| 25-30 | 3★ (Satisfactory) |
| 35-40 | 2★ (Improvement Necessary) |
| 45-50 | 1★ (Major Improvement) |
| 50+ | 0★ (Urgent Improvement) |

**⚠️ Important Override Rules:**
- If ANY single category scores 15+, the maximum rating is 3★
- If ANY single category scores 20+, the rating is further reduced
- A high score in one area can override the total score

## Our Plymouth Research Data (49 restaurants rated)

### Distribution

| Rating | Count | Percentage |
|--------|-------|------------|
| 5★ | 33 | 67.3% |
| 4★ | 12 | 24.5% |
| 3★ | 1 | 2.0% |
| 2★ | 2 | 4.1% |
| 1★ | 1 | 2.0% |

**Average Rating:** 4.51/5 ⭐

### Exemplary Performers (Perfect Scores - Total: 0)

These restaurants achieved a score of 0 (perfect compliance) in all three categories:

- Barbican Kitchen (Original)
- Barbican Kitchen Bar
- Costa Coffee Plymouth
- Five Guys Plymouth
- McDonald's Plymouth
- Starbucks Drake Circus
- Taco Bell Plymouth
- The Bank Restaurant & Bar
- The Mannamead
- Wagamama Plymouth
- Wagamama Royal William Yard

### Restaurants Requiring Attention (≤2★)

#### 🟠 2★ - The Dock
**Inspected:** 2024-05-22
- **Hygiene:** 15 (Satisfactory - issues present)
- **Structural:** 5 (Very good)
- **Confidence in Management:** 10 (Good)
- **Total:** 30 points
- **Analysis:** Hygiene practices need improvement. Score of 15 in Hygiene limits rating to max 3★.

#### 🟠 2★ - Himalayan Spice
**Inspected:** 2024-08-13
- **Hygiene:** 5 (Very good)
- **Structural:** 15 (Satisfactory - issues present)
- **Confidence in Management:** 10 (Good)
- **Total:** 30 points
- **Analysis:** Building/facilities need improvement. Score of 15 in Structural limits rating to max 3★.

#### 🟡 3★ - Koishii Sushi Bar
**Inspected:** 2024-10-14
- **Hygiene:** 10 (Good)
- **Structural:** 10 (Good)
- **Confidence in Management:** 10 (Good)
- **Total:** 30 points
- **Analysis:** All areas are "good" but not excellent. Total score of 30 = 3★ rating.

## Inspection Frequency

Inspections are risk-based:
- **Highest-risk:** Every 6 months
- **Medium-risk:** Every 1-2 years
- **Lower-risk:** Every 2+ years

Factors affecting risk assessment:
- Type of food served
- Customer vulnerability (e.g., hospitals, schools)
- Processing complexity
- Previous hygiene history

## Special Statuses

- **AwaitingInspection**: New establishment not yet inspected
- **Exempt**: Business type doesn't require FHRS rating (e.g., newsagents selling pre-packaged food)

## Data Freshness

Our data is from the FSA XML export dated: **2025-11-15**

Most recent inspection in our dataset: **The Stable Plymouth** (2025-09-19)
Oldest inspection in our dataset: **Miller & Carter Plymouth** (2018-09-06) - may be due for re-inspection

## Dashboard Display Guidelines

When displaying ratings in the dashboard:

1. **Use visual star indicators** ⭐⭐⭐⭐⭐
2. **Color-code by rating:**
   - 5★: Green (excellent)
   - 4★: Light green (good)
   - 3★: Yellow (satisfactory)
   - 2★: Orange (improvement needed)
   - 1★/0★: Red (urgent attention)

3. **Show inspection date** - older inspections may not reflect current state
4. **Include detailed scores** where appropriate
5. **Provide FSA link** for full inspection details
6. **Handle missing ratings** - 49 unmatched restaurants need manual review

## References

- Food Standards Agency: https://www.food.gov.uk/safety-hygiene/food-hygiene-rating-scheme
- FSA API: https://api.ratings.food.gov.uk
- Plymouth Data: https://ratings.food.gov.uk/api/open-data-files/FHRS891en-GB.xml

---

*Document generated: 2025-11-18*
*Data source: FSA FHRS Open Data (Plymouth City - Authority Code 891)*
