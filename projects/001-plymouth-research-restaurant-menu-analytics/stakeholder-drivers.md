# Stakeholder Drivers & Goals Analysis: Plymouth Research Restaurant Menu Analytics

## Document Information

| Field | Value |
|-------|-------|
| **Document ID** | ARC-001-STKE-v1.0 |
| **Project** | Plymouth Research Restaurant Menu Analytics (Project 001) |
| **Document Type** | Stakeholder Drivers & Goals Analysis |
| **Classification** | OFFICIAL |
| **Version** | 1.0 |
| **Status** | DRAFT |
| **Date** | 2025-11-15 |
| **Owner** | Plymouth Research - Project Lead |

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-11-15 | ArcKit AI | Initial creation from `/arckit.stakeholders` command |

---

## Executive Summary

### Purpose
This document identifies key stakeholders for the Plymouth Research Restaurant Menu Analytics platform, their underlying drivers (motivations, concerns, needs), how these drivers manifest into goals, and the measurable outcomes that will satisfy those goals. This analysis ensures stakeholder alignment and provides traceability from individual concerns to project success metrics.

### Key Findings

The Plymouth Research platform has **7 primary stakeholder groups** with generally **HIGH alignment** around data quality and public benefit goals. The strongest driver is delivering accurate, actionable insights to Plymouth consumers and food researchers while maintaining ethical web scraping practices and GDPR compliance. A key tension exists between the research team's desire for comprehensive data coverage (150+ restaurants) and operational constraints (cost, scraping ethics, maintenance burden). Another potential conflict is between consumers wanting real-time menu data versus weekly refresh cycles being more sustainable and respectful to restaurant websites.

### Critical Success Factors
- **Data Quality**: 95%+ accuracy in menu extraction and price normalization - foundation of platform credibility
- **Ethical Scraping**: 100% compliance with robots.txt and rate limiting - protects long-term sustainability
- **User Adoption**: 1,000+ monthly searches within 6 months post-launch - validates market need
- **Cost Sustainability**: Operational costs <£100/month - ensures long-term viability for independent research firm
- **Restaurant Participation**: <5% opt-out rate from restaurants - indicates community acceptance

### Stakeholder Alignment Score
**Overall Alignment**: **HIGH**

There is strong alignment across stakeholders on core values (data quality, ethical practices, public benefit). Minor tensions exist around speed-vs-quality tradeoffs and comprehensiveness-vs-cost. The research team, consumers, and food writers all benefit from the same outcomes (accurate data, broad coverage, easy search). Restaurants have mixed interests - some see value in visibility, others may prefer exclusion. The project's ethical approach (opt-out mechanism, attribution) addresses potential restaurant concerns proactively.

---

## Stakeholder Identification

### Internal Stakeholders

| Stakeholder | Role/Department | Influence | Interest | Engagement Strategy |
|-------------|----------------|-----------|----------|---------------------|
| **Research Director** | Executive Sponsor / Project Owner | HIGH | HIGH | Active involvement, strategic decisions, budget authority |
| **Data Engineer** | Technical Lead / Implementation | MEDIUM | HIGH | Day-to-day development, architecture decisions, scraping logic |
| **Research Analysts** | Primary Users / Data Consumers | LOW | HIGH | Requirements input, user testing, feedback on search features |
| **Operations/IT** | Infrastructure & Maintenance | MEDIUM | MEDIUM | Deployment, monitoring, cost management, operational support |
| **Legal/Compliance Advisor** | Risk & Compliance | HIGH | MEDIUM | GDPR review, web scraping legality, copyright guidance |

### External Stakeholders

| Stakeholder | Organization | Relationship | Influence | Interest |
|-------------|--------------|--------------|-----------|----------|
| **Plymouth Consumers** | General Public | Beneficiaries | LOW | HIGH |
| **Restaurant Owners** | Local Businesses | Data Sources | MEDIUM | MEDIUM |
| **Food Writers/Journalists** | Media/Publications | Users & Amplifiers | MEDIUM | HIGH |
| **Local Tourism Board** | Plymouth City Council | Potential Partner | LOW | MEDIUM |
| **ICO (Information Commissioner)** | UK Regulator | Oversight | HIGH | LOW |
| **Website Hosting Providers** | Technical Services | Suppliers | LOW | LOW |

### Stakeholder Power-Interest Grid

```
HIGH POWER
    │
    │  [Manage Closely]             │  [Keep Satisfied]
    │  - Research Director           │  - Legal/Compliance Advisor
    │  - Data Engineer               │  - ICO (Regulator)
    │  - Restaurant Owners (collective) │
────┼──────────────────────────────────┼─────────────────────────
    │  [Keep Informed]                │  [Monitor]
    │  - Research Analysts            │  - Tourism Board
    │  - Plymouth Consumers           │  - Hosting Providers
    │  - Food Writers/Journalists     │
    │  - Operations/IT                │
    │                                 │
LOW POWER                                           HIGH INTEREST
```

---

## Stakeholder Drivers Analysis

### SD-1: Research Director - Establish Plymouth Research as Authoritative Data Source

**Stakeholder**: Research Director (Project Sponsor)

**Driver Category**: STRATEGIC + PERSONAL

**Driver Statement**:
Establish Plymouth Research as the authoritative, independent source for restaurant menu data in Plymouth, building organizational reputation and demonstrating research capability to attract future funding, partnerships, and clients.

**Context & Background**:
Plymouth Research is an independent research firm seeking to differentiate itself in the local market. Traditional market research is commoditized; data-driven insights from web scraping represent a modern, scalable approach. Success with this platform could lead to expansion (other cities, other data domains) and commercial opportunities (paid API access, consulting). The Research Director's career advancement and organizational growth depend on demonstrating innovation and delivering public value.

**Driver Intensity**: **CRITICAL**

**Enablers**:
- High-quality, accurate data that users trust
- Positive media coverage and word-of-mouth adoption
- Low operational costs enabling long-term sustainability
- Open source approach building credibility with technical audiences
- Academic or journalistic citations validating data quality

**Blockers**:
- Data quality issues damaging reputation
- Legal challenges from restaurants or regulators
- High costs requiring external funding or discontinuation
- Negative publicity about unethical scraping practices
- Technical failures or unreliable platform access

**Related Stakeholders**:
- Food Writers/Journalists (amplify reputation through citations)
- Plymouth Consumers (user adoption validates credibility)
- Restaurant Owners (acceptance indicates community support)

---

### SD-2: Research Director - Minimize Legal and Regulatory Risk

**Stakeholder**: Research Director (Project Sponsor)

**Driver Category**: RISK + COMPLIANCE

**Driver Statement**:
Ensure all web scraping, data storage, and publication activities comply with UK law (Computer Misuse Act, Copyright Act, GDPR) and avoid legal action, ICO fines, or reputational damage from unethical practices.

**Context & Background**:
Web scraping exists in a legal grey area. While scraping publicly accessible data is generally legal in the UK, violating robots.txt, overloading servers, or scraping copyrighted content creates risk. GDPR compliance is mandatory for UK operations. A single ICO fine or lawsuit from a restaurant could bankrupt the small research firm and destroy the Director's career. Risk mitigation is non-negotiable.

**Driver Intensity**: **CRITICAL** (NON-NEGOTIABLE)

**Enablers**:
- Legal review of scraping practices by solicitor
- Strict robots.txt and rate-limiting compliance built into scraper
- Data Protection Impact Assessment (DPIA) completed
- Opt-out mechanism for restaurants
- Clear attribution and transparency about data sources
- No PII collection (only public business data)

**Blockers**:
- Aggressive scraping triggering complaints
- Collecting personal data by mistake (GDPR violation)
- Copyright infringement (scraping creative content beyond factual data)
- Ignoring restaurant opt-out requests
- No legal review or DPIA

**Related Stakeholders**:
- Legal/Compliance Advisor (provides guidance and risk assessment)
- ICO (regulator who could impose fines)
- Restaurant Owners (potential complainants if feel violated)

---

### SD-3: Data Engineer - Build Maintainable, Scalable Technical Solution

**Stakeholder**: Data Engineer (Technical Lead)

**Driver Category**: OPERATIONAL + PERSONAL

**Driver Statement**:
Design and implement a technically sound, maintainable scraping and analytics platform using best practices, avoiding technical debt, and building skills in modern data engineering (web scraping, ETL, dashboards) that advance career prospects.

**Context & Background**:
The Data Engineer is responsible for implementation and ongoing maintenance. Poorly designed architecture creates future pain (manual fixes, brittle scrapers, performance issues). This project is an opportunity to demonstrate modern data engineering skills (Python, ETL, dashboard frameworks, cloud infrastructure) and build a portfolio project. Personal motivation includes learning new technologies, avoiding on-call nightmares from unreliable systems, and career advancement.

**Driver Intensity**: **HIGH**

**Enablers**:
- Open source tools with good documentation and community support
- Clear architecture principles to guide decisions
- Automated testing and CI/CD reducing manual deployment effort
- Infrastructure as Code for reproducible environments
- Adequate time for quality implementation (not rushed MVP)
- Opportunities to experiment with new technologies (within reason)

**Blockers**:
- Rushed timeline forcing technical debt
- Proprietary tools with poor documentation
- Unclear requirements leading to rework
- No budget for infrastructure (forced to use free tiers with limitations)
- Lack of automated testing causing fragile scrapers that break frequently

**Related Stakeholders**:
- Research Director (sets timeline and budget constraints)
- Operations/IT (inherits maintenance burden if Engineer leaves)
- Research Analysts (user feedback informs requirements quality)

---

### SD-4: Research Analysts - Access Reliable Data for Market Research

**Stakeholder**: Research Analysts (Primary Internal Users)

**Driver Category**: OPERATIONAL

**Driver Statement**:
Access accurate, comprehensive restaurant menu data quickly and easily to conduct market research, identify trends, and generate reports for internal analysis or external publications without manual data collection effort.

**Context & Background**:
Currently, Research Analysts manually collect menu data by visiting restaurant websites or calling establishments - time-consuming, error-prone, and not scalable. Analysts need to answer questions like "What's the average price for fish & chips in Plymouth?", "How many restaurants offer vegan mains?", "Which cuisines are most common?". The platform eliminates manual effort and enables data-driven analysis that wasn't feasible before.

**Driver Intensity**: **HIGH**

**Enablers**:
- Fast search functionality (<500ms response time)
- Comprehensive coverage (150+ restaurants)
- Reliable data quality (95%+ accuracy)
- Export to CSV/Excel for further analysis in familiar tools
- Filtering by cuisine, dietary requirements, price range
- Historical data for trend analysis

**Blockers**:
- Slow search queries frustrating user experience
- Incomplete data (missing restaurants or menu items)
- Inaccurate data requiring manual verification (defeating the purpose)
- No export functionality forcing manual copy-paste
- Dashboard unavailable or unreliable

**Related Stakeholders**:
- Data Engineer (implements search and dashboard features)
- Research Director (prioritizes analyst needs in roadmap)

---

### SD-5: Plymouth Consumers - Find Restaurants Meeting Dietary Needs

**Stakeholder**: Plymouth Consumers (External Users - General Public)

**Driver Category**: CUSTOMER

**Driver Statement**:
Easily find restaurants in Plymouth offering specific dishes, dietary options (vegan, gluten-free, nut-free), or within a price range, without manually browsing dozens of restaurant websites.

**Context & Background**:
Consumers with dietary restrictions (vegan, gluten-free, allergies) face friction finding suitable restaurants. Existing solutions (Google search, TripAdvisor) don't aggregate menu data or dietary tags effectively. Parents looking for kid-friendly menus, budget-conscious students seeking affordable options, or food enthusiasts exploring cuisines all benefit from searchable, aggregated menu data. Consumer adoption validates the platform's public value and drives word-of-mouth growth.

**Driver Intensity**: **MEDIUM** (important for public value, but not critical to organizational survival)

