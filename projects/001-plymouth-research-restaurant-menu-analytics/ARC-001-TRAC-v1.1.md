# Requirements Traceability Matrix: Plymouth Research Restaurant Menu Analytics

> **Template Status**: Live | **Version**: 1.1 | **Command**: `/arckit.traceability`

## Document Control

| Field | Value |
|-------|-------|
| **Document ID** | ARC-001-TRAC-v1.1 |
| **Document Type** | Requirements Traceability Matrix |
| **Project** | Plymouth Research Restaurant Menu Analytics (Project 001) |
| **Classification** | PUBLIC |
| **Status** | DRAFT |
| **Version** | 1.1 |
| **Created Date** | 2026-03-01 |
| **Last Modified** | 2026-03-01 |
| **Review Cycle** | Monthly |
| **Next Review Date** | 2026-03-31 |
| **Owner** | Mark Craddock (Product Owner / Technical Lead) |
| **Reviewed By** | [PENDING] |
| **Approved By** | [PENDING] |
| **Distribution** | Project Team, Architecture Team |

## Revision History

| Version | Date | Author | Changes | Approved By | Approval Date |
|---------|------|--------|---------|-------------|---------------|
| 1.0 | 2026-03-01 | ArcKit AI | Initial creation from `/arckit.traceability` command | [PENDING] | [PENDING] |
| 1.1 | 2026-03-01 | ArcKit AI | Recognised ARC-001-DATA-v1.0 as formal design coverage for DR requirements; added research artifacts (AWRS, AZRS, RSCH-001) as design evidence; included vendor profiles as implementation evidence; added coverage trend data; refined traceability score | [PENDING] | [PENDING] |

## Document Purpose

This document provides end-to-end traceability from business, integration, and data requirements through architectural design decisions, implementation components, and test coverage for the Plymouth Research Restaurant Menu Analytics platform. It identifies coverage gaps and orphaned design elements to support governance and release decisions.

---

## 1. Overview

### 1.1 Purpose

This Requirements Traceability Matrix (RTM) provides end-to-end traceability from business requirements through design, implementation, and testing. It ensures:

- All requirements are addressed in design
- All design elements trace to requirements
- All requirements are tested
- Coverage gaps are identified and tracked

### 1.2 Traceability Scope

This matrix traces requirements from two sources (ARC-001-REQ-v1.0 and ARC-001-REQ-v2.0) through architectural decisions, data model design, research artifacts, implementation, and testing.

```mermaid
flowchart TD
    REQ["Requirements<br/>ARC-001-REQ v1.0 & v2.0<br/>24 unique requirements"] --> ADR["Architecture Decisions<br/>ARC-001-ADR-001-v1.0"]
    REQ --> DATA["Data Model<br/>ARC-001-DATA-v1.0<br/>8 entities, 142 attributes"]
    REQ --> RSCH["Research Artifacts<br/>AWRS, AZRS, RSCH-001<br/>+ 10 vendor profiles"]
    ADR --> IMPL["Implementation<br/>Application Code<br/>dashboard_app.py, fetchers, matchers"]
    DATA --> IMPL
    RSCH --> IMPL
    IMPL --> TEST["Testing<br/>Manual/Exploratory<br/>No automated test suite"]

    style REQ fill:#E3F2FD
    style ADR fill:#FFF3E0
    style DATA fill:#E8F5E9
    style RSCH fill:#FCE4EC
    style IMPL fill:#F3E5F5
    style TEST fill:#FFF9C4
```

### 1.3 Document References

| Document | Version | Date | Link |
|----------|---------|------|------|
| Requirements Document | v1.0 | 2025-11-22 | ARC-001-REQ-v1.0.md |
| Requirements Document | v2.0 | 2026-02-17 | ARC-001-REQ-v2.0.md |
| Architecture Decision Record (Cloud Platform) | v1.0 | 2026-02-03 | decisions/ARC-001-ADR-001-v1.0.md |
| Data Model | v1.0 | 2026-02-12 | ARC-001-DATA-v1.0.md |
| AWS Research | v1.0 | — | research/ARC-001-AWRS-v1.0.md |
| Azure Research | v1.0 | — | research/ARC-001-AZRS-v1.0.md |
| Research Findings | v1.0 | — | research/ARC-001-RSCH-001-v1.0.md |
| Stakeholder Analysis | v1.0 | 2026-01-28 | ARC-001-STKE-v1.0.md |
| Risk Register | v1.0 | 2026-01-28 | ARC-001-RISK-v1.0.md |
| Data Source Discovery | v1.0 | — | ARC-001-DSCT-v1.0.md |
| DPIA | v1.0 | — | ARC-001-DPIA-v1.0.md |

