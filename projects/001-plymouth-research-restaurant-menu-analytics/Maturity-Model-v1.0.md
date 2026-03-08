# Maturity Model: Plymouth Research Restaurant Menu Analytics

> **Template Origin**: Official | **ArcKit Version**: 4.0.1 | **Command**: `/arckit:maturity-model`

## Document Control

| Field | Value |
|-------|-------|
| **Document ID** | ARC-001-MMOD-v1.0 |
| **Document Type** | Maturity Model |
| **Project** | Plymouth Research Restaurant Menu Analytics (Project 001) |
| **Classification** | OFFICIAL |
| **Status** | DRAFT |
| **Version** | 1.0 |
| **Created Date** | 2026-03-08 |
| **Last Modified** | 2026-03-08 |
| **Review Cycle** | Quarterly |
| **Next Review Date** | 2026-04-07 |
| **Owner** | Research Director, Plymouth Research |
| **Reviewed By** | PENDING |
| **Approved By** | PENDING |
| **Distribution** | Project Team, Architecture Team |

## Revision History

| Version | Date | Author | Changes | Approved By | Approval Date |
|---------|------|--------|---------|-------------|---------------|
| 1.0 | 2026-03-08 | ArcKit AI | Initial creation from `/arckit:maturity-model` command | PENDING | PENDING |

---

## 1. Executive Summary

This maturity model defines five capability dimensions tailored to the Plymouth Research Restaurant Menu Analytics platform — a data-intensive system that collects restaurant data through web scraping, integrates multiple external sources (FSA hygiene ratings, Trustpilot, Google Places, Companies House), and presents insights through an interactive Streamlit dashboard.

The model enables the Research Director and project team to objectively assess current capabilities, set improvement targets, and plan a structured progression from ad-hoc practices to optimised, automated operations. The five dimensions reflect the project's core value drivers: data quality as the foundation of credibility, ethical and legal compliance as non-negotiable constraints, data integration maturity across six external sources, technology operations supporting reliable delivery, and observability enabling data-driven improvement.

Given the project's current state — a functioning MVP with 98 restaurants, 2,625 menu items, and integrations with three review/rating platforms — the baseline assessment is expected to fall between Level 2 (Repeatable) and Level 3 (Defined) across most dimensions, with targeted progression to Level 3-4 within 12 months.

---

## 2. Purpose and Scope

### Purpose

This maturity model provides a structured framework for assessing and improving the capabilities of the Plymouth Research Restaurant Menu Analytics platform. It informs decisions about where to invest engineering effort, identifies capability gaps that present risk (as documented in ARC-001-RISK-v1.0), and provides measurable criteria for tracking improvement over time.

### Scope

**In scope**:
- Data collection pipelines (web scraping, API integrations, manual matching)
- Data quality management (validation, normalisation, deduplication)
- Ethical and legal compliance (robots.txt, rate limiting, GDPR, DPIA)
- Data integration across six external sources (FSA, Trustpilot, Google Places, Companies House, ONS, Plymouth Council)
- Technology operations (deployment, CI/CD, infrastructure)
- Observability and monitoring (logging, metrics, alerting)

**Out of scope**:
- Organisational maturity beyond the project team
- Commercial maturity (sales, marketing, partnerships)
- Financial management maturity (covered separately by FinOps if needed)

### Target Audience

| Audience | Role in Using the Model |
|----------|------------------------|
| Research Director | Review assessment results, set target maturity levels, approve investment in improvement |
| Data Engineer | Conduct self-assessments, implement improvements, track technical progress |
| Research Analysts | Provide input on data quality experience, validate user-facing improvements |
| Legal/Compliance Advisor | Validate compliance dimension scoring, advise on regulatory requirements |

### How to Use This Model

1. Review the maturity levels and capability dimensions to understand the framework
2. Conduct a self-assessment using the questionnaire in Section 8
3. Score each dimension against the detailed level definitions in Section 5
4. Identify gaps between current and target maturity levels
5. Develop an improvement roadmap based on transition criteria in Section 6
6. Reassess quarterly to track progress

---

## 3. Maturity Model Overview

The following table defines the five maturity levels used throughout this model. Each level builds upon the previous, representing increasing capability, consistency, and optimisation.

| Level | Name | Description |
|-------|------|-------------|
| 1 | Initial / Ad-Hoc | Processes are unpredictable and reactive. Data collection and quality checks depend on individual effort. No documented standards or automated validation. Outcomes are inconsistent across scraping runs. |
| 2 | Repeatable | Basic processes are documented and can be repeated. Scraping scripts work reliably for known restaurant formats. Manual quality checks exist. Key operational procedures are written down but not automated. |
| 3 | Defined | Processes are standardised across the platform. Data validation rules are codified and applied consistently. Compliance controls are documented and enforced. Monitoring covers key metrics. The team follows established procedures. |
| 4 | Managed | Processes are quantitatively measured and controlled. Data quality metrics are tracked against SLAs (e.g., > 95% completeness). Scraping success rates are monitored with automated alerting. Decisions are data-driven with dashboards tracking all key indicators. |
| 5 | Optimised | Continuous improvement is embedded. ML-assisted data extraction adapts to website changes. Automated anomaly detection flags quality degradation before users notice. The platform benchmarks against industry best practices and proactively adopts innovations. |

---

## 4. Capability Dimensions

The maturity model assesses the following capability dimensions. Each dimension represents a distinct area of practice that contributes to overall platform maturity.

