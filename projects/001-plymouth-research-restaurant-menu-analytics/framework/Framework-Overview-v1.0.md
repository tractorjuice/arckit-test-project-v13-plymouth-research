# Architecture Framework Overview: Plymouth Research Restaurant Menu Analytics

> **Template Status**: Live | **Version**: 1.0 | **Command**: `/arckit:framework`

## Document Control

| Field | Value |
|-------|-------|
| **Document ID** | ARC-001-FWRK-v1.0 |
| **Document Type** | Framework Overview |
| **Project** | Plymouth Research Restaurant Menu Analytics (Project 001) |
| **Classification** | OFFICIAL |
| **Status** | DRAFT |
| **Version** | 1.0 |
| **Created Date** | 2026-03-08 |
| **Last Modified** | 2026-03-08 |
| **Review Cycle** | Quarterly |
| **Next Review Date** | 2026-06-08 |
| **Owner** | Mark Craddock (Product Owner / Technical Lead) |
| **Reviewed By** | [PENDING] |
| **Approved By** | [PENDING] |
| **Distribution** | Project Team, Architecture Team, Stakeholders |

## Revision History

| Version | Date | Author | Changes | Approved By | Approval Date |
|---------|------|--------|---------|-------------|---------------|
| 1.0 | 2026-03-08 | AI Agent | Initial creation from `/arckit:framework` command | PENDING | PENDING |

---

## Executive Summary

The Plymouth Research Restaurant Menu Analytics platform is an independent research tool that aggregates publicly available restaurant data from multiple authoritative sources across Plymouth, UK. The platform scrapes restaurant menus, integrates Food Standards Agency hygiene ratings, Trustpilot and Google reviews, Companies House data, and other public datasets into a unified SQLite database, presenting insights through an interactive Streamlit dashboard.

The business challenge is straightforward: no comprehensive, independent source of restaurant menu data exists for Plymouth. Consumers, food researchers, and journalists lack a single place to compare menus, prices, dietary options, and quality indicators across 98+ establishments. Plymouth Research addresses this gap through ethical web scraping, multi-source data aggregation, and an open-source-first technology approach, all within a monthly operational budget of under 100 GBP.

This framework organises 24 architecture artifacts (spanning 15 unique document types) into 5 logical phases, providing a structured reading path from foundational principles through delivery. The framework covers the full governance lifecycle: stakeholder alignment, requirements specification, data architecture, technology research across three cloud providers (AWS, Azure, Google Cloud), architecture decisions, risk management following HM Treasury Orange Book principles, GDPR compliance via DPIA, and delivery planning through a 53-story product backlog.

### Key figures

- **24 artifacts** catalogued across 5 phases
- **57 unique requirements** traced across business, functional, non-functional, integration, and data categories
- **18 architecture principles** governing all decisions (2 non-negotiable: Ethical Web Scraping, Privacy by Design)
- **20 risks** identified and assessed (2 critical, 6 high)
- **8 data entities** with 142 attributes modelled
- **22 external data sources** discovered and evaluated
- **Governance Health Score**: 72/100 (Grade C -- adequate governance, address high-priority issues)

---

## Framework Architecture

### Phase structure

The framework is organised into 5 phases representing the logical progression from governance foundations through operational delivery. Phases are not strictly sequential -- cross-cutting concerns (principles, risk, governance) span and inform all phases.

```
                    ┌─────────────────────────────────┐
                    │  CROSS-CUTTING CONCERNS          │
                    │  Principles (ARC-000-PRIN-v1.0)  │
                    │  Risk (ARC-001-RISK-v1.0)        │
                    │  Governance Analysis (ANAL)       │
                    └─────────────┬───────────────────┘
                                  │
    ┌─────────────┐  ┌───────────┴──────────┐  ┌──────────────────┐
    │  Phase 1    │  │      Phase 2         │  │    Phase 3       │
    │ Foundation  │──│ Requirements & Data  │──│ Architecture &   │
    │             │  │                      │  │ Design           │
    │ PRIN, STKE  │  │ REQ, DATA, DSCT      │  │ RSCH, ADR, AWRS  │
    │             │  │                      │  │ AZRS, GCRS       │
    └──────┬──────┘  └──────────┬───────────┘  └────────┬─────────┘
           │                    │                        │
           │         ┌─────────┴──────────┐             │
           │         │     Phase 4        │             │
           └────────►│ Governance &       │◄────────────┘
                     │ Compliance         │
                     │ RISK, DPIA, ANAL   │
                     │ TRAC               │
                     └────────┬───────────┘
                              │
                     ┌────────┴───────────┐
                     │     Phase 5        │
                     │ Delivery &         │
                     │ Operations         │
                     │ BKLG               │
                     └────────────────────┘
```