---

## 2. Traceability Matrix

### 2.1 Forward Traceability: Requirements → Design → Implementation → Tests

#### 2.1.1 Business Requirements (BR)

| Req ID | Requirement | Priority | REQ Version | Design Reference | Implementation Evidence | Test Coverage | Status |
|--------|-------------|----------|-------------|-----------------|------------------------|---------------|--------|
| BR-001 | Comprehensive Restaurant Coverage | MUST | v1.0, v2.0 | — | 98 restaurants in DB; web scraping pipeline (`scripts/scrapers/`) | Manual verification of restaurant count | ⚠️ Partial |
| BR-002 | Multi-Source Data Aggregation | MUST | v1.0, v2.0 | — | FSA, Trustpilot, Google Places fetchers (`scripts/fetchers/`); 8 data sources operational | Manual validation of data source counts | ⚠️ Partial |
| BR-003 | Cost-Efficient Operations | MUST | v1.0, v2.0 | ADR-001 (Azure ~£26/month, 74% budget headroom) | Currently £0 (Streamlit Cloud free tier); ADR-001 plans Azure at £26/month | Cost monitoring via Azure Cost Management (planned) | ✅ Covered |
| BR-004 | Legal and Ethical Compliance | MUST | v1.0, v2.0 | DPIA-v1.0 (data protection assessment) | robots.txt compliance, rate limiting (5s), honest User-Agent, GDPR considerations | Manual compliance review | ⚠️ Partial |
| BR-005 | Geographic Scalability | SHOULD | v1.0, v2.0 | ADR-001 (Azure App Service scalability pathway) | Plymouth-only scope; architecture supports expansion via config | Not tested | ❌ Gap |
| BR-006 | Data Freshness and Timeliness | MUST | v1.0, v2.0 | ADR-001 (Azure Functions timer triggers for FR-010) | Manual script execution; no automated scheduling yet | Manual verification of data dates | ⚠️ Partial |
| BR-007 | Public Dashboard Accessibility | MUST | v1.0, v2.0 | ADR-001 (Azure App Service B1 with custom domain) | `dashboard_app.py` (Streamlit, 8 tabs) deployed on Streamlit Cloud | Manual UI testing | ✅ Covered |
| BR-008 | Geographic Intelligence and Demographic Context | SHOULD | v2.0 | DATA-v1.0 (E-001 latitude/longitude, ONS geography fields planned) | Google Places lat/long stored; no demographic integration | Not tested | ❌ Gap |

#### 2.1.2 Integration Requirements (INT) — v2.0 only

| Req ID | Requirement | Priority | Design Reference | Implementation Evidence | Test Coverage | Status |
|--------|-------------|----------|-----------------|------------------------|---------------|--------|
| INT-001 | FSA Food Hygiene Rating Scheme | SHOULD | DATA-v1.0 (E-001 hygiene fields); DSCT-v1.0 | `fetch_hygiene_ratings_v2.py`; 49/98 matched | Manual matching validation | ⚠️ Partial |
| INT-002 | Trustpilot Reviews | SHOULD | DATA-v1.0 (E-003); DSCT-v1.0 | `fetch_trustpilot_reviews.py`; 63/98 restaurants, 9,410 reviews | Manual review count validation | ⚠️ Partial |
| INT-003 | Google Places API | SHOULD | DATA-v1.0 (E-004); DSCT-v1.0; vendor profile (google-places-api) | `fetch_google_reviews.py`; 98/98 restaurants, 481 reviews | Manual API response validation | ✅ Covered |
| INT-004 | Companies House API | SHOULD | DSCT-v1.0 | `fetch_companies_house_data.py` exists | Not tested | ⚠️ Partial |
| INT-005 | ONS Postcode Directory | SHOULD | DATA-v1.0 (E-001 ONS geography fields planned); DSCT-v1.0 | Not implemented | Not tested | ❌ Gap |
| INT-006 | Postcodes.io API | SHOULD | DSCT-v1.0; vendor profile (postcodes-io) | Not implemented (vendor profile exists) | Not tested | ❌ Gap |
| INT-007 | Plymouth City Council Licensing Data | SHOULD | DSCT-v1.0 | `scrape_plymouth_licensing_fixed.py` exists | Not tested | ⚠️ Partial |
| INT-008 | VOA Business Rates | SHOULD | DSCT-v1.0 | `match_business_rates_v3.py` exists | Not tested | ⚠️ Partial |

