# Risk Register: Plymouth Research Restaurant Menu Analytics

## Document Information

| Field | Value |
|-------|-------|
| **Document ID** | ARC-001-RISK-v1.0 |
| **Project** | Plymouth Research Restaurant Menu Analytics (Project 001) |
| **Document Type** | Risk Register (HM Treasury Orange Book Framework) |
| **Classification** | OFFICIAL |
| **Version** | 1.0 |
| **Status** | DRAFT |
| **Date** | 2025-11-17 |
| **Owner** | Research Director, Plymouth Research |
| **Risk Register Owner** | Research Director |
| **Next Review Date** | 2025-12-17 |

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-11-17 | ArcKit AI | Initial creation from `/arckit.risk` command |

---

## Executive Summary

### Risk Profile Overview

This risk register identifies and assesses **20 risks** across the Plymouth Research Restaurant Menu Analytics platform following HM Treasury Orange Book (2023) risk management principles. All risks have been assigned owners from the stakeholder RACI matrix and assessed using the 5×5 Likelihood × Impact methodology.

**Risk Distribution by Category**:
- **COMPLIANCE/REGULATORY**: 5 risks (25%) - Highest priority due to legal/ethical non-negotiables
- **TECHNOLOGY**: 4 risks (20%) - Web scraping complexity and infrastructure challenges
- **OPERATIONAL**: 4 risks (20%) - Resource constraints and maintenance burden
- **FINANCIAL**: 3 risks (15%) - Budget overruns and cost sustainability
- **REPUTATIONAL**: 2 risks (10%) - Data quality errors and service failures
- **STRATEGIC**: 2 risks (10%) - Market adoption and competitor threats

**Risk Scores (Residual - After Controls)**:
- **Critical (20-25)**: 2 risks - Require immediate escalation
- **High (13-19)**: 6 risks - Active management required
- **Medium (6-12)**: 9 risks - Monitor and treat
- **Low (1-5)**: 3 risks - Tolerate

**Overall Risk Assessment**: **CONCERNING**

The project faces 2 **Critical risks** that require immediate attention:
1. **R-001: GDPR/Legal Non-Compliance** (Critical 20) - Robots.txt violations, GDPR breaches
2. **R-003: Data Quality Failures** (Critical 20) - Inaccurate menu data damaging credibility

Additionally, **6 High risks** demand active management, particularly around web scraping sustainability (R-002), budget overruns (R-005), and technical implementation challenges (R-008, R-010).

**Inherent vs. Residual Risk**:
- **Total Inherent Risk Score**: 455/500 (before controls)
- **Total Residual Risk Score**: 232/500 (after controls)
- **Risk Reduction**: 49% through planned controls and mitigations

**Risks Requiring Immediate Escalation**: 8 risks (R-001, R-002, R-003, R-004, R-005, R-008, R-010, R-012)

### Key Actions Required

**Immediate (Week 1-2)**:
1. **Legal Review**: Engage Legal/Compliance Advisor to validate robots.txt compliance approach (R-001)
2. **DPIA Initiation**: Begin Data Protection Impact Assessment for GDPR compliance (R-001, R-004)
3. **Technical Feasibility**: Pilot scraping on 10 diverse restaurant websites to validate feasibility (R-002, R-008)
4. **Budget Validation**: Confirm £100/month budget is adequate with contingency planning (R-005)

**Short-term (Month 1-3)**:
5. **Pilot Phase**: Scrape 30 restaurants to measure data quality accuracy baseline (R-003)
6. **Infrastructure Setup**: Implement rate limiting and monitoring controls (R-002, R-010)
7. **Documentation**: Create runbooks for scraper failures and opt-out processing (R-011, R-013)

**Medium-term (Month 4-6)**:
8. **Launch Readiness**: User testing with Research Analysts before public launch (R-012)
9. **Performance Optimization**: Achieve <500ms search response time target (R-010)
10. **Marketing**: Soft launch to Plymouth food community (R-015)

### Orange Book Compliance

This risk register demonstrates compliance with HM Treasury Orange Book 2023:

- ✅ **Governance and Leadership**: Risk owners assigned from RACI matrix (Research Director, Data Engineer, Operations/IT, Legal Advisor)
- ✅ **Integration**: Risks linked to stakeholder goals (G-1 to G-8), outcomes (O-1 to O-4), and business case
- ✅ **Collaboration**: Risks sourced from stakeholder concerns (SD-1 to SD-10) and cross-functional expert judgment
- ✅ **Risk Processes**: Systematic identification (6 categories), assessment (5×5 matrix), response (4Ts framework), monitoring (monthly reviews)
- ✅ **Continual Improvement**: Review framework, action plans, and quarterly risk appetite reassessment

---

## Risk Matrix Visualization

### Inherent Risk Matrix (Before Controls)

```
LIKELIHOOD ↑
       5 | R-01 | R-02 | R-03 |      | R-05 |  ← Almost Certain
       4 |      | R-08 | R-12 | R-15 |      |  ← Likely
       3 | R-04 | R-06 | R-10 | R-13 | R-14 |  ← Possible
       2 | R-07 | R-09 | R-11 | R-17 | R-19 |  ← Unlikely
       1 | R-16 | R-18 | R-20 |      |      |  ← Rare
         +----------------------------------→
           1     2     3     4     5
                IMPACT →

Color Coding:
■ Critical (20-25): R-01, R-02, R-03, R-05
■ High (13-19): R-04, R-08, R-10, R-12, R-13, R-14, R-15
■ Medium (6-12): R-06, R-07, R-09, R-11, R-17, R-19
■ Low (1-5): R-16, R-18, R-20
```

### Residual Risk Matrix (After Controls)

```
LIKELIHOOD ↑
       5 |      |      | R-01 |      |      |  ← Almost Certain
       4 |      |      | R-03 |      |      |  ← Likely
       3 |      | R-02 | R-04 | R-08 | R-10 |  ← Possible
       2 | R-06 | R-12 | R-05 | R-13 | R-15 |  ← Unlikely
       1 | R-07 | R-09 | R-11 | R-14 | R-16 |  ← Rare
         | R-17 | R-18 | R-19 | R-20 |      |
         +----------------------------------→
           1     2     3     4     5
                IMPACT →

Color Coding:
■ Critical (20-25): R-01 (20), R-03 (20)
■ High (13-19): R-02 (16), R-04 (15), R-05 (14), R-08 (15), R-10 (15), R-12 (13)
■ Medium (6-12): R-06 (8), R-11 (9), R-13 (10), R-14 (8), R-15 (10), R-16 (8), R-17 (6), R-18 (6), R-19 (9)
■ Low (1-5): R-07 (4), R-09 (4), R-20 (4)
```

**Risk Movement Analysis**:
- **R-001**: Critical 25 → Critical 20 (controls reduce likelihood but impact remains catastrophic)
- **R-002**: Critical 25 → High 16 (technical feasibility pilot + robots.txt compliance infrastructure reduces likelihood)
- **R-003**: Critical 25 → Critical 20 (validation processes reduce likelihood but reputational impact remains severe)
- **R-005**: Critical 25 → High 14 (managed services + cost monitoring reduce likelihood and impact)
- **R-008**: High 16 → High 15 (pilot testing provides early warning)
- **R-010**: High 15 → High 15 (indexing helps but performance remains challenging)

**Top Movers** (Greatest Risk Reduction):
1. **R-005** (Financial): 25 → 14 (44% reduction) - Managed services + Wardley Map cost analysis effective
2. **R-002** (Technology): 25 → 16 (36% reduction) - Technical feasibility pilot validates approach
3. **R-012** (Operational): 16 → 13 (19% reduction) - User testing pre-launch mitigates adoption risk

---

## Top 10 Risks (Ranked by Residual Score)

| Rank | ID | Title | Category | Inherent | Residual | Owner | Status | Response |
|------|-----|-------|----------|----------|----------|-------|--------|----------|
| 1 | R-001 | GDPR/Legal Non-Compliance | COMPLIANCE | 25 | **20** | Research Director | Open | Treat |
| 2 | R-003 | Data Quality Failures Damage Credibility | REPUTATIONAL | 25 | **20** | Data Engineer | Open | Treat |
| 3 | R-002 | Web Scraping Technically Infeasible | TECHNOLOGY | 25 | **16** | Data Engineer | Open | Treat |
| 4 | R-004 | Robots.txt Violations Trigger Legal Action | COMPLIANCE | 20 | **15** | Data Engineer | Open | Treat |
| 5 | R-008 | Restaurant Websites Too Complex to Scrape | TECHNOLOGY | 16 | **15** | Data Engineer | Open | Treat |
| 6 | R-010 | Performance Requirements Not Met | TECHNOLOGY | 15 | **15** | Data Engineer | Open | Treat |
| 7 | R-005 | Cloud Costs Exceed £100/Month Budget | FINANCIAL | 25 | **14** | Operations/IT | Open | Treat |
| 8 | R-012 | User Adoption Below Target (Market Risk) | STRATEGIC | 16 | **13** | Research Director | Open | Treat |
| 9 | R-013 | Opt-Out Requests Exceed 20% (Coverage Risk) | OPERATIONAL | 12 | **10** | Research Director | Open | Treat |
| 10 | R-015 | Competitor Launches Similar Platform First | STRATEGIC | 16 | **10** | Research Director | Open | Tolerate |

---

## Full Risk Register

### COMPLIANCE/REGULATORY Risks

#### R-001: GDPR/Legal Non-Compliance (CRITICAL)

**Category**: COMPLIANCE/REGULATORY

**Risk Title**: Web scraping activities violate UK GDPR, Computer Misuse Act 1990, or Copyright Act leading to ICO fines, legal action, or platform shutdown

**Risk Description**:
Platform inadvertently collects personal data (PII), violates robots.txt directives, or scrapes copyrighted creative content beyond factual menu data. This triggers ICO investigation (GDPR Article 58), legal complaints from restaurants under Computer Misuse Act 1990, or cease-and-desist letters citing copyright infringement. Worst case: ICO fine up to £17.5M or 4% turnover, legal costs defending lawsuits, injunction forcing platform shutdown.

**Root Cause**:
- Legal grey area around web scraping in UK law
- No explicit authorization from restaurants to scrape their websites
- Complexity of distinguishing factual data (prices, menu items) from creative content (descriptions, photography)
- GDPR applies even to small research organizations with limited compliance resources

**Trigger Events**:
- Restaurant complaint to ICO about unauthorized data processing
- Legal firm sends cease-and-desist letter on behalf of restaurant group
- Scraper inadvertently collects PII (customer reviews containing names/emails)
- Media coverage attracting regulatory scrutiny
- Robots.txt violation logged and discovered during audit

**Consequences if Realized**:
- **Financial**: ICO fine £10K-£17.5M (catastrophic for small firm), legal defense costs £50K-£250K
- **Operational**: Platform shutdown by court injunction, 6-12 month suspension while resolving
- **Reputational**: Research Director's career damaged, organizational reputation destroyed, loss of future funding/clients
- **Strategic**: Project terminated, stakeholder goals (O-1, O-2) completely unachieved

**Affected Stakeholders**:
- Research Director (SD-2: Minimize Legal Risk - CRITICAL driver)
- Legal/Compliance Advisor (SD-8: Mitigate Legal Exposure)
- ICO (SD-9: Data Protection Compliance)
- Restaurant Owners (SD-6: Accurate Representation - may complain if feel violated)

**Related Objectives**: Goal G-3 (100% Ethical Compliance), Goal G-8 (DPIA Completion), Outcome O-2 (Zero Legal Violations)

**Inherent Risk Assessment**:
- **Inherent Likelihood**: 5 (Almost Certain) - Legal grey area, no explicit authorization, high complexity
- **Inherent Impact**: 5 (Catastrophic) - Organization-ending financial/reputational consequences
- **Inherent Risk Score**: **25 (CRITICAL)**

**Current Controls and Mitigations**:
- **Existing Controls**:
  1. Scrapy `ROBOTSTXT_OBEY = True` setting (Wardley Map, research-findings.md)
  2. 5-second rate limiting per domain (requirements.md NFR-C-002)
  3. User-Agent transparency identifying Plymouth Research with contact email (NFR-C-004)
  4. Opt-out form planned with 48-hour SLA (FR-015, NFR-C-005)
  5. Source attribution linking back to restaurant website (FR-005)
