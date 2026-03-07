# Project Requirements: GenAI for UK Policing

> **Template Origin**: Official | **ArcKit Version**: 4.0.0 | **Command**: `arckit.requirements`

## Document Control

| Field | Value |
|-------|-------|
| **Document ID** | ARC-001-REQ-v1.0 |
| **Document Type** | Business and Technical Requirements |
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
| **Distribution** | Project Team, Architecture Team, Security, Data Protection, Legal, Delivery Team, Pilot Forces |

## Revision History

| Version | Date | Author | Changes | Approved By | Approval Date |
|---------|------|--------|---------|-------------|---------------|
| 1.0 | 2026-03-07 | ArcKit AI | Initial creation from `$arckit-requirements` command | PENDING | PENDING |

## Document Purpose

This document defines the business, functional, non-functional, integration, and data requirements
for the GenAI for UK Policing initiative. It is intended to support procurement activity, solution
design, architecture review, delivery planning, supplier evaluation, and downstream testing and
assurance.

---

## Executive Summary

### Business Context

UK policing needs practical generative AI capabilities that reduce administrative effort, accelerate
safe information handling, and improve consistency in bounded assistive workflows. At the same
time, the service must remain lawful, auditable, secure, and acceptable under public scrutiny.

The stakeholder analysis for Project 001 identified strong alignment around workforce productivity,
assurance, and national reuse, with the main tensions being speed versus assurance, local force
autonomy versus standardisation, and frictionless user experience versus evidential and governance
controls. These requirements convert those drivers into testable obligations suitable for RFP and
design governance use.

### Objectives

- Deliver at least three lawful, assured assistive GenAI workflows into controlled live use by
  2026-12-31.
- Reduce administrative effort in selected pilot workflows by 20% by 2027-03-31 without increasing
  rework or evidential risk.
- Preserve human accountability, provenance, and auditability for all material outputs.
- Support a reusable cross-force operating model that can onboard at least five forces by
  2027-06-30.
- Produce a defensible scale-up case supported by measurable operational value and stable
  public-confidence indicators by 2027-09-30.

### Expected Outcomes

- Three production workflows operating under approved assurance controls by 2026-12-31.
- 20% reduction in average completion time for target drafting and summarisation tasks by
  2027-03-31.
- Zero material privacy or security incidents attributable to the service in its first 12 months
  of live operation.
- Five forces onboarded using a standard control pack by 2027-06-30.
- Greater than 25,000 annualized staff hours saved across pilot forces by 2027-09-30.

### Project Scope

**In Scope**:

- Assistive GenAI workflows for drafting, summarisation, retrieval, and bounded decision support
- Human-reviewed outputs for frontline, investigative, intelligence, and corporate workflows
- Federated force onboarding with shared national minimum controls
- Privacy, security, transparency, and audit controls required for live use
- Integration with identity, case, knowledge, security, and reporting systems

**Out of Scope**:

- Fully autonomous operational decision-making or enforcement actions
- Unreviewed public-facing use in high-risk service interactions during the initial rollout
- Model training on unrestricted operational data without separate approval and assurance
- National rollout beyond pilot and early adopter forces in this requirements version
- Replacement of core case-management or records systems

---

## Stakeholders

| Stakeholder | Role | Organization | Involvement Level |
|-------------|------|--------------|-------------------|
| Senior Responsible Owner | Executive Sponsor | National policing programme | Decision maker |
| Service Owner | Service accountability | GenAI for UK Policing | Requirements owner |
| Product Manager | Delivery and prioritisation | Delivery team | Requirements definition |
| Enterprise Architect | Technical oversight | Architecture | Technical governance |
| Security Lead | Security review and acceptance | Security | Security review |
| SIRO / DPO / Legal Lead | Information risk and legality | Governance | Compliance and legal review |
| Force Operational Lead | Pilot-force sponsor | Participating forces | Operational acceptance |
| End User Representative | Frontline and analyst cohort | Participating forces | User acceptance and feedback |
| Finance / Commercial Lead | Value for money and supplier control | Commercial | Business case and procurement review |
| Service Operations Lead | Live service readiness | Operations | Operational readiness and incident response |

---

## Business Requirements

### BR-001: Deliver lawful and assured assistive AI use

**Description**: The programme must deliver a controlled production operating model for assistive
GenAI use in at least three policing workflows by 2026-12-31.

**Rationale**: This requirement addresses stakeholder goals G-1 and O-1 by converting sponsor and
assurance expectations into a measurable delivery obligation.

**Success Criteria**:

- Three workflows are approved for live use by 2026-12-31.
- Each live workflow has completed architecture, privacy, security, legal, and operational review.

**Acceptance Criteria**:

- [ ] A go-live record exists for each in-scope workflow, signed off by Service Owner, SIRO, and
      security authority.
- [ ] Each live workflow has documented human-oversight controls, operating procedures, and support
      runbooks.
- [ ] No workflow enters live operation without a completed assurance pack.

**Priority**: MUST

**Stakeholder**: Senior Responsible Owner, Service Owner

**Traceability**: G-1, O-1; PRIN: Public value, lawfulness, and proportionality; Assurance by
default

---

### BR-002: Achieve measurable workforce productivity gains

**Description**: The service must reduce administrative effort in target pilot workflows by 20% by
2027-03-31 without increasing supervisory rework.

**Rationale**: This captures the operational and financial value expected by force leads, frontline
users, and finance stakeholders.

**Success Criteria**:

- Average task time falls from 45 minutes to 36 minutes or better in target workflows.
- Rework rate remains at or below the current baseline of 18%.

**Acceptance Criteria**:

- [ ] Baseline and post-deployment workflow timing are measured using the same method.
- [ ] At least two pilot workflows demonstrate a 20% or greater time reduction.
- [ ] Supervisory rework does not exceed the pre-pilot baseline for those workflows.

**Priority**: MUST

**Stakeholder**: Chief Constable sponsor for pilot forces, Finance / Commercial Lead

**Traceability**: G-2, O-2, O-6; PRIN: Public value, lawfulness, and proportionality; Performance,
accessibility, and usability

---

### BR-003: Protect evidential integrity and analytical defensibility

**Description**: The service must preserve provenance, reviewability, and source separation for all
AI-assisted workflows involving sensitive case or intelligence material.

**Rationale**: This is required to satisfy investigations, legal, and public-interest stakeholders
who cannot accept generated outputs being mistaken for evidence or authoritative fact.

**Success Criteria**:

- 100% of sensitive pilot workflows use provenance and supervisory review controls before go-live.
- Zero material evidential breaches are attributable to service design.

**Acceptance Criteria**:

- [ ] Generated outputs in sensitive workflows are labeled as generated or derived.
- [ ] Source references or provenance metadata are retained and reviewable.
- [ ] Sensitive outputs cannot overwrite the original source record directly.

**Priority**: MUST

**Stakeholder**: Investigations and Intelligence Lead, SIRO / DPO / Legal Lead

**Traceability**: G-3, O-3; PRIN: Data quality, provenance, and evidential integrity; Human
accountability and contestability

---

### BR-004: Maintain a strong privacy and security posture

**Description**: The service must operate for its first 12 months without a material privacy or
security incident attributable to GenAI design, access control failure, or unmanaged supplier
processing.

**Rationale**: This turns stakeholder risk tolerance into a measurable live-service requirement.

**Success Criteria**:

- Zero material privacy or security incidents in the first 12 months of operation.
- All critical findings are remediated before production release.

**Acceptance Criteria**:

- [ ] Privacy and security incident ownership, triage, and escalation procedures are defined.
- [ ] Critical findings cannot be waived into production without formal senior approval.
- [ ] Security and privacy monitoring are active from the first production release.

**Priority**: MUST

**Stakeholder**: SIRO, Security Lead

**Traceability**: G-4, O-4; PRIN: Security by design and least privilege; Privacy,
confidentiality, and data sovereignty

---

### BR-005: Support national reuse with bounded local flexibility

**Description**: The service must support a standard operating model, control pack, and
integration-contract set that can be used by at least five forces by 2027-06-30, while allowing
bounded local configuration.

**Rationale**: This resolves the stakeholder need for both national consistency and operationally
realistic force-level adoption.

**Success Criteria**:

- Five forces can onboard using the standard pack by 2027-06-30.
- Force-specific design exceptions remain below three active material exceptions.

**Acceptance Criteria**:

- [ ] A documented national minimum control pack exists for onboarding.
- [ ] Force-local configuration options are defined and bounded.
- [ ] Material divergence from the standard pack requires a formal exception decision.

**Priority**: MUST

**Stakeholder**: Enterprise Architect, Home Office / oversight stakeholders

**Traceability**: G-5, O-5; PRIN: Interoperability and federation; Standard interfaces and loose
coupling

---

### BR-006: Produce a defensible scale-up case

**Description**: The programme must produce a scale-up decision pack by 2027-09-30 showing measured
benefits, cost position, public-interest safeguards, and no sustained deterioration in complaint or
trust indicators.

**Rationale**: This is required for future funding and wider adoption.

**Success Criteria**:

- Scale-up investment decision pack approved or conditionally approved by 2027-09-30.
- Annualized benefits exceed 25,000 staff hours saved across pilot forces.

**Acceptance Criteria**:

- [ ] The benefits register includes measured time savings, adoption, quality, and cost indicators.
- [ ] The decision pack includes public-confidence and complaint analysis.
- [ ] The decision pack explicitly documents residual risks and recommended next-phase scope.

**Priority**: MUST

**Stakeholder**: Senior Responsible Owner, Finance / Commercial Lead

**Traceability**: G-6, O-6; PRIN: Supplier, model, and lifecycle governance; Continuous
monitoring, drift response, and improvement

---

## Functional Requirements

### User Personas

#### Persona 1: Frontline officer

- **Role**: Operational user drafting and reviewing case-related text
- **Goals**: Save time on repetitive drafting and information retrieval
- **Pain Points**: High administrative load, interrupted working patterns, limited tolerance for
  slow tools
- **Technical Proficiency**: Medium

#### Persona 2: Detective or intelligence analyst

