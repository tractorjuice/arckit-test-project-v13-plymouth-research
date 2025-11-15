# Plymouth Research Enterprise Architecture Principles

## Document Information

| Field | Value |
|-------|-------|
| **Document ID** | ARC-001-PRIN-v1.0 |
| **Project** | Plymouth Research Restaurant Menu Analytics (Project 001) |
| **Document Type** | Enterprise Architecture Principles |
| **Classification** | OFFICIAL |
| **Version** | 1.0 |
| **Status** | DRAFT |
| **Date** | 2025-11-15 |
| **Owner** | Enterprise Architecture Team |

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-11-15 | ArcKit AI | Initial creation from `/arckit.principles` command |

---

## Executive Summary

This document establishes the immutable principles governing all technology architecture decisions at Plymouth Research. These principles ensure consistency, security, scalability, and alignment with business strategy for the restaurant/bar menu analytics platform and future projects.

**Core Values**: Data Quality First, Open Source Preferred, Ethical Web Scraping, Privacy by Design

**Scope**: All technology projects, systems, and initiatives
**Authority**: Enterprise Architecture Review Board
**Compliance**: Mandatory unless exception approved by CTO/Technical Lead

**Philosophy**: These principles are **technology-agnostic** - they describe WHAT qualities the architecture must have, not HOW to implement them with specific products. Technology selection happens during research and design phases guided by these principles.

---

## I. Strategic Principles

### 1. Data Quality First (FOUNDATIONAL)

**Principle Statement**:
Data quality MUST be prioritized over speed of delivery. All data pipelines MUST implement validation, completeness checks, and accuracy verification before data is consumed by downstream systems or presented to users.

**Rationale**:
Plymouth Research's value proposition is accurate, reliable restaurant menu analysis. Inaccurate data undermines user trust, leads to poor business decisions, and damages reputation. The platform is only as valuable as the data quality it provides.

**Implications**:
- Implement data validation rules at point of ingestion (scraping layer)
- Define data quality metrics and monitor continuously (completeness %, accuracy %, freshness)
- Reject or quarantine data that fails quality checks rather than propagating bad data
- Maintain data lineage from source (restaurant website) to presentation (dashboard)
- Implement duplicate detection and deduplication logic
- Track and report data quality metrics in observability dashboards
- Automated alerts when data quality degrades below thresholds

**Quality Dimensions**:
- **Completeness**: No unexpected nulls in required fields (restaurant name, menu item name, price)
- **Accuracy**: Prices correctly extracted and normalized to GBP format
- **Consistency**: Same menu item normalized consistently across time periods
- **Timeliness**: Data freshness tracked, stale data flagged (e.g., >7 days old)
- **Uniqueness**: Duplicate menu items detected and merged

**Validation Gates**:
- [ ] Data quality rules defined for each data entity (restaurants, menu items, categories)
- [ ] Validation logic implemented at ingestion layer
- [ ] Data quality metrics dashboards created (completeness %, error rates)
- [ ] Automated data quality tests run on every ETL pipeline execution
- [ ] Data quarantine process for failed validation (manual review queue)
- [ ] Data quality SLAs defined (e.g., 95% completeness, 98% accuracy)

**Example Scenarios**:

✅ **GOOD**: Web scraper extracts price "£12.50" → Validates format → Normalizes to decimal 12.50 → Validates range (£0.50-£150) → Stores with source URL and scrape timestamp

❌ **BAD**: Web scraper extracts "Twelve pounds fifty" → Stores as-is → Dashboard displays gibberish → User loses trust

**Common Violations to Avoid**:
- Storing unvalidated scraped data directly without quality checks
- No monitoring of data completeness or freshness
- Proceeding with analysis when data quality is unknown
- No process for handling malformed or suspicious data

---

### 2. Open Source Preferred

**Principle Statement**:
Open source software SHOULD be the default choice for all components unless compelling technical, security, or business reasons justify proprietary alternatives. All technology selections must document "build vs buy vs open source" analysis.

**Rationale**:
Open source reduces vendor lock-in, lowers total cost of ownership, provides community support, enables customization, and aligns with transparency values. For a research organization, open source enables reproducibility and independent verification of analytical methods.

**Implications**:
- Evaluate open source options first during technology research
- Prefer mature, actively maintained projects with strong communities
- Consider total cost of ownership (licensing, support, training) in comparisons
- Contribute improvements back to open source communities where feasible
- Document rationale when proprietary software is selected
- Avoid vendor lock-in through standard interfaces and data portability

**Decision Criteria** (when evaluating open source vs proprietary):
- **Community Health**: Active maintainers, recent commits, responsive issue tracking
- **Maturity**: Production-ready, stable API, good documentation
- **Licensing**: Compatible with project requirements (MIT, Apache 2.0, GPL, etc.)
- **Support**: Commercial support available if needed, or strong community
- **Security**: Regular updates, CVE response process, security audit history
- **Total Cost**: Not just license cost - include maintenance, training, integration effort

