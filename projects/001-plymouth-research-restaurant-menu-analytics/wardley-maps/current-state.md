# Wardley Map: Plymouth Research Restaurant Menu Analytics - Current State

## Document Information

| Field | Value |
|-------|-------|
| **Document ID** | ARC-001-WMAP-v1.0 |
| **Project** | Plymouth Research Restaurant Menu Analytics (Project 001) |
| **Map Type** | Current State - Technology Stack |
| **Classification** | OFFICIAL |
| **Version** | 1.0 |
| **Date** | 2025-11-15 |
| **Owner** | Research Director, Plymouth Research |

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-11-15 | ArcKit AI | Initial Wardley Map creation from requirements and research findings |

---

## Executive Summary

This Wardley Map visualizes the Plymouth Research Restaurant Menu Analytics platform's technology value chain and component evolution. The map guides build vs buy decisions, vendor selection, and strategic positioning.

**Strategic Context**:
- **Budget Constraint**: <£100/month operational costs (Goal G-5)
- **Ethical Imperative**: 100% robots.txt compliance (Principle 3 NON-NEGOTIABLE)
- **Technology Strategy**: Open source preferred (Principle 2)
- **Target**: 150 restaurants, 7,500 menu items, 1,000+ monthly users

**Key Strategic Insights**:
1. **Build Custom**: ETL pipeline and scraping logic (Genesis/Custom components, competitive advantage)
2. **Adopt Open Source**: Scrapy framework, Streamlit dashboard, PostgreSQL (mature commodity tools)
3. **Use Free Tiers**: Streamlit Community Cloud, Render, UptimeRobot (£0 hosting, £0 monitoring)
4. **Buy Commodity**: DigitalOcean PostgreSQL (£15/month), AWS SES (pay-as-you-go)

**Total Monthly Cost**: £16/month operational (84% under budget)

---

## Wardley Map Visualization

**View this map**: Paste the code below into https://create.wardleymaps.ai

```wardley
title Plymouth Research Restaurant Menu Analytics - Current State

anchor Plymouth Consumers [0.95, 0.20]
annotation 1 [0.32, 0.18] BUILD - Competitive Advantage (Genesis/Custom)
annotation 2 [0.85, 0.92] ADOPT - Open Source Commodity
annotation 3 [0.75, 0.15] Total Cost: £16/month (84% under £100 budget)
note Budget Constraint: <£100/month operational (Principle 6: Cost Efficiency) [0.10, 0.05]

component Plymouth Consumers [0.95, 0.20]
component Menu Search & Discovery [0.92, 0.28]
component Dietary Filter Search [0.88, 0.32]
component Interactive Dashboard [0.82, 0.42]
component CSV Data Export [0.78, 0.55]
component Restaurant Coverage Goal [0.72, 0.25]

component Web Scraping ETL Pipeline [0.58, 0.32]
component Data Quality Validation [0.55, 0.38]
component Menu Data Normalization [0.52, 0.35]
component Ethical Scraping Controls [0.50, 0.42]

component Scrapy Framework [0.62, 0.88]
component Streamlit Framework [0.78, 0.82]
component PostgreSQL Database [0.45, 0.92]
component Full-Text Search [0.42, 0.88]

component DigitalOcean Managed DB [0.35, 0.90]
component Streamlit Community Cloud [0.72, 0.95]
component Render Free Tier [0.52, 0.92]
component AWS SES Email [0.48, 0.94]
component UptimeRobot Monitoring [0.38, 0.96]

component UK GDPR Compliance [0.28, 0.68]
component Robots.txt Parser [0.46, 0.85]
component Rate Limiting [0.43, 0.87]

Plymouth Consumers -> Menu Search & Discovery
Plymouth Consumers -> Dietary Filter Search
Menu Search & Discovery -> Interactive Dashboard
Dietary Filter Search -> Interactive Dashboard
Menu Search & Discovery -> CSV Data Export
Interactive Dashboard -> Streamlit Framework
CSV Data Export -> Streamlit Framework

Restaurant Coverage Goal -> Web Scraping ETL Pipeline
Web Scraping ETL Pipeline -> Data Quality Validation
Web Scraping ETL Pipeline -> Menu Data Normalization
Web Scraping ETL Pipeline -> Ethical Scraping Controls

Web Scraping ETL Pipeline -> Scrapy Framework
Ethical Scraping Controls -> Robots.txt Parser
Ethical Scraping Controls -> Rate Limiting
Data Quality Validation -> PostgreSQL Database
Menu Data Normalization -> PostgreSQL Database

Interactive Dashboard -> Full-Text Search
Full-Text Search -> PostgreSQL Database
PostgreSQL Database -> DigitalOcean Managed DB
Streamlit Framework -> Streamlit Community Cloud
Scrapy Framework -> Render Free Tier
Scrapy Framework -> Robots.txt Parser
Scrapy Framework -> Rate Limiting

Ethical Scraping Controls -> UK GDPR Compliance
Data Quality Validation -> UK GDPR Compliance

Web Scraping ETL Pipeline -> AWS SES Email
Interactive Dashboard -> UptimeRobot Monitoring
Web Scraping ETL Pipeline -> UptimeRobot Monitoring

evolve Web Scraping ETL Pipeline 0.52 label Mature ETL patterns emerging
evolve Ethical Scraping Controls 0.68 label Industry standards forming
evolve Streamlit Framework 0.90 label Commoditizing rapidly

pipeline Interactive Dashboard [0.82, 0.42, 0.75]

style wardley
```

---

## Component Inventory

### User Needs & Capabilities (Visibility 0.85-0.95)

