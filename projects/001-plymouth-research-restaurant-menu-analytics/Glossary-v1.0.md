# Glossary: Plymouth Research Restaurant Menu Analytics

> **Template Origin**: Official | **ArcKit Version**: 4.0.1 | **Command**: `/arckit:glossary`

## Document Control

| Field | Value |
|-------|-------|
| **Document ID** | ARC-001-GLOS-v1.0 |
| **Document Type** | Project Glossary |
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
| 1.0 | 2026-03-08 | ArcKit AI | Initial creation from `/arckit:glossary` command | PENDING | PENDING |

---

## Purpose

This glossary provides a single, authoritative reference for all terminology, acronyms, and abbreviations used within the Plymouth Research Restaurant Menu Analytics project. It ensures consistent understanding across all stakeholders, reduces ambiguity in architecture artifacts, and supports onboarding of new team members.

**Scope**: All terms, acronyms, and abbreviations referenced in project architecture documents, requirements, designs, and communications.

**Authority**: Enterprise Architecture team, with contributions from all project workstreams.

**Usage**: All project documentation SHOULD reference this glossary for canonical definitions. When a term has a project-specific meaning that differs from common usage, the glossary definition takes precedence.

---

## Conventions

- Terms are listed in **alphabetical order** within each section
- **Bold** terms within definitions indicate cross-references to other glossary entries
- The **Source Artifact** column references the document where the term was first defined or is most relevant
- The **Category** column classifies terms to aid filtering and navigation
- Acronyms and abbreviations are listed separately for quick lookup
- Where a term has multiple meanings in different contexts, each meaning is listed as a separate row with the context noted

---

## Glossary

### Business Terms

| Term | Definition | Source Artifact | Category |
|------|------------|-----------------|----------|
| Auto-match | A match between records from two data sources that is automatically accepted because the confidence score exceeds the auto-match threshold (0.70). Contrasted with manual matching. | ARC-001-REQ-v2.0 | Business |
| Build vs Buy Analysis | Evaluation methodology comparing the cost, risk, and capability of building a solution in-house versus purchasing a commercial product or using open source software. Includes **TCO** comparison. | ARC-001-RSCH-v1.0 | Business |
| Coverage | The percentage of restaurants in the platform that have data from a specific external source (e.g., "FSA coverage: 50%" means 49 of 98 restaurants have hygiene ratings). | ARC-001-DSCT-v1.0 | Business |
| Cuisine Type | Classification of a restaurant by the style of food served (e.g., Italian, Indian, Chinese, British). Stored as a text field on the restaurants entity. | ARC-001-DATA-v1.0 | Business |
| Data Freshness | The elapsed time since data was last collected or verified from its original source. Stale data is flagged when older than 7 days for menu items. | ARC-000-PRIN-v1.0 | Business |
| Data Source | An external provider of data integrated into the platform. Current sources include **FSA**, **Trustpilot**, **Google Places**, **Companies House**, **ONS**, **VOA**, **Postcodes.io**, and **Plymouth City Council**. | ARC-001-DSCT-v1.0 | Business |
| Dietary Tag | A label indicating dietary suitability of a menu item: Vegan, Vegetarian, Gluten-Free, Dairy-Free, or Nut-Free. Extracted during scraping and stored as boolean flags. | ARC-001-DATA-v1.0 | Business |
| Food Hygiene Rating | A score from 0 to 5 assigned by the **FSA** following an inspection of a food business. 5 = Very Good, 0 = Urgent Improvement Necessary. | ARC-001-STKE-v1.0 | Business |
| High Confidence Match | A fuzzy match between data sources with a confidence score of 0.95 or above, indicating near-certain correspondence between records. | ARC-001-REQ-v2.0 | Business |
| Match Rate | The percentage of restaurants in the platform successfully matched to records in an external data source. Current FSA match rate is 50% (49/98). | ARC-001-DSCT-v1.0 | Business |
| Menu Item | An individual food or drink offering at a restaurant, with attributes including name, price, category, description, and dietary tags. The platform tracks 2,625 menu items. | ARC-001-DATA-v1.0 | Business |
| Opt-Out | The mechanism by which a restaurant can request removal of their data from the platform. Requests must be processed within 48 hours. | ARC-000-PRIN-v1.0 | Business |
| Price Range | A classification of restaurant price level using pound symbols: £ (budget), ££ (moderate), £££ (premium), ££££ (luxury). | ARC-001-DATA-v1.0 | Business |
| Restaurant | The primary entity in the data model representing a food or drink establishment in Plymouth, UK. Each restaurant has a unique `restaurant_id` and up to 52 attributes across core, hygiene, review, and Google metadata fields. | ARC-001-DATA-v1.0 | Business |