**Validation Gates**:
- [ ] Technology research phase includes open source alternatives
- [ ] "Build vs buy vs open source" analysis documented for key components
- [ ] Proprietary selections have documented justification
- [ ] No vendor lock-in patterns (proprietary APIs, data formats, deployment restrictions)
- [ ] Exit strategy defined for proprietary components

**Example Scenarios**:

✅ **GOOD**: Need database → Evaluate PostgreSQL (open source), MySQL (open source), Amazon Aurora (proprietary) → Select PostgreSQL for full-text search, JSONB support, no vendor lock-in, strong community

✅ **GOOD**: Need dashboard → Evaluate Streamlit (open source), Plotly Dash (open source), Tableau (proprietary) → Select Tableau with justification: "Business stakeholders require specific Tableau integrations, proprietary cost justified by reduced training time"

❌ **BAD**: Select proprietary tool without evaluating open source alternatives, then realize open source could have met 90% of needs at 10% of cost

**Common Violations to Avoid**:
- Defaulting to proprietary software without evaluation
- Choosing immature or abandoned open source projects
- Ignoring total cost of ownership (support, training)
- Failing to document "why not open source" for proprietary selections

---

### 3. Ethical Web Scraping (NON-NEGOTIABLE)

**Principle Statement**:
All web scraping activities MUST respect website terms of service, robots.txt directives, rate limits, and intellectual property rights. Scraping is a privilege, not a right—we must operate within legal and ethical boundaries.

**Rationale**:
Unethical scraping damages relationships with data sources (restaurants), creates legal liability (copyright, computer misuse), and risks blocking/legal action. Respectful scraping ensures long-term sustainability and maintains Plymouth Research's reputation.

**Mandatory Requirements**:
- [ ] **Robots.txt Compliance**: MUST respect all robots.txt directives (no scraping disallowed paths)
- [ ] **Rate Limiting**: MUST implement delays between requests (minimum 5 seconds per domain)
- [ ] **User-Agent Identification**: MUST use honest User-Agent string identifying Plymouth Research with contact email
- [ ] **Terms of Service Review**: MUST review website ToS before scraping, respect prohibitions
- [ ] **Copyright Respect**: Only scrape factual data (prices, menu items), not copyrighted creative content
- [ ] **Attribution**: Credit original sources when displaying aggregated data
- [ ] **Opt-Out Mechanism**: Provide way for restaurants to request removal from platform

**Rate Limiting Standards**:
- **Default**: 1 request per 5 seconds per domain
- **Aggressive sites**: Reduce to 1 request per 10-30 seconds if patterns suggest burden
- **Polite hours**: Avoid scraping during peak business hours (11am-2pm, 5pm-9pm) if possible
- **Retry logic**: Exponential backoff on errors, respect HTTP 429 (Too Many Requests)

**Legal Compliance**:
- **UK Computer Misuse Act 1990**: No unauthorized access to computer systems
- **UK Copyright, Designs and Patents Act 1988**: No copying substantial creative works
- **GDPR**: Only scrape public business data, no personal data
- **Contract Law**: Respect website Terms of Service

**Validation Gates**:
- [ ] Robots.txt parser implemented and tested
- [ ] Rate limiting enforced (verified through logs and monitoring)
- [ ] User-Agent string identifies Plymouth Research with contact email
- [ ] Terms of Service review documented for all scraped sites
- [ ] Legal review of scraping practices by solicitor/legal counsel
- [ ] Opt-out mechanism implemented and publicly documented
- [ ] Attribution displayed in dashboard/reports

**Example Scenarios**:

✅ **GOOD**: Check robots.txt → Allowed → Scrape menu page → Wait 5 seconds → Next restaurant → Log all requests with timestamps → Monitor rate compliance

❌ **BAD**: Scrape 100 pages in 10 seconds → Ignore robots.txt → Use fake User-Agent → Get IP blocked → Legal letter from restaurant's lawyer

**Common Violations to Avoid**:
- Ignoring robots.txt "Disallow" directives
- Aggressive scraping that burdens target servers
- Deceptive User-Agent strings (fake Google bot)
- Scraping behind login walls without permission
- No rate limiting or delays between requests

**Exception Process**:
- NONE. Ethical scraping principles are non-negotiable.
- If robots.txt blocks required data, contact website owner for permission or API access

---

### 4. Privacy by Design (NON-NEGOTIABLE)

**Principle Statement**:
All systems MUST implement privacy protections from the start, complying with UK GDPR and data minimization principles. Personal data collection is prohibited unless absolutely necessary and legally justified.

**Rationale**:
Plymouth Research scrapes public business data (restaurant menus), not personal data. However, privacy principles ensure we never drift into PII collection, comply with GDPR, and protect any incidental personal data (e.g., user analytics on dashboard).

**Data Minimization**:
- **Scrape ONLY public business data**: Restaurant names, addresses, menu items, prices, opening hours
- **NO personal data**: No customer reviews, names, emails, phone numbers (unless public business contact)
- **Dashboard users**: Collect minimal analytics (anonymous usage patterns, no tracking across sites)

