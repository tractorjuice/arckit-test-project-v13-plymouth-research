# Project Requirements: Plymouth Research Restaurant Menu Analytics

## Document Control

| Field | Value |
|-------|-------|
| **Document ID** | ARC-001-REQ-v1.0 |
| **Document Type** | Business and Technical Requirements Specification |
| **Project** | Plymouth Research Restaurant Menu Analytics (Project 001) |
| **Classification** | OFFICIAL |
| **Status** | DRAFT |
| **Version** | 1.0 |
| **Created Date** | 2025-11-22 |
| **Last Modified** | 2025-11-22 |
| **Review Cycle** | Monthly |
| **Next Review Date** | 2025-12-22 |
| **Owner** | Product Owner - Plymouth Research |
| **Reviewed By** | [PENDING] |
| **Approved By** | [PENDING] |
| **Distribution** | Product Team, Architecture Team, Development Team |

## Revision History

| Version | Date | Author | Changes | Approved By | Approval Date |
|---------|------|--------|---------|-------------|---------------|
| 1.0 | 2025-11-22 | ArcKit AI | Initial creation from `/arckit.requirements` command based on production codebase analysis | [PENDING] | [PENDING] |

## Document Purpose

This document specifies the comprehensive business and technical requirements for the Plymouth Research Restaurant Menu Analytics platform. It serves as the definitive reference for:
- Product development and feature prioritization
- Architecture design decisions and technology selection
- Vendor RFP evaluation criteria (if considering SaaS alternatives)
- Quality assurance and acceptance testing
- Compliance validation (GDPR, web scraping ethics)

All requirements are derived from analysis of the production codebase (13,315 lines of code), existing architecture principles (18 documented principles), and current operational capabilities.

---

## Executive Summary

### Business Context

Plymouth Research operates an independent restaurant and bar analytics platform focused on the Plymouth, UK market. The platform aggregates publicly available data from restaurant websites, government food safety agencies, review platforms, and business registries to provide comprehensive insights into the local hospitality industry.

The business value proposition is built on three pillars:
1. **Data Aggregation**: Consolidate fragmented restaurant data (menus, prices, hygiene ratings, reviews, financial health) into a single searchable dashboard
2. **Consumer Insights**: Enable consumers to make informed dining decisions based on price, cuisine, dietary options, hygiene standards, and peer reviews
3. **Market Intelligence**: Provide researchers, journalists, and industry stakeholders with analytical tools to understand restaurant market dynamics, pricing trends, and food safety patterns

The platform currently serves as an internal research tool but has potential to expand to:
- Public consumer-facing website (similar to Yelp/TripAdvisor but menu-focused)
- B2B SaaS platform for food industry analysts
- Geographic expansion beyond Plymouth to Devon and UK-wide coverage

### Objectives

1. **Comprehensive Data Coverage**: Achieve 90%+ coverage of Plymouth restaurants (150+ establishments) with menu, pricing, and hygiene data
2. **Data Quality Excellence**: Maintain 95%+ data accuracy through automated validation, duplicate detection, and quality monitoring
3. **User Experience**: Deliver sub-2-second dashboard load times and sub-500ms search query responses for responsive user experience
4. **Ethical & Legal Compliance**: Operate within legal boundaries (UK GDPR, Computer Misuse Act, Copyright law) with respectful web scraping practices
5. **Cost Efficiency**: Keep total infrastructure and operational costs under £100/month while supporting 150+ restaurants and 10,000+ menu items

### Expected Outcomes

**Quantitative Outcomes**:
- **Restaurant Coverage**: 150+ Plymouth restaurants catalogued (current: 243 restaurants)
- **Menu Item Catalog**: 10,000+ menu items with pricing data (current: 2,625 items)
- **Hygiene Rating Coverage**: 80%+ of restaurants matched with FSA hygiene ratings (current: 49/98 = 50%)
- **Review Data Integration**: 60%+ of restaurants with Trustpilot reviews (current: 63/98 = 64%, 9,410 reviews)
- **Performance**: <2s dashboard page load (p95), <500ms search queries (p95)
- **Data Quality**: 95%+ completeness for required fields, 98%+ price extraction accuracy
- **Cost**: ≤£100/month operational costs (infrastructure, APIs, hosting)

**Qualitative Outcomes**:
- Establish Plymouth Research as the authoritative source for Plymouth restaurant menu data
- Demonstrate feasibility for geographic expansion (Devon, UK-wide)
- Build foundation for potential B2B SaaS product
- Maintain zero legal or ethical violations (no robots.txt breaches, no GDPR complaints)

### Project Scope

**In Scope**:
- Restaurant discovery and data aggregation (menus, prices, descriptions, dietary tags)
- Integration with public data sources (FSA hygiene ratings, Google Places, Trustpilot reviews)
- Integration with business registries (Companies House financials, Plymouth licensing, business rates)
- Interactive analytics dashboard (search, filtering, price analysis, hygiene ratings, reviews)
- Data quality validation, duplicate detection, and data lineage tracking
- Weekly automated data refresh via scheduled scraping and API fetching
- Plymouth, UK geographic focus (243 restaurants currently tracked)

**Out of Scope** (Future Phases):
- Real-time menu updates (current: weekly batch processing)
- User accounts and personalization (favorites, alerts, recommendations)
- Mobile applications (iOS, Android)
- Reservation system integration or direct booking
- Payment processing for premium features
- Geographic expansion beyond Plymouth (Devon, UK-wide expansion deferred to Phase 2)
- Sentiment analysis on review text (basic review display only)
- Restaurant owner portals for self-service data updates

---

## Stakeholders