### Technical Terms

| Term | Definition | Source Artifact | Category |
|------|------------|-----------------|----------|
| API-First Design | Architecture principle requiring all data access to go through well-defined API endpoints rather than direct database queries, enabling future integrations and mobile apps. | ARC-000-PRIN-v1.0 | Technical |
| BeautifulSoup | Python library for parsing HTML and XML documents, used as the primary web scraping tool for extracting menu data from restaurant websites. | ARC-001-RSCH-v1.0 | Technical |
| Blue-Green Deployment | Deployment strategy using two identical production environments. Traffic is switched from the current (blue) to the new (green) environment after validation, enabling instant rollback. | ARC-001-RSCH-v1.0 | Technical |
| Cache TTL | Time To Live for cached data. The dashboard uses a 5-minute TTL for Streamlit's `@st.cache_data` and the data loader uses a 1-hour TTL for query results. | ARC-001-REQ-v2.0 | Technical |
| Canary Deployment | Deployment strategy where a new version is rolled out to a small subset of users before full deployment, allowing early detection of issues. | ARC-001-RSCH-v1.0 | Technical |
| Controlled Vocabulary | A predefined, standardised set of terms used for data categorisation. The platform uses controlled vocabularies for menu categories (Starters, Mains, Desserts, Drinks) and dietary tags. | ARC-000-PRIN-v1.0 | Technical |
| Correlation ID | A unique identifier propagated across all components of a request (scrape, ETL, dashboard query) to enable distributed tracing and debugging. | ARC-000-PRIN-v1.0 | Technical |
| DuckDB | An in-process analytical database engine recommended as a future analytics layer enhancement alongside the existing **SQLite** database. Selected for column-oriented analytics performance. | ARC-001-RSCH-v1.0 | Technical |
| Entity Resolution | The process of determining whether records from different data sources refer to the same real-world entity. In this project, matching scraped restaurants to FSA establishments, Trustpilot profiles, and Google Places entries. | ARC-001-DATA-v1.0 | Technical |
| Exponential Backoff | A retry strategy where the wait time between retries increases exponentially (e.g., 1s, 2s, 4s, 8s). Used when encountering HTTP 429 (Too Many Requests) responses during scraping. | ARC-000-PRIN-v1.0 | Technical |
| Full-Text Search | Database indexing technique enabling natural language search across text fields. Implemented in SQLite for searching restaurant names and menu items. | ARC-001-REQ-v2.0 | Technical |
| Fuzzy Matching | Approximate string matching algorithm using `difflib.SequenceMatcher` to score similarity between text values. Used to match restaurant records across data sources. Scoring: name similarity (0-100 pts), postcode bonus (50 pts), address similarity (0-30 pts). | ARC-001-DATA-v1.0 | Technical |
| Geocoding | The process of converting addresses or postcodes to geographic coordinates (latitude/longitude). Performed using **Postcodes.io** and **Google Places** APIs. | ARC-001-DSCT-v1.0 | Technical |
| GeoJSON | An open standard format for encoding geographic data structures based on JSON. Used for restaurant location data interchange. | ARC-000-PRIN-v1.0 | Technical |
| Graceful Degradation | Design pattern where a system continues to function with reduced capability when a component fails. The dashboard shows cached data with a staleness warning if the database is unavailable. | ARC-000-PRIN-v1.0 | Technical |
| Infrastructure as Code | Principle requiring all infrastructure to be defined as version-controlled code rather than manual configuration. Deployment scripts, database migrations, and server configurations must be in Git. | ARC-000-PRIN-v1.0 | Technical |
| JSON Schema | A vocabulary for annotating and validating JSON documents. Used to define and enforce data format standards for API responses. | ARC-000-PRIN-v1.0 | Technical |
| Loguru | Python logging library recommended for structured logging. Provides JSON output, log rotation, and severity filtering. | ARC-001-RSCH-v1.0 | Technical |
| Normalisation | The process of converting data into a consistent, standard format. Examples: prices to decimal GBP, names to Title Case, dates to **ISO 8601**, categories to controlled vocabularies. | ARC-000-PRIN-v1.0 | Technical |
| Pandas | Python data manipulation library used for data processing, transformation, and analysis in the ETL pipeline and dashboard. | ARC-001-RSCH-v1.0 | Technical |
| Plotly | JavaScript-based graphing library with Python bindings, used for interactive charts and visualisations in the Streamlit dashboard. | ARC-001-RSCH-v1.0 | Technical |
| Postcodes.io | Free, open source UK postcode lookup and geocoding API. Provides postcode to latitude/longitude conversion, nearest postcode lookup, and geographic metadata. No authentication required. | ARC-001-DSCT-v1.0 | Technical |
| Pydeck | Python library for large-scale spatial visualisations, used for restaurant location maps in the dashboard. | ARC-001-RSCH-v1.0 | Technical |
| Rate Limiting | The practice of restricting the frequency of requests to external services. The platform enforces a minimum 5-second delay between requests per domain, with 2.5s between Trustpilot pages and 5s between restaurants. | ARC-000-PRIN-v1.0 | Technical |
| Render | Cloud application hosting platform identified as the fallback deployment option if Streamlit Community Cloud is insufficient. Free tier available. | ARC-001-RSCH-v1.0 | Technical |
| Robots.txt | A standard file placed at the root of a website that specifies which paths web crawlers are permitted or forbidden from accessing. Compliance is **non-negotiable** per Principle 3. | ARC-000-PRIN-v1.0 | Technical |
| Scrapy | Python web scraping framework recommended as a future enhancement for scaled scraping. Provides built-in rate limiting, robots.txt compliance, and concurrent request management. | ARC-001-RSCH-v1.0 | Technical |
| Sentry | Application monitoring and error tracking platform. Recommended for production error monitoring with the free Developer tier. | ARC-001-RSCH-v1.0 | Technical |
| Single Source of Truth | Principle requiring every data domain to have exactly one authoritative source. Derived copies must be clearly labelled as read-only caches synchronised from the source. | ARC-000-PRIN-v1.0 | Technical |
| SQLite | Embedded relational database used as the primary data store. The `plymouth_research.db` file is approximately 20 MB with tables for restaurants (243 rows), menu items (2,625 rows), and reviews (9,891 rows). | ARC-001-DATA-v1.0 | Technical |
| Streamlit | Open source Python framework for building data applications. Used as the primary dashboard framework, deployed on Streamlit Community Cloud. | ARC-001-RSCH-v1.0 | Technical |
| UptimeRobot | Free website monitoring service recommended for dashboard availability monitoring. Checks every 5 minutes with email/Slack alerting. | ARC-001-RSCH-v1.0 | Technical |
| User-Agent | HTTP header identifying the client making a request. The platform uses "PlymouthResearchMenuScraper/1.0" with a contact email as required by ethical scraping principles. | ARC-000-PRIN-v1.0 | Technical |
| Web Scraping | The automated extraction of data from websites. The platform scrapes restaurant menu pages to collect names, prices, descriptions, categories, and dietary information. | ARC-000-PRIN-v1.0 | Technical |

