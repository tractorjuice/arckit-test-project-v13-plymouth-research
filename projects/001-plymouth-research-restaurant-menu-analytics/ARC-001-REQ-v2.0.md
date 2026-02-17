# Project Requirements: Plymouth Research Restaurant Menu Analytics

> **Template Status**: Live | **Version**: 2.5.1 | **Command**: `/arckit:requirements`

## Document Control

| Field | Value |
|-------|-------|
| **Document ID** | ARC-001-REQ-v2.0 |
| **Document Type** | Business and Technical Requirements |
| **Project** | Plymouth Research Restaurant Menu Analytics (Project 001) |
| **Classification** | OFFICIAL |
| **Status** | DRAFT |
| **Version** | 2.0 |
| **Created Date** | 2026-02-17 |
| **Last Modified** | 2026-02-17 |
| **Review Cycle** | Monthly |
| **Next Review Date** | 2026-03-19 |
| **Owner** | Product Owner - Plymouth Research |
| **Reviewed By** | [PENDING] |
| **Approved By** | [PENDING] |
| **Distribution** | Product Team, Architecture Team, Development Team |

## Revision History

| Version | Date | Author | Changes | Approved By | Approval Date |
|---------|------|--------|---------|-------------|---------------|
| 1.0 | 2025-11-22 | ArcKit AI | Initial creation from `/arckit.requirements` command based on production codebase analysis | [PENDING] | [PENDING] |
| 2.0 | 2026-02-17 | ArcKit AI | Major update: added ONS geography, enhanced Companies House financials, 3 new database tables, deep stakeholder traceability (STKE goals/drivers), risk-driven requirements (RISK register), Data Source Discovery integration (DSCT-v1.0), formal Data Model alignment (DATA-v1.0), updated template to v2.5.1 | [PENDING] | [PENDING] |

## Document Purpose

This document specifies the comprehensive business and technical requirements for the Plymouth Research Restaurant Menu Analytics platform. It serves as the definitive reference for:
- Product development and feature prioritization
- Architecture design decisions and technology selection
- Vendor RFP evaluation criteria (if considering SaaS alternatives)
- Quality assurance and acceptance testing
- Compliance validation (GDPR, web scraping ethics)
- Traceability from stakeholder goals (ARC-001-STKE-v1.0) through requirements to design and testing

All requirements are derived from:
- Production codebase analysis (13,315+ lines of code)
- Architecture principles (ARC-000-PRIN-v1.0, 18 principles)
- Stakeholder analysis (ARC-001-STKE-v1.0, 10 drivers, 8 goals, 4 outcomes)
- Risk register (ARC-001-RISK-v1.0, 20 risks)
- Data source discovery (ARC-001-DSCT-v1.0, 22 sources identified)
- Formal data model (ARC-001-DATA-v1.0, 8 entities, 142 attributes)
- Current operational capabilities (243 restaurants, 2,625 menu items, 9,410+ reviews, 8 data sources)

---

## Executive Summary

### Business Context

Plymouth Research operates an independent restaurant and bar analytics platform focused on the Plymouth, UK market. The platform aggregates publicly available data from restaurant websites, government food safety agencies, review platforms, business registries, and geographic datasets to provide comprehensive insights into the local hospitality industry.

The business value proposition is built on three pillars:
1. **Data Aggregation**: Consolidate fragmented restaurant data (menus, prices, hygiene ratings, reviews, financial health, geographic context) into a single searchable dashboard
2. **Consumer Insights**: Enable consumers to make informed dining decisions based on price, cuisine, dietary options, hygiene standards, and peer reviews
3. **Market Intelligence**: Provide researchers, journalists, and industry stakeholders with analytical tools to understand restaurant market dynamics, pricing trends, and food safety patterns

The platform currently serves as an internal research tool with a functioning Streamlit dashboard, but has potential to expand to:
- Public consumer-facing website (similar to Yelp/TripAdvisor but menu-focused)
- B2B SaaS platform for food industry analysts
- Geographic expansion beyond Plymouth to Devon and UK-wide coverage

### Objectives

1. **Comprehensive Data Coverage**: Achieve 90%+ coverage of Plymouth restaurants (150+ establishments) with menu, pricing, and hygiene data — *supports SD-1 (Research Director: Establish Authority), G-2 (150+ Restaurants)*
2. **Data Quality Excellence**: Maintain 95%+ data accuracy through automated validation, duplicate detection, and quality monitoring — *supports SD-4 (Research Analysts: Reliable Data), G-1 (95% Data Quality)*
3. **User Experience**: Deliver sub-2-second dashboard load times and sub-500ms search query responses — *supports SD-5 (Consumers: Dietary Needs), G-4 (<500ms Performance)*
4. **Ethical & Legal Compliance**: Operate within legal boundaries (UK GDPR, Computer Misuse Act, Copyright law) with respectful web scraping practices — *supports SD-2 (Minimize Legal Risk), G-3 (100% Ethical Compliance)*
5. **Cost Efficiency**: Keep total infrastructure and operational costs under £100/month — *supports SD-10 (Operations: Minimize Costs), G-5 (Costs <£100/month)*
6. **Geographic Enrichment**: Integrate ONS geography data for spatial analytics and demographic context — *new in v2.0*

### Expected Outcomes

**Quantitative Outcomes**:
- **Restaurant Coverage**: 150+ Plymouth restaurants catalogued (current: 243 restaurants)
- **Menu Item Catalog**: 10,000+ menu items with pricing data (current: 2,625 items)
- **Hygiene Rating Coverage**: 80%+ of restaurants matched with FSA hygiene ratings (current: 49/98 = 50%)
- **Review Data Integration**: 60%+ of restaurants with Trustpilot reviews (current: 63/98 = 64%, 9,410 reviews)
- **Performance**: <2s dashboard page load (p95), <500ms search queries (p95)
- **Data Quality**: 95%+ completeness for required fields, 98%+ price extraction accuracy
- **Cost**: ≤£100/month operational costs (infrastructure, APIs, hosting)
- **Data Sources**: 8+ integrated data sources (current: 8 operational)

**Qualitative Outcomes** (mapped to stakeholder outcomes):
- **O-1**: Establish Plymouth Research as the authoritative source for Plymouth restaurant menu data — 10+ media citations by Month 12
- **O-2**: Zero legal or regulatory violations — no ICO complaints, no cease-and-desist letters
- **O-3**: Operational sustainability achieved — costs <£100/month for 6+ consecutive months
- **O-4**: User satisfaction and adoption targets met — 1,000+ monthly searches, >4.0/5.0 satisfaction

### Project Scope

**In Scope**:
- Restaurant discovery and data aggregation (menus, prices, descriptions, dietary tags)
- Integration with public data sources (FSA hygiene ratings, Google Places, Trustpilot reviews)
- Integration with business registries (Companies House financials, Plymouth licensing, business rates)
- ONS geography enrichment (ward, LSOA, parliamentary constituency, IMD deprivation data)
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
- OpenStreetMap community data integration (identified in DSCT-v1.0, deferred)
- Yelp Fusion or Foursquare API integration (identified in DSCT-v1.0, deferred due to cost)

---

## Stakeholders

| Stakeholder | Role | Organization | Involvement Level | Driver Ref |
|-------------|------|--------------|-------------------|------------|
| Research Director | Executive Sponsor / Project Owner | Plymouth Research | Decision maker, strategic oversight, budget authority | SD-1, SD-2 |
| Data Engineer | Technical Lead / Implementation | Plymouth Research | Architecture decisions, scraping logic, development | SD-3 |
| Research Analysts | Primary Internal Users | Plymouth Research | Requirements input, user testing, data consumers | SD-4 |
| Operations/IT | Infrastructure & Maintenance | Plymouth Research | Deployment, monitoring, cost management | SD-10 |
| Legal/Compliance Advisor | Risk & Compliance | External Consultant | GDPR review, scraping legality, copyright guidance | SD-8 |
| Plymouth Consumers | Beneficiaries (External) | General Public | User acceptance, feature feedback | SD-5 |
| Restaurant Owners | Data Sources (External) | Local Businesses | Opt-out requests, data accuracy feedback | SD-6 |
| Food Writers/Journalists | Users & Amplifiers (External) | Media/Publications | Data-driven reporting, media citations | SD-7 |
| ICO (Information Commissioner) | Regulator (External) | UK Government | GDPR compliance oversight | SD-9 |
| FSA (Food Standards Agency) | Data Provider (External) | UK Government | Hygiene rating data source (OGL) | — |
| Google Places | Data Provider (External) | Google | Restaurant metadata and reviews | — |
| Trustpilot | Data Provider (External) | Trustpilot | Customer review data | — |
| Companies House | Data Provider (External) | UK Government | Business financial data (free API) | — |
| ONS (Office for National Statistics) | Data Provider (External) | UK Government | Postcode directory, geography lookups | — |