| Dimension ID | Dimension | Description |
|--------------|-----------|-------------|
| DIM-01 | Data Quality Management | The policies, validation rules, normalisation standards, and monitoring practices that ensure scraped and integrated data is accurate, complete, consistent, and timely. Core to the platform's value proposition. |
| DIM-02 | Ethical Data Collection | The practices, controls, and governance ensuring all web scraping and data collection respects robots.txt, rate limits, terms of service, copyright, and provides opt-out mechanisms for data sources. |
| DIM-03 | Data Integration & Interoperability | The maturity of integrations with external data sources (FSA, Trustpilot, Google Places, Companies House, ONS, Plymouth Council), including matching algorithms, API management, and data format standardisation. |
| DIM-04 | Technology Operations | The CI/CD pipelines, infrastructure management, deployment automation, testing practices, and operational procedures that support reliable, repeatable platform delivery. |
| DIM-05 | Observability & Data-Driven Improvement | The logging, metrics, monitoring, alerting, and feedback mechanisms used to detect issues, measure performance, and drive continuous improvement of the platform. |

---

## 5. Detailed Level Definitions

This section provides detailed characteristics for each maturity level within each capability dimension. Use these definitions to assess the current maturity level for each dimension.

### 5.1 DIM-01: Data Quality Management

| Level | Characteristics | Evidence | Example |
|-------|----------------|----------|---------|
| 1 - Initial | No formal data validation rules. Scraped data stored as-is. Quality issues discovered reactively by users. No normalisation standards. Duplicate detection absent. | No validation code in scraping pipeline. Raw HTML stored without processing. User complaints about incorrect prices. | Price "Twelve pounds fifty" stored as text string. Dashboard displays unparseable values. |
| 2 - Repeatable | Basic validation for critical fields (price format, restaurant name). Some normalisation applied (GBP format). Manual duplicate checks performed occasionally. Quality issues logged but not systematically tracked. | Validation functions exist in ETL code. Price regex matching implemented. `unmatched_hygiene_ratings.csv` reviewed periodically. | Prices normalised to decimal format. Basic range checks flag prices outside £0.50-£500. Manual review of matcher output CSVs. |
| 3 - Defined | Comprehensive validation rules documented for all entities. Normalisation standards codified (Title Case names, controlled category vocabulary, standardised dietary tags). Automated duplicate detection. Data quality metrics defined with thresholds. | Validation rules documented per ARC-001-DATA-v1.0 field specifications. Automated quality checks run on every ETL execution. Quality thresholds: > 95% completeness, > 98% accuracy. | All menu items validated against schema before database insert. Category taxonomy enforced. Fuzzy matcher scores logged with confidence levels. |
| 4 - Managed | Data quality dashboards track completeness, accuracy, freshness, and uniqueness in real-time. Quality SLAs defined and monitored. Root causes of quality failures analysed and addressed systematically. Trends tracked over time. | Quality metrics dashboard showing: completeness % per entity, accuracy sample audit results, data freshness (hours since last scrape), duplicate rate. Monthly quality trend reports. | Automated alert when menu item completeness drops below 95%. Weekly quality report showing 97.2% completeness, 99.1% price accuracy, 12-hour average freshness. |
| 5 - Optimised | ML-assisted extraction adapts to website format changes automatically. Predictive quality monitoring flags degradation before thresholds are breached. Community feedback loop improves validation rules. Benchmarking against similar platforms. | Self-healing scraper that detects and adapts to HTML structure changes. Anomaly detection model on quality metrics. A/B testing of extraction algorithms. Quality benchmarks vs industry standards. | Scraper detects restaurant website redesign, automatically reconfigures selectors, validates extraction accuracy > 98% before promoting new configuration. |

### 5.2 DIM-02: Ethical Data Collection

| Level | Characteristics | Evidence | Example |
|-------|----------------|----------|---------|
| 1 - Initial | No robots.txt checking. No rate limiting between requests. Generic or deceptive User-Agent string. No terms of service review. No opt-out mechanism for restaurants. | Scraping code with no delay between requests. No robots.txt parser. User-Agent set to default library value or fake Googlebot. | 100 pages scraped in 10 seconds. Robots.txt disallow directives ignored. Restaurant owner has no way to request removal. |
| 2 - Repeatable | Robots.txt checked manually before scraping new sites. Fixed delay between requests (e.g., 5 seconds). Honest User-Agent string set. Basic awareness of legal requirements but not formally documented. | Rate limiting code present (time.sleep). User-Agent includes "PlymouthResearch". Robots.txt reviewed for new domains. | 5-second delay enforced between requests. User-Agent: "PlymouthResearchMenuScraper/1.0". Manual robots.txt check before adding new restaurant. |
| 3 - Defined | Automated robots.txt parser in scraping pipeline. Rate limiting enforced with configurable per-domain settings. Terms of service review documented for all scraped sites. Opt-out mechanism implemented and published. DPIA completed. | `robots.txt` parser module in codebase. Per-domain rate limit configuration. ToS review log. Published opt-out contact/process. ARC-001-DPIA-v1.0 approved. | Scraper automatically respects robots.txt. 5s default, 10s for aggressive sites. Opt-out email address published. DPIA documents all processing activities. |
| 4 - Managed | Scraping compliance monitored with automated audits. Rate limit adherence logged and verified. Opt-out requests tracked with SLA (48-hour processing). Legal review conducted quarterly. Compliance metrics reported to governance. | Compliance dashboard: robots.txt violations (target: 0), rate limit adherence (target: 100%), opt-out processing time, ToS review currency. Quarterly legal review minutes. | Zero robots.txt violations in last quarter. 100% rate limit adherence verified through request logs. 2 opt-out requests processed within 24 hours. |
| 5 - Optimised | Proactive engagement with restaurant community. API partnerships replace scraping where possible. Industry leadership in ethical data collection practices. Automated compliance testing in CI pipeline. Contributing to ethical scraping standards bodies. | API agreements with restaurant chains. Automated compliance test suite. Conference talks on ethical scraping. Industry benchmarking. Proactive ToS monitoring for changes. | Direct API feed from 5 restaurant chains. Automated alert when restaurant ToS changes. Published ethical scraping guidelines adopted by other researchers. |