### Data Terms

| Term | Definition | Source Artifact | Category |
|------|------------|-----------------|----------|
| Data Classification | Categorisation of data by sensitivity level. The platform uses: Public (7 entities — business data, government open data), Internal (1 entity — operational metrics), Confidential (0), Restricted (0). | ARC-001-DATA-v1.0 | Data |
| Data Custodian | Technical role responsible for managing the database, scraping pipelines, and backup procedures. Held by the Data Engineer. | ARC-001-DATA-v1.0 | Data |
| Data Lineage | The ability to trace data from its original source (restaurant website URL, scrape timestamp) through all transformations to its final presentation in the dashboard. Required by Principle 8. | ARC-000-PRIN-v1.0 | Data |
| Data Owner | Business role accountable for data quality, coverage targets, and ethical compliance. Held by the Research Director. | ARC-001-DATA-v1.0 | Data |
| Data Quality Dimensions | The five measurable aspects of data quality tracked by the platform: Completeness (no unexpected nulls), Accuracy (correct price extraction), Consistency (standardised normalisation), Timeliness (freshness tracking), and Uniqueness (duplicate detection). | ARC-000-PRIN-v1.0 | Data |
| Data Retention | The period for which data is stored before deletion. Historical menu and review data: 12 months. Active restaurant master data: permanent. Post-opt-out data: 30 days then hard delete. | ARC-001-DPIA-v1.0 | Data |
| Data Steward | Role responsible for data governance policies, opt-out processing, and correction requests. Held by the Product Owner. | ARC-001-DATA-v1.0 | Data |
| Drinks Table | Database entity storing beverage data with categories, linked to restaurants by `restaurant_id`. | ARC-001-DATA-v1.0 | Data |
| ETL Pipeline | Extract, Transform, Load — the data processing pipeline that collects raw data from sources, applies validation and normalisation, and loads it into the SQLite database. | ARC-000-PRIN-v1.0 | Data |
| Google Reviews Table | Database entity storing up to 5 reviews per restaurant from the Google Places API (481 total rows). Linked to restaurants by `restaurant_id`. | ARC-001-DATA-v1.0 | Data |
| Manual Matches Table | Database entity recording human-verified matches between scraped restaurants and external data sources, used to improve automated matching over time. | ARC-001-DATA-v1.0 | Data |
| Menu Items Table | Database entity storing individual food/drink offerings (2,625 rows, 13 columns) including name, price, category, description, and dietary flags. Linked to restaurants by `restaurant_id`. | ARC-001-DATA-v1.0 | Data |
| Restaurants Table | Master data entity with 243 rows and 52 columns spanning core fields, FSA hygiene (9 columns), Trustpilot (5 columns), Google Places (16 columns), and Google contact/location fields. Primary key: `restaurant_id`. | ARC-001-DATA-v1.0 | Data |
| Scraping Audit Log | Database entity tracking scraping operations per restaurant, including timestamps, success/failure status, and error details. Used for compliance monitoring and troubleshooting. | ARC-001-DATA-v1.0 | Data |
| Trustpilot Reviews Table | Database entity storing customer reviews scraped from Trustpilot (9,410 rows, 13 columns). Includes rating (1-5), review text, author name, and scrape metadata. Linked by `restaurant_id` with cascade delete. | ARC-001-DATA-v1.0 | Data |

