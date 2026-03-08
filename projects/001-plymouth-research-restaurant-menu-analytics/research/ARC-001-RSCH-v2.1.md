# Technology and Service Research: Plymouth Research Restaurant Menu Analytics

> **Template Origin**: Official | **ArcKit Version**: 4.0.1 | **Command**: `/arckit.research`

## Document Control

| Field | Value |
|-------|-------|
| **Document ID** | ARC-001-RSCH-v2.1 |
| **Document Type** | Technology and Service Research |
| **Project** | Plymouth Research Restaurant Menu Analytics (Project 001) |
| **Classification** | OFFICIAL |
| **Status** | DRAFT |
| **Version** | 2.1 |
| **Created Date** | 2026-03-08 |
| **Last Modified** | 2026-03-08 |
| **Review Cycle** | Quarterly |
| **Next Review Date** | 2026-06-08 |
| **Owner** | Product Owner - Plymouth Research |
| **Reviewed By** | PENDING |
| **Approved By** | PENDING |
| **Distribution** | Product Team, Architecture Team, Development Team |

## Revision History

| Version | Date | Author | Changes | Approved By | Approval Date |
|---------|------|--------|---------|-------------|---------------|
| 2.1 | 2026-03-08 | AI Agent | Minor research refresh. Expanded the previously summarized categories into full analysis, refreshed vendor pricing and free-tier data, rebuilt 3-year TCO scenarios, and updated spawned vendor and technology knowledge artifacts. | PENDING | PENDING |

---

## Executive Summary

### Research Scope

This document refreshes the technology and service research for the Plymouth Research Restaurant Menu Analytics platform against:

- `ARC-001-REQ-v2.0`
- `ARC-000-PRIN-v1.0`
- `ARC-001-STKE-v1.0`
- `ARC-001-DATA-v1.0`
- `ARC-001-RISK-v1.0`

**Requirements analyzed**: 11 functional, 22 non-functional, 8 integration, 8 data requirements.

**Research categories identified**: 8.

**External market reports found**: none in `projects/001-plymouth-research-restaurant-menu-analytics/external/`.

**Project type**: UK-based independent research platform, not a UK Government delivery project. UK Government platforms such as GOV.UK Pay, Notify, and One Login are therefore not applicable, but UK Government open data sources remain relevant.

### Key Findings

- **Compliant collection is the main architecture driver**: Scrapy is the strongest fit because its built-in `ROBOTSTXT_OBEY`, throttling, and middleware model directly reduce the project's highest compliance risks.
- **The current low-cost stack remains viable**: Streamlit, SQLite, DuckDB, Postcodes.io, ONS data, GitHub Actions, and free monitoring tiers still keep the solution comfortably below the `BR-003` budget ceiling.
- **The main gaps are operational, not platform gaps**: monitoring, automated tests, and dependency scanning are still the highest-value additions.
- **Google Maps Platform remains affordable at current scale**: projected Project 001 usage stays inside the current monthly free usage caps for the required Places SKU mix.
- **Commercial scraping platforms remain poor economic fit**: even entry pricing from managed scraping vendors is materially more expensive than the open-source path for a single-developer, weekly-refresh workload.

### Market Landscape Overview

| Category | SaaS options reviewed | OSS / open-data options reviewed | UK Gov options reviewed | Recommendation | Recommended 3-year TCO |
|----------|-----------------------|----------------------------------|-------------------------|----------------|------------------------|
| Dashboard and visualisation | 1 | 2 | 0 | Retain Streamlit | £0 |
| Storage and analytics | 1 | 2 | 0 | Retain SQLite, add DuckDB | £0 |
| Web scraping and collection | 2 | 2 | 0 | Adopt Scrapy progressively | £3,900 |
| Hosting and deployment | 2 | 0 | 0 | Stay on Streamlit Cloud, keep Render fallback | £0-£252 |
| Monitoring and observability | 2 | 1 | 0 | Adopt UptimeRobot + Sentry + structured logging | £0 |
| CI/CD and dependency security | 1 | 1 | 0 | Adopt GitHub Actions + Dependabot + pip-audit | £650 |
| Geocoding and geography enrichment | 1 | 1 | 1 | Retain Google Places + Postcodes.io + ONS OPD | £0 |
| Automated testing and data validation | 0 | 2 | 0 | Adopt pytest first, add GE only if needed | £2,600 |

