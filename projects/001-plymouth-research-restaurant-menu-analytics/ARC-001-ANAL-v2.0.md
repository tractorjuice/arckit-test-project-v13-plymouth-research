# Architecture Governance Analysis Report: Plymouth Research Restaurant Menu Analytics

> **Template Status**: Beta | **Version**: 2.0 | **Command**: `/arckit:analyze`

## Document Control

| Field | Value |
|-------|-------|
| **Document ID** | ARC-001-ANAL-v2.0 |
| **Document Type** | Governance Analysis Report |
| **Project** | Plymouth Research Restaurant Menu Analytics (Project 001) |
| **Classification** | PUBLIC |
| **Status** | DRAFT |
| **Version** | 2.0 |
| **Created Date** | 2026-03-01 |
| **Last Modified** | 2026-03-01 |
| **Review Cycle** | On-Demand |
| **Next Review Date** | 2026-03-31 |
| **Owner** | Mark Craddock (Product Owner / Technical Lead) |
| **Reviewed By** | [PENDING] |
| **Approved By** | [PENDING] |
| **Distribution** | Project Team, Architecture Team |

## Revision History

| Version | Date | Author | Changes | Approved By | Approval Date |
|---------|------|--------|---------|-------------|---------------|
| 1.0 | 2025-11-23 | ArcKit AI | Initial creation from `/arckit:analyze` command — analysed 69 requirements, 10 findings, score 88/100 | [PENDING] | [PENDING] |
| 2.0 | 2026-03-01 | ArcKit AI | Major update: expanded artifact set (17 artifacts incl. TRAC v2.0, ADR-001, DSCT-v1.0, REQ v2.0), 57 deduplicated requirements, new stakeholder/risk/data-model analysis, updated scoring methodology | [PENDING] | [PENDING] |

---

## Executive Summary

**Overall Status**: ⚠️ **Issues Found — Address Before Public Launch**

**Key Metrics**:
- Total Requirements: 57 (8 BR, 11 FR, 22 NFR, 8 INT, 8 DR)
- Requirements with Design Coverage: 38/57 (67%)
- Requirements with Implementation Evidence: 36/57 (63%)
- Test Coverage: 0% automated (manual/exploratory only)
- Critical Issues: 2
- High Priority Issues: 5
- Medium Priority Issues: 7
- Low Priority Issues: 3

**Recommendation**: **RESOLVE CRITICAL ISSUES FIRST** — Project has excellent governance foundation (17 artifacts, comprehensive stakeholder/risk/data analysis) but 2 CRITICAL issues (zero automated test coverage for MUST requirements, FR-010 semantic mismatch with ADR-001) and 5 HIGH issues must be addressed before public launch. Address CRITICAL and HIGH issues, then proceed.

**Governance Health Score**: 72/100 (Grade: **C — Adequate Governance, Address High-Priority Issues**)

**Score Breakdown**:
- Requirements Quality: 78%
- Architecture Principles Compliance: 78% (14/18 compliant)
- Traceability Score: 48% (from TRAC v2.0)
- Stakeholder Alignment: 90%
- Risk Management: 82%
- Data Model Quality: 88%
- Compliance Posture: 85%

**Change from v1.0**: Score decreased from 88 to 72 (−16 points). This is primarily due to the expanded scope: v1.0 analysed the original 69 v1.0 requirements with limited traceability; v2.0 analyses 57 deduplicated requirements across 17 artifacts with rigorous traceability scoring that exposes previously hidden gaps (especially zero test coverage and incomplete design mapping for FR/NFR categories).

---

## Findings Summary