| Component | Visibility | Evolution | Stage | Strategic Notes |
|-----------|-----------|-----------|-------|-----------------|
| **Plymouth Consumers** | 0.95 | 0.20 | Genesis | Primary user need - restaurant discovery by dietary requirements |
| **Menu Search & Discovery** | 0.92 | 0.28 | Genesis | Unique capability - no competitors offer dietary-filtered menu search in Plymouth |
| **Dietary Filter Search** | 0.88 | 0.32 | Custom | Emerging need - vegan/gluten-free/allergen search, competitive advantage |
| **Restaurant Coverage Goal** | 0.72 | 0.25 | Genesis | Strategic goal - 150 restaurants (comprehensive Plymouth coverage) |

**Strategic Recommendation**: These are differentiating capabilities. Build custom to establish market position.

### Application Components (Visibility 0.70-0.85)

| Component | Visibility | Evolution | Stage | Strategic Notes |
|-----------|-----------|-----------|-------|-----------------|
| **Interactive Dashboard** | 0.82 | 0.42 | Custom | User-facing interface - use Streamlit (open source) |
| **CSV Data Export** | 0.78 | 0.55 | Product | Standard feature - Streamlit built-in widget |

**Strategic Recommendation**: Use Streamlit (Product 0.82) - mature open source framework, free Community Cloud hosting.

### Core Business Logic (Visibility 0.50-0.70)

| Component | Visibility | Evolution | Stage | Strategic Notes |
|-----------|-----------|-----------|-------|-----------------|
| **Web Scraping ETL Pipeline** | 0.58 | 0.32 | Custom | **BUILD** - Core IP, custom scraping logic for 150 restaurant formats |
| **Data Quality Validation** | 0.55 | 0.38 | Custom | **BUILD** - Principle 1: Data Quality First (95% accuracy target) |
| **Menu Data Normalization** | 0.52 | 0.35 | Custom | **BUILD** - Domain-specific (prices, dietary tags, categories) |
| **Ethical Scraping Controls** | 0.50 | 0.42 | Custom | **BUILD** - Principle 3: NON-NEGOTIABLE ethical compliance |

**Strategic Recommendation**: Build all core business logic - competitive advantage, no suitable products exist, aligns with Genesis/Custom positioning.

### Frameworks & Libraries (Visibility 0.60-0.80)

| Component | Visibility | Evolution | Stage | Strategic Notes |
|-----------|-----------|-----------|-------|-----------------|
| **Scrapy Framework** | 0.62 | 0.88 | **Commodity** | **ADOPT** - Mature open source (58.9k stars), built-in robots.txt compliance |
| **Streamlit Framework** | 0.78 | 0.82 | **Commodity** | **ADOPT** - Rapid dashboard development, 42.2k stars, free hosting |

**Strategic Recommendation**: Adopt mature open source frameworks - don't build custom scraping or dashboard frameworks.

### Data Storage (Visibility 0.40-0.50)

| Component | Visibility | Evolution | Stage | Strategic Notes |
|-----------|-----------|-----------|-------|-----------------|
| **PostgreSQL Database** | 0.45 | 0.92 | **Commodity** | **ADOPT** - Industry standard, full-text search (GIN indexes), mature |
| **Full-Text Search** | 0.42 | 0.88 | **Commodity** | **ADOPT** - Built into PostgreSQL (GIN/GiST indexes) |

**Strategic Recommendation**: Use PostgreSQL - commodity database, no need for specialized search (Elasticsearch overkill for 7,500 records).

### Infrastructure & Utilities (Visibility 0.30-0.55)

| Component | Visibility | Evolution | Stage | Strategic Notes |
|-----------|-----------|-----------|-------|-----------------|
| **DigitalOcean Managed DB** | 0.35 | 0.90 | **Commodity** | **BUY** - £15/month, UK region, automated backups |
| **Streamlit Community Cloud** | 0.72 | 0.95 | **Commodity** | **FREE** - £0/month hosting, auto-deploy from GitHub |
| **Render Free Tier** | 0.52 | 0.92 | **Commodity** | **FREE** - £0/month scraper cron job hosting |
| **AWS SES Email** | 0.48 | 0.94 | **Commodity** | **BUY** - £0.10 per 1,000 emails (opt-out notifications) |
| **UptimeRobot Monitoring** | 0.38 | 0.96 | **Commodity** | **FREE** - 50 monitors, 5-minute intervals |

**Strategic Recommendation**: Use free tiers and cheap commodity services - never build infrastructure. Total: £16/month.

### Compliance Components (Visibility 0.25-0.50)

| Component | Visibility | Evolution | Stage | Strategic Notes |
|-----------|-----------|-----------|-------|-----------------|
| **UK GDPR Compliance** | 0.28 | 0.68 | Product | Regulatory requirement - DPIA, 12-month retention, no PII |
| **Robots.txt Parser** | 0.46 | 0.85 | **Commodity** | Built into Scrapy - one-line config (ROBOTSTXT_OBEY=True) |
| **Rate Limiting** | 0.43 | 0.87 | **Commodity** | Built into Scrapy - DOWNLOAD_DELAY=5 setting |

**Strategic Recommendation**: Use Scrapy's built-in compliance features - don't build custom robots.txt parser or rate limiter.

---

## Evolution Analysis by Stage

### Genesis (0.00-0.25): Novel & Uncertain

| Component | Evolution | Strategic Action |
|-----------|-----------|------------------|
| Plymouth Consumers | 0.20 | **User Need Discovery** - Novel requirement (no competitors offer dietary-filtered menu aggregation in Plymouth) |
| Restaurant Coverage Goal | 0.25 | **Market Positioning** - Comprehensive coverage (150 restaurants) establishes authority |