### Phase dependencies

- **Phase 1 (Foundation)** establishes the principles and stakeholder context that all other phases must align to.
- **Phase 2 (Requirements and Data)** defines what must be built and the data it operates on. Informed by Phase 1 stakeholder goals and principles.
- **Phase 3 (Architecture and Design)** determines how to build it. Technology research and decisions are constrained by Phase 1 principles and driven by Phase 2 requirements.
- **Phase 4 (Governance and Compliance)** validates that Phases 2 and 3 meet regulatory, risk, and quality standards. The traceability matrix traces requirements through to implementation.
- **Phase 5 (Delivery and Operations)** converts requirements into delivery-ready user stories and sprint plans.

### Cross-cutting concerns

Three artifact types span multiple phases and should be consulted throughout the project lifecycle:

1. **Architecture Principles** (ARC-000-PRIN-v1.0) -- 18 principles governing all technology decisions. Two are non-negotiable: Ethical Web Scraping and Privacy by Design.
2. **Risk Register** (ARC-001-RISK-v1.0) -- 20 risks that inform requirements, design choices, and compliance checks.
3. **Governance Analysis** (ARC-001-ANAL) -- Periodic health checks measuring how well the project adheres to its own governance framework.

---

## Design Philosophy

This framework embodies the architecture principles established in `ARC-000-PRIN-v1.0` (projects/000-global/):

- **Data Quality First** (Principle 1, FOUNDATIONAL): The data model (ARC-001-DATA-v1.0) includes dedicated data quality metrics entities. The requirements specify 95%+ accuracy targets. ADR-002 formalises the data quality and governance framework.
- **Open Source Preferred** (Principle 2): Technology research (ARC-001-RSCH-v1.0) evaluates open-source options first across all 8 technology categories. The recommended stack (Streamlit, SQLite, Python) is entirely open source.
- **Ethical Web Scraping** (Principle 3, NON-NEGOTIABLE): Requirements include robots.txt compliance, rate limiting (5s minimum), honest User-Agent identification. The DPIA documents the ethical scraping approach. The risk register assigns the highest severity to scraping violations.
- **Privacy by Design** (Principle 4, NON-NEGOTIABLE): The DPIA confirms only public business data is processed. No PII collection. GDPR legitimate interests basis documented.
- **Cost Efficiency** (Principle 6): All research artifacts evaluate total cost of ownership. The target is under 100 GBP/month operational cost.
- **Data Lineage and Traceability** (Principle 8): The data model stores source URLs and scrape timestamps for every record. The traceability matrix traces requirements through design to implementation.

---

## Document Map

### Phase 1: Foundation (2 artifacts)

| Document ID | Type | Title | Description | Location |
|-------------|------|-------|-------------|----------|
| ARC-000-PRIN-v1.0 | Principles | Plymouth Research Enterprise Architecture Principles | 18 architecture principles across 6 categories (Strategic, Data, Integration, Quality, DevOps, Observability). Defines non-negotiable constraints for ethical scraping and privacy. | projects/000-global/ |
| ARC-001-STKE-v1.0 | Stakeholder Analysis | Stakeholder Drivers & Goals Analysis | 7 primary stakeholder groups, 11 stakeholders, power-interest grid, 10 driver statements, measurable outcomes. Overall alignment: HIGH. | projects/001-.../ |

### Phase 2: Requirements and Data (4 artifacts)