**GDPR Compliance (UK GDPR)**:
- **Lawful Basis**: Legitimate interests (business research and consumer information)
- **Data Subject Rights**: Process for restaurants to request removal (Right to Erasure)
- **Data Retention**: Delete historical data after 12 months (unless longer retention justified)
- **Security**: Encrypt data at rest and in transit
- **Breach Notification**: Process for notifying ICO within 72 hours if breach occurs

**Privacy Controls**:
- [ ] Data classification performed (all scraped data is "public business data")
- [ ] No PII collection in scraping logic (automated detection and filtering)
- [ ] User analytics anonymized (no cookies, no cross-site tracking)
- [ ] Data retention policy automated (12-month deletion for historical data)
- [ ] Encryption at rest for all databases
- [ ] Encryption in transit (HTTPS/TLS for all communication)
- [ ] Privacy policy published and accessible
- [ ] Data Protection Impact Assessment (DPIA) completed

**Validation Gates**:
- [ ] DPIA completed and reviewed
- [ ] Data minimization verified in scraping logic
- [ ] No PII detected in scraped datasets (automated scanning)
- [ ] Retention policy implemented with automated deletion
- [ ] Encryption at rest and in transit validated
- [ ] Privacy policy published on website
- [ ] ICO registration completed (if required)

**Example Scenarios**:

✅ **GOOD**: Scrape restaurant menu → Extract restaurant name (business data), menu items (factual data), prices (factual data) → Store with scrape timestamp → Delete after 12 months

❌ **BAD**: Scrape restaurant page → Extract customer reviews with names → Extract restaurant owner's personal mobile number → Store indefinitely → GDPR violation, potential ICO fine

**Common Violations to Avoid**:
- Scraping personal data without legal basis
- No data retention limits (storing data forever)
- Unencrypted databases or network traffic
- No privacy policy or DPIA
- Ignoring data subject requests (Right to Erasure)

---

### 5. Scalability and Extensibility

**Principle Statement**:
All systems MUST be designed to scale from initial dataset (150 restaurants) to future growth (1,000+ restaurants, multiple cities) without architectural rework.

**Rationale**:
Plymouth Research may expand to other UK cities, add new data sources (food delivery platforms), or increase update frequency. Architecture must anticipate growth without requiring expensive redesign.

**Scalability Dimensions**:
- **Data Volume**: 150 restaurants → 1,000+ restaurants (10,000 → 100,000+ menu items)
- **Update Frequency**: Weekly → Daily → Real-time (as sources allow)
- **Geographic Expansion**: Plymouth → Devon → UK-wide
- **Data Sources**: Restaurant websites → Add food delivery APIs (Deliveroo, Uber Eats)
- **User Load**: Internal research → Public dashboard (1,000+ concurrent users)

**Implications**:
- Database design supports horizontal scaling (sharding, read replicas)
- ETL pipelines parallelizable (scrape multiple restaurants concurrently)
- Stateless application components (can add more instances)
- Avoid hard-coded limits (e.g., "max 200 restaurants")
- Caching strategy for high-traffic queries
- API design supports pagination and filtering

**Validation Gates**:
- [ ] Architecture supports 10x current capacity without major changes
- [ ] Database schema supports sharding or partitioning (if needed at scale)
- [ ] ETL pipelines can run in parallel (multiple workers)
- [ ] Application components are stateless (horizontal scaling)
- [ ] Performance testing at 10x expected load
- [ ] No hard-coded capacity limits in code

**Example Scenarios**:

✅ **GOOD**: Design scraper with configurable parallelism → Deploy 10 workers scraping concurrently → Expand to 100 workers for 1,000 restaurants → No code changes needed

❌ **BAD**: Single-threaded scraper → Takes 12 hours to scrape 150 restaurants → Expanding to 1,000 restaurants would take 80+ hours → Architectural rework required

---

### 6. Cost Efficiency

**Principle Statement**:
All systems MUST optimize for low operational cost while meeting quality and performance requirements. Total cost of ownership (infrastructure, licensing, maintenance) is a key selection criterion.

**Rationale**:
Plymouth Research is an independent research firm with limited budget. Cloud costs, licensing fees, and maintenance overhead must be minimized without compromising data quality or reliability.

**Cost Optimization Strategies**:
- **Open source**: Minimize licensing costs (see Principle 2)
- **Right-sizing**: Don't over-provision infrastructure (start small, scale as needed)
- **Serverless/managed services**: Reduce operational overhead (managed databases, serverless functions)
- **Storage optimization**: Compress historical data, archive old snapshots, delete unnecessary data
- **Caching**: Reduce compute costs by caching expensive queries
- **Spot instances**: Use low-cost compute for non-critical batch jobs (scraping)

**Cost Monitoring**:
- Track infrastructure costs monthly (cloud bills, hosting fees)
- Cost per restaurant (total cost / number of restaurants)
- Cost per query (API/dashboard usage costs)
- Alert on unexpected cost spikes