**Enablers**:
- Accurate dietary tagging (vegan, vegetarian, gluten-free, nut-free)
- Fast search with intuitive filters
- Mobile-friendly dashboard (many searches happen on phones)
- Up-to-date data (weekly refresh minimum)
- Coverage of diverse cuisines and price ranges

**Blockers**:
- Inaccurate dietary tags (dangerous for allergy sufferers)
- Stale data showing menus that have changed
- Slow or confusing search interface
- Limited restaurant coverage missing user's preferred spots
- Desktop-only interface unusable on mobile

**Related Stakeholders**:
- Food Writers/Journalists (amplify platform to consumers via media coverage)
- Research Director (consumer adoption validates strategic goal)
- Restaurant Owners (benefit from increased visibility if data accurate)

---

### SD-6: Restaurant Owners - Accurate Representation & Visibility

**Stakeholder**: Restaurant Owners (Data Sources)

**Driver Category**: CUSTOMER + RISK

**Driver Statement**:
Ensure restaurant menus are represented accurately on the platform (if included), avoid misrepresentation that could mislead customers, and have control over opt-out if desired.

**Context & Background**:
Restaurant owners have **mixed interests**. Some see value in free visibility and searchability ("food discovery platform"). Others may prefer exclusion due to:
- Concern about outdated menu data misleading customers
- Preference to drive traffic to their own website, not aggregators
- Worry about price comparison commoditizing their offering
- Copyright concerns over menu content

The platform must respect restaurant preferences, provide accurate data, and offer opt-out. Most restaurants will be neutral-to-positive if data is accurate and attributed. A vocal minority may resist aggregation.

**Driver Intensity**: **MEDIUM** (collectively important; individually varies)

**Enablers**:
- Accurate menu data with attribution (link to restaurant website)
- Opt-out mechanism prominently advertised
- Weekly refresh so data doesn't become stale
- No republication of copyrighted creative content (only factual menu data)
- Transparency about data sources and methodology

**Blockers**:
- Inaccurate menu data or prices causing customer complaints
- Stale data not reflecting menu changes
- No opt-out mechanism or ignored opt-out requests
- Scraping violating robots.txt or overloading their website
- Republishing copyrighted descriptions or images without permission

**Related Stakeholders**:
- Plymouth Consumers (benefit from accurate representation)
- Research Director (restaurant complaints create risk)
- Legal/Compliance Advisor (advises on copyright and opt-out process)

---

### SD-7: Food Writers/Journalists - Data-Driven Reporting on Food Scene

**Stakeholder**: Food Writers/Journalists (External Users - Media)

**Driver Category**: STRATEGIC + CUSTOMER

**Driver Statement**:
Access aggregated menu data to write data-driven stories about Plymouth's food scene (trends, pricing, dietary diversity), enhancing journalism with quantitative insights and citing Plymouth Research as source.

**Context & Background**:
Food writers traditionally rely on subjective reviews or small samples. Aggregated menu data enables new story angles: "Vegan options increased 40% in 2 years", "Average restaurant main course is £13.50 in Plymouth vs £16 in Bristol", "Only 15% of restaurants mark allergens clearly". Journalists benefit from exclusive access to interesting data. Plymouth Research benefits from media citations building reputation and driving consumer traffic.

**Driver Intensity**: **MEDIUM**

**Enablers**:
- Export functionality (CSV, JSON) for data analysis
- Historical data for trend analysis
- Accurate data that editors won't fact-check and reject
- API access for programmatic data retrieval (future)
- Timely responses to journalist data requests

**Blockers**:
- Inaccurate data damaging journalist's credibility
- No export functionality forcing manual data collection
- No historical data preventing trend analysis
- Slow or unreliable platform access
- Refusal to provide data or clarify methodology

**Related Stakeholders**:
- Research Director (media coverage amplifies reputation)
- Plymouth Consumers (journalist articles drive consumer awareness and traffic)
- Research Analysts (may collaborate on data analysis for articles)

---

### SD-8: Legal/Compliance Advisor - Mitigate Legal Exposure

**Stakeholder**: Legal/Compliance Advisor (External Consultant or Internal Role)

**Driver Category**: COMPLIANCE + RISK

**Driver Statement**:
Ensure Plymouth Research's web scraping activities comply with UK law (Computer Misuse Act 1990, Copyright Act 1988, GDPR), Terms of Service for scraped websites, and ethical norms to avoid legal action, regulatory fines, or reputational damage.

**Context & Background**:
The Legal/Compliance Advisor provides risk assessment and guidance on legal boundaries. Key concerns:
1. **Computer Misuse Act**: Scraping must not constitute "unauthorized access" (respect robots.txt, rate limits, ToS)
2. **Copyright Act**: Menu text may be copyrighted - only scrape factual data (prices, item names), not creative descriptions or images
3. **GDPR**: Only scrape public business data, no PII (customer reviews, personal contact info)
4. **Contract Law**: Website Terms of Service may prohibit scraping - assess enforceability and risk

The advisor's role is to document compliant practices, identify risks, and advise on risk mitigation (DPIA, opt-out mechanism, legal disclaimers).

**Driver Intensity**: **CRITICAL** (for legal stakeholder, though influence is advisory)

**Enablers**:
- Clear documentation of scraping practices for legal review
- Robots.txt and rate-limiting compliance built into scraper
- No PII collection (automated detection and filtering)
- Opt-out mechanism for restaurants
- Transparent data attribution and methodology
- DPIA completed and documented

**Blockers**:
- Aggressive or disrespectful scraping practices
- Collecting PII by mistake
- Ignoring robots.txt or ToS restrictions
- No documentation of legal analysis or risk assessment
- Republishing copyrighted creative content

**Related Stakeholders**:
- Research Director (receives legal advice and makes risk decisions)
- Data Engineer (implements technical compliance controls)
- ICO (regulator who enforces GDPR)

---

### SD-9: ICO (Information Commissioner's Office) - Data Protection Compliance

**Stakeholder**: ICO (UK Data Protection Regulator)

**Driver Category**: COMPLIANCE

**Driver Statement**:
Ensure all organizations processing personal data in the UK comply with GDPR and Data Protection Act 2018, protecting individual rights and imposing fines for violations.

**Context & Background**:
The ICO is the UK regulator for data protection. While Plymouth Research scrapes public business data (not personal data), the ICO has interest in:
1. Ensuring no PII is collected without legal basis
2. Verifying data subject rights are respected (if any personal data exists)
3. Confirming adequate security for any data stored
4. Checking transparency (privacy policy, data usage disclosure)

The ICO is a **low-interest, high-power** stakeholder - unlikely to proactively monitor this project, but could investigate if complaints arise. Compliance is about avoiding attention, not seeking approval.

**Driver Intensity**: **LOW** (for this specific project - public business data, not PII)

**Enablers**:
- DPIA demonstrating low privacy risk
- No PII collection (only public business data)
- Privacy policy and transparency about data use
- Security controls (encryption at rest and in transit)
- Documented data retention and deletion policies

**Blockers**:
- Collecting PII (customer reviews, personal contact info)
- No DPIA or privacy policy
- Data breach exposing scraped data
- Complaints from individuals about data processing

**Related Stakeholders**:
- Legal/Compliance Advisor (interprets ICO guidance)
- Research Director (accountable for GDPR compliance)

---

### SD-10: Operations/IT - Minimize Operational Burden and Costs

**Stakeholder**: Operations/IT (Internal Support Team)

**Driver Category**: OPERATIONAL + FINANCIAL

**Driver Statement**:
Deploy and maintain the platform with minimal manual intervention, keeping infrastructure costs low (<£100/month), and avoiding on-call incidents or complex troubleshooting.

**Context & Background**:
Operations/IT is responsible for deployment, monitoring, backups, and incident response. For a small research firm, this is likely one person or a part-time role. Key concerns:
1. **Cost**: Cloud bills must stay within budget (limited funding)
2. **Reliability**: Platform should "just work" without frequent outages
3. **Maintenance**: Automated deployments, monitoring, and backups reduce manual toil
4. **Simplicity**: Prefer managed services over self-hosted infrastructure (lower operational burden)

**Driver Intensity**: **HIGH**

