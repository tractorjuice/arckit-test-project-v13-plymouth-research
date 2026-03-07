# Risk Register

> **Template Origin**: Official | **ArcKit Version**: 4.0.0 | **Command**: `$arckit-risk`

## Document Control

| Field | Value |
|-------|-------|
| **Document ID** | ARC-001-RISK-v1.0 |
| **Document Type** | Risk Register |
| **Project** | GenAI for UK Policing (Project 001) |
| **Classification** | OFFICIAL |
| **Status** | DRAFT |
| **Version** | 1.0 |
| **Created Date** | 2026-03-07 |
| **Last Modified** | 2026-03-07 |
| **Review Cycle** | Monthly |
| **Next Review Date** | 2026-04-06 |
| **Owner** | Service Owner, GenAI for UK Policing |
| **Reviewed By** | PENDING |
| **Approved By** | PENDING |
| **Distribution** | Project Board, Risk Owners, Architecture Team, Security, Data Protection, Legal, Pilot Forces |

## Revision History

| Version | Date | Author | Changes | Approved By | Approval Date |
|---------|------|--------|---------|-------------|---------------|
| 1.0 | 2026-03-07 | ArcKit AI | Initial creation from `$arckit-risk` command | PENDING | PENDING |

---

## Executive Summary

### Risk Profile Overview

**Total Risks Identified:** 13 risks across 6 categories

| Risk Level | Inherent | Residual | Movement |
|------------|----------|----------|----------|
| **Critical** (20-25) | 6 | 0 | -6 |
| **High** (13-19) | 4 | 0 | -4 |
| **Medium** (6-12) | 3 | 12 | +9 |
| **Low** (1-5) | 0 | 1 | +1 |
| **TOTAL** | 13 | 13 | n/a |

### Risk Category Distribution

| Category | Count | Avg Inherent | Avg Residual | Control Effectiveness |
|----------|-------|--------------|--------------|----------------------|
| **STRATEGIC** | 3 | 19.0 | 7.7 | 59% reduction |
| **OPERATIONAL** | 2 | 16.0 | 9.0 | 44% reduction |
| **FINANCIAL** | 2 | 16.0 | 9.0 | 44% reduction |
| **COMPLIANCE** | 2 | 16.0 | 9.0 | 44% reduction |
| **REPUTATIONAL** | 2 | 16.0 | 9.0 | 44% reduction |
| **TECHNOLOGY** | 2 | 20.0 | 12.0 | 40% reduction |

### Overall Risk Assessment

**Overall Residual Risk Score:** 119/325  
**Risk Reduction from Controls:** 47% reduction from inherent (225 → 119)  
**Risk Profile Status:** Concerning

### Risk Appetite Position

No formal organizational risk appetite statement was provided in
`projects/000-global/risk-appetite.md`. This draft therefore uses **provisional project escalation
thresholds** for decision support only:

- Strategic: 12
- Operational: 9
- Financial: 9
- Compliance: 9
- Reputational: 9
- Technology: 9

### Risks Exceeding Provisional Threshold

**Number of risks exceeding provisional threshold:** 5 risks

| Risk ID | Title | Category | Residual Score | Threshold | Excess | Escalation |
|---------|-------|----------|----------------|-----------|--------|------------|
| R-006 | Scale-up case not approved | FINANCIAL | 12 | 9 | +3 | Project Board |
| R-007 | Lawful basis not sustained | COMPLIANCE | 12 | 9 | +3 | SIRO and Project Board |
| R-009 | Public trust damaged by output failure | REPUTATIONAL | 12 | 9 | +3 | SRO and Project Board |
| R-011 | Integration fails provenance controls | TECHNOLOGY | 12 | 9 | +3 | Service Owner and Project Board |
| R-012 | Sensitive data exposed through orchestration gap | TECHNOLOGY | 12 | 9 | +3 | CISO and Project Board |

### Top 5 Risks Requiring Immediate Attention

1. **R-007** (COMPLIANCE, residual 12): Lawful basis not sustained for a live workflow  
   Owner: SIRO
2. **R-009** (REPUTATIONAL, residual 12): Public trust damaged by inaccurate or biased output  
   Owner: SRO
3. **R-012** (TECHNOLOGY, residual 12): Sensitive data exposed through orchestration security gap  
   Owner: CISO
4. **R-011** (TECHNOLOGY, residual 12): Integration fails provenance and reliability controls  
   Owner: Service Owner
5. **R-006** (FINANCIAL, residual 12): Benefits evidence too weak for scale-up approval  
   Owner: SRO

### Key Findings and Recommendations

**Key Findings**:

- Risk ownership is concentrated in four accountable roles from the stakeholder RACI, with the SRO
  owning the largest share of strategic, financial, and reputational exposure.
- Controls materially reduce catastrophic outcomes, but five residual risks still exceed the
  provisional threshold and need board-level scrutiny.
- The highest remaining risk themes are lawful workflow approval, public trust, legacy integration,
  and proving value-for-money before wider rollout.

**Recommendations**:

1. Escalate R-006, R-007, R-009, R-011, and R-012 to the next Project Board review.
2. Lock high-risk scope behind documented assurance gates until the first three workflows are fully
   evidenced.
3. Prioritize integration proving, lawful basis packs, and security control validation ahead of any
   scope expansion.

---

## A. Risk Matrix Visualization

### Inherent Risk Matrix (Before Controls)

