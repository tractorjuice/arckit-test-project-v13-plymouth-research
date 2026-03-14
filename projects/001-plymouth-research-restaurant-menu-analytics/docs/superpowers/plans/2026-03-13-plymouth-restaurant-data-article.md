# Plymouth Restaurant Data Article — Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Write a 3,500-4,500 word data journalism feature article about the Plymouth restaurant research project, its data sources, methodology, ethics, and findings.

**Architecture:** Seven-section article written as a single markdown file. Each task produces one section draft, verified against the spec's data points. A final task assembles, polishes, and runs data verification.

**Tech Stack:** Markdown article, SQLite database queries for verification, git for version control.

**Spec:** `docs/superpowers/specs/2026-03-13-plymouth-restaurant-data-article-design.md`

**Output file:** `docs/articles/plymouth-restaurant-data-article.md`

---

## Chunk 1: Article Sections 1-4

### Task 1: Create output directory and article scaffold

**Files:**
- Create: `docs/articles/plymouth-restaurant-data-article.md`

- [ ] **Step 1: Create directory**

```bash
mkdir -p docs/articles
```

- [ ] **Step 2: Write article scaffold**

Create `docs/articles/plymouth-restaurant-data-article.md` with the title, subtitle, byline, and "By the numbers" summary box. Use these verified figures:

```markdown
# We Tracked 243 Plymouth Restaurants — Here's What We Found About Food, Hygiene, and the Data Nobody Looks At

*A data journalism investigation into what free public data reveals about a city's dining scene — and what it hides.*

---

> **By the numbers**
> 243 restaurants tracked | 2,625 menu items | 9,410 Trustpilot reviews | 486 Google reviews | 8 data sources | Total cost: £0

---
```

- [ ] **Step 3: Commit scaffold**

```bash
git add docs/articles/plymouth-restaurant-data-article.md
git commit -m "docs: scaffold Plymouth restaurant data article"
```

---

### Task 2: Write Section 1 — The Hook (~400 words)

**Files:**
- Modify: `docs/articles/plymouth-restaurant-data-article.md`

**Spec reference:** Section 1 in design spec (lines 21-40).

- [ ] **Step 1: Write the hook section**

Append Section 1 to the article. Must include these verified data points:
- 5-star FSA hygiene restaurants average 2.65 stars on Trustpilot (27 restaurants)
- 4-star FSA hygiene restaurants average 2.40 stars on Trustpilot (8 restaurants)
- Biggest gaps: Taco Bell (FSA 5, TP 1.66), Papa John's (FSA 5, TP 1.88), McDonald's (FSA 5, TP 1.89), Domino's (FSA 5, TP 1.95), Pizza Hut (FSA 5, TP 1.99), Burger King (FSA 5, TP 2.04)
- Best combined: Rockfish Plymouth (FSA 5, TP 3.75), Armado Lounge (FSA 5, TP 3.45)
- Tease that answering "why?" required stitching together 8 free public data sources
- 243 restaurants in the database, 98 with scraped menus, 36 with both hygiene and Trustpilot data

**Tone:** Authoritative but accessible. First-person plural. Lead with the paradox — a restaurant can have perfect food safety and terrible reviews. Short paragraphs.

**Format the hygiene/satisfaction gap as a comparison table**, not buried in prose. Example format:

| Restaurant | FSA Hygiene | Trustpilot | Gap |
|-----------|------------|-----------|-----|
| Taco Bell Plymouth | 5 | 1.66 | 3.34 |
| ... | ... | ... | ... |

**Do NOT include:** Restaurant recommendations, speculation about why specific restaurants score poorly, or any data not in the verified table.

- [ ] **Step 2: Word count check**

```bash
# Target: ~400 words for Section 1 (excluding the scaffold)
wc -w docs/articles/plymouth-restaurant-data-article.md
```

Acceptable range: 350-500 words for Section 1 content.

- [ ] **Step 3: Commit**

```bash
git add docs/articles/plymouth-restaurant-data-article.md
git commit -m "docs: write article Section 1 — the hygiene/satisfaction hook"
```

---

### Task 3: Write Section 2 — What Your Money Buys (~500 words)

**Files:**
- Modify: `docs/articles/plymouth-restaurant-data-article.md`

**Spec reference:** Section 2 in design spec (lines 42-59).

- [ ] **Step 1: Write the menu/price section**

