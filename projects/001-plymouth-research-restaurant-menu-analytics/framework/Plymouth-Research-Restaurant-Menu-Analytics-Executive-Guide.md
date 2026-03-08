# Plymouth Research Restaurant Menu Analytics -- Executive Guide

## Document Control

| Field | Value |
|-------|-------|
| **Title** | Executive Guide: Plymouth Research Restaurant Menu Analytics |
| **Project** | Plymouth Research Restaurant Menu Analytics (Project 001) |
| **Date** | 2026-03-08 |
| **Version** | 1.0 |
| **Classification** | OFFICIAL |
| **Author** | AI Agent |
| **Audience** | Executive sponsors, senior stakeholders, non-technical decision-makers |

---

## Executive Summary

The Plymouth Research Restaurant Menu Analytics platform is an independent research tool that provides comprehensive, searchable data on restaurants and bars across Plymouth, UK. It aggregates publicly available information -- menus, prices, food hygiene ratings, customer reviews, and business data -- from multiple authoritative sources into a single interactive dashboard.

The platform currently covers 98 restaurants with 2,625 menu items, integrates Food Standards Agency hygiene ratings, over 9,400 Trustpilot reviews, and Google Places data. It operates on an entirely open-source technology stack (Python, SQLite, Streamlit) with zero licensing costs and a target operational budget of under 100 GBP per month. All data collection follows strict ethical web scraping principles and full UK GDPR compliance -- no personal data is collected.

This guide provides a structured walkthrough of the 24 architecture documents that govern the platform. These documents are organised into 5 phases covering everything from foundational principles through to delivery planning. The framework ensures that every technology decision, data handling practice, and compliance measure is documented, traceable, and aligned to stakeholder goals.

---

## Requirements Alignment

The following table maps the key business requirements to their framework coverage, demonstrating that all requirements are addressed within the architecture documentation.

| Requirement Area | Framework Coverage | Key Documents |
|------------------|-------------------|---------------|
| Comprehensive restaurant data (150+ establishments) | Data model defines 8 entities; 22 data sources evaluated; 98 restaurants currently covered | ARC-001-DATA-v1.0, ARC-001-DSCT-v1.0 |
| Multi-source data aggregation (FSA, Trustpilot, Google) | Integration requirements specified; data sources discovered and evaluated | ARC-001-REQ-v2.0 (INT-001 to INT-005), ARC-001-DSCT-v1.0 |
| Ethical and legal data collection | Non-negotiable principles defined; DPIA completed; risks assessed | ARC-000-PRIN-v1.0 (Principles 3-4), ARC-001-DPIA-v1.0, ARC-001-RISK-v1.0 |
| Cost-effective operation ( < 100 GBP/month) | Technology research evaluates TCO across 3 cloud providers; open-source stack selected | ARC-001-RSCH-v1.0, ARC-001-AWRS, ARC-001-AZRS, ARC-001-GCRS |
| Data quality and accuracy (95%+ target) | Principles mandate data quality first; ADR formalises governance framework | ARC-000-PRIN-v1.0 (Principle 1), ARC-001-ADR-002-v1.0 |
| Interactive dashboard with search and filtering | Functional requirements specify dashboard features; backlog plans delivery | ARC-001-REQ-v2.0 (FR-001 to FR-011), ARC-001-BKLG-v1.0 |
| GDPR and UK regulatory compliance | DPIA confirms low risk; privacy principles enforced; opt-out mechanism designed | ARC-001-DPIA-v1.0, ARC-000-PRIN-v1.0 (Principle 4) |
| Scalability (Plymouth to UK-wide) | Principles require 10x capacity design; cloud research evaluates scaling options | ARC-000-PRIN-v1.0 (Principle 5), ARC-001-AWRS/AZRS/GCRS |

---

## Document Map

All 24 architecture artifacts are organised into 5 phases. Each phase builds on the previous one.

### Phase 1: Foundation (2 documents)