```text
                                    IMPACT
              1-Minimal   2-Minor    3-Moderate   4-Major        5-Severe
           ┌───────────┬───────────┬───────────┬──────────────┬──────────────┐
5-Almost   │           │           │           │ R-001,R-011  │ R-013        │
Certain    │    5      │    10     │    15     │    20        │    25        │
           ├───────────┼───────────┼───────────┼──────────────┼──────────────┤
4-Likely   │           │           │           │ R-003,R-004  │ R-005,R-006, │
           │    4      │    8      │    12     │    16        │ R-007,R-009, │
           │           │           │           │              │ R-012         │
           ├───────────┼───────────┼───────────┼──────────────┼──────────────┤
3-Possible │           │           │           │ R-002,R-008, │              │
           │    3      │    6      │    9      │ R-010        │              │
           ├───────────┼───────────┼───────────┼──────────────┼──────────────┤
2-Unlikely │           │           │           │              │              │
           │    2      │    4      │    6      │    8         │    10        │
           ├───────────┼───────────┼───────────┼──────────────┼──────────────┤
1-Rare     │           │           │           │              │              │
           │    1      │    2      │    3      │    4         │    5         │
           └───────────┴───────────┴───────────┴──────────────┴──────────────┘

Legend: Critical (20-25)  High (13-19)  Medium (6-12)  Low (1-5)
```

### Residual Risk Matrix (After Controls)

```text
                                    IMPACT
              1-Minimal   2-Minor    3-Moderate     4-Major        5-Severe
           ┌───────────┬───────────┬──────────────┬──────────────┬───────────┐
5-Almost   │           │           │              │              │           │
Certain    │    5      │    10     │    15        │    20        │    25     │
           ├───────────┼───────────┼──────────────┼──────────────┼───────────┤
4-Likely   │           │           │ R-011,R-012  │              │           │
           │    4      │    8      │    12        │    16        │    20     │
           ├───────────┼───────────┼──────────────┼──────────────┼───────────┤
3-Possible │           │           │ R-003,R-004  │ R-001,R-006, │           │
           │    3      │    6      │    9         │ R-007,R-009  │           │
           ├───────────┼───────────┼──────────────┼──────────────┼───────────┤
2-Unlikely │           │           │ R-005,R-008, │ R-002        │           │
           │    2      │    4      │ R-010        │    8         │    10     │
           ├───────────┼───────────┼──────────────┼──────────────┼───────────┤
1-Rare     │           │           │ R-013        │              │           │
           │    1      │    2      │    3         │    4         │    5      │
           └───────────┴───────────┴──────────────┴──────────────┴───────────┘

Legend: Critical (20-25)  High (13-19)  Medium (6-12)  Low (1-5)
```

### Risk Movement Analysis

- **R-013** moved from Critical (25) to Low (3) because the risky activity is explicitly
  terminated from current scope.
- **R-001**, **R-007**, **R-009**, **R-011**, and **R-012** reduced from Critical to Medium, but
  still require senior monitoring.
- No residual risks remain in the High or Critical zone, but the medium cluster is large and still
  operationally significant.

---

## B. Top 10 Risks (Ranked by Residual Score)

| Rank | ID | Title | Category | Inherent | Residual | Owner | Status | Response |
|------|----|-------|----------|----------|----------|-------|--------|----------|
| 1 | R-007 | Lawful basis not sustained | COMPLIANCE | 20 | 12 | SIRO | In Progress | Treat |
| 2 | R-009 | Public trust damaged by output failure | REPUTATIONAL | 20 | 12 | SRO | Open | Treat |
| 3 | R-012 | Sensitive data exposed through orchestration gap | TECHNOLOGY | 20 | 12 | CISO | In Progress | Treat |
| 4 | R-011 | Integration fails provenance controls | TECHNOLOGY | 20 | 12 | Service Owner | Open | Treat |
| 5 | R-001 | Assurance slippage delays first live release | STRATEGIC | 20 | 12 | SRO | In Progress | Treat |
| 6 | R-006 | Scale-up case not approved | FINANCIAL | 16 | 12 | SRO | Open | Treat |
| 7 | R-003 | Pilot adoption below productivity target | OPERATIONAL | 16 | 9 | Service Owner | In Progress | Treat |
| 8 | R-004 | Support capacity lags force onboarding | OPERATIONAL | 16 | 9 | Service Owner | Open | Treat |
| 9 | R-002 | Policy change reshapes programme priorities | STRATEGIC | 12 | 8 | SRO | Monitoring | Tolerate |
| 10 | R-005 | Supplier cost growth breaches funding envelope | FINANCIAL | 16 | 6 | SRO | In Progress | Transfer |

---

## C. Detailed Risk Register