---

## Business Requirements

### BR-001: Comprehensive Restaurant Coverage

**Description**: The platform MUST provide comprehensive coverage of Plymouth restaurants, targeting 90%+ of establishments to ensure utility for consumers and researchers.

**Rationale**: Partial coverage creates selection bias and limits platform value. Users expect to find any Plymouth restaurant they search for.

**Success Criteria**:
- Minimum 150 restaurants catalogued (representing 90%+ of Plymouth restaurants/bars/cafes)
- Active restaurant status tracked (operational, temporarily closed, permanently closed)
- Coverage gaps identified and documented (e.g., restaurants blocking scraping, no online presence)
- Geographic coverage includes Plymouth city centre and surrounding areas (PL1-PL9 postcodes)

**Priority**: MUST_HAVE

**Stakeholder**: Research Director (SD-1), Plymouth Consumers (SD-5), Research Analysts (SD-4)

**Traceability**: Goal G-2 (150+ Restaurants), Outcome O-1 (Authoritative Source), Principle #1 (Data Quality First)

**Risk Alignment**: R-002 (Web Scraping Technically Infeasible), R-013 (Opt-Out Requests Exceed 20%)

**Current Status**: ✅ IMPLEMENTED (243 restaurants tracked)

---

### BR-002: Multi-Source Data Aggregation

**Description**: The platform MUST aggregate data from multiple authoritative sources to provide comprehensive restaurant intelligence beyond just menu data.

**Rationale**: Combining menu data with hygiene ratings, customer reviews, financial health, and geographic context provides holistic view unavailable from any single source. This differentiation is Plymouth Research's competitive advantage.

**Success Criteria**:
- FSA Food Hygiene Rating Scheme integration (official government safety ratings)
- Trustpilot review integration (customer satisfaction data)
- Google Places integration (location, contact info, service options)
- Companies House integration (financial health indicators, turnover, profit/loss, net assets)
- Plymouth licensing database integration (licensing activities and hours)
- Business rates data integration (property values and business categories)
- ONS geography enrichment (ward, LSOA, parliamentary constituency, IMD deprivation)
- Postcodes.io geocoding validation (latitude/longitude, admin areas)
- Each data source properly attributed in user interface (legal compliance)

**Priority**: MUST_HAVE

**Stakeholder**: Research Director (SD-1), Research Analysts (SD-4), Food Writers (SD-7)

**Traceability**: Goal G-8 (Architecture Design), Outcome O-1 (Authoritative Source), Principle #7 (Single Source of Truth)

**Current Status**: ✅ IMPLEMENTED (8 data sources integrated, ONS/postcodes.io newly added)

---

### BR-003: Cost-Efficient Operations

**Description**: The platform MUST maintain total operational costs below £100/month while supporting 150+ restaurants to ensure financial sustainability.

**Rationale**: Plymouth Research is an independent research organisation with limited budget. Cost efficiency is critical for long-term viability.

**Success Criteria**:
- Total monthly costs (infrastructure + APIs + hosting) ≤ £100
- Cost per restaurant ≤ £0.67/month (£100 / 150 restaurants)
- Free or low-cost data sources prioritised (FSA, Companies House, ONS, VOA are free; Google Places within free tier)
- Infrastructure auto-scales down during low-traffic periods to minimise waste
- Monthly cost tracking dashboard implemented to monitor spend

**Priority**: MUST_HAVE

**Stakeholder**: Research Director (SD-1), Operations/IT (SD-10)

**Traceability**: Goal G-5 (Costs <£100/month), Outcome O-3 (Operational Sustainability), Principle #6 (Cost Efficiency), Principle #2 (Open Source Preferred)

**Risk Alignment**: R-005 (Cloud Costs Exceed £100/Month Budget)

**Current Status**: ✅ IMPLEMENTED (current costs minimal: SQLite is free, Streamlit Cloud free tier)

---

### BR-004: Legal and Ethical Compliance

**Description**: The platform MUST operate within legal boundaries (UK GDPR, Computer Misuse Act 1990, Copyright law) and ethical web scraping standards to avoid legal liability and reputational damage.

**Rationale**: Unethical or illegal scraping creates existential risk: IP blocking, legal action, regulatory fines, reputational damage. Plymouth Research prioritises ethical operations.

**Success Criteria**:
- Zero robots.txt violations (100% compliance with disallow directives)
- Rate limiting enforced: minimum 5 seconds between requests per domain
- Honest User-Agent string identifying Plymouth Research with contact email
- No personal data (PII) scraped beyond public business contact information
- Data Protection Impact Assessment (DPIA) completed and approved (ARC-001-DPIA-v1.0)
- Privacy policy published and accessible
- Restaurant opt-out mechanism implemented and honoured within 72 hours
- FSA, Trustpilot, Google data properly attributed per licence terms
- Open Government Licence v3.0 compliance for all government data (FSA, ONS, VOA)

**Priority**: MUST_HAVE (NON-NEGOTIABLE)

**Stakeholder**: Research Director (SD-2), Legal/Compliance Advisor (SD-8), ICO (SD-9), Restaurant Owners (SD-6)

**Traceability**: Goal G-3 (100% Ethical Compliance), Goal G-8 (DPIA Completion), Outcome O-2 (Zero Legal Violations), Principle #3 (Ethical Web Scraping - NON-NEGOTIABLE), Principle #4 (Privacy by Design - NON-NEGOTIABLE)

**Risk Alignment**: R-001 (GDPR/Legal Non-Compliance - CRITICAL), R-004 (Robots.txt Violations)

**Current Status**: ✅ IMPLEMENTED (robots.txt compliance, rate limiting, DPIA documented)

---

### BR-005: Geographic Scalability

**Description**: The platform SHOULD support future geographic expansion from Plymouth to Devon and UK-wide without architectural rework.

**Rationale**: Current Plymouth focus validates business model. Future growth depends on ability to scale to additional cities without expensive redesign.

**Success Criteria**:
- Database schema supports multiple cities (city field, geographic coordinates, ONS ward/LSOA fields)
- Scraping pipeline configurable by city/region (not hardcoded to Plymouth)
- Performance testing validates 10x capacity (1,500 restaurants, 100,000 menu items)
- Architecture review confirms horizontal scalability (add workers for parallel scraping)
- ONS geography enrichment fields support any UK postcode (not Plymouth-specific)

**Priority**: SHOULD_HAVE (future-proofing)

**Stakeholder**: Research Director (SD-1)

**Traceability**: Principle #5 (Scalability and Extensibility)

**Current Status**: ✅ IMPLEMENTED (architecture supports multi-city; ONS postcode directory covers all UK)

---

### BR-006: Data Freshness and Timeliness

**Description**: The platform MUST provide reasonably fresh data (≤7 days staleness for menu data, ≤30 days for hygiene ratings) to ensure user trust and relevance.

**Rationale**: Stale data (outdated prices, closed restaurants) erodes user trust and platform value. Balance between freshness and ethical scraping rate limits.

**Success Criteria**:
- Menu data refreshed weekly (automated batch scraping)
- FSA hygiene ratings refreshed monthly (government data updated weekly, matcher runs monthly)
- Trustpilot reviews refreshed weekly (incremental updates, only new reviews)
- Companies House data refreshed quarterly (annual filings)
- ONS postcode directory refreshed quarterly (ONS release cycle)
- Data staleness displayed to users (e.g., "Last updated: 2026-02-15")
- Automated monitoring alerts if data refresh fails
- Graceful degradation: show cached data with staleness warning if refresh fails

**Priority**: MUST_HAVE

**Stakeholder**: Plymouth Consumers (SD-5), Research Analysts (SD-4)

**Traceability**: Goal G-1 (95% Data Quality - timeliness dimension), Principle #1 (Data Quality First)

**Current Status**: ⚠️ PARTIALLY IMPLEMENTED (manual refresh workflow exists, automation pending)

---

### BR-007: Public Dashboard Accessibility