**Investment**: Build user research and market validation (Month 1-4). Launch MVP dashboard by Month 4 (BR-005).

**Risk**: Uncertain product-market fit. Mitigate with early user feedback (Goal G-7: 1,000+ searches by Month 9).

### Custom (0.25-0.50): Bespoke & Emerging

| Component | Evolution | Strategic Action |
|-----------|-----------|------------------|
| **Menu Search & Discovery** | 0.28 | **BUILD** - Core differentiator, no market alternatives |
| **Dietary Filter Search** | 0.32 | **BUILD** - Competitive advantage (vegan/gluten-free/allergen search) |
| **Web Scraping ETL Pipeline** | 0.32 | **BUILD** - Domain-specific logic for 150 restaurant formats |
| **Menu Data Normalization** | 0.35 | **BUILD** - Custom rules for prices, dietary tags, categories |
| **Data Quality Validation** | 0.38 | **BUILD** - Principle 1: 95% accuracy target, domain-specific rules |
| **Interactive Dashboard** | 0.42 | **BUILD** using Streamlit framework (Product 0.82) |
| **Ethical Scraping Controls** | 0.42 | **BUILD** - Principle 3: NON-NEGOTIABLE robots.txt + rate limiting |

**Investment**: Development effort (4 weeks @ £3,750/week = £15,000 Year 1). Core IP and competitive moat.

**Opportunity**: First-mover advantage in Plymouth restaurant menu aggregation. No competitors identified.

### Product (0.50-0.75): Off-the-Shelf Solutions

| Component | Evolution | Strategic Action |
|-----------|-----------|------------------|
| CSV Data Export | 0.55 | **USE** Streamlit's built-in st.download_button() widget |
| UK GDPR Compliance | 0.68 | **IMPLEMENT** using standard practices (DPIA template, 12-month retention policy) |

**Investment**: Minimal - use standard frameworks and compliance templates.

**Avoid**: Don't build custom CSV export or GDPR frameworks (commodity patterns exist).

### Commodity (0.75-1.00): Utility Services

| Component | Evolution | Strategic Action |
|-----------|-----------|------------------|
| Streamlit Framework | 0.82 | **ADOPT** - 42.2k GitHub stars, free Community Cloud hosting |
| Full-Text Search | 0.88 | **USE** PostgreSQL GIN indexes (built-in commodity feature) |
| Scrapy Framework | 0.88 | **ADOPT** - 58.9k GitHub stars, built-in robots.txt + rate limiting |
| DigitalOcean Managed DB | 0.90 | **BUY** - £15/month managed PostgreSQL |
| PostgreSQL Database | 0.92 | **ADOPT** - Industry standard, mature, open source |
| Render Free Tier | 0.92 | **USE** - £0/month cron job hosting |
| AWS SES Email | 0.94 | **BUY** - £0.10 per 1,000 emails |
| Streamlit Community Cloud | 0.95 | **USE** - £0/month dashboard hosting |
| UptimeRobot Monitoring | 0.96 | **USE** - £0/month monitoring (50 monitors free) |

**Investment**: Use existing utilities - never build these components.

**Cost Breakdown**:
- DigitalOcean PostgreSQL: £15/month
- AWS SES: <£1/month (50 opt-outs/year expected)
- Free tiers: £0/month (Streamlit Cloud, Render, UptimeRobot)
- **Total**: £16/month (84% under £100 budget)

---

## Build vs Buy Analysis

### BUILD (Genesis/Custom: Competitive Advantage)

**Candidates**:
1. ✅ **Menu Search & Discovery** (0.28) - Novel capability, no market alternatives
2. ✅ **Dietary Filter Search** (0.32) - Competitive differentiator, domain-specific
3. ✅ **Web Scraping ETL Pipeline** (0.32) - Custom logic for 150 restaurant formats
4. ✅ **Menu Data Normalization** (0.35) - Domain rules (prices, tags, categories)
5. ✅ **Data Quality Validation** (0.38) - Principle 1: 95% accuracy, custom rules
6. ✅ **Ethical Scraping Controls** (0.42) - Principle 3: NON-NEGOTIABLE compliance
7. ✅ **Interactive Dashboard UI** (0.42) - User-facing presentation (using Streamlit framework)

**TCO (3-Year)**: £15,000 development + £600 maintenance = £15,600

**Rationale**: These components are competitive advantages, domain-specific, and align with Genesis/Custom positioning. No suitable off-the-shelf products exist. Building establishes Plymouth Research as first-mover in this market.

**Risk Mitigation**:
- Use mature frameworks (Scrapy, Streamlit) to reduce development time
- Implement data quality gates to ensure 95% accuracy (Principle 1)
- Weekly scraper runs detect failures early

### ADOPT (Open Source: Mature Frameworks)

**Candidates**:
1. ✅ **Scrapy Framework** (0.88) - 58.9k stars, built-in robots.txt + rate limiting
2. ✅ **Streamlit Framework** (0.82) - 42.2k stars, rapid dashboard development
3. ✅ **PostgreSQL Database** (0.92) - Industry standard, full-text search, mature
4. ✅ **Robots.txt Parser** (0.85) - Built into Scrapy (ROBOTSTXT_OBEY=True)
5. ✅ **Rate Limiting** (0.87) - Built into Scrapy (DOWNLOAD_DELAY=5)

**TCO (3-Year)**: £0 licensing + £600 maintenance (PostgreSQL) = £600