### 5.3 DIM-03: Data Integration & Interoperability

| Level | Characteristics | Evidence | Example |
|-------|----------------|----------|---------|
| 1 - Initial | Single data source (web scraping only). No external integrations. No matching between sources. Data stored in ad-hoc formats. No API layer. | Only scraped menu data in database. No FSA, Trustpilot, or Google data. Direct SQL queries from dashboard. No data export capability. | Dashboard shows menu items only. No hygiene ratings, reviews, or business information. Data locked in SQLite with no external access. |
| 2 - Repeatable | 2-3 external sources integrated (FSA, Trustpilot). Basic fuzzy matching between sources. Manual matching for difficult cases. CSV/JSON data interchange. Dashboard queries database directly. | Fuzzy matcher with name similarity + postcode bonus scoring. Manual match CSV files. 50% FSA match rate. Trustpilot scraper operational for 63/98 restaurants. | FSA hygiene ratings matched to 49/98 restaurants via fuzzy matching. Trustpilot reviews scraped with 2.5s rate limiting. Unmatched records exported to CSV for manual review. |
| 3 - Defined | All planned sources integrated (FSA, Trustpilot, Google Places, Companies House). Matching algorithms standardised with documented thresholds. Data format standards enforced (ISO 8601, GeoJSON, JSON Schema). API layer between dashboard and database. | 6 external source integrations operational. Matching thresholds documented: 0.60 minimum, 0.70 auto-match, 0.95 high confidence. All timestamps ISO 8601. API endpoints for restaurant/menu queries. | Google Places provides 98/98 restaurant coverage. Companies House financial data enriches business profiles. Standard API: `GET /api/v1/restaurants?cuisine=Italian`. |
| 4 - Managed | Integration health monitored per source. Match rates tracked with improvement targets. API versioning and documentation automated. Data freshness SLAs per source. Failed integrations retry with alerting. | Integration dashboard: per-source match rate, last refresh time, error rate, data freshness. API docs auto-generated (OpenAPI). SLA: FSA weekly, Trustpilot monthly, Google quarterly. | FSA match rate: 72% (target: 80%). Google Places refresh: 98/98 within SLA. Automated alert when Trustpilot scrape fails for > 48 hours. API v1.2 documented at /docs. |
| 5 - Optimised | Real-time or near-real-time data feeds where available. ML-assisted entity resolution across sources. New sources onboarded via pluggable framework in < 1 day. Open data contributions back to community. | Streaming FSA updates. ML entity resolution model with > 95% accuracy. Source plugin framework with documented onboarding. Published open dataset. | New source (Deliveroo API) integrated in 4 hours using plugin framework. ML matcher achieves 96% accuracy. Published open dataset of Plymouth restaurant analytics on data.gov.uk. |

### 5.4 DIM-04: Technology Operations

| Level | Characteristics | Evidence | Example |
|-------|----------------|----------|---------|
| 1 - Initial | Manual deployment via SSH. No version control discipline. No automated tests. Database changes applied manually. No backup or disaster recovery plan. | Deployment via manual file copy. Ad-hoc Git commits. No test files in repository. SQL run directly on production database. No backup script. | Developer SSHs to server, copies files, restarts Streamlit manually. Database migration forgotten on production. No way to roll back. |
| 2 - Repeatable | Code in Git with regular commits. Basic deployment script or Streamlit Cloud auto-deploy. Some manual testing before release. Database migrations as SQL files. Manual backups performed occasionally. | Git history with conventional commits. `requirements.txt` maintained. SQL migration files (`add_*.sql`). Streamlit Cloud deployment configured. Occasional `sqlite3 .backup` commands. | Push to main triggers Streamlit Cloud redeploy. 6 SQL migration files version-controlled. Manual backup before major changes. No automated tests but manual smoke testing. |
| 3 - Defined | CI pipeline runs linting and basic checks on every push. Automated deployment to staging and production. Database migrations applied through scripts. Automated backups on schedule. Infrastructure defined as code. | GitHub Actions workflow for CI. Automated deployment pipeline. Migration runner script. Scheduled backup cron job. Infrastructure config in repository. | GitHub Actions runs `flake8` and `python -m py_compile` on PR. Merge to main auto-deploys. Daily database backup to cloud storage. `requirements.txt` pinned versions. |
| 4 - Managed | Automated test suite with > 70% coverage. Performance testing before release. Blue-green or canary deployments. Rollback capability tested and documented. Dependency scanning for vulnerabilities. | Test suite with pytest, coverage report. Load test results for dashboard. Deployment runbook with rollback procedure. Dependabot or similar configured. Release notes automated. | 75% test coverage. Load test confirms < 2s page load at 100 concurrent users. Canary deployment catches regression before full rollout. Dependabot alerts reviewed weekly. |
| 5 - Optimised | Continuous deployment with feature flags. Chaos engineering tests resilience. Automated performance regression detection. Zero-downtime deployments standard. Platform self-heals from common failures. | Feature flag system. Chaos test results. Automated performance benchmarks in CI. Zero-downtime deployment evidence. Self-healing runbook automation. | Feature flag gates new scraper algorithm. Chaos test confirms dashboard serves cached data during DB outage. Performance regression automatically blocks deployment. |