| Risk ID | Category | Title | Description | Inherent L/I/S | Controls | Residual L/I/S | 4Ts Response | Owner | Status | Actions | Target Date |
|---------|----------|-------|-------------|----------------|----------|----------------|--------------|-------|--------|---------|-------------|
| R-001 | STRATEGIC | Assurance slippage delays first live release | Delivery pressure pushes workflow scope faster than assurance evidence can support. | 4/5/20 | Phased rollout, governance gates, conflict resolution from STKE | 3/4/12 | Treat | SRO | In Progress | Freeze high-risk scope until assurance pack completion dashboard is green | 2026-08-31 |
| R-002 | STRATEGIC | Policy change reshapes programme priorities | Sponsor or policy direction changes before scale-up, altering value case or scope sequencing. | 3/4/12 | Home Office engagement, modular roadmap, reusable architecture | 2/4/8 | Tolerate | SRO | Monitoring | Maintain quarterly policy review and scenario options | 2026-09-30 |
| R-003 | OPERATIONAL | Pilot adoption below productivity target | Users do not trust or consistently use the service, preventing forecast benefits. | 4/4/16 | Pilot workflow selection, safe-use guidance, training and feedback loops | 3/3/9 | Treat | Service Owner | In Progress | Baseline user metrics and improve pilot workflow fit | 2026-10-31 |
| R-004 | OPERATIONAL | Support capacity lags force onboarding | Service operations and onboarding teams cannot support force rollout pace safely. | 4/4/16 | Runbooks, onboarding pack, readiness reviews | 3/3/9 | Treat | Service Owner | Open | Resource force onboarding and operational support plan | 2026-09-15 |
| R-005 | FINANCIAL | Supplier cost growth breaches funding envelope | Consumption, support, or contract changes drive spend above approved limits. | 4/4/16 | Budget tracking, commercial review, usage reporting | 2/3/6 | Transfer | SRO | In Progress | Add price protections, service credits, and capped usage terms | 2026-07-31 |
| R-006 | FINANCIAL | Scale-up case not approved | Benefits evidence is insufficient to justify wider rollout or future investment. | 4/4/16 | Benefits KPIs in REQ, PMO reporting, pilot measures | 3/4/12 | Treat | SRO | Open | Stand up monthly benefits and cost dashboard with independent validation | 2027-06-30 |
| R-007 | COMPLIANCE | Lawful basis not sustained | A workflow goes live or changes materially without a sufficiently evidenced lawful basis or proportionality assessment. | 4/5/20 | Workflow gating, legal review, privacy review, approved-use catalog | 3/4/12 | Treat | SIRO | In Progress | Complete lawful basis pack and re-approval trigger rules for all live workflows | 2026-08-15 |
| R-008 | COMPLIANCE | Accessibility or transparency duties missed | User-facing or workforce workflows fail accessibility or transparency obligations, blocking approval or use. | 3/4/12 | WCAG and transparency requirements in REQ, review gates | 2/3/6 | Treat | Service Owner | Open | Complete accessibility and transparency assurance checklists before UAT exit | 2026-10-15 |
| R-009 | REPUTATIONAL | Public trust damaged by output failure | Inaccurate, biased, or poorly explained output causes complaints, scrutiny, or media criticism. | 4/5/20 | Human review, bounded scope, comms and complaint pathways | 3/4/12 | Treat | SRO | Open | Publish transparency narrative and incident response playbook for public issues | 2026-11-30 |
| R-010 | REPUTATIONAL | Inspection or audit criticism slows rollout | Oversight bodies conclude the service is insufficiently evidenced or governed, reducing confidence and pace. | 3/4/12 | Audit trail, control pack, reporting evidence | 2/3/6 | Tolerate | SRO | Monitoring | Keep review packs current and rehearse inspection responses quarterly | 2026-09-30 |
| R-011 | TECHNOLOGY | Integration fails provenance controls | Legacy integrations fail to deliver stable, source-bounded, provenance-preserving behavior at live scale. | 5/4/20 | Versioned interfaces, technical spikes, architecture standards | 4/3/12 | Treat | Service Owner | Open | Run end-to-end proving exercise for retrieval, provenance, and fallback | 2026-09-30 |
| R-012 | TECHNOLOGY | Sensitive data exposed through orchestration gap | Weak access boundaries, connector controls, or orchestration logic expose sensitive information or privileged actions. | 4/5/20 | Least privilege, misuse testing, monitoring, secrets controls | 3/4/12 | Treat | CISO | In Progress | Close least-privilege, secret-management, and misuse-testing gaps before live use | 2026-08-31 |
| R-013 | STRATEGIC | Autonomous high-impact use escapes scope | Pressure to introduce autonomous or high-impact public-facing AI use before separate approval creates an unacceptable risk event. | 5/5/25 | Out-of-scope definition, workflow catalog controls, governance veto | 1/3/3 | Terminate | SRO | Accepted | Maintain explicit scope prohibition and block activation in the workflow catalog | 2026-04-30 |

---

## D. Risk Profiles

### Risk R-001: Assurance slippage delays first live release

**Category:** STRATEGIC  
**Status:** In Progress  
**Risk Owner:** SRO  
**Action Owner:** Service Owner

**Risk Description:** Delivery urgency causes workflow scope to move faster than assurance evidence,
creating a mismatch between milestone expectations and safe release readiness.

**Root Cause:** Benefits pressure and milestone commitments are stronger than current assurance
throughput.

**Trigger Events:**

- Overdue legal, privacy, or security actions older than 30 days
- Attempted inclusion of a higher-risk workflow before completion of control evidence
- Pilot-force pressure to expand scope before readiness sign-off

**Consequences if Realized:**

- Go-live slips by 1-2 quarters
- Emergency stop on release decision
- Loss of sponsor and force confidence in delivery planning

**Affected Stakeholders:** SRO, Service Owner, SIRO, CISO, pilot-force leads  
**Related Objectives:** G-1, G-4, G-6

| Assessment | Rating | Justification |
|------------|--------|---------------|
| Inherent Likelihood | 4 - Likely | Scope pressure is already visible in stakeholder conflict analysis |
| Inherent Impact | 5 - Catastrophic | Failure at first release would damage delivery and trust materially |
| Inherent Score | 20 | Critical |

**Existing Controls:** Phased rollout by risk class; architecture and assurance gates; documented
conflict resolution in stakeholder analysis  
**Control Effectiveness:** Adequate  
**Evidence of Effectiveness:** Controls exist in artifact form, but are not yet proven in live use

| Assessment | Rating | Justification |
|------------|--------|---------------|
| Residual Likelihood | 3 - Possible | Phasing reduces probability but pressure remains |
| Residual Impact | 4 - Major | A late-stage slip would still materially affect objectives |
| Residual Score | 12 | Medium |

**Risk Response:** Treat  
**Additional Mitigations Needed:** Assurance dashboard, scope-freeze criteria, no-go thresholds  
**Target Residual Risk:** 9  
**Success Criteria:** No workflow enters live approval with overdue critical assurance actions

---

### Risk R-002: Policy change reshapes programme priorities

**Category:** STRATEGIC  
**Status:** Monitoring  
**Risk Owner:** SRO  
**Action Owner:** Product Manager

**Risk Description:** Sponsor or policy direction changes alter rollout priorities, benefits focus,
or the acceptable sequencing of use cases before scale-up.

**Root Cause:** The programme sits in a politically and operationally visible policy environment.

**Trigger Events:**

- New ministerial or Home Office direction
- Change in national policing priorities
- New oversight recommendations requiring scope change

**Consequences if Realized:**

- Backlog reprioritization
- Delay to currently planned force onboarding
- Rework of benefits or scope assumptions

**Affected Stakeholders:** SRO, Service Owner, Home Office, force leads  
**Related Objectives:** G-5, G-6