**Enablers**:
- Infrastructure as Code (repeatable deployments)
- Managed services reducing maintenance (managed database, serverless hosting)
- Automated monitoring and alerting
- Clear runbooks for common issues
- Right-sized infrastructure (don't over-provision)
- Cost tracking and budget alerts

**Blockers**:
- Complex manual deployment processes
- No monitoring leading to undetected failures
- Over-provisioned infrastructure (high costs)
- Frequent scraper failures requiring manual intervention
- No documentation or runbooks

**Related Stakeholders**:
- Data Engineer (implements operational best practices)
- Research Director (sets budget constraints)

---

## Driver-to-Goal Mapping

### Goal G-1: Achieve 95% Data Quality Accuracy

**Derived From Drivers**: SD-1 (Establish Authority), SD-2 (Minimize Legal Risk), SD-4 (Analyst Access to Reliable Data), SD-5 (Consumer Dietary Needs), SD-6 (Restaurant Accurate Representation)

**Goal Owner**: Data Engineer (Technical Implementation) / Research Director (Accountability)

**Goal Statement**:
Achieve and maintain 95% accuracy in menu item extraction, price normalization, and dietary tagging by Q2 2026, measured through monthly manual validation sampling and automated data quality tests.

**Why This Matters**:
Data quality is the foundation of platform credibility. Inaccurate prices mislead consumers and damage trust. Incorrect dietary tags create safety risks (allergies). Poor extraction quality frustrates research analysts and undermines the Research Director's goal of establishing authority. Restaurants will opt-out or complain if misrepresented.

**Success Metrics**:
- **Primary Metric**: Data Quality Accuracy % = (Correct Extractions / Total Extractions) × 100
  - **Correct Extraction**: Menu item name, price, and primary category match manual verification
- **Secondary Metrics**:
  - Price Normalization Error Rate: <2% (prices incorrectly converted to decimal GBP)
  - Dietary Tag Accuracy: >90% (vegan/gluten-free tags match restaurant labeling)
  - Duplicate Detection Rate: >85% (same dish with different spellings merged)
  - Completeness: >95% (required fields populated: restaurant name, menu item, price)

**Baseline**:
Not yet measured (new platform). Expect 70-80% accuracy with basic scraping, improving to 95%+ with validation rules, normalization logic, and iterative refinement.

**Target**:
- **Month 1-2**: 75% accuracy (baseline scrapers)
- **Month 3-4**: 85% accuracy (validation rules added)
- **Month 5-6**: 95% accuracy (normalization logic refined)
- **Ongoing**: Maintain >95% accuracy

**Measurement Method**:
- **Manual Validation**: Monthly sample of 100 menu items (randomly selected) manually verified against source restaurant websites by Research Analyst
- **Automated Tests**: Data quality tests run on every ETL execution (price range validation, null checks, duplicate detection)
- **User Feedback**: Dashboard "Report Incorrect Data" feature (track user-reported errors)

**Dependencies**:
- Scraping logic implemented with extraction rules for each website structure
- Validation rules defined for prices (£0.50-£150 range), categories (controlled vocabulary), dietary tags (keyword extraction)
- Manual verification process established (Research Analyst time budgeted)
- Iterative improvement process (review failures monthly, refine extraction logic)

**Risks to Achievement**:
- **High Website Diversity**: 150 restaurants = 150 different website structures → extraction logic complex and brittle
- **Menu Inconsistency**: Restaurants use inconsistent formats (£12.50, £12.5, 12.50, "Twelve fifty") → normalization logic challenging
- **Dietary Tag Ambiguity**: Not all restaurants label allergens clearly → ML or keyword-based tagging may be inaccurate
- **Stale Data**: Menus change frequently → weekly refresh may still miss rapid changes
- **Resource Constraints**: Manual validation requires analyst time (10 hours/month)

---

### Goal G-2: Scrape 150+ Plymouth Restaurants Within 6 Months

**Derived From Drivers**: SD-1 (Establish Authority), SD-4 (Analyst Reliable Data), SD-5 (Consumer Dietary Needs), SD-7 (Journalist Data-Driven Reporting)

**Goal Owner**: Data Engineer (Implementation) / Research Director (Accountability)

**Goal Statement**:
Successfully scrape and maintain menu data for at least 150 restaurants in Plymouth by Month 6 (May 2026), covering diverse cuisines and price ranges, with weekly automated refresh and <10% scraping failure rate.

**Why This Matters**:
Comprehensive coverage is essential for platform value. Consumers searching for specific cuisines or dietary options need broad choice. Research analysts conducting market analysis need representative samples. Journalists writing trend stories need critical mass of data. 150 restaurants represent ~majority of Plymouth's dining scene, providing credible coverage.

**Success Metrics**:
- **Primary Metric**: Restaurant Count = 150+ restaurants with active, refreshed menu data
- **Secondary Metrics**:
  - Cuisine Diversity: >15 cuisine types represented (British, Italian, Chinese, Indian, Thai, Mediterranean, etc.)
  - Price Range Coverage: Balanced distribution across budget (£5-10), mid-range (£10-20), premium (£20+) average main course prices
  - Scraping Success Rate: >90% (successful scrapes per weekly refresh cycle)
  - Data Freshness: >95% of restaurants refreshed within last 7 days

**Baseline**:
0 restaurants (new platform)

**Target**:
- **Month 1**: 30 restaurants (pilot batch - validate scraping approach)
- **Month 2**: 60 restaurants (expand to major cuisines)
- **Month 3**: 90 restaurants (mid-range and budget establishments)
- **Month 4**: 120 restaurants (comprehensive Plymouth coverage)
- **Month 5**: 140 restaurants (premium and niche cuisines)
- **Month 6**: 150+ restaurants (target achieved, ongoing maintenance)

**Measurement Method**:
- **Database Count**: SELECT COUNT(DISTINCT restaurant_id) FROM restaurants WHERE last_scraped_at > NOW() - INTERVAL '7 days'
- **Cuisine Distribution**: SELECT cuisine_type, COUNT(*) FROM restaurants GROUP BY cuisine_type
- **Scraping Logs**: Automated scraper tracks success/failure per restaurant per week

**Dependencies**:
- Restaurant list compiled (web research, local directories, Google Maps)
- Scraping logic adaptable to different website structures (or manual fallback for difficult sites)
- Robots.txt compliance checked for each restaurant website (some may disallow scraping)
- Rate limiting infrastructure in place (5-second delays between requests)
- Storage capacity for 150 restaurants × ~50 menu items avg = 7,500+ menu items

**Risks to Achievement**:
- **Robots.txt Blocking**: Some restaurants may disallow scraping → reduces achievable count
- **Website Complexity**: Dynamic JavaScript-heavy sites difficult to scrape → requires Selenium (slower, more resource-intensive)
- **Manual Fallback Required**: Some sites too complex → manual data entry (not scalable)
- **Scraping Failures**: Website changes break scrapers → requires ongoing maintenance
- **Opt-Outs**: Some restaurants request removal → reduces final count

---

### Goal G-3: 100% Compliance with Ethical Scraping Principles

**Derived From Drivers**: SD-2 (Minimize Legal Risk), SD-6 (Restaurant Accurate Representation), SD-8 (Legal Compliance)

**Goal Owner**: Data Engineer (Implementation) / Legal/Compliance Advisor (Oversight)

**Goal Statement**:
Achieve and maintain 100% compliance with ethical scraping principles (robots.txt, rate limiting, User-Agent transparency, attribution, opt-out mechanism) throughout the project lifecycle, with zero violations logged or reported.

**Why This Matters**:
Ethical scraping is non-negotiable for legal compliance and long-term sustainability. Violating robots.txt or overloading servers creates legal risk (Computer Misuse Act), damages relationships with restaurants, and risks IP blocking or legal action. Compliance protects the Research Director from liability, satisfies legal advisor requirements, and maintains community goodwill.

**Success Metrics**:
- **Primary Metric**: Ethical Compliance Score = 100% (all scraping activities compliant)
- **Secondary Metrics**:
  - Robots.txt Compliance: 100% (zero disallowed paths scraped)
  - Rate Limiting Compliance: 100% (minimum 5-second delays logged for all requests)
  - User-Agent Transparency: 100% (all requests identify Plymouth Research with contact email)
  - Attribution: 100% (dashboard displays source website link for all menu data)
  - Opt-Out Response Time: 100% (requests processed within 48 hours)

**Baseline**:
Not yet measured (new platform). Expect 100% compliance from day 1 by building controls into scraper design.

**Target**:
100% compliance maintained continuously (no violations ever)

**Measurement Method**:
- **Automated Logging**: Scraper logs every request with timestamp, URL, robots.txt check result, rate-limit delay
- **Monthly Audit**: Legal/Compliance Advisor reviews random sample of scraping logs (50 requests/month)
- **Complaint Tracking**: Document any restaurant complaints or legal inquiries (target: zero)
- **Robots.txt Re-Check**: Automated daily check for robots.txt changes on all scraped domains

**Dependencies**:
- Robots.txt parser library integrated into scraper (validate before every request)
- Rate-limiting enforced at infrastructure layer (cannot be bypassed by code bugs)
- User-Agent string configured correctly and logged
- Dashboard attribution implemented (source URL displayed with menu items)
- Opt-out form published on platform website with clear instructions

**Risks to Achievement**:
- **Code Bugs**: Rate-limiting logic failure → accidental aggressive scraping
- **Robots.txt Changes**: Restaurant adds "Disallow: /menu" → scraper must detect and stop
- **User-Agent Misconfiguration**: Incorrect or missing User-Agent → appears deceptive
- **Attribution Omission**: Dashboard redesign accidentally removes source links
- **Opt-Out Process Failure**: Opt-out requests not monitored → delayed response

---

### Goal G-4: Achieve <500ms Dashboard Search Query Response Time

**Derived From Drivers**: SD-4 (Analyst Reliable Data), SD-5 (Consumer Dietary Needs), SD-7 (Journalist Data-Driven Reporting)

**Goal Owner**: Data Engineer (Implementation)

**Goal Statement**:
Achieve 95th percentile (p95) search query response time of <500ms for dashboard searches (by restaurant name, cuisine, dietary tags, price range) by Month 4 (March 2026), measured through application performance monitoring.

**Why This Matters**:
Users expect instant search results. Slow queries frustrate research analysts conducting analysis, consumers searching for restaurants, and journalists extracting data for articles. Sub-500ms response time feels "instant" and competitive with commercial platforms (Google, TripAdvisor). Performance directly impacts user satisfaction and adoption.

**Success Metrics**:
- **Primary Metric**: p95 Search Response Time <500ms (95% of queries return in under 500ms)
- **Secondary Metrics**:
  - p50 Response Time: <200ms (median query speed)
  - p99 Response Time: <1000ms (99% of queries under 1 second)
  - Search Availability: >99% (search feature operational, not throwing errors)
  - Concurrent User Capacity: 50+ simultaneous searches without degradation

**Baseline**:
Not yet measured (new platform). Expect slower initial performance (1-2 seconds) before optimization.

**Target**:
- **Month 1-2**: <2000ms (basic search implementation)
- **Month 3**: <1000ms (database indexing added)
- **Month 4**: <500ms (caching and optimization)
- **Ongoing**: Maintain <500ms as data grows

**Measurement Method**:
- **Application Performance Monitoring (APM)**: Instrument dashboard with response time tracking (e.g., Prometheus, Grafana)
- **Synthetic Monitoring**: Automated test queries run hourly measuring response time
- **Real User Monitoring (RUM)**: Track actual user query times in production dashboard

**Dependencies**:
- Database indexing on commonly queried fields (restaurant name, cuisine, dietary tags, price)
- Caching layer for popular queries (e.g., "vegan restaurants Plymouth")
- Optimized database schema (normalized, no N+1 query anti-patterns)
- Adequate server resources (CPU, memory) to handle concurrent queries

**Risks to Achievement**:
- **Database Not Indexed**: Full table scans on large datasets → slow queries (seconds)
- **Complex Query Logic**: Filtering by multiple criteria (cuisine + dietary + price) → inefficient joins
- **No Caching**: Every query hits database → unnecessary load and latency
- **Data Growth**: 10,000+ menu items without optimization → performance degrades over time
- **Concurrent Load**: Multiple users querying simultaneously → resource contention

---

### Goal G-5: Maintain Operational Costs <£100/Month

**Derived From Drivers**: SD-1 (Establish Authority - sustainability), SD-10 (Operations Minimize Costs)

**Goal Owner**: Operations/IT (Budget Management) / Research Director (Approval)

**Goal Statement**:
Maintain total monthly operational costs (infrastructure, hosting, data storage, monitoring) below £100/month by Month 6 (May 2026) and ongoing, enabling long-term sustainability for independent research firm.

**Why This Matters**:
Plymouth Research has limited budget. High operational costs require external funding, subscriptions, or advertising - complicating the mission and potentially compromising independence. Cost efficiency enables long-term sustainability, aligns with "open source preferred" principle (reducing licensing fees), and proves the viability of data-driven research for small organizations.

**Success Metrics**:
- **Primary Metric**: Total Monthly Cost <£100 (sum of all infrastructure and service costs)
- **Secondary Metrics**:
  - Cost Per Restaurant: <£0.67/month (£100 ÷ 150 restaurants)
  - Cost Per Query: <£0.01 (assuming 10,000 queries/month)
  - Storage Cost Efficiency: <£10/month for database and file storage
  - Compute Cost Efficiency: <£60/month for scraping and dashboard hosting
  - Monitoring/Tooling Cost: <£30/month (free tiers preferred)

**Baseline**:
£0 (no infrastructure yet)

**Target**:
- **Month 1-3**: <£150/month (initial setup, may be higher during development)
- **Month 4-6**: <£100/month (optimized, production-level costs)
- **Ongoing**: Maintain <£100/month as data and usage grow

**Measurement Method**:
- **Monthly Cost Tracking**: Sum all invoices from cloud providers, hosting, domain registration, monitoring services
- **Cost Allocation**: Tag resources by category (database, compute, storage, monitoring) to identify cost drivers
- **Budget Alerts**: Set up alerts if monthly costs exceed £80 (early warning at 80% of budget)

**Dependencies**:
- Open source software (no licensing fees for Postgres, Python, Streamlit/Dash)
- Managed services with free tiers or low-cost options (e.g., DigitalOcean, Heroku, Render)
- Right-sized infrastructure (don't over-provision CPU/memory)
- Efficient scraping (batch jobs on spot instances or serverless functions)
- Storage optimization (compress historical data, delete unnecessary files)

**Risks to Achievement**:
- **Cloud Cost Creep**: Unoptimized queries, always-on VMs, uncompressed storage → costs grow
- **Traffic Growth**: Viral adoption (10x user growth) → need to scale infrastructure → higher costs
- **Proprietary Services**: Accidentally depend on paid services (monitoring, analytics) beyond free tiers
- **Data Storage Growth**: 12 months of historical data accumulates → storage costs rise
- **Lack of Cost Monitoring**: Don't notice costs increasing until too late

---

### Goal G-6: Launch Public Dashboard by Month 4 (March 2026)

**Derived From Drivers**: SD-1 (Establish Authority), SD-4 (Analyst Data Access), SD-5 (Consumer Dietary Needs), SD-7 (Journalist Reporting)

**Goal Owner**: Data Engineer (Implementation) / Research Director (Launch Decision)

**Goal Statement**:
Launch public-facing, fully functional dashboard by Month 4 (March 2026) with search, filtering, export, and attribution features operational, enabling consumer and analyst access to Plymouth restaurant menu data.

**Why This Matters**:
The dashboard is the primary user interface for all external stakeholders (consumers, journalists, analysts). Launch date determines when platform value materializes - when consumers can search, analysts can export, journalists can cite. Delayed launch postpones all downstream benefits (reputation building, user adoption, media coverage). March 2026 target balances quality (4 months development) with timely delivery.

**Success Metrics**:
- **Primary Metric**: Dashboard Launch Date = March 31, 2026 or earlier
- **Secondary Metrics**:
  - Feature Completeness: 100% of MVP features operational (search, filter, export, attribution)
  - User Acceptance Testing: >90% of test scenarios passed
  - Performance: Search <500ms (per Goal G-4)
  - Data Coverage: >120 restaurants (80% of Goal G-2 target by launch)
  - Zero Critical Bugs: No blocking issues at launch

**Baseline**:
Not yet launched (Month 0)

**Target**:
- **Month 1**: Dashboard prototype (basic search on sample data)
- **Month 2**: Alpha dashboard (core features, internal testing)
- **Month 3**: Beta dashboard (full features, user acceptance testing with 10 beta users)
- **Month 4**: Public launch (March 2026)

**Measurement Method**:
- **Launch Readiness Checklist**: Pre-launch checklist (features complete, performance validated, data quality >90%, legal review complete)
- **UAT Results**: User Acceptance Testing with 10 beta users (research analysts, friendly consumers)
- **Launch Date**: Publicly announce dashboard availability on Plymouth Research website and social media

**Dependencies**:
- Data Engineer availability (4 months development time)
- Dashboard technology selected (Streamlit or Dash - per Goal G-8 technology research)
- Scraping pipeline operational (feeding data into database)
- Database schema stable (no major changes during dashboard development)
- Hosting infrastructure provisioned (per Goal G-5 cost constraints)
- Legal review complete (DPIA, opt-out mechanism, privacy policy published)

**Risks to Achievement**:
- **Scope Creep**: Adding "nice-to-have" features delays MVP launch
- **Technical Complexity**: Underestimated dashboard development effort
- **Data Quality Issues**: Scraping failures delay having sufficient data for launch
- **UAT Failures**: Beta testing reveals critical bugs requiring rework
- **Legal Blockers**: Legal review identifies compliance gaps requiring remediation before launch

---

### Goal G-7: Achieve 1,000+ Monthly Searches by Month 9 (June 2026)

**Derived From Drivers**: SD-1 (Establish Authority), SD-5 (Consumer Dietary Needs), SD-7 (Journalist Reporting)

**Goal Owner**: Research Director (Adoption & Marketing)

**Goal Statement**:
Achieve 1,000+ unique searches per month on the dashboard by Month 9 (June 2026), demonstrating user adoption, validating market need, and establishing Plymouth Research as go-to resource for restaurant menu data.

**Why This Matters**:
User adoption validates the platform's value proposition and justifies the investment. 1,000 monthly searches indicate meaningful usage by consumers, analysts, and journalists - not just curiosity traffic. Adoption supports the Research Director's goal of establishing authority and creates opportunities for future monetization, partnerships, or expansion. Low adoption suggests the platform doesn't meet a real need or has usability issues.

**Success Metrics**:
- **Primary Metric**: Monthly Unique Searches ≥1,000 (distinct search queries executed)
- **Secondary Metrics**:
  - Monthly Active Users (MAU): >500 unique visitors
  - Average Searches Per User: ~2 searches/session
  - Organic Traffic: >70% (users finding platform via Google search, word-of-mouth, not paid ads)
  - Return Visitor Rate: >30% (users coming back multiple times)
  - Data Export Usage: >100 CSV downloads/month (analysts and journalists using data)

**Baseline**:
0 searches (pre-launch)

**Target**:
- **Month 4 (Launch)**: 50 searches (beta testers, internal users)
- **Month 5**: 200 searches (early adopters, word-of-mouth)
- **Month 6**: 400 searches (local SEO kicking in)
- **Month 7**: 600 searches (media coverage driving traffic)
- **Month 8**: 800 searches (growth continues)
- **Month 9**: 1,000+ searches (target achieved)

**Measurement Method**:
- **Web Analytics**: Google Analytics or privacy-respecting alternative (Plausible, Matomo) tracking search queries
- **Dashboard Logs**: Application logs count search API requests (backup to analytics)
- **User Surveys**: Optional feedback form asking "How did you hear about us?" (measure channels)

**Dependencies**:
- Dashboard launched and publicly accessible (Goal G-6)
- Search functionality working reliably (Goal G-4 performance)
- Data coverage sufficient to answer user queries (Goal G-2 restaurant count)
- Basic SEO implemented (meta tags, sitemap, Google Search Console)
- Word-of-mouth promotion (social media posts, local community groups)
- Media coverage (press release to local news, food bloggers)

**Risks to Achievement**:
- **Low Awareness**: Users don't know platform exists → need marketing/PR
- **Poor Usability**: Dashboard confusing or slow → users leave without searching
- **Insufficient Data**: Users search for restaurants not yet in database → frustrated, don't return
- **Competition**: Commercial platforms (TripAdvisor, Google) dominate search results
- **No Unique Value**: Platform doesn't offer compelling advantage over existing solutions

---

### Goal G-8: Complete Technology Research & Architecture Design by Month 1

**Derived From Drivers**: SD-1 (Establish Authority), SD-2 (Minimize Legal Risk), SD-3 (Maintainable Technical Solution), SD-8 (Legal Compliance)

**Goal Owner**: Data Engineer (Research & Design) / Research Director (Approval)

**Goal Statement**:
Complete technology research ("build vs buy vs open source" analysis) and architecture design documentation (ADRs, data model, deployment architecture) by Month 1 (January 2026), aligning with architecture principles and providing clear implementation roadmap.

**Why This Matters**:
Upfront architecture planning reduces technical debt, ensures alignment with principles (data quality first, open source preferred, ethical scraping), and provides clear direction for implementation. Rushing into coding without design leads to rework, principle violations, and maintenance nightmares. The Data Engineer's goal of maintainability depends on thoughtful architecture. Legal compliance (SD-2, SD-8) requires documented decisions on data handling, retention, security.

**Success Metrics**:
- **Primary Metric**: Architecture Documentation Complete by Jan 31, 2026
- **Secondary Metrics**:
  - Technology Research: Build vs buy vs open source analysis documented for scraping framework, database, dashboard, hosting
  - Architecture Decision Records (ADRs): ≥5 ADRs documenting key choices (scraping approach, database schema, dashboard framework, deployment model, data retention)
  - Data Model: ER diagram and schema documented (Restaurants, MenuItems, Categories, DietaryTags)
  - Deployment Architecture: Infrastructure diagram showing components, data flows, security boundaries
  - DPIA (Data Protection Impact Assessment): Completed and reviewed by legal advisor

**Baseline**:
No architecture documentation (Month 0)

**Target**:
Month 1 deliverables:
1. Technology Research Report (comparing options, recommending choices aligned with principles)
2. 5+ ADRs (scraping framework, database, dashboard, deployment, data retention)
3. Data Model (ER diagram, schema DDL)
4. Deployment Architecture Diagram (components, data flows)
5. DPIA (privacy/GDPR compliance assessment)

**Measurement Method**:
- **Document Checklist**: Confirm each artifact exists and is reviewed/approved
- **Principles Compliance Review**: Validate architecture aligns with 18 principles (see `/arckit.principles-compliance` later)
- **Legal Review**: Legal/Compliance Advisor reviews DPIA and architecture for compliance

**Dependencies**:
- Architecture principles defined (already complete - see `.arckit/memory/architecture-principles.md`)
- Data Engineer time allocated for research (estimate 2 weeks full-time equivalent)
- Legal/Compliance Advisor available for DPIA review
- Research Director available for ADR approval

**Risks to Achievement**:
- **Analysis Paralysis**: Over-researching technology options, delaying decisions
- **Rushed Architecture**: Pressure to start coding leads to skipping documentation
- **Legal Review Delays**: Legal advisor unavailable or slow to review DPIA
- **Scope Creep**: Trying to document every detail rather than focusing on key decisions

---

## Goal-to-Outcome Mapping

### Outcome O-1: Plymouth Research Recognized as Authoritative Local Data Source

**Supported Goals**: G-1 (Data Quality), G-2 (Restaurant Coverage), G-6 (Dashboard Launch), G-7 (User Adoption)

**Outcome Statement**:
Plymouth Research is cited as the authoritative source for restaurant menu data in at least 10 media articles (local news, food blogs, academic papers) and achieves 1,000+ monthly searches by Month 12 (September 2026), demonstrating reputation and user trust.

**Measurement Details**:
- **KPI 1: Media Citations**
  - Current Value: 0 (pre-launch)
  - Target Value: ≥10 citations by Month 12
  - Measurement Frequency: Monthly tracking via Google Alerts, manual search
  - Data Source: Media monitoring (Google News, local news websites, food blogs)
  - Report Owner: Research Director

- **KPI 2: Monthly Searches**
  - Current Value: 0 (pre-launch)
  - Target Value: 1,000+ by Month 9 (per Goal G-7)
  - Measurement Frequency: Monthly via web analytics
  - Data Source: Google Analytics / Plausible
  - Report Owner: Research Director

- **KPI 3: User Trust Score (Qualitative)**
  - Target: >4.0/5.0 average rating on user feedback surveys
  - Measurement: Quarterly user survey (optional feedback form)

**Business Value**:
- **Strategic Impact**:
  - Establishes Plymouth Research brand and credibility in data-driven market research
  - Creates foundation for expansion to other cities or data domains
  - Positions organization for partnerships (tourism board, local government, industry associations)
  - Attracts future clients for consulting or custom data analysis

- **Operational Impact**:
  - Demonstrates viability of web scraping as research methodology
  - Builds organizational capability in data engineering and web analytics
  - Creates reusable platform for future research initiatives

- **Customer Impact**:
  - Provides public good (free access to restaurant menu data)
  - Improves food discovery and accessibility for Plymouth residents and visitors
  - Supports dietary inclusivity (vegan, gluten-free, allergen searching)

**Timeline**:
- **Phase 1 (Months 1-4)**: Platform development, no public visibility
  - Early Indicator: Architecture documentation complete (Month 1)
  - Early Indicator: 30 restaurants scraped (Month 1)

- **Phase 2 (Months 4-6)**: Dashboard launch, initial adoption
  - Early Indicator: Dashboard launched (Month 4)
  - Early Indicator: First media mention (local tech news covers launch)
  - Target: 1-2 media citations

- **Phase 3 (Months 7-9)**: Growth and recognition
  - Early Indicator: 500+ monthly searches (Month 6)
  - Early Indicator: Food writer requests data export (journalists using platform)
  - Target: 5+ media citations
  - Target: 1,000+ monthly searches (Month 9)

- **Phase 4 (Months 10-12)**: Established authority
  - Lagging Indicator: 10+ media citations accumulated
  - Lagging Indicator: Academic citation (researcher uses data in study)
  - Lagging Indicator: Partnership inquiry (tourism board or council contacts Plymouth Research)

**Stakeholder Benefits**:
- **Research Director**: Career advancement, organizational reputation, potential for future funding/clients
- **Plymouth Consumers**: Trusted resource for restaurant discovery and dietary needs
- **Food Writers/Journalists**: Credible data source to cite in articles, exclusive insights
- **Research Analysts**: Professional pride in building recognized platform, skill development

**Leading Indicators** (early signals of success):
- Dashboard launch on schedule (Month 4)
- First 100 searches within 2 weeks of launch
- First media mention within 1 month of launch
- Positive user feedback in surveys (>4.0/5.0)
- Social media shares and discussions mentioning platform

**Lagging Indicators** (final proof of success):
- 10+ media citations by Month 12
- 1,000+ monthly searches sustained over 3 consecutive months
- Return visitor rate >30% (users come back repeatedly)
- Inbound partnership inquiries (tourism board, council, industry groups)
- Academic or industry research citing Plymouth Research data

---

### Outcome O-2: Zero Legal or Regulatory Violations

**Supported Goals**: G-3 (Ethical Scraping Compliance), G-8 (Architecture Design with DPIA)

**Outcome Statement**:
Zero legal complaints, cease-and-desist letters, ICO investigations, or regulatory fines related to web scraping, data protection, or copyright throughout project lifecycle (Months 1-12 and ongoing), demonstrating compliance with UK law and ethical standards.

**Measurement Details**:
- **KPI 1: Legal Incidents**
  - Current Value: 0 (pre-launch)
  - Target Value: 0 (maintain zero)
  - Measurement Frequency: Continuous monitoring, monthly reporting
  - Data Source: Legal correspondence tracking, complaint inbox
  - Report Owner: Research Director / Legal Advisor

- **KPI 2: Robots.txt Compliance**
  - Target: 100% (zero violations logged)
  - Measurement Frequency: Continuous logging, monthly audit
  - Data Source: Scraper logs

- **KPI 3: Opt-Out Requests**
  - Target: <5% of restaurants request opt-out (indicates community acceptance)
  - Measurement Frequency: Monthly tracking
  - Data Source: Opt-out form submissions

- **KPI 4: DPIA Completion**
  - Target: DPIA completed and approved by Month 1
  - Data Source: Legal review documentation

**Business Value**:
- **Risk Mitigation**:
  - Avoids ICO fines (up to £17.5M or 4% of turnover under GDPR - would bankrupt small firm)
  - Prevents legal costs defending lawsuits
  - Protects Research Director's career and organization's reputation

- **Strategic Impact**:
  - Ethical reputation enables partnerships with public sector (council, tourism)
  - Compliance demonstrates professionalism to potential clients or funders
  - Sets precedent for responsible web scraping in research context

- **Operational Impact**:
  - Avoids disruption from legal disputes or regulatory investigations
  - Maintains access to data sources (not blocked by restaurants)
  - Preserves team focus on product development vs legal battles

**Timeline**:
- **Phase 1 (Month 1)**: Compliance foundation
  - DPIA completed and legal review passed
  - Robots.txt compliance built into scraper
  - Opt-out mechanism designed and tested

- **Phase 2 (Months 2-6)**: Active scraping, ongoing compliance
  - Monthly compliance audits (50 requests sampled)
  - Zero robots.txt violations logged
  - Opt-out requests processed within 48 hours

- **Phase 3 (Months 7-12)**: Sustained compliance
  - Quarterly legal review meetings
  - Zero complaints or legal inquiries received
  - <5% restaurant opt-out rate maintained

- **Sustainment (Year 2+)**: Continuous compliance
  - Annual DPIA refresh
  - Ongoing monitoring and audits

**Stakeholder Benefits**:
- **Research Director**: Peace of mind, career protection, organizational stability
- **Legal/Compliance Advisor**: Demonstrates due diligence and risk management effectiveness
- **Restaurant Owners**: Respectful scraping practices maintain trust and cooperation
- **ICO**: No complaints requiring investigation (efficient regulatory oversight)

**Leading Indicators** (early signals of success):
- DPIA completed with no critical issues identified (Month 1)
- First 1,000 scraping requests show 100% robots.txt compliance
- Opt-out mechanism tested and operational before launch
- Legal advisor signs off on scraping practices

**Lagging Indicators** (final proof of success):
- Zero legal complaints or cease-and-desist letters received by Month 12
- Zero ICO investigations or fines
- <5% restaurant opt-out rate (community acceptance)
- No IP blocks or technical countermeasures from restaurant websites

---

### Outcome O-3: Operational Sustainability Achieved

**Supported Goals**: G-5 (Cost <£100/month), G-4 (Performance <500ms), G-1 (Data Quality 95%)

**Outcome Statement**:
Platform operates sustainably with monthly costs <£100, search performance <500ms, and data quality >95% maintained for 6+ consecutive months (Months 7-12), demonstrating technical and financial viability for long-term operation.

**Measurement Details**:
- **KPI 1: Monthly Operational Cost**
  - Current Value: £0 (pre-launch)
  - Target Value: <£100/month sustained
  - Measurement Frequency: Monthly invoice tracking
  - Data Source: Cloud provider bills, hosting invoices
  - Report Owner: Operations/IT

- **KPI 2: Search Performance (p95 Response Time)**
  - Target: <500ms sustained
  - Measurement Frequency: Continuous monitoring, weekly review
  - Data Source: APM dashboard (Prometheus/Grafana)

- **KPI 3: Data Quality Accuracy**
  - Target: >95% sustained
  - Measurement Frequency: Monthly manual validation
  - Data Source: QA sampling by Research Analyst

- **KPI 4: Uptime**
  - Target: >99% (dashboard available)
  - Measurement Frequency: Continuous monitoring
  - Data Source: Uptime monitoring (UptimeRobot or similar)

**Business Value**:
- **Financial Impact**:
  - Low operational costs enable indefinite operation without external funding
  - £1,200/year budget (£100/month × 12) is affordable for small research firm
  - Proves viability of data platform for resource-constrained organizations

- **Strategic Impact**:
  - Sustainability enables long-term authority building (not a one-year flash-in-the-pan)
  - Operational success creates template for expansion (other cities, other data domains)
  - Demonstrates open source approach viability (no licensing costs)

- **Operational Impact**:
  - Reliable performance maintains user trust and satisfaction
  - Automated operations reduce manual maintenance burden
  - Cost predictability enables budgeting and planning

**Timeline**:
- **Phase 1 (Months 1-4)**: Development and optimization
  - Month 1-3: Costs may be higher during setup (£150/month acceptable)
  - Month 4: Launch with performance <1000ms (acceptable initially)

- **Phase 2 (Months 4-6)**: Stabilization
  - Month 4-6: Optimize costs to <£100/month
  - Month 4-6: Improve performance to <500ms
  - Month 4-6: Achieve data quality >90%, trending to 95%

- **Phase 3 (Months 7-12)**: Sustained operations
  - Costs maintained <£100/month for 6 consecutive months
  - Performance <500ms sustained
  - Data quality >95% sustained
  - **Outcome achieved**: Operational sustainability proven

**Stakeholder Benefits**:
- **Research Director**: Confidence in long-term viability, no funding crisis
- **Operations/IT**: Manageable workload, no cost surprises or performance fires
- **Data Engineer**: Pride in well-architected system, no on-call nightmares
- **All Users**: Reliable, fast platform they can depend on

**Leading Indicators** (early signals of success):
- Month 1: Architecture optimized for cost efficiency (managed services, right-sizing)
- Month 2: First full month under £150 budget
- Month 4: Performance improvements show progress toward <500ms target
- Month 4: Database indexing improves query speed measurably

**Lagging Indicators** (final proof of success):
- Months 7-12: Costs <£100/month for 6 consecutive months
- Months 7-12: Performance <500ms p95 sustained
- Months 7-12: Data quality >95% in monthly validations
- Month 12: Uptime >99% for full year

---

### Outcome O-4: User Satisfaction and Adoption Targets Met

**Supported Goals**: G-6 (Dashboard Launch), G-7 (1,000+ Monthly Searches)

**Outcome Statement**:
Dashboard achieves 1,000+ monthly searches and >4.0/5.0 user satisfaction rating by Month 9 (June 2026), with 70%+ organic traffic and 30%+ return visitors, demonstrating product-market fit and user value.

**Measurement Details**:
- **KPI 1: Monthly Unique Searches**
  - Current Value: 0 (pre-launch)
  - Target Value: 1,000+ by Month 9
  - Measurement Frequency: Monthly via analytics
  - Data Source: Google Analytics / Plausible

- **KPI 2: User Satisfaction Score**
  - Target: >4.0/5.0 average rating
  - Measurement Frequency: Quarterly user survey
  - Data Source: Optional feedback form on dashboard

- **KPI 3: Organic Traffic %**
  - Target: >70% (non-paid acquisition)
  - Measurement Frequency: Monthly via analytics
  - Data Source: Referral tracking (Google Search, direct, social)

- **KPI 4: Return Visitor Rate**
  - Target: >30% (users come back)
  - Measurement Frequency: Monthly via analytics
  - Data Source: Cookie-based or privacy-respecting visitor tracking

**Business Value**:
- **Customer Impact**:
  - 1,000+ searches = meaningful usage, not just curiosity
  - High satisfaction = platform meets real needs
  - Return visitors = sticky product providing ongoing value

- **Strategic Impact**:
  - Product-market fit validated (users find value and return)
  - Word-of-mouth growth (70%+ organic traffic shows virality)
  - Foundation for future monetization or partnerships

- **Operational Impact**:
  - User feedback guides iterative improvements
  - Organic growth reduces marketing costs
  - Return visitors create network effects (recommendations to others)

**Timeline**:
- **Phase 1 (Month 4)**: Launch and early adoption
  - Early Indicator: 50 searches in first week post-launch
  - Early Indicator: First positive feedback received

- **Phase 2 (Months 5-6)**: Growth
  - 200-400 searches/month
  - First user survey (satisfaction baseline)
  - SEO improvements driving organic traffic

- **Phase 3 (Months 7-9)**: Target achievement
  - 600-1,000 searches/month progression
  - User satisfaction >4.0/5.0
  - **Outcome achieved**: Month 9 targets met

- **Phase 4 (Months 10-12)**: Sustained growth
  - Maintain 1,000+ searches/month
  - Improve satisfaction further (toward 4.5/5.0)
  - Explore feature expansion based on user feedback

**Stakeholder Benefits**:
- **Plymouth Consumers**: Valuable tool for restaurant discovery saves time and improves dining choices
- **Research Analysts**: Validated that their work creates public value and user satisfaction
- **Food Writers/Journalists**: Engaged user base creates audience for data-driven stories citing platform
- **Research Director**: User adoption validates strategic vision and investment

**Leading Indicators** (early signals of success):
- Dashboard usability testing shows 90%+ task completion (pre-launch)
- First 100 searches happen within 2 weeks of launch
- User feedback is positive (>80% of comments are favorable)
- Social media shares and mentions increase weekly

**Lagging Indicators** (final proof of success):
- 1,000+ monthly searches sustained for 3+ months
- User satisfaction >4.0/5.0 in surveys
- 70%+ organic traffic (word-of-mouth and SEO working)
- 30%+ return visitor rate (users come back repeatedly)

---

## Complete Traceability Matrix

### Stakeholder → Driver → Goal → Outcome

| Stakeholder | Driver ID | Driver Summary | Goal ID | Goal Summary | Outcome ID | Outcome Summary |
|-------------|-----------|----------------|---------|--------------|------------|-----------------|
| Research Director | SD-1 | Establish Authority | G-1 | 95% Data Quality | O-1 | Recognized as Authoritative Source |
| Research Director | SD-1 | Establish Authority | G-2 | 150+ Restaurants | O-1 | Recognized as Authoritative Source |
| Research Director | SD-1 | Establish Authority | G-6 | Launch Dashboard Month 4 | O-1 | Recognized as Authoritative Source |
| Research Director | SD-1 | Establish Authority | G-7 | 1,000+ Monthly Searches | O-1 | Recognized as Authoritative Source |
| Research Director | SD-1 | Establish Authority | G-7 | 1,000+ Monthly Searches | O-4 | User Satisfaction & Adoption |
| Research Director | SD-2 | Minimize Legal Risk | G-3 | 100% Ethical Compliance | O-2 | Zero Legal Violations |
| Research Director | SD-2 | Minimize Legal Risk | G-8 | Architecture & DPIA Month 1 | O-2 | Zero Legal Violations |
| Data Engineer | SD-3 | Maintainable Technical Solution | G-1 | 95% Data Quality | O-3 | Operational Sustainability |
| Data Engineer | SD-3 | Maintainable Technical Solution | G-4 | <500ms Performance | O-3 | Operational Sustainability |
| Data Engineer | SD-3 | Maintainable Technical Solution | G-8 | Architecture Design Month 1 | O-3 | Operational Sustainability |
| Research Analysts | SD-4 | Access Reliable Data | G-1 | 95% Data Quality | O-1 | Recognized as Authoritative Source |
| Research Analysts | SD-4 | Access Reliable Data | G-2 | 150+ Restaurants | O-1 | Recognized as Authoritative Source |
| Research Analysts | SD-4 | Access Reliable Data | G-4 | <500ms Performance | O-3 | Operational Sustainability |
| Plymouth Consumers | SD-5 | Find Restaurants by Dietary Needs | G-1 | 95% Data Quality | O-1 | Recognized as Authoritative Source |
| Plymouth Consumers | SD-5 | Find Restaurants by Dietary Needs | G-2 | 150+ Restaurants | O-4 | User Satisfaction & Adoption |
| Plymouth Consumers | SD-5 | Find Restaurants by Dietary Needs | G-4 | <500ms Performance | O-4 | User Satisfaction & Adoption |
| Plymouth Consumers | SD-5 | Find Restaurants by Dietary Needs | G-6 | Launch Dashboard Month 4 | O-4 | User Satisfaction & Adoption |
| Plymouth Consumers | SD-5 | Find Restaurants by Dietary Needs | G-7 | 1,000+ Monthly Searches | O-4 | User Satisfaction & Adoption |
| Restaurant Owners | SD-6 | Accurate Representation | G-1 | 95% Data Quality | O-2 | Zero Legal Violations |
| Restaurant Owners | SD-6 | Accurate Representation | G-3 | 100% Ethical Compliance | O-2 | Zero Legal Violations |
| Food Writers/Journalists | SD-7 | Data-Driven Reporting | G-2 | 150+ Restaurants | O-1 | Recognized as Authoritative Source |
| Food Writers/Journalists | SD-7 | Data-Driven Reporting | G-4 | <500ms Performance | O-1 | Recognized as Authoritative Source |
| Food Writers/Journalists | SD-7 | Data-Driven Reporting | G-6 | Launch Dashboard Month 4 | O-1 | Recognized as Authoritative Source |
| Legal/Compliance Advisor | SD-8 | Mitigate Legal Exposure | G-3 | 100% Ethical Compliance | O-2 | Zero Legal Violations |
| Legal/Compliance Advisor | SD-8 | Mitigate Legal Exposure | G-8 | Architecture & DPIA Month 1 | O-2 | Zero Legal Violations |
| ICO (Regulator) | SD-9 | Data Protection Compliance | G-3 | 100% Ethical Compliance | O-2 | Zero Legal Violations |
| ICO (Regulator) | SD-9 | Data Protection Compliance | G-8 | Architecture & DPIA Month 1 | O-2 | Zero Legal Violations |
| Operations/IT | SD-10 | Minimize Costs & Burden | G-5 | Costs <£100/month | O-3 | Operational Sustainability |
| Operations/IT | SD-10 | Minimize Costs & Burden | G-4 | <500ms Performance | O-3 | Operational Sustainability |

### Conflict Analysis

**Competing Drivers**:

**Conflict 1: Comprehensive Coverage vs. Cost Constraints**
- **Stakeholders**: Research Director (SD-1: wants 150+ restaurants for authority) vs. Operations/IT (SD-10: wants costs <£100/month)
- **Tension**: More restaurants = more scraping compute, more storage, potentially higher costs. 150 restaurants may push costs above £100/month if not optimized.
- **Resolution Strategy**:
  - **Phased Approach**: Start with 30-60 restaurants (Month 1-2) to validate costs. Scale to 150 only if costs stay within budget.
  - **Technical Optimization**: Use serverless scraping (pay per scrape, not always-on VMs), compress historical data, optimize database to keep costs low.
  - **Prioritization**: Focus on most popular/diverse restaurants first. If costs constrain, maintain 100-120 high-value restaurants rather than forcing 150.
  - **Monitoring**: Track cost per restaurant monthly. If exceeds £0.67/restaurant, investigate and optimize before adding more.

**Conflict 2: Real-Time Data vs. Ethical Rate Limiting**
- **Stakeholders**: Plymouth Consumers (SD-5: want up-to-date menus) vs. Restaurant Owners (SD-6: want respectful scraping, not overloaded servers)
- **Tension**: Consumers prefer real-time or daily data. But frequent scraping (daily) increases load on restaurant websites. Ethical scraping requires weekly refresh (balance freshness vs. burden).
- **Resolution Strategy**:
  - **Weekly Refresh Cycle**: Default to weekly scraping (standard, respectful frequency). Communicate to users: "Data refreshed weekly - last updated [date]".
  - **Manual On-Demand Updates**: Allow users to "request refresh" for specific restaurant (rate-limited to 1 request/restaurant/day). This gives users control without overwhelming sites.
  - **Stale Data Warnings**: Flag restaurants not refreshed in >10 days with "Data may be outdated" warning. Set user expectations proactively.
  - **Restaurant Partnerships**: Explore partnerships where restaurants opt-in to daily scraping or provide API access (future enhancement).

**Conflict 3: Speed of Delivery vs. Data Quality**
- **Stakeholders**: Research Director (SD-1: wants timely launch to build authority) vs. Data Engineer (SD-3: wants quality implementation) and Research Analysts (SD-4: need reliable data)
- **Tension**: Pressure to launch quickly (Month 4) may compromise data quality or technical quality. Rushed launch with poor data damages reputation (worse than delayed launch).
- **Resolution Strategy**:
  - **MVP Scope Definition**: Launch with core features only (search, filter, export, 120+ restaurants, 90%+ data quality). Defer nice-to-haves (advanced analytics, mobile app).
  - **Quality Gates**: Non-negotiable quality thresholds: 90%+ data quality, <1000ms performance, zero critical bugs before launch.
  - **Beta Testing**: Month 3 beta testing with 10 users catches quality issues before public launch.
  - **Iterative Improvement**: Accept that Month 4 launch will be "good enough" (90% data quality), then iterate to 95%+ by Month 6. Communicate "continuous improvement" approach to stakeholders.

**Synergies**:

**Synergy 1: Data Quality Benefits All**
- **Stakeholders**: Research Director (SD-1), Research Analysts (SD-4), Plymouth Consumers (SD-5), Restaurant Owners (SD-6), Food Writers (SD-7)
- **Alignment**: Everyone benefits from accurate data. Inaccurate data harms all stakeholders (damaged reputation, unreliable analysis, misleading consumers, restaurant complaints, journalist credibility loss).
- **Opportunity**: Invest heavily in data quality (Goal G-1) - this is a high-leverage, high-alignment goal. Automated validation, manual QA sampling, iterative refinement all have broad stakeholder support.

**Synergy 2: Ethical Scraping Protects Sustainability**
- **Stakeholders**: Research Director (SD-2: avoid legal risk), Legal Advisor (SD-8: compliance), Restaurant Owners (SD-6: respectful treatment), ICO (SD-9: data protection)
- **Alignment**: Ethical scraping satisfies legal, regulatory, and relationship concerns simultaneously. 100% compliance (Goal G-3) is non-negotiable and universally supported.
- **Opportunity**: Make ethical scraping a differentiator and competitive advantage. Publicize compliance (DPIA published, opt-out mechanism prominent) to build trust with restaurants and regulators. Turn compliance into a reputation asset.

**Synergy 3: User Adoption Validates All Internal Stakeholders**
- **Stakeholders**: Research Director (SD-1: authority), Research Analysts (SD-4: useful tool), Data Engineer (SD-3: pride in quality work)
- **Alignment**: 1,000+ monthly searches (Goal G-7) validates that Research Director's vision was correct, Analysts have a useful tool, and Engineer built something people value. User adoption is a shared success metric.
- **Opportunity**: Celebrate milestones together (100 searches, 500 searches, 1,000 searches). Use adoption metrics in team meetings to reinforce shared purpose and progress.

---

## Communication & Engagement Plan

### Stakeholder-Specific Messaging

#### Research Director (Executive Sponsor)

**Primary Message**:
This platform establishes Plymouth Research as the leading independent source for restaurant menu data, demonstrating innovation, delivering public value, and positioning the organization for future growth - all while maintaining ethical standards and fiscal sustainability.

**Key Talking Points**:
- **Authority Building**: 150 restaurants, 95% data quality, 1,000+ monthly searches by Month 9 → recognized as go-to resource
- **Risk Mitigation**: 100% ethical compliance, legal review, DPIA → zero legal exposure, sustainable long-term
- **Cost Efficiency**: <£100/month operational costs → indefinite sustainability without external funding
- **Media & Reputation**: Target 10 media citations by Month 12 → builds organizational brand and credibility
- **Expansion Potential**: Success in Plymouth creates template for other cities, data domains, or commercial services

**Communication Frequency**: Weekly during development (Months 1-4), Bi-weekly post-launch (Months 5-12)

**Preferred Channel**:
- Weekly progress meetings (30 minutes)
- Monthly dashboard reviews (quantitative metrics: costs, data quality, user adoption)
- Quarterly strategic reviews (outcomes, media coverage, expansion opportunities)

**Success Story**:
"Plymouth Research cited in BBC News article as authoritative source for restaurant trends. Dashboard hits 1,500 monthly searches. Council tourism board inquires about partnership. Platform operates at £85/month, fully sustainable."

---

#### Data Engineer (Technical Lead)

**Primary Message**:
Build a technically excellent, maintainable platform using modern data engineering best practices, open source tools, and clean architecture - creating a portfolio project demonstrating your skills while avoiding technical debt and on-call nightmares.

**Key Talking Points**:
- **Technical Quality**: Follow architecture principles, write tests, use Infrastructure as Code → pride in quality work
- **Learning Opportunities**: Modern stack (Python, PostgreSQL, Streamlit/Dash, cloud infrastructure) → career skill development
- **Autonomy**: Clear architecture guidance, but flexibility in implementation details → professional trust
- **Avoid Firefighting**: Invest in quality upfront (automated testing, monitoring) → sleep well, no weekend outages
- **Recognition**: User adoption and media coverage reflect positively on your technical execution

**Communication Frequency**: Daily stand-ups during development (Months 1-4), As-needed post-launch

**Preferred Channel**:
- Slack/chat for quick questions
- Weekly technical reviews with Research Director (architecture decisions, blockers)
- Documentation in Git (ADRs, README, runbooks)

**Success Story**:
"Dashboard launched on time with zero critical bugs. Performance <400ms sustained. Data quality 96%. User feedback: 'Fast and easy to use!' Data Engineer presents platform at local tech meetup, gets job offers demonstrating skill growth."

---

#### Research Analysts (Primary Users)

**Primary Message**:
This platform eliminates manual menu data collection, giving you fast access to accurate, comprehensive restaurant data for market research, trend analysis, and reports - saving hours of work and enabling insights that weren't feasible before.

**Key Talking Points**:
- **Time Savings**: Instant search vs. hours of manual website browsing and data entry
- **Comprehensive Coverage**: 150 restaurants, 10,000+ menu items → complete market view
- **Reliable Data**: 95% accuracy, weekly refresh → trust the data for analysis and publications
- **Export Functionality**: CSV export for Excel/analysis tools → integrate with your workflow
- **Continuous Improvement**: Monthly data quality reviews, feedback drives prioritization → your input shapes product

**Communication Frequency**: Monthly during development (requirements input), Bi-weekly post-launch (feedback sessions)

**Preferred Channel**:
- User testing sessions (beta testing in Month 3)
- Feedback surveys (quarterly)
- Slack/email for bug reports or data issues

**Success Story**:
"Research Analyst completes 'Vegan Options in Plymouth' report in 2 hours instead of 2 days. Exports data to Excel, creates charts, publishes findings. Manager impressed with quick turnaround and comprehensive data."

---

#### Plymouth Consumers (External Users)

**Primary Message**:
Easily find Plymouth restaurants offering the dishes, dietary options, and price ranges you're looking for - all in one place, for free, with up-to-date menus and clear dietary tagging.

**Key Talking Points**:
- **Dietary Inclusivity**: Search for vegan, vegetarian, gluten-free, nut-free options across all restaurants
- **Price Transparency**: Find restaurants within your budget (student-friendly, mid-range, special occasion)
- **Time Savings**: One search instead of browsing dozens of restaurant websites
- **Up-to-Date Data**: Menus refreshed weekly, freshness clearly indicated
- **No Ads, No Tracking**: Free public resource from independent research organization

**Communication Frequency**: As-needed (platform available 24/7, no proactive outreach)

**Preferred Channel**:
- Dashboard itself (self-service search)
- Optional feedback form (rate satisfaction, report errors)
- Social media (Plymouth Research Twitter/Facebook for announcements)

**Success Story**:
"Vegan visiting Plymouth searches 'vegan Sunday roast' → finds 8 restaurants with vegan options, prices, and links to menus → books reservation, has great meal, tells friends about the tool."

---

#### Restaurant Owners (Data Sources)

**Primary Message**:
Your restaurant menu is represented accurately on Plymouth Research's free food discovery platform, driving visibility and customer discovery - with full respect for your website terms, attribution to your site, and easy opt-out if you prefer exclusion.

**Key Talking Points**:
- **Free Visibility**: Searchable menu data helps customers discover your restaurant (especially for dietary needs)
- **Accurate Representation**: 95% data quality, weekly refresh → your menu shown correctly
- **Attribution**: Every menu item links back to your website → drives traffic to your site
- **Respectful Scraping**: Robots.txt compliance, 5-second rate limits → no server burden
- **Opt-Out Available**: Easy removal request process if you prefer not to be included

**Communication Frequency**: Minimal (one-time notification post-launch, as-needed for opt-outs)

**Preferred Channel**:
- Email notification (one-time, post-launch: "Your restaurant is now listed on Plymouth Research platform. Opt-out info: [link]")
- Opt-out form on website (prominent, easy to find)
- Direct email for opt-out requests (48-hour response SLA)

**Success Story**:
"Restaurant owner searches for their own restaurant on platform → sees accurate menu, prices, dietary tags → happy with representation → shares on social media ('Find us on Plymouth Research!'). No opt-out requests received from 95%+ of restaurants."

---

#### Food Writers/Journalists (Media Users)

**Primary Message**:
Access exclusive aggregated restaurant menu data for Plymouth to write data-driven food stories, trend analysis, and comparative insights - citing Plymouth Research as a credible, independent source.

**Key Talking Points**:
- **Unique Data**: Aggregated menu data not available elsewhere → exclusive story angles
- **Trend Analysis**: Historical data enables "Vegan options up 40% in 2 years" type stories
- **Credible Source**: Independent research organization, transparent methodology → editors approve
- **Export Functionality**: CSV export for your own analysis and visualization
- **Collaboration Welcome**: Plymouth Research happy to provide custom data extracts or clarify methodology

**Communication Frequency**: As-needed (journalists contact Plymouth Research when they need data)

**Preferred Channel**:
- Email for data requests or methodology questions
- Dashboard for self-service data export
- Press release at launch (Month 4) announcing platform availability

**Success Story**:
"Food writer for local newspaper writes 'The average price of fish & chips in Plymouth is £11.20, up from £9.50 in 2024, according to Plymouth Research data.' Story cites platform, drives 200 new users that week. Journalist bookmarks platform for future stories."

---

## Change Impact Assessment

### Impact on Stakeholders

| Stakeholder | Current State | Future State | Change Magnitude | Resistance Risk | Mitigation Strategy |
|-------------|---------------|--------------|------------------|-----------------|---------------------|
| **Research Analysts** | Manual menu data collection (hours per report) | Instant search and export (minutes per report) | HIGH (workflow change) | LOW (positive change - saves time) | User training session (Month 3), ongoing support, feedback loop to address usability issues |
| **Data Engineer** | No Plymouth project (working on other tasks) | Full-time platform development & maintenance | HIGH (new project) | LOW (career growth opportunity) | Clear architecture guidance, autonomy in implementation, recognition for quality work |
| **Research Director** | No restaurant data platform | Managing new platform, media inquiries, partnerships | MEDIUM (new responsibility) | LOW (strategic goal) | Monthly reviews, delegated day-to-day to Data Engineer, focus on strategic outcomes |
| **Plymouth Consumers** | Browsing multiple restaurant websites manually | Single search platform for all restaurants | MEDIUM (new tool available) | LOW (optional, no forced change) | Word-of-mouth adoption, SEO, social media promotion - let awareness build organically |
| **Restaurant Owners** | No aggregation of their menus | Menus scraped and displayed on platform | MEDIUM (visibility change) | MEDIUM (some may resist aggregation) | Opt-out mechanism, respectful scraping, accurate data, attribution to their website - address concerns proactively |
| **Operations/IT** | No platform to maintain | Deploy and monitor new platform | MEDIUM (new operational responsibility) | MEDIUM (workload increase) | Infrastructure as Code, managed services, automated monitoring → minimize manual toil |

### Change Readiness

**Champions** (Enthusiastic supporters):
- **Research Director** - Strategic vision owner, career advancement tied to success, fully committed
- **Research Analysts** - Direct beneficiaries (time savings, better data), eager to use platform
- **Data Engineer** - Technical ownership, skill development opportunity, professional pride in building quality product

**Fence-sitters** (Neutral, need convincing):
- **Operations/IT** - Concerned about maintenance burden and costs → Convince with: Infrastructure as Code, managed services, cost monitoring, clear runbooks
- **Food Writers/Journalists** - Will use platform if data quality proven credible → Convince with: 95% accuracy, transparent methodology, quick responses to inquiries
- **Plymouth Consumers** - Unaware platform exists initially → Convince with: SEO, word-of-mouth, social media, useful results (actual value)

**Resisters** (Opposed or skeptical):
- **Some Restaurant Owners** - May perceive aggregation as:
  - **Concern 1**: "Price comparison commoditizes our food" → **Mitigation**: Emphasize quality differentiation (dietary options, cuisine diversity, not just price)
  - **Concern 2**: "Stale data will mislead customers" → **Mitigation**: Weekly refresh, freshness timestamps, "report error" feature
  - **Concern 3**: "We don't want to be listed" → **Mitigation**: Easy opt-out mechanism, 48-hour removal, no questions asked
  - **Strategy**: Respect resistance. Don't fight opt-outs. Focus on 95%+ restaurants who accept or appreciate visibility. Monitor opt-out rate (<5% target indicates community acceptance).

---

## Risk Register (Stakeholder-Related)

### Risk R-1: Low User Adoption (1,000+ Searches Target Not Met)

**Related Stakeholders**: Research Director (SD-1: authority goal), Plymouth Consumers (SD-5: intended users), Food Writers (SD-7: data consumers)

**Risk Description**:
Dashboard launches but users don't discover it or don't find it useful → low search volume (<500/month) → fails to establish authority → wasted investment and damaged credibility.

**Impact on Goals**:
- G-7 (1,000+ Monthly Searches) - MISSED
- G-1 (95% Data Quality) - IRRELEVANT if no users
- O-1 (Recognized as Authoritative Source) - FAILED
- O-4 (User Satisfaction & Adoption) - FAILED

**Probability**: **MEDIUM** (30-40% chance if no marketing/SEO effort)

**Impact**: **HIGH** (strategic goal failure, wasted investment)

**Mitigation Strategy**:
1. **SEO Optimization**: Meta tags, sitemap, Google Search Console setup (Month 2-3)
2. **Word-of-Mouth Launch**:
   - Email to Plymouth food bloggers, local influencers (Month 4 launch week)
   - Social media posts in Plymouth community groups (Reddit r/plymouth, Facebook groups)
   - Press release to local media (Plymouth Herald, BBC Radio Devon)
3. **Content Marketing**:
   - Research Director publishes blog post "Analyzing Plymouth's Restaurant Scene by the Numbers" using platform data (drives traffic)
   - Food writer partnerships (offer exclusive data access for launch week articles)
4. **User Testing Pre-Launch**: 10 beta users (Month 3) validate usability → ensure platform is actually useful before public launch

**Contingency Plan** (if risk occurs):
- **Month 6**: If searches <300/month → diagnose root cause:
  - **Low awareness?** → Increase marketing (paid social media ads, local events sponsorship)
  - **Poor usability?** → User research (surveys, interviews) → prioritize UX improvements
  - **Insufficient data?** → Expand coverage beyond 150 restaurants or improve data quality
- **Month 9**: If searches still <500/month → consider pivoting to B2B (sell data to tourism board, researchers) vs. public consumer platform

---

### Risk R-2: Data Quality Below 95% Target Damages Credibility

**Related Stakeholders**: Research Director (SD-1: reputation), Research Analysts (SD-4: reliable data), Plymouth Consumers (SD-5: trust), Restaurant Owners (SD-6: accurate representation)

**Risk Description**:
Scraping extraction logic struggles with diverse website formats → accuracy remains 70-80% → users find incorrect prices or menu items → lose trust → platform credibility damaged → restaurant complaints increase.

**Impact on Goals**:
- G-1 (95% Data Quality) - MISSED
- O-1 (Recognized as Authoritative Source) - FAILED (reputation damaged)
- O-2 (Zero Legal Violations) - RISK (restaurant complaints could escalate to legal inquiries)

**Probability**: **MEDIUM** (40-50% chance with 150 diverse restaurant websites)

**Impact**: **CRITICAL** (reputation damage, stakeholder dissatisfaction)

**Mitigation Strategy**:
1. **Iterative Quality Improvement**:
   - Month 1: Scrape 30 restaurants, manually validate → identify extraction failures → refine logic
   - Month 2: Scrape 60 restaurants, repeat validation → continue refinement
   - Don't scale to 150 until achieving 90%+ on first 60
2. **Manual Fallback**:
   - For complex websites (JavaScript-heavy, unusual formats), manual data entry acceptable initially
   - Prioritize high-quality data over 100% automation
3. **User-Reported Errors**:
   - "Report Incorrect Data" button on dashboard → users help identify quality issues
   - Research Analyst reviews reports weekly → fixes data and improves extraction rules
4. **Conservative Scope**:
   - If 95% accuracy unachievable at 150 restaurants, maintain 100-120 high-quality restaurants instead
   - Better to have fewer restaurants with excellent data than many restaurants with poor data

**Contingency Plan** (if risk occurs):
- **Month 4**: If data quality <85% → delay public launch (Month 5) until quality improves
- **Month 6**: If data quality still <90% → reduce scope to 80-100 restaurants with highest accuracy
- **Month 9**: If quality persistently low → consider manual curation overlay (Research Analyst spot-checks and corrects high-traffic menu items)

---

### Risk R-3: Legal Complaint or ICO Investigation

**Related Stakeholders**: Research Director (SD-2: legal risk), Legal Advisor (SD-8: compliance), ICO (SD-9: regulator), Restaurant Owners (SD-6: potential complainants)

**Risk Description**:
Despite ethical scraping efforts, a restaurant owner files complaint alleging Computer Misuse Act violation, copyright infringement, or GDPR violation → legal costs, reputational damage, potential platform shutdown.

**Impact on Goals**:
- G-3 (100% Ethical Compliance) - VIOLATED
- O-2 (Zero Legal Violations) - FAILED
- All other goals potentially derailed if platform must shut down

**Probability**: **LOW** (10-15% if ethical scraping principles followed rigorously)

**Impact**: **CRITICAL** (could shut down project, financial liability, reputational disaster)

**Mitigation Strategy**:
1. **Proactive Legal Review**:
   - Legal advisor reviews scraping practices before launch (Month 1)
   - DPIA completed and approved (Month 1)
   - Opt-out mechanism prominent and functional (Month 2)
2. **Technical Compliance Controls**:
   - Robots.txt parser (cannot be bypassed)
   - Rate limiting (infrastructure-enforced, not just code)
   - User-Agent transparency (Plymouth Research identified)
3. **Community Goodwill**:
   - Respectful approach (attribution, opt-out, transparency)
   - Public benefit framing (helping consumers, not commercial exploitation)
   - Open communication with restaurants (email notification at launch)
4. **Insurance**:
   - Consider professional indemnity insurance covering data-related legal claims (if affordable)

**Contingency Plan** (if risk occurs):
- **Immediate Response**:
  - Legal advisor engaged immediately upon complaint receipt
  - Cease scraping complained-about restaurant immediately (opt-out processed within hours)
  - Document all compliance efforts (robots.txt logs, rate limiting, DPIA, opt-out mechanism)
- **Resolution Approach**:
  - Apologize if genuine violation occurred, explain compliance efforts, offer immediate removal
  - If frivolous complaint (no actual violation), provide evidence of compliance, seek legal advisor guidance on response
  - Worst case (ICO investigation): Cooperate fully, demonstrate good-faith compliance efforts, argue public interest and non-commercial nature

---

### Risk R-4: Operational Costs Exceed £100/Month Budget

**Related Stakeholders**: Research Director (SD-1: sustainability), Operations/IT (SD-10: cost management)

**Risk Description**:
Infrastructure costs (database, compute, storage) grow beyond £100/month due to data volume, traffic, or inefficient architecture → financial unsustainability → requires external funding or platform shutdown.

**Impact on Goals**:
- G-5 (Costs <£100/month) - MISSED
- O-3 (Operational Sustainability) - FAILED
- All long-term goals at risk if platform not financially sustainable

**Probability**: **MEDIUM** (30-40% if not carefully optimized)

**Impact**: **HIGH** (financial unsustainability threatens project viability)

**Mitigation Strategy**:
1. **Cost Monitoring**:
   - Monthly invoice tracking and cost allocation
   - Budget alerts at 80% threshold (£80/month)
   - Cost per restaurant metric tracked (target <£0.67)
2. **Architecture Optimization**:
   - Use managed services with generous free tiers (e.g., Render, Heroku, DigitalOcean)
   - Serverless scraping (pay per scrape, not always-on VMs)
   - Right-size database (don't over-provision)
   - Compress historical data, delete unnecessary files
3. **Phased Scaling**:
   - Start with 30 restaurants (Month 1) → validate costs
   - Scale to 150 only if costs remain within budget
   - If costs exceed, maintain 100-120 restaurants instead
4. **Open Source Tooling**:
   - Zero licensing fees (PostgreSQL, Python, Streamlit/Dash)
   - Free monitoring (Prometheus, Grafana free tiers or self-hosted)

**Contingency Plan** (if risk occurs):
- **Month 3**: If costs >£120/month → investigate cost drivers (database size? compute? storage?)
- Optimize highest cost component:
  - Database too large? → Compress historical data, reduce retention from 12 months to 6 months
  - Compute costs high? → Move to cheaper hosting, optimize scraping efficiency
  - Storage costs high? → Delete raw HTML snapshots (keep only processed data)
- **Month 6**: If still >£100/month → reduce restaurant count or seek sponsorship (local tourism board, council grant)

---

### Risk R-5: Key Personnel Departure (Data Engineer Leaves)

**Related Stakeholders**: Data Engineer (SD-3: implementer), Research Director (SD-1: project owner), Operations/IT (SD-10: inherits maintenance)

**Risk Description**:
Data Engineer leaves organization (new job, relocation, illness) mid-project or post-launch → knowledge loss → platform maintenance burden falls on Operations/IT or replacement hire → delays, quality degradation, potential platform failure.

**Impact on Goals**:
- G-6 (Launch Month 4) - DELAYED if departure during development
- G-1, G-4, G-5 (Quality, Performance, Cost) - DEGRADED if no one can maintain platform
- O-3 (Operational Sustainability) - FAILED if platform becomes unmaintainable

**Probability**: **LOW-MEDIUM** (15-25% in any 12-month period)

**Impact**: **HIGH** (project continuity risk)

**Mitigation Strategy**:
1. **Documentation**:
   - README with setup instructions
   - ADRs documenting key architecture decisions
   - Runbooks for deployment, monitoring, common errors
   - Code comments explaining "why" not just "what"
2. **Infrastructure as Code**:
   - All infrastructure reproducible from Git (no manual server setup)
   - Deployment automated (not dependent on Data Engineer's laptop)
3. **Knowledge Sharing**:
   - Monthly architecture reviews with Operations/IT (knowledge transfer)
   - Research Director has high-level understanding of architecture
4. **Maintainability Focus**:
   - Simple, modular architecture (not over-engineered)
   - Open source tools with good community support (easy to find replacement expertise)
   - Automated testing (reduces reliance on tribal knowledge)

**Contingency Plan** (if risk occurs):
- **Immediate**:
  - Data Engineer documents handover (architecture, runbooks, known issues, passwords)
  - Operations/IT takes over basic maintenance (monitoring, restarts)
- **Short-term (1-2 months)**:
  - Research Director hires replacement Data Engineer or contractor
  - Replacement onboards using documentation and IaC (environment reproducible)
- **Worst case**:
  - If no replacement found, freeze development (no new features)
  - Maintain dashboard in "sustaining engineering" mode (bug fixes only, no enhancements)
  - Accept degraded data quality or coverage rather than shutting down

---

## Governance & Decision Rights

### Decision Authority Matrix (RACI)

| Decision Type | Responsible | Accountable | Consulted | Informed |
|---------------|-------------|-------------|-----------|----------|
| **Strategic & Budget** | | | | |
| Budget approval (annual/monthly) | Operations/IT | Research Director | Data Engineer | All stakeholders |
| Project scope (150 restaurants, launch date) | Research Director | Research Director | Data Engineer, Analysts | All stakeholders |
| Expansion to new cities | Research Director | Research Director | Analysts, Data Engineer | All stakeholders |
| **Requirements & Priorities** | | | | |
| Requirements prioritization | Research Director | Research Director | Analysts, Data Engineer | Consumers (feedback) |
| Feature roadmap | Data Engineer | Research Director | Analysts | All users |
| Data quality thresholds (95% target) | Research Director | Research Director | Data Engineer, Analysts | All users |
| **Technical & Architecture** | | | | |
| Architecture decisions (ADRs) | Data Engineer | Research Director | Operations/IT, Legal Advisor | Analysts |
| Technology selection (build vs buy vs open source) | Data Engineer | Research Director | Operations/IT | None |
| Database schema design | Data Engineer | Data Engineer | Analysts (requirements input) | None |
| Infrastructure provisioning | Operations/IT | Operations/IT | Data Engineer | Research Director (cost approval) |
| **Legal & Compliance** | | | | |
| DPIA approval | Legal Advisor | Research Director | Data Engineer | ICO (informed via publication) |
| Ethical scraping policies | Legal Advisor | Research Director | Data Engineer | Restaurant Owners (affected) |
| Opt-out request processing | Operations/IT or Data Engineer | Research Director | Legal Advisor (if contentious) | Restaurant Owner (requestor) |
| **Operations** | | | | |
| Deployment to production | Data Engineer | Data Engineer | Operations/IT | Research Director |
| Monitoring & alerting configuration | Data Engineer | Operations/IT | Research Director | None |
| Incident response (dashboard down) | Operations/IT | Operations/IT | Data Engineer | Research Director, Users (status updates) |
| **Launch & Marketing** | | | | |
| Go/No-go for public launch | Research Director | Research Director | Data Engineer, Legal Advisor | All stakeholders |
| Press release & media outreach | Research Director | Research Director | Analysts (data fact-checking) | All stakeholders |
| User communication (announcements) | Research Director | Research Director | Data Engineer (technical accuracy) | Users |

### Escalation Path

**Level 1: Day-to-Day Operations** (Data Engineer / Operations/IT)
- **Scope**: Technical implementation, bug fixes, monitoring, deployment, routine operations
- **Authority**: Proceed autonomously within architecture principles and approved scope
- **Escalation Trigger**: Scope change requests, architecture principle exceptions, budget overruns, timeline delays >1 week

**Level 2: Project Steering** (Research Director + Data Engineer + Operations/IT)
- **Scope**: Requirements changes, timeline adjustments, cost variances <20%, minor scope changes
- **Authority**: Approve changes that don't fundamentally alter goals or outcomes
- **Escalation Trigger**: Major scope changes (e.g., reduce from 150 to 100 restaurants), budget overruns >20%, timeline delays >1 month, legal complaints, principle violations

**Level 3: Executive Decision** (Research Director with Legal Advisor as needed)
- **Scope**: Strategic direction, major scope changes, legal/compliance issues, project continuation vs. shutdown
- **Authority**: Final authority on all project decisions
- **Examples**:
  - Legal complaint requiring platform changes or shutdown
  - Budget increases requiring external funding
  - Decision to expand to new cities or pivot to B2B model
  - Architecture principle exception requests

---

## Validation & Sign-off

### Stakeholder Review

| Stakeholder | Review Date | Comments | Status |
|-------------|-------------|----------|--------|
| Research Director | 2025-11-15 | [Pending review] | DRAFT |
| Data Engineer | [TBD] | [Pending review] | DRAFT |
| Legal/Compliance Advisor | [TBD] | [Pending review] | DRAFT |
| Research Analysts | [TBD] | [Pending review] | DRAFT |

### Document Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Project Sponsor | Research Director | [Pending] | [TBD] |
| Technical Lead | Data Engineer | [Pending] | [TBD] |
| Legal/Compliance | Legal Advisor | [Pending] | [TBD] |

---

## Appendices

### Appendix A: Architecture Principles Alignment

This stakeholder analysis aligns with the 18 architecture principles defined in `.arckit/memory/architecture-principles.md`:

**Directly Addressed by Stakeholder Drivers**:
1. **Data Quality First (Principle 1)** → SD-1, SD-4, SD-5, SD-6 → Goal G-1 (95% accuracy)
2. **Open Source Preferred (Principle 2)** → SD-3, SD-10 (cost efficiency) → Goal G-8 (technology research)
3. **Ethical Web Scraping (Principle 3)** → SD-2, SD-6, SD-8, SD-9 → Goal G-3 (100% compliance)
4. **Privacy by Design (Principle 4)** → SD-2, SD-8, SD-9 → Goal G-8 (DPIA completion)
5. **Cost Efficiency (Principle 6)** → SD-10 → Goal G-5 (<£100/month)
6. **Performance Targets (Principle 12)** → SD-4, SD-5 → Goal G-4 (<500ms searches)

**Implicitly Supported**:
- Scalability (Principle 5) → G-2 (150+ restaurants, room for growth)
- Infrastructure as Code (Principle 15) → SD-3 (maintainability), Risk R-5 mitigation
- Automated Testing (Principle 16) → SD-3 (quality), Risk R-2 mitigation
- Logging & Monitoring (Principle 18) → SD-10 (operational burden), O-3 (sustainability)

### Appendix B: Next Steps

**Immediate Actions** (Month 1):
1. **Stakeholder Approval**: Circulate this document to Research Director, Data Engineer, Legal Advisor for review and sign-off
2. **Technology Research**: Begin `/arckit.research` for build vs buy vs open source analysis (scraping, database, dashboard)
3. **Requirements Definition**: Run `/arckit.requirements` to translate stakeholder goals into detailed functional and non-functional requirements
4. **DPIA Initiation**: Run `/arckit.dpia` to assess GDPR compliance for web scraping

**Month 2-3 Actions**:
1. **Architecture Design**: Document ADRs, data model, deployment architecture (Goal G-8)
2. **Prototype Development**: Build scraping prototype for 30 restaurants (validate approach)
3. **Legal Review**: Legal advisor reviews DPIA, scraping practices, opt-out mechanism

**Month 4+ Actions**:
1. **Dashboard Launch**: Public launch (Goal G-6)
2. **User Adoption Tracking**: Monitor monthly searches (Goal G-7)
3. **Continuous Improvement**: Iterative data quality improvements (Goal G-1)

### Appendix C: References

- **Architecture Principles**: `.arckit/memory/architecture-principles.md` (2025-11-15)
- **Project Context**: `PROJECT-README.md` (Plymouth Research overview)
- **Stakeholder Template**: `.arckit/templates/stakeholder-drivers-template.md`

---

**Generated by**: ArcKit `/arckit.stakeholders` command
**Generated on**: 2025-11-15
**ArcKit Version**: v0.9.1
**Project**: Plymouth Research Restaurant Menu Analytics (Project 001)
**AI Model**: Claude Sonnet 4.5 (claude-sonnet-4-5-20250929)