**Validation Gates**:
- [ ] Cost model documented for all major components
- [ ] Monthly cost budget defined and monitored
- [ ] Cost optimization opportunities identified and prioritized
- [ ] No unnecessary over-provisioning (right-sized infrastructure)
- [ ] Storage costs managed (compression, archival, deletion)

**Example Scenarios**:

✅ **GOOD**: Use serverless scraping (pay per scrape), managed PostgreSQL (no DBA overhead), static site hosting for dashboard (low cost) → Total cost £50-100/month for 150 restaurants

❌ **BAD**: Deploy always-on large VMs, enterprise database licenses, premium support contracts → Total cost £1,000+/month for same workload

---

## II. Data Principles

### 7. Single Source of Truth

**Principle Statement**:
Every data domain MUST have a single authoritative source. Derived copies must be clearly labeled as read-only caches and synchronized from the source of truth.

**Rationale**:
Multiple authoritative sources create inconsistency, reconciliation overhead, and user confusion. Clear ownership prevents data conflicts.

**Data Domains**:
- **Restaurants**: System of record = Restaurants table (source: scraped websites + manual curation)
- **Menu Items**: System of record = MenuItems table (source: scraped websites)
- **Categories**: System of record = Categories table (source: taxonomy rules)
- **Dietary Tags**: System of record = DietaryTags table (source: extraction rules + manual review)

**Implications**:
- One database table/collection is the authoritative source for each entity
- Dashboard queries read from source of truth or clearly labeled caches
- No bidirectional sync between systems (creates conflicts)
- Derived data (aggregations, analytics) refreshed from source on schedule
- Cache invalidation strategy defined for all derived copies

**Validation Gates**:
- [ ] System of record identified for each data entity
- [ ] Derived copies clearly labeled (e.g., "MenuItemsCache_Readonly")
- [ ] Synchronization strategy documented (frequency, conflict resolution)
- [ ] No bidirectional sync patterns

**Example Scenarios**:

✅ **GOOD**: MenuItems table (source of truth) → Dashboard caches aggregated menu stats → Cache refreshed hourly from source → Users see consistent data

❌ **BAD**: MenuItems table + separate "AnalyticsMenuItems" table both editable → Data diverges → Users see different menu counts in different views → Confusion

---

### 8. Data Lineage and Traceability

**Principle Statement**:
All data MUST be traceable to its original source (restaurant website URL, scrape timestamp) to enable validation, troubleshooting, and compliance.

**Rationale**:
When data quality issues arise ("this price looks wrong"), we must trace back to source (original HTML snapshot) to investigate. Lineage enables debugging, quality audits, and copyright attribution.

**Required Metadata**:
- **Source URL**: Original restaurant website page
- **Scrape Timestamp**: When data was extracted (ISO 8601 format)
- **Scraper Version**: Code version that extracted data (for reproducibility)
- **Raw Data Snapshot**: Archived HTML for re-processing if extraction logic improves
- **Transformation History**: Log of normalization steps applied

**Implications**:
- Store source metadata alongside every data record
- Archive raw HTML snapshots (compressed, for 12 months)
- Version control extraction/transformation logic (Git)
- Ability to re-run ETL on historical data with new logic
- Data quality investigations can reference original source

**Validation Gates**:
- [ ] Source URL and timestamp stored for every menu item
- [ ] Raw HTML snapshots archived (compressed)
- [ ] ETL pipeline code version-controlled
- [ ] Ability to re-process historical data demonstrated
- [ ] Data lineage queryable (e.g., "show me all menu items from Restaurant X scraped on 2025-11-01")

**Example Scenarios**:

✅ **GOOD**: Menu item "Fish & Chips - £12.50" → Stored with source_url="https://restaurant.com/menu", scrape_timestamp="2025-11-15T10:30:00Z", scraper_version="v1.2.3", raw_html_snapshot_id="abc123"

❌ **BAD**: Menu item "Fish & Chips - £12.50" → No source metadata → User reports "this price is wrong" → Impossible to verify, no way to trace back to original website

---

### 9. Data Normalization and Consistency

**Principle Statement**:
All data MUST be normalized to consistent formats and standards to enable accurate comparison, aggregation, and analysis.

**Rationale**:
Restaurant websites use inconsistent formats (£12.50, £12.5, 12.50 GBP, Twelve pounds fifty). Normalization ensures apples-to-apples comparisons and reliable analytics.

**Normalization Rules**:
- **Prices**: Decimal format (12.50), GBP currency, validated range (£0.50 - £500)
- **Restaurant Names**: Title case, no extra whitespace, diacritics preserved (e.g., "Café")
- **Menu Item Names**: Title case, standardized phrases ("Fish and Chips" not "Fish n chips")
- **Categories**: Controlled vocabulary (Starters, Mains, Desserts, Drinks, etc.)
- **Dietary Tags**: Standardized tags (Vegan, Vegetarian, Gluten-Free, Dairy-Free, Nut-Free, etc.)
- **Addresses**: UK postcode format validated, geocoded to lat/lon