### Governance Terms

| Term | Definition | Source Artifact | Category |
|------|------------|-----------------|----------|
| 4Ts Framework | Risk response framework: Tolerate (accept the risk), Treat (mitigate the risk), Transfer (share the risk), Terminate (avoid the risk). Used in the risk register for response planning. | ARC-001-RISK-v1.0 | Governance |
| Architecture Decision Record | A documented record of a significant architecture decision including context, options considered, decision rationale, and consequences. Two ADRs exist: ADR-001 (Azure cloud platform) and ADR-002 (data quality governance framework). | ARC-001-ADR-001-v1.0 | Governance |
| Architecture Review Board | Governance body responsible for reviewing and approving architecture decisions, principle exceptions, and technology selections. | ARC-000-PRIN-v1.0 | Governance |
| Confidence Threshold | The minimum fuzzy matching score required for a match to be accepted. Three tiers: 0.60 (minimum consideration), 0.70 (auto-match), 0.95 (high confidence). | ARC-001-REQ-v2.0 | Governance |
| Exception Process | Formal procedure for requesting a deviation from architecture principles. Requires justification, compensating controls, risk assessment, expiration date, and remediation plan. Not permitted for Principles 3 (Ethical Scraping) and 4 (Privacy by Design). | ARC-000-PRIN-v1.0 | Governance |
| Inherent Risk | The risk level before any controls or mitigations are applied. Total inherent risk score for the project: 455/500. | ARC-001-RISK-v1.0 | Governance |
| MoSCoW Prioritisation | Requirements prioritisation method: Must have, Should have, Could have, Won't have (this time). Used throughout ARC-001-REQ-v2.0. | ARC-001-REQ-v2.0 | Governance |
| Orange Book | HM Treasury publication "Management of Risk: Principles and Concepts" (2023 edition). The risk management framework used for the project risk register. | ARC-001-RISK-v1.0 | Governance |
| Residual Risk | The risk level remaining after controls and mitigations are applied. Total residual risk score: 232/500, representing a 49% reduction from inherent risk. | ARC-001-RISK-v1.0 | Governance |
| Risk Appetite | The level of risk an organisation is willing to accept in pursuit of its objectives. Reassessed quarterly per the risk register governance framework. | ARC-001-RISK-v1.0 | Governance |
| Validation Gate | A checklist of conditions that must be satisfied before proceeding past a project milestone. Each architecture principle defines specific validation gates. | ARC-000-PRIN-v1.0 | Governance |