**Description**: The platform MUST provide a public-facing web dashboard accessible to consumers for restaurant discovery and comparison.

**Rationale**: Public access maximises platform utility and establishes Plymouth Research brand. Dashboard is primary user interface.

**Success Criteria**:
- Dashboard accessible via web browser (desktop, tablet, mobile responsive)
- No login required for basic search and browsing (public access)
- Intuitive UX requiring minimal training (target: 90%+ users can complete search task without help)
- Accessibility compliance (WCAG 2.1 AA for future public launch)

**Priority**: MUST_HAVE

**Stakeholder**: Plymouth Consumers (SD-5), Food Writers (SD-7)

**Traceability**: Goal G-6 (Launch Dashboard by Month 4), Goal G-7 (1,000+ Monthly Searches), Outcome O-4 (User Satisfaction)

**Risk Alignment**: R-012 (User Adoption Below Target)

**Current Status**: ✅ IMPLEMENTED (Streamlit dashboard with 8 tabs deployed)

---

### BR-008: Geographic Intelligence and Demographic Context

**Description**: The platform SHOULD enrich restaurant data with ONS geography and demographic context to enable spatial analytics and deprivation-aware research.

**Rationale**: Understanding restaurant distribution by ward, deprivation index, and parliamentary constituency adds research value for journalists, academics, and local government stakeholders. Identified as top recommendation in Data Source Discovery (ARC-001-DSCT-v1.0).

**Success Criteria**:
- All restaurants with valid UK postcodes enriched with ONS ward, LSOA, parliamentary constituency
- IMD (Index of Multiple Deprivation) decile and rank available per restaurant location
- Geographic data sourced from ONS Postcode Directory (free, quarterly updates, OGL licence)
- Postcodes.io API used for real-time geocoding validation
- Dashboard supports geographic filtering or map-based visualisation (future enhancement)

**Priority**: SHOULD_HAVE

**Stakeholder**: Research Analysts (SD-4), Food Writers (SD-7)