**Rationale**: Mature open source projects with strong communities. Principle 2 (Open Source Preferred) alignment. Zero subscription costs enable <£100/month budget (Goal G-5).

**Risk Mitigation**:
- All projects actively maintained (recent commits, active communities)
- Production-proven (used by thousands of projects)
- Commercial support available if needed (Scrapy: Zyte, PostgreSQL: multiple vendors)

### BUY (Commodity: Managed Services)

**Candidates**:
1. ✅ **DigitalOcean Managed PostgreSQL** (0.90) - £15/month, UK region, automated backups
2. ✅ **AWS SES Email** (0.94) - £0.10 per 1,000 emails (opt-out notifications)

**TCO (3-Year)**: £540 (DigitalOcean) + £3 (AWS SES) = £543

**Rationale**: Commodity managed services cheaper than self-hosting. DigitalOcean £15/month vs self-hosted £30/month (infrastructure + maintenance). Operational burden reduced.

### FREE (Commodity: Free Tiers)

**Candidates**:
1. ✅ **Streamlit Community Cloud** (0.95) - £0/month dashboard hosting
2. ✅ **Render Free Tier** (0.92) - £0/month scraper cron job hosting
3. ✅ **UptimeRobot Free Tier** (0.96) - £0/month monitoring (50 monitors)

**TCO (3-Year)**: £0

**Rationale**: Free tiers sufficient for scale (1,000 monthly users, 150 restaurants). Enables 84% cost savings vs paid alternatives.

**Risk**: Free tier limits (Streamlit: 1 GB, Render: 512 MB). Mitigation: Monitor usage, upgrade if needed (Streamlit paid: £20/month, Render: £9/month).

### REJECTED (Overkill or Budget Violators)

**Firecrawl API** (0.72 - Product):
- ❌ £83/month violates £100 budget (Goal G-5)
- ❌ Unclear robots.txt compliance (Principle 3 NON-NEGOTIABLE)
- ❌ Overkill for static HTML menus (AI features unnecessary)
- **Decision**: Use Scrapy instead (£0 subscription, explicit ethical controls)

**Elasticsearch** (0.88 - Commodity):
- ❌ Overkill for 7,500 records (PostgreSQL full-text search sufficient)
- ❌ Additional cost (£30-100/month managed)
- **Decision**: Use PostgreSQL GIN indexes (<500ms search, NFR-P-001)

---

## Inertia & Barriers to Change

### Inertia 1: Skills Gap (Scrapy Learning Curve)

**Component**: Scrapy Framework (0.88)
**Barrier**: Team unfamiliar with Scrapy framework, steeper learning curve than BeautifulSoup
**Impact**: MEDIUM - Potentially delayed development (1-2 weeks)
**Mitigation**:
- Allocate 1 week for Scrapy training (included in 4-week development estimate)
- Scrapy has excellent documentation and active community
- TCO savings (£3,600 vs Firecrawl £3,738) justify learning investment

**Status**: Manageable - training budget allocated

### Inertia 2: Process Change (Manual → Automated)

**Component**: Web Scraping ETL Pipeline (0.32)
**Barrier**: Research Analysts currently collect menu data manually (hours per restaurant), resistant to automation (job security concerns)
**Impact**: LOW - Analyst role shifts to data QA and market analysis (higher value work)
**Mitigation**:
- Communicate role evolution: Manual data collection → Data quality validation and research insights
- Demonstrate time savings: 8 hours/restaurant manual → 2 minutes automated
- Involve analysts in data quality rule definition (domain expertise)

**Status**: Addressed through stakeholder engagement (stakeholder-drivers.md: Analysts benefit from faster data availability)

### Inertia 3: Ethical Compliance Uncertainty

**Component**: Ethical Scraping Controls (0.42)
**Barrier**: Legal/Compliance Advisor requires explicit proof of robots.txt compliance and rate limiting before DPIA approval
**Impact**: HIGH - Blocks production launch (BR-005: Month 4 dashboard launch)
**Mitigation**:
- **Scrapy Configuration**:
  ```python
  # settings.py
  ROBOTSTXT_OBEY = True  # Mandatory robots.txt compliance
  DOWNLOAD_DELAY = 5      # 5-second delay per domain (Principle 3)
  USER_AGENT = 'Plymouth Research Menu Scraper - contact@plymouthresearch.uk'
  ```
- Provide Legal Advisor with Scrapy documentation proving compliance
- Log all robots.txt blocking events for audit trail
- DPIA approval contingent on demonstrated compliance (Month 1)

**Status**: Critical path - prioritize Month 1

---

## Movement & Evolution Predictions

### 12-Month Predictions (by Nov 2026)

| Component | Current | Target | Movement | Rationale |
|-----------|---------|--------|----------|-----------|
| **Streamlit Framework** | 0.82 | 0.90 | +0.08 | Commoditizing rapidly - more users, simpler deployment |
| **Ethical Scraping Controls** | 0.42 | 0.68 | +0.26 | Industry standards emerging (GDPR precedents, ICO guidance) |
| **Web Scraping ETL Pipeline** | 0.32 | 0.52 | +0.20 | Mature ETL patterns emerging for menu scraping |
| **Menu Search & Discovery** | 0.28 | 0.45 | +0.17 | Competitors may emerge (market validation) |

**Strategic Implications**:

1. **Streamlit commoditization** → Lower barrier to entry for competitors. Maintain advantage through data quality and coverage.

2. **Ethical scraping standardization** → Compliance becomes table stakes, not differentiator. Focus shifts to data accuracy and freshness.