#### 2.1.3 Data Requirements (DR)

| Req ID | Requirement | Priority (v1.0 / v2.0) | Design Reference | Implementation Evidence | Test Coverage | Status |
|--------|-------------|------------------------|-----------------|------------------------|---------------|--------|
| DR-001 | Restaurant Master Data | MUST / SHOULD | DATA-v1.0 (E-001: 52 attributes defined) | `restaurants` table (52 cols, 243 rows) | Manual schema validation | ✅ Covered |
| DR-002 | Menu Item Data | MUST / SHOULD | DATA-v1.0 (E-002: 13 attributes defined) | `menu_items` table (13 cols, 2,625 rows) | Manual data quality checks | ✅ Covered |
| DR-003 | Trustpilot Reviews Data | MUST / SHOULD | DATA-v1.0 (E-003: 13 attributes defined) | `trustpilot_reviews` table (13 cols, 9,410 rows) | Manual review integrity checks | ✅ Covered |
| DR-004 | Google Reviews Data | SHOULD | DATA-v1.0 (E-004: attributes defined) | `google_reviews` table (481 rows) | Manual data validation | ✅ Covered |
| DR-005 | Data Lineage Metadata / Beverages Data | MUST (v1.0) / SHOULD (v2.0) | DATA-v1.0 (E-005: drinks entity defined) | `drinks` table exists; no formal lineage tracking | Not tested | ⚠️ Partial |
| DR-006 | Data Quality Metrics | SHOULD | DATA-v1.0 (E-006: quality metrics entity defined) | Ad-hoc quality scripts in `scripts/utilities/` | Not tested | ❌ Gap |
| DR-007 | Scraping Audit Log | SHOULD | DATA-v1.0 (E-007: audit log entity defined) | `scraped_at` timestamps; `logs/` directory | Not tested | ⚠️ Partial |
| DR-008 | Manual Match Records | SHOULD | DATA-v1.0 (E-008: manual matches entity defined) | `data/manual_matches/` directory; `interactive_matcher_app.py` | Manual validation | ⚠️ Partial |

**Legend**:

- ✅ **Covered**: Requirement has formal design reference AND implementation evidence
- ⚠️ **Partial**: Requirement has implementation evidence but incomplete design or testing
- ❌ **Gap**: Requirement not addressed in design or testing

---

### 2.2 Backward Traceability: Design → Requirements

#### 2.2.1 ADR-001 Requirement References

| Design Element | ADR-001 Component | Requirement IDs Referenced | Trace Status |
|----------------|-------------------|---------------------------|--------------|
| Azure App Service B1 | Dashboard hosting | BR-007, NFR-P-001, NFR-A-001 | ✅ BR-007 traced; NFR-P-001, NFR-A-001 are design-only |
| Azure PostgreSQL Flexible Server | Data storage | NFR-SEC-001, NFR-S-002 | ⚠️ Design-only (NFRs not in REQ) |
| Azure Functions | Scheduled scraping | FR-010, NFR-Q-003 | ⚠️ Design-only (FR/NFRs not in REQ) |
| Azure Key Vault | Secrets management | NFR-SEC-001, NFR-M-001 | ⚠️ Design-only |
| UK South region | Data residency | NFR-C-002 | ⚠️ Design-only |
| Cost model (~£26/month) | Budget compliance | BR-003 | ✅ Traced |

#### 2.2.2 DATA-v1.0 Entity → Requirement Mapping

| Entity | DATA-v1.0 Reference | Requirement IDs Covered | Trace Status |
|--------|---------------------|------------------------|--------------|
| E-001 Restaurants | 52 attributes, incl. hygiene, Google, ONS fields | DR-001, BR-001, BR-008, INT-001, INT-003, INT-005 | ✅ Traced |
| E-002 Menu Items | 13 attributes, prices, dietary tags | DR-002 | ✅ Traced |
| E-003 Trustpilot Reviews | 13 attributes, review lifecycle | DR-003, INT-002 | ✅ Traced |
| E-004 Google Reviews | Review attributes, place metadata | DR-004, INT-003 | ✅ Traced |
| E-005 Drinks | Beverage categories, pricing | DR-005 | ✅ Traced |
| E-006 Data Quality Metrics | Quality scores, completeness | DR-006 | ✅ Traced |
| E-007 Scraping Audit Log | Timestamps, status, rate limiting | DR-007, BR-004 | ✅ Traced |
| E-008 Manual Matches | Match records, confidence scores | DR-008 | ✅ Traced |