| Assessment | Rating | Justification |
|------------|--------|---------------|
| Inherent Likelihood | 3 - Possible | Public-sector policy change is plausible over programme timescales |
| Inherent Impact | 4 - Major | A strategic redirect would alter schedule and investment assumptions |
| Inherent Score | 12 | Medium |

**Existing Controls:** Quarterly sponsor review; modular roadmap; reusable architecture pattern  
**Control Effectiveness:** Adequate  
**Evidence of Effectiveness:** Stakeholder analysis already assumes phased and reusable planning

| Assessment | Rating | Justification |
|------------|--------|---------------|
| Residual Likelihood | 2 - Unlikely | Regular sponsor engagement reduces surprise |
| Residual Impact | 4 - Major | Strategic redirection would still be material |
| Residual Score | 8 | Medium |

**Risk Response:** Tolerate  
**Additional Mitigations Needed:** Scenario planning for alternate scale-up paths  
**Target Residual Risk:** 8  
**Success Criteria:** Roadmap changes absorbed without invalidating first-wave delivery

---

### Risk R-003: Pilot adoption below productivity target

**Category:** OPERATIONAL  
**Status:** In Progress  
**Risk Owner:** Service Owner  
**Action Owner:** Product Manager

**Risk Description:** Users do not adopt the service consistently, or use it in ways that fail to
produce the predicted productivity gains.

**Root Cause:** Weak workflow fit, usability friction, and trust concerns undermine daily use.

**Trigger Events:**

- Weekly active pilot usage remains below 70% of trained cohort
- Rework rate rises above baseline
- Qualitative feedback reports low trust or unclear value

**Consequences if Realized:**

- Benefits case weakens
- Time savings are not realized
- Force leaders lose confidence in further rollout

**Affected Stakeholders:** Frontline users, force leads, Service Owner, finance stakeholders  
**Related Objectives:** G-2, G-6

| Assessment | Rating | Justification |
|------------|--------|---------------|
| Inherent Likelihood | 4 - Likely | Stakeholder analysis highlights trust and workflow fit as live concerns |
| Inherent Impact | 4 - Major | Weak adoption directly threatens benefits and scale-up |
| Inherent Score | 16 | High |

**Existing Controls:** Pilot-first scope, role-based guidance, training assumptions, feedback
capture requirement  
**Control Effectiveness:** Adequate  
**Evidence of Effectiveness:** Controls are specified but not yet validated by usage data

| Assessment | Rating | Justification |
|------------|--------|---------------|
| Residual Likelihood | 3 - Possible | Controlled pilots reduce exposure but do not remove adoption risk |
| Residual Impact | 3 - Moderate | Limited pilot scale contains the immediate effect |
| Residual Score | 9 | Medium |

**Risk Response:** Treat  
**Additional Mitigations Needed:** Workflow-fit validation, weekly pilot adoption review, user
support clinics  
**Target Residual Risk:** 6  
**Success Criteria:** Pilot adoption and usefulness scores meet target by month two of live pilot

---

### Risk R-004: Support and onboarding capacity lags force rollout

**Category:** OPERATIONAL  
**Status:** Open  
**Risk Owner:** Service Owner  
**Action Owner:** Service Operations Lead

**Risk Description:** The service team cannot onboard forces or support live users at the planned
pace, creating operational instability or delayed rollout.

**Root Cause:** Central support capacity and force-local readiness are both constrained.

**Trigger Events:**

- Onboarding tasks slip by more than 20 working days
- Operations headcount remains unfilled at readiness gate
- Repeated pilot incidents exceed support-team capacity

**Consequences if Realized:**

- Force onboarding is delayed
- User confidence declines
- Known issues remain unresolved longer than acceptable

**Affected Stakeholders:** Service operations, force leads, Service Owner, SRO  
**Related Objectives:** G-1, G-5

| Assessment | Rating | Justification |
|------------|--------|---------------|
| Inherent Likelihood | 4 - Likely | Stakeholder analysis flags onboarding and support as prerequisites for trust |
| Inherent Impact | 4 - Major | Live support failure would block scaling and damage adoption |
| Inherent Score | 16 | High |

**Existing Controls:** Onboarding pack, runbook requirements, readiness reviews  
**Control Effectiveness:** Adequate  
**Evidence of Effectiveness:** Design-stage controls only; no live support evidence yet

| Assessment | Rating | Justification |
|------------|--------|---------------|
| Residual Likelihood | 3 - Possible | Planning helps, but staffing risk remains |
| Residual Impact | 3 - Moderate | Early rollout scope can still be contained |
| Residual Score | 9 | Medium |

**Risk Response:** Treat  
**Additional Mitigations Needed:** Named support rota, onboarding capacity plan, force readiness
checklist  
**Target Residual Risk:** 6  
**Success Criteria:** Each onboarding wave starts with signed support and readiness capacity

---

### Risk R-005: Supplier cost growth breaches funding envelope

**Category:** FINANCIAL  
**Status:** In Progress  
**Risk Owner:** SRO  
**Action Owner:** Commercial Lead

**Risk Description:** Usage growth, support cost, or contract change pushes spend above the initial
funding envelope before the scale-up case is approved.

**Root Cause:** Variable consumption models and supplier dependency create cost volatility.

**Trigger Events:**

- Monthly spend rises more than 10% above forecast for two consecutive periods
- Supplier proposes pricing or scope change
- Pilot growth occurs without matching commercial controls

**Consequences if Realized:**

- Budget pressure on the initial phase
- Reduced confidence in value-for-money
- Delayed or constrained rollout decisions

**Affected Stakeholders:** SRO, finance, commercial, Service Owner  
**Related Objectives:** G-2, G-6

| Assessment | Rating | Justification |
|------------|--------|---------------|
| Inherent Likelihood | 4 - Likely | Requirements show third-party and support costs are material |
| Inherent Impact | 4 - Major | Material overspend would change approval appetite |
| Inherent Score | 16 | High |

**Existing Controls:** Indicative budget, usage reporting, procurement review, cost KPIs  
**Control Effectiveness:** Adequate  
**Evidence of Effectiveness:** Budget model exists but no live cost baseline yet