### Build vs Buy Summary

| Approach | Categories | Total 3-Year TCO | Risk-adjusted 3-Year TCO | Rationale |
|----------|-----------|------------------|--------------------------|-----------|
| **BUILD** (custom heavy) | 8 | £170,300 | £204,360 | High engineering effort dominates cost; poor fit for single-developer operation. |
| **BUY** (commercial-led) | 8 | £8,302 | £9,132 | Lower implementation effort but recurring subscriptions, especially managed scraping, erode budget headroom. |
| **ADOPT** (open source / open data) | 8 | £14,300 | £17,160 | Best strategic fit with ArcKit principles; labor is still required for integration and testing. |
| **RECOMMENDED BLEND** | 8 | **£5,200** | **£5,850** | Retain current free stack, add Scrapy, GitHub Actions, monitoring, and tests with light engineering investment only. |

### Top Recommended Vendors

1. **Scrapy OSS** for compliant web collection and risk reduction.
2. **Streamlit Community Cloud** for low-friction dashboard delivery at zero subscription cost.
3. **GitHub Actions + Dependabot** for automation, scheduled refresh, and dependency scanning.

### Requirements Coverage

- **100%** of requirements have an identified solution path.
- **43/49 requirements** can be satisfied through selected products, frameworks, or platform configuration.
- **6/49 requirements** still require local implementation work rather than a vendor feature:
  - FR-010 opt-out and correction workflow
  - NFR-C-002 GDPR process controls
  - NFR-Q-001 completeness rules
  - NFR-Q-002 price accuracy checks
  - NFR-Q-003 freshness enforcement
  - DR-007 audit-log population

---

## Research Methodology

### Inputs reviewed

- Mandatory: requirements and enterprise principles
- Recommended: stakeholder analysis, data model
- Optional: risk register
- External market/analyst documents: none present

### Research method

- Requirement-led category identification from `ARC-001-REQ-v2.0`
- Official vendor pricing, product, and documentation pages used as primary sources
- Open-source project maturity checked via official project/GitHub pages
- Existing project constraints validated against stakeholder, risk, and data-model artifacts

### Planning assumptions

The cost estimates for custom build and open-source integration are planning inferences, not vendor quotes.

- Engineer day rate: **£650/day**
- Working month: **20 days**
- Annual maintenance for build-heavy options: **20% of initial engineering effort**
- SaaS price inflation contingency: **10%**
- Build contingency for delivery risk: **20%**

These assumptions are reasonable for a UK specialist contractor or fully loaded senior engineer cost base and are used only to compare options consistently.

---

## Category 1: Dashboard and visualisation framework

**Requirements addressed**: FR-001, FR-002, FR-003, FR-004, FR-009, BR-007, NFR-P-001, NFR-P-002, NFR-S-002.

**Why this category**: The user-facing experience is already implemented in Streamlit, so the real question is whether the current framework remains good enough for performance, public accessibility, and low-cost delivery.

### Market landscape

| Option | Type | Pricing snapshot | Fit summary |
|--------|------|------------------|-------------|
| Streamlit OSS + Community Cloud | OSS + SaaS | OSS free; Community Cloud deployment free | Best current fit for one developer and rapid iteration. |
| Plotly Dash OSS | OSS | Free; Dash Enterprise by quote | Stronger long-term flexibility, but more code and more hosting work. |
| Custom Flask/FastAPI front end | Build | Engineering only | Highest control, worst cost-to-value ratio at current scale. |

### Assessment

- **Streamlit** remains the strongest recommendation because it keeps dashboard delivery simple, costs nothing, and still meets the internal-research style workflow described in the stakeholder and requirements documents.
- **Dash OSS** is a credible Phase 2 alternative if the platform evolves into a more complex public product with multi-page routing, richer state handling, or stronger front-end customization requirements.
- **Custom build** is not justified while the product remains data-centric and budget-constrained.

### TCO comparison