- **Control Effectiveness**: **Adequate** (planned controls are comprehensive but not yet implemented/validated)
- **Control Owners**: Data Engineer (technical controls), Legal/Compliance Advisor (DPIA, policy review)
- **Evidence of Effectiveness**: Not yet measured (pre-launch) - will be validated through monthly compliance audits

**Residual Risk Assessment**:
- **Residual Likelihood**: 4 (Likely) - Controls reduce but don't eliminate risk (legal grey area persists)
- **Residual Impact**: 5 (Catastrophic) - Impact unchanged if risk materializes
- **Residual Risk Score**: **20 (CRITICAL)**

**Risk Response**: **TREAT**

**Rationale for Response**:
Risk exceeds all acceptable thresholds. Cannot Tolerate (catastrophic impact), cannot Transfer (no insurance covers this fully), cannot Terminate (would abandon entire project). Must Treat through comprehensive legal review, DPIA, and defensive compliance controls.

**Risk Ownership**:
- **Risk Owner**: Research Director (Accountable for all legal/compliance decisions per RACI)
- **Action Owner**: Legal/Compliance Advisor (Responsible for DPIA, legal review)
- **Escalation Path**: Research Director → External Legal Counsel (if complaints arise)

**Action Plan**:

**Additional Mitigations Needed**:
1. **DPIA Completion**: Engage Legal/Compliance Advisor to complete Data Protection Impact Assessment before any scraping begins (Month 1, Week 1)
2. **Legal Opinion**: Obtain written legal opinion from solicitor specializing in internet law confirming scraping approach is legally defensible (Month 1, Week 2)
3. **PII Detection**: Implement automated regex scanning for PII (emails, phone numbers, names) in scraped content with flagging for manual review (Month 1, Week 3)
4. **Exclusion List**: Maintain permanent exclusion list of opted-out restaurants checked before every scrape (Month 1, Week 4)
5. **Compliance Audits**: Monthly audit by Legal Advisor sampling 50 scraping logs to verify 100% robots.txt compliance, rate limiting, User-Agent transparency (Ongoing from Month 2)
6. **Privacy Policy**: Publish privacy policy explaining data collection, use, retention (12 months), and data subject rights (Month 1, Week 2)
7. **Terms of Service**: Add ToS to dashboard clarifying data is provided "as-is" from restaurant sources, not guaranteed accurate (liability limitation) (Month 3, pre-launch)

**Specific Actions**:
| Action | Owner | Due Date | Success Criteria | Status |
|--------|-------|----------|------------------|--------|
| Engage Legal Advisor for DPIA | Research Director | 2025-11-24 | DPIA initiated, scope agreed | Not Started |
| Obtain legal opinion on scraping approach | Legal Advisor | 2025-12-01 | Written opinion confirming defensibility | Not Started |
| Implement PII detection regex scanner | Data Engineer | 2025-12-08 | Automated scan detects test PII samples (100% accuracy) | Not Started |
| Create and test opt-out exclusion list | Data Engineer | 2025-12-15 | Scraper skips URLs on exclusion list (validated) | Not Started |
| Publish privacy policy on website footer | Research Director | 2025-12-01 | Privacy policy live, GDPR-compliant language | Not Started |
| First compliance audit (50 logs sampled) | Legal Advisor | 2026-02-01 | 100% compliance confirmed in audit report | Not Started |

**Target Residual Risk**: 12 (Medium) - After DPIA approval and 3 months of clean compliance audits
**Target Date**: 2026-02-28 (Month 4)

**Success Criteria**:
- DPIA completed and approved with no critical issues identified
- Legal opinion confirms approach is legally defensible
- First 3 compliance audits show 100% robots.txt compliance, zero PII detected
- Zero complaints or legal inquiries received in first 6 months post-launch

**Risk Status**: **OPEN** (Not yet addressed, requires immediate action)

---

#### R-002: Web Scraping Technically Infeasible (HIGH)

**Category**: TECHNOLOGY

**Risk Title**: Restaurant websites prove too complex/diverse to scrape reliably, preventing achievement of 150+ restaurant coverage goal

**Risk Description**:
Plymouth's 150 restaurants use highly diverse website technologies (WordPress, Squarespace, Wix, custom CMS, JavaScript-heavy SPAs, PDF menus, Google Docs). Many require JavaScript rendering (Selenium/Playwright), others have anti-scraping measures (Cloudflare, rate limiting, CAPTCHA). Extraction logic becomes unmanageably complex with 150 different HTML structures. Scraping success rate falls below 60%, making comprehensive coverage infeasible.

**Root Cause**:
- No industry standard for restaurant menu markup (unlike microdata for e-commerce)
- Small independent restaurants use template platforms (Wix, Squarespace) with dynamic JavaScript rendering
- Menu data often in PDFs, images, or embedded Google Docs (not HTML tables)
- Anti-scraping measures increasingly common (bot protection, Cloudflare)

**Trigger Events**:
- Pilot scraping of 30 restaurants shows <70% success rate
- Key cuisine type (Chinese restaurants) predominantly use PDF menus (not parsable with BeautifulSoup)
- Major restaurant group uses Cloudflare bot protection blocking scraper IP
- JavaScript-heavy sites require Selenium, making scraping 10× slower (violates 5-second rate limit at scale)

**Consequences if Realized**:
- **Coverage**: Only 60-90 restaurants scraped (vs 150 target), failing Goal G-2
- **Data Quality**: Missing cuisines (Chinese, Indian) bias dataset toward British/Italian
- **User Value**: Consumers searching for specific cuisines find limited results, reducing adoption
- **Strategic**: Platform perceived as incomplete, damaging authority goal (Outcome O-1)
- **Financial**: Manual data entry fallback costs £20/restaurant/month = £1,800/month (18× budget), unsustainable

**Affected Stakeholders**:
- Data Engineer (SD-3: Maintainable Technical Solution - complexity threatens this)
- Research Director (SD-1: Establish Authority - incomplete coverage undermines this)
- Plymouth Consumers (SD-5: Find Restaurants by Dietary Needs - missing restaurants = unmet needs)
- Research Analysts (SD-4: Access Reliable Data - biased dataset limits research value)

**Related Objectives**: Goal G-2 (150+ Restaurants), Outcome O-1 (Authority), Outcome O-3 (Operational Sustainability)

**Inherent Risk Assessment**:
- **Inherent Likelihood**: 5 (Almost Certain) - Website diversity is known upfront, no industry standards
- **Inherent Impact**: 5 (Catastrophic) - Project fails to achieve core value proposition (comprehensive coverage)
- **Inherent Risk Score**: **25 (CRITICAL)**

**Current Controls and Mitigations**:
- **Existing Controls**:
  1. Scrapy framework selected for flexibility and JavaScript rendering support (research-findings.md)
  2. Selenium/Playwright available for dynamic sites (requirements.md assumptions)
  3. Pilot phase (30 restaurants) planned to validate approach before full rollout (backlog.md Sprint 2)
  4. Manual fallback acknowledged for "difficult sites" (requirements.md FR-011 assumptions)
- **Control Effectiveness**: **Weak** (controls are contingency plans, not preventive)
- **Control Owners**: Data Engineer (scraper development, extraction logic)
- **Evidence of Effectiveness**: Not yet measured - pilot phase (Month 1-2) will provide first evidence

**Residual Risk Assessment**:
- **Residual Likelihood**: 4 (Likely) - Pilot may reveal issues but website diversity persists
- **Residual Impact**: 4 (Major) - Can achieve 100-120 restaurants (not ideal but serviceable), manual fallback for critical sites
- **Residual Risk Score**: **16 (HIGH)**

**Risk Response**: **TREAT**

**Rationale for Response**:
Feasibility is fundamental to project viability. Must validate technical approach through pilot before committing to full build. If pilot fails, may need to pivot to narrower scope (50 major restaurants) or hybrid approach (scraping + manual curation).

**Risk Ownership**:
- **Risk Owner**: Data Engineer (Accountable for technical architecture per RACI)
- **Action Owner**: Data Engineer (Responsible for pilot scraping and feasibility validation)
- **Escalation Path**: Data Engineer → Research Director (if pilot shows <70% success rate requiring scope reduction)

**Action Plan**:

**Additional Mitigations Needed**:
1. **Diverse Pilot Sample**: Select 30 pilot restaurants representing diverse technologies (5 WordPress, 5 Squarespace, 5 Wix, 5 custom CMS, 5 PDF menus, 5 JS-heavy) (Month 1, Week 1)
2. **Feasibility Threshold**: Define success threshold: ≥80% scraping success rate required to proceed with 150-restaurant target (Month 1, Week 1)
3. **Extraction Framework**: Build modular extraction framework with site-specific adapters (WordPress adapter, Squarespace adapter, PDF parser) rather than monolithic scraper (Month 1, Week 2-4)
4. **Manual Fallback Budget**: Budget 10 hours/month Data Engineer time for manual extraction of high-value but difficult sites (Month 2+)
5. **OCR for PDFs**: Integrate Tesseract OCR or similar for PDF menu extraction (Month 2, if pilot shows >20% PDFs)
6. **Headless Browser Pool**: Set up Selenium Grid or Playwright cluster for JavaScript-heavy sites (Month 2, if pilot shows >30% require JS rendering)
7. **Success Rate Monitoring**: Track scraping success rate weekly, escalate if falls below 75% (Ongoing from Month 2)

**Specific Actions**:
| Action | Owner | Due Date | Success Criteria | Status |
|--------|-------|----------|------------------|--------|
| Compile diverse pilot sample (30 restaurants) | Data Engineer | 2025-11-24 | 30 restaurants selected representing 6 technology types | Not Started |
| Define feasibility threshold (80% success) | Data Engineer + Research Director | 2025-11-24 | Threshold agreed, escalation plan documented | Not Started |
| Build modular extraction framework | Data Engineer | 2025-12-15 | 6 site-type adapters (WordPress, Squarespace, etc.) functional | Not Started |
| Execute pilot scraping (30 restaurants) | Data Engineer | 2025-12-22 | All 30 sites attempted, success rate measured | Not Started |
| Pilot review meeting (Go/No-Go decision) | Data Engineer + Research Director | 2025-12-29 | Success rate ≥80% → Proceed; <70% → Scope reduction; 70-80% → Additional pilot | Not Started |
| Implement OCR for PDFs (if needed) | Data Engineer | 2026-01-31 | PDF menus extracted with >80% accuracy | Conditional |

**Target Residual Risk**: 9 (Medium) - After pilot validation showing ≥80% success rate
**Target Date**: 2025-12-31 (Month 2)

**Success Criteria**:
- Pilot shows ≥80% scraping success rate (24+ of 30 restaurants successfully scraped)
- All 6 major cuisine types represented in pilot (British, Italian, Chinese, Indian, Thai, Japanese)
- Manual fallback <20% of total restaurants (manageable effort within 10 hours/month)
- Extraction accuracy ≥85% (prices, item names correctly extracted in manual validation sample)

**Risk Status**: **OPEN** (Pilot scheduled for Month 1-2, awaiting execution)

---

#### R-003: Data Quality Failures Damage Credibility (CRITICAL)

**Category**: REPUTATIONAL

**Risk Title**: Inaccurate menu data (wrong prices, incorrect dietary tags, stale information) damages platform credibility and user trust, destroying authority goal

**Risk Description**:
Scraped menu data contains systematic errors: prices extracted incorrectly (£12.50 → £12), dietary tags misapplied (non-vegan items tagged vegan due to keyword "V" meaning Vegetarian), stale data showing menus from 3 months ago. Consumers find inaccurate information, complain on social media, leave negative feedback. Food journalists cite incorrect data in articles, then publicly retract. Restaurant owners demand removal after misrepresentation. Data quality score falls to 75% (vs 95% target), undermining Goal G-1.

**Root Cause**:
- Diverse website formats make extraction logic error-prone (£12 vs £12.50 vs £12.5)
- Dietary tag keyword matching is heuristic, not 100% accurate ("V" = Vegan OR Vegetarian?)
- Menus change weekly but scraper only runs weekly (7-day staleness window)
- No ground truth for validation (manual checking is only way to verify accuracy)
- Conservative tagging may still misclassify edge cases (gluten-free not guaranteed for celiacs)

**Trigger Events**:
- Consumer with gluten allergy trusts "gluten-free" tag, has allergic reaction, posts angry review
- Food journalist cites "average fish & chips price £15" but manual check shows £12 (calculation error), journalist retracts and criticizes platform
- Restaurant owner complains menu shows items from 6 months ago (stale data), threatens legal action for misrepresentation
- Social media post goes viral: "PlymouthResearch says [Restaurant X] has vegan options - I went and they don't!"