### 5.5 DIM-05: Observability & Data-Driven Improvement

| Level | Characteristics | Evidence | Example |
|-------|----------------|----------|---------|
| 1 - Initial | No structured logging. Errors discovered by users. No metrics collection. No monitoring or alerting. Print statements for debugging. | `print()` statements in code. No log files. No metrics dashboard. Users report "dashboard is down" before team notices. | Scraping failure goes unnoticed for 2 weeks. Data staleness discovered when user reports outdated menu prices. No way to investigate root cause. |
| 2 - Repeatable | Basic logging to files. Key scraping events logged (start, complete, errors). Manual log review after issues. Some operational metrics tracked in spreadsheets. | Log files in `logs/` directory. Scraping logs with timestamps and error counts. Manual review after reported issues. Spreadsheet tracking scrape success rates. | Scraping logs show "Restaurant X: 404 error". Manual log review after user complaint. Spreadsheet: "Week 12: 94/98 restaurants scraped successfully". |
| 3 - Defined | Structured logging (JSON format) with severity levels. Key metrics defined and collected: scrape success rate, data freshness, query latency, error rates. Basic alerting on critical failures. Dashboards for operational metrics. | JSON-structured log entries. Metrics collection for defined KPIs. Alert configuration for critical thresholds. Operational dashboard (Grafana or similar). | Structured log: `{"timestamp": "...", "level": "ERROR", "component": "scraper", "restaurant_id": 42, "error": "robots.txt disallowed"}`. Alert fires when scrape failure > 10%. |
| 4 - Managed | Comprehensive observability stack: distributed tracing, detailed metrics, log aggregation. Performance baselines established. Anomaly detection on key metrics. Regular operational reviews using data. Correlation IDs across pipeline. | Distributed tracing across scrape-ETL-dashboard pipeline. Anomaly detection alerts. Monthly operational review deck with metrics trends. Correlation ID in all log entries. | Correlation ID traces menu item from scrape through ETL to dashboard display. Anomaly detection flags unusual drop in Italian restaurant menu items. Monthly review: "p95 query latency improved 15% after index optimisation". |
| 5 - Optimised | Predictive observability: forecast capacity needs, predict failures before they occur. Automated remediation for known issues. Observability-as-code: monitoring configuration version-controlled. SLO-based alerting with error budgets. | Predictive capacity model. Auto-remediation playbooks. Monitoring-as-code in repository. SLO dashboard with error budget burn rate. | System predicts database storage will exceed capacity in 3 weeks, auto-provisions. Auto-restart of failed scraping job. SLO: 99.5% dashboard availability, current error budget: 72% remaining. |

---

## 6. Transition Criteria Between Levels

The following tables define what must be demonstrated to advance from one maturity level to the next for each dimension.

### DIM-01: Data Quality Management

| From | To | Criteria |
|------|----|----------|
| Level 1 | Level 2 | Validation functions exist for price format (regex), restaurant name (non-empty, trimmed), and required fields. Basic price normalisation to decimal GBP format. At least one manual quality review performed per month. |
| Level 2 | Level 3 | Validation rules documented for all 8 entities in ARC-001-DATA-v1.0. Controlled vocabularies for categories and dietary tags enforced in ETL pipeline. Automated duplicate detection with > 90% precision. Data quality thresholds defined: > 95% completeness, > 98% price accuracy. |
| Level 3 | Level 4 | Data quality metrics dashboard operational with daily refresh. Monthly quality trend reports produced and reviewed. Root cause analysis performed for every quality incident. Quality SLAs contractually defined for dashboard users. Automated quality regression tests in CI pipeline. |
| Level 4 | Level 5 | ML-based extraction achieves > 99% accuracy on price and menu item names. Predictive quality monitoring detects degradation > 24 hours before threshold breach. Self-healing pipelines automatically correct common extraction errors. Annual benchmarking against comparable food data platforms. |

### DIM-02: Ethical Data Collection

| From | To | Criteria |
|------|----|----------|
| Level 1 | Level 2 | Robots.txt reviewed for all currently scraped domains. Rate limiting enforced at minimum 5 seconds between requests per domain. User-Agent string set to "PlymouthResearchMenuScraper/1.0" with contact email. Ethical scraping principles documented and acknowledged by team. |
| Level 2 | Level 3 | Automated robots.txt parser integrated into scraping pipeline. Per-domain rate limit configuration with minimum 5s default. Terms of service review documented for all scraped sites. Opt-out mechanism published and operational. DPIA (ARC-001-DPIA-v1.0) completed and approved. |
| Level 3 | Level 4 | Compliance audit log with zero robots.txt violations for 3 consecutive months. Opt-out requests processed within 48-hour SLA. Quarterly legal review of scraping practices. Compliance metrics reported to Research Director monthly. |
| Level 4 | Level 5 | API partnerships replace scraping for > 30% of data sources. Automated compliance testing in CI pipeline blocks non-compliant code. Proactive engagement with restaurant community (feedback survey, data access requests). Published ethical scraping guidelines. |