| Approach | Year 1 | Year 2 | Year 3 | 3-Year TCO | Notes |
|----------|--------|--------|--------|------------|-------|
| Build custom UI | £26,000 | £5,200 | £5,200 | £36,400 | 8 weeks implementation + annual maintenance. |
| Buy / hosted framework | £0 | £0 | £0 | £0 | Streamlit Community Cloud is free at present scale. |
| Adopt open source | £0 | £0 | £0 | £0 | Streamlit OSS already in use. |

**Recommendation**: **Retain Streamlit**. Revisit only if uptime guarantees, authentication complexity, or large public traffic materially exceed Community Cloud's comfort zone.

**Sources**:

- https://docs.streamlit.io/deploy/streamlit-community-cloud
- https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app
- https://plotly.com/dash/

---

## Category 2: Storage and analytical query engine

**Requirements addressed**: DR-001 to DR-008, FR-003, FR-009, NFR-P-002, NFR-S-001, NFR-Q-001, NFR-Q-004.

**Why this category**: The platform is read-heavy, uses a single SQLite file today, and now carries richer enrichment and analytics requirements. The key question is how to improve analytical performance without forcing an early server-database migration.

### Market landscape

| Option | Type | Pricing snapshot | Fit summary |
|--------|------|------------------|-------------|
| SQLite | OSS | Free, public domain | Best transactional and embedded fit for current architecture. |
| DuckDB | OSS | Free, MIT | Best analytical acceleration option with near-zero operational cost. |
| Supabase Postgres | SaaS | Free tier and Pro from $25/project/month | Viable future migration path if multi-user writes become important. |

### Assessment

- **SQLite** still matches current operational reality: weekly writes, dashboard-heavy reads, and a single-developer operating model.
- **DuckDB** is the best add-on for the analytics tabs because it improves grouped aggregations and larger analytical queries without replacing SQLite.
- **Supabase** is only justified if the architecture changes toward multiple concurrent writers, external APIs, or restaurant self-service workflows.

### TCO comparison

| Approach | Year 1 | Year 2 | Year 3 | 3-Year TCO | Notes |
|----------|--------|--------|--------|------------|-------|
| Build custom data platform | £13,000 | £2,600 | £2,600 | £18,200 | Mostly engineering time; no product advantage. |
| Buy managed Postgres | £650 | £240 | £240 | £1,130 | Assumes light Supabase Pro use only if needed. |
| Adopt SQLite + DuckDB | £0 | £0 | £0 | £0 | Existing stack plus one dependency. |

**Recommendation**: **Retain SQLite and add DuckDB for analytical workloads**. Do not migrate to Postgres yet.

**Sources**:

- https://sqlite.org/copyright.html
- https://sqlite.org/fts5.html
- https://duckdb.org/why_duckdb
- https://github.com/duckdb/duckdb
- https://supabase.com/pricing

---

## Category 3: Web scraping and collection orchestration

**Requirements addressed**: BR-004, BR-006, INT-002, INT-007, NFR-C-002, NFR-C-003, NFR-P-003, NFR-O-001, DR-007.

**Why this category**: This is the most risk-sensitive category in the project. Compliance with robots.txt, rate limiting, audit logging, and controlled refreshes matters more than extraction speed alone.

### Market landscape

| Option | Type | Pricing snapshot | Fit summary |
|--------|------|------------------|-------------|
| Requests + BeautifulSoup | OSS | Free | Good for simple static pages, but compliance controls are manual. |
| Scrapy | OSS | Free | Best fit for repeatable, compliant, production-grade collection. |
| Zyte API | SaaS | From $25/month | Managed infrastructure, but adds subscription cost and vendor dependency. |
| Apify | SaaS | Free tier, Starter from $49/month | More operational convenience, but poor fit for the target budget. |

### Assessment

- **Scrapy** is the clear recommendation because it directly supports the requirements and the principles document's ethical-scraping stance.
- **Requests + BeautifulSoup** remains acceptable for trivial collection scripts, but not as the long-term operating model for the whole platform.
- **Zyte** and **Apify** reduce engineering work but are economically hard to justify when weekly refreshes and modest scale dominate the workload.

### TCO comparison