**Quality Checks**:
- Price range validation (flag outliers)
- Duplicate detection (same dish, different spelling)
- Category assignment rules (ML or keyword-based)
- Dietary tag extraction (allergen keywords, vegan/vegetarian patterns)

**Validation Gates**:
- [ ] Normalization rules defined for all data fields
- [ ] Automated normalization applied in ETL pipeline
- [ ] Quality checks detect outliers and anomalies
- [ ] Duplicate detection and merging logic implemented
- [ ] Standardized taxonomies (categories, dietary tags) documented

**Example Scenarios**:

✅ **GOOD**: Extract "£12.50", "£12.5", "12.50 GBP" → All normalized to 12.50 (decimal) → Users can sort/filter reliably

❌ **BAD**: Store "£12.50", "£12.5", "12.50 GBP" as-is → Dashboard sorting fails → User sees "£12.5" before "£12.50" (string sort, not numeric)

---

## III. Integration & Interoperability Principles

### 10. API-First Design (Future-Proofing)

**Principle Statement**:
All data access SHOULD be through well-defined APIs (even if internal-only initially) to enable future integrations, mobile apps, and third-party access.

**Rationale**:
While initial focus is web dashboard, Plymouth Research may later add mobile apps, public API access, or third-party integrations. API-first design makes these expansions easier.

**Implications**:
- Dashboard consumes data through API endpoints, not direct database queries
- API design follows REST or GraphQL standards
- API versioning strategy defined (e.g., `/v1/restaurants`)
- API documentation generated automatically (OpenAPI/Swagger)
- Authentication and rate limiting planned (even if not enforced initially)

**Validation Gates**:
- [ ] API layer exists between dashboard and database
- [ ] API follows REST or GraphQL conventions
- [ ] API versioning strategy defined
- [ ] API documentation auto-generated and accessible
- [ ] Authentication and rate limiting designed (even if not yet enforced)

**Example Scenarios**:

✅ **GOOD**: Dashboard calls `GET /api/v1/restaurants?city=Plymouth&cuisine=Italian` → API layer queries database → Returns JSON → Future mobile app can use same API

❌ **BAD**: Dashboard runs SQL queries directly against database → Later want mobile app → Must rewrite all data access logic → Expensive refactoring

---

### 11. Standard Data Formats

**Principle Statement**:
All data interchange MUST use standard, documented formats (JSON, CSV, GeoJSON) with published schemas to enable interoperability and third-party integrations.

**Rationale**:
Proprietary or undocumented formats create integration friction. Standard formats enable easy data export, API integrations, and reproducible research.

**Standard Formats**:
- **API responses**: JSON (with JSON Schema for validation)
- **Data exports**: CSV (UTF-8, RFC 4180 compliant)
- **Geographic data**: GeoJSON (for restaurant locations on maps)
- **Dates/timestamps**: ISO 8601 (e.g., 2025-11-15T10:30:00Z)
- **Currency**: Decimal format, explicit currency code (GBP)

**Validation Gates**:
- [ ] API responses follow JSON standard
- [ ] CSV exports RFC 4180 compliant (quoted fields, UTF-8 encoding)
- [ ] Timestamps ISO 8601 format
- [ ] Geographic data GeoJSON compliant
- [ ] Schemas published and versioned

**Example Scenarios**:

✅ **GOOD**: API returns `{"name": "Fish & Chips", "price": 12.50, "currency": "GBP", "scraped_at": "2025-11-15T10:30:00Z"}` → Third-party tools can parse easily

❌ **BAD**: API returns `{"name": "Fish & Chips", "price": "£12.50", "scraped_at": "15/11/2025 10:30"}` → Non-standard date format, currency embedded in string → Parsing fragile

---

## IV. Quality Attributes

### 12. Performance Targets

**Principle Statement**:
All user-facing systems MUST meet defined performance targets to ensure responsive, usable experiences.

**Performance Requirements** (Plymouth Research Dashboard):
- **Dashboard Page Load**: < 2 seconds (p95)
- **Search Query Response**: < 500ms (p95)
- **Data Refresh (Full Scrape)**: < 24 hours for 150 restaurants
- **API Response Time**: < 200ms (p95) for simple queries, < 1s for complex aggregations

**Implications**:
- Performance testing before production deployment
- Database indexing on common query fields (restaurant name, cuisine, price range)
- Caching for expensive aggregations (price distributions, popular dishes)
- Asynchronous loading for large datasets (pagination, infinite scroll)
- Performance monitoring in production (latency percentiles tracked)

**Validation Gates**:
- [ ] Performance targets defined and documented
- [ ] Load testing performed at expected capacity
- [ ] Database indexes on query fields
- [ ] Caching strategy implemented for expensive operations
- [ ] Performance monitoring dashboard created

**Example Scenarios**:

✅ **GOOD**: User searches "vegan restaurants Plymouth" → Query uses index → Returns 20 results in 150ms → User sees instant results