**Traceability**: ARC-001-DSCT-v1.0 (recommended source #1: ONS Postcode Directory), ARC-001-DATA-v1.0 (E-001 restaurants entity ONS fields)

**Current Status**: ✅ IMPLEMENTED (ONS geography enrichment added per commit e08ca94)

---

## Functional Requirements

### User Personas

#### Persona 1: Budget-Conscious Consumer (Sarah)
- **Role**: Plymouth resident, young professional
- **Goals**: Find affordable dining options, compare prices across restaurants, identify dietary-friendly establishments
- **Pain Points**: Restaurant websites don't show full menus/prices, difficult to compare options, unaware of hygiene ratings
- **Technical Proficiency**: Medium (comfortable with web apps, smartphone user)
- **Key Use Cases**: UC-001 (Search Restaurants), UC-003 (Price Comparison), UC-005 (Dietary Filtering)
- **Stakeholder Driver**: SD-5 (Find Restaurants Meeting Dietary Needs)

#### Persona 2: Health-Conscious Diner (James)
- **Role**: Plymouth resident, health & fitness enthusiast
- **Goals**: Find restaurants with healthy options (vegan, vegetarian), check hygiene ratings before dining
- **Pain Points**: Restaurant websites lack dietary information, hygiene ratings buried on FSA website
- **Technical Proficiency**: High (early adopter, uses multiple apps)
- **Key Use Cases**: UC-005 (Dietary Filtering), UC-006 (Hygiene Ratings), UC-001 (Search Restaurants)
- **Stakeholder Driver**: SD-5 (Find Restaurants Meeting Dietary Needs)

#### Persona 3: Food Industry Researcher (Dr. Emma)
- **Role**: Academic researcher, hospitality industry analyst
- **Goals**: Analyse pricing trends, study menu diversity, correlate hygiene ratings with business performance, examine geographic distribution by deprivation
- **Pain Points**: Data scattered across multiple sources, no centralised analytics, manual data collection time-consuming
- **Technical Proficiency**: High (data analysis skills, familiar with analytical tools)
- **Key Use Cases**: UC-007 (Analytics), UC-008 (Data Export), UC-009 (Trend Analysis)
- **Stakeholder Driver**: SD-4 (Access Reliable Data), SD-7 (Data-Driven Reporting)

#### Persona 4: Restaurant Owner (Tom)
- **Role**: Plymouth restaurant owner/manager
- **Goals**: Monitor competitor pricing, understand market positioning, verify accuracy of own restaurant data
- **Pain Points**: Concerned about scraped data accuracy, wants ability to correct errors
- **Technical Proficiency**: Medium (business software user)
- **Key Use Cases**: UC-010 (Data Opt-Out), UC-011 (Data Correction)
- **Stakeholder Driver**: SD-6 (Accurate Representation & Visibility)

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
4. System displays list of Italian restaurants (count displayed)
5. User adds "Vegetarian options" dietary filter
6. System refines results to Italian restaurants with vegetarian dishes
7. User adds "Hygiene rating: 5 stars" filter
8. System further refines to 5-star hygiene rated Italian restaurants with vegetarian options
9. User browses restaurant cards showing: name, address, price range, hygiene badge, menu item preview, service option badges
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
- Restaurants marked "is_active = 0" (closed) are excluded unless user explicitly selects "Show closed restaurants"
- Results sorted by restaurant name (alphabetical) by default; user can re-sort by price range or hygiene rating

**Related Requirements**: FR-001, NFR-P-001, NFR-P-002

---

#### UC-002: View Restaurant Details and Menu

**Actor**: Budget-Conscious Consumer (Sarah)

**Main Flow**:
1. User clicks on restaurant card
2. System displays restaurant detail view with tabs: Menu, Details, Reviews, Hygiene, Financial
3. System shows menu items grouped by category (Starters, Mains, Desserts, Drinks)
4. User browses menu items (each showing: name, description, price, dietary tags)
5. User clicks "Dietary Tags" filter "Vegan" — system filters to vegan items only
6. User clicks "Hygiene" tab — system displays FSA rating with detailed scores
7. User clicks "Reviews" tab — system displays Trustpilot reviews (most recent 20, pagination)
8. User views contact information (phone, website, Google Maps link)
9. User views service option badges (Dine-in, Takeout, Delivery, Reservations)

**Related Requirements**: FR-002, FR-005, FR-006, FR-007, NFR-C-001

---

#### UC-003: Compare Prices Across Restaurants

**Actor**: Budget-Conscious Consumer (Sarah), Food Industry Researcher (Dr. Emma)

**Main Flow**:
1. User navigates to "Price Analysis" tab
2. System displays price distribution histogram (all menu items, £0-£50 range)
3. User views average prices by cuisine (bar chart)
4. User filters to specific cuisine
5. System updates analytics to reflect filter
6. User identifies budget-friendly options

**Related Requirements**: FR-003, NFR-P-002

---

#### UC-004: Search Menu Items by Keyword

**Actor**: Health-Conscious Diner (James)

**Main Flow**:
1. User types "fish and chips" in search box
2. System performs full-text search across menu item names and descriptions
3. System displays matching menu items with restaurant name, price, description
4. User clicks item to navigate to restaurant menu with item highlighted

**Related Requirements**: FR-001, FR-002, NFR-P-002

---

#### UC-005: Filter by Dietary Requirements

**Actor**: Health-Conscious Diner (James)

**Main Flow**:
1. User selects dietary filter "Vegan"
2. System filters to restaurants with vegan menu items (count displayed)
3. User applies additional cuisine filter
4. System refines results
5. User browses dietary-compliant menu items

**Business Rules**:
- Dietary tags extracted from menu descriptions (keyword matching)
- Disclaimer displayed: "Dietary information may be incomplete. Verify with restaurant."

**Related Requirements**: FR-004, NFR-Q-001

---

#### UC-006: View FSA Hygiene Ratings

**Actor**: Health-Conscious Diner (James)

**Main Flow**:
1. User filters restaurants by "Hygiene Rating: 5 stars"
2. System displays rated restaurants with hygiene badges
3. User clicks restaurant for detailed scores breakdown (Hygiene, Structural, Confidence)
4. System shows FSA attribution: "Data from Food Standards Agency (Open Government Licence)"

**Related Requirements**: FR-005, NFR-C-001

---

#### UC-007: Analyse Hygiene vs Customer Satisfaction Correlation

**Actor**: Food Industry Researcher (Dr. Emma)

**Main Flow**:
1. User navigates to "Reviews" tab
2. System displays correlation scatter plot (FSA hygiene vs Trustpilot rating)
3. User observes key insights (e.g., fast food chains: 5-star hygiene, poor reviews)
4. User exports correlation data to CSV

**Related Requirements**: FR-006, FR-007, FR-009

---

#### UC-008: Export Data to CSV

**Actor**: Food Industry Researcher (Dr. Emma)

**Main Flow**:
1. User applies filters on dashboard
2. User clicks "Export to CSV" button
3. System generates RFC 4180 compliant CSV (UTF-8)
4. CSV includes attribution footer

**Business Rules**:
- CSV exports limited to 10,000 rows
- Attribution: "Data from Plymouth Research. Contains FSA data (OGL), Trustpilot reviews (public data)."

**Related Requirements**: FR-009, NFR-I-002

---

#### UC-009: Monitor Data Quality Metrics

**Actor**: Product Owner

**Main Flow**:
1. Product Owner accesses admin/monitoring dashboard
2. System displays data quality metrics (completeness, accuracy, timeliness, duplication)
3. Product Owner identifies issues and creates remediation actions

**Related Requirements**: NFR-Q-001, NFR-Q-002, NFR-Q-003

---

#### UC-010: Restaurant Owner Opt-Out Request

**Actor**: Restaurant Owner (Tom)

**Main Flow**:
1. Restaurant owner discovers listing, navigates to opt-out page
2. Owner sends email requesting removal
3. Product Owner verifies ownership
4. Product Owner sets restaurant is_active = 0 (soft delete)
5. Restaurant removed from dashboard within 24 hours
6. Confirmation sent to owner

**Business Rules**:
- Opt-out honoured within 72 hours (GDPR Right to Erasure)
- Soft delete for 30 days, then hard delete

**Related Requirements**: FR-010, NFR-C-002

---

#### UC-011: Restaurant Owner Data Correction Request

**Actor**: Restaurant Owner (Tom)

**Main Flow**:
1. Owner reports incorrect data via email
2. Product Owner verifies claim against source
3. Manual correction applied with audit trail
4. Confirmation sent to owner

**Related Requirements**: FR-010, NFR-Q-003

---

### Functional Requirements Detail

#### FR-001: Restaurant Search and Discovery

**Description**: The system MUST provide search and filtering capabilities enabling users to discover restaurants by cuisine type, price range, dietary requirements, hygiene rating, and service options.

**Relates To**: BR-001, BR-007, UC-001, UC-004

**Acceptance Criteria**:
- [ ] Search by cuisine type (controlled vocabulary)
- [ ] Filter by price range (£, ££, £££, ££££)
- [ ] Filter by dietary requirements (Vegan, Vegetarian, Gluten-Free, Dairy-Free, Nut-Free)
- [ ] Filter by hygiene rating (0-5 stars)
- [ ] Filter by service options (Dine-in, Takeout, Delivery, Reservations)
- [ ] Filter by meal times (Breakfast, Lunch, Dinner service)
- [ ] Toggle to hide permanently/temporarily closed restaurants
- [ ] Multiple filters combinable with logical AND
- [ ] Result count displayed accurately
- [ ] Query performance <500ms (p95)

**Priority**: MUST_HAVE

**Stakeholder**: All user personas

---

#### FR-002: Menu Item Display and Search

**Description**: The system MUST display restaurant menus with full item details and enable keyword search across all menu items.

**Relates To**: BR-001, UC-002, UC-004

**Acceptance Criteria**:
- [ ] Menu items displayed with: name (required), description (optional), price in £ (required), dietary tags
- [ ] Menu items grouped by category (Starters, Mains, Desserts, Drinks)
- [ ] Full-text search across item names and descriptions
- [ ] Prices displayed in consistent £X.XX format
- [ ] Source attribution: "Menu data scraped from [restaurant website URL] on [date]"

**Priority**: MUST_HAVE

**Traceability**: Principle #9 (Data Normalisation)

---

#### FR-003: Price Comparison and Analytics

**Description**: The system MUST provide analytics visualisations comparing prices across restaurants, cuisines, and price ranges.

**Relates To**: BR-001, UC-003

**Acceptance Criteria**:
- [ ] Price distribution histogram
- [ ] Average price by cuisine type (bar chart)
- [ ] Price range distribution pie chart
- [ ] Statistical summary (min, max, mean, median)
- [ ] Analytics filterable by cuisine, dietary tags, restaurant
- [ ] Export analytics data to CSV

**Priority**: MUST_HAVE

---

#### FR-004: Dietary Information Filtering

**Description**: The system MUST identify and filter menu items by dietary requirements.

**Relates To**: UC-005

**Acceptance Criteria**:
- [ ] Dietary tags extracted from menu descriptions (keyword matching)
- [ ] Dietary tag flags in database (is_vegan, is_vegetarian, is_gluten_free)
- [ ] Filter UI with counts (e.g., "Vegan (156 items)")
- [ ] Disclaimer: "Dietary information may be incomplete. Verify with restaurant."

**Priority**: MUST_HAVE

---

#### FR-005: FSA Hygiene Rating Integration

**Description**: The system MUST integrate FSA Food Hygiene Rating Scheme data.

**Relates To**: BR-002, UC-006

**Acceptance Criteria**:
- [ ] FSA Plymouth XML data fetched weekly
- [ ] Multi-factor matching algorithm (name similarity, postcode, address)
- [ ] Hygiene rating (0-5 stars) displayed prominently
- [ ] Detailed scores breakdown (Hygiene, Structural, Confidence)
- [ ] FSA attribution: "Data from Food Standards Agency (Open Government Licence v3.0)"
- [ ] Ratings >6 months old flagged as "May be outdated"

**Priority**: MUST_HAVE

---

#### FR-006: Trustpilot Review Integration

**Description**: The system MUST integrate Trustpilot customer reviews.

**Relates To**: BR-002, UC-007

**Acceptance Criteria**:
- [ ] Reviews displayed with author, title, body, rating, date
- [ ] Reviews sorted by date (most recent first) with pagination
- [ ] Review statistics: total count, average rating, distribution
- [ ] Trustpilot attribution: "Reviews from Trustpilot.com"
- [ ] Incremental updates (only new reviews)

**Priority**: MUST_HAVE

---

#### FR-007: Google Places Integration

**Description**: The system MUST integrate Google Places API data.

**Relates To**: BR-002, UC-001, UC-002

**Acceptance Criteria**:
- [ ] Contact information: phone, website, Google Maps link
- [ ] Service options badges: Dine-in, Takeout, Delivery, Reservations
- [ ] Meal time service: Breakfast, Lunch, Dinner
- [ ] Google rating and review count displayed
- [ ] Business status tracked: Operational, Temporarily Closed, Permanently Closed
- [ ] Geographic coordinates stored

**Priority**: MUST_HAVE

---

#### FR-008: Business Financial Data Integration

**Description**: The system SHOULD integrate Companies House financial data and Plymouth business rates.

**Relates To**: BR-002, UC-007

**Acceptance Criteria**:
- [ ] Companies House API: company number, financials (turnover, profit/loss, net assets, employee count)
- [ ] Financial health score calculated
- [ ] Plymouth licensing data: activities, opening hours
- [ ] Business rates: rateable value, property valuation
- [ ] Financial data in separate tab (researcher audience)
- [ ] Disclaimer: "Financial data is historical. Current performance may differ."

**Priority**: SHOULD_HAVE

**Current Status**: ✅ IMPLEMENTED (enhanced with fuller CH financials per commit e08ca94)

---

#### FR-009: Data Export and API Access

**Description**: The system SHOULD provide CSV data export capabilities.

**Relates To**: UC-008

**Acceptance Criteria**:
- [ ] Export button on filtered search results and analytics views
- [ ] CSV: UTF-8, RFC 4180 compliant
- [ ] Attribution footer in CSV
- [ ] Export limited to 10,000 rows
- [ ] Future: Public REST API (deferred to Phase 2)

**Priority**: SHOULD_HAVE

---

#### FR-010: Restaurant Owner Opt-Out and Correction

**Description**: The system MUST provide opt-out and correction process for restaurant owners.

**Relates To**: BR-004, UC-010, UC-011

**Acceptance Criteria**:
- [ ] Opt-out process documented with contact email
- [ ] Ownership verification (email domain, business registration)
- [ ] Opt-out honoured within 72 hours (GDPR)
- [ ] Soft delete for 30 days, then hard delete
- [ ] Corrections logged with timestamp and source

**Priority**: MUST_HAVE (GDPR compliance)

---

#### FR-011: ONS Geography Enrichment

**Description**: The system SHOULD enrich restaurant records with ONS geographic and demographic data for spatial analytics.

**Relates To**: BR-008, ARC-001-DSCT-v1.0

**Acceptance Criteria**:
- [ ] Postcodes resolved to ONS ward, LSOA, parliamentary constituency via ONS Postcode Directory
- [ ] IMD (Index of Multiple Deprivation) decile and rank populated per restaurant
- [ ] ONS data refreshed quarterly (aligned with ONS release schedule)
- [ ] Postcodes.io API used for real-time geocoding validation
- [ ] Dashboard supports filtering by ward or IMD decile (future enhancement)

**Priority**: SHOULD_HAVE

**Current Status**: ✅ IMPLEMENTED

---

## Non-Functional Requirements (NFRs)

### Performance Requirements

#### NFR-P-001: Dashboard Page Load Time

**Requirement**: Dashboard MUST load initial page content within 2 seconds (p95).

**Measurement Method**: Browser DevTools, Lighthouse score ≥80

**Load Conditions**: 100 concurrent users, 1,000 page views/day

**Priority**: MUST_HAVE

**Traceability**: Principle #12 (Performance Targets), Goal G-4 (<500ms Performance)

---

#### NFR-P-002: Search Query Response Time

**Requirement**: Search queries MUST return results within 500ms (p95).

**Measurement Method**: Database EXPLAIN ANALYSE, application logging

**Priority**: MUST_HAVE

**Traceability**: Principle #12 (Performance Targets), Goal G-4

**Risk Alignment**: R-010 (Performance Requirements Not Met)

---

#### NFR-P-003: Data Refresh Pipeline Duration

**Requirement**: Weekly data refresh MUST complete within 24 hours.

**Acceptance Criteria**:
- Full scrape of 150 restaurants in <24 hours (parallel scraping with rate limiting)
- FSA hygiene matcher in <2 hours
- Trustpilot incremental scrape in <10 hours
- ONS enrichment batch in <1 hour
- Pipeline failure handling with retries

**Priority**: SHOULD_HAVE

---

### Availability and Resilience Requirements

#### NFR-A-001: Dashboard Uptime

**Requirement**: 99% uptime (7.2 hours downtime/month acceptable).

**Acceptance Criteria**:
- Uptime monitoring (UptimeRobot or similar)
- Planned maintenance in low-traffic hours (Sunday 2-4am GMT)
- MTTR target: <2 hours

**Priority**: MUST_HAVE

**Traceability**: Principle #13 (Reliability and Availability)

---

#### NFR-A-002: Graceful Degradation

**Requirement**: System MUST degrade gracefully when dependencies fail.

**Acceptance Criteria**:
- Database unavailable: show cached data with staleness warning
- FSA API unavailable: skip hygiene update, log warning
- Trustpilot scraping fails: log failure, continue to next restaurant
- Full-text search fails: fall back to LIKE-based search

**Priority**: SHOULD_HAVE

---

### Scalability Requirements

#### NFR-S-001: Data Volume Scalability

**Requirement**: Support 10x current data volume (1,500 restaurants, 100,000 menu items) without architectural changes.

**Priority**: SHOULD_HAVE

**Traceability**: Principle #5 (Scalability), BR-005

---

#### NFR-S-002: Concurrent User Scalability

**Requirement**: Support 100 concurrent users with <2s page load (p95).

**Priority**: SHOULD_HAVE

---

### Security Requirements

#### NFR-SEC-001: Data Encryption

**Requirement**: Encrypt data at rest and in transit.

**Acceptance Criteria**:
- HTTPS/TLS enforced (TLS 1.2+)
- API keys stored in environment variables (not hardcoded)
- Database credentials not in Git

**Priority**: MUST_HAVE

**Traceability**: Principle #4 (Privacy by Design)

---

#### NFR-SEC-002: Access Control (Future)

**Requirement**: Implement authentication for admin features when added.

**Priority**: SHOULD_HAVE (future)

---

#### NFR-SEC-003: Dependency Security Scanning

**Requirement**: Scan dependencies for known vulnerabilities.

**Acceptance Criteria**:
- Scanning in CI/CD (Dependabot, pip-audit, or Snyk)
- Critical CVEs (CVSS ≥9.0) block deployment
- Dependencies updated quarterly

**Priority**: SHOULD_HAVE

---

### Compliance and Regulatory Requirements

#### NFR-C-001: Open Government Licence Compliance

**Requirement**: Comply with OGL v3.0 for FSA, ONS, and VOA data.

**Acceptance Criteria**:
- FSA attribution displayed: "Data from Food Standards Agency (Open Government Licence v3.0)"
- ONS data attributed: "Contains OS data © Crown copyright and database right"
- VOA data attributed where displayed
- Links to OGL licence provided

**Priority**: MUST_HAVE (legal requirement)

---

#### NFR-C-002: UK GDPR Compliance

**Requirement**: Comply with UK GDPR for all data processing.

**Acceptance Criteria**:
- Lawful basis: Legitimate interests (business research, consumer information)
- Data minimisation: Only public business data (no PII)
- DPIA completed and approved (ARC-001-DPIA-v1.0)
- Privacy policy published
- Data subject rights: Erasure (opt-out within 72 hours), Rectification, Access
- Data retention: 12 months for historical data, hard delete after opt-out
- Breach notification: ICO within 72 hours

**Priority**: MUST_HAVE (legal requirement)

**Risk Alignment**: R-001 (GDPR/Legal Non-Compliance - CRITICAL)

---

#### NFR-C-003: Robots.txt and Terms of Service Compliance

**Requirement**: Respect robots.txt and website ToS for all scraping.

**Acceptance Criteria**:
- Robots.txt parser implemented and tested
- Disallowed paths never accessed (100% compliance)
- User-Agent: "PlymouthResearchBot/1.0 (+https://plymouthresearch.co.uk/about)"
- Rate limiting: minimum 5 seconds between requests
- Scraping logs maintained for audit trail

**Priority**: MUST_HAVE (NON-NEGOTIABLE)

**Traceability**: Principle #3 (Ethical Web Scraping - NON-NEGOTIABLE)

---

### Data Quality Requirements

#### NFR-Q-001: Data Completeness

**Requirement**: 95% completeness for required fields (restaurant name, menu item name, price).

**Priority**: MUST_HAVE

**Traceability**: Principle #1 (Data Quality First), Goal G-1

---

#### NFR-Q-002: Data Accuracy

**Requirement**: 98% accuracy for extracted prices.

**Acceptance Criteria**:
- Manual spot-check of 100 random menu items quarterly
- Price range validation: £0.50 ≤ price ≤ £500

**Priority**: MUST_HAVE

---

#### NFR-Q-003: Data Freshness

**Requirement**: 90% of restaurants refreshed within last 7 days; hygiene ratings refreshed monthly.

**Priority**: MUST_HAVE

---

#### NFR-Q-004: Duplicate Detection

**Requirement**: Detect and deduplicate menu items (fuzzy string matching).

**Priority**: SHOULD_HAVE

---

### Maintainability Requirements

#### NFR-M-001: Code Documentation

**Requirement**: Comprehensive documentation (README, CLAUDE.md, ADRs, code comments).

**Priority**: SHOULD_HAVE

**Current Status**: ✅ IMPLEMENTED

---

#### NFR-M-002: Automated Testing

**Requirement**: Automated tests (unit, integration, E2E) for critical paths.

**Priority**: SHOULD_HAVE

**Current Status**: ❌ NOT IMPLEMENTED

---

#### NFR-M-003: Infrastructure as Code

**Requirement**: Infrastructure defined as code, version-controlled.

**Priority**: SHOULD_HAVE

**Current Status**: ⚠️ PARTIALLY IMPLEMENTED

---

### Observability Requirements

#### NFR-O-001: Structured Logging

**Requirement**: Structured logs (JSON) for debugging and audit trails.

**Priority**: SHOULD_HAVE

**Current Status**: ⚠️ PARTIALLY IMPLEMENTED

---

#### NFR-O-002: Metrics and Monitoring

**Requirement**: Operational metrics (scraping success, data quality, API errors).

**Priority**: SHOULD_HAVE

**Current Status**: ❌ NOT IMPLEMENTED

---

## Integration Requirements

### INT-001: FSA Food Hygiene Rating Scheme

**Purpose**: Official government hygiene ratings for food safety transparency

**Integration Type**: XML over HTTP (weekly batch)

**Data Exchanged**: Hygiene ratings, detailed scores, business info for 1,841 Plymouth establishments

**Authentication**: None (public data)

**Licence**: Open Government Licence v3.0

**Priority**: MUST_HAVE

**Current Status**: ✅ IMPLEMENTED

---

### INT-002: Trustpilot Reviews

**Purpose**: Customer satisfaction insights from peer reviews

**Integration Type**: Web scraping (weekly incremental)

**Data Exchanged**: Reviews (author, title, body, rating, date), business profiles

**Authentication**: None (public pages)

**Rate Limiting**: 2.5s between pages, 5s between restaurants

**Priority**: MUST_HAVE

**Current Status**: ✅ IMPLEMENTED (63/98 restaurants, 9,410 reviews)

---

### INT-003: Google Places API

**Purpose**: Location, contact, service options, reviews

**Integration Type**: REST API (monthly refresh)

**Data Exchanged**: Place details, service options, reviews (up to 5 per restaurant)

**Authentication**: API key (environment variable)

**Cost**: Free tier (1,000 requests/month)

**Priority**: MUST_HAVE

**Current Status**: ✅ IMPLEMENTED (98/98 restaurants)

---

### INT-004: Companies House API

**Purpose**: Business financial health indicators

**Integration Type**: REST API (quarterly refresh)

**Data Exchanged**: Company profile, financial statements (turnover, profit/loss, net assets, employees)

**Authentication**: API key (free registration)

**Cost**: Free (600 requests/5 minutes)

**Priority**: SHOULD_HAVE

**Current Status**: ✅ IMPLEMENTED (enhanced financials per commit e08ca94)

---

### INT-005: ONS Postcode Directory

**Purpose**: Geographic enrichment — ward, LSOA, parliamentary constituency, IMD deprivation

**Integration Type**: Bulk CSV download (quarterly)

**Data Exchanged**: Postcode to geography mapping (ward, LSOA, parliamentary constituency, IMD decile/rank)

**Authentication**: None (free download)

**Licence**: Open Government Licence v3.0 / OS data licence

**Priority**: SHOULD_HAVE

**Current Status**: ✅ IMPLEMENTED (new in v2.0)

---

### INT-006: Postcodes.io API

**Purpose**: Real-time geocoding validation and address enrichment

**Integration Type**: REST API (on-demand)

**Data Exchanged**: Postcode lookup → latitude, longitude, admin district, ward, parliamentary constituency

**Authentication**: None (free, no API key required)

**Rate Limiting**: 100 requests/minute (generous free tier)

**Priority**: SHOULD_HAVE

**Current Status**: ✅ IMPLEMENTED (new in v2.0)

---

### INT-007: Plymouth City Council Licensing Data

**Purpose**: Licensing activities, opening hours

**Integration Type**: Web scraping (monthly)

**Authentication**: None (public data)

**Priority**: SHOULD_HAVE

**Current Status**: ✅ IMPLEMENTED

---

### INT-008: VOA Business Rates

**Purpose**: Property valuation and business categories

**Integration Type**: CSV download (quarterly)

**Licence**: Open Government Licence v3.0

**Priority**: SHOULD_HAVE

**Current Status**: ✅ IMPLEMENTED

---

### Integration Summary

| # | System | Type | Frequency | Auth | Cost | Status |
|---|--------|------|-----------|------|------|--------|
| INT-001 | FSA Hygiene API | XML/HTTP | Weekly | None | Free | ✅ |
| INT-002 | Trustpilot | Web scraping | Weekly | None | Free | ✅ |
| INT-003 | Google Places API | REST API | Monthly | API key | Free tier | ✅ |
| INT-004 | Companies House API | REST API | Quarterly | API key | Free | ✅ |
| INT-005 | ONS Postcode Directory | Bulk CSV | Quarterly | None | Free | ✅ |
| INT-006 | Postcodes.io API | REST API | On-demand | None | Free | ✅ |
| INT-007 | Plymouth Licensing | Web scraping | Monthly | None | Free | ✅ |
| INT-008 | VOA Business Rates | CSV | Quarterly | None | Free | ✅ |

---

## Data Requirements

### DR-001: Restaurant Master Data

**Description**: Master database of restaurants with comprehensive attributes (52+ columns per ARC-001-DATA-v1.0 entity E-001).

**Key Fields**: restaurant_id (PK), name, cuisine_type, address, postcode, website_url, is_active, data_source, latitude, longitude, city, plus hygiene (9 cols), Trustpilot (5 cols), Google (16+ cols), Companies House (20+ cols), licensing, business rates, ONS geography fields

**Data Retention**: Permanent for active restaurants; 30 days after opt-out then hard delete

**GDPR Classification**: Public business data

**Priority**: MUST_HAVE

**Current Status**: ✅ IMPLEMENTED (243 restaurants, 52+ columns)

---

### DR-002: Menu Item Data

**Description**: Menu items with pricing, descriptions, and dietary attributes (E-002 in DATA-v1.0).

**Key Fields**: item_id (PK), restaurant_id (FK), item_name, price, currency (GBP), category, description, is_vegetarian, is_vegan, is_gluten_free, allergen_info, scraped_at, last_updated

**Validation**: price £0.50-£500, item_name NOT NULL length ≥3

**Data Retention**: 12 months then deleted

**Priority**: MUST_HAVE

**Current Status**: ✅ IMPLEMENTED (2,625 items)

---

### DR-003: Trustpilot Reviews Data

**Description**: Customer reviews from Trustpilot (E-003 in DATA-v1.0).

**Key Fields**: review_id (PK), restaurant_id (FK), review_date, author_name (pseudonym), review_title, review_body, rating (1-5), author_location, scraped_at

**Privacy Note**: Author names are pseudonyms from public profiles. No PII collected.

**Data Retention**: 12 months then deleted

**Priority**: MUST_HAVE

**Current Status**: ✅ IMPLEMENTED (9,410 reviews)

---

### DR-004: Google Reviews Data

**Description**: Google reviews (up to 5 per restaurant, E-004 in DATA-v1.0).

**Data Retention**: 12 months then deleted

**Priority**: SHOULD_HAVE

**Current Status**: ✅ IMPLEMENTED (481 reviews)

---

### DR-005: Beverages Data

**Description**: Beverage data with categories (E-005 in DATA-v1.0).

**Priority**: SHOULD_HAVE

**Current Status**: ✅ IMPLEMENTED

---

### DR-006: Data Quality Metrics

**Description**: Track data quality metrics (completeness, accuracy, timeliness, duplication) per ARC-001-DATA-v1.0 entity E-006.

**Priority**: SHOULD_HAVE

**Current Status**: ⚠️ NOT IMPLEMENTED (future improvement)

---

### DR-007: Scraping Audit Log

**Description**: Track scraping activities for compliance audit (E-007 in DATA-v1.0).

**Priority**: SHOULD_HAVE

**Current Status**: ✅ IMPLEMENTED (new table per commit e08ca94)

---

### DR-008: Manual Match Records

**Description**: Track human-verified data matches for quality assurance (E-008 in DATA-v1.0).

**Priority**: SHOULD_HAVE

**Current Status**: ✅ IMPLEMENTED (new table per commit e08ca94)

---

## Constraints and Assumptions

### Technical Constraints

**TC-1**: SQLite database engine — suitable for current scale (243 restaurants) but may require migration to PostgreSQL at 1,000+ restaurants

**TC-2**: Streamlit framework — excellent for rapid prototyping but limited for complex interactive UIs; may need migration for Phase 2

**TC-3**: Python 3.8+ required — all dependencies compatible

**TC-4**: Google Places API free tier limited to 1,000 requests/month — refresh ~100 restaurants/month

### Business Constraints

**BC-1**: Total operational budget ≤ £100/month (non-negotiable for sustainability)

**BC-2**: Single developer/operator (Mark Craddock) — architecture must be maintainable by one person

**BC-3**: Plymouth geographic focus for Phase 1 — expansion requires separate project approval

### Assumptions

**A-1**: Restaurant websites remain publicly accessible (not behind paywalls or login walls)

**A-2**: FSA continues providing free XML data under OGL

**A-3**: Google Places API maintains free tier (1,000 requests/month)

**A-4**: ONS continues quarterly postcode directory releases under OGL

**A-5**: UK GDPR legitimate interests basis applies to public business data aggregation

---

## Requirement Conflicts & Resolutions

### Conflict C-1: Data Freshness vs Ethical Scraping Rate Limits

**Conflicting Requirements**:
- **BR-006 (Data Freshness)**: Weekly menu data refresh
- **NFR-C-003 (Ethical Scraping)**: Minimum 5-second delay between requests

**Stakeholders Involved**:
- **Plymouth Consumers (SD-5)**: Want fresh data
- **Restaurant Owners (SD-6)**: Want minimal server load

**Nature of Conflict**: More frequent scraping = fresher data but higher server burden on restaurant websites. Ethical scraping principle is NON-NEGOTIABLE.

**Resolution Strategy**: **PRIORITISE** (Ethics over Freshness)
- **Decision**: Weekly scraping with 5-second rate limits. Principle #3 is NON-NEGOTIABLE.
- **Rationale**: Legal and ethical compliance cannot be compromised. Weekly freshness acceptable for MVP.
- **Stakeholder Impact**: Users accept 7-day staleness; restaurant owners protected.
- **Future Mitigation**: Explore restaurant partnerships for API access (Phase 2)

**Decision Authority**: Product Owner per RACI matrix

---

### Conflict C-2: Comprehensive Coverage vs Budget Constraints

**Conflicting Requirements**:
- **BR-001 (Comprehensive Coverage)**: 150+ restaurants for 90% coverage
- **BR-003 (Cost Efficiency)**: ≤£100/month total costs

**Stakeholders Involved**:
- **Research Director (SD-1)**: Wants broad coverage for authority
- **Operations/IT (SD-10)**: Wants minimal costs

**Nature of Conflict**: More restaurants = more compute, storage, and API costs. From STKE Conflict Analysis: "Phased approach recommended."

**Resolution Strategy**: **COMPROMISE**
- **Decision**: 150 restaurants using free/open-source tools + free API tiers
- **Rationale**: Open-source scraping (Scrapy, BeautifulSoup) = zero licensing. FSA, ONS, Companies House, VOA = free. Google Places within free tier.
- **Cost Model**: £0/month currently (SQLite free, Streamlit Cloud free tier, all APIs free)
- **If costs rise**: Maintain 100-120 high-value restaurants rather than forcing 150

**Decision Authority**: Research Director with Operations/IT input

---

### Conflict C-3: Public Access vs Data Subject Privacy

**Conflicting Requirements**:
- **BR-007 (Public Dashboard)**: No login required for consumers
- **NFR-C-002 (GDPR Compliance)**: Data minimisation and opt-out for data subjects

**Stakeholders Involved**:
- **Plymouth Consumers (SD-5)**: Want unrestricted access
- **Restaurant Owners (SD-6)**: Want control over their data
- **ICO (SD-9)**: Expects GDPR compliance

**Resolution Strategy**: **INNOVATE** (Public with Safeguards)
- **Decision**: Public read-only dashboard + transparent opt-out + DPIA
- **Rationale**: Lawful basis = legitimate interests; only public business data; prominent opt-out; DPIA completed (ARC-001-DPIA-v1.0)
- **Impact**: Users get unrestricted access; owners get 72-hour opt-out; ICO satisfied via DPIA

**Decision Authority**: Product Owner with legal review

---

### Conflict C-4: Speed of Delivery vs Data Quality

**Conflicting Requirements**:
- **G-6 (Launch by Month 4)**: Timely launch to build authority
- **G-1 (95% Data Quality)**: High accuracy before public launch

**Stakeholders Involved**:
- **Research Director (SD-1)**: Wants timely launch
- **Data Engineer (SD-3)**: Wants quality implementation
- **Research Analysts (SD-4)**: Need reliable data

**Source**: STKE Conflict Analysis, Conflict 3

**Resolution Strategy**: **PHASE**
- **Decision**: Launch with 90%+ quality (Month 4), iterate to 95%+ by Month 6
- **Quality Gates**: Non-negotiable 90% data quality, <1000ms performance, zero critical bugs before launch
- **Beta Testing**: Month 3 with 10 users catches issues before public launch
- **Communication**: "Continuous improvement" approach to stakeholders

**Decision Authority**: Research Director (Accountable per RACI)

---

## Requirements Traceability Matrix

| Req ID | Category | Stakeholder Drivers | Goals | Principles | Use Cases | Priority | Status |
|--------|----------|---------------------|-------|------------|-----------|----------|--------|
| BR-001 | Business | SD-1, SD-4, SD-5 | G-2 | #1 | UC-001 | MUST | ✅ |
| BR-002 | Business | SD-1, SD-4, SD-7 | G-8 | #7 | UC-006, UC-007 | MUST | ✅ |
| BR-003 | Business | SD-1, SD-10 | G-5 | #2, #6 | — | MUST | ✅ |
| BR-004 | Business | SD-2, SD-6, SD-8, SD-9 | G-3, G-8 | #3, #4 | UC-010 | MUST | ✅ |
| BR-005 | Business | SD-1 | — | #5 | — | SHOULD | ✅ |
| BR-006 | Business | SD-4, SD-5 | G-1 | #1 | UC-001 | MUST | ⚠️ |
| BR-007 | Business | SD-5, SD-7 | G-6, G-7 | — | All | MUST | ✅ |
| BR-008 | Business | SD-4, SD-7 | — | — | UC-007 | SHOULD | ✅ |
| FR-001 | Functional | All | G-4 | #12 | UC-001, UC-004 | MUST | ✅ |
| FR-002 | Functional | SD-5 | G-1 | #9 | UC-002, UC-004 | MUST | ✅ |
| FR-003 | Functional | SD-4, SD-5, SD-7 | — | #12 | UC-003 | MUST | ✅ |
| FR-004 | Functional | SD-5 | G-1 | #1 | UC-005 | MUST | ✅ |
| FR-005 | Functional | SD-5 | G-1 | #3, #4 | UC-006 | MUST | ✅ |
| FR-006 | Functional | All | — | #3 | UC-007 | MUST | ✅ |
| FR-007 | Functional | All | — | — | UC-001, UC-002 | MUST | ✅ |
| FR-008 | Functional | SD-4, SD-7 | — | — | UC-007 | SHOULD | ✅ |
| FR-009 | Functional | SD-4, SD-7 | — | #10, #11 | UC-008 | SHOULD | ⚠️ |
| FR-010 | Functional | SD-6, SD-8 | G-3 | #4 | UC-010, UC-011 | MUST | ✅ |
| FR-011 | Functional | SD-4, SD-7 | — | — | UC-007 | SHOULD | ✅ |
| NFR-P-001 | Performance | All | G-4 | #12 | All | MUST | ✅ |
| NFR-P-002 | Performance | All | G-4 | #12 | UC-001, UC-004 | MUST | ✅ |
| NFR-P-003 | Performance | SD-10 | — | #5, #12 | — | SHOULD | ✅ |
| NFR-A-001 | Availability | All | — | #13 | All | MUST | ⚠️ |
| NFR-A-002 | Availability | All | — | #13 | All | SHOULD | ⚠️ |
| NFR-S-001 | Scalability | SD-1 | — | #5 | — | SHOULD | ✅ |
| NFR-S-002 | Scalability | All | G-7 | #5 | — | SHOULD | ⚠️ |
| NFR-SEC-001 | Security | All | — | #4 | — | MUST | ⚠️ |
| NFR-SEC-002 | Security | SD-10 | — | #4 | UC-009 | SHOULD | ❌ |
| NFR-SEC-003 | Security | All | — | #17 | — | SHOULD | ❌ |
| NFR-C-001 | Compliance | SD-8, SD-9 | G-3 | #3 | UC-006 | MUST | ✅ |
| NFR-C-002 | Compliance | SD-2, SD-6, SD-8, SD-9 | G-3 | #4 | UC-010 | MUST | ✅ |
| NFR-C-003 | Compliance | SD-6, SD-8 | G-3 | #3 | All scraping | MUST | ✅ |
| NFR-Q-001 | Data Quality | All | G-1 | #1 | All | MUST | ✅ |
| NFR-Q-002 | Data Quality | All | G-1 | #1 | UC-002, UC-003 | MUST | ✅ |
| NFR-Q-003 | Data Quality | All | G-1 | #1 | All | MUST | ⚠️ |
| NFR-Q-004 | Data Quality | SD-4 | G-1 | #1 | UC-003 | SHOULD | ⚠️ |
| NFR-M-001 | Maintainability | SD-3, SD-10 | G-8 | #14 | — | SHOULD | ✅ |
| NFR-M-002 | Maintainability | SD-3 | — | #16 | — | SHOULD | ❌ |
| NFR-M-003 | Maintainability | SD-3, SD-10 | — | #15 | — | SHOULD | ⚠️ |
| NFR-O-001 | Observability | SD-10 | — | #18 | UC-009 | SHOULD | ⚠️ |
| NFR-O-002 | Observability | SD-10 | — | #18 | UC-009 | SHOULD | ❌ |
| INT-001 | Integration | SD-5 | G-1 | #3, #11 | UC-006 | MUST | ✅ |
| INT-002 | Integration | All | — | #3 | UC-007 | MUST | ✅ |
| INT-003 | Integration | All | — | — | UC-001 | MUST | ✅ |
| INT-004 | Integration | SD-4, SD-7 | — | — | UC-007 | SHOULD | ✅ |
| INT-005 | Integration | SD-4, SD-7 | — | — | UC-007 | SHOULD | ✅ |
| INT-006 | Integration | SD-4 | — | — | — | SHOULD | ✅ |
| INT-007 | Integration | SD-4 | — | — | — | SHOULD | ✅ |
| INT-008 | Integration | SD-4 | — | — | — | SHOULD | ✅ |
| DR-001 | Data | All | G-2 | #7, #8 | All | MUST | ✅ |
| DR-002 | Data | SD-5 | G-1 | #1, #9 | UC-002-005 | MUST | ✅ |
| DR-003 | Data | All | — | — | UC-007 | MUST | ✅ |
| DR-004 | Data | All | — | — | UC-007 | SHOULD | ✅ |
| DR-005 | Data | — | — | — | — | SHOULD | ✅ |
| DR-006 | Data | SD-10 | G-1 | #1 | UC-009 | SHOULD | ❌ |
| DR-007 | Data | SD-8 | G-3 | #3, #8 | — | SHOULD | ✅ |
| DR-008 | Data | SD-4 | G-1 | #1 | — | SHOULD | ✅ |

**Legend**: ✅ Implemented | ⚠️ Partial | ❌ Not implemented

---

## Key Gaps and Recommendations

### High Priority Gaps (Block Production Launch)

1. **NFR-SEC-001 (Data Encryption)**: HTTPS enforcement required before public launch
   - **Action**: Deploy to platform with HTTPS (Streamlit Cloud provides free HTTPS)
   - **Timeline**: Before public launch

2. **NFR-A-001 (Uptime Monitoring)**: No proactive monitoring
   - **Action**: Set up UptimeRobot (free tier)
   - **Timeline**: Before public launch

3. **BR-006 / NFR-Q-003 (Data Freshness Automation)**: Manual refresh needs automation
   - **Action**: Implement weekly cron job (GitHub Actions or similar)
   - **Timeline**: Within 2 weeks of launch

### Medium Priority Gaps

4. **NFR-M-002 (Automated Testing)**: No tests exist
   - **Action**: Unit tests for data normalisation, integration tests for DB queries
   - **Timeline**: 1 month post-launch

5. **NFR-O-002 (Metrics and Monitoring)**: No operational metrics
   - **Action**: Simple data quality dashboard (Streamlit admin page)
   - **Timeline**: 1 month post-launch

6. **NFR-SEC-003 (Dependency Scanning)**: No security scanning
   - **Action**: Enable GitHub Dependabot
   - **Timeline**: 2 weeks post-launch

7. **DR-006 (Data Quality Metrics Table)**: Not yet implemented
   - **Action**: Create data_quality_metrics table per DATA-v1.0 specification
   - **Timeline**: 1 month post-launch

### Low Priority Gaps (Future Enhancements)

8. **FR-009 (Public API)**: No programmatic access — defer to Phase 2
9. **NFR-SEC-002 (Access Control)**: No admin authentication — defer until needed
10. **NFR-S-002 (Load Testing)**: Not tested at 100 concurrent users — before marketing push

---

## Success Criteria and KPIs

### Business Success Metrics

| Metric | Baseline | Target | Timeline | Measurement | Goal Ref |
|--------|----------|--------|----------|-------------|----------|
| Restaurant Coverage | 243 | 150+ active | Ongoing | DB count | G-2 |
| Data Quality Accuracy | ~90% | 95%+ | Month 6 | Manual validation | G-1 |
| Monthly Searches | 0 | 1,000+ | Month 9 | Web analytics | G-7 |
| Media Citations | 0 | 10+ | Month 12 | Google Alerts | O-1 |
| Monthly Op Cost | £0 | ≤£100 | Ongoing | Invoice tracking | G-5 |
| Ethical Compliance | N/A | 100% | Ongoing | Audit logs | G-3 |
| Legal Incidents | 0 | 0 | Ongoing | Complaint tracking | O-2 |
| User Satisfaction | N/A | >4.0/5.0 | Month 9 | User surveys | O-4 |

---

## Approval

### Requirements Review

| Reviewer | Role | Status | Date | Comments |
|----------|------|--------|------|----------|
| Research Director | Executive Sponsor | [ ] Approved | [PENDING] | |
| Data Engineer | Technical Lead | [ ] Approved | [PENDING] | |
| Legal/Compliance Advisor | Compliance | [ ] Approved | [PENDING] | |
| Research Analysts | Primary Users | [ ] Approved | [PENDING] | |

---

## Appendices

### Appendix A: Glossary

| Term | Definition |
|------|-----------|
| FSA | Food Standards Agency — UK government body responsible for food safety |
| FHRS | Food Hygiene Rating Scheme — FSA's 0-5 star rating system |
| GDPR | General Data Protection Regulation (UK version) |
| OGL | Open Government Licence v3.0 — licence for UK government data |
| ONS | Office for National Statistics — UK statistics authority |
| VOA | Valuation Office Agency — UK property valuation body |
| LSOA | Lower Super Output Area — ONS geographic unit (~1,500 people) |
| IMD | Index of Multiple Deprivation — measure of relative deprivation |
| PII | Personally Identifiable Information |
| DPIA | Data Protection Impact Assessment |

### Appendix B: Reference Documents

| Document | ID | Description |
|----------|----|-------------|
| Architecture Principles | ARC-000-PRIN-v1.0 | 18 enterprise architecture principles |
| Stakeholder Analysis | ARC-001-STKE-v1.0 | 10 drivers, 8 goals, 4 outcomes |
| Risk Register | ARC-001-RISK-v1.0 | 20 risks (Orange Book framework) |
| Data Model | ARC-001-DATA-v1.0 | 8 entities, 142 attributes |
| Data Source Discovery | ARC-001-DSCT-v1.0 | 22 external data sources evaluated |
| DPIA | ARC-001-DPIA-v1.0 | Data Protection Impact Assessment |
| ADR-001 | ARC-001-ADR-001-v1.0 | Architecture Decision Record |

### Appendix C: External References

| Document | Type | Source | Path |
|----------|------|--------|------|
| FSA FHRS API | Data Source | Food Standards Agency | https://ratings.food.gov.uk/api/open-data-files/FHRS891en-GB.xml |
| Companies House API | Data Source | UK Government | https://developer.company-information.service.gov.uk/ |
| ONS Postcode Directory | Data Source | ONS | https://geoportal.statistics.gov.uk/ |
| Postcodes.io | Data Source | Open Source | https://postcodes.io/ |
| OGL v3.0 | Licence | National Archives | https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/ |

---

**Generated by**: ArcKit `/arckit:requirements` command
**Generated on**: 2026-02-17 12:00:00 GMT
**ArcKit Version**: 2.5.1
**Project**: Plymouth Research Restaurant Menu Analytics (Project 001)
**AI Model**: claude-opus-4-6
**Generation Context**: Major version update from v1.0 incorporating stakeholder analysis (STKE-v1.0), risk register (RISK-v1.0), data model (DATA-v1.0), data source discovery (DSCT-v1.0), DPIA (DPIA-v1.0), and recent database enrichment (ONS geography, enhanced Companies House financials, 3 new tables). All 18 architecture principles traced. 10 stakeholder drivers and 8 goals mapped to requirements.