#### 2.2.3 Research Artifacts → Requirement Mapping

| Artifact | Design Evidence For | Trace Status |
|----------|-------------------|--------------|
| ARC-001-AZRS-v1.0 (Azure Research) | BR-003 (cost), BR-007 (hosting), BR-005 (scalability) | ✅ Traced |
| ARC-001-AWRS-v1.0 (AWS Research) | BR-003 (cost comparison), BR-007 (hosting alternative) | ✅ Traced |
| ARC-001-RSCH-001-v1.0 (General Research) | BR-002 (data aggregation technology landscape) | ✅ Traced |
| ARC-001-DSCT-v1.0 (Data Source Discovery) | INT-001 through INT-008 (all integration sources) | ✅ Traced |

---

## 3. Coverage Analysis

### 3.1 Requirements Coverage Summary

| Category | Total (unique) | Formal Design | Implementation Evidence | Gap (neither) | % Design Coverage |
|----------|----------------|---------------|------------------------|---------------|-------------------|
| Business Requirements (BR) | 8 | 5 | 7 | 1 | 63% |
| Integration Requirements (INT) | 8 | 8 | 6 | 0 | 100% |
| Data Requirements (DR) | 8 | 8 | 7 | 0 | 100% |
| **Total** | **24** | **21** | **20** | **1** | **88%** |

**Note**: The hook reported 37 total requirements across both REQ versions. After deduplication (removing IDs that appear in both v1.0 and v2.0), there are 24 unique requirement IDs.

**v1.1 change**: Formal design coverage increased from 8% (v1.0 — ADR-001 only) to 88% by recognising ARC-001-DATA-v1.0, ARC-001-DSCT-v1.0, ARC-001-DPIA-v1.0, and research artifacts as formal design documents.

### 3.2 Coverage by Priority

| Priority | Total | Design Covered | Implementation Evidence | No Coverage | % Design |
|----------|-------|---------------|------------------------|-------------|----------|
| MUST | 8 | 7 | 7 | 0 | 88% |
| SHOULD | 16 | 14 | 13 | 1 | 88% |

**Target Coverage**: 100% of MUST requirements should be formally traced; > 80% of SHOULD.

**Current Status**: ON TRACK — 88% of MUST requirements have formal design traceability. The remaining gap (BR-001 Comprehensive Restaurant Coverage) has implementation evidence but no dedicated design artefact.

### 3.3 Implementation Coverage

| Component | Requirements Addressed | Evidence |
|-----------|----------------------|----------|
| `dashboard_app.py` (2,053 lines) | BR-001, BR-007, DR-001, DR-002 | 8-tab Streamlit dashboard |
| `scripts/fetchers/` (9 scripts) | BR-002, BR-006, INT-001–INT-004, INT-007–INT-008 | Data fetching pipeline |
| `scripts/matchers/` (4 scripts) | DR-001, DR-008 | Fuzzy matching with SequenceMatcher |
| `scripts/importers/` (7 scripts) | DR-001–DR-005 | Database import pipeline |
| `plymouth_research.db` (20 MB) | DR-001–DR-005, DR-007–DR-008 | SQLite, 52-column schema, triggers/views |
| Rate limiting & robots.txt | BR-004 | 5s delay, honest User-Agent |
| `interactive_matcher_app.py` | DR-008 | Streamlit matching UI |
| `data/manual_matches/` | DR-008 | Human-verified match records |

### 3.4 Test Coverage

| Test Level | Tests | Requirements Covered | % Coverage |
|------------|-------|---------------------|------------|
| Unit Tests | 0 | 0 | 0% |
| Integration Tests | 0 | 0 | 0% |
| E2E Tests | 0 | 0 | 0% |
| Performance Tests | 0 | 0 | 0% |
| Security Tests | 0 | 0 | 0% |
| Manual/Exploratory | Ad-hoc | ~20 (implementation validated) | ~83% |

**Test Coverage Goal**: 100% of MUST requirements tested.

**Critical finding**: No automated test suite exists. All testing is manual/exploratory per project documentation.

---

## 4. Gap Analysis

### 4.1 Requirements Without Formal Design (Orphan Requirements)

Requirements that have NO formal design reference:

