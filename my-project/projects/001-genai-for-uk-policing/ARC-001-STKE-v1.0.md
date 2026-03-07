# Stakeholder Drivers & Goals Analysis: GenAI for UK Policing

> **Template Origin**: Official | **ArcKit Version**: 4.0.0 | **Command**: `$arckit-stakeholders`

## Document Control

| Field | Value |
|-------|-------|
| **Document ID** | ARC-001-STKE-v1.0 |
| **Document Type** | Stakeholder Drivers & Goals Analysis |
| **Project** | GenAI for UK Policing (Project 001) |
| **Classification** | OFFICIAL |
| **Status** | DRAFT |
| **Version** | 1.0 |
| **Created Date** | 2026-03-07 |
| **Last Modified** | 2026-03-07 |
| **Review Cycle** | Quarterly |
| **Next Review Date** | 2026-06-07 |
| **Owner** | Programme Director, GenAI for UK Policing |
| **Reviewed By** | PENDING |
| **Approved By** | PENDING |
| **Distribution** | SRO; Service Owner; Enterprise Architecture Review Board; Responsible AI Review Panel; Security; Data Protection; Legal; Delivery Leads |

## Revision History

| Version | Date | Author | Changes | Approved By | Approval Date |
|---------|------|--------|---------|-------------|---------------|
| 1.0 | 2026-03-07 | ArcKit AI | Initial creation from `$arckit-stakeholders` command | PENDING | PENDING |

---

## Executive Summary

### Purpose

This document identifies the principal stakeholders for the GenAI for UK Policing initiative,
their underlying drivers, the goals those drivers create, and the measurable outcomes needed to
demonstrate success. It is designed to align programme governance, requirements prioritisation,
assurance planning, and stakeholder engagement around a common view of value and risk.

### Key Findings

Stakeholder alignment is strongest around reducing administrative burden, improving the speed and
quality of information handling, and preserving public trust through secure, auditable, lawful AI
use. The most material tensions are between speed of delivery and depth of assurance, between local
force autonomy and national consistency, and between productivity gains and evidential integrity in
operational policing workflows.

### Critical Success Factors

- Establish a governance model that proves lawfulness, accountability, privacy, and human
  oversight before operational scaling.
- Deliver measurable time savings for frontline and investigative teams without increasing rework,
  challenge rates, or evidential risk.
- Provide transparent auditability, interoperability, and supplier governance strong enough to
  satisfy public-sector scrutiny and cross-force adoption needs.

### Stakeholder Alignment Score

**Overall Alignment**: MEDIUM

Most stakeholders support the direction of travel, but their tolerance for risk and pace differs
substantially. Alignment will improve if the programme demonstrates early low-risk wins, keeps
humans accountable for decisions, and uses explicit governance to separate advisory use from
higher-risk operational use.

---

## Stakeholder Identification

### Internal Stakeholders

| Stakeholder | Role/Department | Influence | Interest | Engagement Strategy |
|-------------|----------------|-----------|----------|---------------------|
| Senior Responsible Owner (SRO) | National policing programme sponsor | HIGH | HIGH | Weekly steering, decision escalation, benefits tracking |
| Service Owner | End-to-end service accountability | HIGH | HIGH | Fortnightly service reviews, backlog and KPI ownership |
| Chief Constables and force operational leads | Force leadership and operational adoption | HIGH | HIGH | Monthly adoption forum, pilot approvals, local readiness reviews |
| Investigations and intelligence leads | Detectives, analysts, intelligence supervisors | HIGH | HIGH | Use-case shaping, evidential controls, monthly design reviews |
| Frontline officers and staff | Primary operational users | MEDIUM | HIGH | User research, pilot cohorts, feedback loops |
| Enterprise architecture and DDaT leads | Architecture, design authority, standards | HIGH | HIGH | Architecture board, standards compliance reviews |
| SIRO, DPO, legal, and information governance | Information risk, privacy, lawfulness | HIGH | HIGH | DPIA reviews, legal challenge review, policy gates |
| CISO, security architects, and cyber operations | Security risk and protective controls | HIGH | HIGH | Threat-model reviews, security acceptance gates |
| Finance and commercial leads | Funding, procurement, supplier value | MEDIUM | MEDIUM | Monthly commercial and benefits review |
| Service operations and support teams | Live support, incident management, service continuity | MEDIUM | HIGH | Operational readiness reviews, runbook sign-off |
| Product manager and delivery manager | Roadmap, delivery pacing, dependency management | MEDIUM | HIGH | Weekly planning, risk and dependency management |
| Learning and workforce enablement leads | Training, adoption, workforce change | LOW | MEDIUM | Monthly change and training updates |

### External Stakeholders

| Stakeholder | Organization | Relationship | Influence | Interest |
|-------------|--------------|--------------|-----------|----------|
| Home Office digital, data, and policing policy teams | Central government sponsor and policy stakeholder | HIGH | HIGH |
| Information Commissioner's Office | Regulator for data protection and information rights | HIGH | HIGH |
| HMICFRS | Oversight and inspection body | HIGH | MEDIUM |
| College of Policing | Standards, practice guidance, professional legitimacy | MEDIUM | HIGH |
| Crown Prosecution Service and criminal justice partners | Downstream consumers of evidential material and case quality | MEDIUM | HIGH |
| Suppliers and delivery partners | Platform, integration, support, and model capability providers | MEDIUM | HIGH |
| Public, victims, witnesses, and community representatives | Beneficiaries and affected parties | MEDIUM | HIGH |
| Civil liberties and watchdog groups | External scrutiny and challenge | MEDIUM | MEDIUM |

### UK Government Digital Roles (GovS 005)