### Security & Compliance Terms

| Term | Definition | Source Artifact | Category |
|------|------------|-----------------|----------|
| Computer Misuse Act 1990 | UK legislation making it an offence to access computer systems without authorisation. Relevant to web scraping practices — the platform must ensure all scraping is of publicly accessible data. | ARC-000-PRIN-v1.0 | Security |
| Copyright, Designs and Patents Act 1988 | UK copyright legislation. The platform scrapes only factual data (prices, menu items) and does not copy substantial creative content from restaurant websites. | ARC-000-PRIN-v1.0 | Security |
| Data Minimisation | GDPR principle requiring that only the minimum necessary data is collected and processed. The platform collects only public business data — no customer PII, no personal data. | ARC-001-DPIA-v1.0 | Security |
| Data Protection Impact Assessment | Systematic process to identify and minimise data protection risks. ARC-001-DPIA-v1.0 concluded LOW RISK with no significant privacy risks. ICO prior consultation not required. | ARC-001-DPIA-v1.0 | Security |
| ICO 9-Criteria Screening | Assessment framework from the UK Information Commissioner's Office used to determine whether a DPIA is legally required. The project meets 1 of 9 criteria (matching datasets), below the threshold of 2. | ARC-001-DPIA-v1.0 | Security |
| Lawful Basis | One of six legal grounds under GDPR Article 6 for processing personal data. The platform relies on Legitimate Interests (Article 6(1)(f)) for processing public business data. | ARC-001-DPIA-v1.0 | Security |
| Legitimate Interests | GDPR lawful basis (Article 6(1)(f)) where processing is necessary for legitimate interests pursued by the controller, provided those interests are not overridden by the data subject's rights. Used as the legal basis for restaurant data aggregation. | ARC-001-DPIA-v1.0 | Security |
| Open Government Licence | UK government licence permitting free use, sharing, and adaptation of public sector data. FSA hygiene ratings, ONS geography, and VOA business rates data are published under OGL v3.0. | ARC-001-DSCT-v1.0 | Security |
| Right to Erasure | GDPR Article 17 right allowing data subjects to request deletion of their personal data. Implemented as the restaurant opt-out mechanism with 48-hour processing SLA and 30-day hard delete. | ARC-001-DPIA-v1.0 | Security |
| UK GDPR | The UK's retained version of the EU General Data Protection Regulation, as incorporated by the Data Protection Act 2018. Governs all data processing activities of the platform. | ARC-001-DPIA-v1.0 | Security |

### Financial Terms

| Term | Definition | Source Artifact | Category |
|------|------------|-----------------|----------|
| Free Tier | A usage level offered by cloud services at no cost, typically with limits on requests, storage, or features. The platform operates entirely within free tiers: Streamlit Cloud, Google Places API (free allowance), UptimeRobot, Sentry Developer. | ARC-001-RSCH-v1.0 | Financial |
| Right-Sizing | Cost optimisation practice of matching infrastructure capacity to actual workload requirements. The platform avoids over-provisioning by starting with SQLite and free-tier hosting. | ARC-000-PRIN-v1.0 | Financial |
| Total Cost of Ownership | The complete cost of a technology solution over its lifetime, including licensing, infrastructure, maintenance, training, and operational overhead. Estimated 3-year TCO for the recommended stack: £0-£300. | ARC-001-RSCH-v1.0 | Financial |

