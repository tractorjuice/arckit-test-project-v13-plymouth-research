# Design Spec: Plymouth Restaurant Data Article

## Overview

A long-form data journalism feature (3,500-4,500 words) titled "We Tracked 243 Plymouth Restaurants - Here's What We Found About Food, Hygiene, and the Data Nobody Looks At." Methodology-forward, with Plymouth as the worked example. Aimed at a general audience, with ethical scraping as a prominent theme and radical transparency about data gaps and failures.

## Audience

General readers who are data-curious but not necessarily technical. The piece should be accessible to someone who has never written code, while rewarding technically inclined readers with enough specificity to replicate the work.

## Tone & Voice

- Authoritative but accessible
- First-person plural ("we scraped", "we discovered")
- Technical terms introduced with plain-English context
- Honest about failures without being self-deprecating
- Short paragraphs (2-4 sentences), subheadings every 300-400 words

## Article Structure

### Section 1: The Hook (~400 words)

**Purpose:** Grab attention with the hygiene/satisfaction paradox.

**Key data points:**
- 243 restaurants in the database, 98 with scraped menu data, 36 with both hygiene ratings and Trustpilot reviews
- Restaurants with 5-star FSA hygiene average 2.65 stars on Trustpilot (27 restaurants)
- Restaurants with 4-star FSA hygiene average 2.40 stars on Trustpilot (8 restaurants)
- Chain fast-food outlets consistently score highest on hygiene and lowest on satisfaction
- Best overall performers combine both (e.g., Rockfish Plymouth: 5-star hygiene, 3.75-star Trustpilot)

**Narrative beat:** Tease that answering "why?" required stitching together 8 free public data sources. Set up the rest of the article.

**Visual element:** "By the numbers" summary box:
- 243 restaurants tracked
- 2,625 menu items
- 9,410 Trustpilot reviews
- 486 Google reviews
- 8 data sources
- Total cost: £0

### Section 2: What Your Money Buys (~500 words)

**Purpose:** Make the data tangible and relatable through menu and price findings.

**Key data points:**
- 2,625 menu items with prices, from £0.03 to £153.00
- Average item price: £10.68
- 2,166 items with valid prices (some items lack pricing)
- 17 cuisine categories, led by Pub (45), Restaurant (36), Coffee Shop (23)
- Dietary flags tracked: vegetarian, vegan, gluten-free
- Price distribution across cuisine types

**Narrative beat:** Move from the abstract (ratings) to the concrete (what can you eat, what does it cost). Acknowledge that menu data goes stale — prices change, seasonal menus rotate, restaurants open and close.

**Honest limitations:**
- No automated menu refresh yet — data ages
- Dietary tags are incomplete (scraped from HTML, not verified)
- Price extraction has edge cases (£0.03 minimum suggests parsing errors)

### Section 3: The Data Sources (~800 words)

**Purpose:** Reveal the 8 data sources, what each provides, and what each hides.

**Data source cards (one per source):**

1. **FSA Food Hygiene Ratings**
   - Type: Open data XML download
   - Cost: Free (Open Government Licence v3.0)
   - Coverage: 202 restaurants matched from 1,054 Plymouth establishments
   - Provides: 0-5 star rating, sub-scores (hygiene, structural, management confidence), inspection dates
   - Limitation: Ratings reflect inspection day, not current state; name matching is imperfect

2. **Trustpilot Reviews**
   - Type: Web scraping (public pages)
   - Cost: Free
   - Coverage: 63 of 243 restaurants (26%), 9,410 reviews spanning 2013-present
   - Provides: Star ratings, review text, dates, author metadata
   - Limitation: 74% of restaurants have no Trustpilot presence; chain reviews are company-wide; pages can vanish (we got a 404 mid-project)

3. **Google Places API**
   - Type: REST API
   - Cost: Free tier ($200/month credit, ~11,700 requests)
   - Coverage: ~98% of restaurants
   - Provides: Ratings, review counts, service options (dine-in, delivery, vegetarian), business status, coordinates
   - Limitation: Maximum 5 reviews per restaurant via API

4. **Menu Web Scraping**
   - Type: HTML scraping (BeautifulSoup + Selenium)
   - Cost: Free
   - Coverage: 98 restaurants, 2,625 items
   - Provides: Item names, prices, categories, descriptions, dietary flags
   - Limitation: HTML structures vary wildly; prices can be misread; no automated refresh

5. **Companies House**
   - Type: Free API
   - Cost: Free
   - Coverage: 102 of 243 restaurants (42%) — excludes sole traders and partnerships
   - Provides: Company registration, directors, annual accounts (turnover, profit/loss, net assets)
   - Limitation: Financial data lags 12+ months (annual filings)

6. **ONS Geography**
   - Type: Postcode directory download
   - Cost: Free
   - Coverage: 100% (postcode-based lookup)
   - Provides: Ward, LSOA, parliamentary constituency, IMD deprivation index
   - Limitation: Updated quarterly; postcodes occasionally reassigned