| Assessment | Rating | Justification |
|------------|--------|---------------|
| Residual Likelihood | 2 - Unlikely | Commercial controls can materially reduce exposure |
| Residual Impact | 3 - Moderate | Overspend remains manageable if detected early |
| Residual Score | 6 | Medium |

**Risk Response:** Transfer  
**Additional Mitigations Needed:** Price caps, service credits, contractual change controls,
consumption guardrails  
**Target Residual Risk:** 4  
**Success Criteria:** Monthly spend remains within 5% of approved forecast after controls apply

---

### Risk R-006: Scale-up case not approved

**Category:** FINANCIAL  
**Status:** Open  
**Risk Owner:** SRO  
**Action Owner:** PMO Lead

**Risk Description:** The programme cannot evidence enough operational value, quality stability, and
public-interest control to secure scale-up investment approval.

**Root Cause:** Benefits capture and reporting are weaker than delivery pressure requires.

**Trigger Events:**

- Benefits baseline not agreed before pilot launch
- Benefits data completeness below 90%
- Reviewers reject the scale-up pack as insufficiently evidenced

**Consequences if Realized:**

- No approval for wider rollout
- Early work remains isolated to pilots
- Additional scrutiny of programme value and strategy

**Affected Stakeholders:** SRO, finance, Home Office, force leads  
**Related Objectives:** G-6, O-6

| Assessment | Rating | Justification |
|------------|--------|---------------|
| Inherent Likelihood | 4 - Likely | Stakeholder analysis already identifies benefits proof as a major concern |
| Inherent Impact | 4 - Major | Failure to secure approval constrains the programme materially |
| Inherent Score | 16 | High |

**Existing Controls:** Requirements KPIs, benefits register expectation, pilot metric plan  
**Control Effectiveness:** Weak  
**Evidence of Effectiveness:** Control intent exists, but no measured pilot evidence yet

| Assessment | Rating | Justification |
|------------|--------|---------------|
| Residual Likelihood | 3 - Possible | Active management can improve outcomes, but evidence risk remains |
| Residual Impact | 4 - Major | Scale-up failure would still be a significant strategic setback |
| Residual Score | 12 | Medium |

**Risk Response:** Treat  
**Additional Mitigations Needed:** Monthly validated benefits dashboard, independent finance
assurance, stronger baseline capture  
**Target Residual Risk:** 9  
**Success Criteria:** Scale-up pack accepted for review with no major evidence gaps

---

### Risk R-007: Lawful basis not sustained

**Category:** COMPLIANCE  
**Status:** In Progress  
**Risk Owner:** SIRO  
**Action Owner:** Legal Lead

**Risk Description:** A workflow enters or remains in live use without a clearly evidenced lawful
basis, proportionality case, or re-approval after material change.

**Root Cause:** Workflow change pace can outstrip legal and privacy reassessment discipline.

**Trigger Events:**

- A workflow changes data use or target user group without formal review
- DPIA or legal advice is incomplete at the release gate
- A complaint or challenge reveals missing justification

**Consequences if Realized:**

- Live service suspension
- Regulatory scrutiny or internal risk escalation
- Loss of trust in governance

**Affected Stakeholders:** SIRO, legal, SRO, Service Owner, public-interest groups  
**Related Objectives:** G-1, G-3, G-4

| Assessment | Rating | Justification |
|------------|--------|---------------|
| Inherent Likelihood | 4 - Likely | Multiple workflow and data changes are expected through pilot phases |
| Inherent Impact | 5 - Catastrophic | Unlawful live use would threaten continuation of the programme |
| Inherent Score | 20 | Critical |

**Existing Controls:** Approved workflow catalog, legal review gate, privacy review gate,
requirements controls for lawfulness and minimization  
**Control Effectiveness:** Adequate  
**Evidence of Effectiveness:** Controls are explicit in PRIN, STKE, and REQ, but not yet proven in
operation

| Assessment | Rating | Justification |
|------------|--------|---------------|
| Residual Likelihood | 3 - Possible | Re-approval discipline still depends on operational rigor |
| Residual Impact | 4 - Major | Consequences remain severe if control failure occurs |
| Residual Score | 12 | Medium |

**Risk Response:** Treat  
**Additional Mitigations Needed:** Release checklist with legal sign-off, change-triggered
reassessment, monthly lawful-basis audit  
**Target Residual Risk:** 8  
**Success Criteria:** 100% of live workflows have current legal and privacy approval records

---

### Risk R-008: Accessibility or transparency duties missed

**Category:** COMPLIANCE  
**Status:** Open  
**Risk Owner:** Service Owner  
**Action Owner:** Product Manager

**Risk Description:** The service fails accessibility or transparency obligations for in-scope
workflows, delaying approval or creating avoidable challenge.

**Root Cause:** Accessibility and transparency work is often deferred unless explicitly managed.

**Trigger Events:**

- Accessibility defects remain open at UAT exit
- Public-facing descriptions are not updated after workflow change
- User testing reveals barriers for assisted technology users

**Consequences if Realized:**

- Release delay
- Remediation cost and rework
- Reduced confidence from users and oversight bodies

**Affected Stakeholders:** Service Owner, users, public-interest stakeholders, oversight reviewers  
**Related Objectives:** G-2, G-6

| Assessment | Rating | Justification |
|------------|--------|---------------|
| Inherent Likelihood | 3 - Possible | The programme has not yet produced design and UAT evidence |
| Inherent Impact | 4 - Major | Non-compliance could block or delay use in public-sector context |
| Inherent Score | 12 | Medium |

**Existing Controls:** Accessibility and transparency requirements in REQ; stakeholder expectation
for public accountability  
**Control Effectiveness:** Adequate  
**Evidence of Effectiveness:** Controls are defined but not yet tested in build