- **Role**: User summarising sensitive information and producing analytical outputs
- **Goals**: Accelerate synthesis without weakening accuracy, provenance, or reviewability
- **Pain Points**: Complex case material, high accountability, evidential sensitivity
- **Technical Proficiency**: Medium

#### Persona 3: Service owner or force operational lead

- **Role**: Approver of rollout scope, adoption, and operational use
- **Goals**: Improve productivity while controlling local risk and service quality
- **Pain Points**: Multiple dependencies, local variation, scrutiny over operational failures
- **Technical Proficiency**: Medium

#### Persona 4: Governance reviewer

- **Role**: SIRO, DPO, legal, or security reviewer
- **Goals**: Verify lawfulness, risk control, transparency, and auditability
- **Pain Points**: Weak evidence packs, unclear ownership, incomplete traceability
- **Technical Proficiency**: High

### Use Cases

#### UC-001: Draft an internal summary from approved source material

**Actor**: Frontline officer or detective

**Preconditions**:

- User is authenticated and authorized for the relevant workflow and source data.
- Source records are available through approved retrieval pathways.

**Main Flow**:

1. User selects an approved summarisation workflow.
2. System retrieves only the permitted source context.
3. User requests a draft summary for the task at hand.
4. System generates a draft with source references or provenance markers where required.
5. User edits, accepts, or discards the draft.
6. System records outcome, user action, and audit metadata.

**Postconditions**:

- A generated draft is stored or discarded according to policy.
- Audit metadata records the source context, user action, and time of use.

**Alternative Flows**:

- **Alt 1a**: If retrieval scope is insufficient, the system prompts the user to refine the
  request.
- **Alt 2a**: If the workflow is marked sensitive, supervisory review is required before output is
  committed to the target process.

**Exception Flows**:

- **Ex 1**: If the model or retrieval service is unavailable, the system presents a non-AI fallback
  path and records the interruption.

**Business Rules**:

- Generated content must not overwrite original source records.
- Sensitive workflows require provenance and supervisory review controls.

**Priority**: CRITICAL

#### UC-002: Retrieve a source-backed answer from approved knowledge content

**Actor**: Frontline officer or staff user

**Preconditions**:

- User is authenticated.
- Approved knowledge repositories are available and indexed.

**Main Flow**:

1. User asks a workflow-related question.
2. System retrieves relevant approved content.
3. System generates a bounded answer with source references.
4. User opens the cited source or uses the answer as drafting support.

**Postconditions**:

- User receives a source-backed response or an explicit no-answer result.
- Retrieval and generation actions are logged.

**Alternative Flows**:

- **Alt 1a**: If confidence is low, the system returns citations without a synthesized answer.

**Exception Flows**:

- **Ex 1**: If no approved source exists, the system must not fabricate a definitive answer.

**Business Rules**:

- Only approved repositories may be queried.
- The user must be able to inspect underlying sources.

**Priority**: HIGH

#### UC-003: Create a human-reviewed outbound draft

**Actor**: Frontline officer, staff user, or supervisor

**Preconditions**:

- The target workflow allows draft generation for outbound or internal communication.
- Human approval remains mandatory before release.

**Main Flow**:

1. User provides the task context and intended audience.
2. System generates a draft response using the approved workflow and permitted context.
3. User edits the draft and selects approve, return for review, or discard.
4. If required, a supervisor reviews and approves the final output.
5. System records final disposition and audit metadata.

**Postconditions**:

- The final sent or stored output is attributable to a named human approver.
- The original generated draft remains audit-traceable.

**Alternative Flows**:

- **Alt 1a**: If the content is public-facing and high-risk, the draft is blocked from release
  until additional review is completed.

**Exception Flows**:

- **Ex 1**: If the user rejects the draft, no output is committed and the rejection reason may be
  captured.

**Business Rules**:

- AI output cannot be released automatically for material communications.
- Final accountability rests with the human approver.

**Priority**: HIGH

#### UC-004: Onboard a force using the standard control pack

**Actor**: Service Owner or force operational lead

**Preconditions**:

- National minimum control pack is published.
- Force-specific prerequisites and interfaces are identified.

**Main Flow**:

1. Force lead requests onboarding.
2. Service team validates the force against the standard onboarding pack.
3. Configuration, integration, and assurance checks are completed.
4. Any divergence is recorded for exception handling.
5. Force is approved for pilot or live use.

**Postconditions**:

- Force onboarding status, accepted controls, and exceptions are recorded.
- Reusable onboarding evidence is added to the programme repository.

**Alternative Flows**:

- **Alt 1a**: If the force needs a material deviation, an exception request is escalated.

**Exception Flows**:

- **Ex 1**: If a critical control gap exists, onboarding is blocked pending remediation.

**Business Rules**:

- Material divergence from the standard pack requires formal approval.
- No force may bypass minimum national controls for live use.

**Priority**: HIGH

### Functional Requirements Detail

#### FR-001: Workflow catalog and bounded use-case control

**Description**: The system must provide a governed catalog of approved GenAI workflows with clear
classification of allowed, restricted, and prohibited use cases.

**Relates To**: BR-001, BR-005, UC-001, UC-004

**Rationale**: Stakeholders require explicit separation between low-risk assistive use and
higher-risk operational use.

**Acceptance Criteria**:

- [ ] Given an authorized user, when they access the service, then only approved workflows for
      their role and force are shown.
- [ ] Given a prohibited use case, when a user attempts to invoke it, then the system blocks the
      request and records the attempt.
- [ ] Edge case: if a workflow status changes to suspended, the system removes it from general use
      within 15 minutes.

**Data Requirements**:

- **Inputs**: Workflow metadata, role mapping, force entitlement profile
- **Outputs**: Workflow availability decision, audit event
- **Validations**: Workflow status must be one of approved, pilot, suspended, retired

**Priority**: MUST

**Complexity**: MEDIUM

**Dependencies**: BR-001, INT-001, DR-005

**Assumptions**: Workflow governance statuses are maintained by the service team

**Stakeholder Benefit**: Supports SRO, Service Owner, SIRO, and force leads

**Traceability**: G-1, G-5; PRIN: Public value, lawfulness, and proportionality; Controlled
autonomy and policy guardrails

---

#### FR-002: Source-bounded retrieval and summarisation

**Description**: The system must generate summaries only from approved source content retrieved
through governed interfaces and within the user's authorization scope.

**Relates To**: BR-002, BR-003, UC-001, UC-002

**Rationale**: This requirement converts provenance and minimization obligations into a core system
behavior.

**Acceptance Criteria**:

- [ ] Given approved source records, when a user requests a summary, then the system returns a
      draft based only on permitted content.
- [ ] Given no approved source content, when the user requests a summary, then the system returns
      an explicit no-result or partial-response warning rather than fabricating unsupported facts.
- [ ] Edge case: if a user lacks permission for part of the source set, then the restricted content
      is excluded and the request still follows policy.

**Data Requirements**:

- **Inputs**: Source metadata, user entitlements, workflow policy
- **Outputs**: Generated summary, provenance metadata
- **Validations**: Retrieved content must come from approved repositories only

**Priority**: MUST

**Complexity**: HIGH

**Dependencies**: INT-002, INT-003, DR-001, DR-002

**Assumptions**: Approved source systems expose sufficient metadata for provenance capture

**Stakeholder Benefit**: Supports frontline users, investigations leads, legal reviewers

**Traceability**: G-2, G-3; PRIN: Lawful, purpose-bound, and minimized data use; Data quality,
provenance, and evidential integrity

---

#### FR-003: Human review, edit, approve, and discard controls

**Description**: The system must allow users to edit, approve, reject, or discard generated outputs
before any material output is committed or released.

**Relates To**: BR-001, BR-003, UC-001, UC-003

**Rationale**: Human accountability is a core programme principle and a central stakeholder demand.

**Acceptance Criteria**:

- [ ] Given a generated draft, when a user reviews it, then the interface provides edit, approve,
      reject, and discard actions.
- [ ] Given a workflow marked as requiring supervision, when the primary user selects approve, then
      the draft is routed for supervisory action rather than being finalized immediately.
- [ ] Edge case: if the user leaves the review without deciding, then the draft remains clearly
      unapproved and cannot be treated as final.

**Data Requirements**:

- **Inputs**: Generated draft, workflow policy, user role
- **Outputs**: Final disposition, edited output, audit record
- **Validations**: Final outputs must be attributable to a named human actor

**Priority**: MUST

**Complexity**: MEDIUM

**Dependencies**: FR-002, DR-002, DR-003

**Assumptions**: Workflow owners can classify which outputs require supervisory review

**Stakeholder Benefit**: Supports frontline users, supervisors, SIRO, public-interest stakeholders

**Traceability**: G-1, G-3; PRIN: Human accountability and contestability

---

#### FR-004: Output labeling and provenance visibility

**Description**: The system must label generated outputs and present provenance, citation, or
source-link information appropriate to the workflow risk level.

**Relates To**: BR-003, UC-001, UC-002, UC-003

**Rationale**: Users and reviewers must be able to distinguish source fact from generated text.

**Acceptance Criteria**:

- [ ] Given a generated response, when it is shown to the user, then it is labeled as generated or
      derived.
- [ ] Given a source-backed workflow, when the user requests explanation, then the system shows the
      underlying sources or provenance identifiers.
- [ ] Edge case: if a workflow does not permit direct citation display, then equivalent provenance
      metadata is still retained for audit and review.

**Data Requirements**:

- **Inputs**: Provenance metadata, workflow label policy
- **Outputs**: Output labels, citations, provenance views
- **Validations**: Sensitive workflows must not omit provenance storage

**Priority**: MUST

**Complexity**: MEDIUM

**Dependencies**: FR-002, DR-001, DR-002

**Assumptions**: User interfaces can display provenance without overwhelming core workflow steps

**Stakeholder Benefit**: Supports investigations, legal, public trust, and oversight needs

**Traceability**: G-3, O-3; PRIN: Traceability, transparency, and auditability

---

#### FR-005: Approved knowledge retrieval with no unsupported definitive answer