3. **ETL pattern maturation** → Menu scraping tools may emerge (e.g., Firecrawl). Plymouth Research's custom logic and ethical track record remain competitive moat.

4. **Market validation** → If 1,000+ searches achieved (Goal G-7), competitors likely to enter. First-mover advantage critical.

### 24-Month Predictions (by Nov 2027)

| Component | Current | Target | Movement | Rationale |
|-----------|---------|--------|----------|-----------|
| **Dietary Filter Search** | 0.32 | 0.58 | +0.26 | Dietary restrictions mainstream, product solutions emerge |
| **Data Quality Validation** | 0.38 | 0.55 | +0.17 | Quality frameworks mature, standard tools available |
| **Interactive Dashboard** | 0.42 | 0.62 | +0.20 | Dashboard-as-a-service platforms commoditize analytics |

**Strategic Implications**:

1. **Dietary search commoditization** → Major platforms (Google, TripAdvisor) add dietary filtering. Plymouth Research must expand beyond search (recommendations, trends analysis).

2. **Quality frameworks mature** → Open source data quality tools emerge. Competitive advantage shifts from "having quality" to "speed of quality improvement".

3. **Dashboard commoditization** → No-code dashboard builders proliferate. Value shifts from presentation layer to proprietary data and insights.

**Strategic Response**:
- **Phase 2 (Year 2)**: Expand to recommendation engine, trend analysis, price tracking (Genesis components)
- **Phase 3 (Year 3)**: Geographic expansion (other UK cities), data partnerships (tourism boards)
- **Moat**: First-mover data advantage (historical menu data, dietary trend analysis)

---

## Dependencies & Value Chain

### Dependency Tree

```
Plymouth Consumers (0.95, 0.20)
├── Menu Search & Discovery (0.92, 0.28)
│   ├── Interactive Dashboard (0.82, 0.42)
│   │   ├── Streamlit Framework (0.78, 0.82)
│   │   │   └── Streamlit Community Cloud (0.72, 0.95)
│   │   ├── Full-Text Search (0.42, 0.88)
│   │   │   └── PostgreSQL Database (0.45, 0.92)
│   │   │       └── DigitalOcean Managed DB (0.35, 0.90)
│   │   └── UptimeRobot Monitoring (0.38, 0.96)
│   └── CSV Data Export (0.78, 0.55)
├── Dietary Filter Search (0.88, 0.32)
│   └── Interactive Dashboard (same as above)
└── Restaurant Coverage Goal (0.72, 0.25)
    └── Web Scraping ETL Pipeline (0.58, 0.32)
        ├── Scrapy Framework (0.62, 0.88)
        │   ├── Robots.txt Parser (0.46, 0.85)
        │   ├── Rate Limiting (0.43, 0.87)
        │   └── Render Free Tier (0.52, 0.92)
        ├── Data Quality Validation (0.55, 0.38)
        │   ├── PostgreSQL Database (0.45, 0.92)
        │   └── UK GDPR Compliance (0.28, 0.68)
        ├── Menu Data Normalization (0.52, 0.35)
        │   └── PostgreSQL Database (0.45, 0.92)
        ├── Ethical Scraping Controls (0.50, 0.42)
        │   ├── Robots.txt Parser (0.46, 0.85)
        │   ├── Rate Limiting (0.43, 0.87)
        │   └── UK GDPR Compliance (0.28, 0.68)
        ├── AWS SES Email (0.48, 0.94)
        └── UptimeRobot Monitoring (0.38, 0.96)
```

### Critical Path Analysis

**Path 1: User Search → Data Quality**
```
Plymouth Consumers → Menu Search → Dashboard → Full-Text Search → PostgreSQL → DigitalOcean
```
**Critical Dependencies**:
- DigitalOcean availability (99.99% SLA)
- PostgreSQL GIN index performance (<500ms search, NFR-P-001)
- Streamlit Community Cloud uptime

**Mitigation**:
- Monitor DigitalOcean SLA compliance monthly
- PostgreSQL query optimization (indexes, EXPLAIN ANALYZE)
- Streamlit Community Cloud backup plan (self-host on Render £9/month if needed)

**Path 2: Data Collection → Ethical Compliance**
```
Restaurant Coverage → Scraping ETL → Ethical Controls → Robots.txt Parser → Scrapy
```
**Critical Dependencies**:
- Scrapy robots.txt parser correctness (ROBOTSTXT_OBEY=True)
- Rate limiting enforcement (DOWNLOAD_DELAY=5)
- Legal Advisor DPIA approval

**Mitigation**:
- Automated tests for robots.txt compliance (unit tests + integration tests)
- Logging all blocked requests for audit trail
- Monthly compliance review with Legal Advisor

**Path 3: Data Quality → User Trust**
```
Scraping ETL → Data Quality Validation → PostgreSQL → Dashboard → Plymouth Consumers
```
**Critical Dependencies**:
- Data validation rules (95% accuracy target, Principle 1)
- Deduplication logic (prevent duplicate menu items)
- Freshness indicators (<7 days stale data flagged)

**Mitigation**:
- Weekly data quality reports (completeness %, accuracy %)
- Automated alerts for quality degradation (<90% threshold)
- Research Analysts manual spot-checks (10% sample)

---

## Risk Analysis

### High-Risk Areas

#### Risk 1: Single Vendor Dependency (DigitalOcean)

**Component**: DigitalOcean Managed PostgreSQL (0.90)
**Risk**: Vendor outage or price increase disrupts service
**Likelihood**: LOW (DigitalOcean 99.99% SLA)
**Impact**: HIGH (Dashboard unavailable, data inaccessible)