| Assessment | Rating | Justification |
|------------|--------|---------------|
| Residual Likelihood | 2 - Unlikely | Early requirements reduce surprise if followed |
| Residual Impact | 3 - Moderate | Impact remains manageable with timely remediation |
| Residual Score | 6 | Medium |

**Risk Response:** Treat  
**Additional Mitigations Needed:** Accessibility test plan, transparency record owner, release
checklist item  
**Target Residual Risk:** 4  
**Success Criteria:** No priority accessibility or transparency blockers remain at go-live review

---

### Risk R-009: Public trust damaged by output failure

**Category:** REPUTATIONAL  
**Status:** Open  
**Risk Owner:** SRO  
**Action Owner:** Communications Lead

**Risk Description:** A high-profile inaccurate, biased, or poorly explained output causes public
complaint, media scrutiny, or loss of confidence in the programme.

**Root Cause:** Public understanding is fragile and trust is easily damaged by isolated high-profile
failures.

**Trigger Events:**

- A public-facing or sensitive workflow produces a visible error
- Complaints trend rises following launch
- Oversight or media scrutiny highlights lack of explanation

**Consequences if Realized:**

- Pause or restriction of rollout
- Increased parliamentary or oversight scrutiny
- Reputational damage for participating forces and sponsors

**Affected Stakeholders:** Public, SRO, Home Office, force leads, Service Owner  
**Related Objectives:** G-4, G-6

| Assessment | Rating | Justification |
|------------|--------|---------------|
| Inherent Likelihood | 4 - Likely | Public scrutiny risk is elevated in UK policing contexts |
| Inherent Impact | 5 - Catastrophic | Trust loss would materially affect the programme's future |
| Inherent Score | 20 | Critical |

**Existing Controls:** Human review; out-of-scope restriction on unreviewed high-risk public use;
requirements for transparency and complaints handling  
**Control Effectiveness:** Adequate  
**Evidence of Effectiveness:** Controls are sensible but untested in real incidents

| Assessment | Rating | Justification |
|------------|--------|---------------|
| Residual Likelihood | 3 - Possible | Bounded scope reduces probability but cannot remove it |
| Residual Impact | 4 - Major | A single incident could still materially damage confidence |
| Residual Score | 12 | Medium |

**Risk Response:** Treat  
**Additional Mitigations Needed:** Public issue playbook, sentiment and complaints monitoring,
incident communications protocol  
**Target Residual Risk:** 8  
**Success Criteria:** No sustained increase in substantiated AI-related complaints during pilot

---

### Risk R-010: Inspection or audit criticism slows rollout

**Category:** REPUTATIONAL  
**Status:** Monitoring  
**Risk Owner:** SRO  
**Action Owner:** Enterprise Architecture Lead

**Risk Description:** Oversight, inspection, or audit bodies conclude that governance evidence is
insufficient, slowing rollout or reducing confidence.

**Root Cause:** Reviewers require consistent evidence across forces and workflows.

**Trigger Events:**

- Assurance packs are inconsistent across forces
- Review requests cannot be met quickly with evidence
- Audit findings cite poor traceability or control documentation

**Consequences if Realized:**

- Rollout slowed pending remediation
- Additional management attention and rework
- Lower sponsor confidence in scale-up readiness

**Affected Stakeholders:** SRO, oversight bodies, Service Owner, Enterprise Architecture Lead  
**Related Objectives:** G-5, G-6

| Assessment | Rating | Justification |
|------------|--------|---------------|
| Inherent Likelihood | 3 - Possible | Oversight interest is expected but not certain to become adverse |
| Inherent Impact | 4 - Major | Adverse findings would materially slow rollout |
| Inherent Score | 12 | Medium |

**Existing Controls:** Control pack requirements; auditability and reporting requirements; reusable
onboarding evidence  
**Control Effectiveness:** Adequate  
**Evidence of Effectiveness:** Good alignment in artifacts, but no inspection evidence yet

| Assessment | Rating | Justification |
|------------|--------|---------------|
| Residual Likelihood | 2 - Unlikely | Consistent evidence can reduce this risk substantially |
| Residual Impact | 3 - Moderate | Effects remain manageable if detected early |
| Residual Score | 6 | Medium |

**Risk Response:** Tolerate  
**Additional Mitigations Needed:** Quarterly evidence-pack rehearsal and review  
**Target Residual Risk:** 6  
**Success Criteria:** Review requests can be met from a current and complete evidence baseline

---

### Risk R-011: Integration fails provenance controls

**Category:** TECHNOLOGY  
**Status:** Open  
**Risk Owner:** Service Owner  
**Action Owner:** Enterprise Architecture Lead

**Risk Description:** Legacy or external system integration fails to preserve provenance, timeliness,
or reliable bounded retrieval behavior at live scale.

**Root Cause:** Existing systems were not designed for AI-assisted provenance and retrieval needs.

**Trigger Events:**

- Integration testing shows missing or inconsistent source references
- Retrieval latency or error rate exceeds design assumptions
- Case system or knowledge source metadata is incomplete

**Consequences if Realized:**

- Sensitive workflows cannot go live safely
- Provenance and audit requirements are weakened
- Rework is required across interface design

**Affected Stakeholders:** Service Owner, investigations leads, Enterprise Architecture Lead, users  
**Related Objectives:** G-2, G-3, G-5

| Assessment | Rating | Justification |
|------------|--------|---------------|
| Inherent Likelihood | 5 - Almost Certain | Legacy integration and provenance complexity are core technical challenges |
| Inherent Impact | 4 - Major | Failure here blocks multiple objectives directly |
| Inherent Score | 20 | Critical |

**Existing Controls:** Versioned interface requirements; published control-pack approach; data and
integration requirements in REQ  
**Control Effectiveness:** Adequate  
**Evidence of Effectiveness:** Strong design direction, no live proving evidence yet

| Assessment | Rating | Justification |
|------------|--------|---------------|
| Residual Likelihood | 4 - Likely | Technical proving is still outstanding |
| Residual Impact | 3 - Moderate | Scope phasing reduces immediate blast radius |
| Residual Score | 12 | Medium |