### DIM-03: Data Integration & Interoperability

| From | To | Criteria |
|------|----|----------|
| Level 1 | Level 2 | At least 2 external sources integrated (FSA + one review platform). Fuzzy matching implemented with documented scoring (name similarity + postcode + address). Match rate > 40% for FSA data. Data exported in at least one standard format (CSV or JSON). |
| Level 2 | Level 3 | All 4 primary sources integrated (FSA, Trustpilot, Google Places, Companies House). Matching thresholds documented and configurable. All timestamps ISO 8601. API layer exists between dashboard and database. Data format standards enforced with schema validation. |
| Level 3 | Level 4 | Per-source integration health dashboard operational. Match rates tracked monthly with improvement targets (FSA > 80%, Google > 95%). API versioned with auto-generated documentation. Data freshness SLAs defined and monitored per source. Failed integrations auto-retry with alerting. |
| Level 4 | Level 5 | New data source onboarded within 1 day via pluggable integration framework. ML entity resolution achieves > 95% match accuracy across sources. Near-real-time feeds for sources that support it. Open data contributions published. |

### DIM-04: Technology Operations

| From | To | Criteria |
|------|----|----------|
| Level 1 | Level 2 | All code in Git with conventional commit messages. `requirements.txt` maintained with all dependencies. At least one deployment method documented (Streamlit Cloud or manual). Database schema migrations as SQL files in version control. Manual backup performed before major changes. |
| Level 2 | Level 3 | CI pipeline runs linting and syntax checks on every push. Automated deployment to at least one environment. Database migrations applied through scripted process. Automated daily backups. Infrastructure configuration in version control. Dependency versions pinned. |
| Level 3 | Level 4 | Automated test suite with > 70% coverage for business logic. Performance testing confirms < 2s dashboard page load and < 500ms search at expected load. Blue-green or staged deployments with rollback capability. Dependency vulnerability scanning automated. Release notes auto-generated. |
| Level 4 | Level 5 | Continuous deployment with feature flags. Chaos engineering validates resilience (dashboard serves cached data during DB outage). Automated performance regression detection in CI. Zero-downtime deployments standard. Platform self-heals from common failure modes. |

### DIM-05: Observability & Data-Driven Improvement

| From | To | Criteria |
|------|----|----------|
| Level 1 | Level 2 | Logging to files for all scraping operations with timestamps and error details. Scraping success/failure counts tracked per run. Manual review of logs performed after reported issues. Key metrics (restaurants scraped, items extracted, failures) recorded per batch. |
| Level 2 | Level 3 | Structured logging (JSON) with severity levels (ERROR, WARN, INFO, DEBUG). Key metrics defined and collected automatically: scrape success rate, data freshness, dashboard latency, error rate. Alerting configured for critical failures (scrape failure > 10%, dashboard down). Operational metrics dashboard. |
| Level 3 | Level 4 | Distributed tracing across scrape-ETL-dashboard pipeline with correlation IDs. Anomaly detection on key metrics (automatic, not just threshold-based). Monthly operational reviews using metrics data. Performance baselines established and tracked. Root cause analysis tooling available. |
| Level 4 | Level 5 | Predictive observability forecasts capacity needs and failure probability. Automated remediation for known failure patterns. Monitoring configuration version-controlled (observability-as-code). SLO-based alerting with error budgets. Annual observability benchmarking. |

---

## 7. Self-Assessment Methodology

### Assessment Process

1. **Preparation**: Research Director identifies assessment team (Data Engineer, Research Analyst, Legal Advisor). Gather project documentation (this model, ARC-001-DATA-v1.0, ARC-001-RISK-v1.0, codebase).
2. **Evidence Collection**: Review codebase, deployment configuration, logs, and operational records for each dimension. Interview team members about current practices.
3. **Scoring**: For each dimension, complete the questionnaire in Section 8 and compare against level definitions in Section 5. Assign the level where > 80% of characteristics are met.
4. **Validation**: Review scores with Research Director and Data Engineer. Resolve disagreements with additional evidence.
5. **Gap Analysis**: Compare current scores against target levels. Prioritise dimensions with largest gaps and highest business impact.
6. **Reporting**: Document findings in the Assessment Summary table below. Create radar chart for visual comparison.
7. **Action Planning**: Develop improvement initiatives using transition criteria in Section 6. Assign owners and timelines.

### Scoring Guidance

| Score | Meaning | Guidance |
|-------|---------|----------|
| 1 | Initial / Ad-Hoc | Assign if practices are largely absent or entirely person-dependent with no documentation |
| 2 | Repeatable | Assign if basic processes exist and work for known scenarios but are not standardised or consistently applied |
| 3 | Defined | Assign if processes are documented, standardised, and consistently applied across the platform |
| 4 | Managed | Assign if quantitative measurement is in place and decisions are driven by metrics and data |
| 5 | Optimised | Assign if continuous improvement is demonstrably embedded with innovation and automation |

### Assessment Summary