**Mitigation**:
- Daily automated backups to local storage (S3 compatible)
- PostgreSQL dump scripts for vendor migration (AWS RDS, Azure Database)
- Exit plan: 1-week migration to AWS RDS (similar cost)

**Exit TCO**: AWS RDS £21/month (40% more expensive) - acceptable if forced migration

#### Risk 2: Scrapy Framework Abandonment

**Component**: Scrapy Framework (0.88)
**Risk**: Maintainer (Zyte) stops development, security vulnerabilities unpatched
**Likelihood**: VERY LOW (58.9k stars, 584 contributors, 15+ years active)
**Impact**: MEDIUM (No new features, potential security issues)

**Mitigation**:
- Scrapy is mature and stable (v2.13.3, BSD license)
- Large community can fork if Zyte abandons
- Alternative: BeautifulSoup + Requests (£2,900 migration cost)

**Exit TCO**: £2,900 (2 weeks development to migrate to BeautifulSoup)

#### Risk 3: Ethical Compliance Failure (Robots.txt Violation)

**Component**: Ethical Scraping Controls (0.42)
**Risk**: Accidental robots.txt violation → legal complaint → ICO fine
**Likelihood**: LOW (Scrapy ROBOTSTXT_OBEY enforced, tested)
**Impact**: CRITICAL (Reputational damage, ICO fine £1K-£10K, project shutdown)

**Mitigation**:
- **ROBOTSTXT_OBEY=True** mandatory (hardcoded, cannot be disabled)
- Automated tests verify robots.txt respected (integration test suite)
- Monthly legal compliance review with Legal Advisor
- Comprehensive logging (audit trail for all requests)
- Opt-out form prominent (FR-015: Restaurant opt-out mechanism)

**Remediation Plan**: If violation occurs:
1. Immediate halt of scraper (kill cron job)
2. Legal Advisor notified within 24 hours
3. Affected restaurant contacted with apology and data deletion confirmation
4. Root cause analysis and preventative controls added

#### Risk 4: Budget Overrun (Free Tier Limits)

**Component**: Streamlit Community Cloud (0.95), Render Free Tier (0.92)
**Risk**: Usage exceeds free tier limits → forced upgrade → budget violated
**Likelihood**: MEDIUM (1,000 users may exceed 1 GB Streamlit limit)
**Impact**: MEDIUM (£20-30/month upgrade required)

**Mitigation**:
- Monitor Streamlit resource usage monthly
- Optimize dashboard code (caching, lazy loading)
- Fallback: Self-host Streamlit on Render £9/month (still under £100 budget)

**Budget Buffer**: £84/month available (£100 budget - £16 current costs)

### Opportunities

#### Opportunity 1: Data Monetization (Phase 2)

**Component**: CSV Data Export (0.55)
**Opportunity**: Food researchers and journalists value aggregated menu data
**Potential**: Subscription model (£5/month for unlimited CSV exports)
**Revenue Forecast**: 100 subscribers × £5 = £500/month (5x budget)

**Strategic Alignment**: Monetization violates current "free public resource" scope (BR-004). Defer to Phase 2 after establishing authority.

#### Opportunity 2: Geographic Expansion (Phase 2+)

**Component**: Restaurant Coverage Goal (0.25)
**Opportunity**: Expand beyond Plymouth to other UK cities (Bristol, Exeter, Brighton)
**Scalability**: Scraping logic reusable (marginal cost per city)
**Revenue**: Tourism board partnerships, local advertising

**Strategic Timing**: After Plymouth success (1,000+ searches, 10+ media citations)

#### Opportunity 3: API Access (Phase 3)

**Component**: Interactive Dashboard (0.42)
**Opportunity**: RESTful API for third-party integrations (food blogs, tourism apps)
**Potential Users**: Local media, tourism websites, restaurant discovery apps
**Monetization**: Freemium API (1,000 calls/month free, £50/month unlimited)

**Technical Readiness**: Low - requires API development (not in current scope)

---

## Strategic Recommendations

### Immediate Actions (0-3 Months: Discovery & Alpha)

**Month 1 (December 2025)**:
1. ✅ **Legal Compliance**: DPIA approval from Legal Advisor (contingent on Scrapy robots.txt compliance demonstration)
2. ✅ **Scrapy Setup**: Install Scrapy, configure `ROBOTSTXT_OBEY=True` and `DOWNLOAD_DELAY=5`
3. ✅ **Database Provisioning**: Create DigitalOcean PostgreSQL (UK London region), define schema (DR-001 to DR-009)
4. ⚠️ **Ethical Controls Testing**: Build automated test suite verifying robots.txt compliance (critical path for legal approval)

**Month 2 (January 2026)**:
5. ✅ **Scraper Development**: Build 5-10 test spiders for common restaurant menu patterns (tables, divs, lists)
6. ✅ **Data Quality Pipelines**: Implement validation rules (price format, required fields, deduplication)
7. ✅ **Dashboard Prototype**: Build Streamlit MVP with search, dietary filters, CSV export

**Month 3 (February 2026)**:
8. ✅ **Beta Testing**: Scrape 30-60 restaurants, validate data quality >90%
9. ✅ **Performance Optimization**: PostgreSQL GIN indexes, query optimization (<500ms search target)
10. ✅ **Monitoring Setup**: UptimeRobot monitors for dashboard and scraper uptime

**Deliverable**: Dashboard launched Month 4 (March 31, 2026) per BR-005

### Short-Term Actions (3-12 Months: Beta & Live)