❌ **BAD**: User searches "vegan restaurants Plymouth" → Full table scan → 5-second delay → User assumes site is broken, leaves

---

### 13. Reliability and Availability

**Principle Statement**:
All systems MUST meet defined availability targets with graceful degradation when failures occur.

**Availability Targets**:
- **Dashboard**: 99% uptime (7.2 hours downtime/month acceptable - maintenance windows)
- **Scraping Pipeline**: Best-effort (failures retry, eventual consistency acceptable)
- **Database**: 99.9% uptime (managed service SLA)

**Graceful Degradation**:
- Dashboard shows cached data if database unavailable (with staleness warning)
- Scraping failures logged and retried next cycle (no immediate user impact)
- Search degrades to simple text search if full-text index unavailable

**Validation Gates**:
- [ ] Availability SLAs defined for each component
- [ ] Health check endpoints implemented
- [ ] Graceful degradation tested (e.g., database unavailable)
- [ ] Automated retries for transient failures
- [ ] Monitoring and alerting on availability metrics

**Example Scenarios**:

✅ **GOOD**: Database down for 5 minutes → Dashboard shows cached data with banner "Data may be up to 1 hour old" → Users can still browse, no panic

❌ **BAD**: Database down for 5 minutes → Dashboard shows "500 Internal Server Error" → Users think site is broken

---

### 14. Maintainability and Documentation

**Principle Statement**:
All systems MUST be designed for long-term maintenance with clear documentation, modular architecture, and automated testing.

**Rationale**:
Plymouth Research is a small team. Code must be understandable by future maintainers (or future-you in 6 months). Good documentation reduces onboarding time and debugging effort.

**Documentation Requirements**:
- **Architecture Decision Records (ADRs)**: Document key technology choices and rationale
- **README**: Setup instructions, architecture overview, common tasks
- **Code Comments**: Document "why" not "what" (code should be self-explanatory)
- **API Documentation**: Auto-generated from code (OpenAPI/Swagger)
- **Runbooks**: Operational procedures (deployment, backup, restore, common errors)

**Maintainability Patterns**:
- Modular architecture (scraper, ETL, API, dashboard as separate components)
- Separation of concerns (business logic, data access, presentation)
- Automated tests enable confident refactoring
- Consistent code style (linters, formatters)
- Version control for all code and infrastructure

**Validation Gates**:
- [ ] Architecture documented (diagrams, ADRs)
- [ ] README with setup instructions
- [ ] API documentation auto-generated
- [ ] Runbooks for deployment and operations
- [ ] Automated tests with >70% coverage
- [ ] Code style enforced (linter/formatter)

**Example Scenarios**:

✅ **GOOD**: New developer joins → Reads README → Follows setup steps → Environment running in 30 minutes → ADRs explain key decisions → Productive in days

❌ **BAD**: New developer joins → No documentation → Asks lots of questions → Takes 2 weeks to understand codebase → Productive in months

---

## V. Development & Operations Principles

### 15. Infrastructure as Code

**Principle Statement**:
All infrastructure MUST be defined as code, version-controlled, and deployed through automated pipelines. Manual infrastructure changes are prohibited in production.

**Rationale**:
Manual changes create drift, inconsistency, and "works on my machine" problems. IaC enables repeatability, disaster recovery, and environment parity.

**Implications**:
- Database schemas version-controlled (migrations)
- Server configurations defined in code (even if single server)
- Deployment scripts automated and tested
- Environment parity (dev, staging, prod have same infrastructure code)
- No SSH into production servers for manual changes

**Validation Gates**:
- [ ] Infrastructure defined as code (scripts, config files)
- [ ] Infrastructure code version-controlled in Git
- [ ] Automated deployment pipeline exists
- [ ] Environment parity validated (dev matches prod)
- [ ] No manual production changes policy enforced

**Example Scenarios**:

✅ **GOOD**: Database schema change → Write migration script → Test in dev → Commit to Git → Deploy via automated pipeline → Repeatable, documented

❌ **BAD**: Database schema change → SSH into production → Run manual SQL → Forget exact command → Prod differs from dev → Disaster recovery impossible

---

### 16. Automated Testing

**Principle Statement**:
All code changes MUST be validated through automated tests before deployment to production.

**Test Coverage Requirements**:
- **Unit Tests**: 70%+ coverage for business logic (ETL normalization, validation rules)
- **Integration Tests**: API endpoints, database queries
- **End-to-End Tests**: Critical user flows (search, view menu, data export)
- **Data Quality Tests**: Validate scraped data meets quality standards

**Test Types**:
- **Scraper Tests**: Mock HTML responses, verify extraction correctness
- **ETL Tests**: Validate normalization rules, duplicate detection
- **API Tests**: Validate responses, error handling, authentication
- **Dashboard Tests**: UI component tests, user flow tests

**Validation Gates**:
- [ ] Automated tests exist and run on every commit
- [ ] Test coverage meets thresholds (70%+ unit, 100% critical paths)
- [ ] CI/CD pipeline blocks deployment if tests fail
- [ ] Data quality tests run on every ETL execution