| Dimension ID | Dimension | Current Level | Target Level | Gap | Priority |
|--------------|-----------|---------------|--------------|-----|----------|
| DIM-01 | Data Quality Management | [1-5] | [1-5] | [+N] | HIGH |
| DIM-02 | Ethical Data Collection | [1-5] | [1-5] | [+N] | HIGH |
| DIM-03 | Data Integration & Interoperability | [1-5] | [1-5] | [+N] | MEDIUM |
| DIM-04 | Technology Operations | [1-5] | [1-5] | [+N] | MEDIUM |
| DIM-05 | Observability & Data-Driven Improvement | [1-5] | [1-5] | [+N] | HIGH |

---

## 8. Self-Assessment Questionnaire

Use the following questions to guide the assessment for each dimension. For each question, determine which answer best matches the organisation's current state. Score L2 as between L1 and L3; score L4 as between L3 and L5.

### DIM-01: Data Quality Management

| # | Question | L1 Answer | L3 Answer | L5 Answer |
|---|----------|-----------|-----------|-----------|
| 1 | How are scraped menu prices validated before storage? | No validation — raw text stored as extracted from HTML | Regex validation enforces decimal GBP format, range checks flag outliers (£0.50-£500), invalid prices quarantined for review | ML-based extraction validates prices against historical patterns and cross-references multiple page elements, achieving > 99% accuracy |
| 2 | How is duplicate data detected across scraping runs? | No duplicate detection — same items stored multiple times | Automated fuzzy matching on item name + restaurant + price with > 90% precision. Documented deduplication rules applied in ETL | Self-tuning deduplication model adapts to menu changes (renamed dishes, seasonal items) with < 0.1% false positive rate |
| 3 | How do you know the current completeness of your data? | We do not measure completeness — gaps discovered ad-hoc by users | Completeness metrics defined per entity (restaurants, menu items, prices) and measured weekly against > 95% target with documented thresholds | Real-time completeness dashboard with predictive alerts. Automated enrichment fills gaps from secondary sources within 24 hours |
| 4 | How are data normalisation standards enforced? | No standards — each scraper formats data differently | Controlled vocabularies for categories and dietary tags enforced in ETL. Title Case for names. ISO 8601 for all timestamps. Standards documented in ARC-001-DATA-v1.0 | Normalisation rules auto-generated from data profiling. New formats detected and normalisation rules proposed automatically. Annual review benchmarks against Schema.org Restaurant vocabulary |

### DIM-02: Ethical Data Collection

| # | Question | L1 Answer | L3 Answer | L5 Answer |
|---|----------|-----------|-----------|-----------|
| 1 | How does the scraper handle robots.txt directives? | Robots.txt is not checked — scraper accesses all URLs | Automated robots.txt parser checks every URL before request. Disallowed paths are logged and skipped. Parser tested against edge cases | Proactive robots.txt monitoring detects changes within 24 hours. API partnerships replace scraping for > 30% of sources. Compliance test suite runs in CI |
| 2 | What rate limiting is applied between requests? | No delays — requests sent as fast as possible | Configurable per-domain rate limiting with 5s minimum default and 10s for sensitive sites. Exponential backoff on HTTP 429. Polite hours scheduling available | Adaptive rate limiting adjusts based on server response times. Real-time compliance dashboard shows 100% adherence. Rate limits negotiated directly with restaurant platform operators |
| 3 | Can a restaurant opt out of data collection? | No opt-out mechanism exists | Published opt-out process (email address on public page). Requests processed within 48-hour SLA. Opt-out register maintained and checked before each scrape | Self-service opt-out portal. Automated processing in < 1 hour. Proactive annual review contacts restaurants to confirm continued consent. Published transparency report |
| 4 | Has a Data Protection Impact Assessment been completed? | No DPIA exists and no privacy review has been conducted | DPIA completed (ARC-001-DPIA-v1.0), approved by Legal Advisor, reviewed quarterly. Privacy risks assessed with mitigations documented. ICO registration confirmed | DPIA integrated into CI/CD — automated privacy impact check on code changes that modify data collection. Annual external privacy audit. Privacy-by-design patterns library maintained |

### DIM-03: Data Integration & Interoperability

| # | Question | L1 Answer | L3 Answer | L5 Answer |
|---|----------|-----------|-----------|-----------|
| 1 | How many external data sources are integrated? | Only web-scraped menu data — no external sources | 4+ sources integrated (FSA hygiene, Trustpilot, Google Places, Companies House) with documented matching algorithms and configurable thresholds | 6+ sources with pluggable integration framework. New source onboarded in < 1 day. ML entity resolution > 95% accuracy. Near-real-time feeds where available |
| 2 | What is the match rate between scraped restaurants and external sources? | Not applicable — no matching performed | FSA match rate > 60%. Google Places > 95%. Documented matching algorithm with scoring: name similarity (0-100) + postcode bonus (50) + address similarity (0-30). Thresholds: 0.60 minimum, 0.70 auto-match | ML matcher > 95% across all sources. Continuous learning from manual corrections. Match rate improvement tracked monthly. Published matching methodology |
| 3 | How does the dashboard access data? | Direct SQL queries embedded in Streamlit application code | API layer between dashboard and database. REST endpoints for restaurant/menu queries. Data cached with defined TTL (1 hour). JSON responses with consistent schema | GraphQL API with auto-generated documentation. Real-time subscriptions for data updates. SDK published for third-party developers. OpenAPI spec version-controlled |
| 4 | What data format standards are enforced? | No standards — mixed formats (dates as strings, prices with currency symbols) | All timestamps ISO 8601. Prices as decimal with separate currency field. Geographic data as lat/lon. Controlled vocabularies for categories. JSON Schema validation on API responses | Schema.org vocabulary alignment. Linked Data / JSON-LD for interoperability. Automated format compliance checking in CI. Published data dictionary auto-synced with code |