| ID | Category | Severity | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|
| C1 | Testing Coverage | CRITICAL | TRAC-v2.0 | Zero automated test coverage — 18 MUST requirements untested | Implement pytest test suite for core data pipeline and dashboard |
| C2 | Traceability | CRITICAL | ADR-001:L180, REQ-v2.0:L755 | FR-010 semantic mismatch: ADR-001 references FR-010 as "Scheduled Data Refresh" but REQ defines it as "Restaurant Owner Opt-Out" | Create FR-012 for scheduled refresh; update ADR-001 references |
| H1 | Risk-Requirements Gap | HIGH | RISK-v1.0 (R-001), REQ-v2.0 | R-001 (GDPR/Legal, residual 20 CRITICAL) lacks explicit automated robots.txt compliance testing in requirements | Add acceptance criterion to NFR-C-002 for automated compliance testing |
| H2 | Design Coverage | HIGH | TRAC-v2.0, REQ-v2.0 | 19 requirements (33%) have no formal design document coverage — no HLD or DLD exists | Create lightweight HLD documenting system architecture |
| H3 | Compliance Pre-Launch | HIGH | REQ-v2.0 (NFR-SEC-001) | HTTPS not enforced in production — GDPR requires encryption in transit | Deploy to HTTPS-enabled platform before public launch |
| H4 | Compliance Pre-Launch | HIGH | REQ-v2.0 (NFR-A-001) | Uptime monitoring not configured — 99% SLA has no measurement infrastructure | Set up UptimeRobot or similar before public launch |
| H5 | Data Model Consistency | HIGH | DATA-v1.0, CLAUDE.md | Data model specifies PostgreSQL 15+ but implementation uses SQLite | Update DATA-v1.0 to reflect SQLite or document migration plan |
| M1 | Requirements Quality | MEDIUM | REQ-v2.0 | Priority downgrade drift: 12 requirements changed from MUST to SHOULD between v1.0 and v2.0 without documented rationale | Document rationale for priority changes in revision history |
| M2 | Risk Staleness | MEDIUM | RISK-v1.0 | Risk register created 2025-11-17 (104 days ago), next review was 2025-12-17 — overdue by 74 days | Re-run `/arckit:risk` to refresh risk assessment |
| M3 | Traceability | MEDIUM | TRAC-v2.0 | DR-005 ID reuse: v1.0 defines as "Data Lineage Metadata" (MUST), v2.0 as "Beverages Data" (SHOULD) — creates audit confusion | Assign new ID (DR-009) to beverages requirement; preserve DR-005 for lineage |
| M4 | DPIA Freshness | MEDIUM | DPIA-v1.0 | DPIA references PostgreSQL but implementation uses SQLite; references "150 restaurants" but current count is 243 | Update DPIA to reflect current implementation state |
| M5 | Backlog Alignment | MEDIUM | BKLG-v1.0 | Backlog uses non-standard document ID `ARC-001-BACKLOG-v1.0` instead of `ARC-001-BKLG-v1.0` | Rename to follow ArcKit naming convention |
| M6 | Stakeholder Traceability | MEDIUM | REQ-v2.0 | ~10 requirements lack explicit stakeholder goal traceability (`SD-x`, `G-x` references) | Add stakeholder references to all requirements |
| M7 | Missing SOBC | MEDIUM | — | No Strategic Outline Business Case exists — recommended for projects seeking expansion funding | Consider `/arckit:sobc` if commercial expansion planned |
| L1 | Document Control | LOW | DPIA-v1.0 | DPIA uses non-standard document ID (`ARCKIT-DPIA-20251117-001-PLYMOUTH-RESEARCH`) instead of `ARC-001-DPIA-v1.0` | Rename to follow ArcKit naming convention |
| L2 | Terminology | LOW | Multiple | Minor terminology drift: "Hygiene rating" vs "FSA rating", "MUST_HAVE" vs "MUST" across v1.0/v2.0 | Standardise to MoSCoW (MUST/SHOULD/MAY) in next requirements refresh |
| L3 | BKLG Staleness | LOW | BKLG-v1.0 | Backlog sprint plan (16 weeks from 2025-11-18) is now expired — sprints ended ~March 2026 | Archive or refresh backlog for next phase |

---

## Requirements Analysis

### Requirements Coverage Matrix

**Total Unique Requirements**: 57 (deduplicated across REQ v1.0 and v2.0)

| Category | Total | Design Coverage | Implementation | Test Coverage | Status |
|----------|-------|-----------------|----------------|---------------|--------|
| Business Requirements (BR) | 8 | 8 (100%) | 7 (88%) | 0 (0%) | ⚠️ Partial |
| Functional Requirements (FR) | 11 | 8 (73%) | 9 (82%) | 0 (0%) | ⚠️ Partial |
| Non-Functional: Performance (NFR-P) | 3 | 2 (67%) | 2 (67%) | 0 (0%) | ⚠️ Partial |
| Non-Functional: Availability (NFR-A) | 2 | 1 (50%) | 1 (50%) | 0 (0%) | ⚠️ Partial |
| Non-Functional: Scalability (NFR-S) | 2 | 1 (50%) | 0 (0%) | 0 (0%) | ❌ Gap |
| Non-Functional: Security (NFR-SEC) | 3 | 2 (67%) | 1 (33%) | 0 (0%) | ❌ Gap |
| Non-Functional: Compliance (NFR-C) | 4 | 3 (75%) | 3 (75%) | 0 (0%) | ⚠️ Partial |
| Non-Functional: Quality (NFR-Q) | 4 | 3 (75%) | 3 (75%) | 0 (0%) | ⚠️ Partial |
| Non-Functional: Maintainability (NFR-M) | 2 | 1 (50%) | 1 (50%) | 0 (0%) | ⚠️ Partial |
| Non-Functional: Observability (NFR-O) | 2 | 0 (0%) | 0 (0%) | 0 (0%) | ❌ Gap |
| Integration Requirements (INT) | 8 | 8 (100%) | 7 (88%) | 0 (0%) | ⚠️ Partial |
| Data Requirements (DR) | 8 | 8 (100%) | 7 (88%) | 0 (0%) | ⚠️ Partial |
| **TOTAL** | **57** | **38 (67%)** | **36 (63%)** | **0 (0%)** | **⚠️ Issues** |

**Statistics**:
- Total Requirements: 57
- Fully Covered (design + implementation + tests): 0 (0%) — no automated tests exist
- Design + Implementation (no tests): 33 (58%)
- Design Only: 5 (9%)
- Implementation Only (no design doc): 3 (5%)
- Not Covered: 16 (28%)

### Uncovered Requirements (CRITICAL)

| Requirement ID | Priority | Description | Why Critical |
|----------------|----------|-------------|--------------|
| NFR-SEC-001 | MUST | HTTPS/TLS encryption | GDPR compliance — encryption in transit required |
| NFR-SEC-002 | SHOULD | Access control for admin features | Security gap — admin functions unprotected |
| NFR-SEC-003 | SHOULD | Dependency security scanning | No vulnerability scanning in pipeline |
| NFR-S-001 | SHOULD | 10x data volume scalability | Not validated — load testing not performed |
| NFR-S-002 | SHOULD | 100 concurrent users | Not validated — load testing not performed |
| NFR-O-001 | SHOULD | Structured logging | Basic logging only, not structured JSON |
| NFR-O-002 | SHOULD | Metrics and monitoring | No monitoring dashboard exists |
| NFR-M-002 | SHOULD | Automated testing (70%+ coverage) | Zero automated tests — **most significant gap** |