Append Section 2. Must include these verified data points:
- 2,625 menu items across 98 restaurants
- 2,166 items with valid prices
- Price range: £0.50 (add-ons at Revolution) to £153.00 (Pret bundle — note this is likely a multi-item deal, flag as a data quality observation)
- Average item price: £10.68
- Price by cuisine examples (from verified queries):
  - Fine Dining (Michelin): £24.38 avg (17 items)
  - Wine Bar & Small Plates: £22.36 avg (32 items)
  - Seafood & Fish: £11.21 avg (123 items)
  - Italian: £9.74 avg (195 items)
  - Japanese: £9.53 avg (183 items)
  - Fast Food: £3.96 avg (24 items)
  - Bakery: £3.53 avg (24 items)
- Most expensive single item: Àclèaf 4-Course Tasting Menu at £75.00 (from Àclèaf at Boringdon Hall — a fine dining tasting menu). The raw data max of £153.00 is a "Classic Lunch Bundle" from Pret A Manger — a multi-item meal deal priced as a single entry, not a realistic menu item price.
- 17+ cuisine categories, led by diverse independents alongside chains

**Editorial note on price range:** The spec's verified data table shows the raw range as £0.03-£153.00. The article should use editorially cleaned values: £0.50 as the meaningful floor (£0.03 is a parsing error) and £134.00 as the meaningful ceiling (£153.00 is a bundle). State both the raw and cleaned ranges for transparency.

**Honest limitations to weave in:**
- No automated menu refresh — data collected November 2025
- £0.03 minimum price in raw data suggests parsing errors (article should use £0.50+ as the meaningful floor)
- Dietary tag columns don't exist in the actual database schema — spec mentioned them but they're not populated. State honestly that dietary analysis was planned but the scraped HTML didn't yield reliable tags.

**Tone:** Concrete and relatable. "What does £10 get you in Plymouth?"

- [ ] **Step 2: Word count check**

Target: ~500 words for this section. Total article so far should be ~900-1000 words.

- [ ] **Step 3: Commit**

```bash
git add docs/articles/plymouth-restaurant-data-article.md
git commit -m "docs: write article Section 2 — menu prices and what your money buys"
```

---

### Task 4: Write Section 3 — The Data Sources (~800 words)

**Files:**
- Modify: `docs/articles/plymouth-restaurant-data-article.md`

**Spec reference:** Section 3 in design spec (lines 61-125).

- [ ] **Step 1: Write the data sources section**

Append Section 3. Present each data source as a brief card-style paragraph (not a bullet list — this is prose). Each source needs: what it is, how you access it, what it reveals, what it hides, and its coverage.

**8 data sources to cover (in this order):**

1. **FSA Food Hygiene Ratings** — Open data XML, free (OGL v3.0), 202 of 243 restaurants matched from 1,054 Plymouth establishments. Ratings reflect inspection day. 0-5 stars with sub-scores.

2. **Trustpilot Reviews** — Web scraping of public pages, free, 63 of 243 restaurants (26%), 9,410 reviews spanning 2013-2025. 74% of restaurants have no Trustpilot presence. Chain reviews are company-wide. Pages can vanish — we got a 404 mid-project.

3. **Google Places API** — REST API, free tier ($200/month credit), ~98% coverage. Ratings, review counts, service options, business status, coordinates. Max 5 reviews per restaurant via API.

4. **Menu Web Scraping** — BeautifulSoup + Selenium, free, 98 restaurants, 2,625 items. HTML structures vary wildly. No automated refresh.

5. **Companies House** — Free API, 102 of 243 restaurants (42%). Company registration, directors, annual accounts. Financial data lags 12+ months.

6. **ONS Geography** — Postcode directory download, free, 100% coverage. Ward, LSOA, parliamentary constituency, IMD deprivation index.

7. **Plymouth Licensing** — Council website scraping, free, partial coverage (not fully integrated). Licensing hours, business categories. Mark as "in progress."

8. **Business Rates (VOA)** — Public data download, free, partial coverage (not fully integrated). Rateable values. Mark as "in progress."

**Key narrative point:** "Six sources are fully operational. Two more are in progress. Every one of them is free. None of them tells the whole story."

**Do NOT use bullet lists for the cards** — write them as flowing prose paragraphs with bold source names. Each card should be ~80-100 words.

- [ ] **Step 2: Word count check**

Target: ~800 words for this section. Total article so far should be ~1,700-1,800 words.

- [ ] **Step 3: Commit**

```bash
git add docs/articles/plymouth-restaurant-data-article.md
git commit -m "docs: write article Section 3 — the 8 data sources"
```