**Description**: The system must answer user questions only from approved knowledge sources and
must not present unsupported answers as definitive.

**Relates To**: BR-002, BR-004, UC-002

**Rationale**: Retrieval quality and user trust depend on bounded source use and honest uncertainty.

**Acceptance Criteria**:

- [ ] Given an approved knowledge source, when the user asks a supported question, then the system
      returns an answer with supporting references.
- [ ] Given insufficient supporting information, when the user asks a question, then the system
      returns a no-answer, low-confidence response, or referral path.
- [ ] Edge case: if the source content is stale beyond the allowed freshness threshold, then the
      response is blocked or flagged.

**Data Requirements**:

- **Inputs**: Approved source index, freshness metadata, user query
- **Outputs**: Response, source references, no-answer indicator
- **Validations**: Unapproved repositories must not be included in the retrieval set

**Priority**: MUST

**Complexity**: HIGH

**Dependencies**: INT-003, NFR-C-002, DR-001

**Assumptions**: Approved knowledge content exists for the initial pilot workflows

**Stakeholder Benefit**: Supports frontline users, service owners, public-interest safeguards

**Traceability**: G-2, G-4; PRIN: Data quality, provenance, and evidential integrity

---

#### FR-006: Supervisory review for sensitive workflows

**Description**: The system must enforce supervisory review for workflows classified as sensitive,
including evidential, intelligence, or high-impact public-facing content.

**Relates To**: BR-003, BR-004, UC-001, UC-003

**Rationale**: High-impact use requires stronger assurance and control than low-risk drafting.

**Acceptance Criteria**:

- [ ] Given a workflow marked sensitive, when a user submits a draft, then the system routes it to
      a supervisor before finalization.
- [ ] Given a supervisor rejection, when the draft is returned, then the original user can revise
      or discard it with full audit trace.
- [ ] Edge case: if no eligible supervisor is available, then the system blocks completion and
      presents a defined fallback path.

**Data Requirements**:

- **Inputs**: Workflow sensitivity class, supervisor role assignments
- **Outputs**: Review task, approval decision, audit record
- **Validations**: Sensitive workflows must not bypass supervisory gates

**Priority**: MUST

**Complexity**: MEDIUM

**Dependencies**: INT-001, FR-003, DR-003

**Assumptions**: Sensitive workflow definitions are agreed before live use

**Stakeholder Benefit**: Supports investigations, legal, CPS, SIRO

**Traceability**: G-3, G-4; PRIN: Human accountability and contestability; Controlled autonomy and
policy guardrails

---

#### FR-007: User feedback, override, and quality signal capture

**Description**: The system must capture accept, edit, reject, and override behavior as quality and
assurance signals.

**Relates To**: BR-002, BR-006, UC-001, UC-003

**Rationale**: Continuous monitoring depends on measurable user behavior, not only uptime metrics.

**Acceptance Criteria**:

- [ ] Given any generated output, when the user acts on it, then the action is recorded as accept,
      edit, reject, or discard.
- [ ] Given repeated low-quality outcomes, when threshold rules are exceeded, then the service can
      surface alerts or reports to service management.
- [ ] Edge case: if the user declines to provide qualitative feedback, then the core disposition is
      still captured.

**Data Requirements**:

- **Inputs**: User action, workflow identifier, output identifier
- **Outputs**: Feedback event, quality metrics feed
- **Validations**: Feedback records must be attributable and timestamped

**Priority**: SHOULD

**Complexity**: MEDIUM

**Dependencies**: DR-003, NFR-M-001

**Assumptions**: Pilot teams will review quality metrics at least monthly

**Stakeholder Benefit**: Supports Service Owner, finance, assurance reviewers

**Traceability**: G-2, G-6; PRIN: Continuous monitoring, drift response, and improvement

---

#### FR-008: Force-local configuration within national guardrails

**Description**: The system must allow force-specific configuration of approved workflows, user
groups, and onboarding parameters without altering core national controls.

**Relates To**: BR-005, UC-004

**Rationale**: This is the operational compromise between local flexibility and national reuse.

**Acceptance Criteria**:

- [ ] Given an onboarded force, when an authorized configurator updates force-local settings, then
      only permitted configurable fields can be changed.
- [ ] Given an attempted change to a protected national control, when submitted, then the system
      blocks the change and records it for review.
- [ ] Edge case: if a force requests a material control deviation, then the service triggers the
      formal exception process.

**Data Requirements**:

- **Inputs**: Force profile, configuration request, policy rules
- **Outputs**: Updated configuration, exception request, audit event
- **Validations**: Protected national controls must be immutable to local administrators

**Priority**: MUST

**Complexity**: HIGH

**Dependencies**: BR-005, DR-005, INT-001

**Assumptions**: A national minimum control set is agreed by the architecture and governance boards

**Stakeholder Benefit**: Supports force leads, Service Owner, national oversight bodies

**Traceability**: G-5, O-5; PRIN: Interoperability and federation

---

#### FR-009: Audit and transparency inquiry support

**Description**: The system must provide authorized reviewers with the ability to reconstruct
material workflow activity for audit, investigation, and transparency purposes.

**Relates To**: BR-001, BR-004, BR-006, UC-003, UC-004

**Rationale**: Reviewers need more than raw logs; they need a usable reconstruction trail.

**Acceptance Criteria**:

- [ ] Given an authorized reviewer, when they search by output, workflow, or user identifier, then
      the system returns linked audit, provenance, and disposition records.
- [ ] Given a transparency or incident review, when records are exported, then the export includes
      the required metadata and integrity markers.
- [ ] Edge case: if part of the data is restricted, then the system redacts according to policy
      while preserving reviewability for authorized users.

**Data Requirements**:

- **Inputs**: Search parameters, role entitlements
- **Outputs**: Review record set, export package
- **Validations**: Only authorized roles may access detailed reconstruction data

**Priority**: MUST

**Complexity**: HIGH

**Dependencies**: NFR-C-002, DR-001, DR-003, INT-005

**Assumptions**: Review roles and access policies are agreed during design

**Stakeholder Benefit**: Supports SIRO, legal, security, oversight stakeholders

**Traceability**: G-1, G-4, G-6; PRIN: Traceability, transparency, and auditability

---

#### FR-010: Safe-use guidance and role-based training support

**Description**: The system must provide in-product guidance, training references, and role-based
safe-use prompts aligned to workflow sensitivity.

**Relates To**: BR-002, BR-003, UC-001, UC-002, UC-003

**Rationale**: Adoption and safe operation depend on users understanding what the system can and
cannot do.

**Acceptance Criteria**:

- [ ] Given a user entering a workflow for the first time, when they begin, then the system
      presents concise safe-use guidance for that workflow.
- [ ] Given a sensitive workflow, when the user proceeds, then the system reinforces review and
      accountability obligations.
- [ ] Edge case: if guidance is updated, then the latest approved guidance is shown without code
      changes being required.

**Data Requirements**:

- **Inputs**: Role profile, workflow classification, guidance content
- **Outputs**: Guidance display, acknowledgement event where required
- **Validations**: Guidance version must be traceable

**Priority**: SHOULD

**Complexity**: LOW

**Dependencies**: DR-005, NFR-U-001

**Assumptions**: Training materials are authored by service and change teams before rollout

**Stakeholder Benefit**: Supports frontline users, learning leads, governance reviewers

**Traceability**: G-2, G-3; PRIN: Performance, accessibility, and usability

---

## Non-Functional Requirements (NFRs)

### Performance Requirements

#### NFR-P-001: Interactive response time

**Requirement**: The service must return an initial result for interactive assistive workflows
within < 5 seconds at the 95th percentile under pilot load, excluding approved long-running batch
tasks.

**Rationale**: Frontline and analytical users will reject slow systems and lose time savings if
latency is excessive.

**Measurement Method**: Synthetic monitoring and production telemetry using workflow-specific
latency measures.

**Load Conditions**:

- Peak load: 300 concurrent interactive users during pilot phases
- Average load: 25,000 interactive requests per day across pilot forces
- Data volume: Approved source indexes and audit data available at pilot scale

**Acceptance Criteria**:

- [ ] Under representative pilot load, 95% of interactive requests complete in < 5 seconds.
- [ ] Under the same load, 99% of requests complete in < 10 seconds.
- [ ] If the latency target is breached for 15 continuous minutes, an operational alert is raised.

**Priority**: HIGH

**Traceability**: G-2; PRIN: Performance, accessibility, and usability

---

#### NFR-P-002: Throughput and concurrency

**Requirement**: The service must sustain at least 20 generated or retrieval-assisted transactions
per second at pilot peak and 3x that volume at scale without architectural redesign.

**Rationale**: National reuse depends on handling growth without redesigning the core service.

**Acceptance Criteria**:

- [ ] Load testing demonstrates 20 transactions per second at pilot peak with no material error-rate
      increase.
- [ ] Capacity plan shows how 60 transactions per second can be supported through scaling rather
      than redesign.
- [ ] Load-test reports are reviewed before onboarding additional forces.

**Priority**: HIGH

**Traceability**: G-2, G-5; PRIN: Resilience, continuity, and safe degradation; Maintainability,
portability, and change readiness

---

### Availability and Resilience Requirements

#### NFR-A-001: Availability target

**Requirement**: The live service must achieve > 99.9% availability measured monthly, excluding
approved planned maintenance windows.

**Rationale**: Operational workflows require a dependable service if users are to adopt it.

**Acceptance Criteria**:

- [ ] Monthly service reports show > 99.9% availability for live operation.
- [ ] Planned maintenance is scheduled outside agreed policing peak windows except by approved
      exception.
- [ ] Service reporting distinguishes planned from unplanned downtime.

**Priority**: HIGH

**Traceability**: G-1, G-2; PRIN: Resilience, continuity, and safe degradation

---

#### NFR-A-002: Disaster recovery

**Requirement**: The service must support a recovery point objective of < 15 minutes and a recovery
time objective of < 4 hours for critical service data and configuration.

**Rationale**: The service must recover from platform or regional failure without unacceptable data
or configuration loss.

**Acceptance Criteria**:

- [ ] Backup and recovery tests demonstrate recovery point and recovery time targets.
- [ ] Critical configuration, audit data, and workflow metadata are included in recovery scope.
- [ ] Recovery procedures are reviewed and exercised at least twice per year.

**Priority**: HIGH

**Traceability**: G-1, G-4; PRIN: Resilience, continuity, and safe degradation

---

#### NFR-A-003: Safe degradation and fallback

**Requirement**: The service must degrade safely when model, retrieval, or integration components
fail, and must provide a non-AI fallback path for critical workflows.

**Rationale**: Users must not be trapped by AI dependency failure in operational contexts.

**Acceptance Criteria**:

- [ ] When generation fails, the user is shown a defined fallback or manual pathway.
- [ ] Partial or degraded results are clearly labeled and never presented as authoritative final
      outputs.
- [ ] Failure modes and fallback behaviors are documented in operational runbooks.

**Priority**: MUST

**Traceability**: G-1, G-3; PRIN: Resilience, continuity, and safe degradation

---

### Scalability Requirements

#### NFR-S-001: Horizontal scale and growth support

**Requirement**: The service must support horizontal scaling and operational growth from pilot scope
to at least five forces without code redesign of the core service pattern.

**Rationale**: This supports the national reuse target and avoids costly redesign between pilot and
expansion.

**Growth Projections**:

- Year 1: 5 pilot or early adopter forces, 3 live workflows, 25,000 requests/day
- Year 2: 10 forces, 8 live workflows, 75,000 requests/day
- Year 3: 15 forces, 12 live workflows, 150,000 requests/day

**Scaling Triggers**: Scale action plans must exist for sustained CPU, memory, queue-depth, or
latency breaches defined during design.

**Acceptance Criteria**:

- [ ] Capacity planning covers the three-year growth profile.
- [ ] Scaling tests show that additional demand can be absorbed without functional redesign.
- [ ] The onboarding pack includes scaling thresholds and review points.

**Priority**: HIGH

**Traceability**: G-5, O-5; PRIN: Maintainability, portability, and change readiness

---

#### NFR-S-002: Data volume scaling

**Requirement**: The service must support growth to at least 5 TB of indexed source metadata,
audit records, and generated artifact storage over three years with tiered retention and retrieval
controls.

**Rationale**: Auditability and force onboarding will drive rapid growth in metadata and log volume.

**Acceptance Criteria**:

- [ ] Storage and retention design supports 5 TB total managed data over three years.
- [ ] Query performance for audit and provenance data remains within agreed operational limits at
      projected Year 3 volume.
- [ ] Archival and retrieval behavior is documented by data class.

**Priority**: SHOULD

**Traceability**: G-5; PRIN: Privacy, confidentiality, and data sovereignty

---

### Security Requirements

#### NFR-SEC-001: Workforce authentication and privileged MFA

**Requirement**: All users must authenticate through an approved workforce identity service, and
multi-factor authentication must be enforced for privileged, administrative, and remote access
operations.

**Rationale**: Strong identity controls are required for policing data and administrative functions.

**Acceptance Criteria**:

- [ ] All interactive access is federated through the approved workforce identity service.
- [ ] Privileged and administrative functions require MFA.
- [ ] Session timeouts and re-authentication rules are enforced for sensitive actions.

**Priority**: MUST

**Traceability**: G-4; PRIN: Security by design and least privilege

---

#### NFR-SEC-002: Role-based and least-privilege authorization

**Requirement**: The service must implement role-based authorization with least privilege and
separation of duties for users, administrators, reviewers, and support personnel.

**Rationale**: Different actors need distinct rights, especially where sensitive data or control
changes are involved.

**Acceptance Criteria**:

- [ ] User roles, reviewer roles, and administrative roles are distinct and documented.
- [ ] Force-local administrators cannot change protected national controls.
- [ ] Temporary privilege elevation requires approval, traceability, and expiry.

**Priority**: MUST

**Traceability**: G-1, G-4, G-5; PRIN: Security by design and least privilege

---

#### NFR-SEC-003: Encryption and protected data handling

**Requirement**: Sensitive data, prompts, outputs, and audit records must be protected in transit
and at rest using approved cryptographic controls and managed keys.

**Rationale**: Policing data and AI artifacts require strong confidentiality protections.

**Acceptance Criteria**:

- [ ] All network communication carrying service data uses approved encrypted transport.
- [ ] Stored sensitive data, backups, and generated artifacts are encrypted at rest.
- [ ] Key access and key-use events are restricted and auditable.

**Priority**: MUST

**Traceability**: G-4; PRIN: Privacy, confidentiality, and data sovereignty; Security by design and
least privilege

---

#### NFR-SEC-004: Secrets and configuration protection

**Requirement**: Secrets, credentials, and protected runtime configuration must not be stored in
source code or unmanaged configuration files and must be rotated under policy.

**Rationale**: Prompt assets, service credentials, and policy configuration are sensitive assets.

**Acceptance Criteria**:

- [ ] No production secrets or credentials are committed to code repositories.
- [ ] Secrets and protected runtime settings are retrieved through approved managed controls.
- [ ] Rotation and access-review procedures exist for privileged secrets and service identities.

**Priority**: MUST

**Traceability**: G-4; PRIN: Security by design and least privilege

---

#### NFR-SEC-005: Security testing and AI-specific misuse resistance

**Requirement**: The service must undergo security testing that includes prompt manipulation, data
exfiltration scenarios, over-privileged tool use, dependency vulnerability scanning, and annual
independent penetration testing before scale-up.

**Rationale**: Conventional testing alone is insufficient for GenAI-enabled services.

**Acceptance Criteria**:

- [ ] Pre-production testing includes AI-specific misuse cases and remediation tracking.
- [ ] Critical vulnerabilities are remediated before release; high vulnerabilities within 7 days.
- [ ] Independent penetration testing is completed before scale-up approval.

**Priority**: MUST

**Traceability**: G-4, G-6; PRIN: Security by design and least privilege; Assurance by default

---

### Compliance and Regulatory Requirements

#### NFR-C-001: Lawfulness, privacy, and rights compliance

**Requirement**: The service must support compliance with UK GDPR, Data Protection Act 2018, Human
Rights Act 1998, Equality Act 2010, and relevant policing governance obligations for each live
workflow.

**Rationale**: Lawfulness and proportionality are foundational constraints, not optional features.

**Acceptance Criteria**:

- [ ] Each live workflow has a documented lawful basis, proportionality rationale, and rights
      assessment.
- [ ] DPIA and equality-impact considerations are completed where required before go-live.
- [ ] Workflow changes that materially affect data use or rights impact trigger reassessment.

**Priority**: MUST

**Traceability**: G-1, G-3, G-4; PRIN: Public value, lawfulness, and proportionality; Lawful,
purpose-bound, and minimized data use

---

#### NFR-C-002: Audit logging, records retention, and disclosure readiness

**Requirement**: The service must maintain tamper-evident audit records sufficient to support
incident review, transparency requests, internal assurance, and records-management obligations.

**Rationale**: Stakeholders must be able to reconstruct material activity and manage disclosure.

**Acceptance Criteria**:

- [ ] Audit records capture who, what, when, where, and result for material actions.
- [ ] Audit and security logs are retained for at least 7 years unless a more specific legal policy
      applies.
- [ ] Audit data can be exported in a controlled format for authorized review or disclosure.

**Priority**: MUST

**Traceability**: G-1, G-4, G-6; PRIN: Traceability, transparency, and auditability

---

#### NFR-C-003: Transparency and public-accountability support

**Requirement**: The service must support generation of transparency records and public-accountable
descriptions of AI use, decision boundaries, and safeguards for in-scope use cases.

**Rationale**: Public trust depends on explainable governance, especially in policing contexts.

**Acceptance Criteria**:

- [ ] For each live workflow, a plain-language description of purpose, scope, and safeguards exists.
- [ ] The service can produce evidence needed for internal transparency records or public reporting.
- [ ] Material changes to use-case scope trigger update of transparency documentation.

**Priority**: SHOULD

**Traceability**: G-1, G-6; PRIN: Traceability, transparency, and auditability

---

#### NFR-C-004: Records management and retention enforcement

**Requirement**: The service must enforce retention, deletion, legal-hold, and archival behavior
for prompts, outputs, logs, and derived records according to data class and lawful purpose.

**Rationale**: AI artifacts cannot become unmanaged data exhaust.

**Acceptance Criteria**:

- [ ] Retention rules are defined by data class and implemented technically.
- [ ] Legal-hold and investigation hold processes can suspend routine deletion where authorized.
- [ ] Deletion or archival actions are auditable and reversible only through controlled processes.

**Priority**: MUST

**Traceability**: G-3, G-4; PRIN: Privacy, confidentiality, and data sovereignty

---

### Usability Requirements

#### NFR-U-001: Operational usability

**Requirement**: The service must be usable in frontline and analytical contexts with minimal extra
interaction burden and clear indication of uncertainty or next-step actions.

**Rationale**: Productivity gains will not materialize if the interaction model is awkward or
ambiguous.

**Acceptance Criteria**:

- [ ] Pilot users can complete target workflows without more than two additional steps compared with
      the agreed future-state workflow design.
- [ ] User research shows a usefulness score of at least 70% during pilot phases.
- [ ] Uncertainty, low-confidence conditions, or review requirements are shown clearly in the UI.

**Priority**: HIGH

**Traceability**: G-2; PRIN: Performance, accessibility, and usability

---

#### NFR-U-002: Accessibility and inclusive design

**Requirement**: The service must meet WCAG 2.2 AA and relevant UK public-sector accessibility
obligations for all user-facing workflows in scope.

**Rationale**: Accessibility is mandatory for public-sector digital services and workforce tools.

**Acceptance Criteria**:

- [ ] Keyboard-only navigation is supported for all core functions.
- [ ] Screen-reader compatibility is verified for critical workflows.
- [ ] Accessibility testing includes automated and manual review before release.

**Priority**: MUST

**Traceability**: G-2, G-6; PRIN: Performance, accessibility, and usability

---

### Maintainability and Supportability Requirements