**Consequences if Realized**:
- **Reputational**: Platform labeled "unreliable" on social media, Research Director's credibility damaged
- **Strategic**: Authority goal (Outcome O-1) unachievable, media citations drop to zero
- **Safety**: Dietary tag errors create health risk for allergy sufferers (gluten, nut allergies)
- **Legal**: Restaurant complaints escalate to cease-and-desist if misrepresentation is severe
- **User Adoption**: Goal G-7 (1,000+ searches) unachievable due to trust deficit

**Affected Stakeholders**:
- Research Director (SD-1: Establish Authority - data quality is foundation)
- Plymouth Consumers (SD-5: Find Restaurants by Dietary Needs - inaccurate tags dangerous)
- Restaurant Owners (SD-6: Accurate Representation - misrepresentation triggers complaints)
- Research Analysts (SD-4: Access Reliable Data - low quality data undermines research value)
- Food Writers/Journalists (SD-7: Data-Driven Reporting - incorrect data damages their credibility too)

**Related Objectives**: Goal G-1 (95% Data Quality), Outcome O-1 (Authority), Outcome O-4 (User Satisfaction)

**Inherent Risk Assessment**:
- **Inherent Likelihood**: 5 (Almost Certain) - Data quality failures are expected in web scraping without robust validation
- **Inherent Impact**: 5 (Catastrophic) - Reputational damage is permanent, trust impossible to rebuild
- **Inherent Risk Score**: **25 (CRITICAL)**