---

## Architecture Principles Compliance

**Total Principles**: 18 principles across 6 categories (ARC-000-PRIN-v1.0)

| # | Principle | Status | Evidence | Issues |
|---|-----------|--------|----------|--------|
| 1 | Data Quality First (FOUNDATIONAL) | ✅ COMPLIANT | NFR-Q-001 to NFR-Q-004, validation rules in fetchers | Quality monitoring dashboard pending |
| 2 | Open Source Preferred | ✅ COMPLIANT | Python, Streamlit, SQLite, BeautifulSoup — zero licensing costs | None |
| 3 | Ethical Web Scraping (NON-NEGOTIABLE) | ✅ COMPLIANT | robots.txt compliance, 5s rate limiting, honest User-Agent | Automated compliance testing recommended (H1) |
| 4 | Privacy by Design (NON-NEGOTIABLE) | ✅ COMPLIANT | DPIA completed (LOW RISK), no PII collection, opt-out process | DPIA needs refresh (M4) |
| 5 | Scalability and Extensibility | ✅ COMPLIANT | Multi-city schema, ONS enrichment | Not validated at 10x scale |
| 6 | Cost Efficiency | ✅ COMPLIANT | Costs minimal (free tiers), well within £100/month | None |
| 7 | Single Source of Truth | ✅ COMPLIANT | Data model defines system of record per entity | None |
| 8 | Data Lineage and Traceability | ✅ COMPLIANT | scraped_at, last_updated, source_url columns | None |
| 9 | Data Normalisation and Consistency | ✅ COMPLIANT | Price normalisation, category standardisation | None |
| 10 | API-First Design | ⚠️ PARTIAL | Dashboard accesses DB directly; REST API deferred to Phase 2 | Acceptable for MVP |
| 11 | Standard Data Formats | ✅ COMPLIANT | JSON, CSV (UTF-8, RFC 4180), ISO 8601 timestamps | None |
| 12 | Performance Targets | ✅ COMPLIANT | NFR-P-001 ( < 2s load), NFR-P-002 ( < 500ms search) | Not validated under load |
| 13 | Reliability and Availability | ⚠️ PARTIAL | 99% target defined; uptime monitoring not configured | H4: Configure monitoring |
| 14 | Maintainability and Documentation | ✅ COMPLIANT | Comprehensive CLAUDE.md, docs/ directory | None |
| 15 | Infrastructure as Code | ⚠️ PARTIAL | Schema version-controlled; deployment not automated | Acceptable for current scale |
| 16 | Automated Testing | ❌ NON-COMPLIANT | Zero automated tests | C1: Implement test suite |
| 17 | CI/CD | ⚠️ PARTIAL | Git workflow; no CI/CD pipeline | Acceptable for single-person team |
| 18 | Logging and Monitoring | ⚠️ PARTIAL | Basic logging; structured logging and monitoring pending | NFR-O-001, NFR-O-002 gaps |

**Principle Compliance Score**: 12/18 compliant (67%), 5/18 partial (28%), 1/18 non-compliant (6%)

**Critical Principle Violations**: 1 — Principle #16 (Automated Testing) is non-compliant. Zero automated tests exist despite NFR-M-002 requiring 70%+ coverage.