**Months 4-6 (March-May 2026)**:
11. ✅ **Public Launch**: Dashboard live with 120+ restaurants (80% coverage goal)
12. ✅ **User Feedback Loop**: Quarterly satisfaction surveys (target >4.0/5.0)
13. ✅ **Weekly Scraping**: Automated cron job refreshes all 150 restaurants weekly
14. ✅ **Data Quality Monitoring**: Monthly QA reports (completeness %, accuracy %)

**Months 7-9 (June-August 2026)**:
15. ✅ **Scale to 150 Restaurants**: Achieve comprehensive Plymouth coverage (BR-006)
16. ✅ **User Adoption Campaign**: SEO optimization, local media outreach, social media
17. ✅ **Performance Validation**: Sustain <500ms search (NFR-P-001), >99% uptime (NFR-A-001)

**Months 10-12 (September-November 2026)**:
18. ✅ **Success Metrics Validation**:
    - 1,000+ monthly searches (Goal G-7)
    - 10+ media citations (Goal G-1)
    - >4.0/5.0 user satisfaction (Goal G-7)
    - Costs <£100/month sustained (Goal G-5)
19. ✅ **Retrospective**: Document lessons learned, platform ROI, Phase 2 planning

**Deliverable**: Platform operational sustainability demonstrated (Outcome O-3)

### Long-Term Strategic Actions (12-24 Months: Phase 2)

**Year 2 (2027)**:
20. 🔮 **AI-Powered Recommendations**: Genesis component (0.15 evolution) - personalized restaurant suggestions
21. 🔮 **Trend Analysis**: Custom component (0.35) - dietary trend reports, pricing analysis
22. 🔮 **Historic Data Platform**: Product component (0.65) - time-series menu price tracking
23. 🔮 **Geographic Expansion**: Replicate to 3-5 additional UK cities (Bristol, Exeter, Brighton)
24. 🔮 **Revenue Model Exploration**: Premium features (API access, CSV export subscriptions)

**Year 3 (2028)**:
25. 🔮 **Data Partnerships**: Tourism boards, local councils (free data access in exchange for funding)
26. 🔮 **Mobile App**: React Native app for on-the-go restaurant discovery
27. 🔮 **National Expansion**: Scale to 20-30 UK cities, establish as national restaurant data platform

---

## Traceability

### Requirements Coverage

| Component | Requirements Addressed | Rationale |
|-----------|----------------------|-----------|
| Menu Search & Discovery | FR-001, FR-002, FR-003, BR-001 | Core user-facing capability |
| Dietary Filter Search | FR-002, FR-003, FR-007 | Dietary tags (vegan, gluten-free, allergen-free) |
| Web Scraping ETL | FR-011, NFR-C-001, NFR-P-002, BR-006 | Automated scraping, 150 restaurants |
| Data Quality Validation | BR-001, NFR-P-001 | Principle 1: 95% accuracy target |
| Ethical Scraping Controls | NFR-C-001, NFR-P-002, BR-002 | Principle 3: Robots.txt + rate limiting |
| PostgreSQL Database | DR-001 to DR-009, NFR-P-001 | Database schema, full-text search |
| Interactive Dashboard | FR-001 to FR-010, NFR-U-001 | Search, filter, export UI |
| CSV Data Export | FR-010 | Data export for researchers |
| UK GDPR Compliance | NFR-C-003, BR-002 | DPIA, 12-month retention, no PII |
| DigitalOcean Managed DB | NFR-C-003, NFR-A-001 | UK region, 99.99% SLA |
| Streamlit Community Cloud | BR-003, NFR-A-001 | Free hosting, 99% uptime |
| Render Free Tier | BR-003, NFR-A-001 | Free cron job hosting |
| AWS SES Email | FR-015 | Opt-out notification emails |
| UptimeRobot Monitoring | NFR-M-001, NFR-A-001 | Availability monitoring |

**Coverage**: 100% of requirements mapped to components

### Architecture Principles Alignment

| Principle | Components | Compliance |
|-----------|-----------|------------|
| **1. Data Quality First** | Data Quality Validation (0.38), PostgreSQL Database (0.92) | ✅ 95% accuracy target, validation gates |
| **2. Open Source Preferred** | Scrapy (0.88), Streamlit (0.82), PostgreSQL (0.92) | ✅ All frameworks open source |
| **3. Ethical Web Scraping** | Ethical Scraping Controls (0.42), Robots.txt Parser (0.85), Rate Limiting (0.87) | ✅ NON-NEGOTIABLE compliance |
| **4. Privacy by Design** | UK GDPR Compliance (0.68) | ✅ DPIA, no PII, opt-out mechanism |
| **6. Cost Efficiency** | Free tiers (Streamlit, Render, UptimeRobot) | ✅ £16/month (84% under budget) |
| **12. Performance Targets** | Full-Text Search (0.88), PostgreSQL GIN indexes | ✅ <500ms search (NFR-P-001) |

**Alignment**: 100% of applicable principles satisfied

### Goals & Outcomes Traceability

| Goal/Outcome | Components | Status |
|--------------|-----------|--------|
| **G-1: 95% Data Quality** | Data Quality Validation (0.38), PostgreSQL (0.92) | ✅ Validation pipelines defined |
| **G-2: 150 Restaurants** | Web Scraping ETL (0.32), Scrapy (0.88) | ✅ Scalable architecture |
| **G-3: Ethical Compliance** | Ethical Scraping Controls (0.42), Robots.txt (0.85) | ✅ Scrapy built-in compliance |
| **G-5: Cost <£100/month** | Free tiers, DigitalOcean (£15/month) | ✅ £16/month operational |
| **G-6: Dashboard Launch Month 4** | Streamlit (0.82), PostgreSQL (0.92) | ✅ Rapid dev framework |
| **G-7: 1,000+ Searches** | Interactive Dashboard (0.42), Full-Text Search (0.88) | ✅ Scalable to 10K users |
| **O-3: Operational Sustainability** | All commodity services (free tiers) | ✅ £16/month sustained |