| Document ID | Title |
|-------------|-------|
| ARC-000-PRIN-v1.0 | Plymouth Research Enterprise Architecture Principles |
| ARC-001-STKE-v1.0 | Stakeholder Drivers & Goals Analysis |

### Phase 2: Requirements and Data (4 documents)

| Document ID | Title |
|-------------|-------|
| ARC-001-REQ-v1.0 | Business and Technical Requirements Specification v1.0 |
| ARC-001-REQ-v2.0 | Business and Technical Requirements Specification v2.0 |
| ARC-001-DATA-v1.0 | Data Model |
| ARC-001-DSCT-v1.0 | Data Source Discovery |

### Phase 3: Architecture and Design (10 documents)

| Document ID | Title |
|-------------|-------|
| ARC-001-RSCH-v1.0 | Technology and Service Research Findings |
| ARC-001-ADR-001-v1.0 | ADR: Select Azure as Cloud Platform |
| ARC-001-ADR-002-v1.0 | ADR: Implement Data Quality and Governance Framework |
| ARC-001-AWRS-v1.0 | AWS Technology Research v1.0 |
| ARC-001-AWRS-v1.1 | AWS Technology Research v1.1 |
| ARC-001-AWRS-v2.0 | AWS Technology Research v2.0 |
| ARC-001-AZRS-v1.0 | Azure Technology Research v1.0 |
| ARC-001-AZRS-v2.0 | Azure Technology Research v2.0 |
| ARC-001-GCRS-v1.0 | Google Cloud Technology Research |
| ARC-001-RSCH-001-v1.0 | Sprint 2 Research: Plymouth Restaurant Websites |

### Phase 4: Governance and Compliance (7 documents)

| Document ID | Title |
|-------------|-------|
| ARC-001-RISK-v1.0 | Risk Register (HM Treasury Orange Book) |
| ARC-001-DPIA-v1.0 | Data Protection Impact Assessment |
| ARC-001-ANAL-v1.0 | Architecture Governance Analysis Report v1.0 |
| ARC-001-ANAL-v2.0 | Architecture Governance Analysis Report v2.0 |
| ARC-001-TRAC-v1.0 | Requirements Traceability Matrix v1.0 |
| ARC-001-TRAC-v1.1 | Requirements Traceability Matrix v1.1 |
| ARC-001-TRAC-v2.0 | Requirements Traceability Matrix v2.0 |

### Phase 5: Delivery and Operations (1 document)

| Document ID | Title |
|-------------|-------|
| ARC-001-BKLG-v1.0 | Product Backlog |

---

## Phase-by-phase walkthrough

### Phase 1: Foundation

Phase 1 establishes the governance principles and stakeholder alignment that underpin every subsequent decision. These documents should be read first by anyone joining the project.