| Req ID | Requirement | Priority | Implementation Exists? | Severity | Target |
|--------|-------------|----------|----------------------|----------|--------|
| BR-001 | Comprehensive Restaurant Coverage | MUST | Yes (98 restaurants, scraping pipeline) | LOW | Design note or ADR for coverage strategy |

**Impact**: BR-001 is the sole remaining requirement without a formal design reference. However, it has strong implementation evidence (98 restaurants with scraped data). A brief ADR or design note documenting the coverage strategy would close this gap.

### 4.2 Requirements Without Tests

All 24 requirements lack automated test coverage. The 5 highest-risk gaps:

| Req ID | Requirement | Priority | Design Component | Missing Test Type |
|--------|-------------|----------|-----------------|-------------------|
| BR-004 | Legal and Ethical Compliance | MUST | DPIA, rate limiting, robots.txt | Integration test for scraping compliance |
| BR-006 | Data Freshness and Timeliness | MUST | ADR-001 (Azure Functions), fetcher scripts | Integration test for data currency |
| BR-001 | Comprehensive Restaurant Coverage | MUST | Scraping pipeline | Data completeness validation |
| BR-002 | Multi-Source Data Aggregation | MUST | Multi-fetcher pipeline | End-to-end data pipeline test |
| DR-006 | Data Quality Metrics | SHOULD | DATA-v1.0 (E-006) | Data quality validation suite |

**Risk**: Without automated tests, regression detection relies entirely on manual inspection.

### 4.3 Design Elements Without Requirements (Scope Creep?)

Requirement IDs referenced in ADR-001 that do NOT exist in any REQ document:

| Referenced ID | ADR-001 Context | Assessment | Action |
|---------------|----------------|------------|--------|
| NFR-A-001 | 99% uptime SLA | Legitimate NFR — missing from REQ | Add to REQ v2.1 |
| NFR-P-001 | Dashboard load < 2s (p95) | Legitimate NFR — missing from REQ | Add to REQ v2.1 |
| NFR-P-002 | Query response < 500ms (p95) | Legitimate NFR — missing from REQ | Add to REQ v2.1 |
| NFR-S-002 | 100 concurrent users | Legitimate NFR — missing from REQ | Add to REQ v2.1 |
| NFR-SEC-001 | Encryption at rest and in transit | Legitimate NFR — missing from REQ | Add to REQ v2.1 |
| NFR-C-002 | UK GDPR compliance / data residency | Legitimate NFR — missing from REQ | Add to REQ v2.1 |
| NFR-M-001 | Maintainability | Legitimate NFR — missing from REQ | Add to REQ v2.1 |
| NFR-Q-003 | Data freshness | Legitimate NFR — missing from REQ | Add to REQ v2.1 |
| FR-010 | Scheduled data refresh | Legitimate FR — missing from REQ | Add to REQ v2.1 |

**Assessment**: These are NOT scope creep. They are legitimate non-functional and functional requirements that were defined during ADR creation but were never back-populated into the requirements documents. The REQ documents (v1.0 and v2.0) use BR/INT/DR prefixes only and do not include FR or NFR categories.

**Recommendation**: Update ARC-001-REQ to v2.1 to incorporate FR and NFR requirements, aligning with the ADR references.

---

## 5. Non-Functional Requirements Traceability

### 5.1 Performance Requirements

| NFR ID | Requirement | Target | Design Strategy (ADR-001) | Implementation | Test Plan | Status |
|--------|-------------|--------|--------------------------|----------------|-----------|--------|
| NFR-P-001 | Dashboard page load | < 2s (p95) | Azure App Service B1 + Application Insights | Streamlit with 5-min cache TTL | Not tested (no load test) | ❌ Gap |
| NFR-P-002 | Database query response | < 500ms (p95) | PostgreSQL Flexible Server with indexes | SQLite with FTS indexes | Not tested | ❌ Gap |

### 5.2 Security Requirements

| NFR ID | Requirement | Design Control (ADR-001) | Implementation | Test Plan | Status |
|--------|-------------|-------------------------|----------------|-----------|--------|
| NFR-SEC-001 | Encryption at rest/transit | Azure Key Vault, AES-256, TLS 1.2 | Not yet (SQLite unencrypted) | Not tested | ❌ Gap |

### 5.3 Availability & Resilience

| NFR ID | Requirement | Target | Design Strategy (ADR-001) | Test Plan | Status |
|--------|-------------|--------|--------------------------|-----------|--------|
| NFR-A-001 | Availability SLA | 99% uptime | Azure App Service SLA 99.95% | Not tested | ❌ Gap |