### Requirement ID Prefixes

| Prefix | Meaning | Source Artifact | Category |
|--------|---------|-----------------|----------|
| BC | Business Constraint — a non-negotiable boundary condition on the project (e.g., BC-2: single developer maintainability). | ARC-001-REQ-v2.0 | Governance |
| BR | Business Requirement — a high-level business need the system must satisfy (e.g., BR-001 to BR-007). | ARC-001-REQ-v2.0 | Governance |
| DR | Data Requirement — a requirement relating to data collection, storage, quality, or governance (e.g., DR-001 to DR-006). | ARC-001-REQ-v2.0 | Governance |
| FR | Functional Requirement — a specific system behaviour or feature (e.g., FR-001 onwards). | ARC-001-REQ-v2.0 | Governance |
| INT | Integration Requirement — a requirement for connecting with an external system or data source. | ARC-001-REQ-v2.0 | Governance |
| NFR | Non-Functional Requirement — a quality attribute requirement. Sub-prefixes: NFR-P (Performance), NFR-SEC (Security), NFR-A (Availability), NFR-M (Maintainability), NFR-O (Observability), NFR-C (Compliance). | ARC-001-REQ-v2.0 | Governance |
| UC | Use Case — a user interaction scenario (e.g., UC-001 to UC-011). | ARC-001-REQ-v2.0 | Governance |

---

## Acronyms & Abbreviations

| Acronym | Expansion | Context |
|---------|-----------|---------|
| ADR | Architecture Decision Record | Governance document recording key technology and design decisions |
| API | Application Programming Interface | Standard interface for programmatic data access between systems |
| CI/CD | Continuous Integration / Continuous Deployment | Automated build, test, and deployment pipeline |
| CMMI | Capability Maturity Model Integration | Framework for assessing organisational process maturity |
| CSV | Comma-Separated Values | Data interchange format (RFC 4180) |
| DPIA | Data Protection Impact Assessment | GDPR Article 35 assessment of data protection risks |
| DPA | Data Protection Act (2018) | UK legislation implementing GDPR |
| DSCT | Data Source Discovery (DataScout) | ArcKit artifact type for external data source research |
| ERD | Entity-Relationship Diagram | Visual representation of data model entities and their relationships |
| ETL | Extract, Transform, Load | Data pipeline pattern for collecting and processing data |
| FHRS | Food Hygiene Rating Scheme | FSA scheme for rating food business hygiene (0-5 scale) |
| FSA | Food Standards Agency | UK government body responsible for food safety and hygiene regulation |
| GBP | British Pound Sterling | Currency used for all price data (ISO 4217: GBP) |
| GDPR | General Data Protection Regulation | EU/UK data protection regulation governing personal data processing |
| GPS | Global Positioning System | Satellite navigation providing latitude/longitude coordinates |
| HTML | HyperText Markup Language | Standard markup language for web pages, parsed during scraping |
| HTTP | HyperText Transfer Protocol | Application protocol for web communication |
| IaC | Infrastructure as Code | Practice of defining infrastructure in version-controlled code |
| ICO | Information Commissioner's Office | UK independent authority upholding data privacy rights |
| ISO 8601 | International date/time format standard | Used for all timestamps: YYYY-MM-DDTHH:MM:SSZ |
| JSON | JavaScript Object Notation | Lightweight data interchange format |
| ML | Machine Learning | AI techniques for pattern recognition and prediction |
| MVP | Minimum Viable Product | Smallest product release that delivers core value |
| NFR | Non-Functional Requirement | Quality attribute requirement (performance, security, etc.) |
| OGL | Open Government Licence | UK licence for free use of public sector data (version 3.0) |
| ONS | Office for National Statistics | UK government statistical body providing geography and demographic data |
| OSS | Open Source Software | Software with source code freely available for use and modification |
| PII | Personally Identifiable Information | Data that can identify an individual — not collected by this platform |
| RACI | Responsible, Accountable, Consulted, Informed | Stakeholder responsibility assignment matrix |
| REST | Representational State Transfer | Architectural style for designing networked APIs |
| SLA | Service Level Agreement | Defined target for a service metric (e.g., > 95% completeness) |
| SLO | Service Level Objective | Internal performance target, typically stricter than the SLA |
| SQL | Structured Query Language | Standard language for relational database operations |
| TCO | Total Cost of Ownership | Complete lifetime cost of a technology solution |
| ToS | Terms of Service | Legal agreement governing use of a website or service |
| TTL | Time To Live | Duration for which cached data remains valid before refresh |
| UK GDPR | United Kingdom General Data Protection Regulation | UK-retained version of EU GDPR, incorporated via DPA 2018 |
| URL | Uniform Resource Locator | Web address identifying a resource |
| VOA | Valuation Office Agency | UK government agency providing business rates valuations |
| XML | Extensible Markup Language | Data format used by FSA for hygiene rating data files |