**ARC-000-PRIN-v1.0 (Architecture Principles)** defines 18 principles organised into six categories: Strategic, Data, Integration, Quality, DevOps, and Observability. The most important principles for executives to be aware of are: "Data Quality First" (the platform's value depends on accurate data), "Ethical Web Scraping" (non-negotiable -- the project must respect website terms of service and rate limits), and "Privacy by Design" (non-negotiable -- no personal data is collected). Each principle includes validation gates that must be satisfied before the project can proceed to production.

**ARC-001-STKE-v1.0 (Stakeholder Analysis)** identifies 7 primary stakeholder groups across internal and external categories, from the Research Director (executive sponsor) through to Plymouth consumers and restaurant owners. The analysis maps each stakeholder's drivers, goals, and measurable outcomes. The overall stakeholder alignment score is HIGH, with strong consensus around data quality and public benefit. A key tension identified is between the desire for comprehensive data coverage and the constraints of ethical scraping and limited budget.

### Phase 2: Requirements and Data

Phase 2 defines what the platform must do and the data it operates on. This is the reference point for product decisions and development priorities.

**ARC-001-REQ-v2.0 (Requirements)** is the central artifact consumed by most other documents. It specifies 57 unique requirements across 5 categories: 8 business requirements, 11 functional requirements, 22 non-functional requirements, 8 integration requirements, and 8 data requirements. Requirements are prioritised using MoSCoW (MUST/SHOULD/MAY) and traced to specific stakeholder goals. The v2.0 update added ONS geography enrichment, enhanced Companies House financials, and deep stakeholder traceability. The earlier v1.0 is retained for audit purposes.

**ARC-001-DATA-v1.0 (Data Model)** defines the complete data architecture with 8 entities and 142 attributes. The core entities are restaurants (master data with 52 columns), menu items, Trustpilot reviews, Google reviews, drinks, data quality metrics, scraping audit logs, and manual match records. The model follows the "collect-process-present" pipeline architecture and includes GDPR compliance provisions.

**ARC-001-DSCT-v1.0 (Data Source Discovery)** evaluates 22 external data sources across 8 categories. A key finding is that UK Government open data (FSA, Companies House, ONS, VOA) provides 80% of the platform's external data needs at zero cost. The document identifies which requirements are fully matched to data sources (61%), partially matched (28%), and unmatched (11% -- primarily comprehensive menu data, which requires web scraping).

### Phase 3: Architecture and Design

Phase 3 contains the technology research, architecture decisions, and cloud platform evaluations that determine how the platform is built.

**ARC-001-RSCH-v1.0 (Technology Research)** evaluates options across 8 technology categories: dashboard framework, database, web scraping, hosting, monitoring, CI/CD, geocoding, and automated testing. Each evaluation considers open-source options first (per Principle 2) and is constrained by the 100 GBP/month budget. The recommended stack is entirely open source: Streamlit for the dashboard, SQLite (with DuckDB for analytics), Python for scraping, and Streamlit Cloud for hosting.

**ARC-001-ADR-001-v1.0 and ADR-002-v1.0 (Architecture Decision Records)** document two key decisions: selecting Azure as the cloud platform (over AWS) and implementing a data quality and governance framework. These follow a structured TOGAF-adapted format with stakeholders, options considered, decision rationale, and consequences.

**Cloud Research (AWRS, AZRS, GCRS)** -- Six documents evaluate AWS, Azure, and Google Cloud architectures in detail, including cost modelling, security controls, and migration paths. The AWS research evolved from an RDS-based approach (v1.0) to a more cost-effective App Runner + EFS architecture (v2.0). The Azure research reaffirmed PostgreSQL as the target database, concluding that SQLite-on-Azure-Files is an anti-pattern. Google Cloud research evaluates Cloud Run and Cloud SQL.

**ARC-001-RSCH-001-v1.0 (Sprint 2 Research)** documents field research on Plymouth restaurant websites. The key finding that most restaurants use PDF or image-based menus rather than HTML significantly shaped the scraping strategy and data collection approach.

### Phase 4: Governance and Compliance

Phase 4 validates that the platform meets regulatory, risk, and quality standards. These documents should be consulted before any release or significant change.

**ARC-001-RISK-v1.0 (Risk Register)** identifies 20 risks following HM Treasury Orange Book methodology. Two risks are rated Critical: GDPR/legal non-compliance (residual score 20) and data quality failures (residual score 20). Six risks are rated High, including web scraping sustainability, budget overruns, and technical implementation challenges. The register achieves a 49% risk reduction through planned controls.

**ARC-001-DPIA-v1.0 (DPIA)** screens the platform against the ICO's 9 criteria for mandatory DPIA. Only 1 of 9 criteria is met (matching datasets). The conclusion is LOW RISK, with no significant privacy risks identified. The DPIA confirms that only public business data is processed and no personal data is collected. ICO prior consultation is not required.

**ARC-001-ANAL-v2.0 (Governance Analysis)** is the latest health check, scoring the project at 72/100 (Grade C). It identifies 2 critical issues (zero automated test coverage, a semantic mismatch in requirement FR-010), 5 high-priority issues (including HTTPS not enforced, uptime monitoring not configured), and 7 medium-priority issues. The score decrease from v1.0 (88/100) reflects expanded scope and more rigorous analysis, not deterioration.

**ARC-001-TRAC-v2.0 (Traceability Matrix)** traces all 57 requirements through design, implementation, and test coverage. It reveals that 67% of requirements have design coverage, 63% have implementation evidence, but 0% have automated test coverage -- a critical gap flagged for resolution before public launch.

### Phase 5: Delivery and Operations

Phase 5 converts requirements into delivery-ready work items.

**ARC-001-BKLG-v1.0 (Product Backlog)** organises 53 stories (161 story points) into 8 two-week sprints, covering a 16-week delivery timeline. The backlog includes 6 epics (business requirements), 15 user stories, 21 technical tasks, and 9 data stories. Prioritisation follows MoSCoW, risk, value, and dependency factors. The backlog was created in November 2025 and the sprint plan has since expired, so a refresh is recommended for the next development phase.

---

## Standards and Compliance

| Standard | Coverage | Key Documents |
|----------|----------|---------------|
| UK GDPR (Data Protection Act 2018) | Full -- DPIA completed, legitimate interests basis, no PII | ARC-001-DPIA-v1.0, ARC-000-PRIN-v1.0 |
| HM Treasury Orange Book (2023) | Full -- 20 risks assessed with 5x5 methodology | ARC-001-RISK-v1.0 |
| ICO DPIA Guidance | Full -- 9-criteria screening completed | ARC-001-DPIA-v1.0 |
| UK Computer Misuse Act 1990 | Addressed -- ethical scraping principles enforced | ARC-000-PRIN-v1.0 |
| Open Government Licence v3.0 | Compliant -- FSA, ONS, Companies House data used under OGL | ARC-001-DSCT-v1.0 |
| MoSCoW Prioritisation | Applied across requirements and backlog | ARC-001-REQ-v2.0, ARC-001-BKLG-v1.0 |

---

## How to Use This Framework

### Recommended reading order

For a complete understanding of the project, read the documents in this order:

1. **This Executive Guide** -- for high-level orientation (you are here)
2. **ARC-000-PRIN-v1.0** -- understand the governing principles, especially the non-negotiable ones
3. **ARC-001-STKE-v1.0** -- understand who the stakeholders are and what they need
4. **ARC-001-REQ-v2.0** -- understand what the platform must do (skip v1.0 unless you need the audit trail)
5. **ARC-001-RISK-v1.0** -- understand the key risks, especially the 2 critical ones
6. **ARC-001-ANAL-v2.0** -- understand the current governance health and open issues

### Who should read what

- **Executives and sponsors**: This guide, plus ARC-001-STKE-v1.0 (stakeholder alignment) and ARC-001-RISK-v1.0 (risk profile)
- **Product owners**: ARC-001-REQ-v2.0 (requirements), ARC-001-BKLG-v1.0 (backlog), ARC-001-TRAC-v2.0 (traceability)
- **Developers**: ARC-001-DATA-v1.0 (data model), ARC-001-RSCH-v1.0 (technology stack), ADR documents (architecture decisions)
- **Legal and compliance**: ARC-001-DPIA-v1.0 (privacy assessment), ARC-000-PRIN-v1.0 (ethical scraping principles)
- **New joiners**: Start with this guide, then read Phase 1 and Phase 2 documents in order

### Navigating between documents

All documents use a consistent identification scheme: `ARC-{PROJECT_ID}-{TYPE}-v{VERSION}.md`. The project ID for this project is 001. Document types are abbreviated (REQ = Requirements, RISK = Risk Register, DATA = Data Model, etc.). When a document references another, it uses this Document ID format so you can quickly locate the referenced artifact.

Where multiple versions of a document exist (e.g., REQ v1.0 and v2.0), always refer to the latest version for current information. Earlier versions are retained for audit trail and change history purposes.

---

**Generated by**: ArcKit `/arckit:framework` agent
**Generated on**: 2026-03-08
**ArcKit Version**: v4.0.1
**Project**: Plymouth Research Restaurant Menu Analytics (Project 001)
**AI Model**: Claude Opus 4.6 (claude-opus-4-6)