7. **Plymouth Licensing**
   - Type: Council website scraping
   - Cost: Free
   - Coverage: Partial (not yet fully integrated into pipeline)
   - Provides: Licensing hours, business categories
   - Limitation: Council website structure changes; coverage incomplete
   - Note: Mention as "in progress" in article — demonstrates the long tail of data integration

8. **Business Rates (VOA)**
   - Type: Public data download
   - Cost: Free
   - Coverage: Partial (not yet fully integrated into pipeline)
   - Provides: Rateable values — a proxy for premises size and commercial value
   - Limitation: Property-level data, not always 1:1 with restaurants
   - Note: Mention as "in progress" in article — illustrates that 8 sources is aspirational, 6 are fully operational

**Narrative beat:** Each source tells part of the story. None tells the whole story. The value is in combining them — which introduces the hardest problem.

### Section 4: The Hard Part — Making Data Talk (~700 words)

**Purpose:** Explain fuzzy matching, data reconciliation, and quality measures.

**Key concepts to explain (in plain English):**
- Why matching is hard: "Barbican Kitchen (Original)" in our database is "THE BARBICAN KITCHEN LTD" at Companies House and "Barbican Kitchen Brasserie" on review sites
- The scoring algorithm (from `collection/fetchers/hygiene_fetcher.py`, the code that produced the 202-match result via `run_collection.py`): name_similarity * 0.5 (max 50 points), postcode exact match bonus (30 points), address_similarity * 20 (max 20 points) — total possible score of 100, threshold of 60 for auto-match
- Note: The project's CLAUDE.md documents a different algorithm from the standalone `scripts/fetchers/fetch_hygiene_ratings_v2.py` script (0-100 name + 50 postcode + 30 address, threshold 70). The article should use the `run_collection.py` pipeline algorithm, which is what produced the 202-match figure cited here.
- Thresholds: 60% minimum to consider, 70% auto-match, 95% exact match
- Name normalization: strip "LIMITED", "LTD", "PLC", "(PLYMOUTH)", special characters

**The improvement story:**
- Initial FSA matching: 49 of 98 restaurants (50%)
- After refreshing FSA XML and re-running: 202 of 243 restaurants matched (83%)
- The lesson: stale source data was the bottleneck, not the algorithm

**Data quality framework:**
- Validation at ingestion (price range constraints, postcode regex, NOT NULL checks)
- Deduplication (composite unique indexes on reviews)
- Automated aggregation (database triggers update restaurant-level stats on review insert/delete)
- Quality metrics table (completeness, accuracy, timeliness, duplication tracking)

**Honest admissions:**
- Some matches are probably wrong (similar names, same postcode)
- Manual review needed for 70-80% confidence matches
- No edit audit trail for manual corrections
- Only 36 of 243 restaurants (15%) have both hygiene AND Trustpilot review data — cross-source overlap is the hardest gap to close

### Section 5: Scraping Ethically in 2026 (~600 words)

**Purpose:** Make the ethical framework a first-class theme.

**Key practices explained:**
- **robots.txt enforcement:** Every URL checked before fetch; default deny on network errors (safe approach); crawl-delay respected
- **Rate limiting:** 5-second minimum per domain, enforced by DomainRateLimiter class; thread-safe; 2.5s between Trustpilot pages, 5s between restaurants
- **Honest identification:** User-Agent string includes project name, URL, and contact email (`PlymouthResearchMenuScraper/1.0`)
- **Audit logging:** Every HTTP request logged with robots.txt compliance flag, actual delay, status code, error message — enabling retrospective compliance verification
- **GDPR:** No personal data collected; reviewer names are public pseudonyms; legal basis is legitimate interest; 12-month retention policy; DPIA documented