### 5.4 Compliance Requirements

| NFR ID | Requirement | Design Controls | Evidence | Status |
|--------|-------------|-----------------|----------|--------|
| NFR-C-002 | UK GDPR / data residency | ADR-001 (UK South region); DPIA-v1.0 | DPIA documented; currently US (Streamlit Cloud) | ⚠️ Partial |

---

## 6. Change Impact Analysis

### 6.1 Requirement Version Changes (v1.0 → v2.0)

| Change ID | REQ Version | Change Description | Impacted Components | Impact Level |
|-----------|-------------|--------------------|--------------------|--------------|
| CHG-001 | v2.0 | Added BR-008 (Geographic Intelligence) | Dashboard map tab (future); DATA-v1.0 ONS fields | LOW |
| CHG-002 | v2.0 | Added INT-001 through INT-008 (Integration Requirements) | All fetcher scripts; DSCT-v1.0 | MEDIUM |
| CHG-003 | v2.0 | Added DR-005 Beverages, DR-007 Scraping Audit, DR-008 Manual Matches | `drinks` table, `logs/`, `data/manual_matches/`; DATA-v1.0 E-005/E-007/E-008 | LOW |
| CHG-004 | v2.0 | Changed DR priorities from MUST to SHOULD | Reduces urgency of data requirement gaps | LOW |

### 6.2 Traceability Changes (v1.0 → v1.1)

| Change ID | Description | Impact |
|-----------|------------|--------|
| TRAC-001 | Recognised DATA-v1.0 as formal design coverage for all 8 DR requirements | Design coverage for DR increased from 0% to 100% |
| TRAC-002 | Recognised DSCT-v1.0 as formal design reference for all 8 INT requirements | Design coverage for INT increased from 0% to 100% |
| TRAC-003 | Recognised DPIA-v1.0 as design reference for BR-004 | BR-004 now has formal design evidence |
| TRAC-004 | Recognised ADR-001 scalability section as design reference for BR-005 | BR-005 now has formal design evidence (but no implementation) |
| TRAC-005 | Recognised ADR-001 Azure Functions section as design reference for BR-006 | BR-006 now has formal design evidence |
| TRAC-006 | Added backward traceability for DATA-v1.0 entities and research artifacts | Bidirectional traceability improved from 11% to 88% |

---

## 7. Metrics and KPIs

### 7.1 Traceability Metrics

| Metric | v1.0 Value | v1.1 Value | Target | Status |
|--------|-----------|-----------|--------|--------|
| Requirements with formal design coverage | 2/24 (8%) | 21/24 (88%) | 100% | ⚠️ At Risk |
| Requirements with implementation evidence | 19/24 (79%) | 20/24 (83%) | 100% | ⚠️ At Risk |
| Requirements with automated test coverage | 0/24 (0%) | 0/24 (0%) | 100% MUST, 80% SHOULD | ❌ Behind |
| Orphan design elements (no requirement trace) | 9 | 9 | 0 | ❌ Behind |
| Outstanding requirement gaps (no design) | 22 | 3 | 0 | ⚠️ At Risk |

### 7.2 Traceability Score

**Overall Traceability Score: 52/100** (up from 28/100 in v1.0)

| Dimension | Weight | v1.0 Score | v1.1 Score | Weighted (v1.1) |
|-----------|--------|-----------|-----------|-----------------|
| Formal design coverage | 30% | 8% | 88% | 26.4 |
| Implementation evidence | 30% | 79% | 83% | 24.9 |
| Test coverage (automated) | 25% | 0% | 0% | 0 |
| Bidirectional traceability | 15% | 11% | 88% | 13.2 |
| **Total** | **100%** | | | **64.5 → adjusted 52** |

**Adjustment note**: Score reduced from 64.5 to 52 because 0% automated test coverage for a platform with MUST requirements represents a critical governance gap that outweighs design-level coverage improvements.

**Recommendation**: GAPS MUST BE ADDRESSED — Design traceability is now strong (88%) but the complete absence of automated testing and 9 orphan design elements remain critical blockers for production readiness.

### 7.3 Coverage Trends

| Date | Version | Design Coverage | Implementation Coverage | Test Coverage | Score |
|------|---------|----------------|------------------------|---------------|-------|
| 2026-03-01 | v1.0 | 8% | 79% | 0% | 28/100 |
| 2026-03-01 | v1.1 | 88% | 83% | 0% | 52/100 |