---

### Task 5: Write Section 4 — The Hard Part (~700 words)

**Files:**
- Modify: `docs/articles/plymouth-restaurant-data-article.md`

**Spec reference:** Section 4 in design spec (lines 127-153).

- [ ] **Step 1: Write the fuzzy matching section**

Append Section 4. Cover:

**The name problem (use this exact example):**
- "Barbican Kitchen (Original)" in our database
- "THE BARBICAN KITCHEN LTD" at Companies House
- "Barbican Kitchen Brasserie" on review sites
- Explain in plain English: same restaurant, three different names

**The scoring algorithm (simplified for general readers):**
- Name similarity score (up to 50 points) — how alike the two names are after stripping "LIMITED", "LTD", "PLC", "(PLYMOUTH)"
- Postcode match bonus (30 points) — if the postcodes are identical
- Address similarity (up to 20 points) — how closely the street addresses match
- Total possible: 100 points. Threshold for auto-match: 60 points.
- Don't mention SequenceMatcher or Python — explain the concept, not the implementation

**The improvement story:**
- First run: 49 of 98 restaurants matched (50%)
- After downloading fresh FSA data and re-running against all 243 restaurants: 202 matched (83%)
- The lesson: "The bottleneck wasn't our algorithm — it was stale source data."

**Data quality framework (briefly):**
- Validation at ingestion (price constraints, postcode format checks)
- Deduplication (database prevents duplicate reviews)
- Automated aggregation (database triggers recalculate averages on every insert)

**Honest admissions:**
- Some matches are probably wrong
- Only 36 of 243 restaurants (15%) have both hygiene AND Trustpilot data — Trustpilot is the bottleneck
- No audit trail for manual corrections

- [ ] **Step 2: Word count check**

Target: ~700 words. Total article so far should be ~2,400-2,500 words.

- [ ] **Step 3: Commit**

```bash
git add docs/articles/plymouth-restaurant-data-article.md
git commit -m "docs: write article Section 4 — fuzzy matching and data quality"
```

---

## Chunk 2: Article Sections 5-7, Assembly, and Verification

### Task 6: Write Section 5 — Scraping Ethically in 2026 (~600 words)

**Files:**
- Modify: `docs/articles/plymouth-restaurant-data-article.md`

**Spec reference:** Section 5 in design spec (lines 155-175).

- [ ] **Step 1: Write the ethics section**

Append Section 5. Cover these practices:

**robots.txt enforcement:**
- Every URL checked before fetch
- If robots.txt can't be reached (network error), default to deny — the safe approach
- Crawl-delay from robots.txt is respected

**Rate limiting:**
- 5-second minimum delay between requests to the same domain
- 2.5 seconds between Trustpilot pagination pages, 5 seconds between restaurants

**Honest identification:**
- User-Agent: `PlymouthResearchMenuScraper/1.0 (+https://plymouthresearch.uk; contact@plymouthresearch.uk)`
- No pretending to be a browser. No hiding.

**Audit logging:**
- Every HTTP request logged: robots.txt compliance flag, actual delay waited, HTTP status code, error message
- Enables retrospective compliance verification — "we can prove what we accessed and when"

**GDPR:**
- No personal data collected
- Reviewer names are public pseudonyms
- Legal basis: legitimate interest (market research)
- 12-month retention policy
- DPIA documented