**Risk Response:** Treat  
**Additional Mitigations Needed:** End-to-end technical proving, interface contract validation,
fallback rehearsal  
**Target Residual Risk:** 9  
**Success Criteria:** Provenance and fallback tests pass for all first-wave integrations

---

### Risk R-012: Sensitive data exposed through orchestration gap

**Category:** TECHNOLOGY  
**Status:** In Progress  
**Risk Owner:** CISO  
**Action Owner:** Security Architect

**Risk Description:** Weak access boundaries, connector permissions, or orchestration logic expose
sensitive policing data or privileged actions to unauthorized paths.

**Root Cause:** GenAI orchestration layers increase attack surface and permission complexity.

**Trigger Events:**

- Penetration or misuse testing identifies privileged bypass
- Service identity retains broad unnecessary access
- Monitoring reveals anomalous prompt or export activity

**Consequences if Realized:**

- Material security incident
- Regulatory or legal escalation
- Service suspension and reputational damage

**Affected Stakeholders:** CISO, SIRO, SRO, users, public-interest stakeholders  
**Related Objectives:** G-4, G-6

| Assessment | Rating | Justification |
|------------|--------|---------------|
| Inherent Likelihood | 4 - Likely | Security complexity is high and controls are not yet proven |
| Inherent Impact | 5 - Catastrophic | A sensitive-data exposure event would be severe |
| Inherent Score | 20 | Critical |

**Existing Controls:** Least-privilege requirements; secrets management; AI-specific misuse testing;
security monitoring integration  
**Control Effectiveness:** Adequate  
**Evidence of Effectiveness:** Control pattern is strong, but penetration and live validation are
still pending

| Assessment | Rating | Justification |
|------------|--------|---------------|
| Residual Likelihood | 3 - Possible | Good controls reduce probability if executed rigorously |
| Residual Impact | 4 - Major | Impact remains severe if a failure occurs |
| Residual Score | 12 | Medium |

**Risk Response:** Treat  
**Additional Mitigations Needed:** Close privileged access gaps, complete misuse testing, validate
alerting and containment  
**Target Residual Risk:** 8  
**Success Criteria:** No critical security findings remain open at go-live decision point

---

### Risk R-013: Autonomous high-impact use escapes scope

**Category:** STRATEGIC  
**Status:** Accepted  
**Risk Owner:** SRO  
**Action Owner:** Service Owner

**Risk Description:** Pressure emerges to introduce autonomous or high-impact public-facing AI use
before separate approval and assurance are in place.

**Root Cause:** External pressure for visible innovation may exceed the programme's approved scope.

**Trigger Events:**

- Requests to enable automated decisioning or unreviewed public responses
- Sponsor pressure to expand beyond bounded assistive use
- Workarounds to bypass workflow classification controls

**Consequences if Realized:**

- Unacceptable legal, operational, and public-trust risk
- Immediate governance intervention
- Potential project reset

**Affected Stakeholders:** SRO, Service Owner, SIRO, public-interest stakeholders  
**Related Objectives:** G-1, G-4, G-6

| Assessment | Rating | Justification |
|------------|--------|---------------|
| Inherent Likelihood | 5 - Almost Certain | External pressure for expanded use is foreseeable |
| Inherent Impact | 5 - Catastrophic | Premature autonomous release would exceed safe risk tolerance |
| Inherent Score | 25 | Critical |

**Existing Controls:** Out-of-scope definition in REQ; workflow catalog controls; governance veto  
**Control Effectiveness:** Strong  
**Evidence of Effectiveness:** The activity is explicitly excluded from current requirements and
workflow policy

| Assessment | Rating | Justification |
|------------|--------|---------------|
| Residual Likelihood | 1 - Rare | The activity is blocked by explicit scope and governance decisions |
| Residual Impact | 3 - Moderate | Residual exposure remains through informal pressure only |
| Residual Score | 3 | Low |

**Risk Response:** Terminate  
**Additional Mitigations Needed:** Keep the prohibition explicit in all release and onboarding
materials  
**Target Residual Risk:** 3  
**Success Criteria:** No autonomous high-impact workflow is enabled in the current programme phase

---

## E. Risk by Category Analysis

### STRATEGIC

- **Number of risks**: 3
- **Average inherent score**: 19.0
- **Average residual score**: 7.7
- **Control effectiveness**: 59% reduction
- **Key themes**: scope discipline, policy stability, explicit exclusion of unacceptable use

### OPERATIONAL

- **Number of risks**: 2
- **Average inherent score**: 16.0
- **Average residual score**: 9.0
- **Control effectiveness**: 44% reduction
- **Key themes**: user adoption, onboarding readiness, support capacity

### FINANCIAL

- **Number of risks**: 2
- **Average inherent score**: 16.0
- **Average residual score**: 9.0
- **Control effectiveness**: 44% reduction
- **Key themes**: cost control, benefits proof, scale-up investment confidence

### COMPLIANCE

- **Number of risks**: 2
- **Average inherent score**: 16.0
- **Average residual score**: 9.0
- **Control effectiveness**: 44% reduction
- **Key themes**: lawful basis, accessibility, transparency, re-approval discipline

### REPUTATIONAL

- **Number of risks**: 2
- **Average inherent score**: 16.0
- **Average residual score**: 9.0
- **Control effectiveness**: 44% reduction
- **Key themes**: public trust, complaints, audit and inspection scrutiny

### TECHNOLOGY

- **Number of risks**: 2
- **Average inherent score**: 20.0
- **Average residual score**: 12.0
- **Control effectiveness**: 40% reduction
- **Key themes**: provenance-preserving integration, orchestration security, live technical proof

---

## F. Risk Ownership Matrix

| Stakeholder | Owned Risks | Critical / High Inherent Risks | Notes |
|-------------|-------------|-------------------------------|-------|
| SRO | R-001, R-002, R-005, R-006, R-009, R-010, R-013 | 5 Critical / 1 High | Heavy concentration of strategic, financial, and reputational exposure |
| Service Owner | R-003, R-004, R-008, R-011 | 2 High / 1 Critical | Owns adoption, operational readiness, and integration risk |
| SIRO | R-007 | 1 Critical | Sole owner for the highest compliance risk |
| CISO | R-012 | 1 Critical | Sole owner for the highest security-driven technology risk |