**Trend**: Improving (design traceability significantly strengthened by recognising DATA-v1.0 and research artifacts)

---

## 8. Action Items

### 8.1 Blocking Gaps (Must Fix Before Production Release)

| ID | Gap Description | Owner | Priority | Target Date | Status |
|----|-----------------|-------|----------|-------------|--------|
| GAP-001 | Create FR and NFR requirements in REQ v2.1 (9 design-only references need formal requirements) | Product Owner | HIGH | 2026-03-31 | Open |
| GAP-002 | Add automated test suite — at minimum, integration tests for MUST requirements (BR-001, BR-002, BR-003, BR-004, BR-006, BR-007) | Technical Lead | HIGH | 2026-04-30 | Open |
| GAP-003 | Create design note or ADR for restaurant coverage strategy (closes BR-001 orphan gap) | Technical Lead | MEDIUM | 2026-03-31 | Open |

### 8.2 Non-Blocking Gaps (Fix in Next Sprint)

| ID | Gap Description | Owner | Priority | Target Date | Status |
|----|-----------------|-------|----------|-------------|--------|
| GAP-004 | Implement ONS Postcode Directory integration (INT-005) | Data Engineer | MEDIUM | 2026-04-30 | Open |
| GAP-005 | Implement Postcodes.io API integration (INT-006) | Data Engineer | MEDIUM | 2026-04-30 | Open |
| GAP-006 | Implement formal data quality metrics framework (DR-006) | Data Engineer | MEDIUM | 2026-04-30 | Open |
| GAP-007 | Add geographic intelligence / demographic context (BR-008) | Data Engineer | LOW | 2026-06-30 | Open |
| GAP-008 | Implement data lineage tracking beyond timestamps (DR-005 partial) | Data Engineer | LOW | 2026-06-30 | Open |

### 8.3 Orphan Resolution

| ID | Orphan Item | Type | Resolution | Owner | Target Date | Status |
|----|-------------|------|------------|-------|-------------|--------|
| ORP-001 | NFR-A-001 (99% uptime) | Design-only reference | Add to REQ v2.1 as NFR | Product Owner | 2026-03-31 | Open |
| ORP-002 | NFR-P-001 (Dashboard < 2s) | Design-only reference | Add to REQ v2.1 as NFR | Product Owner | 2026-03-31 | Open |
| ORP-003 | NFR-P-002 (Query < 500ms) | Design-only reference | Add to REQ v2.1 as NFR | Product Owner | 2026-03-31 | Open |
| ORP-004 | NFR-S-002 (100 concurrent users) | Design-only reference | Add to REQ v2.1 as NFR | Product Owner | 2026-03-31 | Open |
| ORP-005 | NFR-SEC-001 (Encryption) | Design-only reference | Add to REQ v2.1 as NFR | Product Owner | 2026-03-31 | Open |
| ORP-006 | NFR-C-002 (UK GDPR) | Design-only reference | Add to REQ v2.1 as NFR | Product Owner | 2026-03-31 | Open |
| ORP-007 | NFR-M-001 (Maintainability) | Design-only reference | Add to REQ v2.1 as NFR | Product Owner | 2026-03-31 | Open |
| ORP-008 | NFR-Q-003 (Data freshness) | Design-only reference | Add to REQ v2.1 as NFR | Product Owner | 2026-03-31 | Open |
| ORP-009 | FR-010 (Scheduled data refresh) | Design-only reference | Add to REQ v2.1 as FR | Product Owner | 2026-03-31 | Open |

---

## 9. Review and Approval

### 9.1 Review Checklist

- [x] All business requirements traced to design or implementation
- [x] All integration requirements traced to design documents (DSCT-v1.0, DATA-v1.0)
- [x] All data requirements traced to data model (DATA-v1.0 entities E-001–E-008)
- [ ] All design components traced back to requirements (9 orphans outstanding)
- [ ] All requirements have automated test coverage (0% automated)
- [x] All gaps identified with severity and recommended actions
- [ ] All NFRs addressed in design and test plan (design addressed in ADR-001; no test plan)
- [x] Change impact analysis complete (v1.0 → v2.0 changes documented; v1.0 → v1.1 TRAC changes documented)
- [x] Coverage percentages calculated per requirement type
- [x] Forward and backward traceability links present

### 9.2 Approval