#### NFR-M-001: Observability and operational telemetry

**Requirement**: The service must emit structured logs, metrics, traces, and workflow-quality
signals sufficient to support troubleshooting, capacity planning, assurance, and incident response.

**Rationale**: Service teams cannot manage what they cannot observe.

**Acceptance Criteria**:

- [ ] Structured operational telemetry exists for request flow, latency, errors, and dependency
      health.
- [ ] Workflow-quality metrics include accept, edit, reject, and override behaviors.
- [ ] Alerts are defined for service health and critical assurance indicators.

**Priority**: MUST

**Traceability**: G-4, G-6; PRIN: Continuous monitoring, drift response, and improvement;
Observability and operational excellence

---

#### NFR-M-002: Documentation and runbooks

**Requirement**: The service must maintain current documentation for architecture, interfaces,
operations, troubleshooting, and user guidance, updated within 5 working days of material change.

**Rationale**: Multi-force rollout and supplier governance require dependable operational
documentation.

**Acceptance Criteria**:

- [ ] Architecture, operational, and user documentation exist before go-live.
- [ ] Runbooks cover deployment, rollback, incident response, and fallback procedures.
- [ ] Material changes trigger documentation update within 5 working days.

**Priority**: HIGH

**Traceability**: G-1, G-5; PRIN: Maintainability, portability, and change readiness

---

### Portability and Interoperability Requirements

#### NFR-I-001: Versioned interface standards

**Requirement**: All external and internal integration contracts must be versioned, published, and
designed to support backward-compatible change where feasible.

**Rationale**: Interoperability and national reuse depend on stable, governed interfaces.

**Acceptance Criteria**:

- [ ] Integration contracts are documented and versioned before dependent build work begins.
- [ ] Material interface changes follow a defined review and deprecation process.
- [ ] No dependent system requires direct database access to service-owned data.

**Priority**: MUST

**Traceability**: G-5; PRIN: Interoperability and federation; Standard interfaces and loose
coupling

---

#### NFR-I-002: Data portability and controlled export

**Requirement**: Authorized administrators and reviewers must be able to export required service
data, audit records, and workflow artifacts in approved structured formats.

**Rationale**: Portability supports audit, legal review, supplier exit, and service continuity.

**Acceptance Criteria**:

- [ ] Export formats are documented for audit records, workflow outcomes, and onboarding metadata.
- [ ] Export processes preserve provenance and integrity metadata where available.
- [ ] Export permissions are restricted to authorized roles and fully logged.

**Priority**: SHOULD

**Traceability**: G-5, G-6; PRIN: Maintainability, portability, and change readiness

---

## Integration Requirements

### External System Integrations

#### INT-001: Integration with workforce identity service

**Purpose**: Provide authentication, entitlement enforcement, and reviewer routing.

**Integration Type**: Real-time identity and access integration

**Rationale**: The service must align to approved workforce identity controls.

**Data Exchanged**:

- **From This System to External System**: Authentication requests, authorization checks
- **From External System to This System**: Identity assertions, role and group claims

**Integration Pattern**: Request/response

**Authentication**: Approved enterprise trust integration

**Error Handling**: Retry where safe; fail closed for privileged operations; user-facing fallback
message for identity outage

**SLA**: Authorization decisions available in < 2 seconds for 99% of requests

**Owner**: Identity and Access Management Team

**Acceptance Criteria**:

- [ ] Authentication and authorization work for all user roles in scope.
- [ ] Privileged roles are distinguished from standard user roles.
- [ ] Identity outage behavior follows approved safe-failure rules.

**Priority**: CRITICAL

**Traceability**: G-1, G-4, G-5; PRIN: Security by design and least privilege

---

#### INT-002: Integration with case and records management systems

**Purpose**: Retrieve approved case context and return human-approved outputs where permitted.

**Integration Type**: Real-time API or governed asynchronous exchange

**Rationale**: The service must work within existing operational systems rather than replace them.

**Data Exchanged**:

- **From This System to External System**: Approved final outputs, workflow status markers
- **From External System to This System**: Case metadata, bounded source content, record references

**Integration Pattern**: Request/response for retrieval; asynchronous for committed outputs where
appropriate

**Authentication**: Service-to-service trust using approved enterprise controls

**Error Handling**: Timeouts, retries for transient failure, dead-letter handling for asynchronous
flows

**SLA**: Retrieval or commit success rate > 99.5% for scheduled live hours

**Owner**: Case Systems Product Team

**Acceptance Criteria**:

- [ ] Only approved fields and records are retrievable by the service.
- [ ] Generated outputs cannot overwrite source records automatically.
- [ ] Integration errors are visible to service operations and do not create silent data loss.

**Priority**: CRITICAL

**Traceability**: G-2, G-3; PRIN: Data quality, provenance, and evidential integrity

---

#### INT-003: Integration with approved knowledge and policy repositories

**Purpose**: Support source-backed retrieval and guidance answers.

**Integration Type**: Real-time retrieval and periodic synchronization of approved content metadata

**Rationale**: Retrieval use cases depend on accurate and approved source content.

**Data Exchanged**:

- **From This System to External System**: Retrieval queries, indexing or sync requests
- **From External System to This System**: Approved content, metadata, freshness markers

**Integration Pattern**: Search and retrieval plus scheduled indexing

**Authentication**: Approved service integration controls

**Error Handling**: Failed syncs trigger alerting; stale content is flagged or excluded

**SLA**: Approved content freshness reflected in the service within 4 hours of repository update

**Owner**: Knowledge Management Team

**Acceptance Criteria**:

- [ ] Only approved repositories can be indexed or queried.
- [ ] Content freshness and repository ownership metadata are preserved.
- [ ] Stale or retired content is excluded or flagged according to policy.

**Priority**: HIGH

**Traceability**: G-2, G-4; PRIN: Lawful, purpose-bound, and minimized data use

---

#### INT-004: Integration with security monitoring and incident management services

**Purpose**: Feed security telemetry, alerts, and incident workflows into established operational
control systems.

**Integration Type**: Event-driven and API-driven

**Rationale**: The service must participate in existing security and incident-management processes.

**Data Exchanged**:

- **From This System to External System**: Security events, alerts, audit extracts
- **From External System to This System**: Incident identifiers, response workflow updates

**Integration Pattern**: Event-driven notification and controlled query

**Authentication**: Approved service authentication and authorization controls

**Error Handling**: Queue and retry with alerting on event-delivery failure

**SLA**: Critical security events forwarded within 60 seconds of detection

**Owner**: Cyber Operations and Service Operations

**Acceptance Criteria**:

- [ ] Critical security and privacy events are forwarded automatically.
- [ ] Failed event delivery is visible and recoverable.
- [ ] Incident identifiers can be correlated with service audit records.

**Priority**: CRITICAL

**Traceability**: G-4; PRIN: Security by design and least privilege; Continuous monitoring, drift
response, and improvement

---

#### INT-005: Integration with reporting, assurance, and transparency repositories

**Purpose**: Publish governed operational, benefits, and assurance data to authorised reporting and
review channels.

**Integration Type**: Scheduled reporting export and query-based retrieval

**Rationale**: Scale-up decisions and oversight need consistent reporting data.

**Data Exchanged**:

- **From This System to External System**: KPI metrics, audit extracts, assurance evidence bundles
- **From External System to This System**: Review requests, reporting schedules

**Integration Pattern**: Scheduled export with controlled pull access

**Authentication**: Approved reviewer and service integration controls

**Error Handling**: Failed exports trigger retry and manual escalation if unresolved within 24 hours

**SLA**: Monthly and quarterly reporting packages delivered by agreed governance deadlines

**Owner**: Programme Management Office and Service Owner

**Acceptance Criteria**:

- [ ] KPI and assurance exports include complete metadata and reporting period coverage.
- [ ] Reviewers can retrieve the latest approved reporting package.
- [ ] Export failures are tracked to closure.

**Priority**: HIGH

**Traceability**: G-1, G-6; PRIN: Traceability, transparency, and auditability

---

#### INT-006: Controlled downstream export for justice and oversight partners

**Purpose**: Support controlled export or sharing of human-approved outputs and related metadata
with justice or oversight partners where authorized.

**Integration Type**: Governed asynchronous exchange

**Rationale**: Downstream partners may require outputs or evidence packs without taking a direct
dependency on service internals.

**Data Exchanged**:

- **From This System to External System**: Human-approved outputs, provenance metadata, export
  manifest
- **From External System to This System**: Acknowledgement or rejection of import package

**Integration Pattern**: Batch or event-based exchange

**Authentication**: Approved cross-organisational trust controls

**Error Handling**: Delivery confirmation, reconciliation, and manual exception handling for failed
transfers

**SLA**: Routine export available within 30 minutes of approved request unless policy requires delay

**Owner**: Justice Integration Lead

**Acceptance Criteria**:

- [ ] Only authorized, human-approved outputs are exportable.
- [ ] Export packages preserve provenance and review metadata.
- [ ] Failed or rejected transfers are reconcilable and auditable.

**Priority**: SHOULD

**Traceability**: G-3, G-6; PRIN: Traceability, transparency, and auditability

---

## Data Requirements

### DR-001: Provenance data model

**Description**: The service must maintain a provenance record linking generated outputs to source
systems, source references, workflow identifiers, and generation events where required by workflow
policy.

**Rationale**: Provenance is central to evidential integrity and challenge handling.

**Acceptance Criteria**:

- [ ] Each in-scope generated output has an associated provenance record or a justified exception.
- [ ] Provenance records are queryable by workflow, output, and source reference.
- [ ] Sensitive workflow provenance is retained according to policy.

**Priority**: MUST

**Traceability**: G-3, O-3; PRIN: Data quality, provenance, and evidential integrity

---

### DR-002: Generated output record and labeling model

**Description**: The service must store generated outputs, human edits, approval states, and final
dispositions with explicit labeling of draft, approved, rejected, or discarded status.

**Rationale**: Output lifecycle control is necessary for audit, rework analysis, and accountability.

**Acceptance Criteria**:

- [ ] Output status transitions are defined and enforced.
- [ ] Human edits and final disposition are distinguishable from the original generated draft.
- [ ] Discarded outputs follow retention rules and cannot be mistaken for approved outputs.

**Priority**: MUST

**Traceability**: G-2, G-3; PRIN: Human accountability and contestability

---

### DR-003: Audit, access, and review event records

**Description**: The service must store audit events for access, retrieval, generation, review,
configuration change, export, and incident-relevant activity.

**Rationale**: Audit coverage is needed for security, privacy, and operational review.

**Acceptance Criteria**:

- [ ] Material user and service actions generate audit events with identity, action, timestamp, and
      result.
- [ ] Audit events support correlation across service operations and security tooling.
- [ ] Tamper-evidence or equivalent integrity protection is applied to retained audit data.

**Priority**: MUST

**Traceability**: G-1, G-4; PRIN: Traceability, transparency, and auditability

---

### DR-004: Data classification, retention, and minimization rules

**Description**: The service must classify and handle prompts, retrieved content, outputs, and logs
according to sensitivity, lawful purpose, retention period, and minimization policy.

**Rationale**: AI artifacts cannot be treated as ungoverned temporary data.

**Acceptance Criteria**:

- [ ] Each major data class has a defined classification and retention rule.
- [ ] Prompt and output retention is limited by use-case policy and legal obligation.
- [ ] Sensitive fields can be excluded, masked, or minimized where policy requires.

**Priority**: MUST

**Traceability**: G-3, G-4; PRIN: Lawful, purpose-bound, and minimized data use; Privacy,
confidentiality, and data sovereignty

---

### DR-005: Force configuration and control-pack data model

**Description**: The service must maintain force-specific onboarding metadata, configuration
profiles, enabled workflows, exception status, and versioned control-pack assignments.

**Rationale**: Federated onboarding requires structured configuration and exception traceability.

**Acceptance Criteria**:

- [ ] Each onboarded force has a versioned configuration profile.
- [ ] Configuration records identify inherited national controls and local settings separately.
- [ ] Exceptions are linked to the force profile and approval outcome.

**Priority**: MUST

**Traceability**: G-5, O-5; PRIN: Interoperability and federation

---

### DR-006: Data migration and onboarding support

**Description**: The service must support controlled onboarding of source metadata, configuration,
and workflow definitions from pilot to additional forces without loss of lineage or control-state
history.

**Rationale**: Reuse requires structured onboarding rather than manual recreation.

**Acceptance Criteria**:

- [ ] Onboarding data migration is documented and repeatable.
- [ ] Migration validation confirms integrity of force profile, workflow definitions, and access
      mappings.
- [ ] Rollback procedures exist for failed onboarding data changes.

**Priority**: SHOULD

**Traceability**: G-5; PRIN: Maintainability, portability, and change readiness

### Data Entities

#### Entity 1: Workflow

**Description**: Represents an approved GenAI workflow and its governance metadata.

**Attributes**:
| Attribute | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| workflow_id | UUID | Yes | Unique workflow identifier | Primary key |
| workflow_name | String(200) | Yes | Human-readable workflow name | Not null |
| workflow_status | Enum | Yes | Approval state | approved, pilot, suspended, retired |
| sensitivity_class | Enum | Yes | Risk classification | low, medium, high, sensitive |
| control_pack_version | String(50) | Yes | Associated control pack | Not null |

**Relationships**:

- One-to-many with Generated Output via workflow_id
- One-to-many with Force Profile via enablement assignment

**Data Volume**: Year 1 < 25 workflows; Year 3 < 150 workflows

**Access Patterns**: Lookup by force, role, status, and risk class

**Data Classification**: INTERNAL

**Data Retention**: Retained for service life plus 7 years of audit history

#### Entity 2: Generated Output

**Description**: Represents a generated draft and its lifecycle state.

**Attributes**:
| Attribute | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| output_id | UUID | Yes | Unique output identifier | Primary key |
| workflow_id | UUID | Yes | Associated workflow | Foreign key |
| output_status | Enum | Yes | Draft lifecycle state | generated, edited, approved, rejected, discarded |
| generated_at | Timestamp | Yes | Generation timestamp | Indexed |
| final_actor_id | String(100) | No | Human finalizer identifier | Required when approved |

**Relationships**:

- Many-to-one with Workflow via workflow_id
- One-to-one or one-to-many with Provenance Record via output_id

**Data Volume**: Year 1 up to 5 million records; Year 3 up to 40 million records

**Access Patterns**: Lookup by workflow, actor, date, and status

**Data Classification**: CONFIDENTIAL

**Data Retention**: Retention by workflow class and legal policy

#### Entity 3: Provenance Record

**Description**: Represents source references and derivation metadata for a generated output.

**Attributes**:
| Attribute | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| provenance_id | UUID | Yes | Unique provenance identifier | Primary key |
| output_id | UUID | Yes | Associated generated output | Foreign key |
| source_system | String(100) | Yes | Source system name | Not null |
| source_reference | String(255) | Yes | Source record or document reference | Indexed |
| provenance_type | Enum | Yes | Provenance style | citation, metadata-only, restricted |

**Relationships**:

- Many-to-one with Generated Output via output_id

**Data Volume**: Year 1 up to 10 million references; Year 3 up to 80 million references

**Access Patterns**: Query by output, source system, source reference

**Data Classification**: CONFIDENTIAL

**Data Retention**: Retained in line with output and audit policy

#### Entity 4: Force Profile

**Description**: Represents force-level onboarding, configuration, and exception data.

**Attributes**:
| Attribute | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| force_profile_id | UUID | Yes | Unique profile identifier | Primary key |
| force_code | String(20) | Yes | Force identifier | Unique |
| control_pack_version | String(50) | Yes | Assigned control pack version | Not null |
| configuration_status | Enum | Yes | Onboarding state | planned, pilot, live, suspended |
| exception_count | Integer | Yes | Active material exceptions | >= 0 |

**Relationships**:

- Many-to-many with Workflow via enabled-workflow mapping

**Data Volume**: Year 1 < 10 profiles; Year 3 < 50 profiles

**Access Patterns**: Lookup by force, status, control-pack version

**Data Classification**: INTERNAL

**Data Retention**: Service life plus 7 years

### Data Quality Requirements

**Data Accuracy**: Provenance references, user actions, and workflow statuses must have an error
rate below 0.1% in monthly sampled records.

**Data Completeness**: Required audit, provenance, and output-status fields must be populated for
100% of material workflow transactions.

**Data Consistency**: Cross-system reconciliation for committed outputs and onboarding state must
run daily for live workflows.

**Data Timeliness**: Approved knowledge and policy content freshness must be reflected in the
service within 4 hours of source update unless a documented exception applies.

**Data Lineage**: Lineage must be retained from approved source content to generated output and
exported artifact where required by workflow class.

### Data Migration Requirements

**Migration Scope**: Force onboarding metadata, workflow definitions, configuration profiles, and
approved source-index metadata required for new-force rollout

**Migration Strategy**: Phased onboarding with validation checkpoints and rollback at each force
onboarding step

**Data Transformation**: Local source references must be mapped to the national provenance and
workflow model without losing original identifiers

**Data Validation**: Force onboarding is not complete until configuration, entitlement, and
provenance validation checks pass

**Rollback Plan**: Each onboarding step must be reversible to the previous approved control-pack
state

**Migration Timeline**: Force onboarding cutovers should occur in approved windows and avoid
critical policing peak periods

---

## Constraints and Assumptions

### Technical Constraints

**TC-001**: The service must integrate with existing workforce identity, case, and knowledge
systems rather than replacing them.

**TC-002**: No dependent system may require direct database access to service-owned data stores.

**TC-003**: Force-local configuration must operate within a national minimum control pack and
exception process.

### Business Constraints

**BC-001**: Initial live rollout must remain limited to assistive workflows and may not include
fully autonomous operational decision-making.

**BC-002**: The first three live workflows must be ready for approval by 2026-12-31.

**BC-003**: The initial programme phase is planned within an indicative cap of £3.7M for delivery
through first live operation.

### Assumptions

**A-001**: Pilot forces will provide operational SMEs, pilot users, and local service support by
Q2 2026.

**A-002**: In-scope source systems will expose sufficient interfaces and metadata to support
retrieval, provenance, and audit requirements.

**A-003**: Legal, privacy, and security reviewers will participate in a regular integrated
assurance cadence rather than isolated late-stage review.

**Validation Plan**: Assumptions will be validated through discovery workshops, interface
assessments, pilot onboarding checkpoints, and assurance-board review before build commitments are
finalized.

---

## Success Criteria and KPIs

### Business Success Metrics

| Metric | Baseline | Target | Timeline | Measurement Method |
|--------|----------|--------|----------|-------------------|
| Approved live workflows | 0 | 3 | 2026-12-31 | Governance tracker and go-live approvals |
| Average admin task time | 45 minutes | 36 minutes | 2027-03-31 | Time-and-motion study and workflow analytics |
| Annualized hours saved | 0 | > 25,000 hours | 2027-09-30 | Benefits register validated by pilot data |
| Forces onboarded on standard pack | 0 | 5 | 2027-06-30 | Onboarding register and exception log |
| Material AI-attributable privacy/security incidents | 0 live baseline | 0 | First 12 live months | Incident and privacy review records |

### Technical Success Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Interactive response time (p95) | < 5 seconds | Application telemetry and load tests |
| System availability | > 99.9% | Uptime monitoring |
| Audit coverage for material actions | 100% | Audit sampling and control reports |
| Mean time to contain priority events | < 4 hours | Incident tracking |
| Interface adoption on published contracts | > 90% | Architecture compliance reviews |

### User Adoption Metrics

| Metric | Target | Timeline | Measurement Method |
|--------|--------|----------|-------------------|
| Weekly active pilot users | > 70% of trained pilot cohort | 3 months post-launch | Service analytics |
| Useful response rating | > 70% positive | Ongoing during pilot | In-product feedback and survey |
| Rework rate after supervisor review | At or below 18% baseline | 6 months post-launch | Supervisory sampling |

---

## Dependencies and Risks