---

## G. 4Ts Response Summary

| Response | Count | % | Key Examples |
|----------|-------|---|--------------|
| Tolerate | 2 | 15% | R-002, R-010 |
| Treat | 9 | 69% | R-001, R-003, R-006, R-007, R-009, R-011, R-012 |
| Transfer | 1 | 8% | R-005 |
| Terminate | 1 | 8% | R-013 |

---

## H. Risk Appetite Compliance

| Category | Provisional Threshold | Risks Within | Risks Exceeding | Action Required |
|----------|-----------------------|--------------|-----------------|-----------------|
| STRATEGIC | 12 | 3 | 0 | Monitor through Project Board |
| OPERATIONAL | 9 | 2 | 0 | Maintain monthly review |
| FINANCIAL | 9 | 1 | 1 | Escalate R-006 to Project Board |
| COMPLIANCE | 9 | 1 | 1 | Escalate R-007 to SIRO and Project Board |
| REPUTATIONAL | 9 | 1 | 1 | Escalate R-009 to SRO and Project Board |
| TECHNOLOGY | 9 | 0 | 2 | Escalate R-011 and R-012 immediately |

**Assessment Note:** This section uses a provisional threshold because no formal risk appetite
statement was supplied. Approval authorities should confirm or replace these thresholds.

---

## I. Action Plan

| Priority | Action | Risk(s) Addressed | Owner | Due Date | Status |
|----------|--------|-------------------|-------|----------|--------|
| 1 | Freeze any high-risk workflow expansion until assurance dashboard is green | R-001, R-007, R-009, R-013 | SRO | 2026-04-30 | Not Started |
| 2 | Complete lawful basis, DPIA trigger, and workflow re-approval pack for first-wave live workflows | R-007 | SIRO | 2026-08-15 | In Progress |
| 3 | Run end-to-end technical proving for retrieval, provenance, and fallback across first-wave integrations | R-011, R-003 | Service Owner | 2026-08-31 | Not Started |
| 4 | Close least-privilege, secret-management, and misuse-testing gaps before release | R-012 | CISO | 2026-08-31 | In Progress |
| 5 | Establish monthly benefits, quality, and cost dashboard with independent validation | R-003, R-005, R-006 | SRO | 2026-06-30 | Not Started |
| 6 | Put contractual price protections and usage guardrails in place | R-005 | SRO | 2026-07-31 | In Progress |
| 7 | Publish accessibility, transparency, and public-issue response pack | R-008, R-009, R-010 | Service Owner | 2026-09-30 | Not Started |
| 8 | Confirm named support capacity and onboarding readiness for each pilot force | R-004 | Service Owner | 2026-09-15 | Not Started |

---

## J. Monitoring and Review Framework

- **Review Frequency**:
  - Monthly for all risks
  - Additional fortnightly review for risks with residual score 12
  - Immediate review after any incident, complaint spike, or material control failure
- **Escalation Criteria**:
  - Any residual score increase of 4 or more points
  - Any new residual High or Critical risk
  - Any risk exceeding provisional threshold for two consecutive review cycles
  - Any control failure affecting lawfulness, security, or public confidence
- **Reporting Requirements**:
  - Monthly: Full risk register to Project Board
  - Fortnightly: Escalated risks to SRO, SIRO, CISO, and Service Owner
  - Quarterly: Risk trend summary for sponsor and oversight review pack
- **Next Review Date**: 2026-04-06
- **Risk Register Owner**: Service Owner

---

## K. Integration with SOBC

This risk register should feed directly into a future SOBC as follows:

- **Strategic Case**: R-001, R-002, R-009, and R-013 explain urgency, political sensitivity, and
  why bounded scope matters.
- **Economic Case**: R-005 and R-006 inform cost sensitivity, benefits certainty, and optimism-bias
  considerations.
- **Commercial Case**: R-005 and R-012 inform supplier controls, exit strategy, and contracting
  protections.
- **Management Case Part E**: All risks, owners, actions, and review cadence flow directly into the
  formal risk-management section.

---

## Orange Book Compliance Checklist

- Governance and Leadership: All 13 risks have named owners from accountable stakeholder roles.
- Integration: Risks are linked to stakeholder goals, requirements, and architecture principles.
- Collaboration: Risks are derived from stakeholder conflict analysis, requirements, and governance
  concerns.
- Risk Processes: Each risk has inherent and residual assessment, controls, response, owner,
  actions, and review cadence.
- Continual Improvement: The register includes escalation criteria, action plan, and review
  framework for ongoing refinement.

---

## External References

| Document | Type | Source | Key Extractions | Path |
|----------|------|--------|-----------------|------|
| ARC-001-STKE-v1.0 | Stakeholder analysis | Local project artifact | Risk owners, conflict analysis, stakeholder drivers, RACI escalation structure | projects/001-genai-for-uk-policing/ARC-001-STKE-v1.0.md |
| ARC-001-REQ-v1.0 | Requirements baseline | Local project artifact | Scope boundaries, NFRs, control expectations, integration and data requirements | projects/001-genai-for-uk-policing/ARC-001-REQ-v1.0.md |
| ARC-000-PRIN-v1.0 | Architecture principles | Local project artifact | Lawfulness, accountability, resilience, interoperability, privacy, auditability | projects/000-global/ARC-000-PRIN-v1.0.md |
| No formal risk appetite statement provided | N/A | Local project context | Provisional thresholds used for escalation only in this draft | projects/000-global/policies/ |

---

**Generated by**: ArcKit `$arckit-risk` command
**Generated on**: 2026-03-07
**ArcKit Version**: 4.0.0
**Project**: GenAI for UK Policing (Project 001)
**AI Model**: GPT-5 Codex