| Role | Name | Review Date | Approval | Signature | Date |
|------|------|-------------|----------|-----------|------|
| Product Owner | Mark Craddock | [PENDING] | [ ] Approve [ ] Reject | _________ | [PENDING] |
| Technical Lead | [PENDING] | [PENDING] | [ ] Approve [ ] Reject | _________ | [PENDING] |

---

## 10. Appendices

### Appendix A: Full Requirements List

- ARC-001-REQ-v1.0.md — Original requirements (BR-001–BR-007, DR-001–DR-006)
- ARC-001-REQ-v2.0.md — Extended requirements (BR-001–BR-008, INT-001–INT-008, DR-001–DR-008)

### Appendix B: Design Documents

- ARC-001-ADR-001-v1.0.md — Select Azure as Cloud Platform over AWS
- ARC-001-DATA-v1.0.md — Data Model (8 entities, 142 attributes)
- ARC-001-DSCT-v1.0.md — Data Source Discovery (22 sources identified)
- ARC-001-DPIA-v1.0.md — Data Protection Impact Assessment
- research/ARC-001-AWRS-v1.0.md — AWS Research
- research/ARC-001-AZRS-v1.0.md — Azure Research
- research/ARC-001-RSCH-001-v1.0.md — General Research Findings

### Appendix C: Test Coverage

No automated test suite is currently configured. Testing is manual/exploratory only. A test framework (pytest recommended) should be established as part of GAP-002.

### Appendix D: Coverage Heatmap

```mermaid
quadrantChart
    title Requirement Coverage by Category (v1.1)
    x-axis Low Implementation --> High Implementation
    y-axis Low Design Coverage --> High Design Coverage
    quadrant-1 Well Governed
    quadrant-2 Design Without Code
    quadrant-3 Ungoverned
    quadrant-4 Code Without Design
    Business-BR: [0.75, 0.63]
    Integration-INT: [0.5, 1.0]
    Data-DR: [0.7, 1.0]
```

### Appendix E: Vendor Profiles (Implementation Evidence)

| Vendor Profile | Supports Requirements | Status |
|----------------|----------------------|--------|
| duckdb-profile.md | BR-002 (analytics engine alternative) | Evaluated |
| github-actions-profile.md | BR-006 (CI/CD for automated refresh) | Evaluated |
| google-places-api-profile.md | INT-003 (Google Places integration) | Implemented |
| plotly-dash-profile.md | BR-007 (dashboard alternative) | Evaluated |
| postcodes-io-profile.md | INT-006 (geocoding API) | Evaluated |
| render-profile.md | BR-007 (hosting alternative) | Evaluated |
| scrapy-profile.md | BR-001, BR-002 (scraping framework) | Evaluated |
| sentry-profile.md | BR-007 (error monitoring) | Evaluated |
| streamlit-profile.md | BR-007 (dashboard framework) | Implemented |
| uptimerobot-profile.md | NFR-A-001 (uptime monitoring) | Evaluated |

## External References

| Document | Type | Source | Key Extractions | Path |
|----------|------|--------|-----------------|------|
| FSA FHRS Data | XML | Food Standards Agency | Restaurant hygiene ratings | data/raw/plymouth_fsa_data.xml |
| Trustpilot Reviews | Web scraping | Trustpilot.com | 9,410 customer reviews | trustpilot_reviews table |
| Google Places API | API | Google | 481 reviews + metadata | google_reviews table |
| Companies House | API | Companies House | Business financial data | fetch_companies_house_data.py |
| Plymouth Licensing | Web scraping | Plymouth City Council | Licensing data | scrape_plymouth_licensing_fixed.py |
| VOA Business Rates | Web scraping | Valuation Office Agency | Business rates | match_business_rates_v3.py |

---

**Generated by**: ArcKit `/arckit.traceability` command
**Generated on**: 2026-03-01 14:30 GMT
**ArcKit Version**: 2.22.3
**Project**: Plymouth Research Restaurant Menu Analytics (Project 001)
**AI Model**: Claude Opus 4.6 (claude-opus-4-6)
**Generation Context**: Based on ARC-001-REQ-v1.0, ARC-001-REQ-v2.0, ARC-001-ADR-001-v1.0, ARC-001-DATA-v1.0, ARC-001-DSCT-v1.0, ARC-001-DPIA-v1.0, research artifacts (AWRS, AZRS, RSCH-001), 10 vendor profiles, and project CLAUDE.md implementation documentation. Updated from TRAC v1.0 with expanded design artifact recognition.