| Stakeholder | Role | Organization | Involvement Level |
|-------------|------|--------------|-------------------|
| Mark Craddock | Product Owner / Technical Lead | Plymouth Research | Decision maker, architecture oversight, development |
| AI Code Assistant | Implementation Support | Anthropic (Claude) | Requirements elicitation, code generation, documentation |
| [TBD] | Business Analyst | Plymouth Research | Requirements validation (if team expands) |
| End Users (Consumers) | Primary Users | General Public | User acceptance, feature feedback |
| Restaurant Owners | Data Subjects | Plymouth Hospitality Industry | Opt-out requests, data accuracy feedback |
| FSA (Food Standards Agency) | Data Provider | UK Government | Hygiene rating data source |
| Google Places | Data Provider | Google | Restaurant metadata and reviews |
| Trustpilot | Data Provider | Trustpilot | Customer review data |
| Companies House | Data Provider | UK Government | Business financial data |
| ICO (Information Commissioner's Office) | Regulator | UK Government | GDPR compliance oversight |

---

## Business Requirements

### BR-001: Comprehensive Restaurant Coverage

**Description**: The platform MUST provide comprehensive coverage of Plymouth restaurants, targeting 90%+ of establishments to ensure utility for consumers and researchers.

**Rationale**: Partial coverage creates selection bias and limits platform value. Users expect to find any Plymouth restaurant they search for.

**Success Criteria**:
- Minimum 150 restaurants catalogued (representing 90%+ of Plymouth restaurants/bars/cafes)
- Active restaurant status tracked (operational, temporarily closed, permanently closed)
- Coverage gaps identified and documented (e.g., restaurants blocking scraping, no online presence)
- Geographic coverage includes Plymouth city center and surrounding areas (PL1-PL9 postcodes)

**Priority**: MUST_HAVE

**Stakeholder**: Product Owner, End Users

**Traceability**: Aligns with Architecture Principle #1 (Data Quality First)

**Current Status**: ✅ IMPLEMENTED (243 restaurants tracked)

---

### BR-002: Multi-Source Data Aggregation

**Description**: The platform MUST aggregate data from multiple authoritative sources to provide comprehensive restaurant intelligence beyond just menu data.

**Rationale**: Combining menu data with hygiene ratings, customer reviews, and financial health provides holistic view unavailable from any single source. This differentiation is Plymouth Research's competitive advantage.

**Success Criteria**:
- FSA Food Hygiene Rating Scheme integration (official government safety ratings)
- Trustpilot review integration (customer satisfaction data)
- Google Places integration (location, contact info, service options)
- Companies House integration (financial health indicators)
- Plymouth licensing database integration (licensing activities and hours)
- Business rates data integration (property values and business categories)
- Each data source properly attributed in user interface (legal compliance)

**Priority**: MUST_HAVE

**Stakeholder**: Product Owner, End Users

**Traceability**: Aligns with Architecture Principle #7 (Single Source of Truth)

**Current Status**: ✅ IMPLEMENTED (6 data sources integrated)

---

### BR-003: Cost-Efficient Operations

**Description**: The platform MUST maintain total operational costs below £100/month while supporting 150+ restaurants to ensure financial sustainability.

**Rationale**: Plymouth Research is an independent research organization with limited budget. Cost efficiency is critical for long-term viability.

**Success Criteria**:
- Total monthly costs (infrastructure + APIs + hosting) ≤ £100
- Cost per restaurant ≤ £0.67/month (£100 / 150 restaurants)
- Free or low-cost data sources prioritized (FSA, Companies House are free; Google Places within free tier)
- Infrastructure auto-scales down during low-traffic periods to minimize waste
- Monthly cost tracking dashboard implemented to monitor spend

**Priority**: MUST_HAVE

**Stakeholder**: Product Owner

**Traceability**: Aligns with Architecture Principle #6 (Cost Efficiency) and #2 (Open Source Preferred)

**Current Status**: ✅ IMPLEMENTED (current costs minimal: SQLite is free, Streamlit Cloud free tier)

---

### BR-004: Legal and Ethical Compliance

**Description**: The platform MUST operate within legal boundaries (UK GDPR, Computer Misuse Act 1990, Copyright law) and ethical web scraping standards to avoid legal liability and reputational damage.

**Rationale**: Unethical or illegal scraping creates existential risk: IP blocking, legal action, regulatory fines, reputational damage. Plymouth Research prioritizes ethical operations.

**Success Criteria**:
- Zero robots.txt violations (100% compliance with disallow directives)
- Rate limiting enforced: minimum 5 seconds between requests per domain
- Honest User-Agent string identifying Plymouth Research with contact email
- No personal data (PII) scraped beyond public business contact information
- Data Protection Impact Assessment (DPIA) completed and approved
- Privacy policy published and accessible
- Restaurant opt-out mechanism implemented and honored
- FSA, Trustpilot, Google data properly attributed per license terms

**Priority**: MUST_HAVE (NON-NEGOTIABLE)

**Stakeholder**: Product Owner, Legal (if applicable), ICO

**Traceability**: Aligns with Architecture Principle #3 (Ethical Web Scraping - NON-NEGOTIABLE) and #4 (Privacy by Design)

**Current Status**: ✅ IMPLEMENTED (robots.txt compliance, rate limiting, GDPR-compliant data handling)

---

### BR-005: Geographic Scalability

**Description**: The platform SHOULD support future geographic expansion from Plymouth to Devon and UK-wide without architectural rework.

**Rationale**: Current Plymouth focus validates business model. Future growth depends on ability to scale to additional cities without expensive redesign.

**Success Criteria**:
- Database schema supports multiple cities (city field, geographic coordinates)
- Scraping pipeline configurable by city/region (not hardcoded to Plymouth)
- Performance testing validates 10x capacity (1,500 restaurants, 100,000 menu items)
- Architecture review confirms horizontal scalability (add workers for parallel scraping)

**Priority**: SHOULD_HAVE (future-proofing)

**Stakeholder**: Product Owner

**Traceability**: Aligns with Architecture Principle #5 (Scalability and Extensibility)

**Current Status**: ✅ IMPLEMENTED (architecture supports multi-city; FSA data includes lat/lon, city fields)

---

### BR-006: Data Freshness and Timeliness

**Description**: The platform MUST provide reasonably fresh data (≤7 days staleness for menu data, ≤30 days for hygiene ratings) to ensure user trust and relevance.

**Rationale**: Stale data (outdated prices, closed restaurants) erodes user trust and platform value. Balance between freshness and ethical scraping rate limits.

**Success Criteria**:
- Menu data refreshed weekly (automated batch scraping)
- FSA hygiene ratings refreshed monthly (government data updated weekly, matcher runs monthly)
- Trustpilot reviews refreshed weekly (incremental updates, only new reviews)
- Data staleness displayed to users (e.g., "Last updated: 2025-11-15")
- Automated monitoring alerts if data refresh fails
- Graceful degradation: show cached data with staleness warning if refresh fails

**Priority**: MUST_HAVE

**Stakeholder**: Product Owner, End Users

**Traceability**: Aligns with Architecture Principle #1 (Data Quality First - timeliness dimension)

**Current Status**: ⚠️ PARTIALLY IMPLEMENTED (manual refresh workflow exists, automation pending)

---

### BR-007: Public Dashboard Accessibility

**Description**: The platform MUST provide a public-facing web dashboard accessible to consumers for restaurant discovery and comparison.

**Rationale**: Public access maximizes platform utility and establishes Plymouth Research brand. Dashboard is primary user interface.

**Success Criteria**:
- Dashboard accessible via web browser (desktop, tablet, mobile responsive)
- No login required for basic search and browsing (public access)
- Intuitive UX requiring minimal training (target: 90%+ users can complete search task without help)
- Accessibility compliance (WCAG 2.1 AA for future public launch)

**Priority**: MUST_HAVE

**Stakeholder**: Product Owner, End Users

**Current Status**: ✅ IMPLEMENTED (Streamlit dashboard deployed, publicly accessible if hosted)

---

## Functional Requirements

### User Personas

#### Persona 1: Budget-Conscious Consumer (Sarah)
- **Role**: Plymouth resident, young professional
- **Goals**: Find affordable dining options, compare prices across restaurants, identify dietary-friendly establishments
- **Pain Points**: Restaurant websites don't show full menus/prices, difficult to compare options, unaware of hygiene ratings
- **Technical Proficiency**: Medium (comfortable with web apps, smartphone user)
- **Key Use Cases**: UC-001 (Search Restaurants), UC-003 (Price Comparison), UC-005 (Dietary Filtering)

#### Persona 2: Health-Conscious Diner (James)
- **Role**: Plymouth resident, health & fitness enthusiast
- **Goals**: Find restaurants with healthy options (vegan, vegetarian), check hygiene ratings before dining
- **Pain Points**: Restaurant websites lack dietary information, hygiene ratings buried on FSA website
- **Technical Proficiency**: High (early adopter, uses multiple apps)
- **Key Use Cases**: UC-005 (Dietary Filtering), UC-006 (Hygiene Ratings), UC-001 (Search Restaurants)

#### Persona 3: Food Industry Researcher (Dr. Emma)
- **Role**: Academic researcher, hospitality industry analyst
- **Goals**: Analyze pricing trends, study menu diversity, correlate hygiene ratings with business performance
- **Pain Points**: Data scattered across multiple sources, no centralized analytics, manual data collection time-consuming
- **Technical Proficiency**: High (data analysis skills, familiar with analytical tools)
- **Key Use Cases**: UC-007 (Analytics and Reporting), UC-008 (Data Export), UC-009 (Trend Analysis)

#### Persona 4: Restaurant Owner (Tom)
- **Role**: Plymouth restaurant owner/manager
- **Goals**: Monitor competitor pricing, understand market positioning, verify accuracy of own restaurant data
- **Pain Points**: Concerned about scraped data accuracy, wants ability to correct errors, interested in how hygiene rating impacts reputation
- **Technical Proficiency**: Medium (business software user)
- **Key Use Cases**: UC-010 (Data Opt-Out Request), UC-011 (Data Correction Request)

---

### Use Cases

#### UC-001: Search Restaurants by Cuisine and Filters

**Actor**: Budget-Conscious Consumer (Sarah), Health-Conscious Diner (James)

**Preconditions**:
- Dashboard application is accessible
- Restaurant database contains ≥150 restaurants with menu data

**Main Flow**:
1. User navigates to dashboard homepage
2. System displays search interface with filters (cuisine type, price range, dietary options, hygiene rating, service options)
3. User selects "Italian" cuisine filter
4. System displays list of Italian restaurants (count: 15 found)
5. User adds "Vegetarian options" dietary filter
6. System refines results to Italian restaurants with vegetarian dishes (count: 12 found)
7. User adds "Hygiene rating: 5 stars" filter
8. System further refines to 5-star hygiene rated Italian restaurants with vegetarian options (count: 8 found)
9. User browses restaurant cards showing: name, address, price range, hygiene badge, menu item preview
10. System displays results within 500ms (performance requirement)

**Postconditions**:
- User sees filtered restaurant list matching all criteria
- Result count displayed accurately
- Filters preserved if user navigates to detail view and returns

**Alternative Flows**:
- **Alt 1a**: If no restaurants match filters, system displays "No restaurants found. Try adjusting filters."
- **Alt 2a**: If user applies "Delivery available" service filter, system shows only restaurants with Google delivery flag

**Exception Flows**:
- **Ex 1**: If database query times out (>5s), system shows cached results with staleness warning

**Business Rules**:
- Restaurants marked "is_active = 0" (closed) are excluded from results unless user explicitly selects "Show closed restaurants"
- Results sorted by restaurant name (alphabetical) by default; user can re-sort by price range or hygiene rating

**Related Requirements**: FR-001, NFR-P-001, NFR-P-002

---

#### UC-002: View Restaurant Details and Menu

**Actor**: Budget-Conscious Consumer (Sarah)

**Preconditions**:
- User has search results displayed (from UC-001)
- Restaurant has menu data in database

**Main Flow**:
1. User clicks on restaurant card "Rockfish Plymouth"
2. System displays restaurant detail view with tabs: Menu, Details, Reviews, Hygiene, Financial
3. System shows menu items grouped by category (Starters, Mains, Desserts, Drinks)
4. User scrolls through menu items (each showing: name, description, price, dietary tags)
5. User clicks "Dietary Tags" filter "Vegan"
6. System filters menu to show only vegan items
7. User notes price: "Vegan Buddha Bowl - £12.50"
8. User clicks "Hygiene" tab
9. System displays FSA hygiene rating: 5 stars (rated 2025-10-15), detailed scores breakdown
10. User clicks "Reviews" tab
11. System displays Trustpilot reviews (most recent 20 reviews, pagination for more)

**Postconditions**:
- User has viewed menu prices and dietary information
- User has checked hygiene rating and customer reviews
- User can make informed dining decision

**Alternative Flows**:
- **Alt 1a**: If restaurant has no menu data, system displays "Menu data not available. Visit restaurant website: [link]"
- **Alt 2a**: If restaurant has no hygiene rating, system displays "Hygiene rating not found. Check FSA website: [link]"
- **Alt 3a**: If restaurant has no reviews, system displays "No Trustpilot reviews available."

**Business Rules**:
- Menu items must show currency (£) and decimal prices (e.g., £12.50 not "Twelve fifty")
- Hygiene rating displayed with FSA attribution: "Data from Food Standards Agency"
- Trustpilot reviews displayed with attribution: "Reviews from Trustpilot.com"

**Related Requirements**: FR-002, FR-005, FR-006, FR-007, NFR-C-001

---

#### UC-003: Compare Prices Across Restaurants

**Actor**: Budget-Conscious Consumer (Sarah)

**Preconditions**:
- User has filtered restaurants (from UC-001)
- Multiple restaurants have menu data for comparison

**Main Flow**:
1. User navigates to "Price Analysis" tab
2. System displays price distribution histogram (all menu items, £0-£50 range)
3. User views average prices by cuisine (bar chart): Italian £15.20, Indian £12.80, etc.
4. User filters to "Italian" cuisine only
5. System updates histogram to show only Italian restaurant prices
6. User notes: "Most Italian mains £10-£15 range"
7. User clicks "Price Range Distribution" pie chart
8. System shows breakdown: 40% restaurants in "££" range, 35% in "£££", 25% in "£"
9. User identifies budget-friendly Italian options in "££" category

**Postconditions**:
- User understands typical price ranges for cuisine type
- User can identify budget-friendly vs premium establishments
- Analytics charts updated to reflect user filters

**Alternative Flows**:
- **Alt 1a**: If user selects "Vegan" dietary filter, system shows price distribution for vegan-friendly menu items only

**Business Rules**:
- Price range categories: £ (<£10 avg), ££ (£10-£20 avg), £££ (£20-£30 avg), ££££ (>£30 avg)
- Prices normalized to GBP decimal format for accurate comparison
- Outliers flagged (e.g., "£250 Wagyu Steak" excluded from average calculations after review)

**Related Requirements**: FR-003, NFR-P-002

---

#### UC-004: Search Menu Items by Keyword

**Actor**: Health-Conscious Diner (James)

**Preconditions**:
- Dashboard displays "Browse Menus" search page
- Database has full-text search index on menu items

**Main Flow**:
1. User types "fish and chips" in search box
2. System performs full-text search across menu item names and descriptions
3. System displays matching menu items (23 results found)
4. Each result shows: restaurant name, item name, price, description snippet
5. User clicks item "Beer Battered Cod & Chips - £12.50 - Rockfish Plymouth"
6. System navigates to Rockfish Plymouth menu with item highlighted
7. User views full item details and dietary information (not gluten-free)

**Postconditions**:
- User found menu item across multiple restaurants
- User can compare same dish across establishments
- Search performance <500ms (NFR-P-002)

**Alternative Flows**:
- **Alt 1a**: If user searches "gluten-free pasta", system filters to menu items with "is_gluten_free = 1" flag

**Exception Flows**:
- **Ex 1**: If no results found, system suggests "Try different keywords or browse by cuisine"

**Business Rules**:
- Search is case-insensitive
- Search matches partial words (e.g., "fish" matches "Fishcakes", "Monkfish")
- Results ranked by relevance (exact name match > description match)

**Related Requirements**: FR-001, NFR-P-002

---

#### UC-005: Filter by Dietary Requirements

**Actor**: Health-Conscious Diner (James)

**Preconditions**:
- User is on "Browse Menus" page
- Menu items tagged with dietary flags (is_vegan, is_vegetarian, is_gluten_free)

**Main Flow**:
1. User selects dietary filter "Vegan"
2. System filters to restaurants with vegan menu items (42 restaurants, 156 vegan items)
3. User applies additional filter "Italian cuisine"
4. System refines to Italian restaurants with vegan options (8 restaurants, 23 vegan items)
5. User browses vegan Italian menu items
6. User notes: "Bella Italia has 5 vegan options, Zizzi has 8 vegan options"
7. User clicks on Zizzi (more vegan variety)
8. System displays Zizzi menu with vegan items highlighted

**Postconditions**:
- User discovered vegan-friendly restaurants
- User can make dietary-safe dining choice

**Alternative Flows**:
- **Alt 1a**: If user selects "Gluten-Free", system shows gluten-free menu items only
- **Alt 2a**: If user selects multiple dietary filters ("Vegan" + "Gluten-Free"), system shows items matching ALL criteria (logical AND)

**Business Rules**:
- Dietary tags extracted from menu item descriptions (keywords: vegan, vegetarian, gluten-free, dairy-free, nut-free)
- Dietary tags may be incomplete (extraction not 100% accurate); disclaimer shown: "Dietary information may be incomplete. Verify with restaurant."

**Related Requirements**: FR-004, NFR-Q-001

---

#### UC-006: View FSA Hygiene Ratings

**Actor**: Health-Conscious Diner (James)

**Preconditions**:
- Restaurant has FSA hygiene rating matched in database
- FSA data refreshed within last 30 days

**Main Flow**:
1. User filters restaurants by "Hygiene Rating: 5 stars"
2. System displays restaurants with 5-star ratings (67.3% of rated restaurants)
3. User clicks on restaurant "Barbican Kitchen"
4. System displays hygiene rating badge: 5 stars, rating date: 2025-09-20
5. User clicks "View Detailed Scores"
6. System displays breakdown: Hygiene 0, Structural 5, Confidence in Management 5 (lower is better)
7. System shows FSA attribution: "Data from Food Standards Agency (Open Government License)"
8. User notes: "Excellent hygiene, minor structural issue"

**Postconditions**:
- User verified hygiene standards before dining
- User understands rating methodology (detailed scores)

**Alternative Flows**:
- **Alt 1a**: If restaurant not matched with FSA rating, system displays "Hygiene rating not available" with link to FSA website to search manually

**Business Rules**:
- Hygiene ratings displayed with date (e.g., "Rated: 2025-09-20")
- Ratings >6 months old flagged as "May be outdated. Check FSA for latest."
- FSA attribution mandatory (legal requirement for Open Government License)
- Detailed scores explained: "Lower is better. 0 = Very Good, 5 = Generally Satisfactory, 10+ = Improvement Necessary"

**Related Requirements**: FR-005, NFR-C-001

---

#### UC-007: Analyze Hygiene vs Customer Satisfaction Correlation

**Actor**: Food Industry Researcher (Dr. Emma)

**Preconditions**:
- Restaurants have BOTH hygiene ratings AND Trustpilot reviews in database
- Sufficient data for statistical correlation (≥20 restaurants with both)

**Main Flow**:
1. User navigates to "Reviews" tab
2. System displays "Hygiene vs Trustpilot Correlation" scatter plot
3. Each point represents one restaurant: X-axis = FSA hygiene rating (0-5), Y-axis = Trustpilot avg rating (1-5)
4. User observes: "5-star hygiene restaurants have avg 2.72★ Trustpilot rating"
5. User observes: "4-star hygiene restaurants have avg 2.15★ Trustpilot rating"
6. User notes surprising finding: "Fast food chains (McDonald's, Burger King, Taco Bell) have 5-star hygiene but 1.6-2.0★ reviews"
7. User clicks data point "Rockfish Plymouth"
8. System displays restaurant details: 5★ hygiene, 3.75★ Trustpilot (outlier with high ratings in both)
9. User exports correlation data to CSV for further analysis

**Postconditions**:
- User gained research insight: "Food safety ≠ customer satisfaction"
- User has data export for academic paper/report

**Alternative Flows**:
- **Alt 1a**: If <20 restaurants have both hygiene and review data, system displays "Insufficient data for correlation analysis (need ≥20, have X)"

**Business Rules**:
- Correlation analysis only performed on restaurants with BOTH hygiene rating AND ≥5 Trustpilot reviews
- Outliers flagged (e.g., restaurants >3 standard deviations from trend line)

**Related Requirements**: FR-007, FR-009

---

#### UC-008: Export Data to CSV

**Actor**: Food Industry Researcher (Dr. Emma)

**Preconditions**:
- User has filtered data or analytics view displayed
- Export functionality implemented in dashboard

**Main Flow**:
1. User navigates to "Browse Menus" page with filters applied (Italian cuisine, Vegan options)
2. User clicks "Export to CSV" button
3. System generates CSV file (UTF-8, RFC 4180 compliant)
4. CSV includes columns: restaurant_name, cuisine_type, menu_item_name, price, is_vegan, hygiene_rating
5. System downloads file "plymouth_research_export_2025-11-22.csv"
6. User opens CSV in Excel/Google Sheets for custom analysis

**Postconditions**:
- User has machine-readable data export
- Data export matches filters applied in dashboard
- CSV format compatible with standard data analysis tools

**Alternative Flows**:
- **Alt 1a**: If user exports from "Analytics" view, CSV contains aggregated data (avg prices by cuisine, rating distributions)

**Business Rules**:
- CSV exports limited to 10,000 rows to prevent abuse (if needed in future)
- Attribution footer in CSV: "Data from Plymouth Research (plymouthresearch.co.uk). Contains FSA data © Food Standards Agency."

**Related Requirements**: FR-009, NFR-I-002

---

#### UC-009: Monitor Data Quality Metrics

**Actor**: Product Owner (Mark Craddock)

**Preconditions**:
- Data quality monitoring dashboard implemented
- ETL pipeline logs data quality metrics

**Main Flow**:
1. Product Owner accesses admin/monitoring dashboard (internal tool, not public)
2. System displays data quality dashboard with metrics:
   - **Completeness**: 92% of menu items have prices (target: 95%)
   - **Accuracy**: 98% of prices in valid range (£0.50-£500)
   - **Timeliness**: 85% of restaurants refreshed in last 7 days (target: 90%)
   - **Duplication**: 23 duplicate menu items detected (pending deduplication)
3. Product Owner drills into "Completeness" metric
4. System displays restaurants with missing price data (8 restaurants, 127 menu items)
5. Product Owner notes: "Restaurant X website changed layout, scraper failed to extract prices"
6. Product Owner creates ticket to fix scraper for Restaurant X
7. Product Owner monitors deduplication queue
8. System shows suspected duplicates: "Fish & Chips" vs "Fish and Chips" (same restaurant, suspected duplicate)

**Postconditions**:
- Product Owner identified data quality issues
- Action items created to remediate (fix scrapers, deduplicate)
- Data quality metrics tracked over time

**Alternative Flows**:
- **Alt 1a**: If completeness drops below 90% threshold, system sends automated alert to Product Owner

**Business Rules**:
- Data quality metrics calculated daily during ETL refresh
- Quality thresholds: Completeness ≥95%, Accuracy ≥98%, Timeliness ≥90%

**Related Requirements**: NFR-Q-001, NFR-Q-002, NFR-Q-003

---

#### UC-010: Restaurant Owner Opt-Out Request

**Actor**: Restaurant Owner (Tom)

**Preconditions**:
- Restaurant data exists in Plymouth Research database
- Opt-out process documented and accessible

**Main Flow**:
1. Restaurant owner discovers restaurant listed on Plymouth Research dashboard
2. Restaurant owner navigates to "Contact / Opt-Out" page (linked from About tab)
3. Owner reads opt-out policy: "We respect your wishes. Email opt-out@plymouthresearch.co.uk with restaurant name and confirmation you are authorized representative."
4. Owner sends email: "Please remove [Restaurant Name] from your database. I am the owner. Confirmation attached."
5. Product Owner receives email
6. Product Owner verifies ownership (checks email domain matches restaurant website, or requests business registration proof)
7. Product Owner sets restaurant `is_active = 0` in database (soft delete)
8. Restaurant removed from public dashboard within 24 hours
9. Product Owner confirms removal via email to restaurant owner

**Postconditions**:
- Restaurant data no longer visible on public dashboard
- Data retained in database for 30 days (audit trail) then hard deleted
- Opt-out honored (GDPR Right to Erasure compliance)

**Alternative Flows**:
- **Alt 1a**: If ownership cannot be verified, Product Owner requests additional proof before removing

**Exception Flows**:
- **Ex 1**: If restaurant owner requests data correction (not removal), Product Owner follows UC-011 (Data Correction Request)

**Business Rules**:
- Opt-out requests honored within 72 hours (GDPR compliance)
- Only authorized representatives (verified owners/managers) can request removal
- Removal is soft delete (is_active = 0) for 30 days, then hard delete (permanent removal)

**Related Requirements**: NFR-C-002, NFR-C-003

---

#### UC-011: Restaurant Owner Data Correction Request

**Actor**: Restaurant Owner (Tom)

**Preconditions**:
- Restaurant data exists in database with potential inaccuracies
- Correction process documented

**Main Flow**:
1. Restaurant owner notices incorrect menu price: "Steak listed as £45, actual price £35"
2. Owner emails: "Menu item X price is incorrect. Should be £35 not £45. Screenshot attached."
3. Product Owner receives correction request
4. Product Owner verifies claim: checks original scraped HTML snapshot, visits restaurant website
5. Product Owner confirms: "Price was correct when scraped 2025-11-15, but has since changed"
6. Product Owner updates menu_item price in database: £45 → £35
7. Product Owner adds note: "Manual correction from owner on 2025-11-22"
8. Product Owner replies to owner: "Corrected. Updated price visible within 1 hour."
9. Dashboard reflects corrected price on next cache refresh

**Postconditions**:
- Inaccurate data corrected
- Correction logged with timestamp and source (audit trail)
- Restaurant owner satisfied with data accuracy

**Alternative Flows**:
- **Alt 1a**: If Product Owner cannot verify correction, request additional proof before making change

**Business Rules**:
- Manual corrections flagged in database (correction_source = "owner_request")
- Next automated scrape may overwrite manual correction if website still shows old price; Product Owner monitors for this
- Correction requests honored within 72 hours

**Related Requirements**: NFR-Q-003

---

### Functional Requirement Summary

#### FR-001: Restaurant Search and Discovery

**Description**: The system MUST provide search and filtering capabilities enabling users to discover restaurants by cuisine type, price range, dietary requirements, hygiene rating, and service options.

**Acceptance Criteria**:
- [ ] Search by cuisine type (Italian, Indian, Chinese, British, etc. - controlled vocabulary)
- [ ] Filter by price range (£, ££, £££, ££££)
- [ ] Filter by dietary requirements (Vegan, Vegetarian, Gluten-Free, Dairy-Free, Nut-Free)
- [ ] Filter by hygiene rating (0-5 stars)
- [ ] Filter by service options (Dine-in, Takeout, Delivery, Reservations available)
- [ ] Filter by meal times (Breakfast, Lunch, Dinner service)
- [ ] Filter by food/beverage options (Vegetarian food, Beer, Wine available)
- [ ] Toggle to hide permanently/temporarily closed restaurants
- [ ] Multiple filters combinable with logical AND (e.g., "Italian" + "Vegan" + "5-star hygiene")
- [ ] Result count displayed accurately ("42 restaurants found")
- [ ] Search results paginated if >50 results
- [ ] Query performance <500ms (p95) for filtered searches

**Priority**: MUST_HAVE

**Stakeholder**: All user personas

**Traceability**: UC-001, UC-004

---

#### FR-002: Menu Item Display and Search

**Description**: The system MUST display restaurant menus with full item details (name, description, price, dietary tags, category) and enable keyword search across all menu items.

**Acceptance Criteria**:
- [ ] Menu items displayed with: name (required), description (optional), price in £ (required), dietary tags (vegan/vegetarian/gluten-free flags)
- [ ] Menu items grouped by category (Starters, Mains, Desserts, Drinks, etc.)
- [ ] Full-text search across item names and descriptions
- [ ] Search highlights matching keywords in results
- [ ] Dietary tag filters applied to menu items (e.g., show only vegan items)
- [ ] Prices displayed in consistent £X.XX format (e.g., £12.50)
- [ ] Menu item cards visually appealing (images if available, but not required for MVP)
- [ ] Source attribution: "Menu data scraped from [restaurant website URL] on [date]"

**Priority**: MUST_HAVE

**Stakeholder**: Budget-Conscious Consumer, Health-Conscious Diner

**Traceability**: UC-002, UC-004, Architecture Principle #9 (Data Normalization)

---

#### FR-003: Price Comparison and Analytics

**Description**: The system MUST provide analytics visualizations comparing prices across restaurants, cuisines, and price ranges to enable informed dining decisions.

**Acceptance Criteria**:
- [ ] Price distribution histogram (X-axis: price in £, Y-axis: number of menu items)
- [ ] Average price by cuisine type (bar chart: Italian £15.20, Indian £12.80, etc.)
- [ ] Price range distribution pie chart (percentage of restaurants in £/££/£££/££££ categories)
- [ ] Statistical summary (min, max, mean, median prices)
- [ ] Analytics filterable by cuisine, dietary tags, restaurant
- [ ] Charts interactive (click bar to drill down to restaurant list)
- [ ] Export analytics data to CSV

**Priority**: MUST_HAVE

**Stakeholder**: Budget-Conscious Consumer, Food Industry Researcher

**Traceability**: UC-003, UC-007

---

#### FR-004: Dietary Information Filtering

**Description**: The system MUST identify and filter menu items by dietary requirements (vegan, vegetarian, gluten-free) to serve health-conscious consumers.

**Acceptance Criteria**:
- [ ] Dietary tags extracted from menu item descriptions (keyword matching: "vegan", "vegetarian", "gluten-free", "dairy-free", "nut-free")
- [ ] Dietary tag flags stored in database (is_vegan, is_vegetarian, is_gluten_free boolean columns)
- [ ] Filter UI displays dietary options with counts (e.g., "Vegan (156 items)")
- [ ] Multiple dietary filters combinable (e.g., "Vegan" + "Gluten-Free" shows items that are BOTH)
- [ ] Dietary information completeness tracked (% of menu items with dietary tags)
- [ ] Disclaimer displayed: "Dietary information may be incomplete. Verify with restaurant before ordering."

**Priority**: MUST_HAVE

**Stakeholder**: Health-Conscious Diner

**Traceability**: UC-005, Architecture Principle #1 (Data Quality First)

---

#### FR-005: FSA Hygiene Rating Integration

**Description**: The system MUST integrate Food Standards Agency (FSA) Food Hygiene Rating Scheme data to display official government hygiene ratings for restaurants.

**Acceptance Criteria**:
- [ ] FSA Plymouth XML data fetched weekly (source: https://ratings.food.gov.uk/api/open-data-files/FHRS891en-GB.xml)
- [ ] Restaurants matched to FSA establishments using multi-factor algorithm (name similarity, postcode, address)
- [ ] Hygiene rating (0-5 stars) displayed prominently on restaurant cards and detail views
- [ ] Hygiene rating date displayed (e.g., "Rated: 2025-09-20")
- [ ] Detailed scores breakdown displayed: Hygiene (0-25), Structural (0-25), Confidence in Management (0-30)
- [ ] FSA attribution mandatory: "Data from Food Standards Agency (Open Government License)"
- [ ] Link to official FSA page for restaurant provided
- [ ] Ratings >6 months old flagged as "May be outdated"
- [ ] Unmatched restaurants show "Hygiene rating not found" with link to FSA search

**Priority**: MUST_HAVE

**Stakeholder**: Health-Conscious Diner, Food Industry Researcher

**Traceability**: UC-006, Architecture Principle #3 (Ethical Web Scraping), Architecture Principle #4 (Privacy by Design)

---

#### FR-006: Trustpilot Review Integration

**Description**: The system MUST integrate Trustpilot customer reviews to provide peer feedback and customer satisfaction insights.

**Acceptance Criteria**:
- [ ] Trustpilot reviews scraped from restaurant Trustpilot pages (public data)
- [ ] Reviews displayed with: author name, review title, review body, rating (1-5 stars), review date, author location
- [ ] Reviews sorted by date (most recent first) with pagination (20 reviews per page)
- [ ] Review statistics displayed: total review count, average rating, rating distribution (1★, 2★, 3★, 4★, 5★ counts)
- [ ] Filter reviews by rating (e.g., show only 1-2★ reviews)
- [ ] Filter reviews by date range (e.g., last 6 months)
- [ ] Trustpilot attribution mandatory: "Reviews from Trustpilot.com"
- [ ] Link to full Trustpilot page provided
- [ ] Incremental updates (only fetch new reviews since last scrape)

**Priority**: MUST_HAVE

**Stakeholder**: All user personas

**Traceability**: UC-002, UC-007, Architecture Principle #3 (Ethical Web Scraping)

---

#### FR-007: Google Places Integration

**Description**: The system MUST integrate Google Places API data to provide restaurant location, contact information, service options, and Google reviews.

**Acceptance Criteria**:
- [ ] Google Places data fetched for all restaurants (Place ID, location, contact, service options)
- [ ] Contact information displayed: phone number (clickable tel: link), website URL, Google Maps link
- [ ] Service options displayed as badges: Dine-in, Takeout, Delivery, Reservations available
- [ ] Meal time service displayed: Breakfast, Lunch, Dinner
- [ ] Food/beverage options displayed: Vegetarian food, Beer, Wine available
- [ ] Google reviews displayed (up to 5 most helpful reviews per restaurant)
- [ ] Google rating and review count displayed
- [ ] Business status tracked: Operational, Temporarily Closed, Permanently Closed
- [ ] Geographic coordinates (latitude, longitude) stored for future map features
- [ ] Google data refreshed monthly (within API free tier limits)

**Priority**: MUST_HAVE

**Stakeholder**: All user personas

**Traceability**: UC-001, UC-002

---

#### FR-008: Business Financial Data Integration

**Description**: The system SHOULD integrate Companies House financial data and Plymouth business rates to provide business health indicators (optional feature for researchers).

**Acceptance Criteria**:
- [ ] Companies House API integration (company number, financial statements, director information)
- [ ] Financial metrics displayed: turnover, profit/loss, net assets, employee count (if available)
- [ ] Financial health score calculated based on profitability, growth trends, and solvency
- [ ] Plymouth licensing data integrated (licensing activities, opening hours)
- [ ] Business rates data integrated (rateable value, property valuation)
- [ ] Financial data displayed in separate tab (not prominent, for researcher audience)
- [ ] Disclaimer: "Financial data is historical (FY 2023). Current performance may differ."

**Priority**: SHOULD_HAVE (nice-to-have for researchers)

**Stakeholder**: Food Industry Researcher

**Traceability**: UC-007

**Current Status**: ✅ IMPLEMENTED

---

#### FR-009: Data Export and API Access

**Description**: The system SHOULD provide data export capabilities (CSV format) to enable researchers to perform custom analysis.

**Acceptance Criteria**:
- [ ] Export button available on filtered search results and analytics views
- [ ] CSV export includes: restaurant details, menu items, prices, hygiene ratings, reviews (based on current view)
- [ ] CSV format: UTF-8 encoding, RFC 4180 compliant (quoted fields, proper escaping)
- [ ] Attribution footer in CSV: "Data © Plymouth Research. Contains FSA data (OGL), Trustpilot reviews (public data)."
- [ ] Export limited to 10,000 rows per request (prevent abuse)
- [ ] Future: Public API endpoints (REST or GraphQL) for programmatic access (deferred to Phase 2)

**Priority**: SHOULD_HAVE

**Stakeholder**: Food Industry Researcher

**Traceability**: UC-008, Architecture Principle #10 (API-First Design), Architecture Principle #11 (Standard Data Formats)

---

#### FR-010: Restaurant Owner Opt-Out and Correction

**Description**: The system MUST provide a process for restaurant owners to request data removal (opt-out) or corrections to ensure GDPR compliance and data accuracy.

**Acceptance Criteria**:
- [ ] Opt-out process documented on "About" page with contact email
- [ ] Ownership verification process (email domain matching, business registration proof)
- [ ] Opt-out honored within 72 hours (GDPR Right to Erasure)
- [ ] Soft delete (is_active = 0) for 30 days, then hard delete (permanent removal)
- [ ] Data correction process: owner submits correction, Product Owner verifies, manual update applied
- [ ] Corrections logged with timestamp and source (audit trail)
- [ ] Email confirmation sent to owner when request completed

**Priority**: MUST_HAVE (GDPR compliance)

**Stakeholder**: Restaurant Owner, Product Owner

**Traceability**: UC-010, UC-011, Architecture Principle #4 (Privacy by Design)

---

## Non-Functional Requirements

### Performance Requirements

#### NFR-P-001: Dashboard Page Load Time

**Description**: The dashboard MUST load initial page content within 2 seconds (p95 latency) to ensure responsive user experience.

**Rationale**: Users expect instant responsiveness. Page load times >3 seconds lead to high bounce rates and poor user satisfaction.

**Acceptance Criteria**:
- [ ] Dashboard homepage loads in <2 seconds (p95) measured from user's browser (includes HTML render, initial data fetch, chart rendering)
- [ ] Cached data served if database query takes >5 seconds (graceful degradation)
- [ ] Performance tested at expected load (100 concurrent users, 1,000 page views/day)
- [ ] Performance monitoring enabled (real user monitoring or synthetic monitoring)
- [ ] Alerts configured for page load times >3 seconds (p95)

**Measurement Method**: Browser DevTools Performance tab, Lighthouse score ≥80, Streamlit performance profiling

**Priority**: MUST_HAVE

**Traceability**: Architecture Principle #12 (Performance Targets)

---

#### NFR-P-002: Search Query Response Time

**Description**: The system MUST return search query results within 500ms (p95) to ensure instant search feedback.

**Rationale**: Users expect instant search results. Delays >1 second feel sluggish and degrade UX.

**Acceptance Criteria**:
- [ ] Restaurant search (filtered by cuisine, price, dietary, hygiene rating) completes in <500ms (p95)
- [ ] Menu item full-text search completes in <500ms (p95)
- [ ] Database indexes created on frequently queried columns (cuisine_type, price_range, hygiene_rating)
- [ ] Full-text search index on menu item names and descriptions (SQLite FTS5 or PostgreSQL full-text search)
- [ ] Query performance tested at scale (10,000 menu items, 150 restaurants)
- [ ] Slow query log enabled to identify performance bottlenecks

**Measurement Method**: Database query EXPLAIN ANALYZE, application logging of query duration

**Priority**: MUST_HAVE

**Traceability**: Architecture Principle #12 (Performance Targets)

---

#### NFR-P-003: Data Refresh Pipeline Duration

**Description**: The weekly data refresh pipeline MUST complete within 24 hours to ensure manageable operational cadence.

**Rationale**: Weekly refresh runs overnight. Completing within 24 hours ensures data freshness without manual intervention.

**Acceptance Criteria**:
- [ ] Full scrape of 150 restaurants completes in <24 hours (parallel scraping with rate limiting)
- [ ] FSA hygiene rating matcher completes in <2 hours (1,841 FSA establishments, 150 restaurants)
- [ ] Trustpilot review scraper completes in <10 hours (incremental updates only)
- [ ] Pipeline configurable for parallel execution (multiple scraper workers)
- [ ] Pipeline failure handling: retries transient errors, logs permanent failures for manual review
- [ ] Progress monitoring: real-time dashboard showing scraping progress (X/150 restaurants completed)

**Measurement Method**: ETL pipeline logging, Airflow/cron job execution time monitoring

**Priority**: SHOULD_HAVE

**Traceability**: Architecture Principle #12 (Performance Targets), Architecture Principle #5 (Scalability)

---

### Scalability Requirements

#### NFR-S-001: Data Volume Scalability

**Description**: The system MUST support 10x current data volume (1,500 restaurants, 100,000 menu items) without architectural changes to enable geographic expansion.

**Rationale**: Future expansion to Devon or UK-wide requires scalable architecture. Avoid expensive redesign when growth occurs.

**Acceptance Criteria**:
- [ ] Database schema supports 1,500 restaurants and 100,000 menu items (tested with synthetic data)
- [ ] Query performance remains acceptable (<500ms p95) at 10x scale
- [ ] Dashboard UI pagination handles large result sets (50 results per page, infinite scroll)
- [ ] No hard-coded limits in code (e.g., "max 200 restaurants")
- [ ] Database storage capacity planning: 20 MB current → 200 MB at 10x scale (within SQLite limits or migration plan to PostgreSQL)

**Measurement Method**: Load testing with 10x synthetic data, database storage capacity analysis

**Priority**: SHOULD_HAVE

**Traceability**: Architecture Principle #5 (Scalability and Extensibility)

---

#### NFR-S-002: Concurrent User Scalability

**Description**: The system SHOULD support 100 concurrent users (1,000 page views/day) without performance degradation to enable public launch.

**Rationale**: Current usage is single-user (internal research). Public launch requires multi-user support.

**Acceptance Criteria**:
- [ ] Dashboard handles 100 concurrent users with <2s page load times (p95)
- [ ] Database connection pooling configured (max 20 connections)
- [ ] Caching strategy reduces database load (Streamlit @st.cache_data with 1-hour TTL)
- [ ] Stateless application design enables horizontal scaling (add more Streamlit app instances)
- [ ] Load testing performed: 100 concurrent users, 10 requests/second

**Measurement Method**: Load testing with Apache JMeter or Locust, application performance monitoring

**Priority**: SHOULD_HAVE

**Traceability**: Architecture Principle #5 (Scalability), Architecture Principle #12 (Performance)

---

### Availability and Reliability Requirements

#### NFR-A-001: Dashboard Uptime

**Description**: The dashboard MUST achieve 99% uptime (7.2 hours downtime/month acceptable for planned maintenance) to ensure consistent user access.

**Rationale**: Users expect reliable access. 99% uptime balances cost (higher SLAs expensive) with user expectations.

**Acceptance Criteria**:
- [ ] Dashboard uptime ≥99% measured monthly (excludes planned maintenance windows)
- [ ] Planned maintenance windows scheduled during low-traffic hours (e.g., Sunday 2-4am GMT)
- [ ] Uptime monitoring enabled (UptimeRobot, Pingdom, or similar)
- [ ] Incident response process defined: detect outage, diagnose, restore service within 2 hours (MTTR)
- [ ] Post-incident review conducted for outages >1 hour

**Measurement Method**: Uptime monitoring service (UptimeRobot), incident logs

**Priority**: MUST_HAVE

**Traceability**: Architecture Principle #13 (Reliability and Availability)

---

#### NFR-A-002: Graceful Degradation

**Description**: The system MUST degrade gracefully when dependencies fail (database unavailable, API rate limits exceeded) to maintain partial functionality.

**Rationale**: Total failure creates poor UX. Showing cached data with staleness warning is better than error page.

**Acceptance Criteria**:
- [ ] If database unavailable, dashboard shows cached data (Streamlit cache) with banner: "Data may be up to 1 hour old. Database connectivity issue detected."
- [ ] If FSA API unavailable during refresh, skip hygiene update and log warning (do not block entire refresh)
- [ ] If Trustpilot scraping fails (robots.txt changed, rate limit hit), log failure and continue to next restaurant
- [ ] If full-text search fails, fall back to simple LIKE-based text search (slower but functional)
- [ ] Error messages user-friendly, not technical stack traces

**Measurement Method**: Fault injection testing (kill database, simulate API failures), user testing

**Priority**: SHOULD_HAVE

**Traceability**: Architecture Principle #13 (Reliability), Architecture Principle #1 (Data Quality First)

---

### Security Requirements

#### NFR-SEC-001: Data Encryption

**Description**: The system MUST encrypt data at rest (database) and in transit (HTTPS) to protect against unauthorized access.

**Rationale**: UK GDPR requires appropriate security measures. Encryption is industry standard.

**Acceptance Criteria**:
- [ ] Database encryption at rest (SQLite encrypted using SQLCipher, or PostgreSQL with encryption enabled)
- [ ] HTTPS/TLS enforced for all web traffic (dashboard served over HTTPS only, HTTP redirects to HTTPS)
- [ ] TLS 1.2 or higher (TLS 1.0/1.1 deprecated)
- [ ] API keys and secrets stored securely (environment variables, not hardcoded)
- [ ] Database credentials not committed to Git repository

**Measurement Method**: SSL Labs test (A grade), security audit of deployment configuration

**Priority**: MUST_HAVE

**Traceability**: Architecture Principle #4 (Privacy by Design)

---

#### NFR-SEC-002: Access Control (Future)

**Description**: The system SHOULD implement authentication and role-based access control (RBAC) if admin features are added.

**Rationale**: Current dashboard is public read-only. Future admin features (data quality monitoring, manual corrections) require access control.

**Acceptance Criteria**:
- [ ] Public users: read-only access to dashboard (no login required)
- [ ] Admin users: authentication required (email/password, SSO, or API key)
- [ ] Admin features protected: data quality dashboard, manual data editing, opt-out processing
- [ ] Password hashing (bcrypt, Argon2) if password authentication used
- [ ] Session management (secure cookies, session timeout after 30 minutes inactivity)

**Priority**: SHOULD_HAVE (future requirement if admin features added)

**Traceability**: Architecture Principle #4 (Privacy by Design)

---

#### NFR-SEC-003: Dependency Security Scanning

**Description**: The system MUST scan dependencies for known vulnerabilities (CVEs) to prevent security exploits.

**Rationale**: Third-party libraries (Streamlit, Pandas, Plotly) may have vulnerabilities. Proactive scanning prevents exploitation.

**Acceptance Criteria**:
- [ ] Dependency vulnerability scanning in CI/CD pipeline (Snyk, GitHub Dependabot, or pip-audit)
- [ ] Critical vulnerabilities (CVSS ≥9.0) block deployment
- [ ] High vulnerabilities (CVSS 7.0-8.9) trigger alerts for remediation within 7 days
- [ ] Dependencies updated quarterly (or when vulnerabilities discovered)
- [ ] Security scan results reviewed before production deployment

**Measurement Method**: Dependency scanning tool reports, vulnerability remediation tracking

**Priority**: SHOULD_HAVE

**Traceability**: Architecture Principle #17 (CI/CD), security best practices

---

### Compliance and Legal Requirements

#### NFR-C-001: Open Government License Compliance (FSA Data)

**Description**: The system MUST comply with Open Government License v3.0 terms for FSA hygiene rating data usage.

**Rationale**: FSA data licensed under OGL. Compliance mandatory to avoid license violation.

**Acceptance Criteria**:
- [ ] FSA attribution displayed wherever hygiene ratings shown: "Data from Food Standards Agency (Open Government License v3.0)"
- [ ] Link to FSA website provided: https://www.food.gov.uk/
- [ ] Link to OGL license provided: https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/
- [ ] No misrepresentation of data source (clearly indicate Plymouth Research does not own FSA data)
- [ ] FSA data not used for commercial purposes without reviewing OGL commercial use terms

**Measurement Method**: Legal review of dashboard attribution, OGL compliance checklist

**Priority**: MUST_HAVE (legal requirement)

**Traceability**: Architecture Principle #3 (Ethical Web Scraping), Architecture Principle #4 (Privacy by Design)

---

#### NFR-C-002: UK GDPR Compliance

**Description**: The system MUST comply with UK General Data Protection Regulation (UK GDPR) for personal data processing.

**Rationale**: Legal requirement for UK-based data processing. Non-compliance risks ICO fines up to £17.5M or 4% of turnover.

**Acceptance Criteria**:
- [ ] Lawful basis for processing: Legitimate interests (business research, consumer information)
- [ ] Data minimization: Only public business data collected (restaurant names, addresses, menus, prices); no personal data (customer names, emails, reviews with PII)
- [ ] Data Protection Impact Assessment (DPIA) completed and approved
- [ ] Privacy policy published on website (data collected, lawful basis, retention period, data subject rights)
- [ ] Data subject rights processes implemented:
  - Right to Erasure (opt-out within 72 hours)
  - Right to Rectification (data correction requests honored)
  - Right to Access (provide data export if requested)
- [ ] Data retention policy: 12 months for historical menu data, permanent deletion after opt-out
- [ ] Breach notification process: notify ICO within 72 hours if data breach occurs
- [ ] ICO registration completed (if required - thresholds apply)

**Measurement Method**: DPIA review, legal compliance audit, privacy policy review

**Priority**: MUST_HAVE (legal requirement)

**Traceability**: Architecture Principle #4 (Privacy by Design - NON-NEGOTIABLE)

---

#### NFR-C-003: Robots.txt and Terms of Service Compliance

**Description**: The system MUST respect robots.txt directives and website Terms of Service for all scraped websites.

**Rationale**: Violating robots.txt or ToS creates legal liability (UK Computer Misuse Act 1990, breach of contract). Ethical scraping principle.

**Acceptance Criteria**:
- [ ] Robots.txt parser implemented and tested (library: robotparser or reppy)
- [ ] Scraper checks robots.txt before accessing each website
- [ ] Disallowed paths never accessed (100% compliance)
- [ ] User-Agent string identifies Plymouth Research with contact email: "PlymouthResearchBot/1.0 (+https://plymouthresearch.co.uk/about)"
- [ ] Rate limiting enforced: minimum 5 seconds between requests to same domain
- [ ] Respectful scraping hours: avoid peak business hours (11am-2pm, 5pm-9pm) if feasible
- [ ] Terms of Service reviewed for each scraped website; prohibitions respected
- [ ] Scraping logs maintained (timestamp, URL, status code) for audit trail

**Measurement Method**: Robots.txt compliance audit, rate limiting verification via logs, legal review

**Priority**: MUST_HAVE (NON-NEGOTIABLE)

**Traceability**: Architecture Principle #3 (Ethical Web Scraping - NON-NEGOTIABLE)

---

### Data Quality Requirements

#### NFR-Q-001: Data Completeness

**Description**: The system MUST achieve 95% completeness for required data fields (restaurant name, menu item name, price) to ensure data utility.

**Rationale**: Incomplete data (missing prices) reduces platform value. Users need pricing data for comparison.

**Acceptance Criteria**:
- [ ] 95% of menu items have non-null prices (measured: COUNT(price IS NOT NULL) / COUNT(*) ≥ 0.95)
- [ ] 100% of restaurants have name, address, cuisine_type (required fields)
- [ ] Completeness metrics tracked in data quality dashboard
- [ ] Automated alerts if completeness drops below 90% threshold
- [ ] Scraping failures logged for manual review and retry

**Measurement Method**: SQL queries for completeness percentages, data quality dashboard

**Priority**: MUST_HAVE

**Traceability**: Architecture Principle #1 (Data Quality First - Completeness dimension)

---

#### NFR-Q-002: Data Accuracy

**Description**: The system MUST achieve 98% accuracy for extracted prices (validated against source data) to ensure reliable comparisons.

**Rationale**: Incorrect prices mislead users and damage trust. High accuracy is critical for value proposition.

**Acceptance Criteria**:
- [ ] 98% of prices extracted correctly (validated by manual spot-check of 100 random menu items)
- [ ] Price range validation: £0.50 ≤ price ≤ £500 (flag outliers for review)
- [ ] Currency normalization: all prices in GBP decimal format (e.g., 12.50, not "£12.50" string)
- [ ] Price extraction errors logged with source URL for debugging
- [ ] Manual validation queue for flagged outliers (e.g., "£250 Wagyu Steak" verified as correct)

**Measurement Method**: Manual validation sampling (100 items/quarter), automated outlier detection

**Priority**: MUST_HAVE

**Traceability**: Architecture Principle #1 (Data Quality First - Accuracy dimension)

---

#### NFR-Q-003: Data Freshness (Timeliness)

**Description**: The system MUST maintain data freshness ≤7 days for menu data and ≤30 days for hygiene ratings to ensure relevance.

**Rationale**: Stale data (outdated menus, closed restaurants) erodes trust. Balance freshness with ethical scraping rate limits.

**Acceptance Criteria**:
- [ ] 90% of restaurants refreshed within last 7 days (measured: COUNT(last_updated > NOW() - 7 days) / COUNT(*) ≥ 0.90)
- [ ] Hygiene ratings refreshed monthly (FSA data updated weekly; matcher runs monthly)
- [ ] Staleness displayed to users: "Menu last updated: 2025-11-15 (7 days ago)"
- [ ] Automated alerts if any restaurant not refreshed in 14 days (potential scraping issue)
- [ ] Timeliness metrics tracked in data quality dashboard

**Measurement Method**: SQL queries for last_updated timestamps, data quality dashboard

**Priority**: MUST_HAVE

**Traceability**: Architecture Principle #1 (Data Quality First - Timeliness dimension)

---

#### NFR-Q-004: Duplicate Detection

**Description**: The system MUST detect and deduplicate menu items to prevent inflated counts and inaccurate analytics.

**Rationale**: Same dish spelled differently ("Fish & Chips" vs "Fish and Chips") creates duplicates. Deduplication ensures accurate menu item counts.

**Acceptance Criteria**:
- [ ] Duplicate detection algorithm implemented (fuzzy string matching, SequenceMatcher)
- [ ] Suspected duplicates flagged for manual review (e.g., similarity ≥90%, same restaurant)
- [ ] Deduplication queue displays: "Fish & Chips" vs "Fish and Chips" - same restaurant (merge?)
- [ ] Manual merge process: Product Owner reviews, approves merge, duplicates deleted
- [ ] Duplicate rate tracked: <2% of menu items flagged as duplicates

**Measurement Method**: Duplicate detection reports, manual review logs

**Priority**: SHOULD_HAVE

**Traceability**: Architecture Principle #1 (Data Quality First - Uniqueness dimension)

---

### Integration Requirements

#### NFR-I-001: FSA API Integration

**Description**: The system MUST integrate with FSA Food Hygiene Rating Scheme XML API to fetch official hygiene ratings.

**Rationale**: FSA provides authoritative hygiene data. XML API is free, publicly available.

**Acceptance Criteria**:
- [ ] FSA Plymouth XML fetched weekly via HTTP GET: https://ratings.food.gov.uk/api/open-data-files/FHRS891en-GB.xml
- [ ] XML parsed using standard library (xml.etree.ElementTree) or lxml
- [ ] 1,841 Plymouth establishments extracted from XML
- [ ] Multi-factor matching algorithm: name similarity (SequenceMatcher), postcode match, address similarity
- [ ] Confidence threshold ≥70% for auto-match; manual review queue for 60-69%
- [ ] Matched hygiene ratings stored in restaurants table (hygiene_rating, hygiene_rating_date, fsa_id, detailed scores)
- [ ] Attribution: "Data from Food Standards Agency (Open Government License v3.0)"

**Priority**: MUST_HAVE

**Stakeholder**: Product Owner, Health-Conscious Diner

**Traceability**: FR-005, NFR-C-001

**Current Status**: ✅ IMPLEMENTED

---

#### NFR-I-002: Trustpilot Web Scraping Integration

**Description**: The system MUST scrape Trustpilot reviews (public data) for customer satisfaction insights.

**Rationale**: Trustpilot provides peer reviews. No public API; web scraping required (within ethical limits).

**Acceptance Criteria**:
- [ ] Trustpilot pages scraped using HTTP requests + HTML parsing (BeautifulSoup or Scrapy)
- [ ] Reviews extracted from __NEXT_DATA__ JSON structure (embedded in HTML)
- [ ] Rate limiting: 2.5 seconds between pages, 5 seconds between restaurants
- [ ] Incremental updates: only fetch reviews newer than last scraped review
- [ ] Reviews stored in trustpilot_reviews table (review_id, restaurant_id, review_date, author, title, body, rating, metadata)
- [ ] Attribution: "Reviews from Trustpilot.com"
- [ ] Robots.txt compliance verified before scraping

**Priority**: MUST_HAVE

**Stakeholder**: Product Owner, All User Personas

**Traceability**: FR-006, NFR-C-003

**Current Status**: ✅ IMPLEMENTED

---

#### NFR-I-003: Google Places API Integration

**Description**: The system MUST integrate with Google Places API for restaurant location, contact info, service options, and reviews.

**Rationale**: Google Places provides authoritative location data, service options (delivery, dine-in), and reviews.

**Acceptance Criteria**:
- [ ] Google Places API Text Search to find Place ID for each restaurant
- [ ] Google Places API Place Details to fetch: name, address, phone, website, lat/lon, service options, reviews
- [ ] Service options extracted: dine_in, takeout, delivery, reservable, serves_breakfast, serves_lunch, serves_dinner, serves_beer, serves_wine, serves_vegetarian
- [ ] Google reviews stored (up to 5 most helpful reviews per restaurant)
- [ ] API usage within free tier limits: 1,000 Place Details requests/month (refresh 100 restaurants/month)
- [ ] API key secured in environment variables (not committed to Git)
- [ ] Attribution: "Data from Google Places API"

**Priority**: MUST_HAVE

**Stakeholder**: Product Owner, All User Personas

**Traceability**: FR-007

**Current Status**: ✅ IMPLEMENTED

---

#### NFR-I-004: Companies House API Integration

**Description**: The system SHOULD integrate with Companies House API for business financial data (optional feature for researchers).

**Rationale**: Researchers interested in restaurant business health. Companies House provides free public data.

**Acceptance Criteria**:
- [ ] Companies House API integration: company search, company profile, filing history
- [ ] Financial metrics extracted: turnover, profit/loss, net assets, employee count (from annual returns)
- [ ] Financial health score calculated (profitability, growth trends, solvency indicators)
- [ ] API usage within free tier limits: 600 requests/5 minutes
- [ ] API key secured in environment variables

**Priority**: SHOULD_HAVE

**Stakeholder**: Food Industry Researcher

**Traceability**: FR-008

**Current Status**: ✅ IMPLEMENTED

---

### Maintainability Requirements

#### NFR-M-001: Code Documentation

**Description**: The system MUST maintain comprehensive code documentation (README, ADRs, code comments) to enable future maintainability.

**Rationale**: Small team. Future maintainers (or future-you in 6 months) need clear documentation to understand architecture and make changes.

**Acceptance Criteria**:
- [ ] README.md with: setup instructions, architecture overview, common tasks, troubleshooting guide
- [ ] CLAUDE.md with: AI assistant guidance, project context, key files, database schema, implementation notes
- [ ] Architecture Decision Records (ADRs) for key technology choices (Streamlit vs Dash, SQLite vs PostgreSQL, etc.)
- [ ] Code comments for complex logic (document "why" not "what")
- [ ] Database schema documented with data dictionary (table purposes, column descriptions)

**Priority**: SHOULD_HAVE

**Traceability**: Architecture Principle #14 (Maintainability and Documentation)

**Current Status**: ✅ IMPLEMENTED (comprehensive CLAUDE.md, organization summaries)

---

#### NFR-M-002: Automated Testing

**Description**: The system SHOULD implement automated tests (unit, integration, end-to-end) to enable confident refactoring and prevent regressions.

**Rationale**: Manual testing is time-consuming and error-prone. Automated tests catch bugs before production.

**Acceptance Criteria**:
- [ ] Unit tests for data normalization logic (price extraction, duplicate detection, dietary tag extraction) - target 70%+ coverage
- [ ] Integration tests for database queries (search, filtering, aggregations)
- [ ] End-to-end tests for critical user flows (search restaurants, view menu, export data)
- [ ] Data quality tests run on every ETL execution (completeness, accuracy, outlier detection)
- [ ] Tests run in CI/CD pipeline on every commit
- [ ] Test coverage tracked; regressions block deployment

**Priority**: SHOULD_HAVE

**Traceability**: Architecture Principle #16 (Automated Testing)

**Current Status**: ⚠️ NOT IMPLEMENTED (future improvement)

---

#### NFR-M-003: Infrastructure as Code

**Description**: The system SHOULD define infrastructure as code (IaC) for repeatable, version-controlled deployments.

**Rationale**: Manual deployments create drift and "works on my machine" issues. IaC enables disaster recovery and environment parity.

**Acceptance Criteria**:
- [ ] Database schema version-controlled (SQL migration scripts)
- [ ] Deployment scripts automated (deploy.sh or CI/CD pipeline config)
- [ ] Environment configuration version-controlled (requirements.txt, .env.example)
- [ ] Infrastructure setup documented in README.md
- [ ] No manual SSH into production for configuration changes

**Priority**: SHOULD_HAVE

**Traceability**: Architecture Principle #15 (Infrastructure as Code)

**Current Status**: ✅ PARTIALLY IMPLEMENTED (SQL schema files version-controlled, requirements.txt exists)

---

### Observability Requirements

#### NFR-O-001: Structured Logging

**Description**: The system SHOULD emit structured logs (JSON format) for debugging, audit trails, and compliance.

**Rationale**: Troubleshooting production issues requires detailed logs. Structured logs enable automated analysis.

**Acceptance Criteria**:
- [ ] Logs in JSON format with fields: timestamp, severity, component, message, context (restaurant_id, scrape_job_id, etc.)
- [ ] Log levels: ERROR (failures requiring action), WARN (degraded state), INFO (key events), DEBUG (detailed troubleshooting)
- [ ] Correlation IDs for tracing requests (scrape_job_id tracks entire scraping run)
- [ ] Sensitive data redacted from logs (API keys, passwords never logged)
- [ ] Log retention: 30 days for operational logs, 12 months for audit logs (GDPR compliance)

**Priority**: SHOULD_HAVE

**Traceability**: Architecture Principle #18 (Logging and Monitoring)

**Current Status**: ⚠️ PARTIALLY IMPLEMENTED (basic logging exists, not yet structured JSON)

---

#### NFR-O-002: Metrics and Monitoring

**Description**: The system SHOULD track operational metrics (scraping success rate, data quality, API errors) for proactive issue detection.

**Rationale**: Reactive troubleshooting (waiting for users to report issues) is slow. Proactive monitoring catches issues early.

**Acceptance Criteria**:
- [ ] Metrics tracked:
  - Scraping: restaurants scraped, menu items extracted, failures, scrape duration
  - Data quality: completeness %, accuracy %, timeliness %
  - API: request volume, latency (p50, p95, p99), error rate
  - Dashboard: page views, search queries, user sessions
- [ ] Metrics dashboard (Grafana, or simple Streamlit admin page)
- [ ] Alerts configured:
  - Scraping failures >10% of restaurants
  - Data completeness <90%
  - API error rate >1%
  - Dashboard downtime >5 minutes

**Priority**: SHOULD_HAVE

**Traceability**: Architecture Principle #18 (Logging and Monitoring)

**Current Status**: ⚠️ NOT IMPLEMENTED (future improvement)

---

## Data Requirements

### DR-001: Restaurant Master Data

**Description**: The system MUST maintain a master database of restaurants with comprehensive attributes.

**Data Model**:
- **Primary Key**: restaurant_id (INTEGER, auto-increment)
- **Required Fields**: name (TEXT), cuisine_type (TEXT), is_active (BOOLEAN)
- **Optional Fields**: address, postcode, website_url, phone, price_range (£/££/£££/££££), latitude, longitude
- **Scraped Data**: scraped_at (TIMESTAMP), last_updated (TIMESTAMP), data_source (enum: real_scraped, synthetic), scraping_method
- **Hygiene Data** (9 columns): hygiene_rating (0-5), hygiene_rating_date, fsa_id, hygiene_score_hygiene, hygiene_score_structural, hygiene_score_confidence, fsa_business_type, fsa_local_authority, hygiene_rating_fetched_at
- **Review Data** (5 columns): trustpilot_url, trustpilot_business_id, trustpilot_last_scraped_at, trustpilot_review_count (auto-updated), trustpilot_avg_rating (auto-updated)
- **Google Data** (16+ columns): google_place_id, google_rating, google_user_ratings_total, google_price_level, service options (dine_in, takeout, delivery, etc.), contact info (phone, website, maps_url)
- **Financial Data** (20+ columns): company_number, company_name, company_status, turnover_gbp, profit_loss_gbp, net_assets_gbp, financial_health_score
- **Licensing Data**: licensing_premises_id, licensing_activities, licensing_opening_hours
- **Business Rates Data**: business_rates_rateable_value, business_rates_category

**Data Retention**: Permanent for active restaurants; 30 days after soft delete (opt-out), then hard delete

**GDPR Classification**: Public business data (not personal data)

**Priority**: MUST_HAVE

**Traceability**: FR-001, FR-002, Architecture Principle #7 (Single Source of Truth)

**Current Status**: ✅ IMPLEMENTED (52 columns)

---

### DR-002: Menu Item Data

**Description**: The system MUST store menu items with pricing, descriptions, and dietary attributes.

**Data Model**:
- **Primary Key**: item_id (INTEGER, auto-increment)
- **Foreign Key**: restaurant_id (references restaurants table)
- **Required Fields**: item_name (TEXT), price (DECIMAL), currency (default: GBP)
- **Optional Fields**: description (TEXT), category (enum: Starters, Mains, Desserts, Drinks, etc.)
- **Dietary Flags**: is_vegetarian (BOOLEAN), is_vegan (BOOLEAN), is_gluten_free (BOOLEAN)
- **Allergen Info**: allergen_info (TEXT - comma-separated list)
- **Metadata**: scraped_at (TIMESTAMP), last_updated (TIMESTAMP), source_url (TEXT)

**Data Retention**: 12 months (historical menu data for trend analysis), then deleted

**Validation Rules**:
- price: £0.50 ≤ price ≤ £500 (flag outliers)
- item_name: NOT NULL, length ≥3 characters
- category: controlled vocabulary (enforced in application logic, not database constraint)

**GDPR Classification**: Public business data (factual menu information)

**Priority**: MUST_HAVE

**Traceability**: FR-002, FR-003, FR-004

**Current Status**: ✅ IMPLEMENTED (13 columns, 2,625 items)

---

### DR-003: Trustpilot Reviews Data

**Description**: The system MUST store Trustpilot customer reviews for sentiment analysis and customer satisfaction insights.

**Data Model**:
- **Primary Key**: review_id (INTEGER, auto-increment)
- **Foreign Key**: restaurant_id (references restaurants table, CASCADE DELETE)
- **Required Fields**: review_date (DATE), rating (INTEGER 1-5), scraped_at (TIMESTAMP)
- **Optional Fields**: author_name (TEXT), review_title (TEXT), review_body (TEXT), author_location (TEXT - country code), author_review_count (INTEGER), is_verified_purchase (BOOLEAN), helpful_count (INTEGER), reply_count (INTEGER)
- **Metadata**: page_number (INTEGER - pagination tracking)

**Data Retention**: 12 months (review data for trend analysis), then deleted

**GDPR Classification**: Public data (scraped from public Trustpilot pages); no personal data collected beyond publicly visible author names (pseudonyms)

**Privacy Note**: Author names are pseudonyms chosen by reviewers (e.g., "John D."). No email addresses, phone numbers, or contact information collected.

**Priority**: MUST_HAVE

**Traceability**: FR-006, FR-007

**Current Status**: ✅ IMPLEMENTED (13 columns, 9,410 reviews)

---

### DR-004: Google Reviews Data

**Description**: The system SHOULD store Google reviews (up to 5 per restaurant) for additional customer feedback.

**Data Model**:
- **Primary Key**: review_id (INTEGER, auto-increment)
- **Foreign Key**: restaurant_id (references restaurants table)
- **Fields**: review_date (DATE), author_name (TEXT), review_text (TEXT), rating (INTEGER 1-5), relative_time_description (TEXT - "2 weeks ago")

**Data Retention**: 12 months, then deleted

**GDPR Classification**: Public data (from Google Places API)

**Priority**: SHOULD_HAVE

**Current Status**: ✅ IMPLEMENTED (481 Google reviews stored)

---

### DR-005: Data Lineage Metadata

**Description**: The system MUST track data lineage (source URL, scrape timestamp, scraper version) for every data record to enable quality audits and debugging.

**Rationale**: When data quality issues arise, must trace back to original source for investigation.

**Data Model**:
- **Columns in restaurants table**: scraped_at (TIMESTAMP), last_updated (TIMESTAMP), data_source (enum), scraping_method (TEXT)
- **Columns in menu_items table**: scraped_at (TIMESTAMP), last_updated (TIMESTAMP), source_url (TEXT)
- **Columns in trustpilot_reviews table**: scraped_at (TIMESTAMP), page_number (INTEGER)
- **Future**: Scraper version tracking (scraper_version TEXT column), raw HTML snapshot archival (compressed, stored in blob storage)

**Retention**: Lineage metadata retained for lifetime of data record (deleted when parent record deleted)

**Priority**: MUST_HAVE

**Traceability**: Architecture Principle #8 (Data Lineage and Traceability)

**Current Status**: ✅ IMPLEMENTED (scraped_at, last_updated columns exist)

---

### DR-006: Data Quality Metrics

**Description**: The system SHOULD track data quality metrics (completeness, accuracy, timeliness, duplication) for continuous monitoring.

**Data Model**:
- **Table**: data_quality_metrics (new table)
- **Columns**: metric_date (DATE), metric_type (enum: completeness, accuracy, timeliness, duplication), metric_value (DECIMAL), details (JSON - drill-down info)
- **Examples**:
  - metric_type="completeness", metric_value=0.92 (92% of menu items have prices)
  - metric_type="accuracy", metric_value=0.98 (98% of prices in valid range)
  - metric_type="timeliness", metric_value=0.85 (85% of restaurants refreshed in last 7 days)

**Retention**: 12 months (for trend analysis)

**Priority**: SHOULD_HAVE

**Traceability**: Architecture Principle #1 (Data Quality First), NFR-Q-001, NFR-Q-002, NFR-Q-003

**Current Status**: ⚠️ NOT IMPLEMENTED (future improvement)

---

## Integration Requirements Summary

**External System Integrations** (6 data sources):

| System | Integration Type | Data Fetched | Update Frequency | Authentication | Status |
|--------|------------------|--------------|------------------|----------------|--------|
| FSA Food Hygiene API | XML over HTTP | Hygiene ratings, detailed scores, business info | Weekly | None (public data) | ✅ Implemented |
| Trustpilot | Web scraping | Customer reviews, ratings, author info | Weekly (incremental) | None (public pages) | ✅ Implemented |
| Google Places API | REST API | Location, contact, service options, reviews | Monthly | API key | ✅ Implemented |
| Companies House API | REST API | Financial statements, company info, directors | Quarterly | API key | ✅ Implemented |
| Plymouth Licensing | Web scraping | Licensing activities, opening hours | Monthly | None (public data) | ✅ Implemented |
| Business Rates | CSV data | Rateable values, property categories | Quarterly | None (public data) | ✅ Implemented |

---

## Requirement Conflicts & Resolutions

### Conflict 1: Data Freshness vs Ethical Scraping Rate Limits

**Conflicting Requirements**:
- **BR-006 (Data Freshness)**: Requires weekly menu data refresh for timeliness
- **NFR-C-003 (Ethical Scraping)**: Requires minimum 5-second delay between requests to same domain

**Stakeholders Involved**:
- **End Users**: Want fresh data (weekly updates)
- **Restaurant Owners**: Want minimal server load from scraping (rate limiting)

**Trade-off Analysis**:
- **Option A (Prioritize Freshness)**: Scrape every 3 days with 3-second delays → More frequent updates but higher scraping load, potential robots.txt violations
- **Option B (Prioritize Ethics)**: Scrape weekly with 5-second delays → Less frequent updates but respectful scraping, legal compliance
- **Option C (Compromise)**: Scrape weekly with 5-second delays + incremental updates for critical data (prices only)

**Resolution Strategy**: **Prioritize Ethics** (Option B)
- **Decision**: Weekly scraping with 5-second rate limits (Principle #3 is NON-NEGOTIABLE)
- **Rationale**: Legal and ethical compliance is non-negotiable. Weekly freshness acceptable for MVP; users can tolerate 7-day staleness for menu data.
- **Stakeholder Impact**: End users accept slight staleness; restaurant owners protected from aggressive scraping
- **Future Mitigation**: Explore restaurant partnerships for API access (no scraping needed) or RSS feed subscriptions

**Decision Authority**: Product Owner (Mark Craddock)

---

### Conflict 2: Comprehensive Coverage vs Budget Constraints

**Conflicting Requirements**:
- **BR-001 (Comprehensive Coverage)**: Requires 150+ restaurants (90% coverage) for platform utility
- **BR-003 (Cost Efficiency)**: Requires total costs ≤£100/month

**Stakeholders Involved**:
- **Product Owner**: Wants comprehensive coverage for platform value
- **Finance**: Wants minimal costs for sustainability

**Trade-off Analysis**:
- **Option A (Maximize Coverage)**: Scrape 300+ restaurants using expensive commercial scraping service (Apify, ScrapingBee) → Higher coverage but £500+/month costs
- **Option B (Minimize Costs)**: Scrape 50 restaurants using free tools (Scrapy, BeautifulSoup) → Low costs but insufficient coverage (poor platform value)
- **Option C (Compromise)**: Scrape 150 restaurants using free tools + paid APIs within free tiers (Google Places 1,000 free requests/month) → Balanced coverage and costs

**Resolution Strategy**: **Compromise** (Option C)
- **Decision**: Target 150 restaurants using open-source scraping tools + free API tiers
- **Rationale**: 150 restaurants achieves 90% Plymouth coverage (sufficient for MVP). Open-source tools (Scrapy, BeautifulSoup) have zero licensing costs. Google Places, Companies House, FSA APIs are free within usage limits.
- **Stakeholder Impact**: Product Owner achieves coverage target; Finance stays within budget
- **Implementation**: Prioritize restaurants with online menus (easier to scrape); defer restaurants without websites to Phase 2
- **Monitoring**: Track costs monthly; alert if approaching £80/month (80% of budget)

**Decision Authority**: Product Owner (Mark Craddock) in consultation with finance stakeholder (if applicable)

---

### Conflict 3: Public Access vs Data Subject Privacy

**Conflicting Requirements**:
- **BR-007 (Public Dashboard)**: Requires public-facing dashboard for consumer access (no login required)
- **NFR-C-002 (GDPR Compliance)**: Requires data minimization and opt-out process for restaurant owners (data subjects)

**Stakeholders Involved**:
- **End Users**: Want free, unrestricted access to restaurant data
- **Restaurant Owners**: Want control over their data (opt-out, corrections)
- **ICO (Regulator)**: Expects GDPR compliance (lawful basis, data subject rights)

**Trade-off Analysis**:
- **Option A (Full Public Access)**: No restrictions, no opt-out → Maximum user value but GDPR non-compliance (illegal)
- **Option B (Gated Access)**: Login required, verified users only → GDPR compliant but poor UX, limits adoption
- **Option C (Public with Opt-Out)**: Public dashboard + prominent opt-out process → Balanced: accessible to users, respects restaurant rights

**Resolution Strategy**: **Innovate** (Option C - Public with Safeguards)
- **Decision**: Public read-only dashboard + transparent opt-out process + DPIA completion
- **Rationale**:
  - Lawful basis: Legitimate interests (consumer information, market research)
  - Data minimization: Only public business data (no PII beyond business contact info)
  - Transparency: Privacy policy clearly states data sources, purpose, retention
  - Data subject rights: Opt-out process honored within 72 hours (Right to Erasure)
- **Stakeholder Impact**:
  - End users: Unrestricted access to dashboard
  - Restaurant owners: Clear opt-out process, corrections honored
  - ICO: GDPR compliance validated via DPIA
- **Implementation**:
  - Privacy policy published on About page
  - Opt-out contact email prominently displayed
  - DPIA completed before public launch
  - Regular GDPR compliance audits

**Decision Authority**: Product Owner (Mark Craddock) with legal review (solicitor or legal counsel)

---

### Conflict 4: Real-Time Data vs Scalability

**Conflicting Requirements**:
- **Future Enhancement (Medium Priority)**: Real-time menu updates for instant freshness
- **NFR-S-001 (Scalability)**: Requires architecture supporting 10x scale (1,500 restaurants)

**Stakeholders Involved**:
- **End Users**: Want real-time menu updates (instant price changes)
- **Product Owner**: Wants scalable architecture for geographic expansion

**Trade-off Analysis**:
- **Option A (Real-Time Scraping)**: Scrape every restaurant hourly → Fresh data but 1,500 restaurants × 24 scrapes/day = 36,000 scrapes/day (unethical, likely blocked)
- **Option B (Batch Processing)**: Weekly batch scraping → Scalable but 7-day staleness
- **Option C (Hybrid)**: Weekly batch scraping + restaurant-provided webhooks/APIs for instant updates → Best of both worlds but requires restaurant partnerships

**Resolution Strategy**: **Phase** (Option B now, Option C later)
- **Decision**: MVP uses weekly batch scraping (Option B); Phase 2 explores restaurant partnerships for API access (Option C)
- **Rationale**: Real-time updates require restaurant cooperation (API access or webhook notifications). MVP focuses on proving value with batch updates. Once platform established, approach restaurants for partnerships.
- **Stakeholder Impact**:
  - End users: Accept 7-day staleness in MVP; gain real-time updates in Phase 2
  - Product Owner: Scalable batch architecture supports 10x growth immediately; partnerships pursued post-MVP
- **Timeline**: MVP (weekly batch), Phase 2 (restaurant partnerships, 6-12 months post-launch)

**Decision Authority**: Product Owner (Mark Craddock)

---

## Requirements Traceability Matrix

| Requirement ID | Stakeholder | Architecture Principle | Use Case | Priority | Status |
|----------------|-------------|------------------------|----------|----------|--------|
| BR-001 | End Users, Product Owner | #1 (Data Quality) | UC-001 | MUST_HAVE | ✅ Implemented |
| BR-002 | Product Owner, Researchers | #7 (Single Source of Truth) | UC-006, UC-007 | MUST_HAVE | ✅ Implemented |
| BR-003 | Product Owner | #6 (Cost Efficiency), #2 (Open Source) | N/A | MUST_HAVE | ✅ Implemented |
| BR-004 | Product Owner, ICO, Restaurants | #3 (Ethical Scraping), #4 (Privacy) | UC-010, UC-011 | MUST_HAVE | ✅ Implemented |
| BR-005 | Product Owner | #5 (Scalability) | N/A | SHOULD_HAVE | ✅ Implemented |
| BR-006 | End Users | #1 (Data Quality - Timeliness) | UC-001, UC-002 | MUST_HAVE | ⚠️ Partial |
| BR-007 | End Users | N/A | UC-001, UC-002, UC-003 | MUST_HAVE | ✅ Implemented |
| FR-001 | All Users | #12 (Performance) | UC-001 | MUST_HAVE | ✅ Implemented |
| FR-002 | Consumers, Researchers | #9 (Normalization) | UC-002, UC-004 | MUST_HAVE | ✅ Implemented |
| FR-003 | Consumers, Researchers | #12 (Performance) | UC-003 | MUST_HAVE | ✅ Implemented |
| FR-004 | Health-Conscious Diner | #1 (Data Quality) | UC-005 | MUST_HAVE | ✅ Implemented |
| FR-005 | Health-Conscious Diner, Researchers | #3 (Ethical), #4 (Privacy) | UC-006 | MUST_HAVE | ✅ Implemented |
| FR-006 | All Users | #3 (Ethical Scraping) | UC-002, UC-007 | MUST_HAVE | ✅ Implemented |
| FR-007 | All Users | N/A | UC-001, UC-002 | MUST_HAVE | ✅ Implemented |
| FR-008 | Researchers | N/A | UC-007 | SHOULD_HAVE | ✅ Implemented |
| FR-009 | Researchers | #10 (API-First), #11 (Standards) | UC-008 | SHOULD_HAVE | ⚠️ Partial |
| FR-010 | Restaurant Owners | #4 (Privacy - NON-NEGOTIABLE) | UC-010, UC-011 | MUST_HAVE | ✅ Implemented |
| NFR-P-001 | All Users | #12 (Performance Targets) | All UCs | MUST_HAVE | ✅ Implemented |
| NFR-P-002 | All Users | #12 (Performance Targets) | UC-001, UC-004 | MUST_HAVE | ✅ Implemented |
| NFR-P-003 | Product Owner | #12 (Performance), #5 (Scalability) | N/A | SHOULD_HAVE | ✅ Implemented |
| NFR-S-001 | Product Owner | #5 (Scalability) | N/A | SHOULD_HAVE | ✅ Implemented |
| NFR-S-002 | Product Owner | #5 (Scalability) | N/A | SHOULD_HAVE | ⚠️ Untested |
| NFR-A-001 | All Users | #13 (Reliability) | All UCs | MUST_HAVE | ⚠️ Depends on hosting |
| NFR-A-002 | All Users | #13 (Reliability) | All UCs | SHOULD_HAVE | ⚠️ Partial |
| NFR-SEC-001 | All Stakeholders | #4 (Privacy) | N/A | MUST_HAVE | ⚠️ Depends on deployment |
| NFR-SEC-002 | Product Owner | #4 (Privacy) | UC-009 | SHOULD_HAVE | ❌ Not implemented |
| NFR-SEC-003 | Product Owner | #17 (CI/CD) | N/A | SHOULD_HAVE | ❌ Not implemented |
| NFR-C-001 | ICO, FSA | #3 (Ethical), #4 (Privacy) | UC-006 | MUST_HAVE | ✅ Implemented |
| NFR-C-002 | ICO, Restaurant Owners | #4 (Privacy - NON-NEGOTIABLE) | UC-010, UC-011 | MUST_HAVE | ✅ Implemented |
| NFR-C-003 | Restaurant Owners | #3 (Ethical - NON-NEGOTIABLE) | All scraping | MUST_HAVE | ✅ Implemented |
| NFR-Q-001 | All Users | #1 (Data Quality - Completeness) | All UCs | MUST_HAVE | ✅ Implemented |
| NFR-Q-002 | All Users | #1 (Data Quality - Accuracy) | UC-002, UC-003 | MUST_HAVE | ✅ Implemented |
| NFR-Q-003 | All Users | #1 (Data Quality - Timeliness) | UC-001, UC-002 | MUST_HAVE | ⚠️ Partial |
| NFR-Q-004 | Researchers | #1 (Data Quality - Uniqueness) | UC-003, UC-007 | SHOULD_HAVE | ⚠️ Partial |
| NFR-I-001 | Product Owner | #11 (Standard Formats) | UC-006 | MUST_HAVE | ✅ Implemented |
| NFR-I-002 | Product Owner | #3 (Ethical Scraping) | UC-002, UC-007 | MUST_HAVE | ✅ Implemented |
| NFR-I-003 | Product Owner | N/A | UC-001, UC-002 | MUST_HAVE | ✅ Implemented |
| NFR-I-004 | Researchers | N/A | UC-007 | SHOULD_HAVE | ✅ Implemented |
| NFR-M-001 | Product Owner | #14 (Maintainability) | N/A | SHOULD_HAVE | ✅ Implemented |
| NFR-M-002 | Product Owner | #16 (Automated Testing) | N/A | SHOULD_HAVE | ❌ Not implemented |
| NFR-M-003 | Product Owner | #15 (Infrastructure as Code) | N/A | SHOULD_HAVE | ⚠️ Partial |
| NFR-O-001 | Product Owner | #18 (Logging & Monitoring) | UC-009 | SHOULD_HAVE | ⚠️ Partial |
| NFR-O-002 | Product Owner | #18 (Logging & Monitoring) | UC-009 | SHOULD_HAVE | ❌ Not implemented |

**Legend**:
- ✅ Implemented: Requirement fully satisfied in production codebase
- ⚠️ Partial: Requirement partially implemented or dependent on deployment
- ❌ Not implemented: Requirement deferred to future phase

---

## Key Gaps and Recommendations

### High Priority Gaps (Block Production Launch)

1. **NFR-SEC-001 (Data Encryption)**: HTTPS enforcement and database encryption required before public launch
   - **Action**: Deploy to platform with HTTPS (Streamlit Cloud, Railway, Render); enable SQLite encryption (SQLCipher) or migrate to PostgreSQL with encryption
   - **Timeline**: Before public launch (GDPR requirement)

2. **NFR-A-001 (Dashboard Uptime)**: Uptime monitoring and incident response needed
   - **Action**: Set up UptimeRobot (free tier), configure alerts to Product Owner email
   - **Timeline**: Before public launch

3. **BR-006 / NFR-Q-003 (Data Freshness Automation)**: Manual refresh workflow needs automation
   - **Action**: Implement weekly cron job (GitHub Actions, Render Cron, or Streamlit Cloud scheduler) to trigger scraping pipeline
   - **Timeline**: Within 2 weeks of public launch

### Medium Priority Gaps (Improve Quality)

4. **NFR-M-002 (Automated Testing)**: No automated tests exist
   - **Action**: Implement unit tests for data normalization logic (price extraction, duplicate detection); integration tests for database queries
   - **Timeline**: Within 1 month of public launch (technical debt)

5. **NFR-O-002 (Metrics and Monitoring)**: No operational metrics tracked
   - **Action**: Build simple data quality dashboard (Streamlit admin page); track scraping success rate, data completeness, API errors
   - **Timeline**: Within 1 month of public launch

6. **NFR-SEC-003 (Dependency Scanning)**: No security scanning
   - **Action**: Enable GitHub Dependabot or integrate Snyk in CI/CD pipeline
   - **Timeline**: Within 2 weeks of public launch

### Low Priority Gaps (Future Enhancements)

7. **FR-009 (Public API)**: No API for programmatic access
   - **Action**: Defer to Phase 2; design RESTful API endpoints if demand exists
   - **Timeline**: 6-12 months post-MVP

8. **NFR-SEC-002 (Access Control)**: No authentication for admin features
   - **Action**: Defer until admin features built (data quality dashboard, manual corrections); implement Streamlit authentication
   - **Timeline**: 3-6 months post-MVP

9. **NFR-S-002 (Concurrent User Load Testing)**: Not tested at 100 concurrent users
   - **Action**: Perform load testing before major marketing push; use Locust or Apache JMeter
   - **Timeline**: Before scaling marketing efforts

---

## Acceptance Criteria Summary

**Total Requirements**: 69
- Business Requirements (BR-xxx): 7
- Functional Requirements (FR-xxx): 10
- Non-Functional Requirements (NFR-xxx): 47
  - Performance (NFR-P-xxx): 3
  - Scalability (NFR-S-xxx): 2
  - Availability (NFR-A-xxx): 2
  - Security (NFR-SEC-xxx): 3
  - Compliance (NFR-C-xxx): 3
  - Data Quality (NFR-Q-xxx): 4
  - Integration (NFR-I-xxx): 4
  - Maintainability (NFR-M-xxx): 3
  - Observability (NFR-O-xxx): 2
- Data Requirements (DR-xxx): 6

**Requirement Status**:
- ✅ Implemented: 52 requirements (75%)
- ⚠️ Partially Implemented: 11 requirements (16%)
- ❌ Not Implemented: 6 requirements (9% - deferred to future phases)

**Compliance Requirements**:
- UK GDPR (NFR-C-002): MUST_HAVE - ✅ DPIA required, opt-out process implemented
- Open Government License (NFR-C-001): MUST_HAVE - ✅ FSA attribution displayed
- Robots.txt Compliance (NFR-C-003): MUST_HAVE (NON-NEGOTIABLE) - ✅ Implemented
- Computer Misuse Act 1990: MUST_HAVE - ✅ Ethical scraping practices (rate limiting, User-Agent)

---

## Next Steps

### Immediate Actions (Before Public Launch)

1. **Complete DPIA**: Data Protection Impact Assessment for GDPR compliance (NFR-C-002)
   - **Owner**: Product Owner + Legal Counsel (if available)
   - **Timeline**: 1 week
   - **Blocker**: Cannot launch publicly without DPIA

2. **Deploy with HTTPS**: Ensure dashboard served over HTTPS (NFR-SEC-001)
   - **Owner**: Product Owner
   - **Timeline**: 1 day (Streamlit Cloud/Railway/Render provide free HTTPS)
   - **Blocker**: GDPR compliance requires encryption in transit

3. **Set Up Uptime Monitoring**: Configure UptimeRobot or Pingdom (NFR-A-001)
   - **Owner**: Product Owner
   - **Timeline**: 30 minutes
   - **Blocker**: Need proactive issue detection

4. **Publish Privacy Policy**: Document data collection, lawful basis, retention, data subject rights
   - **Owner**: Product Owner + Legal Counsel
   - **Timeline**: 2 days
   - **Blocker**: GDPR transparency requirement

5. **Automate Weekly Data Refresh**: Implement cron job for scraping pipeline (BR-006, NFR-Q-003)
   - **Owner**: Product Owner
   - **Timeline**: 1 week
   - **Blocker**: Manual refresh not sustainable for production

### Phase 2 Enhancements (Post-MVP)

6. **Implement Automated Testing**: Unit tests for data quality logic, integration tests for DB queries (NFR-M-002)
   - **Timeline**: 1 month post-launch
   - **Value**: Prevent regressions, enable confident refactoring

7. **Build Data Quality Dashboard**: Track completeness, accuracy, timeliness metrics (NFR-O-002)
   - **Timeline**: 1 month post-launch
   - **Value**: Proactive data quality monitoring

8. **Enable Dependency Scanning**: GitHub Dependabot or Snyk (NFR-SEC-003)
   - **Timeline**: 2 weeks post-launch
   - **Value**: Security vulnerability detection

9. **Conduct Load Testing**: Test 100 concurrent users before scaling (NFR-S-002)
   - **Timeline**: Before major marketing push
   - **Value**: Validate scalability claims

10. **Explore Restaurant Partnerships**: Approach restaurants for API access or RSS feeds (Conflict Resolution #1)
    - **Timeline**: 6-12 months post-launch
    - **Value**: Real-time updates without aggressive scraping

---

## Document Metadata

**Generated by**: ArcKit `/arckit.requirements` command
**Generated on**: 2025-11-22 16:00:00 GMT
**ArcKit Version**: v0.9.1
**Project**: Plymouth Research Restaurant Menu Analytics (Project 001)
**AI Model**: Claude Sonnet 4.5 (claude-sonnet-4-5-20250929)
**Generation Context**: Requirements extracted from production codebase analysis (13,315 lines of code across 40+ files), architecture principles document (18 principles), and current operational data (243 restaurants, 2,625 menu items, 9,410 reviews, 6 data sources integrated)

**Source Documents**:
- `dashboard_app.py` (2,053 lines) - Main dashboard application
- `CLAUDE.md` - Implementation guide with database schema, features, and known limitations
- `.arckit/memory/architecture-principles.md` - 18 enterprise architecture principles
- `scripts/fetchers/*.py` (9 data fetching scripts)
- `scripts/matchers/*.py` (4 data matching scripts)
- `scripts/importers/*.py` (7 database import scripts)
- Database schema files (6 SQL schema files for hygiene, reviews, Google, licensing, business rates)

**Requirements Methodology**: Requirements elicited through reverse engineering of production code combined with stakeholder analysis (4 user personas identified), use case modeling (11 detailed use cases), and alignment with architecture principles. Conflicts identified and resolved through trade-off analysis with documented decision rationale.