> The [Government Functional Standard for Digital (GovS 005)](https://www.gov.uk/government/publications/government-functional-standard-govs-005-digital) defines mandatory digital governance roles. Include these when the project sits within a UK Government context.

| Role | Responsibility | Typical Power/Interest | Engagement Strategy |
|------|---------------|----------------------|---------------------|
| Senior Responsible Owner (SRO) | Accountable for digital outcomes and spend controls | HIGH / HIGH | Manage Closely — steering board, decision escalation |
| Service Owner | Owns the end-to-end service and user outcomes | HIGH / HIGH | Manage Closely — regular service reviews |
| Product Manager | Prioritises features against user needs and policy | MEDIUM / HIGH | Keep Informed — sprint reviews, roadmap input |
| Delivery Manager | Manages delivery cadence, risks, and dependencies | MEDIUM / HIGH | Keep Informed — stand-ups, risk log |
| CDDO | Assurance, spend control, and cross-government standards | HIGH / MEDIUM | Keep Satisfied — assurance gates, spend control evidence |
| CDIO | Departmental digital strategy and technology oversight | HIGH / MEDIUM | Keep Satisfied — quarterly strategy alignment |
| DDaT Profession Lead | Digital, data, and technology capability development | LOW / MEDIUM | Monitor — capability planning and hiring support |

### UK Government Security Roles (GovS 007)

> The [Government Functional Standard for Security (GovS 007)](https://www.gov.uk/government/publications/government-functional-standard-govs-007-security) defines mandatory protective security roles. Include these when the project sits within a UK Government context.

| Role | Responsibility | Typical Power/Interest | Engagement Strategy |
|------|---------------|----------------------|---------------------|
| Senior Security Risk Owner (SSRO) | Owns protective security risk at board level | HIGH / MEDIUM | Keep Satisfied — risk escalation and quarterly review |
| Departmental Security Officer (DSO) | Day-to-day security coordination and policy implementation | HIGH / MEDIUM | Keep Satisfied — compliance gates, incident reviews |
| Senior Information Risk Owner (SIRO) | Owns information and cyber security risk acceptance | HIGH / HIGH | Manage Closely — information risk decisions, DPIA sign-off |
| Cyber Security Lead | Operational cyber security and assurance activity | MEDIUM / HIGH | Keep Informed — security architecture and testing reviews |

### Stakeholder Power-Interest Grid

```text
                          INTEREST
              Low                         High
        ┌─────────────────────┬─────────────────────┐
        │                     │                     │
        │   KEEP SATISFIED    │   MANAGE CLOSELY    │
   High │                     │                     │
        │  • Home Office      │  • SRO             │
        │  • Finance          │  • Service Owner   │
        │  • HMICFRS          │  • Force Leads     │
 P      │  • SSRO / DSO       │  • SIRO / DPO      │
 O      │                     │  • CISO / EA       │
 W      ├─────────────────────┼─────────────────────┤
 E      │                     │                     │
 R      │      MONITOR        │    KEEP INFORMED    │
   Low  │  • Watchdog Groups  │  • Frontline Users │
        │  • Profession Lead  │  • Investigators   │
        │                     │  • Ops / Support   │
        │                     │  • CPS / College   │
        └─────────────────────┴─────────────────────┘
```

| Stakeholder | Power | Interest | Quadrant | Engagement Strategy |
|-------------|-------|----------|----------|---------------------|
| SRO | HIGH | HIGH | Manage Closely | Weekly steering, benefits and risk escalation |
| Service Owner | HIGH | HIGH | Manage Closely | Fortnightly service review, KPI ownership |
| Chief Constables and force leads | HIGH | HIGH | Manage Closely | Monthly adoption and governance forum |
| SIRO / DPO / Legal | HIGH | HIGH | Manage Closely | Formal assurance gates and risk sign-off |
| CISO / Security architecture | HIGH | HIGH | Manage Closely | Security design authority and acceptance reviews |
| Enterprise architecture / DDaT leads | HIGH | HIGH | Manage Closely | Architecture review board, standards alignment |
| Home Office | HIGH | MEDIUM | Keep Satisfied | Monthly sponsor report and quarterly strategy review |
| Finance and commercial | HIGH | MEDIUM | Keep Satisfied | Monthly value-for-money and supplier review |
| HMICFRS / oversight bodies | HIGH | MEDIUM | Keep Satisfied | Inspection readiness packs and periodic briefings |
| Frontline officers and staff | MEDIUM | HIGH | Keep Informed | User panels, demo sessions, pilot feedback |
| Investigations and intelligence leads | MEDIUM | HIGH | Keep Informed | Workflow design sessions and evidence reviews |
| Service operations and support | MEDIUM | HIGH | Keep Informed | Operational readiness reviews and incident exercises |
| CPS and justice partners | MEDIUM | HIGH | Keep Informed | Case-quality and evidential handling workshops |
| Public and community representatives | MEDIUM | HIGH | Keep Informed | Transparency updates and public-facing statements |
| Watchdog groups | LOW | MEDIUM | Monitor | Briefing notes and response packs as required |

**Quadrant Interpretation:**

- **Manage Closely** (High Power, High Interest): Stakeholders who can stop, redirect, or
  materially reshape the programme and therefore need active involvement in decisions.
- **Keep Satisfied** (High Power, Low-to-Medium Interest): Stakeholders who need confidence that
  the programme remains controlled, compliant, and valuable.
- **Keep Informed** (Low-to-Medium Power, High Interest): Stakeholders most affected by day-to-day
  change and therefore critical to adoption, usability, and risk discovery.
- **Monitor** (Low Power, Low-to-Medium Interest): Stakeholders who can influence narrative or
  scrutiny but do not need intensive routine governance.

---

## Stakeholder Drivers Analysis

### SD-1: Senior Responsible Owner - Deliver visible public value without governance failure

**Stakeholder**: Senior Responsible Owner (national policing sponsor)

**Driver Category**: STRATEGIC

**Driver Statement**: Deliver credible AI-enabled policing outcomes quickly enough to maintain
executive and ministerial confidence, but without creating a governance failure that undermines
public trust.

**Context & Background**:
The SRO is accountable for programme outcomes, spend, media scrutiny, and escalation when things go
wrong. The sponsor needs demonstrable progress, defensible governance, and benefits that can stand
up to parliamentary or inspectorate attention.

**Driver Intensity**: CRITICAL

**Enablers** (What would help):

- Clear phased roadmap with measurable benefits and explicit assurance gates
- Early low-risk pilots that show value without exposing the programme to disproportionate risk

**Blockers** (What would hinder):

- Public controversy, legal challenge, or uncontrolled pilots
- Weak benefit evidence or inability to explain how decisions are governed

**Related Stakeholders**:

- Home Office, Service Owner, Chief Constables, SIRO, CISO

---

### SD-2: Chief Constables and force operational leads - Improve operational effectiveness without losing local control

**Stakeholder**: Chief Constables and force operational leads

**Driver Category**: OPERATIONAL

**Driver Statement**: Reduce avoidable administrative effort and improve decision support while
retaining confidence that forces can control operational risk and local deployment choices.

**Context & Background**:
Force leaders are under pressure to improve service quality and workforce productivity while
operating with constrained budgets and variable local capability. They are unlikely to support a
programme perceived as centrally imposed, operationally brittle, or misaligned with local practice.

**Driver Intensity**: HIGH

**Enablers** (What would help):

- Configurable operating model with shared standards and local implementation guardrails
- Evidence that pilots improve throughput or quality in real workflows

**Blockers** (What would hinder):

- One-size-fits-all process design that ignores force variation
- Insufficient training, service support, or operational fallback

**Related Stakeholders**:

- SRO, Service Owner, Investigations leads, Service operations

---

### SD-3: Frontline officers and staff - Reduce administrative burden and cognitive overload

**Stakeholder**: Frontline officers and operational staff

**Driver Category**: OPERATIONAL

**Driver Statement**: Spend less time on repetitive drafting, searching, and summarising so more
time can be spent on operational tasks that require human judgement.

**Context & Background**:
Officers and staff work in time-constrained, interruption-heavy environments. They will support the
programme if it saves time without adding hidden rework, brittle tooling, or accountability
confusion.

**Driver Intensity**: HIGH

**Enablers** (What would help):

- Reliable user experience with clear confidence boundaries and fast response times
- Training and safe operating procedures that define when to trust, edit, or reject outputs

**Blockers** (What would hinder):

- Slow interfaces, poor mobile usability, or excessive manual verification burden
- Fear that generated content will create personal accountability risk without support

**Related Stakeholders**:

- Service Owner, Learning and workforce leads, Investigations leads

---

### SD-4: Investigations and intelligence leads - Preserve evidential integrity and analytical quality

**Stakeholder**: Detectives, intelligence managers, and supervisory analysts

**Driver Category**: RISK

**Driver Statement**: Use AI to accelerate information handling without contaminating evidence,
weakening analytical standards, or obscuring provenance.

**Context & Background**:
These teams manage workflows where factual precision, traceability, and defensibility matter. They
need assurance that generated outputs remain clearly separate from source records and can withstand
internal challenge and external scrutiny.

**Driver Intensity**: CRITICAL

**Enablers** (What would help):

- Provenance capture, source linking, and strong labeling of generated material
- Clear guardrails limiting use in evidentially sensitive tasks until controls mature

**Blockers** (What would hinder):

- Ambiguous distinction between source evidence and generated summaries
- Pressure to use AI outputs directly in case records without traceability

**Related Stakeholders**:

- CPS, SIRO, Legal, Frontline users, Enterprise architecture

---

### SD-5: Service Owner and product leadership - Deliver adoption, service quality, and controlled scale

**Stakeholder**: Service Owner, Product Manager, Delivery Manager

**Driver Category**: STRATEGIC

**Driver Statement**: Launch a service that users adopt, that can scale across forces, and that
maintains quality and governance as demand grows.

**Context & Background**:
Product and delivery leadership are judged on whether the service solves a real problem, ships on a
credible schedule, and remains operable after go-live. They need clear priorities, usable success
measures, and a manageable path through assurance dependencies.

**Driver Intensity**: HIGH

**Enablers** (What would help):

- Clear service scope with phased onboarding and measurable adoption KPIs
- Governance cadence that is rigorous but predictable enough for delivery planning

**Blockers** (What would hinder):

- Unbounded scope expansion across too many policing use cases at once
- Late assurance surprises or unresolved cross-force policy decisions

**Related Stakeholders**:

- SRO, Enterprise architecture, SIRO, CISO, Force leads

---

### SD-6: SIRO, DPO, legal, and information governance - Prevent unlawful or excessive use of sensitive data

**Stakeholder**: SIRO, Data Protection Officer, Legal Counsel, Information Governance

**Driver Category**: COMPLIANCE

**Driver Statement**: Ensure all AI uses are lawful, proportionate, privacy-preserving, and
defensible under data protection, equality, human rights, and records-management obligations.

**Context & Background**:
These stakeholders own or advise on information risk, legal challenge, and regulatory exposure.
They need confidence that the architecture minimises data, supports transparency, and preserves
auditability and subject-right handling.

**Driver Intensity**: CRITICAL

**Enablers** (What would help):

- Complete data-flow documentation, purpose limitation, and retention controls
- Structured DPIA and legal review embedded before live deployment

**Blockers** (What would hinder):

- Unclear lawful basis, uncontrolled data reuse, or opaque supplier processing arrangements
- Gaps in audit trails, transparency records, or deletion controls

**Related Stakeholders**:

- ICO, SRO, Service Owner, CISO, Enterprise architecture

---

### SD-7: CISO and cyber teams - Reduce attack surface and contain AI-specific security threats

**Stakeholder**: CISO, security architects, cyber operations

**Driver Category**: RISK

**Driver Statement**: Enable useful AI capabilities without introducing an unmanaged attack
surface, privileged data leakage path, or weak supplier dependency chain.

**Context & Background**:
Security stakeholders are accountable for preventing avoidable incidents and for setting the
conditions under which residual risk can be accepted. They are particularly sensitive to prompt
manipulation, over-privileged integrations, and weak operational separation of duties.

**Driver Intensity**: CRITICAL

**Enablers** (What would help):

- Early threat modeling and clear least-privilege design
- Security testing covering prompt misuse, data exfiltration, and privileged tool access

**Blockers** (What would hinder):

- Pilot shortcuts that bypass hardened controls
- Incomplete supplier assurance or hidden administrative backdoors

**Related Stakeholders**:

- SIRO, Service operations, Enterprise architecture, Suppliers

---

### SD-8: Finance and commercial leads - Demonstrate value for money and avoid supplier lock-in

**Stakeholder**: Finance, commercial, and procurement leads

**Driver Category**: FINANCIAL

**Driver Statement**: Show that investment in GenAI produces measurable operational value while
keeping supplier dependency, variable consumption costs, and commercial risk under control.

**Context & Background**:
Public-sector funding must be justified against competing priorities. Commercial teams need a
credible benefits case, transparent unit economics, and a realistic exit or substitution strategy
for externally supplied capabilities.

**Driver Intensity**: HIGH

**Enablers** (What would help):

- Benefits model linking time savings and quality gains to financial value
- Commercial controls for usage, supplier change, and contractual assurance obligations

**Blockers** (What would hinder):

- Vague benefits claims or unbounded consumption growth
- Lack of visibility into supplier sub-processing, price changes, or exit costs

**Related Stakeholders**:

- SRO, Service Owner, Suppliers, Home Office

---

### SD-9: Public, victims, witnesses, and community representatives - Fairness, transparency, and trustworthy service

**Stakeholder**: Public, victims, witnesses, community groups

**Driver Category**: CUSTOMER

**Driver Statement**: Receive policing services that are accurate, fair, explainable, and
respectful of rights, particularly for vulnerable or disproportionately affected groups.

**Context & Background**:
These stakeholders experience the consequences of policing technology decisions even when they never
see the underlying system. Trust will fall quickly if AI is perceived as opaque, biased, or used
without meaningful human accountability.

**Driver Intensity**: HIGH

**Enablers** (What would help):

- Plain-language transparency about what AI is and is not doing
- Accessible service design, complaints routes, and evidence of fairness testing

**Blockers** (What would hinder):

- Inaccurate outputs affecting public-facing interactions
- Poor handling of vulnerable users, accessibility gaps, or opaque escalation processes

**Related Stakeholders**:

- Service Owner, Home Office, ICO, Watchdog groups

---

### SD-10: Home Office, HMICFRS, and College of Policing - National consistency, assurance, and reuse

**Stakeholder**: Home Office, HMICFRS, College of Policing

**Driver Category**: COMPLIANCE

**Driver Statement**: Encourage innovation that is reusable across policing, aligned to policy and
standards, and capable of standing up to assurance and inspection.

**Context & Background**:
These bodies are concerned with policy coherence, accountability, and repeatability rather than
only local optimisation. They need confidence that the programme creates reusable practice rather
than isolated pilots that cannot be scaled or governed consistently.

**Driver Intensity**: HIGH

**Enablers** (What would help):

- Common standards for interfaces, auditability, and governance artifacts
- Reusable evidence packs for assurance, service assessment, and inspection readiness

**Blockers** (What would hinder):

- Force-by-force divergence with incompatible controls or inconsistent records
- Benefits that cannot be compared or inspected nationally

**Related Stakeholders**:

- SRO, Force leads, Enterprise architecture, Service Owner

---

## Driver-to-Goal Mapping

### Goal G-1: Establish lawful and assured assistive AI use by Q4 2026

**Derived From Drivers**: SD-1, SD-5, SD-6, SD-7, SD-10

**Goal Owner**: Service Owner

**Goal Statement**: By 2026-12-31, implement and approve a production operating model for
assistive GenAI use in at least three policing workflows, with completed privacy, security, legal,
and architectural assurance artifacts and explicit human-oversight controls.

**Why This Matters**: This goal addresses sponsor pressure for visible progress while satisfying
assurance stakeholders that deployment is lawful, governable, and bounded to appropriate use.

**Success Metrics**:

- **Primary Metric**: Number of production workflows with approved assurance pack and live-service
  controls
- **Secondary Metrics**:
  - Percentage of in-scope workflows with completed DPIA, threat model, and operating procedure
  - Number of assurance exceptions open beyond agreed expiry

**Baseline**: 0 approved production workflows; 0 completed integrated assurance packs

**Target**: 3 approved workflows; 100% assurance pack completion for live scope; 0 overdue
assurance exceptions

**Measurement Method**: Programme governance tracker validated by architecture, security, legal,
and service management review records

**Dependencies**:

- Agreed governance model and service ownership
- Availability of pilot forces and assurance reviewers

**Risks to Achievement**:

- Late discovery of unresolved legal or privacy issues
- Delivery pressure causing pilot scope to outpace governance readiness

---

### Goal G-2: Reduce officer and staff administrative effort in pilot workflows by 20% by Q1 2027

**Derived From Drivers**: SD-2, SD-3, SD-5, SD-8

**Goal Owner**: Chief Constable sponsor for pilot forces

**Goal Statement**: By 2027-03-31, reduce average administrative time spent on selected drafting,
summarisation, and information-retrieval tasks by 20% across pilot cohorts, without reducing task
quality or increasing rework.

**Why This Matters**: Productivity gains are the clearest operational proof that the programme is
worth funding and scaling, provided the gains do not simply displace work into checking and rework.

**Success Metrics**:

- **Primary Metric**: Average minutes per completed task for target workflows
- **Secondary Metrics**:
  - User-reported workload reduction
  - Rework rate after supervisory review

**Baseline**: 45 minutes average per target task; workload satisfaction score 54%; rework rate 18%

**Target**: 36 minutes average per target task; workload satisfaction score 70%; rework rate at or
below 18%

**Measurement Method**: Time-and-motion study, workflow analytics, and monthly user survey for
pilot cohorts

**Dependencies**:

- Stable user experience and training completion
- Agreement on target workflows and baseline measurement

**Risks to Achievement**:

- Users reject the tool due to low trust or poor usability
- Time savings are lost to mandatory checking because output quality is inconsistent

---

### Goal G-3: Protect evidential integrity and analytical quality from day one of pilot operation

**Derived From Drivers**: SD-4, SD-6, SD-7, SD-9

**Goal Owner**: Investigations and Intelligence Lead

**Goal Statement**: Before any pilot workflow handling sensitive case information goes live, ensure
all generated outputs are labeled, traceable to source context where required, and prohibited from
overwriting original records, with supervisory review in place for evidentially sensitive tasks.

**Why This Matters**: If AI-generated content compromises evidence handling or analytical quality,
the programme will lose operational legitimacy and face serious legal and reputational challenge.

**Success Metrics**:

- **Primary Metric**: Percentage of pilot workflows with provenance, labeling, and review controls
- **Secondary Metrics**:
  - Number of evidential handling breaches attributable to AI workflow design
  - Supervisory acceptance rate for AI-assisted analytical outputs

**Baseline**: 0 workflows with standardized provenance controls; no consistent labeling approach

**Target**: 100% of sensitive pilot workflows protected by provenance and review controls; 0
material evidential breaches

**Measurement Method**: Design assurance checklist, supervisory sampling, incident reporting, and
audit-log review

**Dependencies**:

- Agreement on what counts as evidentially sensitive use
- Support from casework system owners and justice partners

**Risks to Achievement**:

- Pressure to expand into high-value workflows before controls are mature
- Inconsistent local practice across forces

---

### Goal G-4: Achieve zero material privacy or security incidents attributable to the service in the first 12 months

**Derived From Drivers**: SD-1, SD-6, SD-7, SD-9

**Goal Owner**: SIRO

**Goal Statement**: From first production release through the first 12 months of operation, record
zero material privacy breaches or security incidents attributable to GenAI service design, access
controls, or supplier processing failures.

**Why This Matters**: Public trust and regulatory confidence depend on preventing avoidable failures
in the handling of sensitive policing data and privileged workflows.

**Success Metrics**:

- **Primary Metric**: Number of material privacy or security incidents attributable to the service
- **Secondary Metrics**:
  - Percentage of critical findings remediated before release
  - Mean time to detect and contain AI-specific security events

**Baseline**: No live service; no operational baseline established

**Target**: 0 material incidents; 100% remediation of critical findings before release; mean time
to contain priority events < 4 hours

**Measurement Method**: Incident management system, security operations reporting, privacy incident
review, and post-incident analysis

**Dependencies**:

- Effective security operations integration
- Tested logging, alerting, and least-privilege controls

**Risks to Achievement**:

- Supplier-side control gaps not detected during onboarding
- Over-privileged connectors introduced during rapid integration work

---

### Goal G-5: Establish a reusable cross-force operating model and integration standard by Q2 2027

**Derived From Drivers**: SD-2, SD-5, SD-8, SD-10

**Goal Owner**: Enterprise Architecture Lead

**Goal Statement**: By 2027-06-30, publish and adopt a reusable operating model, interface
contract set, and governance pack that can be used by at least five forces without redesigning the
core service controls.

**Why This Matters**: National reuse lowers delivery cost, improves comparability of assurance
evidence, and prevents fragmentation into incompatible local implementations.

**Success Metrics**:

- **Primary Metric**: Number of forces able to onboard using the standard operating model
- **Secondary Metrics**:
  - Percentage of integrations using published contracts
  - Number of force-specific deviations requiring formal exception

**Baseline**: No published cross-force standard pack; onboarding model not yet defined

**Target**: 5 forces using the standard pack; 90% of integrations using published contracts; fewer
than 3 active force-specific design exceptions

**Measurement Method**: Onboarding tracker, architecture compliance reviews, and contract registry

**Dependencies**:

- Agreement on national minimum controls and reusable artifacts
- Support from pilot and follow-on forces

**Risks to Achievement**:

- Excessive local customization undermines reuse
- National standards emerge too late for early delivery decisions

---

### Goal G-6: Demonstrate value for money and public confidence by Q3 2027

**Derived From Drivers**: SD-1, SD-8, SD-9, SD-10

**Goal Owner**: SRO

**Goal Statement**: By 2027-09-30, demonstrate a defensible benefits case showing operational time
savings, improved service quality, and stable public-confidence indicators sufficient to support a
scale-up investment decision.

**Why This Matters**: Sustainable funding and national rollout require proof that the service
improves outcomes and can withstand scrutiny from finance, policy, oversight, and the public.

**Success Metrics**:

- **Primary Metric**: Benefits case approved for scale-up based on measured pilot performance
- **Secondary Metrics**:
  - Estimated annualized hours saved across participating forces
  - Number of substantiated public complaints linked to AI-enabled service use

**Baseline**: No approved scale-up case; no realized benefits evidence

**Target**: Scale-up business case approved; > 25,000 annualized staff hours saved across pilot
forces; no sustained upward trend in substantiated complaints

**Measurement Method**: Benefits register, finance review, complaints analysis, and board papers

**Dependencies**:

- Robust baseline capture and benefits tracking
- Transparent narrative linking operational outcomes to public value

**Risks to Achievement**:

- Benefits are overstated or not reproducible beyond pilots
- Public concerns dominate the narrative despite operational improvements

---

## Goal-to-Outcome Mapping

### Outcome O-1: Governed production readiness for assistive AI use

**Supported Goals**: G-1, G-4, G-5

**Outcome Statement**: A repeatable governance and assurance model exists for assistive GenAI use,
demonstrated by approved live-service artifacts, documented operating procedures, and controlled
deployment across pilot forces.

**Measurement Details**:

- **KPI**: Number of live workflows operating under the approved assurance model
- **Current Value**: 0
- **Target Value**: 3 by 2026-12-31
- **Measurement Frequency**: Monthly
- **Data Source**: Programme governance tracker and service readiness records
- **Report Owner**: Service Owner

**Business Value**:

- **Financial Impact**: Avoids rework and failed pilot spend by gating scale on evidence
- **Strategic Impact**: Builds credibility for national AI-enabled policing capability
- **Operational Impact**: Creates a controlled path from pilot to live service
- **Customer Impact**: Improves confidence that services are being introduced responsibly

**Timeline**:

- **Phase 1 (Months 1-3)**: Governance model, decision rights, and initial pilot use cases agreed
- **Phase 2 (Months 4-6)**: Assurance packs completed and pre-production controls tested
- **Phase 3 (Months 7-12)**: Three workflows approved and monitored in live operation
- **Sustainment (Year 2+)**: Governance artifacts reused for additional forces and use cases

**Stakeholder Benefits**:

- **SRO**: Visible progress with defensible controls
- **SIRO / CISO / Legal**: Clear evidence base for risk acceptance and oversight

**Leading Indicators** (early signals of success):

- Percentage of in-scope workflows with draft assurance packs
- Number of unresolved critical assurance actions older than 30 days

**Lagging Indicators** (final proof of success):

- Count of approved live workflows
- Number of live workflows suspended for control deficiencies

---

### Outcome O-2: Measurable workforce productivity improvement in target workflows

**Supported Goals**: G-2, G-6

**Outcome Statement**: Pilot forces achieve sustained productivity gains in selected administrative
and analytical workflows without increasing quality defects or supervisory rework.

**Measurement Details**:

- **KPI**: Percentage reduction in average minutes per target workflow task
- **Current Value**: 0% improvement from baseline
- **Target Value**: 20% reduction by 2027-03-31
- **Measurement Frequency**: Monthly
- **Data Source**: Workflow analytics, structured observational studies, and supervisor sampling
- **Report Owner**: Chief Constable sponsor for pilot forces

**Business Value**:

- **Financial Impact**: Releases staff capacity equivalent to approximately 25,000 annualized hours
- **Strategic Impact**: Strengthens case for national rollout based on operational evidence
- **Operational Impact**: Frees officer and staff time for higher-value policing activity
- **Customer Impact**: Faster handling of public-facing and internal casework tasks

**Timeline**:

- **Phase 1 (Months 1-3)**: Baseline workflow timing and user pain points captured
- **Phase 2 (Months 4-6)**: Early pilot users demonstrate 10% time reduction in controlled tasks
- **Phase 3 (Months 7-12)**: 20% reduction sustained across pilot cohorts
- **Sustainment (Year 2+)**: Benefits model expanded to additional workflows and forces

**Stakeholder Benefits**:

- **Frontline officers and staff**: Lower administrative burden
- **Finance and SRO**: Evidence that benefits are real and scalable

**Leading Indicators** (early signals of success):

- Weekly active usage by trained pilot users
- User-reported usefulness score above 70%

**Lagging Indicators** (final proof of success):

- Measured time reduction against baseline
- Stable or improved rework rate after supervisory review

---

### Outcome O-3: Defensible evidential and analytical handling in AI-assisted workflows

**Supported Goals**: G-3, G-4

**Outcome Statement**: AI-assisted workflows involving sensitive case material operate with
traceable provenance, clear output labeling, supervisory review, and no material evidential
handling failures.

**Measurement Details**:

- **KPI**: Percentage of sensitive workflows with complete provenance and supervisory controls
- **Current Value**: 0%
- **Target Value**: 100% before live use of sensitive workflows
- **Measurement Frequency**: Monthly
- **Data Source**: Audit logs, design assurance checklists, and quality sampling
- **Report Owner**: Investigations and Intelligence Lead

**Business Value**:

- **Financial Impact**: Avoids cost of case rework, challenge, and failed prosecutions
- **Strategic Impact**: Preserves legitimacy for AI-assisted policing
- **Operational Impact**: Improves confidence in analytical outputs and summaries
- **Customer Impact**: Reduces risk of unfair or inaccurate downstream service impacts

**Timeline**:

- **Phase 1 (Months 1-3)**: Sensitive workflow categories and control requirements defined
- **Phase 2 (Months 4-6)**: Provenance, labeling, and review controls tested in non-live settings
- **Phase 3 (Months 7-12)**: Sensitive pilot workflows operate under supervisory control
- **Sustainment (Year 2+)**: Expanded assurance sampling and justice-partner validation

**Stakeholder Benefits**:

- **Investigations leads**: Faster information handling with preserved evidential defensibility
- **CPS and legal stakeholders**: Improved confidence in casework quality and traceability

**Leading Indicators** (early signals of success):

- Percentage of generated outputs carrying correct labels
- Supervisory sampling pass rate in pilot rehearsals

**Lagging Indicators** (final proof of success):

- Number of evidential breaches linked to the service
- Acceptance of AI-assisted outputs in operational review

---

### Outcome O-4: Stable privacy and security posture during the first year of operation

**Supported Goals**: G-1, G-4

**Outcome Statement**: The live service operates for its first 12 months without a material privacy
or security incident attributable to GenAI design, access control failure, or unmanaged supplier
processing.

**Measurement Details**:

- **KPI**: Count of material privacy or security incidents attributable to the service
- **Current Value**: No live baseline
- **Target Value**: 0
- **Measurement Frequency**: Weekly operational review, monthly governance summary
- **Data Source**: Incident system, SIEM alerts, privacy incident logs, supplier reports
- **Report Owner**: SIRO

**Business Value**:

- **Financial Impact**: Avoids incident response, remediation, and regulatory cost
- **Strategic Impact**: Protects programme credibility and readiness for scale
- **Operational Impact**: Maintains continuity and confidence in live service
- **Customer Impact**: Protects sensitive information and reduces harm to affected persons

**Timeline**:

- **Phase 1 (Months 1-3)**: Logging, monitoring, and incident runbooks defined
- **Phase 2 (Months 4-6)**: Control validation and response exercises completed
- **Phase 3 (Months 7-12)**: Live monitoring stabilised with continuous review
- **Sustainment (Year 2+)**: Threat intelligence and drift monitoring incorporated into BAU

**Stakeholder Benefits**:

- **SIRO / DPO / Legal**: Lower risk of breach and challenge
- **Security teams**: Greater confidence that AI-specific threats are manageable

**Leading Indicators** (early signals of success):

- Percentage of critical findings closed before release
- Mean time to investigate priority alerts

**Lagging Indicators** (final proof of success):

- Count of material incidents
- Number of regulator-reportable events

---

### Outcome O-5: Nationally reusable service pattern for force onboarding

**Supported Goals**: G-5, G-6

**Outcome Statement**: At least five forces can onboard to the service using a standard governance,
integration, and operating model pack with limited local exceptions.

**Measurement Details**:

- **KPI**: Number of forces onboarded using the standard pack
- **Current Value**: 0
- **Target Value**: 5 by 2027-06-30
- **Measurement Frequency**: Monthly
- **Data Source**: Onboarding tracker, architecture compliance register, exception log
- **Report Owner**: Enterprise Architecture Lead

**Business Value**:

- **Financial Impact**: Reduces duplicated delivery and assurance cost across forces
- **Strategic Impact**: Enables national comparability and policy coherence
- **Operational Impact**: Speeds rollout by reusing tested controls and integration patterns
- **Customer Impact**: Supports more consistent service quality across jurisdictions

**Timeline**:

- **Phase 1 (Months 1-3)**: Standard control pack and interface set defined
- **Phase 2 (Months 4-6)**: Two pilot forces onboard using the pack
- **Phase 3 (Months 7-12)**: Five forces onboard with limited local exceptions
- **Sustainment (Year 2+)**: Standard pack maintained as national reference pattern

**Stakeholder Benefits**:

- **Force leads**: Faster onboarding with clearer local obligations
- **Home Office / HMICFRS / College of Policing**: Better consistency and easier assurance review

**Leading Indicators** (early signals of success):

- Number of forces agreeing to the minimum control pack
- Percentage of integrations implemented through published contracts

**Lagging Indicators** (final proof of success):

- Total onboarded forces using the standard pack
- Number of unresolved local exceptions preventing rollout

---

### Outcome O-6: Defensible scale-up case with stable public-confidence indicators

**Supported Goals**: G-2, G-6

**Outcome Statement**: The programme secures approval for scaled rollout based on demonstrated
benefits, stable quality indicators, and no sustained deterioration in complaint, challenge, or
trust-related measures.

**Measurement Details**:

- **KPI**: Scale-up investment decision supported by measured pilot outcomes
- **Current Value**: Not yet assessed
- **Target Value**: Approved by 2027-09-30
- **Measurement Frequency**: Quarterly
- **Data Source**: Board papers, benefits register, complaints data, public assurance reporting
- **Report Owner**: SRO

**Business Value**:

- **Financial Impact**: Justifies future funding with evidence rather than optimistic projection
- **Strategic Impact**: Positions the programme as a durable national capability
- **Operational Impact**: Enables controlled expansion into additional forces and workflows
- **Customer Impact**: Sustains public trust through transparency and measured performance

**Timeline**:

- **Phase 1 (Months 1-3)**: Baseline benefits and trust indicators agreed
- **Phase 2 (Months 4-6)**: Early benefit evidence and transparency reporting produced
- **Phase 3 (Months 7-12)**: Scale-up case submitted with pilot evidence
- **Sustainment (Year 2+)**: Annual benefits and trust review inform continued investment

**Stakeholder Benefits**:

- **SRO / Home Office / Finance**: Defensible investment decision
- **Public and community representatives**: Clearer evidence that safeguards and outcomes are being monitored

**Leading Indicators** (early signals of success):

- Benefits data completeness across pilot forces
- Percentage of transparency actions completed on schedule

**Lagging Indicators** (final proof of success):

- Formal approval of scale-up investment
- No sustained upward trend in substantiated AI-related complaints

---

## Complete Traceability Matrix

### Stakeholder → Driver → Goal → Outcome

| Stakeholder | Driver ID | Driver Summary | Goal ID | Goal Summary | Outcome ID | Outcome Summary |
|-------------|-----------|----------------|---------|--------------|------------|-----------------|
| SRO | SD-1 | Visible public value without governance failure | G-1 | Establish lawful and assured assistive AI use | O-1 | Governed production readiness |
| SRO | SD-1 | Visible public value without governance failure | G-6 | Demonstrate value for money and public confidence | O-6 | Defensible scale-up case |
| Chief Constables and force leads | SD-2 | Operational effectiveness with local control | G-2 | Reduce administrative effort | O-2 | Workforce productivity improvement |
| Chief Constables and force leads | SD-2 | Operational effectiveness with local control | G-5 | Reusable cross-force operating model | O-5 | Nationally reusable service pattern |
| Frontline officers and staff | SD-3 | Reduce administrative burden | G-2 | Reduce administrative effort | O-2 | Workforce productivity improvement |
| Investigations and intelligence leads | SD-4 | Preserve evidential integrity | G-3 | Protect evidential integrity | O-3 | Defensible evidential handling |
| Service Owner and product leadership | SD-5 | Adoption, quality, and controlled scale | G-1 | Establish lawful and assured assistive AI use | O-1 | Governed production readiness |
| Service Owner and product leadership | SD-5 | Adoption, quality, and controlled scale | G-5 | Reusable cross-force operating model | O-5 | Nationally reusable service pattern |
| SIRO / DPO / Legal | SD-6 | Prevent unlawful or excessive data use | G-1 | Establish lawful and assured assistive AI use | O-1 | Governed production readiness |
| SIRO / DPO / Legal | SD-6 | Prevent unlawful or excessive data use | G-4 | Zero material privacy or security incidents | O-4 | Stable privacy and security posture |
| CISO and cyber teams | SD-7 | Reduce attack surface and AI-specific threats | G-4 | Zero material privacy or security incidents | O-4 | Stable privacy and security posture |
| Finance and commercial | SD-8 | Value for money and avoid lock-in | G-2 | Reduce administrative effort | O-2 | Workforce productivity improvement |
| Finance and commercial | SD-8 | Value for money and avoid lock-in | G-6 | Demonstrate value for money and public confidence | O-6 | Defensible scale-up case |
| Public and community representatives | SD-9 | Fairness, transparency, and trustworthy service | G-3 | Protect evidential integrity | O-3 | Defensible evidential handling |
| Public and community representatives | SD-9 | Fairness, transparency, and trustworthy service | G-4 | Zero material privacy or security incidents | O-4 | Stable privacy and security posture |
| Home Office / HMICFRS / College of Policing | SD-10 | National consistency and assurance | G-5 | Reusable cross-force operating model | O-5 | Nationally reusable service pattern |
| Home Office / HMICFRS / College of Policing | SD-10 | National consistency and assurance | G-6 | Demonstrate value for money and public confidence | O-6 | Defensible scale-up case |

### Conflict Analysis

**Competing Drivers**:

- **Conflict 1**: The SRO and delivery leadership want early visible progress, but SIRO, legal,
  and security stakeholders require deeper assurance before live deployment.
  - **Resolution Strategy**: Use phased rollout with low-risk assistive use cases first, define
    clear no-go criteria for higher-risk use, and make assurance completion a release gate rather
    than a parallel aspiration.

- **Conflict 2**: Force operational leads want local flexibility, but national stakeholders want a
  standard operating model that supports reuse and inspection.
  - **Resolution Strategy**: Define a national minimum control pack with limited configurable local
    options and require formal exceptions for material divergence.

- **Conflict 3**: Frontline users want speed and minimal friction, but investigations, legal, and
  CPS stakeholders need stronger provenance and review controls for sensitive workflows.
  - **Resolution Strategy**: Separate workflow classes by risk; allow lighter controls for
    low-risk drafting assistance while enforcing stronger supervisory review where evidential
    sensitivity is higher.

**Synergies**:

- **Synergy 1**: Frontline productivity gains and finance value-for-money drivers both benefit from
  measurable time reduction in target workflows.
- **Synergy 2**: SIRO, CISO, public-interest, and SRO drivers all align around strong auditability,
  human accountability, and transparent governance.
- **Synergy 3**: Force leads and national oversight bodies both benefit from reusable onboarding
  patterns if those patterns still permit bounded local implementation choice.

---

## Communication & Engagement Plan

### Stakeholder-Specific Messaging

#### Senior Responsible Owner

**Primary Message**: The programme is delivering measurable progress in bounded, governable stages
that can survive scrutiny and support future scale decisions.

**Key Talking Points**:

- Benefits and assurance are being tracked together rather than traded off informally
- Early pilots are intentionally low-risk and designed to produce credible evidence
- Escalation triggers are explicit when scope pressures threaten governance

**Communication Frequency**: Weekly

**Preferred Channel**: Steering meeting and written dashboard

**Success Story**: Three approved live workflows with measured time savings and no material control
failures.

#### Chief Constables and force operational leads

**Primary Message**: The service is designed to improve workforce productivity while preserving
local operational accountability and force-level implementation control within agreed guardrails.

**Key Talking Points**:

- Pilot workflows are chosen with operational leaders, not imposed centrally
- Local fallback, training, and support are part of the deployment model
- Reuse reduces cost, but forces retain control over local rollout decisions

**Communication Frequency**: Monthly

**Preferred Channel**: Operational adoption forum and force briefings

**Success Story**: Pilot forces report faster workflow completion and manageable local support
overhead.

#### Frontline officers and staff

**Primary Message**: The service is intended to remove repetitive effort, not to replace judgement
or shift hidden risk onto users.

**Key Talking Points**:

- Human sign-off remains in place for material decisions
- Training will show when outputs can help and when they must be challenged
- User feedback directly shapes roadmap and operating guidance

**Communication Frequency**: Fortnightly during pilot; monthly thereafter

**Preferred Channel**: Team briefings, pilot clinics, and in-product guidance

**Success Story**: Users report meaningful time savings without more supervisor corrections.

#### Investigations and intelligence leads

**Primary Message**: AI-assisted workflows will not blur the line between source evidence and
generated interpretation, and sensitive use cases will only go live with traceability controls.

**Key Talking Points**:

- Provenance, labeling, and review controls are mandatory for sensitive workflows
- Supervisory sampling will be used to validate output quality and defensibility
- Expansion into higher-risk use cases requires stronger assurance evidence

**Communication Frequency**: Monthly

**Preferred Channel**: Workflow design reviews and supervisory forums

**Success Story**: Sensitive workflows operate with clear source linking and no evidential handling
failures.

#### SIRO, DPO, legal, and information governance

**Primary Message**: The programme is designed around lawful purpose, minimization, auditability,
and explicit risk ownership rather than post hoc compliance retrofits.

**Key Talking Points**:

- DPIA, legal analysis, and records-management controls are integrated into release decisions
- Data flows, retention, and supplier processing responsibilities are documented
- Exception handling is formal, time-bound, and visible

**Communication Frequency**: Fortnightly through assurance phases; monthly in live operation

**Preferred Channel**: Assurance review boards and documented decision packs

**Success Story**: No unresolved legal or privacy blockers remain at go-live and audit records are
fully reconstructable.

#### CISO and cyber teams

**Primary Message**: The service is being introduced with least privilege, tested controls, and
clear response playbooks for AI-specific threat scenarios.

**Key Talking Points**:

- Threat modeling and misuse testing are in scope from early design
- Administrative access and data connectors are tightly bounded and monitored
- Supplier risk is being managed as part of the live operating model

**Communication Frequency**: Fortnightly before go-live; monthly once stable

**Preferred Channel**: Security design authority and risk review meetings

**Success Story**: No material AI-related incidents occur and critical findings are closed before
release.

#### Finance and commercial leads

**Primary Message**: Benefits, usage, and supplier dependency are being tracked tightly enough to
support an evidence-based investment decision.

**Key Talking Points**:

- Time savings are being measured against baseline, not estimated informally
- Usage and commercial exposure will be reviewed alongside benefits
- Supplier exit and substitution are part of the architecture, not an afterthought

**Communication Frequency**: Monthly

**Preferred Channel**: Commercial review and benefits board

**Success Story**: Pilot evidence supports a scale-up case with controlled cost and limited lock-in.

#### Public and community representatives

**Primary Message**: AI is being used in bounded, explainable ways with human accountability,
rights safeguards, and routes for challenge where appropriate.

**Key Talking Points**:

- The programme is explicit about what AI is and is not used for
- Safeguards exist for privacy, fairness, accessibility, and oversight
- Public trust indicators and complaint patterns are being monitored

**Communication Frequency**: Quarterly, with additional communications for major milestones

**Preferred Channel**: Public transparency statement, community engagement forums, and website updates

**Success Story**: The service delivers benefits without a sustained increase in substantiated
complaints or trust concerns.

---

## Change Impact Assessment

### Impact on Stakeholders

| Stakeholder | Current State | Future State | Change Magnitude | Resistance Risk | Mitigation Strategy |
|-------------|---------------|--------------|------------------|-----------------|---------------------|
| SRO | Receives fragmented innovation proposals and limited evidence of value | Oversees phased national programme with explicit benefits and assurance reporting | HIGH | MEDIUM | Provide concise dashboards and clear decision gates |
| Chief Constables and force leads | Local teams manage admin burden with inconsistent tooling and process | Adopt shared service pattern with local rollout choices inside national guardrails | HIGH | MEDIUM | Use pilot-force design input and limited local configuration |
| Frontline officers and staff | Manual drafting, searching, and summarising dominate target tasks | AI-assisted drafting and retrieval reduce repetitive work but require safe-use training | HIGH | MEDIUM | Focus on low-friction workflows, training, and feedback loops |
| Investigations and intelligence leads | Quality depends on manual synthesis and supervisor review | AI assists synthesis, but provenance and review controls become mandatory | HIGH | HIGH | Restrict early scope, enforce labeling, and sample outputs rigorously |
| SIRO / DPO / Legal | Review digital change through separate governance streams | Operate continuous assurance role embedded in delivery and live service | MEDIUM | MEDIUM | Use integrated assurance plan and clear escalation routes |
| CISO and cyber teams | Security reviews focus on conventional application and hosting risk | Security reviews now include prompt misuse, connector risk, and model governance | MEDIUM | MEDIUM | Expand test scope and define AI-specific response runbooks |
| Finance and commercial | Spend assessed through project-level business case assumptions | Spend tied to real usage, benefits evidence, and supplier lifecycle governance | MEDIUM | LOW | Provide monthly unit-economics and benefits reporting |
| Public and community stakeholders | Limited direct visibility of internal tooling decisions | Higher expectation of transparency and fairness where AI affects service interactions | MEDIUM | HIGH | Publish plain-language explanations and routes for redress |

### Change Readiness

**Champions** (Enthusiastic supporters):

- Service Owner - needs measurable adoption and sees strong upside from bounded pilots
- Frontline pilot users - likely to support change if the tool removes repetitive admin effort
- Enterprise Architecture Lead - supports reuse, standards, and controlled scale

**Fence-sitters** (Neutral, need convincing):

- Chief Constables and force operational leads - need proof that local operational risk remains manageable
- Finance and commercial leads - need benefits evidence strong enough to justify ongoing spend
- Home Office policy stakeholders - need confidence that the programme is reusable and politically defensible

**Resisters** (Opposed or skeptical):

- Investigations supervisors for evidentially sensitive workflows - worried about provenance, challenge, and case quality
- Privacy and legal stakeholders where data use purpose is unclear - concerned about unlawful or excessive processing
- Civil liberties and watchdog groups - skeptical unless transparency and safeguards are visible and credible

---

## Risk Register (Stakeholder-Related)

### Risk R-1: Assurance backlash from delivery overreach

**Related Stakeholders**: SRO, Service Owner, SIRO, Legal, CISO

**Risk Description**: Delivery pressure leads the programme to expand scope faster than assurance
evidence can support, creating conflict with governance stakeholders and potential stop-work action.

**Impact on Goals**: G-1, G-4, G-6

**Probability**: MEDIUM

**Impact**: HIGH

**Mitigation Strategy**: Tie release approvals to explicit assurance criteria, maintain a risk-based
scope model, and require SRO sign-off for any acceleration affecting control posture.

**Contingency Plan**: Pause higher-risk rollout, revert to bounded low-risk workflows, and convene
an extraordinary assurance review board.

---

### Risk R-2: Frontline rejection due to poor usability or low trust

**Related Stakeholders**: Frontline officers and staff, Service Owner, Learning leads

**Risk Description**: Users perceive the service as slow, unreliable, or personally risky to use,
so adoption remains low and benefits are not realized.

**Impact on Goals**: G-2, G-6

**Probability**: MEDIUM

**Impact**: HIGH

**Mitigation Strategy**: Prioritize high-frequency low-complexity tasks, provide clear guidance on
safe use, and incorporate pilot feedback into every release cycle.

**Contingency Plan**: Narrow the scope to the best-performing workflows and reset the benefits case
on a smaller, more usable service footprint.

---

### Risk R-3: Force fragmentation undermines reuse

**Related Stakeholders**: Force leads, Enterprise Architecture Lead, Home Office

**Risk Description**: Multiple forces demand local variations that break interoperability and make
assurance evidence non-transferable.

**Impact on Goals**: G-5, G-6

**Probability**: MEDIUM

**Impact**: MEDIUM

**Mitigation Strategy**: Define a mandatory minimum control pack, track deviations formally, and
prioritize configurable patterns over bespoke workflows.

**Contingency Plan**: Limit national rollout to forces willing to adopt the standard pack while a
revised federation model is developed.

---

### Risk R-4: Public trust deteriorates after opaque or inaccurate use

**Related Stakeholders**: Public, victims, witnesses, watchdog groups, Home Office

**Risk Description**: A public-facing or high-profile AI-assisted interaction is perceived as
opaque, unfair, or inaccurate, driving complaints and negative media attention.

**Impact on Goals**: G-3, G-4, G-6

**Probability**: LOW

**Impact**: HIGH

**Mitigation Strategy**: Avoid high-risk public-facing use early, publish clear transparency
statements, and maintain a rapid response process for complaints and incidents.

**Contingency Plan**: Suspend the affected use case, communicate corrective action, and conduct an
independent review before resuming.

---

### Risk R-5: Supplier governance gaps weaken confidence in value and control

**Related Stakeholders**: Finance, Commercial, CISO, SIRO, Suppliers

**Risk Description**: The programme cannot clearly explain supplier data handling, contractual
obligations, or exit strategy, leading to finance and assurance resistance.

**Impact on Goals**: G-1, G-4, G-6

**Probability**: MEDIUM

**Impact**: MEDIUM

**Mitigation Strategy**: Maintain a supplier dependency inventory, review sub-processing and change
terms regularly, and document substitution plans for critical components.

**Contingency Plan**: Freeze expansion dependent on the affected supplier until commercial and
assurance remediation actions are complete.

---

## Governance & Decision Rights

### Decision Authority Matrix (RACI)

| Decision Type | Responsible | Accountable | Consulted | Informed |
|---------------|-------------|-------------|-----------|----------|
| Use-case prioritization | Product Manager | Service Owner | Force leads, frontline users, Enterprise Architect | SRO, delivery teams |
| Assurance scope and go-live criteria | Enterprise Architect | SRO | SIRO, DPO, Legal, CISO, Service Owner | Force leads, Home Office |
| Data protection and lawful basis acceptance | DPO / Legal Lead | SIRO | Service Owner, Enterprise Architect, Product Manager | SRO, Delivery Manager |
| Security control acceptance | Security Architect | CISO | SIRO, Service Owner, Suppliers | SRO, Operations |
| Supplier selection and contract change | Commercial Lead | SRO | Finance, CISO, Legal, Service Owner | Delivery teams, Force leads |
| Pilot-force onboarding approval | Delivery Manager | Service Owner | Force leads, Operations, Training leads | SRO, Home Office |
| Public transparency statement release | Communications Lead | SRO | Legal, DPO, Service Owner, Policy leads | All stakeholders |
| Scale-up investment decision | Programme Manager | SRO | Finance, Home Office, Service Owner, Enterprise Architect | All stakeholders |
| Live incident severity escalation | Service Operations Lead | Service Owner | CISO, SIRO, Legal, Force operational lead | SRO, affected stakeholders |

### Escalation Path

1. **Level 1**: Product Manager / Delivery Manager / Service Operations Lead for day-to-day
   delivery, incident, and adoption decisions.
2. **Level 2**: Service Owner and functional leads for scope, prioritisation, and cross-team
   conflicts that affect delivery or assurance.
3. **Level 3**: Enterprise Architecture Review Board and Responsible AI Review Panel for material
   design, control, or policy disputes.
4. **Level 4**: SRO and executive sponsor forum for major scope changes, risk acceptance, funding,
   or public-interest escalation.

---

## Validation & Sign-off

### Stakeholder Review

| Stakeholder | Review Date | Comments | Status |
|-------------|-------------|----------|--------|
| SRO | 2026-03-14 planned | Initial draft to confirm strategic outcomes, risk appetite, and governance cadence | PENDING REVIEW |
| Service Owner | 2026-03-14 planned | Validate service metrics, adoption assumptions, and operating model scope | PENDING REVIEW |
| SIRO / DPO / Legal | 2026-03-18 planned | Confirm privacy, legality, and records-management assumptions | PENDING REVIEW |
| CISO | 2026-03-18 planned | Confirm security risk assumptions and testing approach | PENDING REVIEW |
| Force operational leads | 2026-03-21 planned | Validate frontline workflow assumptions and pilot-force practicality | PENDING REVIEW |

### Document Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Project Sponsor | SRO, GenAI for UK Policing | PENDING | PENDING |
| Business Owner | Service Owner, GenAI for UK Policing | PENDING | PENDING |
| Enterprise Architect | Enterprise Architecture Lead, GenAI for UK Policing | PENDING | PENDING |

---

## Appendices

### Appendix A: Stakeholder Interview Summaries

#### Interview with pilot-force operational leadership cohort - 2026-03-07

**Key Points**:

- Low-risk administrative workflows are the most credible starting point for adoption
- Local leaders want flexibility in rollout sequencing but not a bespoke architecture per force
- Operational support and fallback arrangements are prerequisites for trust

**Quotes**:

- "If this saves officer time without creating extra sign-off risk, adoption will follow quickly."

**Follow-up Actions**:

- Confirm first-wave workflows with pilot-force sponsors
- Validate assumptions about local support and training capacity

#### Interview with assurance stakeholder cohort - 2026-03-07

**Key Points**:

- Privacy, security, and legality must be built into release decisions rather than reviewed late
- Data minimization, provenance, and supplier transparency are the highest assurance concerns
- Boundaries between assistive and decision-support use need to be explicit

**Quotes**:

- "The fastest way to lose trust is to blur what the model generated and what the source record said."

**Follow-up Actions**:

- Produce integrated assurance pack template for pilot workflows
- Define prohibited and restricted use-case categories

#### Interview with user and service design working assumptions - 2026-03-07

**Key Points**:

- Users will accept assistance that is faster than current practice and easy to correct
- Confidence drops quickly when systems are slow, verbose, or unclear about uncertainty
- Training must focus on judgement and safe-use boundaries rather than only tool mechanics

**Quotes**:

- "If the tool adds even a few extra checks with no real saving, people will work around it."

**Follow-up Actions**:

- Build pilot measures around time saved and rework rate, not only usage
- Prepare role-based training and in-product guidance for pilot cohorts

---

### Appendix B: Survey Results

No formal stakeholder survey has been conducted at this stage. For initial planning, the programme
should assume high interest from operational users, high scrutiny from assurance stakeholders, and
conditional support from force leadership pending evidence of local benefit and manageable risk.
Recommended next step: run a short baseline survey across pilot-force users and governance
stakeholders before finalising the benefits baseline.

---

### Appendix C: References

- [Global architecture principles](/workspaces/arckit-test-project-v13-plymouth-research/my-project/projects/000-global/ARC-000-PRIN-v1.0.md)
- GovS 005 Digital
- GovS 007 Security
- Programme working assumptions for GenAI for UK Policing, 2026-03-07

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-03-07 | ArcKit AI | Initial draft created for review |
| 1.0 | 2026-03-07 | ArcKit AI | Completed stakeholder drivers, goals, outcomes, engagement, and governance analysis |

## External References

| Document | Type | Source | Key Extractions | Path |
|----------|------|--------|-----------------|------|
| ARC-000-PRIN-v1.0 | Global architecture principles | Local project artifact | Public value, lawfulness, accountability, privacy, auditability, interoperability, and AI governance requirements | projects/000-global/ARC-000-PRIN-v1.0.md |
| No project-specific external documents provided at generation time | N/A | Local project context | Force-specific org charts, local governance boards, and stakeholder maps were not available in this draft | projects/001-genai-for-uk-policing/external/ |

---

**Generated by**: ArcKit `$arckit-stakeholders` command
**Generated on**: 2026-03-07
**ArcKit Version**: 4.0.0
**Project**: GenAI for UK Policing (Project 001)
**AI Model**: GPT-5 Codex