### DIM-04: Technology Operations

| # | Question | L1 Answer | L3 Answer | L5 Answer |
|---|----------|-----------|-----------|-----------|
| 1 | How is the application deployed? | Manual file copy to server via SSH or FTP | CI pipeline runs linting and checks on push. Automated deployment to Streamlit Cloud on merge to main. Infrastructure configuration in version control | Continuous deployment with feature flags. Zero-downtime deployments. Canary releases validate changes before full rollout. Self-healing infrastructure restarts failed services |
| 2 | What automated testing exists? | No automated tests — manual testing only | Automated test suite with > 70% coverage for business logic (ETL normalisation, validation rules, matching algorithms). Tests run on every CI build. Integration tests for API endpoints | 95%+ coverage including scraper resilience tests. Chaos engineering validates graceful degradation. Automated performance regression detection. Contract tests for all integrations |
| 3 | How are database schema changes managed? | SQL run directly on production database by developer | Migration SQL files version-controlled. Migration runner script applies changes in order. Rollback scripts exist for each migration. Automated backup before migration | Automated schema migration in deployment pipeline. Schema drift detection. Backward-compatible migrations only. Automated data validation post-migration |
| 4 | How are dependencies managed? | `pip install` with no version pinning — whatever is latest | `requirements.txt` with pinned versions. Dependency vulnerability scanning automated (Dependabot). Monthly review of dependency updates. Lock file for reproducible builds | Automated dependency update PRs with test validation. SBOM (Software Bill of Materials) generated. License compliance automated. Supply chain security verified (Sigstore) |

### DIM-05: Observability & Data-Driven Improvement

| # | Question | L1 Answer | L3 Answer | L5 Answer |
|---|----------|-----------|-----------|-----------|
| 1 | How are scraping failures detected? | Users report stale data — no proactive detection | Structured logging captures all scrape events. Alert fires when failure rate > 10%. Metrics dashboard shows per-restaurant scrape status and data freshness | Predictive model forecasts scrape failures based on website change patterns. Auto-remediation retries with alternative strategies. < 1 hour mean time to detection |
| 2 | What operational metrics are tracked? | None — no metrics collection in place | Key metrics defined and collected: scrape success rate, data freshness (hours), dashboard p95 latency, error rate, match rate per source. Operational dashboard updated daily | Comprehensive metrics with anomaly detection. Automated correlation between metrics (e.g., scrape failure causes data freshness degradation). Business metrics tied to operational health |
| 3 | How do you investigate data issues? | Read source code and print debug output. No logs or tracing available | Structured JSON logs with correlation IDs. Log aggregation searchable by restaurant, time range, component. Error logs include stack traces and context | Distributed tracing from scrape request through ETL to dashboard query. One-click root cause analysis. Automated runbooks for common issues. Post-incident review process |
| 4 | How are improvement decisions made? | Based on intuition and user complaints | Monthly operational review examines metrics trends. Improvement priorities based on data (highest error rate, worst data quality, slowest queries). Decisions documented | Continuous improvement embedded. A/B testing for pipeline changes. Error budget-based prioritisation. Quarterly benchmarking against industry. Improvement backlog auto-prioritised by impact |

---

## 9. Principle Traceability

This section maps architecture principles (from ARC-000-PRIN-v1.0) to maturity model dimensions, showing how each principle influences maturity expectations.