**Traceability**: All goals and outcomes have architectural support

---

## Next Steps

### Recommended ArcKit Commands

1. **`/arckit.sobc`** - Create Strategic Outline Business Case
   - **Why**: Wardley Map provides TCO data (£16/month operational) and build vs buy analysis for Economic Case
   - **Input**: Research findings (£6,093 3-year TCO), stakeholder goals (outcomes O-1 to O-4)
   - **Output**: 5-case business case (strategic, economic, commercial, financial, management)

2. **`/arckit.hld-review`** - Review High-Level Design
   - **Why**: Validate HLD architecture decisions against Wardley Map strategic positioning
   - **Checks**:
     - ✅ Not building commodity components (e.g., using Scrapy not custom scraper)
     - ✅ Building Genesis/Custom components for competitive advantage
     - ✅ Component evolution alignment (Scrapy 0.88 = Commodity = Adopt)
     - ✅ Dependencies match value chain (user needs → capabilities → infrastructure)

3. **`/arckit.roadmap`** - Create Architecture Roadmap
   - **Why**: Wardley Map movement predictions inform multi-year roadmap
   - **Timeline**:
     - **Q1-Q2 2026**: Dashboard launch (current state components)
     - **Q3-Q4 2026**: Scale to 150 restaurants, achieve 1,000+ searches
     - **2027**: Phase 2 (AI recommendations, trend analysis, geographic expansion)
     - **2028**: Phase 3 (national expansion, mobile app, data partnerships)

4. **`/arckit.backlog`** - Generate Product Backlog
   - **Why**: Convert Wardley Map components into prioritized user stories and sprints
   - **Epic 1**: Web Scraping ETL (FR-011, NFR-C-001) - 4 sprints
   - **Epic 2**: Interactive Dashboard (FR-001 to FR-010) - 3 sprints
   - **Epic 3**: Data Quality & Compliance (Principle 1, Principle 3) - 2 sprints

### Strategic Decisions to Review

1. **Decision Point: Firecrawl vs Scrapy**
   - **Wardley Analysis**: Both similar TCO (£3,738 vs £3,600), but Firecrawl violates budget (£83/month) and lacks ethical transparency
   - **Recommendation**: Scrapy confirmed - explicit robots.txt compliance, £0 subscription
   - **Status**: ✅ Resolved in research-findings.md v1.1

2. **Decision Point: Self-Host vs Managed Database**
   - **Wardley Analysis**: PostgreSQL is commodity (0.92) - buy managed service
   - **Recommendation**: DigitalOcean £15/month vs self-host £30/month
   - **Status**: ✅ Resolved - DigitalOcean selected

3. **Decision Point: Streamlit vs Plotly Dash**
   - **Wardley Analysis**: Both commodity frameworks (0.82 vs 0.75), Streamlit has free hosting
   - **Recommendation**: Streamlit - £0/month vs Dash £9/month hosting
   - **Status**: ✅ Resolved - Streamlit Community Cloud

### Open Questions for Stakeholders

1. **Phase 2 Timing**: When to start revenue model exploration (subscriptions, API access)?
   - **Current Scope**: Free public resource (BR-004)
   - **Opportunity**: £500/month potential revenue (100 subscribers × £5)
   - **Decision**: Defer until success validated (Month 12)

2. **Geographic Expansion Priority**: Which cities to expand to in Phase 2?
   - **Options**: Bristol, Exeter, Brighton, Bath, Southampton
   - **Criteria**: Similar size to Plymouth, active food scene, tourism potential
   - **Decision Needed**: Month 10 (based on Plymouth success)

3. **Data Partnerships**: Should Plymouth Research pursue tourism board partnerships?
   - **Benefit**: Free data access in exchange for funding/support
   - **Risk**: Loss of editorial independence
   - **Decision Needed**: Month 6 (after initial media citations)

---

## Conclusion

This Wardley Map confirms the Plymouth Research platform's strategic positioning:

**Strategic Strengths**:
1. ✅ **Build for Advantage**: Genesis/Custom components (menu search, scraping ETL, data quality) establish competitive moat
2. ✅ **Adopt Commodity**: Scrapy, Streamlit, PostgreSQL reduce development time and cost
3. ✅ **Free Tier Strategy**: £0 hosting (Streamlit, Render, UptimeRobot) enables 84% cost savings
4. ✅ **Ethical Foundation**: Explicit robots.txt compliance (Principle 3) mitigates legal risk

**Budget Achievement**: £16/month operational costs (84% under £100 budget)

**Risk Mitigation**: Single vendor dependencies (DigitalOcean), ethical compliance testing, free tier limits monitoring

**Evolution Strategy**: First-mover advantage (Genesis 0.20-0.32), anticipate commoditization (12-24 months), Phase 2 expansion (AI, geography, revenue)

**Next Actions**: Legal DPIA approval (Month 1), Scrapy development (Month 1-3), Dashboard launch (Month 4)

---

**Generated by**: ArcKit `/arckit.wardley` command
**Generated on**: 2025-11-15
**ArcKit Version**: 0.9.1
**Project**: Plymouth Research Restaurant Menu Analytics (Project 001)
**Model**: Claude Sonnet 4.5