| Document ID | Type | Title | Description | Location |
|-------------|------|-------|-------------|----------|
| ARC-001-REQ-v1.0 | Requirements | Business and Technical Requirements Specification | Initial requirements: 69 requirements (7 BR, 10 FR, 47 NFR, 6 DR) based on production codebase analysis. | projects/001-.../ |
| ARC-001-REQ-v2.0 | Requirements | Business and Technical Requirements Specification | Major update: 57 deduplicated requirements with ONS geography, enhanced Companies House financials, stakeholder traceability, risk-driven requirements. | projects/001-.../ |
| ARC-001-DATA-v1.0 | Data Model | Data Model | 8 entities, 142 attributes, 7 relationships. Covers restaurants, menu items, reviews (Trustpilot, Google), drinks, data quality metrics, scraping audit logs, manual matches. | projects/001-.../ |
| ARC-001-DSCT-v1.0 | Data Source Discovery | Data Source Discovery | 22 external data sources evaluated across 8 categories. UK Government open data provides 80% of needs at zero cost. 61% of requirements fully matched to sources. | projects/001-.../ |

### Phase 3: Architecture and Design (10 artifacts)

| Document ID | Type | Title | Description | Location |
|-------------|------|-------|-------------|----------|
| ARC-001-RSCH-v1.0 | Research | Technology and Service Research Findings | 8 technology categories researched: dashboard, database, scraping, hosting, monitoring, CI/CD, geocoding, testing. Recommendations constrained by 100 GBP/month budget. | projects/001-.../ |
| ARC-001-ADR-001-v1.0 | ADR | Select Azure as Cloud Platform | Evaluates AWS vs Azure for cloud hosting. Selects Azure based on cost, developer experience, and UK data residency. | projects/001-.../decisions/ |
| ARC-001-ADR-002-v1.0 | ADR | Implement Data Quality and Governance Framework | Addresses orphaned data quality requirements. Proposes validation framework for data governance. | projects/001-.../decisions/ |
| ARC-001-AWRS-v1.0 | AWS Research | AWS Technology Research | Initial AWS architecture evaluation: RDS for PostgreSQL, Lambda, S3, CloudWatch. | projects/001-.../research/ |
| ARC-001-AWRS-v1.1 | AWS Research | AWS Technology Research (Refreshed) | Refreshed cost estimates based on ADR-001 decision context. | projects/001-.../research/ |
| ARC-001-AWRS-v2.0 | AWS Research | AWS Technology Research (App Runner + EFS) | Major revision: proposes App Runner with EFS for SQLite lift-and-shift. More cost-effective migration path. | projects/001-.../research/ |
| ARC-001-AZRS-v1.0 | Azure Research | Azure Technology Research | Initial Azure evaluation: App Service, Azure Database for PostgreSQL, Azure Files. | projects/001-.../research/ |
| ARC-001-AZRS-v2.0 | Azure Research | Azure Technology Research (PostgreSQL Reaffirmed) | Reaffirms PostgreSQL recommendation. Concludes SQLite-on-Azure-Files is an anti-pattern. Enhanced cost and security analysis. | projects/001-.../research/ |
| ARC-001-GCRS-v1.0 | GCP Research | Google Cloud Technology Research | Google Cloud evaluation: Cloud Run, Cloud SQL, Cloud Storage. First analysis of GCP option. | projects/001-.../research/ |
| ARC-001-RSCH-001-v1.0 | Research | Sprint 2 Research: Plymouth Restaurant Websites | Field research on 10+ Plymouth restaurants. Key finding: most use PDF/image menus, not HTML. Impacts scraping strategy. | projects/001-.../research/ |

### Phase 4: Governance and Compliance (7 artifacts)