| Principle | Dimension Alignment | Maturity Implication |
|-----------|---------------------|----------------------|
| P-01: Data Quality First (FOUNDATIONAL) | DIM-01 (primary), DIM-05 | Sets the floor for DIM-01 at Level 3 minimum — validation, normalisation, and quality metrics are non-negotiable. DIM-05 must track quality metrics to verify compliance. |
| P-02: Open Source Preferred | DIM-04 | Technology Operations tooling should prefer open source (pytest, flake8, GitHub Actions free tier, Grafana). Proprietary tools require documented justification. |
| P-03: Ethical Web Scraping (NON-NEGOTIABLE) | DIM-02 (primary) | DIM-02 has a hard floor at Level 2 — robots.txt compliance and rate limiting are mandatory from day one. Target Level 3 within 6 months of any scraping activity. |
| P-04: Privacy by Design (NON-NEGOTIABLE) | DIM-02 (primary), DIM-01 | DPIA must be completed (DIM-02 Level 3). Data quality rules must include PII detection and filtering (DIM-01). No personal data stored without legal basis. |
| P-05: Scalability and Extensibility | DIM-03, DIM-04 | DIM-03 integration framework must support new sources without architectural rework. DIM-04 infrastructure must scale from 150 to 1,000+ restaurants. |
| P-06: Cost Efficiency | DIM-04, DIM-05 | Technology Operations must right-size infrastructure (DIM-04). Observability must track cost metrics alongside performance (DIM-05). Target < £100/month operational cost. |
| P-07: Single Source of Truth | DIM-01, DIM-03 | Each data entity has one authoritative source (DIM-01). Integration layer must clearly designate derived copies vs source of truth (DIM-03). |
| P-08: Data Lineage and Traceability | DIM-01, DIM-05 | Every data record must trace to source URL and timestamp (DIM-01 Level 2+). Observability must support lineage queries (DIM-05 Level 3+). |
| P-09: Data Normalisation and Consistency | DIM-01 (primary), DIM-03 | Normalisation rules defined and automated (DIM-01 Level 3). Standard formats enforced across all integrations (DIM-03 Level 3). |
| P-10: API-First Design | DIM-03 (primary) | API layer required between dashboard and database (DIM-03 Level 3). API versioning and documentation at Level 4. |
| P-11: Standard Data Formats | DIM-03 (primary) | ISO 8601, JSON Schema, GeoJSON, RFC 4180 CSV enforced across all data interchange (DIM-03 Level 3+). |
| P-12: Performance Targets | DIM-04, DIM-05 | Dashboard < 2s load, search < 500ms (DIM-04 Level 4 requires performance testing). DIM-05 must monitor latency percentiles. |
| P-13: Reliability and Availability | DIM-04 (primary), DIM-05 | 99% dashboard uptime (DIM-04 Level 3+). Graceful degradation tested (DIM-04 Level 4). Availability monitoring (DIM-05 Level 3+). |
| P-14: Maintainability and Documentation | DIM-04 (primary) | ADRs, README, runbooks required (DIM-04 Level 3). Automated tests > 70% coverage (DIM-04 Level 4). |
| P-15: Infrastructure as Code | DIM-04 (primary) | All infrastructure defined as code (DIM-04 Level 3). No manual production changes. Automated deployment pipeline. |
| P-16: Automated Testing | DIM-04 (primary) | Unit tests > 70% coverage (DIM-04 Level 4). Data quality tests on every ETL run (DIM-01 Level 3). CI blocks deployment on test failure. |
| P-17: CI/CD | DIM-04 (primary) | CI pipeline on every commit (DIM-04 Level 3). Automated deployment (DIM-04 Level 3). Quality gates enforced (DIM-04 Level 4). |
| P-18: Logging and Monitoring | DIM-05 (primary) | Structured logging (DIM-05 Level 3). Metrics dashboards (DIM-05 Level 3). Alerting on critical issues (DIM-05 Level 3). Correlation IDs (DIM-05 Level 4). |

### Coverage Analysis

**Dimensions without strong principle coverage**: None — all 5 dimensions are covered by multiple principles.

**Principles with strongest dimension coverage**:
- P-01 (Data Quality First) — influences DIM-01 and DIM-05
- P-03 (Ethical Web Scraping) — drives DIM-02 as non-negotiable
- P-04 (Privacy by Design) — drives DIM-02 with DPIA requirement

**Principle-driven minimum maturity floors**:
- DIM-01: Level 3 (driven by P-01 Data Quality First)
- DIM-02: Level 3 (driven by P-03 Ethical Scraping and P-04 Privacy, both non-negotiable)
- DIM-03: Level 3 (driven by P-10 API-First and P-11 Standard Formats)
- DIM-04: Level 3 (driven by P-15 IaC, P-16 Testing, P-17 CI/CD)
- DIM-05: Level 3 (driven by P-18 Logging and Monitoring)

---

## 10. Glossary

| Term | Definition |
|------|------------|
| Completeness | Percentage of required data fields that contain valid, non-null values across all records in an entity |
| Data Freshness | Time elapsed since data was last collected or verified from the original source |
| Entity Resolution | Process of determining whether records from different sources refer to the same real-world entity (e.g., matching FSA establishment to scraped restaurant) |
| ETL | Extract, Transform, Load — the pipeline that collects raw data, applies normalisation and validation, and stores it in the database |
| Fuzzy Matching | Approximate string matching algorithm that scores similarity between text values (e.g., restaurant names) to identify probable matches across data sources |
| Opt-Out | Process by which a restaurant can request removal of their data from the platform |
| Robots.txt | Standard file on websites that specifies which pages web crawlers are allowed or disallowed from accessing |
| SLA | Service Level Agreement — a defined target for a metric (e.g., > 95% data completeness, < 2s page load time) |
| SLO | Service Level Objective — an internal target that is typically stricter than the external SLA |

---

## 11. External References

| Reference | Type | Source | Relevance |
|-----------|------|--------|-----------|
| CMMI Institute - Capability Maturity Model Integration | Framework | ISACA / CMMI Institute | Foundational maturity model methodology adapted for this project-specific context |
| HM Treasury Orange Book (2023) | Guidance | HM Treasury | Risk management framework referenced in ARC-001-RISK-v1.0, informing risk-related maturity criteria |
| UK GDPR / Data Protection Act 2018 | Standard | UK Government / ICO | Legal compliance requirements underpinning DIM-02 ethical data collection and privacy maturity |
| Food Standards Agency FHRS Open Data | Standard | Food Standards Agency | Primary external data source, integration maturity measured in DIM-03 |
| DAMA DMBOK (Data Management Body of Knowledge) | Framework | DAMA International | Industry standard for data management maturity, informing DIM-01 data quality dimension design |

---

**Generated by**: ArcKit `/arckit:maturity-model` command
**Generated on**: 2026-03-08 GMT
**ArcKit Version**: 4.0.1
**Project**: Plymouth Research Restaurant Menu Analytics (Project 001)
**AI Model**: Claude Opus 4.6 (claude-opus-4-6)
**Generation Context**: Synthesised from ARC-000-PRIN-v1.0 (18 principles), ARC-001-REQ-v2.0 (requirements), ARC-001-STKE-v1.0 (stakeholders), ARC-001-RISK-v1.0 (20 risks), ARC-001-DATA-v1.0 (8 entities, 142 attributes)