**Example Scenarios**:

✅ **GOOD**: Developer changes price extraction logic → Unit tests fail (detects regression) → Fix before merge → Bug never reaches production

❌ **BAD**: Developer changes price extraction logic → No tests → Deploy → Discover all prices now off by 10% → Manual data cleanup required

---

### 17. Continuous Integration and Deployment

**Principle Statement**:
All code changes MUST go through automated build, test, and deployment pipelines with quality gates at each stage.

**Pipeline Stages**:
1. **Code Commit**: Developer pushes to Git
2. **Build**: Automated compilation/packaging (if applicable)
3. **Test**: Run automated test suite
4. **Quality Scan**: Linting, code quality checks, security scanning
5. **Deploy to Dev**: Automated deployment to development environment
6. **Manual Approval**: (Optional) for production deployment
7. **Deploy to Production**: Automated deployment

**Quality Gates**:
- All tests must pass (no failures)
- Code quality meets standards (linter passes)
- No critical security vulnerabilities (dependency scanning)
- Code review approved (for production deployments)

**Validation Gates**:
- [ ] CI/CD pipeline exists and runs on every commit
- [ ] Pipeline includes automated testing, quality checks, security scanning
- [ ] Deployment to production is automated (after approval)
- [ ] Rollback capability tested

**Example Scenarios**:

✅ **GOOD**: Developer commits code → CI runs tests → All pass → Deploy to dev automatically → Manual approval → Deploy to prod → Deployment takes 10 minutes

❌ **BAD**: Developer commits code → No CI → Manual testing → Manual deployment → Takes 2 hours, error-prone, inconsistent

---

## VI. Observability & Monitoring

### 18. Logging and Monitoring

**Principle Statement**:
All systems MUST emit structured logs and metrics enabling real-time monitoring, troubleshooting, and capacity planning.

**Logging Requirements**:
- **Structured Logs**: JSON format with timestamp, severity, component, message, context
- **Log Levels**: ERROR (failures requiring action), WARN (degraded state), INFO (key events), DEBUG (detailed troubleshooting)
- **Correlation IDs**: Track requests across components (scrape job ID, API request ID)

**Metrics to Track**:
- **Scraping**: Restaurants scraped, menu items extracted, failures, scrape duration
- **Data Quality**: Validation errors, duplicate detection rate, data completeness %
- **API**: Request volume, latency (p50, p95, p99), error rate
- **Dashboard**: Page views, search queries, user sessions
- **Infrastructure**: CPU, memory, disk usage, database connections

**Alerting**:
- Scraping failures exceed 10% of restaurants
- Data quality drops below 90% completeness
- API error rate exceeds 1%
- Database disk usage exceeds 80%

**Validation Gates**:
- [ ] Structured logging implemented (JSON format)
- [ ] Key metrics tracked and dashboards created
- [ ] Alerting configured for critical issues
- [ ] Log retention policy defined (30-90 days)
- [ ] Runbooks linked to alerts (what to do when alert fires)

**Example Scenarios**:

✅ **GOOD**: Scraping job fails for 20 restaurants → Logs show "robots.txt changed, now disallowed" → Alert fires → Team investigates and contacts restaurants → Issue resolved

❌ **BAD**: Scraping job silently fails → No logs → No monitoring → Discover 2 weeks later that data is stale → Users lost trust

---

## VII. Exception Process

### Requesting Architecture Exceptions

Principles are mandatory unless a documented exception is approved by the Enterprise Architecture Review Board (or Technical Lead for small teams).