| Document ID | Type | Title | Description | Location |
|-------------|------|-------|-------------|----------|
| ARC-001-RISK-v1.0 | Risk Register | Risk Register (HM Treasury Orange Book) | 20 risks across 6 categories. 2 critical (GDPR/legal, data quality), 6 high. 49% risk reduction through controls. Overall: CONCERNING. | projects/001-.../ |
| ARC-001-DPIA-v1.0 | DPIA | Data Protection Impact Assessment | ICO 9-criteria screening: 1/9 met. Conclusion: LOW RISK. Only public business data processed. ICO consultation not required. | projects/001-.../ |
| ARC-001-ANAL-v1.0 | Governance Analysis | Architecture Governance Analysis Report v1.0 | Initial analysis: 69 requirements, 75% implemented. Score: 88/100 (Grade B). Recommendation: PROCEED. | projects/001-.../ |
| ARC-001-ANAL-v2.0 | Governance Analysis | Architecture Governance Analysis Report v2.0 | Expanded analysis: 57 deduplicated requirements, 17 artifacts. Score: 72/100 (Grade C). 2 critical issues, 5 high. | projects/001-.../ |
| ARC-001-TRAC-v1.0 | Traceability Matrix | Requirements Traceability Matrix v1.0 | Initial traceability: 24 requirements (BR, INT, DR only). | projects/001-.../ |
| ARC-001-TRAC-v1.1 | Traceability Matrix | Requirements Traceability Matrix v1.1 | Added DATA, DSCT, DPIA recognition as design evidence. Resolved orphan requirements. | projects/001-.../ |
| ARC-001-TRAC-v2.0 | Traceability Matrix | Requirements Traceability Matrix v2.0 | Full scope: 57 requirements across all categories. Identified FR-010 semantic mismatch. | projects/001-.../ |

### Phase 5: Delivery and Operations (1 artifact)

| Document ID | Type | Title | Description | Location |
|-------------|------|-------|-------------|----------|
| ARC-001-BKLG-v1.0 | Product Backlog | Product Backlog | 53 stories, 161 story points, 8 sprints (16 weeks). 6 epics, 15 user stories, 21 technical tasks, 9 data stories. | projects/001-.../ |

---

## Standards Alignment

The framework aligns to the following standards, frameworks, and regulations:

| Standard / Framework | Coverage | Key Documents |
|----------------------|----------|---------------|
| **UK GDPR (Data Protection Act 2018)** | Full | ARC-001-DPIA-v1.0, ARC-000-PRIN-v1.0 (Principle 4), ARC-001-RISK-v1.0 (R-001) |
| **HM Treasury Orange Book (2023)** | Full | ARC-001-RISK-v1.0 (risk management methodology) |
| **ICO DPIA Guidance** | Full | ARC-001-DPIA-v1.0 (9-criteria screening) |
| **UK Computer Misuse Act 1990** | Addressed | ARC-000-PRIN-v1.0 (Principle 3 -- Ethical Web Scraping) |
| **UK Copyright, Designs and Patents Act 1988** | Addressed | ARC-000-PRIN-v1.0 (Principle 3), ARC-001-DPIA-v1.0 |
| **Open Government Licence v3.0** | Compliant | ARC-001-DSCT-v1.0 (FSA data, ONS data, Companies House) |
| **MoSCoW Prioritisation** | Applied | ARC-001-REQ-v2.0, ARC-001-BKLG-v1.0 |
| **TOGAF ADR Format** | Adapted | ARC-001-ADR-001-v1.0, ARC-001-ADR-002-v1.0 |
| **GDS Service Standard** | Partial | User-centred design principles reflected in stakeholder analysis |

---

## Adoption Guidance

### Entry points by role

| Role | Start Here | Then Read | Key Concerns |
|------|-----------|-----------|--------------|
| **Executive / Sponsor** | Executive Guide, then ARC-001-STKE-v1.0 | ARC-001-RISK-v1.0, ARC-001-ANAL-v2.0 | Budget, risk, stakeholder alignment |
| **Product Owner** | ARC-001-REQ-v2.0 | ARC-001-BKLG-v1.0, ARC-001-TRAC-v2.0 | Requirements coverage, delivery plan |
| **Developer / Engineer** | ARC-001-DATA-v1.0 | ARC-001-RSCH-v1.0, ARC-001-ADR-001-v1.0 | Data schema, technology stack, architecture decisions |
| **Data Engineer** | ARC-001-DATA-v1.0 | ARC-001-DSCT-v1.0, ARC-001-RSCH-001-v1.0 | Data model, external sources, scraping feasibility |
| **Compliance / Legal** | ARC-001-DPIA-v1.0 | ARC-000-PRIN-v1.0, ARC-001-RISK-v1.0 | GDPR, ethical scraping, legal risk |
| **Architect** | This document (FWRK) | ARC-000-PRIN-v1.0, ARC-001-ANAL-v2.0 | Governance health, principles compliance |
| **New Team Member** | This document (FWRK) | Phase 1 artifacts, then Phase 2 | Project context, orientation |