**Current Controls and Mitigations**:
- **Existing Controls**:
  1. Conservative dietary tagging (only tag if explicitly labeled, don't infer) (requirements.md FR-007)
  2. Price normalization with outlier flagging (£0.50-£150 range, flag for review) (FR-006)
  3. Weekly automated refresh to minimize staleness (7 days max age) (FR-013)
  4. Manual validation sampling (100 items/month by Research Analyst) (Goal G-1 measurement method)
  5. User feedback "Report Error" mechanism planned (DR-007, backlog.md DS-007)
  6. Data quality monitoring dashboard with automated alerts if <90% (FR-014, backlog.md US-014)
- **Control Effectiveness**: **Adequate** (controls are comprehensive but rely on manual validation, not preventive)
- **Control Owners**: Data Engineer (extraction logic, validation rules), Research Analysts (manual validation)
- **Evidence of Effectiveness**: Not yet measured - will be validated through Month 1 pilot (30 restaurants)

**Residual Risk Assessment**:
- **Residual Likelihood**: 4 (Likely) - Controls reduce but don't eliminate extraction errors
- **Residual Impact**: 5 (Catastrophic) - Reputational damage remains severe even with controls
- **Residual Risk Score**: **20 (CRITICAL)**

**Risk Response**: **TREAT**

**Rationale for Response**:
Data quality is existential to credibility. Cannot Tolerate (catastrophic impact), cannot Transfer (no insurance for reputation), cannot Terminate (abandons project). Must Treat through rigorous validation, conservative defaults, and rapid error correction.

**Risk Ownership**:
- **Risk Owner**: Data Engineer (Accountable for database schema, extraction logic per RACI)
- **Action Owner**: Research Analysts (Responsible for manual validation sampling)
- **Escalation Path**: Data Engineer → Research Director (if data quality drops below 90% in monthly validation)

**Action Plan**:

**Additional Mitigations Needed**:
1. **Pilot Validation**: Manual validation of all 30 pilot restaurant menus to measure baseline accuracy (Month 1, Week 4)
2. **Accuracy Baseline**: Establish baseline accuracy from pilot (expect 75-80% initially), create improvement roadmap to 95% (Month 2, Week 1)
3. **Dietary Tag Disclaimer**: Add disclaimer to dashboard: "Dietary tags are based on restaurant labeling and may not reflect full ingredient lists. Always confirm with restaurant for allergies." (Month 3, pre-launch)
4. **Price Confidence Scoring**: Add confidence score to prices (HIGH = extracted cleanly, MEDIUM = required normalization, LOW = flagged as outlier) and hide LOW confidence prices (Month 2)
5. **Staleness Warnings**: Display "Last updated: X days ago" on all menu items, warn if >10 days old (FR-005) (Month 2)
6. **Rapid Error Correction**: SLA for user-reported errors: fix within 48 hours if confirmed valid (Month 4, post-launch)
7. **Crowdsourced Validation**: Allow users to upvote/downvote accuracy ("Is this menu current? Yes/No") to identify stale data (Month 6, Phase 2)

**Specific Actions**:
| Action | Owner | Due Date | Success Criteria | Status |
|--------|-------|----------|------------------|--------|
| Manual validation of 30 pilot menus | Research Analyst | 2025-12-29 | All 30 menus validated, accuracy % calculated | Not Started |
| Calculate baseline accuracy from pilot | Data Engineer | 2026-01-05 | Baseline accuracy measured (expect 75-85%), improvement plan documented | Not Started |
| Add dietary tag disclaimer to dashboard | Data Engineer | 2026-02-28 | Disclaimer visible on all menu pages, legal language approved | Not Started |
| Implement price confidence scoring | Data Engineer | 2026-01-31 | Prices tagged HIGH/MEDIUM/LOW, LOW hidden from display | Not Started |
| Add staleness warnings (>10 days) | Data Engineer | 2026-01-31 | "Data may be outdated" warning appears if >10 days | Not Started |
| Define error correction SLA (48 hours) | Research Director | 2026-03-15 | SLA documented, process for user-reported errors defined | Not Started |

**Target Residual Risk**: 12 (Medium) - After 3 months of ≥95% accuracy in manual validations
**Target Date**: 2026-06-30 (Month 8)

**Success Criteria**:
- Monthly manual validation shows ≥95% accuracy for 3 consecutive months (Month 6-8)
- User-reported errors <5 per month after Month 6 (indicates high perceived quality)
- Zero media retractions or public complaints about data inaccuracy
- User satisfaction score >4.0/5.0 (Outcome O-4) indicating trust in data quality

**Risk Status**: **OPEN** (Awaiting pilot validation to establish baseline)

---

#### R-004: Robots.txt Violations Trigger Legal Action (HIGH)

**Category**: COMPLIANCE/REGULATORY

**Risk Title**: Scraper violates robots.txt directives (bug, human error, infrastructure failure), triggering Computer Misuse Act complaints or IP bans

**Risk Description**:
Scraper code contains bug bypassing robots.txt check, or infrastructure-level failure (Redis rate limiter down) allows requests to disallowed paths. Restaurant detects violation via server logs, sends cease-and-desist letter citing Computer Misuse Act 1990 (unauthorized access to computer system). Platform IP address blocked by Cloudflare or website firewall, preventing further scraping. ICO investigates due to complaint, discovers robots.txt violation, escalates to legal action or fine.

**Root Cause**:
- Robots.txt compliance relies on correct implementation (software bugs possible)
- Infrastructure dependencies (Redis for rate limiting) can fail silently
- Human error during code changes could disable robots.txt check
- Scrapy `ROBOTSTXT_OBEY` setting is software-level, not infrastructure-enforced
- No external validation that scraper is truly respecting robots.txt (relies on logs)

**Trigger Events**:
- Code deployment introduces bug disabling robots.txt parser
- Redis rate limiter service outage → scraper sends rapid requests triggering anti-bot measures
- Developer accidentally sets `ROBOTSTXT_OBEY = False` during testing, forgets to re-enable
- Restaurant admin notices 500 requests/hour in server logs, investigates, finds Plymouth Research User-Agent
- Cloudflare bot protection triggers based on request patterns, blocks scraper IP entirely

**Consequences if Realized**:
- **Legal**: Cease-and-desist letter, potential lawsuit under Computer Misuse Act 1990
- **Operational**: IP address banned, scraping stops entirely until resolved (loss of 1-4 weeks data refresh)
- **Reputational**: Perceived as unethical, restaurants proactively block or complain
- **Financial**: Legal costs £5K-£25K defending complaint, potential settlement costs
- **Strategic**: Goal G-3 (100% Ethical Compliance) failed, Outcome O-2 (Zero Legal Violations) unachieved

**Affected Stakeholders**:
- Research Director (SD-2: Minimize Legal Risk - Computer Misuse Act violation is critical concern)
- Legal/Compliance Advisor (SD-8: Mitigate Legal Exposure)
- Restaurant Owners (SD-6: Accurate Representation - robots.txt violations feel intrusive)
- Data Engineer (SD-3: Maintainable Technical Solution - bugs undermine reliability)

**Related Objectives**: Goal G-3 (100% Ethical Compliance), Outcome O-2 (Zero Legal Violations), NFR-C-001 (Robots.txt Compliance)

**Inherent Risk Assessment**:
- **Inherent Likelihood**: 4 (Likely) - Software bugs are common, infrastructure failures happen
- **Inherent Impact**: 5 (Catastrophic) - Legal action, IP bans, project shutdown
- **Inherent Risk Score**: **20 (HIGH)**

**Current Controls and Mitigations**:
- **Existing Controls**:
  1. Scrapy `ROBOTSTXT_OBEY = True` setting (built-in compliance) (research-findings.md)
  2. Scraping logs record robots.txt check results for audit trail (DR-005)
  3. Monthly compliance audits by Legal Advisor (50 logs sampled) (NFR-C-001)
  4. Infrastructure-level rate limiting via Redis (prevents runaway requests) (backlog.md TS-002)
- **Control Effectiveness**: **Adequate** (controls exist but not fail-safe - software bugs possible)
- **Control Owners**: Data Engineer (scraper code), Operations/IT (infrastructure monitoring)
- **Evidence of Effectiveness**: Not yet measured - will be validated through monthly audits starting Month 2

**Residual Risk Assessment**:
- **Residual Likelihood**: 3 (Possible) - Controls reduce likelihood but cannot eliminate software bugs entirely
- **Residual Impact**: 5 (Catastrophic) - Legal/reputational impact unchanged
- **Residual Risk Score**: **15 (HIGH)**

**Risk Response**: **TREAT**

**Rationale for Response**:
Robots.txt compliance is legally and ethically non-negotiable (Principle 3). Must Treat through defense-in-depth: software controls + infrastructure enforcement + monitoring + audits.

**Risk Ownership**:
- **Risk Owner**: Data Engineer (Accountable for scraper technical implementation per RACI)
- **Action Owner**: Data Engineer (Responsible for robots.txt compliance code) + Operations/IT (infrastructure monitoring)
- **Escalation Path**: Data Engineer → Research Director → Legal Advisor (if violation detected)

**Action Plan**:

**Additional Mitigations Needed**:
1. **Automated Testing**: Unit tests verify robots.txt parser works correctly (test cases: Allow, Disallow, Wildcard, Missing robots.txt) (Month 1, Week 2)
2. **Infrastructure-Level Enforcement**: Network-level firewall rule or proxy blocks requests to known disallowed paths (fail-safe even if code fails) (Month 1, Week 3)
3. **Real-Time Monitoring**: Alert if scraper attempts request to disallowed path (log monitoring with Slack/email alert within 10 minutes) (Month 2)
4. **Pre-Deployment Checklist**: Mandatory checklist before code deployment: "Verify ROBOTSTXT_OBEY = True", "Run robots.txt test suite" (Month 1, Week 4)
5. **External Validation**: Third-party service monitors Plymouth Research scraper behavior from outside (e.g., website owner's perspective) to detect violations (Month 3)
6. **Incident Response Plan**: Runbook for robots.txt violation: immediate stop scraper, notify Research Director, legal review, apologize to restaurant, document root cause (Month 1, Week 4)

**Specific Actions**:
| Action | Owner | Due Date | Success Criteria | Status |
|--------|-------|----------|------------------|--------|
| Write robots.txt parser unit tests | Data Engineer | 2025-12-01 | 100% test coverage, all edge cases (Disallow, Wildcard, Missing) tested | Not Started |
| Implement infrastructure-level firewall rule | Operations/IT | 2025-12-08 | Firewall blocks requests to /admin, /wp-admin (common disallowed paths) | Not Started |
| Set up real-time monitoring alerts | Operations/IT | 2026-01-15 | Alert fires within 10 minutes of disallowed request attempt | Not Started |
| Create pre-deployment checklist | Data Engineer | 2025-12-01 | Checklist documented, mandatory review before production deploy | Not Started |
| Develop incident response runbook | Data Engineer + Legal Advisor | 2025-12-15 | Runbook tested in tabletop exercise, all stakeholders trained | Not Started |

**Target Residual Risk**: 6 (Medium) - After 3 months of clean audits with infrastructure-level enforcement
**Target Date**: 2026-03-31 (Month 5)

**Success Criteria**:
- Unit tests show 100% coverage of robots.txt parsing logic
- First 3 monthly audits confirm zero violations (100% compliance)
- Infrastructure firewall successfully blocks test violation attempts (verified in testing)
- Incident response runbook tested and all stakeholders familiar with procedure

**Risk Status**: **OPEN** (Awaiting implementation of additional mitigations)

---

#### R-007: DPIA Identifies High Privacy Risks (MEDIUM)

**Category**: COMPLIANCE/REGULATORY

**Risk Title**: Data Protection Impact Assessment (DPIA) identifies high privacy risks requiring extensive mitigations or project redesign

**Risk Description**:
Legal/Compliance Advisor completes DPIA and identifies risks previously underestimated: scraping restaurant staff photos constitutes processing biometric data (GDPR Article 9 special category), collecting postcode data enables identification of individuals, data retention >12 months violates necessity principle. ICO guidance requires additional safeguards (encryption, pseudonymization, consent mechanisms) that add £20K cost and 3-month timeline delay. Worst case: DPIA concludes risk is unacceptable, ICO recommends project redesign or abandonment.

**Root Cause**:
- GDPR interpretation is complex and evolving (case law changes regularly)
- Small research firm lacks in-house GDPR expertise (relies on external legal advisor)
- Scraping scope may inadvertently include personal data (staff photos, "Meet the Chef" bios)
- No prior DPIA conducted for similar web scraping projects (no precedent to reference)

**Trigger Events**:
- DPIA reveals restaurant "Our Team" pages contain staff photos (biometric data under GDPR)
- Legal advisor determines postcode-level restaurant data could indirectly identify owners (small towns)
- ICO publishes new guidance on web scraping tightening acceptable use policies
- DPIA concludes residual risk is "HIGH" requiring ICO consultation (GDPR Article 36)

**Consequences if Realized**:
- **Timeline**: 3-month delay while implementing additional safeguards or ICO consultation
- **Financial**: £10K-£20K additional legal costs, technical implementations (encryption, pseudonymization)
- **Scope**: Project scope reduced to exclude staff photos, owner names, detailed addresses
- **Strategic**: Launch delayed from Month 4 to Month 7, missing spring tourism season (user adoption impact)

**Affected Stakeholders**:
- Research Director (SD-2: Minimize Legal Risk - DPIA issues create timeline/budget risk)
- Legal/Compliance Advisor (SD-8: Mitigate Legal Exposure - must resolve findings)
- Data Engineer (SD-3: Maintainable Technical Solution - scope changes require rework)

**Related Objectives**: Goal G-8 (DPIA Completion Month 1), Outcome O-2 (Zero Legal Violations)

**Inherent Risk Assessment**:
- **Inherent Likelihood**: 3 (Possible) - DPIA may identify issues, but public business data is lower risk
- **Inherent Impact**: 4 (Major) - Timeline delay, cost increase, scope reduction (not catastrophic)
- **Inherent Risk Score**: **12 (MEDIUM)**

**Current Controls and Mitigations**:
- **Existing Controls**:
  1. DPIA planned for Month 1 before any scraping begins (requirements.md Goal G-8)
  2. Scope explicitly excludes PII collection (no customer reviews, personal contact info) (NFR-C-003)
  3. Only public business data scraped (restaurant names, addresses, menus) (NFR-C-003)
  4. 12-month data retention with automated deletion (GDPR data minimization) (NFR-C-003)
- **Control Effectiveness**: **Adequate** (scope definition is defensive, but DPIA may reveal edge cases)
- **Control Owners**: Legal/Compliance Advisor (conducts DPIA), Research Director (approves scope changes)
- **Evidence of Effectiveness**: Not yet measured - DPIA scheduled for Month 1

**Residual Risk Assessment**:
- **Residual Likelihood**: 2 (Unlikely) - Narrow scope (public business data only) reduces likelihood of high-risk findings
- **Residual Impact**: 2 (Minor) - Minor scope adjustments or safeguards manageable within budget/timeline
- **Residual Risk Score**: **4 (LOW)**

**Risk Response**: **TOLERATE**

**Rationale for Response**:
After DPIA, residual risk is acceptable (low). Likelihood is reduced by narrow scope (public business data only). Impact is manageable (minor adjustments, not project redesign). Cost of further mitigation (extensive legal review) exceeds benefit.

**Risk Ownership**:
- **Risk Owner**: Research Director (Accountable for DPIA approval per RACI)
- **Action Owner**: Legal/Compliance Advisor (Responsible for DPIA conduct)
- **Escalation Path**: Legal Advisor → Research Director → ICO (if Article 36 consultation required)

**Action Plan**:

**Additional Mitigations Needed**:
1. **Early DPIA Scoping**: Define DPIA scope with Legal Advisor before execution to flag potential issues early (Month 1, Week 1)
2. **ICO Guidance Review**: Legal Advisor reviews latest ICO guidance on web scraping and data collection (Month 1, Week 1)
3. **Staff Photo Exclusion**: Configure scraper to exclude /team, /staff, /about-us pages preemptively (avoid biometric data) (Month 1, Week 2)
4. **DPIA Iteration**: Budget 2 iterations of DPIA (initial draft, refinement after issues identified) (Month 1)

**Specific Actions**:
| Action | Owner | Due Date | Success Criteria | Status |
|--------|-------|----------|------------------|--------|
| Define DPIA scope with Legal Advisor | Research Director + Legal Advisor | 2025-11-24 | Scope agreed, timeline confirmed (4 weeks) | Not Started |
| Review ICO web scraping guidance | Legal Advisor | 2025-11-24 | Latest guidance (2023-2025) reviewed, summary provided | Not Started |
| Configure scraper to exclude staff pages | Data Engineer | 2025-12-01 | Scraper skips /team, /staff, /our-story URLs (validated) | Not Started |
| DPIA first draft completed | Legal Advisor | 2025-12-15 | Draft DPIA provided, high-level findings discussed | Not Started |
| DPIA finalized and approved | Legal Advisor + Research Director | 2025-12-31 | Final DPIA approved, no HIGH risk findings requiring ICO consultation | Not Started |

**Target Residual Risk**: 4 (Low) - After DPIA approval with no HIGH findings
**Target Date**: 2025-12-31 (Month 2)

**Success Criteria**:
- DPIA completed by 2025-12-31 with no HIGH risk findings
- All MEDIUM risk findings addressed through scope adjustments or safeguards
- No ICO Article 36 consultation required (residual risk acceptable)
- Legal Advisor provides written sign-off on DPIA adequacy

**Risk Status**: **OPEN** (Awaiting DPIA execution Month 1)

---

### TECHNOLOGY Risks

#### R-005: Cloud Costs Exceed £100/Month Budget (HIGH)

**Category**: FINANCIAL

**Risk Title**: Cloud hosting, database, and infrastructure costs exceed £100/month budget, threatening operational sustainability

**Risk Description**:
Actual cloud costs reach £200-£300/month due to underestimated usage: PostgreSQL database requires larger instance (£40/month vs £15 planned), Render background workers exceed free tier (£25/month), Selenium Grid for JavaScript rendering needs dedicated VMs (£50/month), bandwidth costs for 150 weekly scrapes (£30/month), backup storage (£15/month). Operations/IT faces budget shortfall, Research Director cannot secure additional funding, forces scope reduction or service tier downgrades impacting performance.

**Root Cause**:
- Cost estimates based on assumptions (10,000 menu items, 150 restaurants) not validated
- Free tier limits misunderstood (Render free tier = 750 hours/month, not unlimited)
- Selenium/Playwright resource requirements underestimated (requires dedicated compute)
- Database growth underestimated (menu item descriptions, historical data retention = larger DB size)
- No experience with production workloads at this scale (research firm's first data platform)

**Trigger Events**:
- DigitalOcean database bill £40/month (not £15) due to performance tuning requiring larger instance
- Render charges £50/month for background worker overages (not free as assumed)
- Selenium Grid on AWS EC2 costs £60/month (JavaScript rendering for 40% of sites)
- Total monthly cost: £180/month (80% over budget)
- Month 3 budget review reveals 3 consecutive months >£100/month

**Consequences if Realized**:
- **Financial**: Budget overrun requires Research Director to secure £1,200-£2,400 additional funding annually
- **Operational**: Cannot afford managed services, must self-host (increases Operations/IT burden 10×)
- **Performance**: Downgrade database to smaller instance → search queries slow to 2 seconds (fails Goal G-4)
- **Strategic**: Operational sustainability (Outcome O-3) unachieved, project unsustainable long-term
- **Coverage**: Reduce scraping frequency from weekly to monthly to cut costs → stale data complaints

**Affected Stakeholders**:
- Operations/IT (SD-10: Minimize Costs & Burden - budget overrun is primary concern)
- Research Director (SD-2: Minimize Legal Risk - cost overrun threatens organizational stability)
- Data Engineer (SD-3: Maintainable Technical Solution - cost cuts force technical compromises)

**Related Objectives**: Goal G-5 (Costs <£100/month), Outcome O-3 (Operational Sustainability)

**Inherent Risk Assessment**:
- **Inherent Likelihood**: 5 (Almost Certain) - Cost estimates are preliminary, production workloads unknown
- **Inherent Impact**: 5 (Catastrophic) - Budget overrun threatens project viability (no contingency funding)
- **Inherent Risk Score**: **25 (CRITICAL)**

**Current Controls and Mitigations**:
- **Existing Controls**:
  1. Wardley Map cost analysis shows £16/month operational costs (research-findings.md, wardley-maps/current-state.md)
  2. Managed services selected to minimize operational complexity (DigitalOcean PostgreSQL £15/month)
  3. Free tiers maximized (Streamlit Community Cloud, Render free tier, UptimeRobot free)
  4. Monthly cost tracking and budget alerts planned (Goal G-5 measurement)
  5. Right-sizing infrastructure (don't over-provision) (architecture principle)
- **Control Effectiveness**: **Strong** (Wardley Map analysis is comprehensive, costs validated against vendor pricing)
- **Control Owners**: Operations/IT (monitors costs), Research Director (approves budget variances)
- **Evidence of Effectiveness**: Wardley Map shows £16/month projected costs (84% under budget), providing significant buffer

**Residual Risk Assessment**:
- **Residual Likelihood**: 2 (Unlikely) - Wardley Map analysis reduces likelihood, buffer exists
- **Residual Impact**: 4 (Major) - Cost overrun still threatens sustainability if significantly over budget
- **Residual Risk Score**: **8 (MEDIUM)**

**Risk Response**: **TREAT**

**Rationale for Response**:
Cost sustainability is critical to Outcome O-3. Wardley Map analysis provides confidence but production validation needed. Must Treat through monthly monitoring and contingency planning (scope reduction if needed).

**Risk Ownership**:
- **Risk Owner**: Operations/IT (Accountable for infrastructure provisioning per RACI)
- **Action Owner**: Operations/IT (Responsible for cost tracking and optimization)
- **Escalation Path**: Operations/IT → Research Director (if monthly costs exceed £120 for 2 consecutive months)

**Action Plan**:

**Additional Mitigations Needed**:
1. **Cost Monitoring Dashboard**: Set up real-time cost tracking dashboard (DigitalOcean, Render, AWS SES usage) (Month 1)
2. **Budget Alerts**: Configure automated alerts if monthly costs exceed £80 (80% threshold) (Month 1)
3. **Monthly Cost Reviews**: Operations/IT reviews costs monthly, identifies optimization opportunities (Ongoing from Month 2)
4. **Contingency Plan**: Define cost reduction contingency: (A) Reduce scraping frequency weekly → biweekly (saves £8/month), (B) Downgrade database instance (saves £10/month), (C) Self-host Streamlit (saves £15/month Render cost) (Month 1)
5. **Selenium Optimization**: Minimize Selenium usage by detecting JavaScript-only sites upfront (scrape only when necessary) (Month 2)
6. **Database Optimization**: Implement data archival (delete menu items >12 months) to minimize database size (Month 6)

**Specific Actions**:
| Action | Owner | Due Date | Success Criteria | Status |
|--------|-------|----------|------------------|--------|
| Set up cost monitoring dashboard | Operations/IT | 2025-12-08 | Dashboard shows real-time DigitalOcean, Render, AWS costs | Not Started |
| Configure budget alerts (£80 threshold) | Operations/IT | 2025-12-08 | Email alert fires when monthly cost forecast exceeds £80 | Not Started |
| Document cost reduction contingency plan | Operations/IT + Research Director | 2025-12-01 | 3-tier plan documented (£80, £100, £120 thresholds) | Not Started |
| First monthly cost review | Operations/IT | 2026-01-31 | Month 1 actual costs measured, variance from £16 projection explained | Not Started |
| Optimize Selenium usage (detect JS-only sites) | Data Engineer | 2026-01-31 | Selenium usage reduced by 50% (20% of sites, not 40%) | Not Started |

**Target Residual Risk**: 4 (Low) - After 3 months <£50/month actual costs
**Target Date**: 2026-03-31 (Month 5)

**Success Criteria**:
- First 3 months (Month 2-4) average costs <£50/month (significant buffer under £100 target)
- No budget alerts triggered in first 6 months
- Contingency plan documented and approved but not needed
- Wardley Map projections validated within 20% accuracy

**Risk Status**: **OPEN** (Awaiting Month 1 production cost validation)

---

#### R-008: Restaurant Websites Too Complex to Scrape (HIGH)

**Category**: TECHNOLOGY

**Risk Title**: Extraction logic for diverse restaurant websites (150 different HTML structures) becomes unmanageably complex and brittle

**Risk Description**:
Each restaurant website uses different HTML structure (WordPress, Squarespace, Wix, custom CMS). Extraction logic becomes monolithic "if-else" spaghetti code: "if site is WordPress theme A, extract menu from div.menu-items; if Squarespace template B, extract from section.menu; if custom site C, use regex parsing." Code reaches 5,000 lines, impossible to maintain. Website updates break scrapers monthly, requiring constant manual fixes. Data Engineer spends 15 hours/week maintaining extraction logic (unsustainable).

**Root Cause**:
- No industry standard for restaurant menu markup (unlike Schema.org for e-commerce)
- Template platforms (Wix, Squarespace) change HTML structure in version updates
- Independent restaurants use diverse, inconsistent HTML structures
- Monolithic extraction code couples all logic together (one change breaks everything)

**Trigger Events**:
- WordPress releases new default theme breaking extraction logic for 30 restaurants
- Squarespace template update changes menu CSS classes → 20 restaurants fail overnight
- Data Engineer estimates 20 hours/week maintenance required to keep scrapers working
- Scraping success rate drops from 85% to 60% over 3 months due to website changes

**Consequences if Realized**:
- **Operational**: Maintenance burden unsustainable (20 hours/week = 50% of Data Engineer time)
- **Coverage**: Scraping success rate <70%, missing 45+ restaurants (fails Goal G-2)
- **Data Quality**: Extraction errors increase as hacky workarounds accumulate (fails Goal G-1)
- **Financial**: Must hire additional developer (£50K/year) to maintain scrapers (5× budget overrun)

**Affected Stakeholders**:
- Data Engineer (SD-3: Maintainable Technical Solution - this is nightmare scenario)
- Research Director (SD-1: Establish Authority - incomplete coverage undermines goal)
- Operations/IT (SD-10: Minimize Burden - maintenance hell creates operational burden)

**Related Objectives**: Goal G-2 (150+ Restaurants), Goal G-1 (95% Data Quality), Outcome O-3 (Operational Sustainability)

**Inherent Risk Assessment**:
- **Inherent Likelihood**: 4 (Likely) - Website diversity is known, monolithic code is common anti-pattern
- **Inherent Impact**: 4 (Major) - Maintenance burden threatens sustainability but not immediate project failure
- **Inherent Risk Score**: **16 (HIGH)**

**Current Controls and Mitigations**:
- **Existing Controls**:
  1. Pilot phase (30 restaurants) validates extraction approach before scaling to 150 (backlog.md Sprint 1-2)
  2. Modular extraction framework planned with site-specific adapters (R-002 mitigation)
  3. Scrapy framework provides infrastructure for managing multiple spiders (research-findings.md)
- **Control Effectiveness**: **Adequate** (modular approach is planned but not yet validated)
- **Control Owners**: Data Engineer (responsible for extraction framework architecture)
- **Evidence of Effectiveness**: Not yet measured - pilot will validate modular approach

**Residual Risk Assessment**:
- **Residual Likelihood**: 3 (Possible) - Modular approach reduces likelihood but website changes persist
- **Residual Impact**: 5 (Catastrophic) - Maintenance burden could still overwhelm Data Engineer
- **Residual Risk Score**: **15 (HIGH)**

**Risk Response**: **TREAT**

**Rationale for Response**:
Maintainability is critical to Outcome O-3 (Operational Sustainability). Cannot Tolerate (maintenance hell threatens project viability), cannot Transfer (no vendor provides this), cannot Terminate (abandons project). Must Treat through modular architecture and automated testing.

**Risk Ownership**:
- **Risk Owner**: Data Engineer (Accountable for database schema design per RACI, extraction logic falls under this)
- **Action Owner**: Data Engineer (Responsible for extraction framework implementation)
- **Escalation Path**: Data Engineer → Research Director (if maintenance >10 hours/week for 2 consecutive months)

**Action Plan**:

**Additional Mitigations Needed**:
1. **Modular Adapter Pattern**: Build extraction framework with pluggable site-type adapters (WordPress adapter, Squarespace adapter, Wix adapter, Generic fallback) (Month 1-2)
2. **Automated Testing**: Unit tests for each adapter with mock HTML fixtures (detect breakage immediately when website changes) (Month 2)
3. **Scraping Success Rate Monitoring**: Weekly dashboard tracking success rate per site-type (identify WordPress breakage affecting 30 sites immediately) (Month 2)
4. **Maintenance Budget**: Allocate 5 hours/week Data Engineer time for scraper maintenance (monitored, escalate if exceeds 10 hours) (Ongoing from Month 2)
5. **Fallback Strategy**: Generic extraction logic for unsupported sites (extract all text, use keyword matching for menu items) 60% accuracy acceptable for niche sites (Month 2)
6. **Template Change Monitoring**: Subscribe to WordPress, Squarespace, Wix developer newsletters to get early warning of template changes (Month 2)

**Specific Actions**:
| Action | Owner | Due Date | Success Criteria | Status |
|--------|-------|----------|------------------|--------|
| Design modular adapter pattern architecture | Data Engineer | 2025-12-01 | Architecture doc with 6 adapter types (WordPress, Squarespace, Wix, Custom, PDF, Generic) | Not Started |
| Implement WordPress adapter with unit tests | Data Engineer | 2025-12-15 | WordPress adapter extracts 90%+ menus correctly, 20 unit tests passing | Not Started |
| Implement Squarespace adapter with tests | Data Engineer | 2025-12-22 | Squarespace adapter functional, 15 unit tests passing | Not Started |
| Set up scraping success rate dashboard | Data Engineer | 2026-01-15 | Weekly success rate tracked per site-type, alerts if drops <75% | Not Started |
| Subscribe to template change notifications | Data Engineer | 2025-12-01 | Subscribed to WordPress.org, Squarespace, Wix developer blogs/newsletters | Not Started |

**Target Residual Risk**: 9 (Medium) - After modular adapters validated in production for 3 months
**Target Date**: 2026-04-30 (Month 6)

**Success Criteria**:
- Modular adapter architecture implemented with 6 adapter types
- Unit test coverage >80% for all adapters
- Maintenance time <5 hours/week average over 3 months (Month 4-6)
- Scraping success rate maintained >80% despite website changes

**Risk Status**: **OPEN** (Awaiting modular adapter implementation Month 1-2)

---

#### R-010: Performance Requirements Not Met (<500ms Search) (HIGH)

**Category**: TECHNOLOGY

**Risk Title**: Dashboard search queries exceed 500ms p95 response time target due to database query complexity or inadequate indexing

**Risk Description**:
PostgreSQL full-text search queries on 10,000 menu items return results in 800-1,500ms (p95), failing Goal G-4 (<500ms). Users perceive dashboard as "slow", abandon searches, adoption suffers. Research Analysts frustrated by lag during data exploration. Root cause: missing database indexes, inefficient JOIN queries (menu_items → dietary_tags → restaurants), full-text search tsvector not properly indexed. Data Engineer spends weeks optimizing queries post-launch instead of building new features.

**Root Cause**:
- Database indexing strategy not validated under production load
- Full-text search (tsvector/tsquery) performance depends on corpus size (10K items may exceed budget)
- Complex JOIN queries (5 tables: restaurants, menu_items, dietary_tags, menu_item_dietary_tags, categories) create query planner challenges
- No load testing performed pre-launch (performance surprises post-launch)

**Trigger Events**:
- Public launch (Month 4) → 100 concurrent users trigger slow queries
- Search query with dietary filter (vegan + gluten-free) takes 1,200ms due to inefficient JOIN
- Research Analyst reports "dashboard too slow to use for data exploration"
- User feedback survey: 40% cite "slow search" as primary complaint

**Consequences if Realized**:
- **User Adoption**: Goal G-7 (1,000+ monthly searches) unachieved due to poor UX (users abandon)
- **Performance**: Goal G-4 (<500ms) failed, Outcome O-4 (User Satisfaction) unachieved
- **Operational**: Data Engineer spends 4 weeks optimizing queries post-launch (delays other work)
- **Reputational**: "Slow, clunky interface" perception damages authority goal (Outcome O-1)

**Affected Stakeholders**:
- Plymouth Consumers (SD-5: Find Restaurants by Dietary Needs - slow search frustrates)
- Research Analysts (SD-4: Access Reliable Data - slow queries impede analysis)
- Data Engineer (SD-3: Maintainable Technical Solution - performance firefighting unsustainable)

**Related Objectives**: Goal G-4 (<500ms Performance), Outcome O-3 (Operational Sustainability), Outcome O-4 (User Satisfaction)

**Inherent Risk Assessment**:
- **Inherent Likelihood**: 3 (Possible) - Performance unknowns, but Streamlit/PostgreSQL are proven technologies
- **Inherent Impact**: 5 (Catastrophic) - Poor performance kills user adoption (project failure)
- **Inherent Risk Score**: **15 (HIGH)**

**Current Controls and Mitigations**:
- **Existing Controls**:
  1. Database indexing planned (B-tree on name, GIN on tsvector) (backlog.md TS-012, DS-009)
  2. Query optimization via EXPLAIN ANALYZE (TS-012)
  3. Redis caching layer for popular queries planned (TS-006, TS-014)
  4. Load testing in Sprint 7 (backlog.md TS-006)
  5. Performance monitoring dashboard (TS-006)
- **Control Effectiveness**: **Adequate** (controls planned but not yet implemented/validated)
- **Control Owners**: Data Engineer (query optimization, indexing)
- **Evidence of Effectiveness**: Not yet measured - load testing Sprint 7 will validate

**Residual Risk Assessment**:
- **Residual Likelihood**: 3 (Possible) - Indexing + caching should work, but production surprises possible
- **Residual Impact**: 5 (Catastrophic) - Impact unchanged if performance fails post-launch
- **Residual Risk Score**: **15 (HIGH)**

**Risk Response**: **TREAT**

**Rationale for Response**:
Performance is existential to user adoption (Goal G-7, Outcome O-4). Cannot Tolerate (catastrophic impact), cannot Transfer (performance is internal technical issue), cannot Terminate (abandons project). Must Treat through early load testing and optimization.

**Risk Ownership**:
- **Risk Owner**: Data Engineer (Accountable for database schema design per RACI)
- **Action Owner**: Data Engineer (Responsible for query optimization and indexing)
- **Escalation Path**: Data Engineer → Research Director (if load testing shows >800ms p95, requiring architecture changes)

**Action Plan**:

**Additional Mitigations Needed**:
1. **Early Load Testing**: Conduct load testing in Sprint 3 (not Sprint 7) with synthetic 10,000 menu items dataset (Month 3, not Month 7) to detect issues before launch
2. **Index Validation**: Verify all critical queries use indexes via EXPLAIN ANALYZE before launch (Month 3)
3. **Query Budget**: Establish query performance budget: single-table queries <100ms, multi-table JOINs <300ms, full-text search <500ms (Month 2)
4. **Redis Caching**: Implement caching for top 100 popular queries (e.g., "vegan", "gluten-free", popular restaurant names) (Month 3)
5. **Database Connection Pooling**: Use PgBouncer or application-level pooling to prevent connection exhaustion under load (Month 3)
6. **Query Simplification**: Denormalize data where needed (e.g., cache dietary tags as JSON array in menu_items table) to avoid JOINs (Month 3)

**Specific Actions**:
| Action | Owner | Due Date | Success Criteria | Status |
|--------|-------|----------|------------------|--------|
| Generate synthetic 10K menu items dataset | Data Engineer | 2026-01-31 | Realistic dataset with 150 restaurants, 10K items, dietary tags | Not Started |
| Conduct early load testing (100 concurrent users) | Data Engineer | 2026-02-15 | p95 response time measured, bottlenecks identified | Not Started |
| Implement database indexes (B-tree, GIN) | Data Engineer | 2026-02-22 | All indexes created, EXPLAIN ANALYZE confirms usage | Not Started |
| Implement Redis caching layer | Data Engineer | 2026-02-28 | Top 100 queries cached, cache hit rate >60% | Not Started |
| Set up database connection pooling (PgBouncer) | Operations/IT | 2026-02-28 | PgBouncer configured, connection limits tested | Not Started |

**Target Residual Risk**: 6 (Medium) - After load testing validates <500ms p95 with 10K items
**Target Date**: 2026-02-28 (Month 4, before public launch)

**Success Criteria**:
- Load testing shows p95 <500ms for all search queries (name, dietary, cuisine, price filters)
- Cache hit rate >60% for popular queries
- Database connection pooling handles 100 concurrent users without exhaustion
- No query optimization firefighting required post-launch (performance validated pre-launch)

**Risk Status**: **OPEN** (Awaiting early load testing Month 3)

---

### OPERATIONAL Risks

#### R-011: Scraper Failures Require Excessive Manual Intervention (MEDIUM)

**Category**: OPERATIONAL

**Risk Title**: Weekly automated scraping cycles fail frequently (>15% failure rate) requiring Operations/IT manual intervention, creating unsustainable operational burden

**Risk Description**:
Weekly scraper runs encounter failures: website timeouts (10% of sites), robots.txt fetching fails (5%), HTML structure changes breaking extraction logic (10%), SSL certificate errors (2%). Scraping success rate averages 73% (vs >90% target), meaning 40+ restaurants fail weekly. Operations/IT spends 10 hours/week manually restarting failed jobs, investigating errors, updating extraction logic. Operational burden unsustainable, goal of "set and forget" automation unachieved.

**Root Cause**:
- Websites are unreliable (downtime, slow response times, certificate errors)
- Extraction logic brittleness (website HTML changes break scrapers)
- Rate limiting too aggressive (5-second delays cause timeouts on slow sites)
- Error handling insufficient (scraper crashes on unexpected HTML instead of gracefully skipping)

**Trigger Events**:
- Restaurant website down during weekly scrape → failure logged, no retry attempted
- WordPress theme update changes HTML structure → 30 restaurants fail simultaneously
- SSL certificate expired on restaurant website → scraper crashes instead of logging error
- Operations/IT notices 3 consecutive weeks of 20+ failures requiring manual intervention

**Consequences if Realized**:
- **Operational**: Operations/IT burden 10 hours/week unsustainable (SD-10: Minimize Burden violated)
- **Data Freshness**: Failed scrapers mean stale data (>10 days old) for 40 restaurants → staleness warnings frustrate users
- **Coverage**: Effective coverage drops from 150 to 110 restaurants (27% reduction)
- **Strategic**: Outcome O-3 (Operational Sustainability) unachieved due to maintenance burden

**Affected Stakeholders**:
- Operations/IT (SD-10: Minimize Operational Burden - this is primary concern)
- Data Engineer (SD-3: Maintainable Technical Solution - brittle scrapers violate this)
- Plymouth Consumers (SD-5: Find Restaurants by Dietary Needs - stale data reduces value)

**Related Objectives**: Goal G-2 (150+ Restaurants), Outcome O-3 (Operational Sustainability), NFR-P-003 (Scraping Cycle Completion)

**Inherent Risk Assessment**:
- **Inherent Likelihood**: 3 (Possible) - Website failures and extraction errors are common in web scraping
- **Inherent Impact**: 4 (Major) - Operational burden threatens sustainability but not catastrophic
- **Inherent Risk Score**: **12 (MEDIUM)**

**Current Controls and Mitigations**:
- **Existing Controls**:
  1. Automated weekly scraping with Celery Beat scheduler (FR-013, backlog.md US-013)
  2. Error handling logs failures and retries next cycle (FR-013 acceptance criteria)
  3. Scraping logs track success/failure per restaurant (DR-005)
  4. Success rate monitoring dashboard planned (FR-014)
  5. 3 consecutive failures flag restaurant for manual review (FR-013 acceptance criteria)
- **Control Effectiveness**: **Adequate** (retry logic exists but manual intervention still required)
- **Control Owners**: Operations/IT (monitors failures), Data Engineer (improves error handling)
- **Evidence of Effectiveness**: Not yet measured - will be validated in Month 2 first scraping cycle

**Residual Risk Assessment**:
- **Residual Likelihood**: 3 (Possible) - Error handling reduces but doesn't eliminate failures
- **Residual Impact**: 3 (Moderate) - Manual intervention <5 hours/week acceptable (not 10+)
- **Residual Risk Score**: **9 (MEDIUM)**

**Risk Response**: **TREAT**

**Rationale for Response**:
Operational burden is manageable at <5 hours/week but must be minimized. Treat through improved error handling, automated retries, and runbooks to reduce manual intervention time.

**Risk Ownership**:
- **Risk Owner**: Operations/IT (Accountable for incident response per RACI)
- **Action Owner**: Data Engineer (Responsible for improving scraper error handling)
- **Escalation Path**: Operations/IT → Research Director (if manual intervention >10 hours/week for 2 consecutive months)

**Action Plan**:

**Additional Mitigations Needed**:
1. **Automated Retry Logic**: Retry failed scrapers 3× with exponential backoff (1 hour, 4 hours, 12 hours) before flagging for manual intervention (Month 2)
2. **Graceful Error Handling**: Scraper catches exceptions (timeout, SSL, HTML parsing errors) and logs warning instead of crashing (Month 1)
3. **Runbook for Common Failures**: Document 10 most common failure types with resolution steps (e.g., "SSL error → skip and retry tomorrow") (Month 2)
4. **Success Rate Alerts**: Alert if weekly success rate <85% (indicates systemic issue like WordPress theme update) (Month 2)
5. **Partial Success Handling**: If restaurant menu extraction partially succeeds (50% of items), accept partial data rather than failing entire restaurant (Month 2)
6. **Website Health Check**: Pre-flight health check (HTTP HEAD request) before scraping to detect downtime early (skip if down, retry tomorrow) (Month 2)

**Specific Actions**:
| Action | Owner | Due Date | Success Criteria | Status |
|--------|-------|----------|------------------|--------|
| Implement 3× retry logic with exponential backoff | Data Engineer | 2026-01-31 | Scraper retries failures automatically, logs retry attempts | Not Started |
| Add graceful error handling (catch exceptions) | Data Engineer | 2025-12-15 | Scraper handles timeout, SSL, parsing errors without crashing | Not Started |
| Document runbook for common failures | Operations/IT + Data Engineer | 2026-01-31 | Runbook covers 10 common error types with resolution steps | Not Started |
| Set up success rate alerts (<85% threshold) | Operations/IT | 2026-01-31 | Email alert fires if weekly success rate <85% | Not Started |
| Implement website health check pre-flight | Data Engineer | 2026-01-31 | HTTP HEAD request sent before scraping, skip if 5XX error | Not Started |

**Target Residual Risk**: 6 (Medium) - After automated retries reduce manual intervention to <3 hours/week
**Target Date**: 2026-03-31 (Month 5)

**Success Criteria**:
- Scraping success rate >90% average over 3 months (Month 3-5)
- Manual intervention <3 hours/week average (Month 3-5)
- Automated retries resolve 70%+ of transient failures (timeout, downtime)
- Runbook documented and used successfully for common failures

**Risk Status**: **OPEN** (Awaiting Month 2 first scraping cycle validation)

---

#### R-012: User Adoption Below Target (Market Risk) (HIGH)

**Category**: STRATEGIC

**Risk Title**: Dashboard fails to achieve 1,000+ monthly searches by Month 9 due to lack of market fit, poor UX, or inadequate marketing

**Risk Description**:
Public launch (Month 4) generates initial interest (200 searches/month) but adoption plateaus. Month 6: 400 searches, Month 9: 600 searches (40% below 1,000 target). Root cause: consumers don't perceive value (existing solutions like TripAdvisor/Google Maps "good enough"), search UX is clunky, no marketing budget to drive awareness. Goal G-7 (1,000+ searches) and Outcome O-4 (User Satisfaction & Adoption) unachieved. Research Director's authority goal (Outcome O-1) unachieved.

**Root Cause**:
- Unvalidated product-market fit assumption (consumers may not need aggregated menu search)
- No user testing pre-launch (UX issues undiscovered until post-launch complaints)
- Zero marketing budget (relying on organic word-of-mouth and SEO only)
- Competitive alternatives (TripAdvisor, Google Maps, individual restaurant websites) may satisfy need adequately
- Plymouth market size limited (200K population, ~150 restaurants = niche audience)

**Trigger Events**:
- Month 4 launch: only 150 searches in first month (below 500 expectation)
- Month 6: 350 searches (linear growth, not exponential)
- User survey feedback: "I just use Google Maps" (TripAdvisor sufficient)
- SEO analysis: Dashboard not ranking for key terms ("Plymouth restaurants", "vegan Plymouth")
- Zero media coverage post-launch (no journalists discover/cite platform)

**Consequences if Realized**:
- **Strategic**: Goal G-7 (1,000+ searches) failed, Outcome O-1 (Authority) unachieved
- **Reputational**: Research Director's strategic vision questioned by stakeholders
- **Financial**: ROI negative (£6,000 investment, minimal public value created)
- **Operational**: Platform maintained indefinitely with low usage (wasted effort)

**Affected Stakeholders**:
- Research Director (SD-1: Establish Authority - adoption validates this goal)
- Plymouth Consumers (SD-5: Find Restaurants by Dietary Needs - if unmet, solution inadequate)
- Food Writers/Journalists (SD-7: Data-Driven Reporting - if no adoption, no citations)

**Related Objectives**: Goal G-7 (1,000+ Monthly Searches), Outcome O-1 (Authority & Recognition), Outcome O-4 (User Satisfaction)

**Inherent Risk Assessment**:
- **Inherent Likelihood**: 4 (Likely) - Product-market fit unvalidated, competitive market
- **Inherent Impact**: 4 (Major) - Strategic goals unachieved but project technically successful
- **Inherent Risk Score**: **16 (HIGH)**

**Current Controls and Mitigations**:
- **Existing Controls**:
  1. User testing with Research Analysts pre-launch planned (backlog.md Sprint 8)
  2. Mobile-responsive design for mobile search (TS-020)
  3. SEO optimization (organic traffic goal 70%+)
  4. Soft launch to Plymouth food community (Month 4)
  5. CSV export for journalists/analysts (drives media citations)
- **Control Effectiveness**: **Adequate** (UX controls exist but market validation weak)
- **Control Owners**: Research Director (marketing, launch strategy), Data Engineer (UX implementation)
- **Evidence of Effectiveness**: Not yet measured - will be validated post-launch Month 4-6

**Residual Risk Assessment**:
- **Residual Likelihood**: 3 (Possible) - UX improvements reduce risk but market uncertainty persists
- **Residual Impact**: 4 (Major) - Strategic failure remains significant
- **Residual Risk Score**: **12 (MEDIUM)**

**Risk Response**: **TREAT**

**Rationale for Response**:
Market risk is significant but addressable through early validation and pivots. Must Treat through user testing, soft launch, and rapid iteration based on feedback.

**Risk Ownership**:
- **Risk Owner**: Research Director (Accountable for go/no-go launch decision per RACI)
- **Action Owner**: Research Director (Responsible for marketing and launch strategy)
- **Escalation Path**: Research Director (strategic decision: pivot vs continue vs terminate)

**Action Plan**:

**Additional Mitigations Needed**:
1. **Pre-Launch User Testing**: 10 Plymouth consumers (diverse demographics) test dashboard, provide feedback on value proposition and UX (Month 3)
2. **Value Proposition Validation**: Survey 50 Plymouth residents: "Would you use a restaurant menu search tool?" Validate demand before launch (Month 2)
3. **Soft Launch**: Launch to 50-person beta group (food bloggers, vegan Facebook groups) before public launch to validate adoption (Month 3)
4. **Launch Marketing Plan**: Local press release, social media campaign (Twitter, Plymouth subreddit, local Facebook groups), outreach to food bloggers (Month 4)
5. **Early Adoption Metrics**: Track daily searches Week 1-4 post-launch, pivot if <10 searches/day (Month 4-5)
6. **Journalist Outreach**: Email 20 local food writers with dashboard demo and CSV export offer (Month 4)
7. **Pivot Options**: If Month 6 <500 searches, pivot to (A) B2B focus (sell data to restaurants/tourism), (B) Geographic expansion (add Exeter, Torquay), or (C) Niche focus (vegan-only directory)

**Specific Actions**:
| Action | Owner | Due Date | Success Criteria | Status |
|--------|-------|----------|------------------|--------|
| Conduct pre-launch user testing (10 users) | Research Director | 2026-02-28 | 10 consumers tested, feedback documented, UX changes implemented | Not Started |
| Survey 50 residents on value proposition | Research Director | 2026-01-31 | 50 survey responses, >60% say "Yes, I would use this" | Not Started |
| Recruit 50-person soft launch beta group | Research Director | 2026-02-28 | 50 beta testers recruited (food bloggers, vegan groups) | Not Started |
| Execute soft launch (beta only) | Research Director | 2026-03-15 | Beta launch complete, early feedback collected | Not Started |
| Public launch with press release | Research Director | 2026-04-01 | Press release sent to 10 local media, social media posts live | Not Started |
| Month 6 adoption review (pivot decision) | Research Director | 2026-09-30 | If <500 searches, pivot plan activated; >500 → continue | Not Started |

**Target Residual Risk**: 8 (Medium) - After soft launch validates >500 searches/month trajectory
**Target Date**: 2026-05-31 (Month 6, 2 months post-launch)

**Success Criteria**:
- User testing shows >80% find value proposition compelling ("I would use this")
- Soft launch beta group achieves >20 searches/day (600/month trajectory)
- Month 4-5 average >500 searches/month (on track for 1,000 by Month 9)
- At least 2 local media outlets cover launch (driving awareness)

**Risk Status**: **OPEN** (Awaiting user testing and soft launch Month 3-4)

---

## Risk by Category Analysis

### COMPLIANCE/REGULATORY (5 risks)

**Total Risks**: 5
**Average Inherent Score**: 18.8
**Average Residual Score**: 12.6
**Effectiveness of Controls**: 33% reduction

**Critical/High Risks**: 4 (R-001, R-002 partially, R-004, R-007)

**Key Themes**:
- Legal grey area around web scraping in UK creates inherent uncertainty
- GDPR compliance is complex for small organizations without in-house expertise
- Robots.txt violations have severe consequences (legal action, IP bans, reputation damage)
- DPIA may reveal unexpected privacy risks requiring costly mitigations

**Top Mitigation**: Engage Legal/Compliance Advisor early (Month 1 Week 1) for DPIA and legal opinion

**Escalation Required**: R-001 (GDPR/Legal Non-Compliance) and R-004 (Robots.txt Violations) require Research Director sign-off on mitigation plans

---

### TECHNOLOGY (4 risks)

**Total Risks**: 4
**Average Inherent Score**: 20.3
**Average Residual Score**: 15.5
**Effectiveness of Controls**: 24% reduction

**Critical/High Risks**: 4 (R-002, R-005, R-008, R-010)

**Key Themes**:
- Web scraping technical complexity is underestimated (diverse websites, JavaScript rendering, anti-scraping measures)
- Performance at scale unvalidated (10,000 menu items, 100 concurrent users)
- Extraction logic maintainability threatened by website diversity (150 different HTML structures)
- Cloud cost estimates based on assumptions, not production validation

**Top Mitigation**: Conduct pilot scraping (30 diverse restaurants) in Month 1-2 to validate feasibility before full build

**Escalation Required**: R-002 (Web Scraping Feasibility) requires Go/No-Go decision if pilot shows <70% success rate

---

### OPERATIONAL (4 risks)

**Total Risks**: 4
**Average Inherent Score**: 13.5
**Average Residual Score**: 10.0
**Effectiveness of Controls**: 26% reduction

**Critical/High Risks**: 1 (R-012)

**Key Themes**:
- Manual operational burden threatens "set and forget" automation goal
- Scraper failures expected (website downtime, HTML changes, SSL errors) requiring robust error handling
- User adoption risk due to unvalidated product-market fit
- Opt-out requests could reduce coverage significantly if >20% restaurants request removal

**Top Mitigation**: Implement automated retry logic and graceful error handling to minimize manual intervention

**Escalation Required**: R-012 (User Adoption) requires pivot decision at Month 6 if <500 searches/month

---

### FINANCIAL (3 risks)

**Total Risks**: 3
**Average Inherent Score**: 18.3
**Average Residual Score**: 10.0
**Effectiveness of Controls**: 45% reduction (highest effectiveness)

**Critical/High Risks**: 1 (R-005)

**Key Themes**:
- Cloud cost overruns threaten operational sustainability (largest inherent risk: R-005 score 25)
- Budget constraints limit options (no contingency funding for overruns)
- Managed services balance cost vs operational complexity trade-off
- Wardley Map analysis provides strong confidence in cost projections (£16/month)

**Top Mitigation**: Monthly cost monitoring with £80/month alert threshold to detect overruns early

**Escalation Required**: R-005 (Cloud Costs) requires Research Director approval if costs exceed £120/month for 2 consecutive months

---

### REPUTATIONAL (2 risks)

**Total Risks**: 2
**Average Inherent Score**: 22.5
**Average Residual Score**: 17.5
**Effectiveness of Controls**: 22% reduction

**Critical/High Risks**: 2 (R-003, R-006 partially)

**Key Themes**:
- Data quality failures have catastrophic reputational impact (trust impossible to rebuild)
- Service outages during peak usage damage credibility
- Dietary tag errors create safety risks (allergy sufferers)
- Negative social media posts can go viral, destroying authority goal overnight

**Top Mitigation**: Conservative dietary tagging with explicit disclaimers to prevent dangerous misclassification

**Escalation Required**: R-003 (Data Quality Failures) requires immediate Research Director notification if accuracy drops below 85% in any monthly validation

---

### STRATEGIC (2 risks)

**Total Risks**: 2
**Average Inherent Score**: 16.0
**Average Residual Score**: 11.0
**Effectiveness of Controls**: 31% reduction

**Critical/High Risks**: 1 (R-012)

**Key Themes**:
- Market adoption is largest strategic uncertainty (product-market fit unvalidated)
- Competitive threats from better-funded platforms (TripAdvisor, Google Maps extensions)
- Geographic market size limited (Plymouth = 200K population)
- First-mover advantage critical (18-month window before competitors react)

**Top Mitigation**: Pre-launch user testing and soft launch beta to validate demand before public launch

**Escalation Required**: R-012 (User Adoption) and R-015 (Competitor Threat) require strategic review at Month 6

---

## Risk Ownership Matrix

| Stakeholder | Owned Risks | Critical/High Risks | Notes |
|-------------|-------------|---------------------|-------|
| **Research Director** | R-001, R-007, R-012, R-013, R-015 | 2 Critical (R-001), 1 High (R-012) | Heavy concentration of strategic/compliance risks; accountable for all legal/compliance decisions per RACI |
| **Data Engineer** | R-002, R-003, R-004, R-008, R-010 | 2 Critical (R-003), 4 High (R-002, R-004, R-008, R-010) | Highest risk load; owns all technology risks; critical path for project success |
| **Operations/IT** | R-005, R-006, R-011, R-014, R-016 | 1 High (R-005) | Financial sustainability focus; infrastructure reliability critical |
| **Legal/Compliance Advisor** | (Support role, no primary ownership) | Supports R-001, R-004, R-007 | Advisory capacity per RACI, not primary risk owner |

**Risk Concentration Analysis**:
- **Data Engineer**: 5 risks, 6 Critical/High → Heaviest burden, requires Research Director support
- **Research Director**: 5 risks, 3 Critical/High → Strategic/compliance focus, appropriate for executive
- **Operations/IT**: 5 risks, 1 High → Operational focus, manageable load

**Recommendations**:
1. **Data Engineer Support**: Consider hiring junior developer (Month 3) to assist with extraction logic maintenance (reduces R-008, R-011 burden)
2. **Legal Advisor Engagement**: Formalize retainer agreement (5 hours/month) for ongoing compliance support (R-001, R-004, R-007)
3. **Research Director Prioritization**: Focus on R-001 (GDPR) and R-012 (User Adoption) as highest strategic priorities

---

## 4Ts Response Summary

| Response | Count | % | Key Examples |
|----------|-------|---|--------------|
| **Tolerate** | 3 risks | 15% | R-007 (DPIA risks - low after controls), R-009 (Developer turnover - unavoidable), R-020 (Minor UI bugs) |
| **Treat** | 15 risks | 75% | R-001 (GDPR - DPIA + legal review), R-002 (Feasibility - pilot), R-003 (Data Quality - validation), R-005 (Costs - monitoring), R-008 (Complexity - modular architecture) |
| **Transfer** | 1 risk | 5% | R-006 (Service Outages - managed hosting SLA), R-014 (DDoS - Cloudflare) |
| **Terminate** | 1 risk | 5% | R-019 (High-risk vendor - cancel contract if compliance unclear) |

**4Ts Distribution Analysis**:
- **Treat dominance** (75%): Reflects project phase (pre-launch, active risk mitigation required)
- **Low Transfer** (5%): Limited insurance/outsourcing options for web scraping project
- **Low Terminate** (5%): No activities identified as risk exceeding appetite requiring termination
- **Tolerate appropriate** (15%): Low residual risks after controls applied

**Pattern Observations**:
- Critical risks (R-001, R-003) → Treat (cannot tolerate catastrophic impact)
- High likelihood + High impact (R-002, R-005, R-008) → Treat (mitigations reduce to acceptable level)
- Low residual score (R-007, R-020) → Tolerate (cost of further mitigation exceeds benefit)
- Infrastructure failures (R-006, R-014) → Transfer (managed hosting providers assume responsibility)

---

## Action Plan (Prioritized)

### Priority 1: IMMEDIATE (Week 1-2, Nov 18-Dec 1)

| Priority | Action | Risk(s) Addressed | Owner | Due Date | Status |
|----------|--------|-------------------|-------|----------|--------|
| **1** | Engage Legal/Compliance Advisor for DPIA initiation | R-001 (Critical) | Research Director | 2025-11-24 | Not Started |
| **2** | Obtain legal opinion on web scraping defensibility | R-001 (Critical), R-004 (High) | Legal Advisor | 2025-12-01 | Not Started |
| **3** | Compile diverse pilot sample (30 restaurants) | R-002 (High), R-008 (High) | Data Engineer | 2025-11-24 | Not Started |
| **4** | Define technical feasibility threshold (≥80% success) | R-002 (High) | Data Engineer + Research Director | 2025-11-24 | Not Started |
| **5** | Write robots.txt parser unit tests | R-004 (High) | Data Engineer | 2025-12-01 | Not Started |
| **6** | Set up cost monitoring dashboard | R-005 (High) | Operations/IT | 2025-12-08 | Not Started |
| **7** | Configure budget alerts (£80/month threshold) | R-005 (High) | Operations/IT | 2025-12-08 | Not Started |
| **8** | Survey 50 Plymouth residents on value proposition | R-012 (High) | Research Director | 2025-12-01 | Not Started |

### Priority 2: SHORT-TERM (Month 1-3, Dec-Feb)

| Priority | Action | Risk(s) Addressed | Owner | Due Date | Status |
|----------|--------|-------------------|-------|----------|--------|
| **9** | Execute pilot scraping (30 restaurants) | R-002 (High), R-008 (High) | Data Engineer | 2025-12-22 | Not Started |
| **10** | Manual validation of 30 pilot menus (accuracy baseline) | R-003 (Critical) | Research Analyst | 2025-12-29 | Not Started |
| **11** | Pilot review meeting (Go/No-Go decision) | R-002 (High) | Data Engineer + Research Director | 2025-12-29 | Not Started |
| **12** | Implement PII detection regex scanner | R-001 (Critical) | Data Engineer | 2025-12-08 | Not Started |
| **13** | DPIA first draft completed | R-001 (Critical), R-007 (Medium) | Legal Advisor | 2025-12-15 | Not Started |
| **14** | Build modular extraction framework (6 adapters) | R-008 (High) | Data Engineer | 2025-12-15 | Not Started |
| **15** | Implement 3× retry logic with exponential backoff | R-011 (Medium) | Data Engineer | 2026-01-31 | Not Started |
| **16** | Conduct early load testing (100 concurrent users) | R-010 (High) | Data Engineer | 2026-02-15 | Not Started |
| **17** | Implement database indexes (B-tree, GIN) | R-010 (High) | Data Engineer | 2026-02-22 | Not Started |
| **18** | Implement Redis caching layer | R-010 (High) | Data Engineer | 2026-02-28 | Not Started |
| **19** | Pre-launch user testing (10 Plymouth consumers) | R-012 (High) | Research Director | 2026-02-28 | Not Started |
| **20** | Recruit 50-person soft launch beta group | R-012 (High) | Research Director | 2026-02-28 | Not Started |

### Priority 3: MEDIUM-TERM (Month 4-6, Mar-May)

| Priority | Action | Risk(s) Addressed | Owner | Due Date | Status |
|----------|--------|-------------------|-------|----------|--------|
| **21** | Execute soft launch (beta only) | R-012 (High) | Research Director | 2026-03-15 | Not Started |
| **22** | Public launch with press release | R-012 (High) | Research Director | 2026-04-01 | Not Started |
| **23** | First compliance audit (50 logs sampled) | R-001 (Critical), R-004 (High) | Legal Advisor | 2026-02-01 | Not Started |
| **24** | Add dietary tag disclaimer to dashboard | R-003 (Critical) | Data Engineer | 2026-02-28 | Not Started |
| **25** | Month 6 adoption review (pivot decision point) | R-012 (High) | Research Director | 2026-09-30 | Not Started |

### Priority 4: ONGOING (Month 2+)

| Priority | Action | Risk(s) Addressed | Owner | Frequency | Status |
|----------|--------|-------------------|-------|-----------|--------|
| **26** | Monthly compliance audits | R-001, R-004 | Legal Advisor | Monthly | Not Started |
| **27** | Monthly cost reviews and optimization | R-005 | Operations/IT | Monthly | Not Started |
| **28** | Weekly scraping success rate monitoring | R-002, R-008, R-011 | Data Engineer | Weekly | Not Started |
| **29** | Monthly data quality validation (100 items) | R-003 | Research Analyst | Monthly | Not Started |

---

## Monitoring and Review Framework

### Review Frequency

**Critical Risks (Score 20-25)**: **Weekly review** with Research Director
- R-001: GDPR/Legal Non-Compliance
- R-003: Data Quality Failures

**High Risks (Score 13-19)**: **Bi-weekly review** with risk owners
- R-002: Web Scraping Feasibility
- R-004: Robots.txt Violations
- R-005: Cloud Costs Exceed Budget
- R-008: Restaurant Websites Too Complex
- R-010: Performance Requirements Not Met
- R-012: User Adoption Below Target

**Medium Risks (Score 6-12)**: **Monthly review** with risk owners
- R-006, R-007, R-011, R-013, R-014, R-015, R-016, R-017, R-018, R-019

**Low Risks (Score 1-5)**: **Quarterly review**
- R-009, R-020

### Escalation Criteria

**Immediate Escalation to Research Director** (within 24 hours):
- Any Critical risk (R-001, R-003) increases in score by 3+ points
- Any new Critical risk identified (score 20-25)
- Legal complaint, cease-and-desist letter, or ICO inquiry received
- Pilot scraping shows <70% success rate (R-002 trigger)
- Data quality drops below 85% in any monthly validation (R-003 trigger)
- Monthly costs exceed £120 for 2 consecutive months (R-005 trigger)

**Escalation to Steering Committee** (weekly meeting):
- Any High risk unmitigated for 2+ weeks beyond target date
- 3+ risks increase in score within same month (systemic issue indicator)
- Budget variance >20% (£120+/month actual costs)
- Timeline delay >2 weeks on critical path

**Escalation to Legal Advisor** (ad-hoc):
- Robots.txt violation detected (R-004)
- Restaurant complaint received (R-001, R-004)
- DPIA identifies HIGH risk finding (R-007)

### Reporting Requirements

**Weekly Risk Report** (Research Director):
- Critical risks status update (R-001, R-003)
- Top 3 action items due in next 2 weeks
- Any new risks identified or escalations

**Monthly Project Board Report**:
- Full risk register summary (all 20 risks)
- Risk matrix (inherent vs residual visualization)
- Top 10 risks ranked by residual score
- 4Ts response distribution
- Action plan progress (% complete)
- Risk appetite compliance assessment (if appetite defined)

**Quarterly Audit Committee Report** (if applicable):
- Risk appetite compliance (3-month trend)
- Major risk movements (3+ point changes)
- Compliance risks (R-001, R-004, R-007) deep dive
- Financial risks (R-005, R-017) trend analysis

**Ad-hoc Incident Reports**:
- Robots.txt violation incident (R-004)
- Data quality failure causing user complaint (R-003)
- Legal correspondence (R-001, R-004)

### Next Review Date

**Risk Register Comprehensive Review**: 2025-12-17 (1 month from creation)

**Review Agenda**:
1. Validate pilot scraping results (R-002, R-008) - Go/No-Go decision
2. Review DPIA findings (R-001, R-007) - Legal approval status
3. Assess Month 1 cost actuals vs projections (R-005)
4. Update residual risk scores based on new evidence
5. Identify any new risks from pilot phase learnings
6. Confirm risk ownership assignments (RACI validation)

---

## Integration with SOBC (Strategic Outline Business Case)

This risk register feeds into the following SOBC sections:

### Strategic Case (Part A)
- **Strategic Risks**: R-012 (User Adoption), R-015 (Competitor Threat) inform "Why Now?" urgency argument
- **Reputation Risks**: R-003 (Data Quality) supports need for robust quality controls in strategic approach

### Economic Case (Part B)
- **Risk-Adjusted Costs**: R-005 (Cloud Costs) used to calculate optimism bias adjustment (+20% contingency)
- **Sensitivity Analysis**: R-002 (Feasibility), R-008 (Complexity) inform "What if scraping success rate is only 70%?" scenario
- **Benefit Realization Risk**: R-012 (User Adoption) affects value-for-money calculation (lower adoption = lower benefits)

### Commercial Case (Part C)
- **Procurement Risk**: R-019 (Vendor risk) - if applicable for managed services procurement
- **Contract Risk**: R-005 (Cloud costs) inform contract negotiation and SLA requirements

### Financial Case (Part D)
- **Budget Risk**: R-005 (Cloud Costs), R-017 (Funding shortfall) inform contingency budget (recommend 25% contingency = £25/month reserve)
- **Affordability Assessment**: Residual financial risks demonstrate project remains within £100/month affordability constraint

### Management Case (Part E)
- **Risk Management Approach**: Full risk register demonstrates Orange Book-compliant risk management
- **Governance Arrangements**: Risk ownership matrix aligns with RACI governance structure
- **Assurance Strategy**: Monthly compliance audits (R-001, R-004) provide assurance evidence

**Recommendation for SOBC Authors**:
- Reference this risk register in Management Case Part E (Risk Management section)
- Use R-005 (Cloud Costs) residual score 14 (High) to justify £25/month contingency budget
- Cite R-002 (Feasibility pilot) as critical approval condition ("Approval conditional on pilot success ≥80%")
- Flag R-001 (GDPR) and R-003 (Data Quality) as NON-NEGOTIABLE - must achieve residual score <15 before proceeding to Outline Business Case

---

## Appendix A: Risk Assessment Scales

### Likelihood Scale (1-5)

| Score | Level | Probability | Frequency | Description |
|-------|-------|-------------|-----------|-------------|
| **1** | Rare | <5% | Once every 5+ years | Highly unlikely to occur, no history of occurrence |
| **2** | Unlikely | 5-25% | Once every 2-5 years | Could happen but probably won't, rare occurrence |
| **3** | Possible | 25-50% | Once every 1-2 years | Reasonable chance of occurring, has happened before |
| **4** | Likely | 50-75% | Multiple times per year | More likely to happen than not, regular occurrence |
| **5** | Almost Certain | >75% | Expected monthly/quarterly | Expected to occur, frequent/ongoing issue |

### Impact Scale (1-5)

| Score | Level | Financial | Timeline | Reputation | Strategic |
|-------|-------|-----------|----------|------------|-----------|
| **1** | Negligible | <£5K / <5% variance | <1 week delay | Minimal notice | Minor setback, easily recovered |
| **2** | Minor | £5-10K / 5-10% variance | 1-2 week delay | Local criticism | Temporary goal delay |
| **3** | Moderate | £10-25K / 10-20% variance | 2-4 week delay | Media coverage | Significant goal impact |
| **4** | Major | £25-50K / 20-40% variance | 1-3 month delay | Sustained negative coverage | Major goals unachieved |
| **5** | Catastrophic | >£50K / >40% variance | >3 month delay or project failure | Permanent reputation damage | Project/organizational failure |

### Risk Score Matrix (Likelihood × Impact)

| Score Range | Level | Color | Action Required |
|-------------|-------|-------|-----------------|
| **20-25** | Critical | Red | Immediate escalation to Research Director, urgent mitigation, weekly review |
| **13-19** | High | Orange | Active management, mitigation plan required, bi-weekly review |
| **6-12** | Medium | Yellow | Mitigate where cost-effective, monthly monitoring |
| **1-5** | Low | Green | Accept/tolerate, quarterly review |

---

## Appendix B: Glossary

**DPIA**: Data Protection Impact Assessment - mandatory GDPR assessment for high-risk data processing

**Inherent Risk**: Risk level before any controls or mitigations applied (worst-case scenario)

**Residual Risk**: Risk level after current controls and planned mitigations applied (realistic scenario)

**4Ts Framework**: HM Treasury risk response options - Tolerate, Treat, Transfer, Terminate

**RACI Matrix**: Responsible, Accountable, Consulted, Informed - governance decision-making framework

**Orange Book**: HM Treasury guidance on risk management in UK Government and public sector organizations

**Robots.txt**: Website file specifying which parts of site can be accessed by automated scrapers (web standard)

**GDPR**: General Data Protection Regulation (UK GDPR post-Brexit) - data protection law

**Computer Misuse Act 1990**: UK law criminalizing unauthorized access to computer systems (relevant to web scraping)

**ICO**: Information Commissioner's Office - UK data protection regulator

**p95**: 95th percentile - 95% of events complete within this time (performance measurement standard)

**Scrapy**: Open source Python web scraping framework (research-findings.md Option 1A)

**Selenium/Playwright**: Browser automation tools for scraping JavaScript-heavy websites

**PostgreSQL**: Open source relational database with full-text search capability

**Streamlit**: Open source Python dashboard framework (research-findings.md)

---

## Appendix C: Risk Register Ownership and Approval

**Risk Register Owner**: Research Director (accountable for overall risk management per RACI)

**Contributors**:
- Data Engineer: Technology and operational risks (R-002, R-003, R-004, R-008, R-010, R-011)
- Operations/IT: Financial and infrastructure risks (R-005, R-006, R-014, R-016)
- Legal/Compliance Advisor: Compliance and regulatory risks (R-001, R-004, R-007)
- Research Analysts: User adoption and data quality risks (R-003, R-012)

**Review and Approval**:

| Role | Name | Review Date | Comments | Approval Status |
|------|------|-------------|----------|-----------------|
| **Research Director** (Risk Owner) | [Awaiting Approval] | [TBD] | [Pending review] | DRAFT |
| **Data Engineer** (Technology Risks) | [Awaiting Approval] | [TBD] | [Pending review] | DRAFT |
| **Legal/Compliance Advisor** (Compliance) | [Awaiting Approval] | [TBD] | [Pending review] | DRAFT |
| **Operations/IT** (Financial/Infrastructure) | [Awaiting Approval] | [TBD] | [Pending review] | DRAFT |

**Next Steps**:
1. Circulate draft risk register to all stakeholders for review (2025-11-20)
2. Incorporate feedback and finalize v1.0 (2025-11-27)
3. Present to Steering Committee for approval (2025-12-04)
4. Commence immediate actions (Priority 1) upon approval

---

**Generated by**: ArcKit `/arckit.risk` command
**Generated on**: 2025-11-17
**ArcKit Version**: 0.9.1
**Project**: Plymouth Research Restaurant Menu Analytics (Project 001)
**AI Model**: Claude 3.5 Sonnet (claude-sonnet-4-5-20250929)
**Framework**: HM Treasury Orange Book 2023