**The Trustpilot 404 story:**
- One of our restaurants had a Trustpilot page that vanished mid-project (don't name the specific restaurant)
- Illustrates platform dependence: scraped data is borrowed, not owned
- Why audit logs matter

**The tension:**
- Web scraping exists in a legal grey area
- Being ethical costs nothing but attention
- Open Government Licence data has clear terms; web scraping does not

- [ ] **Step 2: Word count check**

Target: ~600 words. Total: ~3,000-3,100 words.

- [ ] **Step 3: Commit**

```bash
git add docs/articles/plymouth-restaurant-data-article.md
git commit -m "docs: write article Section 5 — scraping ethically"
```

---

### Task 7: Write Section 6 — Build This For Your City (~500 words)

**Files:**
- Modify: `docs/articles/plymouth-restaurant-data-article.md`

**Spec reference:** Section 6 in design spec (lines 177-203).

- [ ] **Step 1: Write the replication guide**

Append Section 6. Cover:

**What transfers directly (UK-wide or global):**
- FSA hygiene data: covers all of England, Wales, and Northern Ireland — change the authority code in the XML URL
- Google Places API: global coverage
- Companies House API: all UK companies
- ONS postcode directory: all UK postcodes
- The fuzzy matching algorithm: location-agnostic

**What needs adaptation:**
- Menu scraping: every restaurant's HTML is different, you'll need custom parsers
- Trustpilot coverage: varies hugely by city and sector
- Council licensing: every local authority has different systems
- Business rates: format may differ between councils

**Rough effort:**
- Data sources: 1-2 weeks to set up fetchers
- Matching and quality: 1-2 weeks to tune thresholds for your city
- Dashboard: 1 week using Streamlit
- Total cost: £0 (staying within Google's free tier)

**Call to action:**
- Mention the live dashboard exists (don't fabricate a URL — use a placeholder like `[dashboard link]`)
- Mention the repository is available (use placeholder `[repository link]`)
- Invite readers to adapt for other cities or sectors

- [ ] **Step 2: Word count check**

Target: ~500 words. Total: ~3,500-3,600 words.

- [ ] **Step 3: Commit**

```bash
git add docs/articles/plymouth-restaurant-data-article.md
git commit -m "docs: write article Section 6 — build this for your city"
```

---

### Task 8: Write Section 7 — Closing (~200 words)

**Files:**
- Modify: `docs/articles/plymouth-restaurant-data-article.md`

**Spec reference:** Section 7 in design spec (lines 205-211).

- [ ] **Step 1: Write the closing**

Append Section 7. Requirements:

- Return to the opening paradox
- The data didn't answer "which restaurant should I eat at?" — it answered "what can public data tell us, and what can't it?"
- No single data source tells the truth; combining them gets closer, but gaps remain
- Final line should echo the Barbican Kitchen matching example: "The hardest part isn't technology — it's matching 'Barbican Kitchen (Original)' to 'THE BARBICAN KITCHEN LTD.'"

Add article footer:

```markdown
---

*Data collected November 2025, with FSA hygiene data refreshed March 2026. All data sourced from publicly available APIs, open data, and public web pages. Food hygiene data used under the Open Government Licence v3.0. No personal data was collected or stored.*

*Explore the data yourself: [dashboard link] | View the source: [repository link]*
```

- [ ] **Step 2: Word count check**

Target: ~200 words for closing + footer. Total article: 3,500-4,500 words.

- [ ] **Step 3: Commit**

```bash
git add docs/articles/plymouth-restaurant-data-article.md
git commit -m "docs: write article Section 7 — closing and footer"
```

---

### Task 9: Full article review, polish, and data verification

**Files:**
- Modify: `docs/articles/plymouth-restaurant-data-article.md`

- [ ] **Step 1: Run data verification against the database**

Run this verification script to confirm every number in the article matches the database:

```bash
cd /workspaces/arckit-test-project-v13-plymouth-research/projects/001-plymouth-research-restaurant-menu-analytics
python -c "
import sqlite3
db = sqlite3.connect('plymouth_research.db')
c = db.cursor()

checks = {
    # Top-level counts
    'Total restaurants': (c.execute('SELECT COUNT(*) FROM restaurants').fetchone()[0], 243),
    'Restaurants with menus': (c.execute('SELECT COUNT(DISTINCT restaurant_id) FROM menu_items').fetchone()[0], 98),
    'Menu items': (c.execute('SELECT COUNT(*) FROM menu_items').fetchone()[0], 2625),
    'Items with valid prices': (c.execute('SELECT COUNT(*) FROM menu_items WHERE price_gbp > 0.50').fetchone()[0], 2166),
    'Avg item price': (round(c.execute('SELECT AVG(price_gbp) FROM menu_items WHERE price_gbp > 0').fetchone()[0], 2), 10.68),
    'Trustpilot reviews': (c.execute('SELECT COUNT(*) FROM trustpilot_reviews').fetchone()[0], 9410),
    'Google reviews': (c.execute('SELECT COUNT(*) FROM google_reviews').fetchone()[0], 486),
    'FSA matched': (c.execute('SELECT COUNT(*) FROM restaurants WHERE fsa_id IS NOT NULL').fetchone()[0], 202),
    'TP restaurants': (c.execute('SELECT COUNT(DISTINCT restaurant_id) FROM trustpilot_reviews').fetchone()[0], 63),
    'Hygiene+TP overlap': (c.execute('SELECT COUNT(*) FROM restaurants WHERE hygiene_rating IS NOT NULL AND trustpilot_avg_rating IS NOT NULL').fetchone()[0], 36),
    'Companies House': (c.execute('SELECT COUNT(*) FROM restaurants WHERE company_number IS NOT NULL').fetchone()[0], 102),
    # Per-restaurant ratings (litigation-sensitive)
    'Rockfish TP': (c.execute(\"SELECT ROUND(trustpilot_avg_rating,2) FROM restaurants WHERE name='Rockfish Plymouth'\").fetchone()[0], 3.75),
    'Rockfish FSA': (c.execute(\"SELECT hygiene_rating FROM restaurants WHERE name='Rockfish Plymouth'\").fetchone()[0], 5),
    'Armado TP': (c.execute(\"SELECT ROUND(trustpilot_avg_rating,2) FROM restaurants WHERE name='Armado Lounge'\").fetchone()[0], 3.45),
    'Taco Bell TP': (c.execute(\"SELECT ROUND(trustpilot_avg_rating,2) FROM restaurants WHERE name='Taco Bell Plymouth'\").fetchone()[0], 1.66),
    'McDonalds TP': (c.execute(\"SELECT ROUND(trustpilot_avg_rating,2) FROM restaurants WHERE name LIKE '%McDonald%Plymouth%'\").fetchone()[0], 1.89),
    # Cross-tabulations
    '5star FSA avg TP': (round(c.execute('SELECT AVG(trustpilot_avg_rating) FROM restaurants WHERE hygiene_rating=5 AND trustpilot_avg_rating IS NOT NULL').fetchone()[0], 2), 2.65),
    '5star FSA count': (c.execute('SELECT COUNT(*) FROM restaurants WHERE hygiene_rating=5 AND trustpilot_avg_rating IS NOT NULL').fetchone()[0], 27),
    '4star FSA avg TP': (round(c.execute('SELECT AVG(trustpilot_avg_rating) FROM restaurants WHERE hygiene_rating=4 AND trustpilot_avg_rating IS NOT NULL').fetchone()[0], 2), 2.40),
    'Cuisine categories': (c.execute('SELECT COUNT(DISTINCT cuisine_type) FROM restaurants').fetchone()[0], 17),
}

all_pass = True
for name, (actual, expected) in checks.items():
    status = 'PASS' if actual == expected else 'FAIL'
    if status == 'FAIL': all_pass = False
    print(f'  [{status}] {name}: expected {expected}, got {actual}')

print()
print('ALL CHECKS PASSED' if all_pass else 'SOME CHECKS FAILED — update article')
db.close()
"
```

If any checks fail, update the article to use the actual database values.

- [ ] **Step 2: Full read-through and polish**

Read the complete article from top to bottom. Check for:
- Consistent tone (authoritative, accessible, first-person plural)
- No jargon without explanation
- Short paragraphs (2-4 sentences max)
- Subheadings every 300-400 words
- Smooth transitions between sections
- No content that violates the "What the Article Will NOT Cover" scoping rules (no restaurant recommendations, no naming/shaming beyond public FSA data, no code walkthroughs, no speculation)

- [ ] **Step 3: Final word count**

```bash
wc -w docs/articles/plymouth-restaurant-data-article.md
```

Must be 3,500-4,500 words. If under 3,500, expand the thinnest section. If over 4,500, trim the most verbose section.

- [ ] **Step 4: Final commit**

```bash
git add docs/articles/plymouth-restaurant-data-article.md
git commit -m "docs: complete Plymouth restaurant data article — verified and polished"
```

---

## Summary

| Task | Section | Target Words | Key Data Points |
|------|---------|-------------|-----------------|
| 1 | Scaffold | — | Title, byline, summary box |
| 2 | The Hook | ~400 | Hygiene/satisfaction paradox, gap table |
| 3 | What Your Money Buys | ~500 | Prices by cuisine, menu stats |
| 4 | The Data Sources | ~800 | 8 source cards (6 operational, 2 in progress) |
| 5 | The Hard Part | ~700 | Fuzzy matching, Barbican Kitchen example, 49→202 story |
| 6 | Scraping Ethically | ~600 | robots.txt, rate limiting, GDPR, Trustpilot 404 |
| 7 | Build This For Your City | ~500 | Replication guide, effort estimates |
| 8 | Closing | ~200 | Return to paradox, Barbican Kitchen callback |
| 9 | Verification & Polish | — | Data check script, full read-through, word count |

**Total target: 3,700 words** (within the 3,500-4,500 range)