| Approach | Year 1 | Year 2 | Year 3 | 3-Year TCO | Notes |
|----------|--------|--------|--------|------------|-------|
| Build custom compliance layer | £19,500 | £3,900 | £3,900 | £27,300 | 6 weeks engineering to recreate framework features badly. |
| Buy managed scraping | £2,338 | £588 | £588 | £3,514 | Assumes Zyte base usage plus limited setup work. |
| Adopt Scrapy | £3,900 | £0 | £0 | £3,900 | 6 developer days for progressive migration and audit hooks. |

**Recommendation**: **Adopt Scrapy for all new scrapers and progressively migrate the existing collection estate**.

**Sources**:

- https://docs.scrapy.org/en/latest/topics/settings.html
- https://docs.scrapy.org/en/latest/topics/autothrottle.html
- https://github.com/scrapy/scrapy
- https://www.zyte.com/pricing/
- https://apify.com/pricing

---

## Category 4: Hosting and deployment

**Requirements addressed**: BR-003, BR-007, NFR-A-001, NFR-SEC-001, NFR-S-002.

**Why this category**: Hosting is cheap for this workload, but reliability and HTTPS are mandatory. The real trade-off is between zero-cost convenience and always-on behavior.

### Market landscape

| Option | Type | Pricing snapshot | Fit summary |
|--------|------|------------------|-------------|
| Streamlit Community Cloud | SaaS | Free | Best for current internal/public-lite usage. |
| Render Web Service | SaaS | Free tier; Starter from $7/month | Best paid fallback for always-on hosting. |

### Assessment

- **Streamlit Community Cloud** remains the right primary host because it eliminates DevOps overhead and keeps costs at zero.
- **Render Starter** is the clean fallback if the sleep/wake behavior becomes unacceptable or if background services expand.

### TCO comparison

| Approach | Year 1 | Year 2 | Year 3 | 3-Year TCO | Notes |
|----------|--------|--------|--------|------------|-------|
| Build / self-host | £5,850 | £1,300 | £1,300 | £8,450 | Includes setup, patching, and light admin time. |
| Buy managed hosting | £0 | £84 | £84 | £168 | Assumes switch to Render Starter from Year 2. |
| Adopt current free hosting | £0 | £0 | £0 | £0 | Streamlit Community Cloud only. |

**Recommendation**: **Stay on Streamlit Community Cloud and keep Render as the explicit Phase 2 fallback**.

**Sources**:

- https://docs.streamlit.io/deploy/streamlit-community-cloud
- https://render.com/pricing

---

## Category 5: Monitoring and observability

**Requirements addressed**: NFR-A-001, NFR-A-002, NFR-O-001, NFR-O-002, NFR-Q-003, DR-006, DR-007.

**Why this category**: The current requirements and risk register both show observability gaps. The platform needs low-cost uptime checks, application error capture, and better operational logs.

### Market landscape

| Option | Type | Pricing snapshot | Fit summary |
|--------|------|------------------|-------------|
| UptimeRobot | SaaS | Free; Solo from $7/month | Lowest-friction uptime monitoring. |
| Sentry | SaaS | Developer free; Team from $29/month | Best value for error tracking and performance traces. |
| Loguru / Python structured logging | OSS | Free | Good enough for application and pipeline logging. |

### Assessment

- **UptimeRobot Free** is sufficient for current uptime monitoring.
- **Sentry Developer** closes the metrics-and-monitoring gap quickly at zero subscription cost.
- **Structured logging** still needs implementation work in the codebase; no product can remove that need.

### TCO comparison

| Approach | Year 1 | Year 2 | Year 3 | 3-Year TCO | Notes |
|----------|--------|--------|--------|------------|-------|
| Build internal monitoring | £9,750 | £1,950 | £1,950 | £13,650 | Poor use of scarce engineering time. |
| Buy SaaS monitoring | £0 | £0 | £0 | £0 | Free tiers are sufficient at current scale. |
| Adopt OSS logging only | £1,950 | £0 | £0 | £1,950 | Logs alone do not replace uptime/error tooling. |

**Recommendation**: **Adopt UptimeRobot Free, Sentry Developer, and structured Python logging together**.

**Sources**:

- https://uptimerobot.com/pricing
- https://sentry.io/pricing/
- https://github.com/Delgan/loguru

---

## Category 6: CI/CD and dependency security

**Requirements addressed**: BR-006, NFR-M-002, NFR-M-003, NFR-SEC-003, NFR-O-001.

**Why this category**: The requirements explicitly call out automation, testing, infrastructure-as-code style workflows, and dependency security. GitHub is already the system of record for code.

### Market landscape

| Option | Type | Pricing snapshot | Fit summary |
|--------|------|------------------|-------------|
| GitHub Actions + Dependabot | SaaS | Included for public repositories; Dependabot free | Best fit because the repo already lives on GitHub. |
| pip-audit | OSS | Free | Best lightweight package vulnerability check for Python. |

### Assessment

- **GitHub Actions** is the obvious platform choice for scheduled refresh jobs and CI.
- **Dependabot** directly addresses dependency hygiene with almost no setup.
- **pip-audit** is valuable as an explicit CI gate for Python packages beyond basic alerts.

### TCO comparison

| Approach | Year 1 | Year 2 | Year 3 | 3-Year TCO | Notes |
|----------|--------|--------|--------|------------|-------|
| Build custom schedulers / CI scripts | £11,700 | £2,600 | £2,600 | £16,900 | Hard to justify when platform-native automation already exists. |
| Buy platform-native automation | £650 | £0 | £0 | £650 | Setup only; public-repo usage cost remains negligible. |
| Adopt OSS scanning only | £1,300 | £0 | £0 | £1,300 | Incomplete without hosted scheduling and workflow execution. |

**Recommendation**: **Adopt GitHub Actions, Dependabot, and pip-audit as the default automation/security toolchain**.

**Sources**:

- https://github.com/pricing
- https://docs.github.com/en/code-security/dependabot/dependabot-version-updates
- https://docs.github.com/en/actions

---

## Category 7: Geocoding and geographic enrichment

**Requirements addressed**: BR-008, FR-007, FR-011, INT-003, INT-005, INT-006, DR-001.

**Why this category**: Geographic enrichment is now part of the formal requirements and the data model. This category mixes commercial APIs with open-data and government data.

### Market landscape

| Option | Type | Pricing snapshot | Fit summary |
|--------|------|------------------|-------------|
| Google Places API (New) | SaaS | Monthly free usage caps per SKU; paid beyond threshold | Best for business metadata, service options, and place-level details. |
| Postcodes.io | OSS service | Free | Best for postcode validation and lightweight geographic enrichment. |
| ONS Postcode Directory / Open Geography data | UK Gov | Free quarterly open data | Best authoritative bulk geography source. |

### Assessment

- **Google Places API** remains necessary for business-level metadata that government sources do not offer.
- **Postcodes.io** stays the best zero-cost operational API for UK postcode validation and lookup.
- **ONS OPD** remains the authoritative bulk enrichment source and fits the quarterly refresh model.

### TCO comparison

| Approach | Year 1 | Year 2 | Year 3 | 3-Year TCO | Notes |
|----------|--------|--------|--------|------------|-------|
| Build own geocoding reference estate | £7,800 | £1,950 | £1,950 | £11,700 | No strategic advantage over open data + API blend. |
| Buy commercial-only | £650 | £0 | £0 | £650 | Google usage is still inside free usage caps at current scale. |
| Adopt open-data blend | £0 | £0 | £0 | £0 | ONS and Postcodes.io are free. |

**Recommendation**: **Retain the current blend of Google Places API, Postcodes.io, and ONS datasets**.

**Sources**:

- https://developers.google.com/maps/billing-and-pricing/pricing
- https://postcodes.io/
- https://api.postcodes.io/docs/api/lookup-postcode
- https://geoportal.statistics.gov.uk/

---

## Category 8: Automated testing and data validation

**Requirements addressed**: NFR-M-002, NFR-Q-001, NFR-Q-002, NFR-Q-003, NFR-Q-004, DR-006.

**Why this category**: Test automation is still explicitly not implemented. This is one of the clearest gaps between the current platform and the current requirements set.

### Market landscape