**The Trustpilot 404 story:**
- One of our restaurants had a Trustpilot page that vanished mid-project (don't name the specific restaurant)
- Illustrates platform dependence — scraped data is borrowed, not owned
- Why audit logs matter: you can prove what you accessed and when

**The tension:**
- Web scraping exists in a grey area
- Being ethical costs nothing but attention — rate limits, User-Agent strings, robots.txt checks
- The alternative (ignoring these) is faster but unsustainable and potentially illegal
- Open Government Licence data (FSA, ONS, VOA) has clear terms; web scraping does not

### Section 6: Build This For Your City (~500 words)

**Purpose:** Practical replication guide.

**What transfers directly:**
- FSA hygiene data covers all of England, Wales, and Northern Ireland (change the authority code in the XML URL)
- Google Places API is global
- Companies House API covers all UK companies
- ONS postcode directory covers all UK postcodes
- The fuzzy matching algorithm is location-agnostic

**What needs adaptation:**
- Menu scraping — every restaurant's HTML is different
- Trustpilot coverage varies by city and sector
- Council licensing data varies by local authority
- Business rates format may differ

**Rough effort estimate:**
- Data sources: 1-2 weeks to set up fetchers
- Matching and quality: 1-2 weeks to tune thresholds
- Dashboard: 1 week (Streamlit is fast for prototyping)
- Total cost: £0 if staying within Google's free tier

**Call to action:**
- Link to the live dashboard
- Link to the repository (with caveat that scraping dependencies need separate installation)
- Invitation to adapt for other cities or sectors (hospitality, retail, healthcare)

### Section 7: Closing (~200 words)

**Purpose:** Wrap up with a reflective conclusion.

**Narrative beat:** Return to the opening paradox. The data didn't answer "which restaurant should I eat at?" — it answered "what can public data tell us, and what can't it?" The real finding is that no single data source tells the truth. Combining them gets closer, but gaps remain. That honesty is the point.

**Final thought:** Every city has this data sitting in public databases, XML files, and review platforms. Most of it is never combined. The tools to do it are free. The hardest part isn't technology — it's matching "Barbican Kitchen (Original)" to "THE BARBICAN KITCHEN LTD."

## Visual Treatment

**Inline elements:**
- "By the numbers" summary box (top of article)
- Data source cards (8 small boxed summaries in Section 3)
- Hygiene vs satisfaction comparison table (Section 1)
- Pull quotes from the data (scattered throughout)

**Not included in article:**
- Interactive charts — readers directed to the live dashboard instead
- Code snippets — readers directed to the repository
- Screenshots of the dashboard — mentioned but not embedded, to avoid staleness

## Scoping: What the Article Will NOT Cover

- Individual restaurant recommendations or "best of" rankings
- Naming and shaming low-hygiene restaurants beyond public FSA data
- Detailed code walkthroughs or API documentation
- Speculation about why specific restaurants have poor reviews
- Comparison with other cities
- Commercial or monetisation angles
- Sentiment analysis of review text (star ratings only)

## Data Currency

All data was originally collected in November 2025. The FSA hygiene XML was re-downloaded on 2026-03-13 (1,054 establishments in the March 2026 extract vs 1,841 in the November 2025 extract). The difference likely reflects FSA filtering criteria or data format changes in the XML endpoint — both downloads use the same URL (FHRS891en-GB.xml, Plymouth authority). The article should note the download date and establishment count without speculating on the difference. Menu data, Trustpilot reviews, and Google reviews have not been refreshed since November 2025. The article should state the data collection period explicitly and note that prices, ratings, and business status may have changed.

## Verified Data Points (from database as of 2026-03-13)

All values below were queried directly from `plymouth_research.db` on 2026-03-13.

| Metric | Value | Notes |
|--------|-------|-------|
| Total restaurants | 243 | All active |
| Restaurants with menu data | 98 | Scraped Nov 2025 |
| Menu items | 2,625 | |
| Items with valid prices | 2,166 | |
| Price range | £0.03 - £153.00 | £0.03 min likely a parsing error |
| Average item price | £10.68 | |
| Trustpilot reviews | 9,410 | Spanning 2013-2025 |
| Google reviews | 486 | All fetched 2025-11-19; CLAUDE.md's "481" was inaccurate | Max 5 per restaurant (API limit) |
| FSA establishments in XML | 1,054 | March 2026 download |
| FSA matched restaurants | 202 | Up from 49 after XML refresh |
| Restaurants with Trustpilot URL | 65 | |
| Restaurants with Trustpilot reviews | 63 | |
| Restaurants with Companies House data | 102 | |
| Hygiene + Trustpilot overlap | 36 | Key cross-source metric |
| Hygiene + Google overlap | 198 | |
| All three (hygiene + TP + Google) | 36 | Same as hygiene+TP — Trustpilot is the bottleneck; nearly all hygiene-matched restaurants also have Google data |
| Cuisine categories | 17 | |
| Top cuisine: Pub | 45 restaurants | |
| 5-star FSA avg Trustpilot | 2.65 stars (27 restaurants) | |
| 4-star FSA avg Trustpilot | 2.40 stars (8 restaurants) | |
| Rockfish Plymouth | FSA 5, TP 3.75, Google 4.4 | Verified current |
| Armado Lounge | FSA 5, TP 3.45, Google 4.3 | Verified current |

**Note on discrepancies with project CLAUDE.md:** The project CLAUDE.md (last updated 2025-11-22) documents some figures from the original data collection (49 FSA matches, 481 Google reviews, different matching algorithm weights). The verified data table above reflects the current database state after the 2026-03-13 FSA refresh. The article should use these verified figures.

## Editorial Process

Before publication, all data claims in the finished article must be verified against the database. A verification script should be run to confirm every number cited. Any figures that have shifted since this spec was written should be updated in the article draft.

## Output

A single markdown file written to the project, suitable for publication as a blog post or web article. Self-contained with inline data, pointing to the dashboard and repository for interactive exploration. No specific publication platform assumed — the markdown format is portable to Medium, Substack, a personal blog, or a static site generator.
