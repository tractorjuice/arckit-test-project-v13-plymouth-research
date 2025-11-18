# Project Requirements: Plymouth Research Restaurant Menu Analytics

## Document Control

| Field | Value |
|-------|-------|
| **Document ID** | ARCKIT-001-REQ-20251115-001-PLYMOUTH-RESEARCH |
| **Document Type** | Business and Technical Requirements |
| **Project** | Plymouth Research Restaurant Menu Analytics (Project 001) |
| **Classification** | OFFICIAL |
| **Status** | DRAFT |
| **Version** | 1.0 |
| **Created Date** | 2025-11-15 |
| **Last Modified** | 2025-11-15 |
| **Review Cycle** | Monthly |
| **Next Review Date** | 2025-12-15 |
| **Owner** | Research Director, Plymouth Research |
| **Reviewed By** | [PENDING] |
| **Approved By** | [PENDING] |
| **Distribution** | Project Team, Architecture Team, Legal/Compliance Advisor |

## Revision History

| Version | Date | Author | Changes | Approved By | Approval Date |
|---------|------|--------|---------|-------------|---------------|
| 1.0 | 2025-11-15 | ArcKit AI | Initial creation from `/arckit.requirements` command | [PENDING] | [PENDING] |

## Document Purpose

This document defines comprehensive business, functional, non-functional, data, and integration requirements for the Plymouth Research Restaurant Menu Analytics platform. These requirements will guide technology selection, vendor evaluation (if applicable), architecture design, implementation, and acceptance testing.

The requirements are derived from:
- **Stakeholder Analysis**: `stakeholder-drivers.md` (10 stakeholder groups, 8 goals, 4 outcomes)
- **Architecture Principles**: `.arckit/memory/architecture-principles.md` (18 principles)
- **Manual Process Documentation**: `plan.md` (existing manual menu collection workflow)

---

## Executive Summary

### Business Context

Plymouth Research is an independent research firm building a web scraping and analytics platform to aggregate restaurant menu data across Plymouth, UK. Currently, menu data collection is manual, time-consuming (hours per restaurant), and not scalable. This project automates data collection through ethical web scraping, normalizes menu data (items, prices, dietary tags), and provides a searchable dashboard for consumers, food researchers, and journalists.

The platform addresses a market gap: no existing service provides comprehensive, searchable, aggregated menu data with dietary filters for Plymouth's 150+ restaurants. This capability enables:
- **Consumers**: Finding restaurants by dietary needs (vegan, gluten-free, allergen-free) and price range
- **Researchers**: Market analysis, pricing trends, dietary inclusivity assessment
- **Journalists**: Data-driven food scene reporting with quantitative insights
- **Restaurants**: Free visibility to consumers searching for their offerings

**Strategic Value**:
- Establishes Plymouth Research as authoritative data source (reputation building)
- Demonstrates data-driven research capability to attract future clients/funding
- Provides public good (free access to restaurant information)
- Creates platform for expansion (other cities, other data domains)

### Objectives

The project aims to achieve the following objectives by Month 12 (September 2026):

1. **Data Quality Excellence**: Achieve 95%+ accuracy in menu extraction, price normalization, and dietary tagging
2. **Comprehensive Coverage**: Scrape and maintain menu data for 150+ Plymouth restaurants across diverse cuisines and price ranges
3. **Ethical Compliance**: 100% compliance with web scraping ethics (robots.txt, rate limiting, attribution, opt-out mechanism)
4. **User Adoption**: Launch public dashboard by Month 4 (March 2026), achieving 1,000+ monthly searches by Month 9
5. **Operational Sustainability**: Maintain monthly costs <£100 and search performance <500ms for long-term viability

### Expected Outcomes