### Dependencies

| Dependency | Description | Owner | Target Date | Status | Impact if Delayed |
|------------|-------------|-------|-------------|--------|-------------------|
| D-001 | Agreement on first-wave pilot workflows and prohibited-use list | Service Owner | 2026-04-15 | On Track | HIGH |
| D-002 | Access to identity, case, and knowledge interfaces | Product Manager | 2026-05-15 | On Track | HIGH |
| D-003 | Integrated assurance cadence and review participation | SIRO / Security Lead | 2026-04-30 | On Track | HIGH |
| D-004 | Pilot-force onboarding resources and training support | Force Operational Leads | 2026-06-01 | At Risk | MEDIUM |
| D-005 | Benefits-baseline measurement and reporting model | PMO / Finance | 2026-05-31 | On Track | MEDIUM |

### Risks

| Risk ID | Description | Probability | Impact | Mitigation Strategy | Owner |
|---------|-------------|-------------|--------|---------------------|-------|
| R-001 | Delivery pressure weakens assurance gates | MEDIUM | HIGH | Make assurance completion a release condition and escalate scope pressure early | SRO |
| R-002 | Users reject the service due to poor usability or trust | MEDIUM | HIGH | Pilot low-friction workflows first and measure quality and rework continuously | Service Owner |
| R-003 | Force-specific divergence undermines reuse | MEDIUM | MEDIUM | Use a mandatory national control pack with formal exceptions | Enterprise Architect |
| R-004 | Public trust declines after opaque or inaccurate use | LOW | HIGH | Limit early public-facing use and maintain transparency and complaints review | Service Owner |
| R-005 | Supplier governance gaps weaken confidence in value and control | MEDIUM | MEDIUM | Maintain supplier dependency inventory and exit planning | Commercial Lead |

**Risk Scoring**: Probability × Impact = Risk Level

- High Risk (Red): Requires executive escalation
- Medium Risk (Yellow): Active monitoring and mitigation
- Low Risk (Green): Accepted with monitoring

---

## Requirement Conflicts & Resolutions

> **Purpose**: Document conflicting requirements that arise from competing stakeholder drivers and
> show how conflicts were resolved.
>
> **Source**: Stakeholder conflicts were derived from [ARC-001-STKE-v1.0](/workspaces/arckit-test-project-v13-plymouth-research/my-project/projects/001-genai-for-uk-policing/ARC-001-STKE-v1.0).
>
> **Principle**: Trade-offs are explicit; conflicting demands are not hidden.

### Conflict C-001: Speed of rollout versus assurance depth

**Conflicting Requirements**:

- **Requirement A**: BR-001 and FR-001 require three live workflows by 2026-12-31.
- **Requirement B**: BR-004, FR-006, and NFR-C-001 require complete privacy, security, legal, and
  review controls before live use.

**Stakeholders Involved**:

- **SRO / Service Owner**: Want early visible progress and measurable delivery.
- **SIRO / Legal / Security Lead**: Want strong assurance before any live deployment.

**Nature of Conflict**:

- Three live workflows by year-end cannot be achieved safely if high-risk use cases are attempted
  too early.
- Assurance effort grows materially with workflow sensitivity.

**Trade-off Analysis**:

| Option | Pros | Cons | Impact |
|--------|------|------|--------|
| Prioritize speed across all workflow types | Faster visible delivery | High risk of governance failure | Sponsor satisfied, assurance stakeholders opposed |
| Prioritize assurance only | Stronger control posture | Benefits delayed, weak sponsor confidence | Assurance satisfied, sponsor frustrated |
| Phase by risk | Early low-risk wins plus assurance discipline | Higher-risk workflows delayed | Balanced outcome |

**Resolution Strategy**: PHASE

**Decision**: Start with bounded assistive workflows only; defer higher-risk public-facing or
evidentially sensitive expansion until controls mature.

**Rationale**: This preserves the 2026-12-31 milestone without forcing unacceptable risk into the
first live release.

**Decision Authority**: SRO accountable, with input from Enterprise Architect, SIRO, Security Lead,
and Service Owner under the stakeholder RACI.

**Impact on Requirements**:

- **Prioritized**: BR-001, FR-001, FR-002, FR-003, NFR-C-001
- **Constrained**: FR-006 applies from day one for sensitive workflows
- **Deferred**: High-risk public-facing use beyond bounded pilot scope

**Stakeholder Management**:

- **SRO (won timeline discipline)**: Receives milestone visibility through low-risk delivery.
- **Assurance stakeholders (won control depth for high-risk use)**: Retain veto over higher-risk
  expansion.

**Future Consideration**:

- Reassess expansion scope after at least three months of live pilot evidence and assurance review.

---

### Conflict C-002: Local force flexibility versus national standardization

**Conflicting Requirements**:

- **Requirement A**: FR-008 requires force-local configuration and onboarding flexibility.
- **Requirement B**: BR-005 and NFR-I-001 require national minimum controls and versioned shared
  interfaces.

**Stakeholders Involved**:

- **Force operational leads**: Want local fit and rollout control.
- **Home Office / oversight / Enterprise Architecture**: Want consistency, reuse, and inspectable
  governance.

**Nature of Conflict**:

- Unlimited local variation would break reuse and comparability.
- Rigid central standardization would suppress operational adoption.

**Trade-off Analysis**:

| Option | Pros | Cons | Impact |
|--------|------|------|--------|
| Full local customization | High local fit | No consistent national model | Forces satisfied, national stakeholders lose |
| Full central standardization | Strong reuse and comparability | Weak local adoption fit | National stakeholders satisfied, forces resist |
| Bounded configuration | Reuse with limited local choice | Some local needs deferred to exceptions | Balanced outcome |

**Resolution Strategy**: COMPROMISE

**Decision**: Adopt a national minimum control pack with bounded force-local configuration and a
formal exception process for material divergence.

**Rationale**: This provides a reusable architecture while allowing local rollout sequencing and
operational settings within guardrails.

**Decision Authority**: Service Owner accountable for onboarding decisions; Enterprise Architecture
Review Board decides material control deviations.

**Impact on Requirements**:

- **Modified**: FR-008 explicitly limits local configuration to approved fields.
- **Reinforced**: NFR-I-001 and DR-005 govern shared standards and exception traceability.
- **Rejected**: Direct local modification of protected national controls.

**Stakeholder Management**:

- **Force leads (partial loss)**: Can tailor rollout and local settings but cannot bypass core
  controls.
- **National stakeholders (partial loss)**: Accept limited local configuration to secure adoption.

**Future Consideration**:

- Review common exception themes quarterly and convert recurring approved exceptions into standard
  configurable features where appropriate.

---

### Conflict C-003: Frictionless user experience versus evidential and review controls

**Conflicting Requirements**:

- **Requirement A**: BR-002 and NFR-U-001 require low-friction usability and time savings.
- **Requirement B**: BR-003, FR-004, FR-006, and NFR-C-002 require provenance visibility, review
  routing, and strong auditability.

**Stakeholders Involved**:

- **Frontline users**: Want fast, simple task completion.
- **Investigations / Legal / CPS / SIRO**: Want stronger controls for sensitive outputs.

**Nature of Conflict**:

- Full review and provenance controls add time and interaction overhead.
- Removing those controls would undermine defensibility in high-sensitivity workflows.

**Trade-off Analysis**:

| Option | Pros | Cons | Impact |
|--------|------|------|--------|
| Minimize all workflow friction | Better short-term usability | Unacceptable evidential risk | Users win, governance loses |
| Apply strongest controls everywhere | Maximum defensibility | Productivity gains collapse | Governance wins, users lose |
| Risk-tiered controls | Balance usability with defensibility | More complex workflow design | Most balanced outcome |

**Resolution Strategy**: INNOVATE

**Decision**: Use risk-tiered workflow classes with lighter interaction for low-risk tasks and
mandatory provenance plus supervisory review for sensitive workflows.

**Rationale**: This satisfies the majority of productivity use cases while protecting high-risk
activity.

**Decision Authority**: Service Owner and Investigations Lead jointly recommend; SRO approves for
live scope based on assurance input.

**Impact on Requirements**:

- **Modified**: FR-004 and FR-006 apply by workflow class rather than uniformly.
- **Maintained**: NFR-U-001 continues to apply to low-risk workflows.
- **Deferred**: High-friction controls for low-risk workflows unless evidence justifies extension.

**Stakeholder Management**:

- **Frontline users (won in low-risk workflows)**: Keep lightweight assistive experiences for
  common tasks.
- **Investigations and legal stakeholders (won in sensitive workflows)**: Retain strong review and
  provenance controls where defensibility matters.

**Future Consideration**:

- Revisit the tiering model after pilot evidence on time savings, rework, and incident rates.

---

## Requirements Traceability Matrix