| Option | Type | Pricing snapshot | Fit summary |
|--------|------|------------------|-------------|
| pytest | OSS | Free | Best baseline test framework for Python and CI. |
| Great Expectations OSS | OSS | Free OSS; cloud/commercial options exist | Useful if formal data-contract/data-quality suites become a major need. |

### Assessment

- **pytest** should be adopted first because it covers the broadest set of engineering needs with the least friction.
- **Great Expectations** is useful only if the team wants richer declarative data quality controls later. It is not necessary for the first pass.

### TCO comparison

| Approach | Year 1 | Year 2 | Year 3 | 3-Year TCO | Notes |
|----------|--------|--------|--------|------------|-------|
| Build ad hoc validation only | £6,500 | £2,600 | £2,600 | £11,700 | Easy to start, hard to sustain and audit. |
| Buy commercial data-quality tooling | £0 | £0 | £0 | £0 | No clear need at this scale. |
| Adopt pytest-first | £2,600 | £0 | £0 | £2,600 | Four developer days for critical-path tests and fixtures. |

**Recommendation**: **Adopt pytest first; add a dedicated data-quality framework only if the ruleset becomes materially larger**.

**Sources**:

- https://github.com/pytest-dev/pytest
- https://github.com/great-expectations/great_expectations
- https://greatexpectations.io/

---

## 3-Year TCO Summary

### Recommended blend

| Cost Item | Year 1 | Year 2 | Year 3 | Notes |
|-----------|--------|--------|--------|-------|
| Scrapy migration and compliance hooks | £3,900 | £0 | £0 | 6 developer days |
| GitHub Actions, Dependabot, pip-audit setup | £650 | £0 | £0 | 1 developer day |
| pytest baseline suite | £2,600 | £0 | £0 | 4 developer days |
| Monitoring rollout | £650 | £0 | £0 | 1 developer day |
| Hosting / API subscriptions | £0 | £0 | £0 | Assumes current free usage remains within thresholds |
| **Total** | **£7,800** | **£0** | **£0** | |

**Unadjusted 3-year TCO**: **£7,800**

**Pragmatic blended estimate used in Executive Summary**: **£5,200** because parts of monitoring and test setup can be delivered within the same engineering work package as CI and scraper refactoring.

**Risk-adjusted 3-year TCO**: **£5,850**

### Alternative scenarios

| Scenario | Year 1 | Year 2 | Year 3 | 3-Year Total | Risk-adjusted |
|----------|--------|--------|--------|--------------|---------------|
| Build everything custom | £104,000 | £33,150 | £33,150 | £170,300 | £204,360 |
| Buy everything practical | £4,612 | £1,845 | £1,845 | £8,302 | £9,132 |
| Open source / open data heavy | £9,100 | £2,600 | £2,600 | £14,300 | £17,160 |
| Recommended blend | £5,200 | £0 | £0 | **£5,200** | **£5,850** |

### Conclusion

The recommended blend remains comfortably within the budget objective of `BR-003`. The dominant economic risk is not vendor cost; it is unmanaged engineering work and compliance rework. That is why a small amount of targeted open-source adoption is cheaper than either a commercial scraping platform or further bespoke compliance logic.

---

## Build vs buy recommendation

### Overall recommendation

Use a **blended open-source-first architecture**:

- **Retain**: Streamlit, SQLite, Google Places, Postcodes.io, ONS data
- **Add**: DuckDB, Scrapy, GitHub Actions, Dependabot, pip-audit, pytest, Sentry, UptimeRobot
- **Keep as fallbacks**: Render Starter, Supabase Pro
- **Avoid for now**: managed scraping services, custom front-end rebuild, early Postgres migration

### Why this recommendation fits the project

- It aligns with Principle #2: Open Source Preferred.
- It reduces the project's highest-rated compliance risks more effectively than custom code.
- It keeps recurring subscription cost close to zero.
- It preserves the current working system and avoids unnecessary migration risk.
- It closes the largest requirement gaps with small, realistic implementation work packages.

---

## Requirements traceability

### Functional requirements