### Phased adoption approach

1. **Orientation (Day 1)**: Read this Framework Overview and the Executive Guide to understand scope and structure.
2. **Foundation (Week 1)**: Review Phase 1 -- understand principles (especially non-negotiable ones) and stakeholder context.
3. **Requirements (Week 1-2)**: Review Phase 2 -- understand what the platform must do and the data it manages.
4. **Design (Week 2-3)**: Review Phase 3 -- understand technology choices and the rationale behind them.
5. **Governance (Ongoing)**: Phase 4 artifacts should be consulted when making changes, assessing risk, or preparing for releases.
6. **Delivery (Ongoing)**: Phase 5 backlog drives sprint planning and feature delivery.

---

## Traceability

### Source artifacts table

This table maps each section of this framework document back to the source artifacts it was synthesised from.

| Framework Section | Source Artifacts |
|-------------------|----------------|
| Executive Summary | ARC-001-REQ-v2.0 (project context), ARC-001-STKE-v1.0 (business drivers), ARC-001-ANAL-v2.0 (governance metrics) |
| Framework Architecture | All artifacts (structural analysis), ARC-000-PRIN-v1.0 (cross-cutting concerns) |
| Design Philosophy | ARC-000-PRIN-v1.0 (principles), ARC-001-DATA-v1.0 (data quality), ARC-001-ADR-002-v1.0 (governance framework), ARC-001-RSCH-v1.0 (technology evaluation) |
| Document Map | All 24 artifacts catalogued from projects/001-.../ and projects/000-global/ |
| Standards Alignment | ARC-000-PRIN-v1.0 (legal frameworks), ARC-001-DPIA-v1.0 (ICO/GDPR), ARC-001-RISK-v1.0 (Orange Book), ARC-001-DSCT-v1.0 (OGL data) |
| Adoption Guidance | ARC-001-STKE-v1.0 (stakeholder roles), ARC-001-ANAL-v2.0 (governance findings) |

### Artifact version summary

Where multiple versions of an artifact exist, the latest version is the current reference. Earlier versions are retained for audit trail purposes.

| Artifact Type | Latest Version | Previous Versions |
|--------------|----------------|-------------------|
| Requirements (REQ) | v2.0 | v1.0 |
| Traceability (TRAC) | v2.0 | v1.0, v1.1 |
| Governance Analysis (ANAL) | v2.0 | v1.0 |
| AWS Research (AWRS) | v2.0 | v1.0, v1.1 |
| Azure Research (AZRS) | v2.0 | v1.0 |

---

## Coverage Gaps

The following gaps have been identified. These represent areas where additional artifacts would strengthen the framework:

| Gap | Impact | Recommended Action |
|-----|--------|-------------------|
| **No High-Level Design (HLD)** | 33% of requirements lack formal design coverage (finding H2 in ANAL-v2.0) | Run `/arckit:diagram` to create system architecture diagrams |
| **No Strategic Outline Business Case (SOBC)** | Commercial expansion rationale undocumented (finding M7 in ANAL-v2.0) | Run `/arckit:sobc` if seeking expansion funding |
| **No Roadmap** | No formal roadmap artifact beyond the backlog | Run `/arckit:roadmap` to create phased delivery roadmap |
| **Zero Automated Test Coverage** | Critical finding C1 in ANAL-v2.0 -- 18 MUST requirements untested | Implement pytest test suite before public launch |
| **Risk Register Overdue** | Created 2025-11-17, review overdue by 74+ days (finding M2) | Run `/arckit:risk` to refresh risk assessment |

---

**Generated by**: ArcKit `/arckit:framework` agent
**Generated on**: 2026-03-08
**ArcKit Version**: v4.0.1
**Project**: Plymouth Research Restaurant Menu Analytics (Project 001)
**AI Model**: Claude Opus 4.6 (claude-opus-4-6)