| Requirement ID | Type | Primary Goal / Outcome | Primary Beneficiary | Principle Alignment |
|----------------|------|------------------------|---------------------|--------------------|
| BR-001 | Business | G-1 / O-1 | SRO, Service Owner | Public value; Assurance by default |
| BR-002 | Business | G-2 / O-2 | Force leads, frontline users | Performance and usability |
| BR-003 | Business | G-3 / O-3 | Investigations, legal | Provenance and accountability |
| BR-004 | Business | G-4 / O-4 | SIRO, Security Lead | Security by design |
| BR-005 | Business | G-5 / O-5 | Force leads, Enterprise Architect | Interoperability and federation |
| BR-006 | Business | G-6 / O-6 | SRO, Finance | Lifecycle governance |
| FR-001 | Functional | G-1 / O-1 | Service Owner | Policy guardrails |
| FR-002 | Functional | G-2, G-3 / O-2, O-3 | Users, investigations | Minimized data use; provenance |
| FR-003 | Functional | G-1, G-3 / O-1, O-3 | Users, supervisors | Human accountability |
| FR-004 | Functional | G-3 / O-3 | Investigations, legal | Transparency and auditability |
| FR-005 | Functional | G-2, G-4 / O-2, O-4 | Users, public-interest stakeholders | Provenance and quality |
| FR-006 | Functional | G-3, G-4 / O-3, O-4 | Supervisors, SIRO | Policy guardrails |
| FR-007 | Functional | G-2, G-6 / O-2, O-6 | Service Owner, Finance | Continuous monitoring |
| FR-008 | Functional | G-5 / O-5 | Force leads | Federation |
| FR-009 | Functional | G-1, G-4, G-6 / O-1, O-4, O-6 | Reviewers | Transparency and auditability |
| FR-010 | Functional | G-2, G-3 / O-2, O-3 | Users, learning leads | Usability |
| NFR-P-001 | NFR Performance | G-2 / O-2 | Frontline users | Performance and usability |
| NFR-P-002 | NFR Performance | G-2, G-5 / O-2, O-5 | Service Owner | Resilience and change readiness |
| NFR-A-001 | NFR Availability | G-1, G-2 / O-1, O-2 | Users, Service Owner | Resilience |
| NFR-A-002 | NFR Availability | G-1, G-4 / O-1, O-4 | Service operations | Resilience |
| NFR-A-003 | NFR Availability | G-1, G-3 / O-1, O-3 | Users, supervisors | Safe degradation |
| NFR-S-001 | NFR Scalability | G-5 / O-5 | Enterprise Architect | Change readiness |
| NFR-S-002 | NFR Scalability | G-5 / O-5 | Service Owner | Data sovereignty |
| NFR-SEC-001 | NFR Security | G-4 / O-4 | Security Lead | Security by design |
| NFR-SEC-002 | NFR Security | G-1, G-4, G-5 / O-1, O-4, O-5 | SIRO, Security Lead | Least privilege |
| NFR-SEC-003 | NFR Security | G-4 / O-4 | SIRO, Security Lead | Privacy and sovereignty |
| NFR-SEC-004 | NFR Security | G-4 / O-4 | Security Lead | Security by design |
| NFR-SEC-005 | NFR Security | G-4, G-6 / O-4, O-6 | Security Lead, SRO | Assurance by default |
| NFR-C-001 | NFR Compliance | G-1, G-3, G-4 / O-1, O-3, O-4 | SIRO, Legal | Lawfulness and proportionality |
| NFR-C-002 | NFR Compliance | G-1, G-4, G-6 / O-1, O-4, O-6 | Legal, reviewers | Auditability |
| NFR-C-003 | NFR Compliance | G-1, G-6 / O-1, O-6 | Public, oversight bodies | Transparency |
| NFR-C-004 | NFR Compliance | G-3, G-4 / O-3, O-4 | SIRO, DPO | Data sovereignty |
| NFR-U-001 | NFR Usability | G-2 / O-2 | Frontline users | Usability |
| NFR-U-002 | NFR Usability | G-2, G-6 / O-2, O-6 | Users, public bodies | Accessibility |
| NFR-M-001 | NFR Maintainability | G-4, G-6 / O-4, O-6 | Service ops, assurance teams | Monitoring |
| NFR-M-002 | NFR Maintainability | G-1, G-5 / O-1, O-5 | Service ops, onboarding teams | Change readiness |
| NFR-I-001 | NFR Interoperability | G-5 / O-5 | Enterprise Architect | Interfaces and loose coupling |
| NFR-I-002 | NFR Interoperability | G-5, G-6 / O-5, O-6 | Reviewers, admins | Portability |
| INT-001 | Integration | G-1, G-4, G-5 / O-1, O-4, O-5 | IAM and security stakeholders | Security by design |
| INT-002 | Integration | G-2, G-3 / O-2, O-3 | Case system owners, investigators | Provenance |
| INT-003 | Integration | G-2, G-4 / O-2, O-4 | Knowledge owners, users | Minimized data use |
| INT-004 | Integration | G-4 / O-4 | Security ops | Monitoring and response |
| INT-005 | Integration | G-1, G-6 / O-1, O-6 | PMO, oversight | Transparency |
| INT-006 | Integration | G-3, G-6 / O-3, O-6 | Justice partners | Auditability |
| DR-001 | Data | G-3 / O-3 | Investigations, legal | Provenance |
| DR-002 | Data | G-2, G-3 / O-2, O-3 | Users, supervisors | Accountability |
| DR-003 | Data | G-1, G-4 / O-1, O-4 | Reviewers, security teams | Auditability |
| DR-004 | Data | G-3, G-4 / O-3, O-4 | SIRO, DPO | Minimized data use |
| DR-005 | Data | G-5 / O-5 | Force leads, architecture | Federation |
| DR-006 | Data | G-5 / O-5 | Onboarding teams | Change readiness |

---

## Timeline and Milestones

### High-Level Milestones

| Milestone | Description | Target Date | Dependencies |
|-----------|-------------|-------------|--------------|
| Requirements Approval | Stakeholder sign-off on requirements | 2026-04-06 | This document, stakeholder review |
| Discovery and HLD Complete | High-level design and assurance approach approved | 2026-06-30 | Requirements, pilot workflow selection |
| Build and Integration Complete | Core workflows, integrations, and controls implemented | 2026-09-30 | Design, interface access, delivery team |
| UAT and Assurance Complete | UAT, security, privacy, and operational readiness completed | 2026-11-30 | Build, pilot-force readiness |
| Production Launch | First live workflows approved and launched | 2026-12-31 | UAT, assurance, go-live approval |

---

## Budget

### Cost Estimate

| Category | Estimated Cost | Notes |
|----------|----------------|-------|
| Development | £1,800,000 | Product, engineering, QA, architecture for initial phase |
| Infrastructure and platform operations | £550,000 | Hosting, search, storage, observability, networking |
| Third-party services and supplier support | £650,000 | External service consumption and supplier onboarding support |
| Security, privacy, and assurance testing | £450,000 | Security testing, legal review support, audit preparation |
| Training and change | £250,000 | Pilot training, guidance, adoption support |
| **Total** | **£3,700,000** | Indicative initial-phase estimate through first live operation |

### Ongoing Operational Costs

| Category | Annual Cost | Notes |
|----------|-------------|-------|
| Infrastructure and platform operations | £500,000 | Live hosting, monitoring, resilience |
| Third-party and support contracts | £550,000 | Supplier support and service consumption |
| Support and incident response | £250,000 | Service operations, on-call, runbook maintenance |
| Assurance and compliance refresh | £150,000 | Recurring review, testing, and reporting |
| **Total** | **£1,450,000** | Indicative annual run cost at early scale |

---

## Approval

### Requirements Review

| Reviewer | Role | Status | Date | Comments |
|----------|------|--------|------|----------|
| SRO, GenAI for UK Policing | Business Sponsor | Pending | 2026-03-14 planned | Confirm strategic outcomes and scale criteria |
| Service Owner, GenAI for UK Policing | Product Owner | Pending | 2026-03-14 planned | Confirm workflow scope and adoption assumptions |
| Enterprise Architecture Lead | Enterprise Architect | Pending | 2026-03-18 planned | Confirm standards, interoperability, and control pack assumptions |
| Security Lead | Security | Pending | 2026-03-18 planned | Confirm security testing and access-control requirements |
| SIRO / DPO / Legal Lead | Compliance | Pending | 2026-03-18 planned | Confirm lawfulness, privacy, retention, and transparency requirements |

### Sign-Off

By signing below, stakeholders confirm that requirements are complete enough to proceed to design
phase subject to future controlled change.

| Stakeholder | Signature | Date |
|-------------|-----------|------|
| Senior Responsible Owner | PENDING | PENDING |
| Service Owner | PENDING | PENDING |
| Enterprise Architecture Lead | PENDING | PENDING |

---

## Appendices

### Appendix A: Glossary

- **Assistive GenAI**: Generative AI used to support human work rather than replace human
  decision-making authority
- **Control pack**: Standard set of controls, obligations, and evidence required for onboarding and
  live use
- **DPIA**: Data Protection Impact Assessment
- **Provenance**: Traceable record of what source information informed a generated output
- **SIRO**: Senior Information Risk Owner
- **SRO**: Senior Responsible Owner

### Appendix B: Reference Documents

- [Global architecture principles](/workspaces/arckit-test-project-v13-plymouth-research/my-project/projects/000-global/ARC-000-PRIN-v1.0.md)
- [Stakeholder drivers analysis](/workspaces/arckit-test-project-v13-plymouth-research/my-project/projects/001-genai-for-uk-policing/ARC-001-STKE-v1.0.md)
- GovS 005 Digital
- GovS 007 Security

### Appendix C: Wireframes and Mockups

Wireframes and mockups are not yet available. They should be produced during design and linked into
the next document revision once reviewed by frontline and governance stakeholders.

### Appendix D: Data Models

A detailed project data model should be created in a follow-on `DATA` artifact based on the `DR`
requirements and data entities defined in this document.

---

**Document History**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-03-07 | ArcKit AI | Initial draft |
| 1.0 | 2026-03-07 | ArcKit AI | Completed first requirements baseline aligned to stakeholder analysis and global principles |

## External References

| Document | Type | Source | Key Extractions | Path |
|----------|------|--------|-----------------|------|
| ARC-001-STKE-v1.0 | Stakeholder analysis | Local project artifact | Goals, outcomes, conflicts, RACI, stakeholder priorities | projects/001-genai-for-uk-policing/ARC-001-STKE-v1.0.md |
| ARC-000-PRIN-v1.0 | Architecture principles | Local project artifact | Lawfulness, accountability, privacy, security, interoperability, auditability | projects/000-global/ARC-000-PRIN-v1.0.md |
| No project-specific external specifications provided at generation time | N/A | Local project context | No legacy system specifications, user research reports, or procurement packs were available for extraction in this version | projects/001-genai-for-uk-policing/external/ |

---

**Generated by**: ArcKit `$arckit-requirements` command
**Generated on**: 2026-03-07 13:15 GMT
**ArcKit Version**: 4.0.0
**Project**: GenAI for UK Policing (Project 001)
**AI Model**: GPT-5 Codex
**Generation Context**: Used ARC-001-STKE-v1.0 and ARC-000-PRIN-v1.0; no project-specific
external specifications, RISK artifact, or SOBC artifact were available