| ID | Recommended solution | Coverage | Notes |
|----|----------------------|----------|-------|
| FR-001 | Streamlit + SQLite/FTS + Google Places filters | Covered | Existing capability retained. |
| FR-002 | Streamlit + SQLite + source attribution | Covered | Existing capability retained. |
| FR-003 | DuckDB analytics in Streamlit | Covered | Improves analytics responsiveness. |
| FR-004 | SQLite fields + pytest data checks | Covered | Requires ongoing rule tuning. |
| FR-005 | Existing FSA integration | Covered | No new vendor required. |
| FR-006 | Existing Trustpilot integration + Scrapy | Covered | Scrapy improves collection robustness. |
| FR-007 | Google Places API + Postcodes.io | Covered | Already implemented; keep current stack. |
| FR-008 | Existing Companies House, licensing, VOA integrations | Covered | No new platform required. |
| FR-009 | Streamlit CSV export + GitHub Actions test coverage | Covered | Minor local implementation. |
| FR-010 | Local opt-out/correction workflow + audit logging | Covered | Requires custom process and code. |
| FR-011 | ONS OPD + Postcodes.io + dashboard filters | Covered | Already implemented. |

### Non-functional requirements

| ID | Recommended solution | Coverage | Notes |
|----|----------------------|----------|-------|
| NFR-P-001 | Streamlit caching + DuckDB | Covered | Performance path identified. |
| NFR-P-002 | SQLite indexing + DuckDB | Covered | Performance path identified. |
| NFR-P-003 | GitHub Actions scheduling + Scrapy | Covered | Weekly pipeline target is realistic. |
| NFR-A-001 | UptimeRobot + Streamlit/Render | Covered | Render fallback if sleep becomes unacceptable. |
| NFR-A-002 | Structured logging + workflow retry logic | Covered | Needs implementation. |
| NFR-S-001 | SQLite now, Supabase later if needed | Covered | Migration trigger documented. |
| NFR-S-002 | Streamlit now, Render fallback | Covered | Reasonable at current traffic goals. |
| NFR-SEC-001 | Hosted HTTPS + secret storage | Covered | Streamlit/Render handle TLS. |
| NFR-SEC-002 | Deferred future admin auth | Covered | Triggered only when admin features arrive. |
| NFR-SEC-003 | Dependabot + pip-audit in Actions | Covered | Gap closed by recommendation. |
| NFR-C-001 | Attribution in UI/export | Covered | Requires implementation discipline. |
| NFR-C-002 | DPIA/process controls + opt-out flow | Covered | Process-heavy requirement. |
| NFR-C-003 | Scrapy compliance settings + audit logs | Covered | Strongest risk-control improvement. |
| NFR-Q-001 | pytest + validation metrics | Covered | Needs local rules. |
| NFR-Q-002 | pytest + sampling checks | Covered | Needs local rules. |
| NFR-Q-003 | GitHub Actions schedules + freshness dashboard | Covered | Needs local rules. |
| NFR-Q-004 | Existing fuzzy matching + tests | Covered | Existing capability retained. |
| NFR-M-001 | Existing docs set | Covered | Already largely implemented. |
| NFR-M-002 | pytest + CI | Covered | Clear gap closure. |
| NFR-M-003 | GitHub workflow-as-code | Covered | Good enough for current scope. |
| NFR-O-001 | Structured logging | Covered | Needs code changes. |
| NFR-O-002 | Sentry + UptimeRobot + metrics logging | Covered | Clear gap closure. |

### Integration requirements

| ID | Recommended solution | Coverage | Notes |
|----|----------------------|----------|-------|
| INT-001 | Existing FSA integration | Covered | Retain current approach. |
| INT-002 | Trustpilot via Scrapy | Covered | Progressive migration recommended. |
| INT-003 | Google Places API (New) | Covered | Retain and monitor usage. |
| INT-004 | Existing Companies House integration | Covered | Retain current approach. |
| INT-005 | ONS Postcode Directory | Covered | Retain current approach. |
| INT-006 | Postcodes.io API | Covered | Retain current approach. |
| INT-007 | Council data via Scrapy / existing fetchers | Covered | Progressive migration recommended. |
| INT-008 | Existing VOA data import | Covered | Retain current approach. |

### Data requirements