**Valid Exception Reasons**:
- Technical constraints that prevent compliance (e.g., third-party API doesn't support required feature)
- Regulatory or legal requirements (e.g., must use specific proprietary tool for compliance)
- Transitional state during migration (e.g., legacy system being phased out)
- Pilot/proof-of-concept with defined end date (temporary exception)

**Exception Request Requirements**:
- [ ] Justification with business/technical rationale
- [ ] Alternative approach and compensating controls
- [ ] Risk assessment and mitigation plan
- [ ] Expiration date (exceptions are time-bound, typically 3-6 months max)
- [ ] Remediation plan to achieve compliance

**Approval Process**:
1. Submit exception request to Technical Lead/Architecture team
2. Review by technical team or architecture review board
3. Approval or rejection with feedback
4. Document exception in project architecture documentation
5. Regular review of exceptions (quarterly or at key project gates)

**Exceptions NOT Permitted**:
- Ethical Web Scraping (Principle 3) - NON-NEGOTIABLE
- Privacy by Design (Principle 4) - NON-NEGOTIABLE
- Security by Design controls - May vary implementation, but controls mandatory

---

## VIII. Governance and Compliance

### Architecture Review Gates

All projects should pass architecture reviews at key milestones:

**Discovery/Alpha**:
- [ ] Architecture principles understood and acknowledged
- [ ] High-level approach aligns with principles (no obvious violations)
- [ ] Technology research includes open source options
- [ ] Ethical and legal constraints identified

**Beta/Design**:
- [ ] Detailed architecture documented (ADRs, diagrams)
- [ ] Compliance with each principle validated or exceptions documented
- [ ] Data quality strategy defined
- [ ] Security and privacy controls designed
- [ ] Performance targets defined

**Pre-Production**:
- [ ] Implementation matches approved architecture
- [ ] All validation gates passed (tests, security scans, performance tests)
- [ ] Operational readiness verified (monitoring, logging, runbooks)
- [ ] Data Protection Impact Assessment (DPIA) completed

### Enforcement

- Architecture reviews are **recommended** for all projects (mandatory for large/risky projects)
- Principle violations should be remediated before production deployment
- Approved exceptions are time-bound and reviewed quarterly
- Retrospective reviews for compliance on live systems (annual audit)

---

## IX. Appendix

### Principle Summary Checklist

| # | Principle | Category | Criticality | Key Validation |
|---|-----------|----------|-------------|----------------|
| 1 | Data Quality First | Data | CRITICAL | Quality metrics, validation rules |
| 2 | Open Source Preferred | Strategic | HIGH | Build vs buy analysis |
| 3 | Ethical Web Scraping | Compliance | CRITICAL (NON-NEGOTIABLE) | Robots.txt compliance, rate limiting |
| 4 | Privacy by Design | Compliance | CRITICAL (NON-NEGOTIABLE) | DPIA, no PII collection |
| 5 | Scalability | Strategic | HIGH | 10x capacity testing |
| 6 | Cost Efficiency | Strategic | MEDIUM | Cost monitoring, optimization |
| 7 | Single Source of Truth | Data | HIGH | System of record identified |
| 8 | Data Lineage | Data | HIGH | Source URL + timestamp stored |
| 9 | Data Normalization | Data | HIGH | Normalization rules automated |
| 10 | API-First Design | Integration | MEDIUM | API layer exists |
| 11 | Standard Data Formats | Integration | MEDIUM | JSON Schema, ISO 8601 |
| 12 | Performance Targets | Quality | HIGH | Load testing, <500ms queries |
| 13 | Reliability | Quality | HIGH | 99% uptime, graceful degradation |
| 14 | Maintainability | Quality | MEDIUM | Documentation, ADRs, tests |
| 15 | Infrastructure as Code | DevOps | HIGH | IaC version-controlled |
| 16 | Automated Testing | DevOps | HIGH | 70%+ coverage, CI runs tests |
| 17 | CI/CD | DevOps | HIGH | Automated pipeline exists |
| 18 | Logging & Monitoring | Observability | HIGH | Structured logs, metrics dashboards |

**Criticality Levels**:
- **CRITICAL (NON-NEGOTIABLE)**: No exceptions permitted, mandatory compliance
- **CRITICAL**: Exceptions rare and require strong justification
- **HIGH**: Compliance expected, exceptions must be documented and time-bound
- **MEDIUM**: Compliance recommended, pragmatic exceptions acceptable

---

## X. Plymouth Research Context

### Project-Specific Considerations

**Current Project**: Restaurant Menu Analytics Dashboard (Plymouth, UK)

**Principle Priorities for This Project**:
1. **Data Quality First** - Core value proposition depends on accurate menu data
2. **Ethical Web Scraping** - Legal and reputational risk if violated
3. **Privacy by Design** - GDPR compliance mandatory for UK operation
4. **Open Source Preferred** - Budget constraints favor open source
5. **Cost Efficiency** - Limited budget requires optimization

**Recommended Technology Stack** (Principle-Compliant Examples):
- **Scraping**: Python (Beautiful Soup, Scrapy) - open source, mature, ethical scraping support
- **Database**: PostgreSQL - open source, full-text search, JSONB, GeoSpatial support
- **ETL**: Python (Pandas, data quality libraries) - open source, data science ecosystem
- **Dashboard**: Streamlit or Plotly Dash - open source, Python-native, rapid development
- **Hosting**: Cloud VPS (DigitalOcean, Linode) or managed services (Heroku, Render) - cost-efficient
- **Monitoring**: Open source stack (Prometheus, Grafana) or managed (free tier sufficient initially)

**Next Steps**:
1. Run `/arckit.stakeholders` to analyze stakeholder drivers and measurable outcomes
2. Run `/arckit.requirements` to document detailed requirements aligned with these principles
3. Run `/arckit.research` to evaluate technology options (build vs buy vs open source) using principle criteria
4. Run `/arckit.dpia` to assess privacy/GDPR compliance for web scraping
5. Run `/arckit.data-model` to design database schema with quality and lineage metadata

---

**Generated by**: ArcKit `/arckit.principles` command
**Generated on**: 2025-11-15
**ArcKit Version**: v0.9.1
**Project**: Plymouth Research Restaurant Menu Analytics (Project 001)
**AI Model**: Claude Sonnet 4.5 (claude-sonnet-4-5-20250929)
**Command Arguments**: A dashboard for analysing plymouth resturant/bars menus. Data first. Use open source