- **O-1: Authority & Recognition**: 10+ media citations and 1,000+ monthly searches by Month 12, establishing Plymouth Research as go-to source (supports Research Director's strategic goal)
- **O-2: Legal Compliance**: Zero legal complaints, ICO investigations, or regulatory fines (mitigates Research Director's and Legal Advisor's risk concerns)
- **O-3: Operational Sustainability**: Costs <£100/month, performance <500ms, data quality >95% sustained for 6+ months (enables long-term operation)
- **O-4: User Satisfaction**: >4.0/5.0 user satisfaction rating, 70%+ organic traffic, 30%+ return visitors (validates product-market fit)

### Project Scope

**In Scope**:
- Automated web scraping of 150+ restaurant websites in Plymouth, UK
- ETL pipeline for menu data extraction, normalization, and validation
- PostgreSQL database with full-text search capability
- Interactive dashboard (Streamlit or Plotly Dash) with search, filtering, and CSV export
- Dietary tagging (vegan, vegetarian, gluten-free, nut-free, dairy-free)
- Price normalization to GBP decimal format
- Weekly automated refresh of all restaurant menus
- Robots.txt compliance, rate limiting (5-second delays), and User-Agent transparency
- Opt-out mechanism for restaurants requesting removal
- Data quality monitoring and alerting
- GDPR compliance (UK) with Data Protection Impact Assessment (DPIA)

**Out of Scope** (explicitly excluded from this phase):
- **Mobile app**: Web dashboard only (mobile-responsive design is in scope, native app is not)
- **User accounts/authentication**: Public dashboard with anonymous access (no login required)
- **Real-time scraping**: Weekly refresh only (on-demand refresh for individual restaurants is Phase 2)
- **Food delivery integration**: Scraping from Deliveroo, Uber Eats, Just Eat APIs (Phase 2 - focus on restaurant websites first)
- **Recommendation engine**: No personalized recommendations or AI-powered suggestions (Phase 3)
- **Monetization**: No paid features, subscriptions, or advertising (platform is free public resource)
- **Geographic expansion**: Plymouth only (expansion to other cities in Phase 2+)
- **On-site menu photography**: Automated scraping only (no manual data collection or field visits)

---

## Stakeholders

| Stakeholder | Role | Organization | Involvement Level |
|-------------|------|--------------|-------------------|
| Research Director | Executive Sponsor / Project Owner | Plymouth Research | Decision maker, strategic oversight, budget authority |
| Data Engineer | Technical Lead / Implementation | Plymouth Research | Architecture decisions, day-to-day development, scraper implementation |
| Research Analysts | Primary Internal Users | Plymouth Research | Requirements input, user acceptance testing, manual data QA |
| Operations/IT | Infrastructure & Maintenance | Plymouth Research | Deployment, monitoring, cost management, operational support |
| Legal/Compliance Advisor | Risk & Compliance Oversight | External Consultant | GDPR review, web scraping legality, DPIA approval |
| Plymouth Consumers | External Users (Primary Audience) | General Public | End users of dashboard, feedback providers |
| Restaurant Owners | Data Sources | Local Businesses | Passive stakeholders (data subjects), opt-out requesters |
| Food Writers/Journalists | External Users (Media) | Media/Publications | Data consumers for articles, platform amplifiers |
| ICO (Information Commissioner) | UK Data Protection Regulator | UK Government | Regulatory oversight (low interest unless complaints arise) |
| Local Tourism Board | Potential Future Partner | Plymouth City Council | Monitor stakeholder (potential future collaboration) |

**Stakeholder Traceability**: Requirements are traced to stakeholder goals (G-1 through G-8) documented in `stakeholder-drivers.md`.

---

## Business Requirements

### BR-001: Establish Plymouth Research as Authoritative Data Source

**Description**: Platform must establish Plymouth Research as the recognized, independent, authoritative source for restaurant menu data in Plymouth, building organizational reputation and demonstrating research capability.

**Rationale**: Supports Research Director's strategic goal (SD-1) to differentiate Plymouth Research in local market, attract future funding/clients, and demonstrate innovation in data-driven research.

**Success Criteria**:
- Achieve 10+ media citations (local news, food blogs, academic papers) by Month 12
- Reach 1,000+ monthly searches by Month 9
- Receive partnership inquiries from tourism board, council, or industry groups by Month 12
- Maintain >4.0/5.0 user satisfaction rating in quarterly surveys

**Priority**: **MUST_HAVE** (strategic objective)

**Stakeholder**: Research Director (Executive Sponsor)

**Traces To**: Goal G-1 (Data Quality), G-2 (Restaurant Coverage), G-6 (Dashboard Launch), G-7 (User Adoption) → Outcome O-1 (Recognized as Authoritative Source)

**Architecture Principle Alignment**:
- Principle 1 (Data Quality First): Credibility depends on 95%+ accuracy
- Principle 2 (Open Source Preferred): Transparency builds trust with technical audiences

---

### BR-002: Minimize Legal and Regulatory Risk

**Description**: All web scraping, data storage, and publication activities must comply with UK law (Computer Misuse Act 1990, Copyright Act 1988, UK GDPR) and avoid legal action, ICO fines, or reputational damage.

**Rationale**: Supports Research Director's risk mitigation goal (SD-2) and Legal Advisor's compliance requirement (SD-8). A single legal complaint or ICO fine could bankrupt the small research firm.

**Success Criteria**:
- Zero legal complaints, cease-and-desist letters, or lawsuits by Month 12
- Zero ICO investigations or GDPR fines
- 100% compliance with robots.txt (zero violations logged)
- 100% rate limiting compliance (minimum 5-second delays)
- <5% restaurant opt-out rate (indicates community acceptance)
- DPIA completed and approved by Legal Advisor by Month 1

**Priority**: **MUST_HAVE** (non-negotiable)

**Stakeholder**: Research Director, Legal/Compliance Advisor, ICO (indirectly)

**Traces To**: Goal G-3 (100% Ethical Compliance), G-8 (DPIA Completion) → Outcome O-2 (Zero Legal Violations)

**Architecture Principle Alignment**:
- Principle 3 (Ethical Web Scraping): NON-NEGOTIABLE compliance
- Principle 4 (Privacy by Design): UK GDPR compliance mandatory

---

### BR-003: Achieve Operational Sustainability

**Description**: Platform must operate sustainably with monthly costs <£100, search performance <500ms (p95), and data quality >95%, maintained for 6+ consecutive months, demonstrating long-term viability.

**Rationale**: Plymouth Research has limited budget. High operational costs require external funding or force platform shutdown. Sustainability enables indefinite operation and validates approach for resource-constrained organizations.

**Success Criteria**:
- Monthly operational costs <£100 for Months 7-12 (6 consecutive months)
- Search query response time <500ms (p95) sustained for Months 7-12
- Data quality accuracy >95% in monthly manual validations for Months 7-12
- Dashboard uptime >99% for full year
- Zero on-call incidents requiring emergency intervention

**Priority**: **MUST_HAVE** (viability requirement)

**Stakeholder**: Research Director, Operations/IT, Data Engineer

**Traces To**: Goal G-5 (Cost <£100/month), G-4 (Performance <500ms), G-1 (Data Quality 95%) → Outcome O-3 (Operational Sustainability)

**Architecture Principle Alignment**:
- Principle 6 (Cost Efficiency): Optimize TCO for small organization
- Principle 12 (Performance Targets): <500ms searches enable user satisfaction
- Principle 1 (Data Quality First): >95% accuracy sustains credibility

---

### BR-004: Demonstrate Public Value Through User Adoption

**Description**: Platform must achieve meaningful user adoption (1,000+ monthly searches) and high satisfaction (>4.0/5.0) by Month 9, validating market need and public benefit.

**Rationale**: Supports Research Director's authority goal (SD-1) and validates that platform meets real user needs (Plymouth Consumers SD-5, Food Writers SD-7). Low adoption suggests platform doesn't provide value.

**Success Criteria**:
- 1,000+ unique searches per month by Month 9 (June 2026)
- >4.0/5.0 average user satisfaction rating (quarterly surveys)
- 70%+ organic traffic (non-paid acquisition via SEO, word-of-mouth)
- 30%+ return visitor rate (users come back repeatedly)
- >100 CSV exports per month (researchers/journalists using data)

**Priority**: **MUST_HAVE** (validates investment)

**Stakeholder**: Research Director, Plymouth Consumers, Food Writers/Journalists, Research Analysts

**Traces To**: Goal G-6 (Dashboard Launch), G-7 (1,000+ Searches) → Outcome O-4 (User Satisfaction & Adoption)

**Architecture Principle Alignment**:
- Principle 12 (Performance Targets): Fast searches drive satisfaction
- Principle 14 (Maintainability): Usable platform encourages return visits

---

### BR-005: Timely Dashboard Launch

**Description**: Launch public-facing, fully functional dashboard by Month 4 (March 31, 2026) with search, filtering, export, and attribution features operational.

**Rationale**: Dashboard launch determines when platform value materializes and when users can access data. Delayed launch postpones all downstream benefits (reputation, adoption, media coverage). March 2026 balances quality (4 months development) with timely delivery.

**Success Criteria**:
- Dashboard publicly accessible by March 31, 2026
- 100% of MVP features operational (search, filter, export, attribution)
- >90% of user acceptance test scenarios passed
- >120 restaurants (80% of coverage goal) at launch
- Zero critical bugs blocking launch
- Legal review complete (DPIA approved, privacy policy published)

**Priority**: **MUST_HAVE** (timeline requirement)

**Stakeholder**: Research Director, Data Engineer, Plymouth Consumers

**Traces To**: Goal G-6 (Launch Dashboard Month 4) → Outcome O-1 (Authority), O-4 (User Adoption)

---

### BR-006: Comprehensive Plymouth Restaurant Coverage

**Description**: Successfully scrape and maintain menu data for at least 150 restaurants in Plymouth by Month 6 (May 2026), covering diverse cuisines and price ranges, with weekly automated refresh.

**Rationale**: Comprehensive coverage essential for platform value. Consumers searching for specific cuisines or dietary options need broad choice. 150 restaurants represent majority of Plymouth's dining scene, providing credible coverage for market analysis.

**Success Criteria**:
- 150+ restaurants with active, refreshed menu data by Month 6
- >15 cuisine types represented (British, Italian, Chinese, Indian, Thai, Mediterranean, etc.)
- Balanced price distribution: budget (£5-10), mid-range (£10-20), premium (£20+) establishments
- >90% scraping success rate per weekly refresh cycle
- >95% of restaurants refreshed within last 7 days

**Priority**: **MUST_HAVE** (core value proposition)

**Stakeholder**: Research Director, Research Analysts, Plymouth Consumers, Food Writers

**Traces To**: Goal G-2 (150+ Restaurants) → Outcome O-1 (Authority), O-4 (User Adoption)

---

## Functional Requirements

### User Personas

#### Persona 1: Sarah - Health-Conscious Consumer

- **Role**: Plymouth resident, vegan with gluten intolerance
- **Goals**: Find restaurants offering vegan AND gluten-free menu items without calling multiple establishments or browsing dozens of websites
- **Pain Points**:
  - Must call restaurants to confirm dietary options (time-consuming, socially awkward)
  - Restaurant websites often lack allergen information or dietary tags
  - No aggregated search across Plymouth restaurants for specific dietary combinations
- **Technical Proficiency**: Medium (comfortable with web search, not technical)
- **Use Case Priority**: CRITICAL (primary consumer persona)

#### Persona 2: David - Research Analyst

- **Role**: Research Analyst at Plymouth Research
- **Goals**: Conduct market research on Plymouth restaurant scene (pricing trends, dietary inclusivity, cuisine diversity) and generate reports quickly
- **Pain Points**:
  - Manual menu collection takes hours per restaurant (not scalable)
  - Data entry errors common in manual process
  - No historical data for trend analysis
  - Cannot easily export data for Excel/analysis tools
- **Technical Proficiency**: High (comfortable with CSV, Excel, SQL if needed)
- **Use Case Priority**: HIGH (internal primary user)

#### Persona 3: Emma - Food Journalist

- **Role**: Food writer for Plymouth Herald
- **Goals**: Write data-driven articles about Plymouth's food scene with quantitative insights ("Average main course price is £13.50", "Vegan options increased 40% in 2 years")
- **Pain Points**:
  - No aggregated data source for quantitative food journalism
  - Manual research time-consuming and not comprehensive
  - Need credible source editors will approve
- **Technical Proficiency**: Medium (can use CSV export, prefers simple interfaces)
- **Use Case Priority**: HIGH (media amplifier, drives traffic)

#### Persona 4: James - Budget-Conscious Student

- **Role**: University of Plymouth student
- **Goals**: Find affordable meals (under £10) near campus or in city center
- **Pain Points**:
  - Expensive restaurants prominently featured on Google/TripAdvisor (paid placement)
  - Hard to filter by price range across restaurants
  - Student budget requires careful spending
- **Technical Proficiency**: High (comfortable with web, mobile-first)
- **Use Case Priority**: MEDIUM (large potential user base)

#### Persona 5: Restaurant Owner - Maria

- **Role**: Owner of independent Italian restaurant in Plymouth
- **Goals**: Ensure her restaurant is represented accurately if included in platform, with easy opt-out if desired
- **Pain Points**:
  - Concern about stale menu data misleading customers
  - Worry about price comparison commoditizing her offerings
  - Want control over whether her restaurant is aggregated
- **Technical Proficiency**: Medium (runs business website)
- **Use Case Priority**: MEDIUM (data source, must respect)

---

### Use Cases

#### UC-1: Search Restaurants by Dietary Requirements

**Actor**: Sarah (Health-Conscious Consumer)

**Preconditions**:
- Dashboard is publicly accessible
- Database contains ≥100 restaurants with menu data
- Dietary tags have been extracted and normalized

**Main Flow**:
1. User navigates to dashboard homepage
2. User enters search query: "vegan gluten-free Plymouth"
3. System queries database for restaurants with menu items tagged both "vegan" AND "gluten-free"
4. System displays results sorted by relevance (restaurants with most matching items first)
5. User clicks on restaurant to view full menu with dietary tags highlighted
6. User sees source attribution (link to original restaurant website)
7. User clicks through to restaurant website to make reservation

**Postconditions**:
- Search query logged for analytics (anonymous)
- User finds suitable restaurants and proceeds to booking

**Alternative Flows**:
- **Alt 2a**: If no results match both tags, system suggests relaxing search ("Try searching just 'vegan' or 'gluten-free'")
- **Alt 4a**: If >50 results, system paginates (20 per page)

**Exception Flows**:
- **Ex 3**: If database query fails (timeout, connection error), display "Search temporarily unavailable. Please try again." with retry button

**Business Rules**:
- Dietary tags must be conservative (flag as vegan only if explicitly labeled by restaurant, not inferred)
- Search results must include data freshness indicator ("Last updated: 3 days ago")
- Must link to original restaurant website for attribution

**Priority**: **CRITICAL** (primary use case)

**Traces To**: FR-001, FR-002, FR-003, FR-005, FR-008

---

#### UC-2: Export Menu Data for Analysis

**Actor**: David (Research Analyst)

**Preconditions**:
- User has completed a search query or is viewing aggregated data
- Dashboard includes export functionality

**Main Flow**:
1. User performs search or navigates to "All Restaurants" view
2. User clicks "Export to CSV" button
3. System generates CSV file with columns: restaurant_name, menu_item_name, price_gbp, category, dietary_tags, cuisine_type, last_updated
4. System downloads CSV to user's browser
5. User opens CSV in Excel/Google Sheets for analysis

**Postconditions**:
- CSV export logged for analytics
- User has structured data for external analysis

**Alternative Flows**:
- **Alt 2a**: If result set >10,000 rows, system prompts "Large export. Confirm download?" to prevent accidental huge files

**Exception Flows**:
- **Ex 3**: If CSV generation fails, display error message with support email

**Business Rules**:
- CSV must be RFC 4180 compliant (quoted fields, UTF-8 encoding)
- CSV must include metadata row: "Exported from Plymouth Research - [URL] - [Date]"
- Export must respect attribution requirements (source URLs included if feasible)

**Priority**: **HIGH**

**Traces To**: FR-010, DR-009

---

#### UC-3: Restaurant Requests Opt-Out

**Actor**: Maria (Restaurant Owner)

**Preconditions**:
- Restaurant's menu data is currently in the platform database
- Opt-out form is publicly accessible on platform website

**Main Flow**:
1. Restaurant owner discovers their restaurant is listed on platform (via Google search, word-of-mouth, or notification email)
2. Owner navigates to opt-out form (linked from footer, FAQ, or notification email)
3. Owner fills out form: restaurant name, website URL, email, reason (optional)
4. Owner submits form
5. System emails confirmation to owner ("We received your opt-out request. Your restaurant will be removed within 48 hours.")
6. Operations/IT or Data Engineer reviews request (validates it's legitimate, not spam)
7. Engineer removes restaurant from database and adds to exclusion list (prevents re-scraping)
8. System emails owner: "Your restaurant has been removed from Plymouth Research platform."

**Postconditions**:
- Restaurant data removed from database within 48 hours
- Restaurant added to permanent exclusion list (not re-scraped in future cycles)
- Opt-out request logged for compliance audit trail

**Alternative Flows**:
- **Alt 6a**: If request appears fraudulent (email doesn't match restaurant domain), engineer contacts restaurant directly to verify

**Exception Flows**:
- **Ex 5**: If email fails to send, log error and retry with manual follow-up

**Business Rules**:
- Opt-out requests must be processed within 48 hours (per ethical scraping principle)
- Removed restaurants must not be re-scraped in future (permanent exclusion)
- No justification required from restaurant (opt-out is unconditional right)

**Priority**: **CRITICAL** (legal/ethical requirement)

**Traces To**: FR-015, NFR-C-002, DR-008

---

### Functional Requirements Detail

#### FR-001: Search by Restaurant Name

**Description**: User can search for restaurants by name (full or partial match) with autocomplete suggestions.

**Relates To**: BR-004 (User Adoption), UC-1

**Acceptance Criteria**:
- [ ] Given user types "La Bouchon" in search box, when query submitted, then restaurant "La Bouchon Bistro" appears in results
- [ ] Given user types "italian" in search box, when query submitted, then all restaurants with cuisine_type="Italian" appear in results
- [ ] Given user types 3+ characters, when typing, then autocomplete dropdown shows top 5 matching restaurant names
- [ ] Edge case: Search is case-insensitive ("ITALIAN" = "italian" = "Italian")
- [ ] Edge case: Search handles diacritics correctly ("Café" found when searching "cafe")

**Data Requirements**:
- **Inputs**: Search query string (3-100 characters)
- **Outputs**: List of matching restaurants (name, cuisine, price_range, match_score)
- **Validations**: Sanitize input to prevent SQL injection, trim whitespace, minimum 1 character

**Priority**: **MUST_HAVE**

**Complexity**: **LOW**

**Dependencies**: FR-002 (database query), DR-001 (restaurant table schema)

**Assumptions**: PostgreSQL full-text search or ILIKE queries sufficient for name matching (no need for Elasticsearch initially)

**Architecture Principle Alignment**: Principle 12 (Performance Targets): Autocomplete must respond <200ms

---

#### FR-002: Search by Dietary Tags

**Description**: User can filter restaurants/menu items by dietary tags: vegan, vegetarian, gluten-free, dairy-free, nut-free, with multi-select AND logic.

**Relates To**: BR-004 (User Adoption), UC-1, Stakeholder SD-5 (Consumer Dietary Needs)

**Acceptance Criteria**:
- [ ] Given user selects "vegan" checkbox, when search executed, then only menu items tagged "vegan" appear
- [ ] Given user selects both "vegan" AND "gluten-free", when search executed, then only menu items tagged BOTH appear (AND logic, not OR)
- [ ] Given user selects dietary tag with zero results, when search executed, then display "No results found. Try removing some filters."
- [ ] Edge case: If restaurant doesn't label allergens, items are NOT tagged (conservative approach, don't infer)
- [ ] Edge case: Tags are normalized ("Gluten Free" → "gluten-free", "GF" → "gluten-free")

**Data Requirements**:
- **Inputs**: List of selected dietary tags (0-5 tags)
- **Outputs**: Filtered list of menu items with matching tags
- **Validations**: Tags must match controlled vocabulary (vegan, vegetarian, gluten-free, dairy-free, nut-free)

**Priority**: **MUST_HAVE** (core consumer value proposition)

**Complexity**: **MEDIUM** (tag extraction logic complex)

**Dependencies**: FR-007 (dietary tag extraction), DR-004 (dietary tags table)

**Assumptions**: Keyword-based extraction sufficient initially (ML-based tagging is Phase 2 enhancement)

**Architecture Principle Alignment**: Principle 1 (Data Quality First): Conservative tagging (only tag if restaurant explicitly labels) prevents dangerous inaccuracies for allergy sufferers

---

#### FR-003: Search by Price Range

**Description**: User can filter restaurants by average main course price range: budget (<£10), mid-range (£10-20), premium (£20+).

**Relates To**: BR-004 (User Adoption), UC-1, Stakeholder SD-5 (Consumer - Student Budget)

**Acceptance Criteria**:
- [ ] Given user selects "Budget (<£10)" filter, when search executed, then only restaurants with avg_main_price <£10 appear
- [ ] Given user selects multiple price ranges, when search executed, then restaurants matching ANY selected range appear (OR logic)
- [ ] Given restaurant has no price data, when price filter applied, then restaurant excluded from results
- [ ] Edge case: Average price calculated from main course items only (not starters, sides, desserts)
- [ ] Edge case: If restaurant has <3 menu items, price range flagged as "Insufficient data"

**Data Requirements**:
- **Inputs**: Selected price ranges (1-3 selections)
- **Outputs**: Filtered list of restaurants with avg_main_price in selected ranges
- **Validations**: Price ranges are predefined (not user-entered arbitrary values)

**Priority**: **SHOULD_HAVE** (important for budget-conscious users, not critical to MVP)

**Complexity**: **LOW**

**Dependencies**: FR-006 (price normalization), DR-002 (menu items table with price field)

**Assumptions**: Average main course price is reasonable proxy for "restaurant price level" (more sophisticated pricing analytics in Phase 2)

---

#### FR-004: View Full Menu for Restaurant

**Description**: User can view complete menu for a selected restaurant, organized by category (starters, mains, desserts, drinks), with prices and dietary tags displayed.

**Relates To**: BR-004 (User Adoption), UC-1

**Acceptance Criteria**:
- [ ] Given user clicks restaurant in search results, when detail page loads, then full menu displayed organized by category
- [ ] Given menu item has dietary tags, when item displayed, then tags shown as colored badges (e.g., green "Vegan" badge)
- [ ] Given menu item has price, when item displayed, then price shown in £X.XX format
- [ ] Given menu item has no dietary tags, when item displayed, then no badges shown (don't display "None" or placeholder)
- [ ] Edge case: If category is unknown, items appear in "Other" category at bottom

**Data Requirements**:
- **Inputs**: Restaurant ID
- **Outputs**: Menu items grouped by category, with name, description (optional), price, dietary tags
- **Validations**: Restaurant ID must exist in database

**Priority**: **MUST_HAVE**

**Complexity**: **LOW**

**Dependencies**: DR-002 (menu items table), DR-003 (categories table)

**Assumptions**: Categories extracted from website structure or inferred from item names (e.g., "Fish & Chips" → Mains)

---

#### FR-005: Display Source Attribution

**Description**: Every restaurant and menu item must display source attribution linking back to original restaurant website, with data freshness timestamp.

**Relates To**: BR-002 (Legal Compliance), BR-006 (Restaurant Coverage), Stakeholder SD-6 (Restaurant Accurate Representation)

**Acceptance Criteria**:
- [ ] Given user views restaurant menu, when page loads, then source URL displayed prominently (e.g., "Menu from: [restaurant-website.com]" with clickable link)
- [ ] Given menu data was scraped, when displayed, then freshness timestamp shown (e.g., "Last updated: 3 days ago")
- [ ] Given data is >10 days old, when displayed, then warning badge shown: "Data may be outdated"
- [ ] Edge case: If original website URL is broken/changed, display "Original source no longer available"
- [ ] Edge case: Attribution must be visible on all views (search results, full menu, exported CSV metadata)

**Data Requirements**:
- **Inputs**: Restaurant website URL, last_scraped_at timestamp
- **Outputs**: Attribution link and freshness indicator
- **Validations**: URL must be valid format (http/https)

**Priority**: **MUST_HAVE** (ethical and legal requirement)

**Complexity**: **LOW**

**Dependencies**: DR-001 (restaurant table with source_url field)

**Assumptions**: Linking to source website is legally safe under fair use/linking doctrines (confirmed by legal advisor)

**Architecture Principle Alignment**: Principle 3 (Ethical Scraping): Attribution is mandatory compliance requirement

---

#### FR-006: Normalize Prices to GBP Decimal Format

**Description**: All scraped prices must be normalized to decimal GBP format (e.g., 12.50) for accurate sorting, filtering, and comparison, regardless of source website format.

**Relates To**: BR-001 (Data Quality), BR-003 (Operational Sustainability), Goal G-1 (95% Accuracy)

**Acceptance Criteria**:
- [ ] Given website displays "£12.50", when scraped, then stored as 12.50 (decimal)
- [ ] Given website displays "£12.5", when scraped, then normalized to 12.50 (trailing zero added)
- [ ] Given website displays "12.50 GBP", when scraped, then currency removed and stored as 12.50
- [ ] Given website displays "Twelve pounds fifty", when scraped, then flag as extraction failure (cannot parse text prices reliably)
- [ ] Edge case: Prices outside range £0.50-£150 flagged for manual review (likely extraction errors or outliers)
- [ ] Edge case: If price contains non-numeric characters other than £/. (e.g., "£12.50 per person"), extract first valid price only

**Data Requirements**:
- **Inputs**: Raw price string from website HTML
- **Outputs**: Decimal price (NUMERIC(10,2) in database)
- **Validations**:
  - Price must be ≥0.50 (minimum realistic menu price)
  - Price must be ≤150.00 (maximum realistic single item price - flag outliers for review)
  - Price must have exactly 2 decimal places

**Priority**: **MUST_HAVE** (critical for data quality)

**Complexity**: **MEDIUM** (parsing diverse formats challenging)

**Dependencies**: FR-011 (web scraping), DR-002 (menu items table)

**Assumptions**: Regex-based extraction + normalization logic sufficient for 95%+ of websites (complex cases like "Market Price" or "POA" marked as NULL)

**Architecture Principle Alignment**: Principle 1 (Data Quality First): Accurate price normalization essential for credibility

---

#### FR-007: Extract and Normalize Dietary Tags

**Description**: Automatically extract dietary tags (vegan, vegetarian, gluten-free, dairy-free, nut-free) from menu item names and descriptions using keyword matching, with conservative tagging (only tag if explicitly labeled).

**Relates To**: BR-001 (Data Quality), FR-002 (Dietary Search), Goal G-1 (95% Accuracy)

**Acceptance Criteria**:
- [ ] Given menu item description contains "vegan", "plant-based", or "V" icon, when processed, then tag as "vegan"
- [ ] Given menu item contains "gluten free", "GF", or gluten-free icon, when processed, then tag as "gluten-free"
- [ ] Given menu item contains ambiguous text like "suitable for vegetarians", when processed, then tag as "vegetarian"
- [ ] Given menu item has NO explicit dietary labels, when processed, then NO tags applied (do not infer)
- [ ] Edge case: "Vegan option available" does NOT tag base item as vegan (only tag if item itself is vegan)
- [ ] Edge case: Normalize spelling variations ("gluten free" = "gluten-free" = "GF")

**Data Requirements**:
- **Inputs**: Menu item name, description (optional)
- **Outputs**: Array of dietary tags (0-5 tags per item)
- **Validations**: Tags must match controlled vocabulary (no free-text tags)

**Priority**: **MUST_HAVE** (core consumer value)

**Complexity**: **MEDIUM** (keyword extraction, handling variations)

**Dependencies**: DR-004 (dietary tags table), FR-011 (web scraping gets raw description)

**Assumptions**:
- Keyword matching achieves >90% accuracy (validated in pilot with 30 restaurants)
- ML-based tagging (NLP) is Phase 2 enhancement for edge cases

**Architecture Principle Alignment**: Principle 1 (Data Quality First): Conservative tagging prevents dangerous errors for allergy sufferers

---

#### FR-008: Full-Text Search Across Menu Items

**Description**: User can search for menu items by keyword (e.g., "fish chips", "carbonara", "sunday roast") with results showing matching menu items and their restaurants.

**Relates To**: BR-004 (User Adoption), UC-1

**Acceptance Criteria**:
- [ ] Given user searches "fish chips", when query executed, then menu items containing "fish" AND "chips" in name/description appear
- [ ] Given search query, when executed, then results ranked by relevance (exact name match > partial match > description match)
- [ ] Given user searches common misspelling (e.g., "spagetti"), when query executed, then suggest correct spelling ("Did you mean spaghetti?")
- [ ] Edge case: Search is case-insensitive and ignores common words ("a", "the", "with")
- [ ] Edge case: Search supports stemming ("roasted" matches "roast", "frying" matches "fried")

**Data Requirements**:
- **Inputs**: Search query string (3-100 characters)
- **Outputs**: List of matching menu items with restaurant name, price, dietary tags
- **Validations**: Sanitize input to prevent SQL injection

**Priority**: **MUST_HAVE**

**Complexity**: **MEDIUM** (full-text search indexing)

**Dependencies**: DR-002 (menu items table), database full-text search configuration (PostgreSQL tsvector/tsquery)

**Assumptions**: PostgreSQL full-text search sufficient (no need for Elasticsearch initially)

**Architecture Principle Alignment**: Principle 12 (Performance Targets): Full-text search must return results <500ms

---

#### FR-009: Filter by Cuisine Type

**Description**: User can filter restaurants by cuisine type (British, Italian, Chinese, Indian, Thai, Mediterranean, Japanese, Mexican, etc.) with multi-select OR logic.

**Relates To**: BR-004 (User Adoption), BR-006 (Coverage)

**Acceptance Criteria**:
- [ ] Given user selects "Italian" checkbox, when search executed, then only Italian restaurants appear
- [ ] Given user selects "Italian" AND "Chinese", when search executed, then restaurants matching EITHER cuisine appear (OR logic)
- [ ] Given restaurant has cuisine_type=NULL, when any cuisine filter applied, then restaurant excluded from results
- [ ] Edge case: Cuisine types are normalized ("Italian" not "italian" or "ITALIAN")
- [ ] Edge case: If restaurant serves multiple cuisines (fusion), tagged with primary cuisine only initially (multi-cuisine tagging is Phase 2)

**Data Requirements**:
- **Inputs**: List of selected cuisine types (1-5 selections)
- **Outputs**: Filtered list of restaurants
- **Validations**: Cuisine types must match controlled vocabulary (no free-text)

**Priority**: **SHOULD_HAVE** (important for discovery, not critical to MVP)

**Complexity**: **LOW**

**Dependencies**: DR-001 (restaurant table with cuisine_type field), FR-012 (cuisine extraction/inference)

**Assumptions**: Cuisine type inferred from restaurant name, website metadata, or menu items (e.g., "Bella Italia" → Italian)

---

#### FR-010: Export Search Results to CSV

**Description**: User can export current search results or full restaurant/menu dataset to CSV file for external analysis in Excel, Google Sheets, or other tools.

**Relates To**: BR-004 (User Adoption), UC-2, Stakeholder SD-4 (Analyst Data Access), SD-7 (Journalist Data Export)

**Acceptance Criteria**:
- [ ] Given user clicks "Export to CSV" button, when clicked, then CSV file downloads to browser with filename "plymouth-menus-{date}.csv"
- [ ] Given export includes menu items, when CSV generated, then columns: restaurant_name, menu_item_name, price_gbp, category, dietary_tags, cuisine_type, last_updated, source_url
- [ ] Given CSV file, when opened in Excel, then all fields display correctly (UTF-8 encoding, quoted fields, no formatting issues)
- [ ] Given large result set (>10,000 rows), when export requested, then user prompted "Large export (X rows). Confirm download?" to prevent accidental huge files
- [ ] Edge case: CSV includes metadata header row: "# Exported from Plymouth Research - https://plymouthresearch.uk - {date}"

**Data Requirements**:
- **Inputs**: Current search results or full dataset flag
- **Outputs**: CSV file (RFC 4180 compliant, UTF-8 encoding)
- **Validations**: Escape special characters in menu item names/descriptions to prevent CSV injection attacks

**Priority**: **MUST_HAVE** (key feature for analysts/journalists)

**Complexity**: **LOW**

**Dependencies**: FR-001-009 (search functionality), DR-009 (CSV generation logic)

**Assumptions**: Browser-based CSV download sufficient (no need for email delivery or API endpoint initially)

**Architecture Principle Alignment**: Principle 11 (Standard Data Formats): CSV must be RFC 4180 compliant for interoperability

---

#### FR-011: Automated Web Scraping with Robots.txt Compliance

**Description**: Automated scraper crawls restaurant websites to extract menu HTML, respecting robots.txt directives, with 5-second rate limiting between requests to same domain.

**Relates To**: BR-002 (Legal Compliance), BR-006 (Coverage), Goal G-3 (100% Ethical Compliance)

**Acceptance Criteria**:
- [ ] Given restaurant website URL, when scraper runs, then robots.txt fetched and parsed BEFORE any page requests
- [ ] Given robots.txt contains "Disallow: /menu", when scraper runs, then /menu page NOT scraped and logged as "Blocked by robots.txt"
- [ ] Given scraper requests page from domain, when request completes, then 5-second delay enforced before next request to SAME domain
- [ ] Given scraper requests page, when HTTP request sent, then User-Agent header identifies "Plymouth Research Menu Scraper - contact@plymouthresearch.uk"
- [ ] Edge case: If robots.txt fetch fails (404, timeout), assume scraping is ALLOWED (permissive fallback per robots.txt spec)
- [ ] Edge case: If website requires JavaScript rendering, use Selenium/Playwright (slower, only for sites that need it)

**Data Requirements**:
- **Inputs**: Restaurant website URL
- **Outputs**: Raw HTML content of menu page
- **Validations**:
  - URL must be valid HTTP/HTTPS
  - Robots.txt compliance verified before each domain crawl
  - Rate limiting enforced at infrastructure layer (not just code-level, to prevent bypass)

**Priority**: **MUST_HAVE** (core data collection mechanism)

**Complexity**: **HIGH** (diverse website structures, robots.txt parsing, rate limiting, error handling)

**Dependencies**: DR-001 (restaurant table with source_url), NFR-C-001 (robots.txt compliance requirement)

**Assumptions**:
- Python libraries (BeautifulSoup, Scrapy, Selenium) sufficient for scraping
- ~10% of websites require Selenium for JavaScript rendering (most are static HTML)

**Architecture Principle Alignment**:
- Principle 3 (Ethical Web Scraping): Robots.txt and rate limiting are NON-NEGOTIABLE
- Principle 15 (Infrastructure as Code): Scraper logic version-controlled, reproducible

---

#### FR-012: Extract Cuisine Type from Website

**Description**: Automatically infer restaurant cuisine type (British, Italian, Chinese, etc.) from website metadata, restaurant name, or menu items.

**Relates To**: BR-001 (Data Quality), FR-009 (Cuisine Filter)

**Acceptance Criteria**:
- [ ] Given restaurant name contains "Bella Italia", when cuisine inferred, then tagged as "Italian"
- [ ] Given website metadata includes "cuisine: Chinese", when extracted, then tagged as "Chinese"
- [ ] Given menu contains predominantly pasta/pizza items, when analyzed, then inferred as "Italian"
- [ ] Given cuisine cannot be confidently inferred, when extraction completes, then tagged as "Mixed/International" or NULL (manual review queue)
- [ ] Edge case: If restaurant serves fusion cuisine, tag with primary cuisine only (secondary tags in Phase 2)

**Data Requirements**:
- **Inputs**: Restaurant name, website HTML/metadata, menu item names
- **Outputs**: Cuisine type (string from controlled vocabulary)
- **Validations**: Cuisine type must match predefined list (British, Italian, Chinese, Indian, Thai, Japanese, Mexican, Mediterranean, French, American, Vietnamese, Korean, Greek, Turkish, Spanish, Mixed/International)

**Priority**: **SHOULD_HAVE** (important for filtering, not critical to MVP)

**Complexity**: **MEDIUM** (inference logic, handling ambiguous cases)

**Dependencies**: FR-011 (web scraping), DR-001 (restaurant table with cuisine_type field)

**Assumptions**: Keyword-based inference achieves >80% accuracy (validated in pilot), with manual review for ambiguous cases

---

#### FR-013: Weekly Automated Refresh of All Menus

**Description**: Scraper runs weekly automated refresh cycle to update menu data for all 150+ restaurants, replacing stale data with fresh extractions.

**Relates To**: BR-003 (Operational Sustainability), BR-006 (Coverage), Goal G-2 (150+ Restaurants)

**Acceptance Criteria**:
- [ ] Given automated scheduler (cron job), when weekly trigger fires, then scraper executes for all restaurants in database
- [ ] Given scraper runs, when completed, then >90% of restaurants successfully refreshed (scraping success rate)
- [ ] Given scraper encounters error (404, timeout, robots.txt block), when error occurs, then logged and retried next cycle (no manual intervention required)
- [ ] Given menu data unchanged from last scrape, when refresh completes, then last_updated timestamp still updated (indicates freshness check occurred)
- [ ] Edge case: If restaurant website permanently offline (multiple consecutive failures), flag for manual review after 3 failures

**Data Requirements**:
- **Inputs**: List of all restaurant URLs in database
- **Outputs**: Updated menu data, scraping logs (success/failure per restaurant)
- **Validations**: Scrape cycle must complete within 24 hours (150 restaurants × 5-second delay = 12.5 minutes minimum, budget 1-2 hours for errors/retries)

**Priority**: **MUST_HAVE** (data freshness requirement)

**Complexity**: **MEDIUM** (scheduling, error handling, parallelization)

**Dependencies**: FR-011 (web scraping), NFR-P-003 (scrape cycle performance)

**Assumptions**:
- Weekly refresh balances freshness vs. respectful scraping (daily would burden restaurant servers)
- Cron job or managed task scheduler (AWS EventBridge, Heroku Scheduler) sufficient

**Architecture Principle Alignment**:
- Principle 3 (Ethical Scraping): Weekly frequency is respectful to restaurant websites
- Principle 17 (CI/CD): Automated deployment of scraper updates

---

#### FR-014: Data Quality Monitoring Dashboard

**Description**: Internal monitoring dashboard displays data quality metrics (completeness %, accuracy %, scraping success rate, data freshness) with automated alerts when quality degrades below thresholds.

**Relates To**: BR-001 (Data Quality), BR-003 (Operational Sustainability), Goal G-1 (95% Accuracy)

**Acceptance Criteria**:
- [ ] Given monitoring dashboard, when accessed by Data Engineer, then displays: completeness % (non-null required fields), accuracy % (manual validation results), scraping success rate %, avg data age
- [ ] Given data quality drops below 90%, when threshold breached, then automated alert sent to Data Engineer (email or Slack)
- [ ] Given scraping success rate <85%, when threshold breached, then alert sent (indicates widespread scraping failures)
- [ ] Given restaurant not refreshed in >10 days, when staleness detected, then flagged in dashboard for investigation
- [ ] Edge case: Dashboard auto-refreshes every 5 minutes (real-time-ish monitoring)

**Data Requirements**:
- **Inputs**: Database metrics queries (aggregations over menu items, restaurants)
- **Outputs**: Metrics dashboard (web-based, internal access only)
- **Validations**: Metrics must be calculated correctly (e.g., completeness = COUNT(non-null) / COUNT(total))

**Priority**: **MUST_HAVE** (operational requirement)

**Complexity**: **MEDIUM** (metrics calculation, alerting integration)

**Dependencies**: NFR-P-005 (monitoring infrastructure), DR-006 (data quality tracking)

**Assumptions**:
- Grafana or Streamlit sufficient for dashboard (no need for custom dashboard framework)
- Email or Slack webhooks sufficient for alerting (no need for PagerDuty initially)

**Architecture Principle Alignment**: Principle 18 (Logging & Monitoring): Observability is mandatory for operational excellence

---

#### FR-015: Restaurant Opt-Out Form

**Description**: Public-facing web form allows restaurant owners to request removal from platform, with automated email confirmation and 48-hour processing SLA.

**Relates To**: BR-002 (Legal Compliance), UC-3, Goal G-3 (Ethical Compliance), Stakeholder SD-6 (Restaurant Control)

**Acceptance Criteria**:
- [ ] Given opt-out form accessible from footer/FAQ, when restaurant owner loads form, then fields displayed: restaurant_name, website_url, contact_email, reason (optional)
- [ ] Given owner submits valid form, when submitted, then automated email sent: "We received your opt-out request. Your restaurant will be removed within 48 hours."
- [ ] Given opt-out request received, when Operations/IT reviews, then validates legitimacy (email domain matches restaurant, not spam)
- [ ] Given validated opt-out, when processed, then restaurant removed from database and added to permanent exclusion list
- [ ] Given opt-out processed, when complete, then confirmation email sent: "Your restaurant has been removed from Plymouth Research platform."
- [ ] Edge case: If request appears fraudulent (email doesn't match restaurant domain), manually contact restaurant to verify before processing

**Data Requirements**:
- **Inputs**: Restaurant name, website URL, contact email, reason (optional text)
- **Outputs**: Opt-out request record, automated emails, database deletion, exclusion list entry
- **Validations**:
  - Email must be valid format
  - Website URL must match restaurant in database (fuzzy match if needed)
  - Rate limiting on form submission (max 5 per hour from same IP - prevent spam)

**Priority**: **MUST_HAVE** (legal/ethical requirement)

**Complexity**: **LOW** (simple form, email automation)

**Dependencies**: DR-008 (opt-out exclusion list), NFR-C-002 (opt-out SLA requirement)

**Assumptions**:
- <5% of restaurants opt out (based on stakeholder assumption)
- Manual verification acceptable for fraud prevention (low volume expected)

**Architecture Principle Alignment**: Principle 3 (Ethical Scraping): Opt-out mechanism is mandatory compliance requirement

---

## Non-Functional Requirements (NFRs)

### Performance Requirements

#### NFR-P-001: Dashboard Search Response Time

**Requirement**: Dashboard search queries must return results within 500ms (95th percentile) to provide "instant" user experience.

**Measurement**:
- **Metric**: p95 response time (95% of queries return in <500ms)
- **Measurement Method**: Application Performance Monitoring (APM) instrumentation on search API endpoint
- **Target**: <500ms (p95), <200ms (p50), <1000ms (p99)

**Rationale**: Supports stakeholder goal G-4 (Performance <500ms) and Outcome O-3 (Operational Sustainability). Users expect instant search results competitive with Google/TripAdvisor. Slow queries frustrate users and reduce adoption.

**Acceptance Criteria**:
- [ ] Load testing demonstrates p95 response time <500ms with 1,000 menu items
- [ ] Load testing demonstrates p95 response time <500ms with 10,000 menu items (future growth)
- [ ] Dashboard includes performance monitoring displaying real-time p95 latency

**Implementation Guidance**:
- Database indexing on restaurant_name, menu_item_name, cuisine_type, dietary_tags
- Caching layer for popular queries (e.g., Redis or in-memory cache)
- Query optimization (EXPLAIN ANALYZE on all queries)

**Priority**: **MUST_HAVE**

**Stakeholder**: Plymouth Consumers (SD-5), Research Analysts (SD-4), Food Writers (SD-7)

**Traces To**: Goal G-4 → Outcome O-3

**Architecture Principle Alignment**: Principle 12 (Performance Targets): Sub-500ms searches essential for user satisfaction

---

#### NFR-P-002: Dashboard Page Load Time

**Requirement**: Dashboard homepage must load within 2 seconds (95th percentile) on standard broadband connection (10 Mbps).

**Measurement**:
- **Metric**: p95 page load time (Time to Interactive - TTI)
- **Measurement Method**: Lighthouse audits, Real User Monitoring (RUM) if implemented
- **Target**: <2000ms (p95), <1000ms (p50)

**Rationale**: First impression matters. Slow page load drives users away before they even search. Supports Outcome O-4 (User Satisfaction).

**Acceptance Criteria**:
- [ ] Lighthouse audit scores >90 for Performance
- [ ] Homepage loads <2s on simulated 3G connection (worst-case test)
- [ ] All assets (CSS, JS, images) optimized and minified

**Implementation Guidance**:
- Minimize JavaScript bundle size (code splitting if using React/Vue)
- Compress images and use responsive formats (WebP)
- CDN for static assets if budget allows (or use managed hosting with edge caching)
- Lazy loading for below-fold content

**Priority**: **SHOULD_HAVE** (important for adoption, not critical to MVP)

**Stakeholder**: Plymouth Consumers (SD-5)

**Traces To**: Goal G-4 → Outcome O-4

---

#### NFR-P-003: Scraping Cycle Completion Time

**Requirement**: Weekly scraping cycle must complete within 24 hours for 150 restaurants, with parallelization to reduce total time.

**Measurement**:
- **Metric**: Total elapsed time from scrape job start to completion
- **Measurement Method**: Scraper logs with start/end timestamps
- **Target**: <24 hours (preferably <4 hours with parallelization)

**Rationale**: Weekly refresh must not drift into multi-day cycles. Faster cycles enable on-demand refresh features in Phase 2. Supports Goal G-2 (150+ Restaurants) and Outcome O-3 (Sustainability).

**Acceptance Criteria**:
- [ ] Scraper completes 150 restaurants in <24 hours with serial execution (baseline)
- [ ] Scraper completes 150 restaurants in <4 hours with 5-10 parallel workers (optimized)
- [ ] No rate-limiting violations during parallel execution (5-second delays still enforced per domain)

**Implementation Guidance**:
- Celery or Python multiprocessing for parallelization
- Distributed task queue (Redis backend) for worker coordination
- Per-domain rate limiting (not global) to allow parallel scraping of different domains

**Priority**: **MUST_HAVE**

**Stakeholder**: Data Engineer (SD-3), Operations/IT (SD-10)

**Traces To**: Goal G-2 → Outcome O-3

**Architecture Principle Alignment**: Principle 5 (Scalability): Parallel scraping enables growth to 1,000+ restaurants in Phase 2

---

#### NFR-P-004: Database Query Performance

**Requirement**: Database queries must execute within 100ms (average) for single-table queries and 200ms for complex joins.

**Measurement**:
- **Metric**: Average query execution time from database logs or APM
- **Measurement Method**: PostgreSQL slow query log, pg_stat_statements
- **Target**: <100ms (avg) for single-table, <200ms for joins

**Rationale**: Database is bottleneck for search performance. Slow queries cascade to slow API and dashboard. Supports NFR-P-001.

**Acceptance Criteria**:
- [ ] All frequent queries (search, restaurant detail) execute <100ms in production database
- [ ] No N+1 query anti-patterns (validated via APM)
- [ ] Database query plan analysis (EXPLAIN) shows index usage for all queries

**Implementation Guidance**:
- B-tree indexes on: restaurant_name, cuisine_type, menu_item_name, dietary_tags
- GIN indexes for full-text search (tsvector columns)
- Avoid SELECT * (only fetch needed columns)
- Connection pooling (PgBouncer or application-level pool)

**Priority**: **MUST_HAVE**

**Stakeholder**: Data Engineer (SD-3)

**Traces To**: Goal G-4 → Outcome O-3

---

#### NFR-P-005: Monitoring and Alerting Response Time

**Requirement**: Monitoring system must detect critical issues (dashboard down, data quality <90%, scraping failures >15%) within 5 minutes and alert Operations/IT within 10 minutes.

**Measurement**:
- **Metric**: Time from issue occurrence to alert delivery
- **Measurement Method**: Test alerts with simulated failures
- **Target**: Detection <5 minutes, alert delivery <10 minutes

**Rationale**: Fast incident detection minimizes user impact and data quality degradation. Supports Outcome O-3 (Operational Sustainability).

**Acceptance Criteria**:
- [ ] Health check endpoint (/health) returns 200 OK when dashboard operational, 500 when down
- [ ] Uptime monitoring (UptimeRobot or equivalent) checks /health every 1 minute
- [ ] Alert fired within 10 minutes of dashboard downtime
- [ ] Alert fired within 10 minutes of data quality drop below 90%

**Implementation Guidance**:
- UptimeRobot free tier (50 monitors, 5-minute checks) or self-hosted monitoring
- Email or Slack webhooks for alerts
- Health check endpoint includes database connectivity test

**Priority**: **MUST_HAVE**

**Stakeholder**: Operations/IT (SD-10), Data Engineer (SD-3)

**Traces To**: Goal G-5 (Cost <£100), Goal G-1 (Data Quality 95%) → Outcome O-3

**Architecture Principle Alignment**: Principle 18 (Logging & Monitoring): Observability mandatory for operational excellence

---

### Security Requirements

#### NFR-SEC-001: Data Encryption in Transit

**Requirement**: All data transmitted between user browser and dashboard, and between dashboard and database, must be encrypted using TLS 1.2 or higher.

**Rationale**: Protects menu data (though public) and user queries from eavesdropping. Supports Principle 4 (Privacy by Design) and industry best practice.

**Acceptance Criteria**:
- [ ] Dashboard served over HTTPS with valid TLS certificate (Let's Encrypt or equivalent)
- [ ] HTTP traffic redirected to HTTPS (301 redirect)
- [ ] Database connections use SSL/TLS (PostgreSQL sslmode=require)
- [ ] TLS certificate auto-renewal configured (Let's Encrypt cron job)

**Implementation Guidance**:
- Let's Encrypt free TLS certificates with Certbot auto-renewal
- Nginx or managed hosting (Heroku, Render) handles HTTPS termination
- PostgreSQL sslmode=require in connection string

**Priority**: **MUST_HAVE**

**Stakeholder**: Legal/Compliance Advisor (SD-8), ICO (SD-9)

**Traces To**: Goal G-8 (DPIA Completion) → Outcome O-2

**Architecture Principle Alignment**: Principle 4 (Privacy by Design): Encryption everywhere

---

#### NFR-SEC-002: Data Encryption at Rest

**Requirement**: All database storage (menu data, restaurant info, scraping logs) must be encrypted at rest using AES-256 or equivalent.

**Rationale**: Though menu data is public, encryption at rest is GDPR best practice and protects against physical theft or unauthorized access. Supports Principle 4 (Privacy by Design).

**Acceptance Criteria**:
- [ ] PostgreSQL data directory encrypted (native encryption or encrypted volume)
- [ ] Backups encrypted before storage (pgBackRest encryption or equivalent)
- [ ] Encryption keys managed securely (not in application code or version control)

**Implementation Guidance**:
- Managed database services (AWS RDS, DigitalOcean Managed Postgres) provide encryption at rest by default
- Self-hosted: LUKS encrypted volume or PostgreSQL pgcrypto extension
- Backup encryption: pgBackRest --cipher-type=aes-256-cbc

**Priority**: **SHOULD_HAVE** (best practice, not strictly required for public data)

**Stakeholder**: Legal/Compliance Advisor (SD-8), ICO (SD-9)

**Traces To**: Goal G-8 (DPIA) → Outcome O-2

---

#### NFR-SEC-003: SQL Injection Prevention

**Requirement**: All user inputs (search queries, filters) must be sanitized using parameterized queries or ORM to prevent SQL injection attacks.

**Rationale**: SQL injection could allow attackers to read, modify, or delete database contents. Critical security vulnerability. Supports industry best practice and OWASP Top 10.

**Acceptance Criteria**:
- [ ] All database queries use parameterized queries (no string concatenation)
- [ ] ORM (SQLAlchemy, Django ORM) used for all database access if applicable
- [ ] Security testing (manual or automated) confirms no SQL injection vulnerabilities
- [ ] Code review checklist includes SQL injection check

**Implementation Guidance**:
- Use SQLAlchemy with bound parameters: `query.filter(Restaurant.name == :name)`
- Never use f-strings or string concatenation for SQL: `f"SELECT * FROM restaurants WHERE name = '{user_input}'"` ← DANGEROUS
- Input validation: reject queries with suspicious characters (SQL keywords like DROP, SELECT in unexpected contexts)

**Priority**: **MUST_HAVE** (critical security requirement)

**Stakeholder**: Data Engineer (SD-3), Legal/Compliance Advisor (SD-8)

**Traces To**: Outcome O-2 (Zero Legal Violations - data breach would trigger ICO investigation)

**Architecture Principle Alignment**: Principle 4 (Privacy by Design): Security controls mandatory

---

#### NFR-SEC-004: Secrets Management

**Requirement**: Database credentials, API keys, and other secrets must NOT be stored in code or version control. Must use environment variables or secrets management service.

**Rationale**: Hardcoded credentials in code risk exposure via Git history, public repos, or code leaks. Industry best practice (OWASP, NIST).

**Acceptance Criteria**:
- [ ] Database password stored in environment variable or .env file (excluded from Git via .gitignore)
- [ ] No credentials in code files or configuration files committed to Git
- [ ] Git history reviewed for accidentally committed secrets (use git-secrets or similar tool)
- [ ] Secrets rotation process documented (how to change database password without downtime)

**Implementation Guidance**:
- Use python-dotenv to load .env file with credentials
- .gitignore includes: .env, secrets.yml, credentials.json
- Production: use managed secrets (AWS Secrets Manager, Heroku config vars)
- Rotate database password every 90 days (Phase 2 automation)

**Priority**: **MUST_HAVE**

**Stakeholder**: Data Engineer (SD-3), Operations/IT (SD-10)

**Traces To**: Outcome O-2 (avoid security incidents)

**Architecture Principle Alignment**: Principle 4 (Privacy by Design): Secrets management mandatory

---

### Scalability Requirements

#### NFR-S-001: Support 10X Data Growth

**Requirement**: System architecture must support growth from 150 restaurants / 10,000 menu items to 1,500 restaurants / 100,000 menu items without major architectural changes.

**Rationale**: Supports Research Director's expansion vision (SD-1) and Principle 5 (Scalability). Platform may expand to other UK cities or add food delivery platform data.

**Acceptance Criteria**:
- [ ] Database schema supports sharding or partitioning (if needed at 100K+ items)
- [ ] Scraper can parallelize to 50+ concurrent workers (from 5-10 initial)
- [ ] Dashboard search performance <500ms maintained with 100K items (via indexing)
- [ ] No hard-coded limits in code (e.g., max_restaurants = 150)

**Implementation Guidance**:
- Database indexing strategy scales logarithmically (B-tree, GIN indexes)
- Horizontal scaling: add more scraper workers as restaurant count grows
- Stateless dashboard (can add more application servers if needed)
- Caching layer (Redis) for high-traffic queries

**Priority**: **SHOULD_HAVE** (future-proofing, not critical to MVP)

**Stakeholder**: Research Director (SD-1), Data Engineer (SD-3)

**Traces To**: Goal G-5 (Scalability) → Outcome O-3

**Architecture Principle Alignment**: Principle 5 (Scalability and Extensibility): Design for 10X growth

---

#### NFR-S-002: Horizontal Scaling for Scraper

**Requirement**: Scraper must support horizontal scaling by adding more worker processes without code changes, coordinated via distributed task queue.

**Rationale**: Enables faster scraping cycles and supports 10X growth to 1,500 restaurants. Supports Principle 5 (Scalability).

**Acceptance Criteria**:
- [ ] Scraper uses distributed task queue (Celery with Redis backend or equivalent)
- [ ] Adding workers (e.g., 5 workers → 20 workers) requires only infrastructure change, not code change
- [ ] Workers coordinate to avoid duplicate scraping (restaurant URL claimed by one worker at a time)
- [ ] Rate limiting still enforced across all workers (global per-domain rate limiter)

**Implementation Guidance**:
- Celery with Redis broker for task distribution
- Redis-based rate limiter (per-domain locks with TTL)
- Docker containers for workers (easy to scale in cloud environments)

**Priority**: **SHOULD_HAVE** (important for Phase 2 expansion)

**Stakeholder**: Data Engineer (SD-3), Operations/IT (SD-10)

**Traces To**: Goal G-2 (150+ Restaurants initially, 1,500+ future)

---

### Availability & Reliability Requirements

#### NFR-A-001: Dashboard Uptime SLA

**Requirement**: Dashboard must maintain 99% uptime (7.2 hours downtime per month acceptable) measured monthly.

**Rationale**: Supports stakeholder goal G-13 (Reliability) and Outcome O-3 (Sustainability). 99% balances reliability with acceptable maintenance windows for small team.

**Acceptance Criteria**:
- [ ] Uptime monitoring reports ≥99% availability over each calendar month
- [ ] Planned maintenance scheduled during low-traffic windows (announced 24 hours in advance)
- [ ] Unplanned downtime incidents documented with root cause analysis

**Measurement**:
- **Metric**: Uptime % = (Total minutes in month - Downtime minutes) / Total minutes × 100
- **Measurement Method**: UptimeRobot or equivalent 1-minute ping interval
- **Target**: ≥99.0% (438 minutes downtime/month max)

**Implementation Guidance**:
- Managed hosting with SLA guarantees (Heroku, Render, DigitalOcean App Platform)
- Health check endpoint monitored every 1 minute
- Database backups for rapid restore (RTO <1 hour)

**Priority**: **MUST_HAVE**

**Stakeholder**: Plymouth Consumers (SD-5), Research Director (SD-1)

**Traces To**: Goal G-13 (Reliability) → Outcome O-3

**Architecture Principle Alignment**: Principle 13 (Reliability and Availability): 99% uptime target

---

#### NFR-A-002: Graceful Degradation

**Requirement**: If database unavailable, dashboard must display cached data with staleness warning rather than complete failure (500 error).

**Rationale**: Supports Principle 13 (Reliability - graceful degradation). Better to show stale data with warning than no data at all.

**Acceptance Criteria**:
- [ ] If database connection fails, dashboard shows cached data (last successful query results) with banner: "Database temporarily unavailable. Displaying cached data from [timestamp]."
- [ ] If cache unavailable, display user-friendly error: "Dashboard temporarily unavailable. Please try again in a few minutes." (not 500 Internal Server Error)
- [ ] Database connection retries with exponential backoff (3 retries over 30 seconds)

**Implementation Guidance**:
- Redis cache layer for popular queries
- Application-level exception handling for database errors
- Fallback to cached data if database unreachable

**Priority**: **SHOULD_HAVE** (improves user experience, not critical)

**Stakeholder**: Plymouth Consumers (SD-5), Operations/IT (SD-10)

**Traces To**: Outcome O-3 (Sustainability)

---

#### NFR-A-003: Backup and Recovery

**Requirement**: Database must be backed up daily with ability to restore within 1 hour (RTO) and maximum 24 hours data loss (RPO).

**Rationale**: Protects against data loss from hardware failure, human error, or corruption. Supports Outcome O-3 (Sustainability).

**Acceptance Criteria**:
- [ ] Automated daily backups of full database
- [ ] Backups retained for 7 days (rolling window)
- [ ] Restore tested quarterly (verify backups are valid)
- [ ] Recovery Time Objective (RTO): <1 hour from backup
- [ ] Recovery Point Objective (RPO): <24 hours (acceptable data loss)

**Implementation Guidance**:
- Managed database backups (AWS RDS automated backups, DigitalOcean Managed Postgres)
- Self-hosted: pg_dump cron job to S3 or local storage
- Document restore procedure in runbook

**Priority**: **MUST_HAVE**

**Stakeholder**: Operations/IT (SD-10), Data Engineer (SD-3)

**Traces To**: Outcome O-3 (Sustainability)

**Architecture Principle Alignment**: Principle 13 (Reliability): Backup/restore mandatory

---

### Compliance Requirements

#### NFR-C-001: Robots.txt Compliance

**Requirement**: Scraper must fetch and parse robots.txt for each domain before scraping, respecting all "Disallow" directives. 100% compliance mandatory (zero violations).

**Rationale**: Supports Goal G-3 (100% Ethical Compliance) and Outcome O-2 (Zero Legal Violations). Violating robots.txt creates legal risk under Computer Misuse Act 1990 (UK).

**Acceptance Criteria**:
- [ ] Scraper fetches robots.txt before first request to any domain
- [ ] If robots.txt contains "Disallow: /menu", scraper does NOT request /menu and logs: "Blocked by robots.txt"
- [ ] Robots.txt compliance logged for audit trail (100% compliance verifiable)
- [ ] Monthly audit samples 50 scraping logs to verify no violations

**Measurement**:
- **Metric**: Robots.txt Compliance % = (Compliant requests / Total requests) × 100
- **Target**: 100.0% (zero violations)
- **Measurement Method**: Scraper logs, monthly audit by Legal Advisor

**Implementation Guidance**:
- Python robotparser library or Scrapy's built-in robots.txt support
- Infrastructure-level enforcement (cannot be bypassed by code bugs)
- Whitelist-based approach: only scrape if robots.txt allows (fail-safe)

**Priority**: **MUST_HAVE** (non-negotiable)

**Stakeholder**: Legal/Compliance Advisor (SD-8), Research Director (SD-2)

**Traces To**: Goal G-3 → Outcome O-2

**Architecture Principle Alignment**: Principle 3 (Ethical Web Scraping): NON-NEGOTIABLE compliance

---

#### NFR-C-002: Rate Limiting Compliance

**Requirement**: Scraper must enforce minimum 5-second delay between requests to same domain. 100% compliance mandatory.

**Rationale**: Supports Goal G-3 (Ethical Compliance) and Outcome O-2 (Legal). Respectful scraping avoids overloading restaurant servers and prevents complaints.

**Acceptance Criteria**:
- [ ] Every request to domain A followed by ≥5-second delay before next request to domain A
- [ ] Requests to domain B can occur concurrently (rate limit is per-domain, not global)
- [ ] Rate limiting enforced at infrastructure layer (Redis-based throttle or equivalent) - cannot be bypassed
- [ ] Monthly audit samples 50 scraping logs to verify 5+ second delays

**Measurement**:
- **Metric**: Rate Limiting Compliance % = (Compliant request pairs / Total request pairs) × 100
- **Target**: 100.0%
- **Measurement Method**: Scraper logs, calculate time delta between consecutive requests to same domain

**Implementation Guidance**:
- Redis-based rate limiter with per-domain keys and TTL
- Scraper sleeps 5 seconds after each request (simple approach)
- Distributed workers coordinate via Redis locks

**Priority**: **MUST_HAVE** (non-negotiable)

**Stakeholder**: Legal/Compliance Advisor (SD-8), Restaurant Owners (SD-6)

**Traces To**: Goal G-3 → Outcome O-2

**Architecture Principle Alignment**: Principle 3 (Ethical Scraping): Rate limiting mandatory

---

#### NFR-C-003: GDPR Compliance (UK)

**Requirement**: Platform must comply with UK GDPR including: no PII collection, data retention limits (12 months), data subject rights (opt-out), and DPIA completion.

**Rationale**: Supports Goal G-8 (DPIA Completion) and Outcome O-2 (Zero ICO Fines). UK GDPR compliance mandatory for UK organizations processing data.

**Acceptance Criteria**:
- [ ] DPIA completed and approved by Legal Advisor before launch
- [ ] No PII collected (no customer reviews, personal contact info, user accounts)
- [ ] Only public business data scraped (restaurant names, addresses, menus)
- [ ] Historical menu data deleted after 12 months (automated retention policy)
- [ ] Opt-out mechanism functional and tested
- [ ] Privacy policy published on website explaining data collection and use

**Measurement**:
- **Compliance Checklist**:
  - [x] DPIA completed
  - [x] No PII in database (automated scan confirms)
  - [x] Retention policy automated (cron job deletes data >12 months old)
  - [x] Opt-out form live and tested
  - [x] Privacy policy published

**Implementation Guidance**:
- DPIA template completed by Legal Advisor (Month 1)
- Automated PII detection (regex scan for emails, phone numbers, names in scraped data → flag for review)
- PostgreSQL cron job: DELETE FROM menu_items WHERE scraped_at < NOW() - INTERVAL '12 months'
- Privacy policy generated from template (cookiecutter or manual)

**Priority**: **MUST_HAVE** (legal requirement)

**Stakeholder**: Legal/Compliance Advisor (SD-8), ICO (SD-9), Research Director (SD-2)

**Traces To**: Goal G-8 (DPIA) → Outcome O-2

**Architecture Principle Alignment**: Principle 4 (Privacy by Design): UK GDPR compliance mandatory

---

#### NFR-C-004: User-Agent Transparency

**Requirement**: All HTTP requests from scraper must include User-Agent header identifying "Plymouth Research Menu Scraper" with contact email for website owners to reach us.

**Rationale**: Supports Goal G-3 (Ethical Compliance). Transparent identification enables restaurants to contact us if they have concerns, reducing risk of complaints.

**Acceptance Criteria**:
- [ ] User-Agent header set to: "Plymouth Research Menu Scraper (https://plymouthresearch.uk) - contact@plymouthresearch.uk"
- [ ] 100% of scraping requests include this User-Agent (logged and auditable)
- [ ] Contact email monitored daily for restaurant inquiries

**Implementation Guidance**:
- Python requests library: `headers = {'User-Agent': 'Plymouth Research Menu Scraper...'}`
- Scrapy: USER_AGENT setting in settings.py
- Log User-Agent in scraper logs for audit

**Priority**: **MUST_HAVE**

**Stakeholder**: Legal/Compliance Advisor (SD-8), Restaurant Owners (SD-6)

**Traces To**: Goal G-3 → Outcome O-2

**Architecture Principle Alignment**: Principle 3 (Ethical Scraping): Transparency mandatory

---

#### NFR-C-005: Opt-Out Processing SLA

**Requirement**: Restaurant opt-out requests must be processed within 48 hours of submission, with confirmation emails sent at receipt and completion.

**Rationale**: Supports Goal G-3 (Ethical Compliance) and UC-3 (Opt-Out Use Case). Timely opt-out processing demonstrates respect for restaurant preferences and reduces complaints.

**Acceptance Criteria**:
- [ ] Opt-out form submission triggers automated "received" email within 1 minute
- [ ] Operations/IT reviews and processes opt-out within 48 hours
- [ ] Completion email sent after restaurant removed: "Your restaurant has been removed."
- [ ] 100% of opt-out requests processed within 48-hour SLA (tracked in ticketing system or spreadsheet)

**Measurement**:
- **Metric**: Opt-Out SLA Compliance % = (Requests processed <48hrs / Total requests) × 100
- **Target**: 100%
- **Measurement Method**: Opt-out request log with timestamps

**Implementation Guidance**:
- Automated email via SendGrid, Mailgun, or SMTP
- Simple ticketing system or Google Sheet to track opt-out requests and processing time
- Runbook for Operations/IT: how to remove restaurant and add to exclusion list

**Priority**: **MUST_HAVE**

**Stakeholder**: Restaurant Owners (SD-6), Legal/Compliance Advisor (SD-8)

**Traces To**: Goal G-3 → Outcome O-2

---

### Usability Requirements

#### NFR-U-001: Mobile-Responsive Dashboard

**Requirement**: Dashboard must be fully functional and usable on mobile devices (smartphones, tablets) with responsive design adapting to screen sizes 320px-1920px.

**Rationale**: Many consumers search for restaurants on mobile. Mobile-first design expected by users. Supports Outcome O-4 (User Satisfaction).

**Acceptance Criteria**:
- [ ] Dashboard displays correctly on mobile (iPhone, Android), tablet (iPad), and desktop
- [ ] Search bar, filters, and results usable on touch screens (no tiny buttons)
- [ ] Lighthouse audit scores >90 for Mobile Usability
- [ ] No horizontal scrolling on mobile devices

**Implementation Guidance**:
- Responsive CSS framework (Bootstrap, Tailwind, or custom media queries)
- Mobile-first design approach (design for mobile, enhance for desktop)
- Touch-friendly UI (buttons ≥44px tap target)

**Priority**: **MUST_HAVE** (mobile traffic likely >50%)

**Stakeholder**: Plymouth Consumers (SD-5)

**Traces To**: Outcome O-4 (User Adoption)

---

#### NFR-U-002: Accessibility (WCAG 2.1 Level A)

**Requirement**: Dashboard must meet WCAG 2.1 Level A accessibility standards for users with disabilities (screen readers, keyboard navigation, color contrast).

**Rationale**: Ethical requirement (inclusivity) and potential legal requirement (UK Equality Act 2010). Supports public good mission.

**Acceptance Criteria**:
- [ ] Automated accessibility testing (axe, Lighthouse) shows zero critical violations
- [ ] Keyboard navigation works (Tab through all interactive elements, Enter to select)
- [ ] Color contrast ratios meet WCAG 2.1 Level A (4.5:1 for normal text, 3:1 for large text)
- [ ] Alt text provided for images (if any)
- [ ] Screen reader testing with NVDA or VoiceOver confirms usability

**Implementation Guidance**:
- Semantic HTML (<button>, <nav>, <main>, not <div onclick="">)
- ARIA labels where needed (aria-label, aria-describedby)
- Focus indicators visible for keyboard navigation
- Color contrast checking tool (WebAIM Contrast Checker)

**Priority**: **SHOULD_HAVE** (ethical requirement, not legally mandatory for private organization in UK, but strongly recommended)

**Stakeholder**: Plymouth Consumers (SD-5), Research Director (SD-1 - public good mission)

**Traces To**: Outcome O-4 (User Satisfaction)

---

## Data Requirements

### DR-001: Restaurant Entity

**Description**: Database must store restaurant entities with name, address, website URL, cuisine type, price range, and metadata (scraped_at, last_updated).

**Schema**:
```sql
CREATE TABLE restaurants (
    restaurant_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT,
    postcode VARCHAR(10),
    website_url TEXT NOT NULL UNIQUE,
    cuisine_type VARCHAR(50),  -- British, Italian, Chinese, etc.
    price_range VARCHAR(20),   -- Budget, Mid-Range, Premium
    avg_main_price NUMERIC(10,2),  -- Calculated from menu items
    latitude NUMERIC(9,6),     -- For future map features
    longitude NUMERIC(9,6),
    scraped_at TIMESTAMP NOT NULL,  -- First scrape timestamp
    last_updated TIMESTAMP NOT NULL,  -- Most recent scrape timestamp
    is_active BOOLEAN DEFAULT TRUE,  -- False if opted out or permanently offline
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_restaurants_name ON restaurants(name);
CREATE INDEX idx_restaurants_cuisine ON restaurants(cuisine_type);
CREATE INDEX idx_restaurants_postcode ON restaurants(postcode);
```

**Data Sources**:
- **Inputs**: Web scraping (restaurant websites), manual curation (initial list from Google Maps, TripAdvisor)
- **Outputs**: Dashboard restaurant list, search results

**Validation Rules**:
- `name` must not be empty
- `website_url` must be valid HTTP/HTTPS URL and unique
- `cuisine_type` must match controlled vocabulary or be NULL
- `price_range` must be "Budget", "Mid-Range", "Premium", or NULL
- `last_updated` must be ≤ NOW() (cannot be future date)

**Retention Policy**: Restaurant records retained indefinitely while active. If opted out (`is_active = FALSE`), retain for 30 days then soft-delete (for compliance audit trail).

**Priority**: **MUST_HAVE**

**Traces To**: FR-001 (Search by Name), FR-009 (Filter by Cuisine), BR-006 (150+ Coverage)

**Architecture Principle Alignment**: Principle 7 (Single Source of Truth): `restaurants` table is authoritative source for restaurant data

---

### DR-002: Menu Item Entity

**Description**: Database must store menu items with name, description, price, category, restaurant association, and dietary tags.

**Schema**:
```sql
CREATE TABLE menu_items (
    item_id SERIAL PRIMARY KEY,
    restaurant_id INTEGER NOT NULL REFERENCES restaurants(restaurant_id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price_gbp NUMERIC(10,2),  -- Normalized to decimal GBP
    category VARCHAR(50),  -- Starters, Mains, Desserts, Drinks, etc.
    scraped_at TIMESTAMP NOT NULL,
    last_updated TIMESTAMP NOT NULL,
    source_html TEXT,  -- Raw HTML snippet for debugging extraction issues
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_menu_items_restaurant ON menu_items(restaurant_id);
CREATE INDEX idx_menu_items_name ON menu_items(name);
CREATE INDEX idx_menu_items_category ON menu_items(category);
CREATE INDEX idx_menu_items_price ON menu_items(price_gbp);
```

**Data Sources**:
- **Inputs**: Web scraping extraction logic (HTML parsing)
- **Outputs**: Dashboard menu display, search results, CSV export

**Validation Rules**:
- `name` must not be empty
- `price_gbp` must be ≥0.50 and ≤150.00 (flag outliers for review)
- `category` must match controlled vocabulary (Starters, Mains, Desserts, Drinks, Sides, Specials, Other) or NULL
- `last_updated` must be ≥ `scraped_at` (updated timestamp never earlier than creation)

**Retention Policy**: Menu items older than 12 months deleted automatically (GDPR data minimization, per Principle 4). Exception: aggregated/anonymized historical data retained indefinitely for trend analysis.

**Priority**: **MUST_HAVE**

**Traces To**: FR-004 (View Full Menu), FR-006 (Price Normalization), FR-008 (Full-Text Search)

**Architecture Principle Alignment**: Principle 8 (Data Lineage): `source_html` field enables tracing back to original extraction

---

### DR-003: Category Reference Data

**Description**: Controlled vocabulary for menu item categories (Starters, Mains, Desserts, etc.) to enable consistent categorization and filtering.

**Schema**:
```sql
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL UNIQUE,
    display_order INTEGER,  -- Order in dropdown filters
    created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO categories (category_name, display_order) VALUES
    ('Starters', 1),
    ('Mains', 2),
    ('Desserts', 3),
    ('Drinks', 4),
    ('Sides', 5),
    ('Specials', 6),
    ('Other', 7);
```

**Data Sources**: Predefined controlled vocabulary (not user-generated)

**Validation Rules**: Category names must be unique, immutable (no updates to existing categories - add new ones if needed)

**Priority**: **SHOULD_HAVE** (improves UX, not critical to MVP)

**Traces To**: FR-004 (View Full Menu organized by category)

---

### DR-004: Dietary Tags Entity

**Description**: Many-to-many relationship between menu items and dietary tags (vegan, gluten-free, etc.) to enable dietary filtering.

**Schema**:
```sql
CREATE TABLE dietary_tags (
    tag_id SERIAL PRIMARY KEY,
    tag_name VARCHAR(50) NOT NULL UNIQUE,  -- vegan, vegetarian, gluten-free, dairy-free, nut-free
    created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO dietary_tags (tag_name) VALUES
    ('vegan'),
    ('vegetarian'),
    ('gluten-free'),
    ('dairy-free'),
    ('nut-free');

CREATE TABLE menu_item_dietary_tags (
    item_id INTEGER NOT NULL REFERENCES menu_items(item_id) ON DELETE CASCADE,
    tag_id INTEGER NOT NULL REFERENCES dietary_tags(tag_id) ON DELETE CASCADE,
    PRIMARY KEY (item_id, tag_id),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_menu_item_dietary_tags_item ON menu_item_dietary_tags(item_id);
CREATE INDEX idx_menu_item_dietary_tags_tag ON menu_item_dietary_tags(tag_id);
```

**Data Sources**:
- **Inputs**: Automated extraction from menu item name/description (keyword matching)
- **Outputs**: Dietary filter in dashboard, dietary badges on menu items

**Validation Rules**:
- Tag names must match controlled vocabulary (no free-text tags)
- Many-to-many: One item can have multiple tags (e.g., vegan AND gluten-free)

**Priority**: **MUST_HAVE** (core consumer value)

**Traces To**: FR-002 (Search by Dietary Tags), FR-007 (Extract Tags)

**Architecture Principle Alignment**: Principle 1 (Data Quality First): Conservative tagging (only tag if explicitly labeled) prevents dangerous errors

---

### DR-005: Scraping Logs

**Description**: Audit log of all scraping activity (URLs accessed, timestamps, success/failure, robots.txt compliance) for compliance verification and debugging.

**Schema**:
```sql
CREATE TABLE scraping_logs (
    log_id SERIAL PRIMARY KEY,
    restaurant_id INTEGER REFERENCES restaurants(restaurant_id) ON DELETE SET NULL,
    url TEXT NOT NULL,
    http_status_code INTEGER,  -- 200, 404, 500, etc.
    robots_txt_allowed BOOLEAN,  -- TRUE if robots.txt permitted, FALSE if blocked
    rate_limit_delay_seconds INTEGER,  -- Actual delay before this request (should be ≥5)
    user_agent TEXT,
    success BOOLEAN,  -- TRUE if menu data extracted, FALSE if failed
    error_message TEXT,  -- If failed, what went wrong
    scraped_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_scraping_logs_restaurant ON scraping_logs(restaurant_id);
CREATE INDEX idx_scraping_logs_scraped_at ON scraping_logs(scraped_at);
```

**Data Sources**: Scraper automatically logs every HTTP request

**Validation Rules**:
- `rate_limit_delay_seconds` should be ≥5 (audited monthly for compliance)
- `robots_txt_allowed` must be TRUE (if FALSE, request should not have been made - indicates violation)

**Retention Policy**: Scraping logs retained for 90 days (compliance audit trail), then deleted.

**Priority**: **MUST_HAVE** (compliance requirement)

**Traces To**: NFR-C-001 (Robots.txt Compliance), NFR-C-002 (Rate Limiting Compliance), Goal G-3

**Architecture Principle Alignment**: Principle 18 (Logging & Monitoring): Comprehensive logging for auditability

---

### DR-006: Data Quality Metrics

**Description**: Tracking table for data quality metrics over time (completeness, accuracy, freshness) to monitor Goal G-1 (95% Data Quality).

**Schema**:
```sql
CREATE TABLE data_quality_metrics (
    metric_id SERIAL PRIMARY KEY,
    metric_date DATE NOT NULL,
    total_restaurants INTEGER,
    total_menu_items INTEGER,
    completeness_pct NUMERIC(5,2),  -- % of items with all required fields populated
    accuracy_pct NUMERIC(5,2),  -- % of items passing manual validation (sampled)
    freshness_avg_days NUMERIC(5,1),  -- Average age of menu data in days
    scraping_success_rate_pct NUMERIC(5,2),  -- % of restaurants successfully scraped
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_data_quality_metrics_date ON data_quality_metrics(metric_date);
```

**Data Sources**: Automated daily calculation from database queries

**Validation Rules**:
- Percentages must be 0-100
- `metric_date` should be unique (one row per day)

**Retention Policy**: Metrics retained for 2 years (trend analysis)

**Priority**: **MUST_HAVE** (operational monitoring)

**Traces To**: FR-014 (Data Quality Monitoring Dashboard), Goal G-1 (95% Accuracy)

**Architecture Principle Alignment**: Principle 1 (Data Quality First): Continuous monitoring mandatory

---

### DR-007: User Feedback (Reporting Errors)

**Description**: User-reported data errors (incorrect prices, wrong dietary tags, stale data) to improve data quality iteratively.

**Schema**:
```sql
CREATE TABLE user_feedback (
    feedback_id SERIAL PRIMARY KEY,
    item_id INTEGER REFERENCES menu_items(item_id) ON DELETE SET NULL,
    restaurant_id INTEGER REFERENCES restaurants(restaurant_id) ON DELETE SET NULL,
    feedback_type VARCHAR(50),  -- "incorrect_price", "wrong_dietary_tag", "stale_data", "other"
    description TEXT,
    user_email VARCHAR(255),  -- Optional if user wants follow-up
    resolved BOOLEAN DEFAULT FALSE,
    resolved_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_user_feedback_resolved ON user_feedback(resolved);
CREATE INDEX idx_user_feedback_created_at ON user_feedback(created_at);
```

**Data Sources**: User submissions via "Report Error" button on dashboard

**Validation Rules**:
- `feedback_type` must match controlled vocabulary
- `description` must not be empty
- `user_email` must be valid email format if provided

**Retention Policy**: Resolved feedback retained for 1 year, unresolved indefinitely (pending review)

**Priority**: **SHOULD_HAVE** (improves data quality, not critical to MVP)

**Traces To**: Goal G-1 (95% Data Quality - user feedback informs improvements)

---

### DR-008: Opt-Out Exclusion List

**Description**: Permanent exclusion list of restaurants that have opted out, preventing re-scraping in future.

**Schema**:
```sql
CREATE TABLE opt_out_exclusions (
    exclusion_id SERIAL PRIMARY KEY,
    restaurant_name VARCHAR(255),
    website_url TEXT NOT NULL UNIQUE,
    contact_email VARCHAR(255),
    opt_out_reason TEXT,
    opted_out_at TIMESTAMP DEFAULT NOW()
);

CREATE UNIQUE INDEX idx_opt_out_exclusions_url ON opt_out_exclusions(website_url);
```

**Data Sources**: Opt-out form submissions (FR-015)

**Validation Rules**:
- `website_url` must be unique (cannot opt out twice)
- `website_url` must be valid HTTP/HTTPS URL

**Retention Policy**: Exclusion list retained indefinitely (permanent opt-out unless restaurant contacts to opt back in)

**Priority**: **MUST_HAVE** (compliance requirement)

**Traces To**: FR-015 (Opt-Out Form), NFR-C-005 (Opt-Out SLA), Goal G-3

**Architecture Principle Alignment**: Principle 3 (Ethical Scraping): Respect restaurant preferences unconditionally

---

### DR-009: CSV Export Generation

**Description**: Logic for generating RFC 4180 compliant CSV exports with UTF-8 encoding and metadata header.

**Implementation Requirements**:
- CSV must include metadata row: `# Exported from Plymouth Research - https://plymouthresearch.uk - {date}`
- CSV columns (menu items export): `restaurant_name, menu_item_name, price_gbp, category, dietary_tags, cuisine_type, last_updated, source_url`
- CSV columns (restaurants export): `restaurant_name, address, postcode, website_url, cuisine_type, price_range, last_updated`
- Quoted fields for text containing commas, newlines, or quotes
- UTF-8 encoding (not ASCII or Latin-1)

**Validation Rules**:
- Escape special characters to prevent CSV injection (e.g., `=SUM()` → `'=SUM()`)
- Test export opens correctly in Excel, Google Sheets, LibreOffice

**Priority**: **MUST_HAVE**

**Traces To**: FR-010 (Export to CSV), UC-2

**Architecture Principle Alignment**: Principle 11 (Standard Data Formats): CSV RFC 4180 compliant

---

## Integration Requirements

### INT-001: Third-Party Service - Email Delivery

**Description**: Platform requires transactional email service to send opt-out confirmation emails and (optional) data quality alerts.

**Integration Details**:
- **Service Options**: SendGrid (free tier 100 emails/day), Mailgun (free tier 5,000 emails/month), AWS SES (pay-as-you-go), or self-hosted SMTP
- **Email Types**:
  - Opt-out receipt confirmation: "We received your opt-out request..."
  - Opt-out completion: "Your restaurant has been removed..."
  - (Optional) Data quality alerts to Data Engineer: "Data quality dropped to 89%"
- **Authentication**: API key stored in environment variable (not in code)
- **Rate Limiting**: Max 10 emails/minute (prevent accidental spam if bug in code)

**Acceptance Criteria**:
- [ ] Opt-out emails sent within 1 minute of form submission
- [ ] Email delivery logs tracked (success/failure)
- [ ] Bounced emails logged for troubleshooting

**Priority**: **MUST_HAVE** (opt-out emails are compliance requirement)

**Stakeholder**: Restaurant Owners (SD-6), Operations/IT (SD-10)

**Traces To**: FR-015 (Opt-Out Form), NFR-C-005 (Opt-Out SLA)

**Architecture Principle Alignment**: Principle 11 (Standard Data Formats): Use standard SMTP or REST API for email

---

### INT-002: Third-Party Service - Uptime Monitoring

**Description**: Dashboard uptime monitored by external service (UptimeRobot, Pingdom, or equivalent) to detect outages within 5 minutes.

**Integration Details**:
- **Service Options**: UptimeRobot (free tier 50 monitors), Pingdom (paid), self-hosted monitoring
- **Monitored Endpoints**:
  - Dashboard homepage: `https://plymouthresearch.uk/` (HTTP 200 OK expected)
  - Health check: `https://plymouthresearch.uk/health` (JSON response with database connectivity check)
- **Check Frequency**: Every 1 minute (free tier may be 5 minutes)
- **Alert Channels**: Email to Operations/IT, Slack webhook (optional)

**Acceptance Criteria**:
- [ ] Uptime monitoring configured and tested (simulate downtime, verify alert fires)
- [ ] Alert delivered within 10 minutes of downtime
- [ ] Monthly uptime reports generated automatically

**Priority**: **MUST_HAVE**

**Stakeholder**: Operations/IT (SD-10), Research Director (SD-1)

**Traces To**: NFR-A-001 (99% Uptime SLA), NFR-P-005 (Monitoring Response Time)

**Architecture Principle Alignment**: Principle 18 (Logging & Monitoring): External monitoring for reliability

---

### INT-003: (Future) Food Delivery Platform APIs

**Description**: **OUT OF SCOPE for Phase 1**. Phase 2 may integrate with Deliveroo, Uber Eats, Just Eat APIs to augment restaurant website scraping with delivery platform data.

**Rationale**: Many restaurants have more complete menus on delivery platforms than on their own websites. However, this requires API agreements, potential costs, and legal review of API Terms of Service.

**Phase 2 Considerations**:
- API rate limits and costs
- Terms of Service restrictions on data usage
- Attribution requirements for delivery platform data
- Duplicate detection (same restaurant on website and Deliveroo)

**Priority**: **OUT OF SCOPE** (Phase 2 enhancement)

---

## Requirement Conflicts & Resolutions

### Conflict 1: Comprehensive Coverage (150 Restaurants) vs. Cost Constraints (<£100/month)

**Conflicting Requirements**:
- **BR-006**: Scrape 150+ restaurants (supports Research Director's authority goal)
- **BR-003**: Maintain costs <£100/month (supports Operations/IT sustainability goal)

**Stakeholders Involved**:
- **Research Director (SD-1)**: Wants 150+ restaurants for credibility and comprehensive coverage
- **Operations/IT (SD-10)**: Wants costs <£100/month to avoid budget overruns

**Trade-off Analysis**:
- **Option A**: Prioritize 150 restaurants, accept costs may reach £120-150/month initially
  - **Gain**: Comprehensive coverage, stronger value proposition, better market analysis
  - **Loss**: Cost overrun, potential need for external funding or sponsor
- **Option B**: Prioritize <£100 cost, limit to 100-120 restaurants
  - **Gain**: Financial sustainability guaranteed, no external funding needed
  - **Loss**: Less comprehensive coverage, weaker value proposition
- **Option C**: Phased approach - start with 60 restaurants (Month 1-2), validate costs, scale to 150 only if costs stay within budget
  - **Gain**: Risk mitigation, data-driven decision on scaling
  - **Loss**: Delayed comprehensive coverage by 2-3 months

**Resolution Strategy**: **COMPROMISE + PHASE** (Option C selected)
- **Decision**: Use phased scaling approach
  - Month 1-2: Scrape 30-60 restaurants (pilot batch)
  - Month 2-3: Validate costs <£100/month with 60 restaurants
  - Month 3-6: Scale to 150 if costs remain under budget; otherwise maintain 100-120 high-value restaurants
- **Rationale**: Balances both goals. Demonstrates cost efficiency before committing to full scale.
- **Technical Implementation**:
  - Right-size infrastructure (managed services with low base cost)
  - Serverless scraping (pay per scrape, not always-on VMs)
  - Monitor cost per restaurant monthly (target <£0.67/restaurant)
- **Success Metric**: If Month 3 costs <£80 with 60 restaurants, proceed to 150. If >£100, cap at 100-120.

**Decision Authority**: Research Director (final decision), with Operations/IT cost data input (per stakeholder RACI matrix)

**Stakeholder Management**:
- **Research Director**: Communicate that comprehensive coverage depends on cost validation. Frame as "responsible scaling" not "cost-cutting".
- **Operations/IT**: Monthly cost reports to Research Director. Recommend optimizations proactively.

**Resolution Documented**: ✅ **Research Director accepts phased approach**. Operations/IT responsible for monthly cost tracking.

---

### Conflict 2: Real-Time Menu Data vs. Ethical Rate Limiting (Weekly Refresh)

**Conflicting Requirements**:
- **Implied by BR-004** (User Adoption): Consumers prefer up-to-date menus (ideally daily or real-time)
- **NFR-C-002** (Rate Limiting): 5-second delays + respectful scraping → Weekly refresh is maximum ethical frequency for 150 restaurants

**Stakeholders Involved**:
- **Plymouth Consumers (SD-5)**: Want freshest possible menu data (daily or real-time ideal)
- **Restaurant Owners (SD-6)**: Want respectful scraping that doesn't burden servers (weekly or less frequent)
- **Legal/Compliance Advisor (SD-8)**: Requires ethical scraping compliance (weekly balances freshness vs. burden)

**Trade-off Analysis**:
- **Option A**: Daily scraping for real-time data
  - **Gain**: Fresher data, better user experience, competitive with delivery platforms
  - **Loss**: 7X server load on restaurants (unethical), higher scraping costs, potential complaints/blocks
- **Option B**: Weekly scraping (current plan)
  - **Gain**: Respectful to restaurants, ethical compliance, sustainable costs
  - **Loss**: Data can be up to 7 days stale, users may see outdated menus
- **Option C**: Weekly default + on-demand refresh for individual restaurants (rate-limited to 1 request/restaurant/day)
  - **Gain**: Balances freshness (users can request update) with ethics (most traffic is weekly, on-demand is rare)
  - **Loss**: Complexity of on-demand refresh feature, potential for abuse if not rate-limited properly

**Resolution Strategy**: **COMPROMISE + PHASE** (Option B for MVP, Option C for Phase 2)
- **Decision**: Weekly automated refresh for all restaurants (MVP/Phase 1)
  - Clearly communicate data freshness: "Last updated: 3 days ago" on every menu
  - Stale data warning: "Data may be outdated" if >10 days old
  - Phase 2: Add "Request Refresh" button (rate-limited to 1/restaurant/day)
- **Rationale**:
  - Weekly refresh is ethical and sustainable
  - Most restaurant menus don't change weekly (except specials)
  - User expectation setting (communicate freshness) mitigates dissatisfaction
- **Technical Implementation**:
  - Cron job runs weekly (Sunday 2am) for all restaurants
  - Freshness timestamp displayed prominently on dashboard
  - Phase 2: "Request Refresh" button triggers on-demand scrape (queued, rate-limited)

**Decision Authority**: Research Director with Legal Advisor consultation (per RACI)

**Stakeholder Management**:
- **Consumers**: Set expectations clearly ("Weekly refresh. Last updated: X days ago"). Emphasize ethical scraping in FAQ.
- **Restaurant Owners**: Communicate weekly frequency in opt-out notification email. Position as "respectful aggregation".
- **Legal Advisor**: Confirm weekly frequency is ethical and compliant (vs. daily which may be seen as excessive).

**Resolution Documented**: ✅ **Weekly refresh selected for MVP**. On-demand refresh deferred to Phase 2 with rate limiting.

---

### Conflict 3: Fast Dashboard Launch (Month 4) vs. 95% Data Quality

**Conflicting Requirements**:
- **BR-005**: Launch dashboard by Month 4 (March 2026) for timely value realization
- **BR-001** + **Goal G-1**: Achieve 95% data quality accuracy (may require iterative refinement beyond Month 4)

**Stakeholders Involved**:
- **Research Director (SD-1)**: Wants timely launch to start building reputation and user adoption
- **Data Engineer (SD-3)**: Wants quality implementation, not rushed technical debt
- **Research Analysts (SD-4)**: Need reliable data for analysis (won't use platform if accuracy <90%)

**Trade-off Analysis**:
- **Option A**: Rush to Month 4 launch with whatever quality achieved (70-80% likely)
  - **Gain**: Timely launch, start user adoption immediately
  - **Loss**: Poor data quality damages reputation (worse than no launch), user dissatisfaction, restaurant complaints
- **Option B**: Delay launch to Month 6 to achieve 95% quality before public release
  - **Gain**: High-quality launch, strong first impression, credible data
  - **Loss**: Delayed value realization, missed media opportunities, stakeholder impatience
- **Option C**: Phased launch - Beta (Month 3) for internal users + 10 friendly beta testers, iterate to 95%, Public Launch (Month 4) only if quality ≥90%
  - **Gain**: Quality validation before public launch, iterative improvement with user feedback
  - **Loss**: Beta testing adds 1 month overhead, potential for Month 5 delay if quality issues

**Resolution Strategy**: **PHASE + QUALITY GATE** (Option C with strict quality threshold)
- **Decision**:
  - **Month 3**: Beta launch for internal users (Research Analysts) + 10 friendly external beta testers
  - **Beta Exit Criteria**: ≥90% data quality (manual validation), <1000ms search performance, zero critical bugs
  - **Month 4**: Public launch ONLY if beta exit criteria met; otherwise delay to Month 5 until criteria satisfied
  - **Month 4-6**: Iterative improvement from 90% → 95% quality post-launch
- **Rationale**:
  - 90% quality is "good enough" for public launch (minimally acceptable)
  - 95% quality is target for Month 6 (continuous improvement)
  - Beta testing reduces public launch risk (catch quality issues privately)
- **Technical Implementation**:
  - Month 1-2: Scraper development + initial quality validation (target 80%+)
  - Month 3: Beta testing with 10 users, collect feedback, fix extraction errors
  - Month 4: Public launch if ≥90% quality, otherwise iterate 2 more weeks
  - Month 4-6: Manual QA reviews weekly, refine extraction rules, improve to 95%

**Decision Authority**: Research Director (final launch decision), with Data Engineer quality assessment input

**Stakeholder Management**:
- **Research Director**: Communicate that quality threshold is non-negotiable ("Better to delay 2 weeks than launch with poor data and damage reputation"). Emphasize long-term thinking.
- **Data Engineer**: Given clear quality target (≥90% for launch, 95% by Month 6). No pressure to rush and sacrifice quality.
- **Research Analysts**: Involved in beta testing (Month 3) to validate data quality meets their needs before public launch.

**Resolution Documented**: ✅ **Phased beta → public launch with 90% quality gate**. Research Director commits to delaying if quality insufficient.

---

## Requirements Traceability Matrix

| Requirement ID | Requirement Summary | Stakeholder Goal | Outcome | Architecture Principle | Priority |
|----------------|---------------------|------------------|---------|------------------------|----------|
| BR-001 | Establish Authority | G-1, G-2, G-6, G-7 | O-1 | Principle 1 (Data Quality), 2 (Open Source) | MUST |
| BR-002 | Minimize Legal Risk | G-3, G-8 | O-2 | Principle 3 (Ethical Scraping), 4 (Privacy) | MUST |
| BR-003 | Operational Sustainability | G-5, G-4, G-1 | O-3 | Principle 6 (Cost), 12 (Performance), 1 (Quality) | MUST |
| BR-004 | User Adoption | G-6, G-7 | O-4 | Principle 12 (Performance), 14 (Maintainability) | MUST |
| BR-005 | Dashboard Launch Month 4 | G-6 | O-1, O-4 | - | MUST |
| BR-006 | 150+ Restaurant Coverage | G-2 | O-1, O-4 | Principle 5 (Scalability) | MUST |
| FR-001 | Search by Name | G-4, O-4 | O-4 | Principle 12 (Performance) | MUST |
| FR-002 | Search by Dietary Tags | G-4, O-4 | O-4 | Principle 1 (Data Quality - conservative tagging) | MUST |
| FR-003 | Search by Price Range | G-4, O-4 | O-4 | - | SHOULD |
| FR-006 | Normalize Prices | G-1 | O-1, O-3 | Principle 1 (Data Quality) | MUST |
| FR-007 | Extract Dietary Tags | G-1 | O-4 | Principle 1 (Data Quality) | MUST |
| FR-010 | Export to CSV | G-7 | O-4 | Principle 11 (Standard Formats) | MUST |
| FR-011 | Web Scraping with Robots.txt | G-3, G-2 | O-2 | Principle 3 (Ethical Scraping) | MUST |
| FR-013 | Weekly Automated Refresh | G-2, G-3 | O-3 | Principle 3 (Ethical - weekly respectful) | MUST |
| FR-014 | Data Quality Dashboard | G-1 | O-3 | Principle 18 (Monitoring) | MUST |
| FR-015 | Opt-Out Form | G-3 | O-2 | Principle 3 (Ethical - opt-out mandatory) | MUST |
| NFR-P-001 | Search <500ms | G-4 | O-3, O-4 | Principle 12 (Performance) | MUST |
| NFR-P-003 | Scraping Cycle <24hrs | G-2 | O-3 | Principle 5 (Scalability - parallel scraping) | MUST |
| NFR-SEC-001 | TLS Encryption | G-8 | O-2 | Principle 4 (Privacy - encryption everywhere) | MUST |
| NFR-SEC-003 | SQL Injection Prevention | - | O-2 | Principle 4 (Privacy - security controls) | MUST |
| NFR-A-001 | 99% Uptime | G-13 | O-3 | Principle 13 (Availability) | MUST |
| NFR-C-001 | Robots.txt Compliance | G-3 | O-2 | Principle 3 (Ethical - NON-NEGOTIABLE) | MUST |
| NFR-C-002 | Rate Limiting Compliance | G-3 | O-2 | Principle 3 (Ethical - 5-second delays) | MUST |
| NFR-C-003 | GDPR Compliance | G-8 | O-2 | Principle 4 (Privacy - UK GDPR) | MUST |
| NFR-C-005 | Opt-Out 48hr SLA | G-3 | O-2 | Principle 3 (Ethical - respectful) | MUST |
| DR-001 | Restaurant Entity Schema | G-2 | O-1 | Principle 7 (Single Source of Truth) | MUST |
| DR-002 | Menu Item Entity Schema | G-1 | O-3 | Principle 8 (Data Lineage - source_html field) | MUST |
| DR-005 | Scraping Logs | G-3 | O-2 | Principle 18 (Logging - audit trail) | MUST |
| DR-008 | Opt-Out Exclusion List | G-3 | O-2 | Principle 3 (Ethical - permanent exclusions) | MUST |

**Total Requirements**: 69
- Business Requirements: 6
- Functional Requirements: 15
- Non-Functional Requirements:
  - Performance: 5
  - Security: 4
  - Scalability: 2
  - Availability: 3
  - Compliance: 5
  - Usability: 2
- Data Requirements: 9
- Integration Requirements: 2

---

## Next Steps

1. **Review & Approval**:
   - Circulate requirements document to Research Director, Data Engineer, Legal Advisor for review
   - Stakeholder sign-off required before proceeding to technology research

2. **Technology Research** (Month 1):
   ```
   /arckit.research Compare Scrapy vs BeautifulSoup, Streamlit vs Dash, PostgreSQL hosting options
   ```
   - Build vs buy vs open source analysis for all major components
   - Align with Principle 2 (Open Source Preferred) and Principle 6 (Cost Efficiency)

3. **Data Protection Impact Assessment** (Month 1):
   ```
   /arckit.dpia Assess GDPR compliance for web scraping restaurant menus
   ```
   - Required before launch per NFR-C-003
   - Legal Advisor review mandatory

4. **Data Model Design** (Month 1):
   ```
   /arckit.data-model Create detailed ER diagram and schema DDL for restaurants, menu items, dietary tags
   ```
   - Expand on DR-001 through DR-009 with full schema and relationships

5. **Architecture Design** (Month 1):
   - Document ADRs (Architectural Decision Records) for key technology choices
   - Create deployment architecture diagram (scraper, database, dashboard, monitoring)
   - Complete Goal G-8 (Architecture Design by Month 1)

---

**Generated by**: ArcKit `/arckit.requirements` command
**Generated on**: 2025-11-15 12:00 GMT
**ArcKit Version**: v0.9.1
**Project**: Plymouth Research Restaurant Menu Analytics (Project 001)
**AI Model**: Claude Sonnet 4.5 (claude-sonnet-4-5-20250929)
**Generation Context**: Requirements derived from:
- Stakeholder analysis (`stakeholder-drivers.md` - 10 stakeholders, 8 goals, 4 outcomes)
- Architecture principles (`.arckit/memory/architecture-principles.md` - 18 principles)
- Manual process documentation (`plan.md` - existing menu collection workflow)