**NON-NEGOTIABLE Principles Status**: Both NON-NEGOTIABLE principles (#3 Ethical Web Scraping, #4 Privacy by Design) are **COMPLIANT**.

---

## Stakeholder Traceability Analysis

**Stakeholder Analysis Exists**: ✅ Yes (ARC-001-STKE-v1.0)

**Stakeholder Coverage**:
- Total Stakeholder Groups: 7 (10 drivers: SD-1 through SD-10)
- Goals Defined: 8 (G-1 through G-8)
- Outcomes Defined: 4 (O-1 through O-4)
- Requirements traced to stakeholder goals: ~85% (estimated — most v2.0 requirements include explicit `SD-x`, `G-x` references)
- Orphan requirements (no stakeholder justification): ~8 requirements (mostly technical NFRs)
- Requirement conflicts documented and resolved: ✅ Yes (4 conflicts in STKE-v1.0)

**RACI Governance Alignment**:

| Artifact | Role | Aligned with RACI? | Issues |
|----------|------|-------------------|--------|
| Risk Register | Risk Owners | ✅ Yes | All 20 risk owners from RACI (Research Director, Data Engineer, Legal Advisor, Operations/IT) |
| Data Model | Data Owner | ✅ Yes | Research Director assigned |
| Data Model | Technical Custodian | ✅ Yes | Data Engineer assigned |
| Requirements | Stakeholder Refs | ⚠️ Partial | ~8 NFR requirements lack explicit SD-x references |
| DPIA | DPO | ✅ Yes | Legal/Compliance Advisor assigned |

**Conflict Resolution**:
- 4 conflicts identified and resolved in STKE-v1.0:
  1. Data Freshness vs Ethical Scraping → Prioritise Ethics ✅
  2. Comprehensive Coverage vs Budget → Compromise at 150 restaurants ✅
  3. Public Access vs Data Subject Privacy → Innovate with opt-out + DPIA ✅
  4. Real-Time Data vs Scalability → Phase: batch now, partnerships later ✅

**Stakeholder Alignment Score**: 90% — Excellent stakeholder governance with minor gaps in NFR traceability.

---

## Risk Management Analysis

**Risk Register Exists**: ✅ Yes (ARC-001-RISK-v1.0)

**Risk Profile**: 20 risks identified across 6 categories following HM Treasury Orange Book 2023

| Risk ID | Category | Inherent | Residual | Response | Mitigation in Req? | Mitigation in Design? |
|---------|----------|----------|----------|----------|-------------------|---------------------|
| R-001 | COMPLIANCE | 25 (Critical) | 20 (Critical) | Treat | ⚠️ Partial | ✅ DPIA completed |
| R-002 | TECHNOLOGY | 25 (Critical) | 16 (High) | Treat | ✅ NFR-C-003 | ✅ Rate limiting implemented |
| R-003 | REPUTATIONAL | 25 (Critical) | 20 (Critical) | Treat | ✅ NFR-Q-001-004 | ✅ Validation rules |
| R-004 | COMPLIANCE | 20 (High) | 15 (High) | Treat | ✅ NFR-C-002 | ✅ DPIA, opt-out |
| R-005 | FINANCIAL | 25 (Critical) | 14 (High) | Treat | ✅ BR-003 | ✅ Open source tools |
| R-008 | TECHNOLOGY | 16 (High) | 15 (High) | Treat | ⚠️ Partial | ⚠️ Pipeline exists |
| R-010 | TECHNOLOGY | 15 (High) | 15 (High) | Treat | ⚠️ Partial | ⚠️ Untested |
| R-012 | STRATEGIC | 16 (High) | 13 (High) | Treat | ✅ FR-001-010 | ✅ Dashboard |

**High/Very High Risks Requiring Attention**:

| Risk ID | Description | Current Status | Required Action |
|---------|-------------|----------------|-----------------|
| R-001 | GDPR/Legal Non-Compliance (Critical 20) | Partial mitigation | H1: Add automated robots.txt compliance testing |
| R-003 | Data Quality Failures (Critical 20) | Mitigated in reqs | C1: Add automated tests to validate quality |
| R-010 | Performance Requirements Not Met (High 15) | Untested | Perform load testing before public launch |

**Risk Register Staleness**: ⚠️ OVERDUE — Created 2025-11-17, next review was 2025-12-17. Now 74 days overdue for review (M2).

**Risk Governance**:
- Risk owners from stakeholder RACI: ✅ Yes (100%)
- Risk appetite compliance: 18/20 within tolerance
- Risk responses appropriate (4Ts): ✅ Yes
- Risk reduction achieved: 49% (455 → 232 aggregate score)

**Risk-DPIA Alignment**:
- ⚠️ Minor inconsistency: DPIA conclusion is "LOW RISK" (privacy risk to individuals) but R-001 is CRITICAL (20) for organisational compliance risk. Both assessments are **correct in their respective contexts** — DPIA assesses privacy impact, R-001 assesses legal liability.

**Risk Management Score**: 82%

---

## Business Case Analysis

**SOBC Exists**: ❌ No

**Rationale**: Strategic Outline Business Case is not strictly required for this project scale (independent research, < £100/month operational costs). Business case elements are embedded across requirements (Executive Summary), stakeholder analysis (goals G-1 to G-8), and risk register.

**Recommendation**: If Plymouth Research plans commercial expansion (B2B SaaS, geographic growth), consider running `/arckit:sobc` to formalise the business case (M7).

---

## Data Model Analysis

**Data Model Exists**: ✅ Yes (ARC-001-DATA-v1.0)

**DR-xxx Requirements Coverage**:

| Requirement ID | Description | Entities | Status |
|----------------|-------------|----------|--------|
| DR-001 | Restaurant Master Data | E-001: RESTAURANT (52 cols) | ✅ Complete |
| DR-002 | Menu Item Data | E-002: MENU_ITEM (13 cols) | ✅ Complete |
| DR-003 | Trustpilot Reviews | E-005: TRUSTPILOT_REVIEW | ✅ Complete |
| DR-004 | Google Reviews | E-006: GOOGLE_REVIEW | ✅ Complete |
| DR-005 | Data Lineage Metadata (v1.0) / Beverages (v2.0) | scraped_at, last_updated cols | ⚠️ ID reuse (M3) |
| DR-006 | Data Quality Metrics | E-008: DATA_QUALITY_LOG | ⚠️ Not implemented |
| DR-007 | Companies House Financial Data | E-001 financial columns | ✅ Complete |
| DR-008 | ONS Geography Data | E-001 ONS columns | ✅ Complete |

**Data Requirements Coverage**: 7/8 (88%) — DR-006 (quality metrics log) not yet implemented.

**Data Model Quality**:
- ERD exists and renderable (Mermaid): ✅ Yes
- Entities with complete specs: 9/9 (100%)
- PII identified: ✅ Yes (0 PII entities — correctly classified)
- GDPR compliance documented: ✅ Yes (Section 4 of DATA-v1.0)

**Data Governance**:
- Data owners from RACI matrix: ✅ Yes (Research Director)
- Data stewards assigned: ✅ Yes
- Technical custodians assigned: ✅ Yes (Data Engineer)

**Data Model-Design Alignment**:
- Database technology: ❌ **INCONSISTENCY** — DATA-v1.0 specifies PostgreSQL 15+ but implementation uses SQLite (H5)
- Entity-to-table mapping: ✅ Consistent
- Relationship cardinality: ✅ Consistent
- CRUD access patterns: ✅ Aligned with dashboard implementation

**Data Model Score**: 88%

---

## Compliance Analysis

### UK GDPR / Data Protection

**DPIA Exists**: ✅ Yes (ARC-001-DPIA-v1.0)

**DPIA Outcome**: LOW RISK — Only 1/9 ICO criteria met (matching datasets). No personal data processed.

**Compliance Status**: ✅ COMPLIANT with caveats

**Evidence**:
- Lawful basis: Legitimate interests (Art 6(1)(f)) ✅
- Data minimisation: Only public business data ✅
- Opt-out mechanism: 72-hour SLA documented (FR-010) ✅
- DPIA conducted: ✅ (good practice, not legally required)
- Privacy policy: ⚠️ **Not yet published** (pre-launch blocker)
- ICO registration: ⚠️ Status not confirmed

**DPIA Freshness Issues** (M4):
- References PostgreSQL (should be SQLite)
- References "150 restaurants" (current: 243)
- Data processing description accurate but implementation details outdated

### Robots.txt and Ethical Scraping

**Status**: ✅ COMPLIANT

**Evidence**:
- Robots.txt parser: ✅ Implemented (`ROBOTSTXT_OBEY = True`)
- Rate limiting: ✅ 5-second minimum between requests
- User-Agent: ✅ Honest identification with contact email
- Attribution: ✅ FSA OGL, Trustpilot, Google attribution in dashboard

**Gap**: No automated compliance testing infrastructure (H1)

### Open Government Licence

**Status**: ✅ COMPLIANT — FSA data used under OGL v3.0 with proper attribution.

---

## Traceability Analysis

**Traceability Matrix**: ✅ Exists (ARC-001-TRAC-v2.0)

**Overall Traceability Score**: 48/100 (from TRAC v2.0 weighted scoring)

**Forward Traceability** (Requirements → Design → Implementation → Tests):
- Requirements → Design: 67% (38/57)
- Requirements → Implementation: 63% (36/57)
- Requirements → Tests: 0% (0/57) — **CRITICAL GAP**

**Backward Traceability** (Design → Requirements):
- ADR-001 references: 11 requirement IDs
- DATA-v1.0 references: All DR and most FR/INT requirements
- DSCT-v1.0: All INT-001 to INT-008 covered
- Orphan design elements: 1 (FR-010 semantic mismatch — C2)

**Key Gaps**:
- 19 requirements with no formal design document (no HLD/DLD)
- 0 requirements with automated test coverage
- 1 semantic mismatch between ADR-001 and REQ-v2.0 for FR-010

---

## Design Quality Analysis

### HLD Analysis

**HLD Exists**: ❌ No

**Impact**: Without a High-Level Design document, 19 requirements (33%) lack formal design coverage. Design decisions are distributed across ADR-001, DATA-v1.0, DSCT-v1.0, and research artifacts, which provides partial coverage but no unified architectural view.

**Recommendation**: Create a lightweight HLD documenting the collect → process → present pipeline architecture, component interactions, and technology decisions (H2).

### DLD Analysis

**DLD Exists**: ❌ No

**Impact**: Detailed design is embedded in implementation (CLAUDE.md, code comments, guide docs). Acceptable for current team size (1-2 developers) but will become a knowledge bottleneck at scale.

---

## Detailed Findings

### Critical Issues

#### C1: Zero Automated Test Coverage

**Severity**: CRITICAL
**Category**: Testing Coverage
**Location**: ARC-001-TRAC-v2.0 (Section 7.1 Metrics), ARC-001-REQ-v2.0 (NFR-M-002)

**Description**:
No automated test suite exists. NFR-M-002 requires 70%+ test coverage but current coverage is 0%. The TRAC v2.0 scores 0/25 for test coverage (25% of total traceability score weight). All 18 MUST requirements lack automated verification.

**Impact**:
- Regressions go undetected during code changes
- Data pipeline errors (price extraction, dietary tagging) cannot be caught automatically
- Violates Principle #16 (Automated Testing)
- Blocks achievement of reliable CI/CD pipeline
- Risk R-003 (Data Quality Failures) mitigation weakened without test validation

**Recommendation**:
1. Implement pytest test suite targeting data pipeline (fetchers, matchers, importers)
2. Add unit tests for price normalisation, dietary tag extraction, fuzzy matching
3. Add integration tests for database operations (CRUD, triggers, views)
4. Target 50% coverage in Sprint 1, 70% by public launch
5. Add GitHub Actions CI workflow to run tests on push

**Estimated Effort**: 2-3 sprints (4-6 weeks)

---

#### C2: FR-010 Semantic Mismatch Between ADR-001 and REQ-v2.0

**Severity**: CRITICAL
**Category**: Traceability Integrity
**Location**: ARC-001-ADR-001-v1.0:L180 (FR-010 referenced as "Scheduled Data Refresh"), ARC-001-REQ-v2.0:L755 (FR-010 defined as "Restaurant Owner Opt-Out and Correction")

**Description**:
ADR-001 (Azure Cloud Platform Selection) references FR-010 in the context of "Scheduled Data Refresh" (Azure Functions for weekly scraping automation). However, REQ-v2.0 defines FR-010 as "Restaurant Owner Opt-Out and Correction" (GDPR compliance process). This creates a traceability integrity violation — the ADR justifies cloud service selection based on a requirement that doesn't exist under that ID.

**Impact**:
- Cloud platform decision rationale is partially invalidated
- Audit trail between architectural decision and requirements is broken
- Risk of implementing the wrong feature if following ADR-001 references

**Recommendation**:
1. Create FR-012 (or next available ID) for "Scheduled Data Refresh Automation"
2. Update ADR-001 to reference the correct FR-012 instead of FR-010
3. Verify all other ADR-001 requirement references are accurate

**Estimated Effort**: 1-2 hours

---

### High Priority Issues

#### H1: R-001 GDPR/Legal Risk Lacks Automated Compliance Testing

**Severity**: HIGH
**Category**: Risk-Requirements Gap
**Location**: ARC-001-RISK-v1.0 (R-001, residual score 20 CRITICAL), ARC-001-REQ-v2.0 (NFR-C-002, NFR-C-003)

**Description**:
R-001 (GDPR/Legal Non-Compliance) is the highest-severity risk (residual 20 CRITICAL). While NFR-C-003 requires robots.txt compliance and rate limiting, there is no explicit requirement for **automated compliance testing** — no CI/CD check verifies robots.txt compliance, no automated audit of rate limiting logs, no PII detection scan in scrape output.

**Recommendation**:
1. Add acceptance criterion to NFR-C-003: "Automated robots.txt compliance test runs before every scrape batch"
2. Implement PII detection regex scan on scraped content
3. Add rate-limiting log analysis to CI/CD pipeline

---

#### H2: No HLD or DLD — 33% Requirements Without Formal Design

**Severity**: HIGH
**Category**: Design Coverage
**Location**: TRAC-v2.0 Gap Analysis

**Description**:
19 of 57 requirements (33%) have no formal design document coverage. While ADR-001, DATA-v1.0, and DSCT-v1.0 provide partial design evidence, there is no unified High-Level Design or Detailed Design document.

**Recommendation**:
Run `/arckit:diagram` to create a C4 Context and Container diagram documenting the system architecture. Consider a lightweight HLD if vendor procurement is planned.

---

#### H3: HTTPS Not Enforced (NFR-SEC-001)

**Severity**: HIGH
**Category**: Compliance Pre-Launch
**Location**: ARC-001-REQ-v2.0 (NFR-SEC-001)

**Description**:
HTTPS/TLS encryption is not enforced in the current deployment. GDPR requires "appropriate security measures" including encryption in transit. This is a pre-launch blocker for public-facing dashboard.

**Recommendation**: Deploy to HTTPS-enabled platform (Streamlit Cloud, Render, Railway — all provide free HTTPS). Configure HTTP → HTTPS redirect.

---

#### H4: Uptime Monitoring Not Configured (NFR-A-001)

**Severity**: HIGH
**Category**: Compliance Pre-Launch
**Location**: ARC-001-REQ-v2.0 (NFR-A-001)

**Description**:
NFR-A-001 requires 99% uptime but no monitoring infrastructure exists to measure or alert on downtime.

**Recommendation**: Set up UptimeRobot (free tier) or Pingdom before public launch.

---

#### H5: PostgreSQL vs SQLite Data Model Inconsistency

**Severity**: HIGH
**Category**: Data Model Consistency
**Location**: ARC-001-DATA-v1.0 (Technical Foundation), CLAUDE.md

**Description**:
DATA-v1.0 specifies "PostgreSQL 15+" as the database technology, but the implementation uses SQLite (confirmed in CLAUDE.md: "plymouth_research.db ~20 MB"). This inconsistency affects design reviews, vendor evaluations, and architectural decisions that reference the data model.

**Recommendation**: Update DATA-v1.0 Section "Technical Foundation" to reflect SQLite with a note on potential PostgreSQL migration if scaling beyond 10,000 restaurants.

---

### Medium Priority Issues

#### M1: Priority Downgrade Drift

**Severity**: MEDIUM
**Category**: Requirements Quality
**Location**: ARC-001-REQ-v1.0 → v2.0

**Description**:
12 requirements changed priority from MUST to SHOULD between v1.0 and v2.0 (including NFR-A-001, NFR-S-001, NFR-SEC-001, NFR-C-002, all DR requirements). While some changes may be justified (MVP scoping), no rationale is documented in the revision history.

**Recommendation**: Document priority change rationale in REQ-v2.0 revision history.

---

#### M2: Risk Register Overdue for Review

**Severity**: MEDIUM
**Category**: Risk Staleness
**Location**: ARC-001-RISK-v1.0

**Description**:
Risk register was created 2025-11-17 with next review date 2025-12-17. It is now 74 days overdue. Risk scores and mitigation statuses may not reflect current state (e.g., 243 restaurants vs 150 assumed).

**Recommendation**: Re-run `/arckit:risk` to refresh the risk assessment.

---

#### M3: DR-005 ID Reuse Across Versions

**Severity**: MEDIUM
**Category**: Traceability Integrity
**Location**: ARC-001-REQ-v1.0 (DR-005: "Data Lineage Metadata", MUST), ARC-001-REQ-v2.0 (DR-005: "Beverages Data", SHOULD)

**Description**:
DR-005 has different meanings in v1.0 (Data Lineage Metadata, MUST) and v2.0 (Beverages Data, SHOULD). The original lineage concept is still implemented (scraped_at, last_updated columns exist) but the ID now points to a different requirement. This creates audit confusion.

**Recommendation**: Assign DR-009 to "Beverages Data" in v2.0; preserve DR-005 as "Data Lineage Metadata" for backward compatibility.

---

#### M4: DPIA Needs Refresh

**Severity**: MEDIUM
**Location**: ARC-001-DPIA-v1.0

**Description**: DPIA references PostgreSQL (should be SQLite), states "150 restaurants" (current: 243), and predates several data source integrations (Companies House, ONS, business rates). While the core DPIA conclusion (LOW RISK) remains valid, implementation details are outdated.

---

#### M5: Backlog Non-Standard Document ID

**Severity**: MEDIUM
**Location**: ARC-001-BKLG-v1.0

**Description**: Uses `ARC-001-BACKLOG-v1.0` instead of `ARC-001-BKLG-v1.0`.

---

#### M6: NFR Requirements Lack Stakeholder References

**Severity**: MEDIUM
**Location**: ARC-001-REQ-v2.0

**Description**: ~8 technical NFR requirements (NFR-S-001/002, NFR-SEC-002/003, NFR-O-001/002, NFR-M-002/003) lack explicit stakeholder driver references (`SD-x`, `G-x`).

---

#### M7: No SOBC for Commercial Expansion

**Severity**: MEDIUM
**Location**: —

**Description**: No Strategic Outline Business Case exists. While not required at current scale, recommended if planning B2B SaaS expansion or geographic growth.

---

### Low Priority Issues

#### L1: DPIA Non-Standard Document ID

Uses `ARCKIT-DPIA-20251117-001-PLYMOUTH-RESEARCH` instead of `ARC-001-DPIA-v1.0`.

#### L2: Terminology Drift

Minor inconsistencies: "MUST_HAVE" vs "MUST", "Hygiene rating" vs "FSA rating". Non-blocking.

#### L3: Backlog Sprint Plan Expired

Sprint 8 (Week 16) endpoint was ~March 2026. Backlog should be archived or refreshed.

---

## Metrics Dashboard

### Requirement Quality
- Total Requirements: 57
- Ambiguous Requirements: 1 (FR-010 semantic conflict)
- Duplicate Requirements: 0 (deduplicated in TRAC v2.0)
- Untestable Requirements: 0
- ID Reuse Issues: 1 (DR-005)
- **Quality Score**: 78%

### Architecture Alignment
- Principles Compliant: 12/18 (67%)
- Principles Partial: 5/18 (28%)
- Principles Non-Compliant: 1/18 (6%)
- NON-NEGOTIABLE Principles: ✅ Both compliant
- **Alignment Score**: 78%

### Traceability
- Requirements with Design: 38/57 (67%)
- Requirements with Implementation: 36/57 (63%)
- Requirements with Tests: 0/57 (0%)
- Orphan Design Elements: 1
- **Traceability Score**: 48%

### Stakeholder Traceability
- Requirements traced to stakeholder goals: ~85%
- Orphan requirements: ~8 (technical NFRs)
- Conflicts resolved: 4/4 (100%)
- RACI governance alignment: 95%
- **Stakeholder Score**: 90%

### Risk Management
- Total Risks: 20
- Critical Residual: 2 (R-001, R-003)
- High Residual: 6
- Risk owners from RACI: 100%
- Risk reduction achieved: 49%
- Risk register freshness: ⚠️ Overdue (M2)
- **Risk Management Score**: 82%

### Data Model
- DR-xxx mapped to entities: 88% (7/8)
- PII identified: 100% (0 PII — correct)
- Data governance complete: 90%
- Database tech consistency: ❌ (H5)
- **Data Model Score**: 88%

### Compliance Posture
- GDPR/DPIA: ✅ Compliant
- Ethical Scraping: ✅ Compliant
- OGL: ✅ Compliant
- HTTPS: ❌ Not enforced (H3)
- Privacy Policy: ⚠️ Not published
- **Compliance Score**: 85%

### Overall Governance Health

**Score**: 72/100
**Grade**: C

**Grade Thresholds**:
- A (90-100%): Excellent governance, ready to proceed
- B (80-89%): Good governance, minor issues
- C (70-79%): Adequate governance, address high-priority issues
- D (60-69%): Poor governance, major rework needed
- F ( < 60%): Insufficient governance, do not proceed

---

## Recommendations

### Critical Actions (MUST resolve before public launch)

1. **[C1] Implement automated test suite**: Zero test coverage creates unacceptable risk for data quality (R-003) and regression detection. Target 50%+ coverage for data pipeline. — Addresses C1, Principle #16
2. **[C2] Fix FR-010 semantic mismatch**: Create FR-012 for "Scheduled Data Refresh", update ADR-001 to reference correct ID. — Addresses C2

### High Priority Actions (SHOULD resolve before public launch)

1. **[H1] Add automated compliance testing**: Robots.txt validation and PII scan before every scrape batch. — Addresses H1, Risk R-001
2. **[H2] Create system architecture diagram**: Run `/arckit:diagram` to document C4 Context and Container views. — Addresses H2
3. **[H3] Deploy with HTTPS**: Use Streamlit Cloud, Render, or Railway for free HTTPS. — Addresses H3, NFR-SEC-001
4. **[H4] Configure uptime monitoring**: Set up UptimeRobot free tier. — Addresses H4, NFR-A-001
5. **[H5] Update data model for SQLite**: Correct DATA-v1.0 Technical Foundation section. — Addresses H5

### Medium Priority Actions (Improve quality)

1. **[M1] Document priority change rationale**: Add to REQ-v2.0 revision history. — Addresses M1
2. **[M2] Refresh risk register**: Run `/arckit:risk` to update. — Addresses M2
3. **[M3] Fix DR-005 ID reuse**: Assign DR-009 to beverages. — Addresses M3
4. **[M4] Update DPIA**: Refresh implementation details. — Addresses M4
5. **[M5-M6] Fix document IDs and stakeholder refs**: Housekeeping. — Addresses M5, M6

### Low Priority Actions (Optional improvements)

1. **[L1-L3] Fix DPIA document ID, terminology drift, archive expired backlog**. — Addresses L1, L2, L3

---

## Next Steps

### Immediate Actions

1. **CRITICAL issues exist**: ⚠️ **Address C1 and C2 before public launch.**
   - C1: Implement pytest test suite (2-3 sprints)
   - C2: Fix FR-010 mismatch (1-2 hours)

2. **HIGH issues**: Address H1-H5 before public launch (1-2 sprints combined)

### Suggested Commands

**Governance Foundation**:
- `/arckit:risk` — Refresh overdue risk register (M2)
- `/arckit:sobc` — Create business case if commercial expansion planned (M7)

**Requirements & Design**:
- `/arckit:requirements` — Refresh to fix FR-010, DR-005, priority rationale
- `/arckit:diagram` — Create C4 architecture diagrams (H2)

**Analysis & Traceability**:
- `/arckit:traceability` — Re-run after fixing C2 and adding tests
- `/arckit:analyze` — Re-run after addressing Critical/High findings

### Re-run Analysis

After making changes, re-run:
```
/arckit:analyze
```

Expected improvement: Score should increase from 72 to 85+ after addressing C1, C2, H1-H5.

---

## Appendix A: Artifacts Analyzed

| Artifact | Location | Last Modified | Status |
|----------|----------|---------------|--------|
| Architecture Principles | `projects/000-global/ARC-000-PRIN-v1.0.md` | 2025-11-15 | ✅ Analyzed |
| Stakeholder Drivers | `projects/001-*/ARC-001-STKE-v1.0.md` | 2025-11-15 | ✅ Analyzed |
| Requirements v1.0 | `projects/001-*/ARC-001-REQ-v1.0.md` | 2025-11-22 | ✅ Analyzed (superseded by v2.0) |
| Requirements v2.0 | `projects/001-*/ARC-001-REQ-v2.0.md` | 2026-02-17 | ✅ Analyzed |
| Risk Register | `projects/001-*/ARC-001-RISK-v1.0.md` | 2025-11-17 | ✅ Analyzed |
| DPIA | `projects/001-*/ARC-001-DPIA-v1.0.md` | 2025-11-17 | ✅ Analyzed |
| Data Model | `projects/001-*/ARC-001-DATA-v1.0.md` | 2025-11-22 | ✅ Analyzed |
| Data Source Discovery | `projects/001-*/ARC-001-DSCT-v1.0.md` | 2025-11-22 | ✅ Analyzed |
| ADR-001 Cloud Platform | `projects/001-*/decisions/ARC-001-ADR-001-v1.0.md` | 2025-11-22 | ✅ Analyzed |
| Product Backlog | `projects/001-*/ARC-001-BKLG-v1.0.md` | 2025-11-15 | ✅ Analyzed |
| Traceability Matrix | `projects/001-*/ARC-001-TRAC-v2.0.md` | 2026-03-01 | ✅ Analyzed |
| Research Findings | `projects/001-*/research/ARC-001-RSCH-001-v1.0.md` | 2025-11-22 | ✅ Analyzed |
| AWS Research | `projects/001-*/research/ARC-001-AWRS-v1.0.md` | 2025-11-22 | ✅ Analyzed |
| Azure Research | `projects/001-*/research/ARC-001-AZRS-v1.0.md` | 2025-11-22 | ✅ Analyzed |
| Vendor Profiles | `projects/001-*/vendors/*.md` | Various | ✅ Analyzed (10 profiles) |
| Tech Notes | `projects/001-*/tech-notes/*.md` | Various | ✅ Analyzed (6 notes) |
| Previous Analysis v1.0 | `projects/001-*/ARC-001-ANAL-v1.0.md` | 2025-11-23 | ✅ Referenced |

**Total Artifacts Analyzed**: 17 primary + 16 supporting = 33 documents

---

## Appendix B: Analysis Methodology

**Analysis Date**: 2026-03-01
**Analyzed By**: ArcKit `/arckit:analyze` command

**Checks Performed**:
- Requirements completeness and quality (57 deduplicated requirements)
- Architecture principles compliance (18 principles)
- Stakeholder traceability (10 drivers, 8 goals, 4 outcomes)
- Risk coverage and mitigation (20 risks)
- Data model consistency (9 entities, 142 attributes)
- Design quality (ADR, DATA, DSCT — no HLD/DLD)
- Compliance posture (GDPR, OGL, ethical scraping)
- Traceability (TRAC v2.0 analysis)
- Consistency across artifacts

**Severity Classification**:
- CRITICAL: Blocks public launch, must resolve immediately
- HIGH: Significant risk, resolve before public launch
- MEDIUM: Should be addressed, can proceed with caution
- LOW: Minor issues, address when convenient

**Scoring Methodology**:
Weighted average across 7 dimensions:
- Requirements Quality (15%): 78% × 0.15 = 11.7
- Principles Compliance (15%): 78% × 0.15 = 11.7
- Traceability (20%): 48% × 0.20 = 9.6
- Stakeholder Alignment (10%): 90% × 0.10 = 9.0
- Risk Management (15%): 82% × 0.15 = 12.3
- Data Model (10%): 88% × 0.10 = 8.8
- Compliance (15%): 85% × 0.15 = 12.75
- **Total**: 75.85 → **72** (rounded with deductions for 2 CRITICAL issues at −2 each)

---

**Generated by**: ArcKit `/arckit:analyze` command
**Generated on**: 2026-03-01 12:00 GMT
**ArcKit Version**: 2.22.3
**Project**: Plymouth Research Restaurant Menu Analytics (Project 001)
**AI Model**: claude-opus-4-6
**Generation Context**: Analysed 17 primary artifacts including REQ v2.0 (57 requirements), TRAC v2.0, RISK v1.0 (20 risks), STKE v1.0 (10 drivers), DATA v1.0 (9 entities), DPIA v1.0, ADR-001, BKLG v1.0, DSCT v1.0, 3 research artifacts, 10 vendor profiles, and 6 tech notes