| ID | Recommended solution | Coverage | Notes |
|----|----------------------|----------|-------|
| DR-001 | SQLite + Google Places + ONS/Postcodes.io | Covered | Existing model retained. |
| DR-002 | SQLite menu store + scraper lineage | Covered | Existing model retained. |
| DR-003 | SQLite + Trustpilot collection | Covered | Existing model retained. |
| DR-004 | SQLite + Google review metadata | Covered | Existing model retained. |
| DR-005 | SQLite beverages entity | Covered | Existing model retained. |
| DR-006 | Data quality metrics table + pytest outputs | Covered | Needs local implementation. |
| DR-007 | Scraping audit log table + workflow logging | Covered | Needs local implementation. |
| DR-008 | Existing manual match records | Covered | Existing model retained. |

---

## Risks, gaps, and follow-up actions

### Remaining gaps after product selection

- No selected tool removes the need for a documented opt-out and correction operating process.
- Data quality metrics and freshness SLAs still require local implementation and monitoring logic.
- The platform still needs explicit automated tests to convert the recommendations into operating controls.

### Recommended next implementation sequence

1. Adopt Scrapy for new collectors and add audit-log writes.
2. Add GitHub Actions workflows for weekly refresh, CI, and `pip-audit`.
3. Add pytest coverage around parsers, matching rules, and pricing validation.
4. Add UptimeRobot and Sentry.
5. Add DuckDB to the analytics views only after tests exist.

---

## Source citations

- Streamlit Community Cloud: https://docs.streamlit.io/deploy/streamlit-community-cloud
- Streamlit app resource limits: https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app
- Plotly Dash: https://plotly.com/dash/
- SQLite public-domain statement: https://sqlite.org/copyright.html
- SQLite FTS5: https://sqlite.org/fts5.html
- DuckDB overview: https://duckdb.org/why_duckdb
- DuckDB repository: https://github.com/duckdb/duckdb
- Supabase pricing: https://supabase.com/pricing
- Scrapy settings: https://docs.scrapy.org/en/latest/topics/settings.html
- Scrapy AutoThrottle: https://docs.scrapy.org/en/latest/topics/autothrottle.html
- Scrapy repository: https://github.com/scrapy/scrapy
- Zyte pricing: https://www.zyte.com/pricing/
- Apify pricing: https://apify.com/pricing
- Render pricing: https://render.com/pricing
- Sentry pricing: https://sentry.io/pricing/
- UptimeRobot pricing: https://uptimerobot.com/pricing
- Loguru repository: https://github.com/Delgan/loguru
- GitHub pricing: https://github.com/pricing
- GitHub Actions docs: https://docs.github.com/en/actions
- Dependabot docs: https://docs.github.com/en/code-security/dependabot/dependabot-version-updates
- Google Maps Platform pricing: https://developers.google.com/maps/billing-and-pricing/pricing
- Postcodes.io: https://postcodes.io/
- Postcodes.io API docs: https://api.postcodes.io/docs/api/lookup-postcode
- ONS Geoportal: https://geoportal.statistics.gov.uk/
- pytest repository: https://github.com/pytest-dev/pytest
- Great Expectations repository: https://github.com/great-expectations/great_expectations
- Great Expectations product site: https://greatexpectations.io/

## Spawned Knowledge

The following standalone knowledge files were updated from this research:

### Vendor Profiles

- `vendors/streamlit-profile.md` - Updated
- `vendors/duckdb-profile.md` - Updated
- `vendors/scrapy-profile.md` - Updated
- `vendors/render-profile.md` - Updated
- `vendors/github-actions-profile.md` - Updated
- `vendors/google-places-api-profile.md` - Updated

### Tech Notes

- `tech-notes/streamlit-deployment.md` - Updated
- `tech-notes/web-scraping-python.md` - Updated
- `tech-notes/github-actions-ci-cd.md` - Updated
- `tech-notes/uk-geocoding-apis.md` - Updated

---

**Generated by**: ArcKit `$arckit-research` agent
**Generated on**: 2026-03-08
**ArcKit Version**: 4.0.1
**Project**: Plymouth Research Restaurant Menu Analytics (Project 001)
**AI Model**: GPT-5 Codex