---

## Standards Reference Table

| Standard | Version | Relevance | URL |
|----------|---------|-----------|-----|
| UK GDPR / Data Protection Act 2018 | 2018 | Governs all data processing; lawful basis, data minimisation, retention, breach notification | N/A (UK legislation) |
| UK Computer Misuse Act 1990 | 1990 | Ensures web scraping does not constitute unauthorised computer access | N/A (UK legislation) |
| UK Copyright, Designs and Patents Act 1988 | 1988 | Limits scraping to factual data; prohibits copying creative content | N/A (UK legislation) |
| HM Treasury Orange Book | 2023 | Risk management framework used for the project risk register (ARC-001-RISK-v1.0) | N/A (HM Treasury) |
| Open Government Licence | v3.0 | Licence for FSA, ONS, and VOA open data used by the platform | N/A (National Archives) |
| ISO 8601 | 2019 | Date/time format standard for all timestamps in the platform | N/A (ISO) |
| RFC 4180 | 2005 | CSV format standard for data exports | N/A (IETF) |
| GeoJSON | RFC 7946 | Standard format for geographic data interchange | N/A (IETF) |
| JSON Schema | Draft 2020-12 | Vocabulary for validating JSON API responses | N/A (json-schema.org) |
| FSA Food Hygiene Rating Scheme | Current | Hygiene rating methodology (0-5 scale) for food businesses | N/A (FSA) |

---

## Traceability

This glossary was compiled from terms found in the following architecture artifacts:

| Document | Document ID | Terms Contributed |
|----------|-------------|-------------------|
| Architecture Principles | ARC-000-PRIN-v1.0 | 22 terms |
| Requirements Specification | ARC-001-REQ-v2.0 | 12 terms |
| Data Model | ARC-001-DATA-v1.0 | 16 terms |
| Stakeholder Analysis | ARC-001-STKE-v1.0 | 3 terms |
| Risk Register | ARC-001-RISK-v1.0 | 6 terms |
| DPIA | ARC-001-DPIA-v1.0 | 8 terms |
| Data Source Discovery | ARC-001-DSCT-v1.0 | 5 terms |
| Research Findings | ARC-001-RSCH-v1.0 | 12 terms |
| ADR-001 (Azure Cloud Platform) | ARC-001-ADR-001-v1.0 | 2 terms |
| ADR-002 (Data Quality Governance) | ARC-001-ADR-002-v1.0 | 1 term |

---

## Maintenance

This glossary is a **living document** that should be updated when:

- New architecture artifacts are created (run `/arckit:glossary` to regenerate)
- New external data sources are integrated
- Terminology is refined through stakeholder feedback
- New acronyms or standards are introduced to the project

---

**Generated by**: ArcKit `/arckit:glossary` command
**Generated on**: 2026-03-08 GMT
**ArcKit Version**: 4.0.1
**Project**: Plymouth Research Restaurant Menu Analytics (Project 001)
**AI Model**: Claude Opus 4.6 (claude-opus-4-6)
**Generation Context**: Synthesised from 10 project artifacts (ARC-000-PRIN-v1.0, ARC-001-REQ-v2.0, ARC-001-DATA-v1.0, ARC-001-STKE-v1.0, ARC-001-RISK-v1.0, ARC-001-DPIA-v1.0, ARC-001-DSCT-v1.0, ARC-001-RSCH-v1.0, ARC-001-ADR-001-v1.0, ARC-001-ADR-002-v1.0)
