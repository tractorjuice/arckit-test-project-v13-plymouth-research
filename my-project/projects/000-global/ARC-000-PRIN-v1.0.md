# GenAI for UK Policing Enterprise Architecture Principles

> **Template Origin**: Official | **ArcKit Version**: 4.0.0 | **Command**: `$arckit-principles`

## Document Control

| Field | Value |
|-------|-------|
| **Document ID** | ARC-000-PRIN-v1.0 |
| **Document Type** | Enterprise Architecture Principles |
| **Project** | GenAI for UK Policing (Project 000) |
| **Classification** | OFFICIAL |
| **Status** | DRAFT |
| **Version** | 1.0 |
| **Created Date** | 2026-03-07 |
| **Last Modified** | 2026-03-07 |
| **Review Cycle** | Quarterly |
| **Next Review Date** | 2026-06-07 |
| **Owner** | Enterprise Architecture Lead, GenAI for UK Policing |
| **Reviewed By** | PENDING |
| **Approved By** | PENDING |
| **Distribution** | Enterprise Architecture Review Board; Responsible AI Review Panel; Information Security; Data Protection; Legal; Product and Delivery Leads |

## Revision History

| Version | Date | Author | Changes | Approved By | Approval Date |
|---------|------|--------|---------|-------------|---------------|
| 1.0 | 2026-03-07 | ArcKit AI | Initial creation from `$arckit-principles` command for generative AI in UK policing | PENDING | PENDING |

---

## Executive Summary

This document establishes the architecture principles governing all generative AI capabilities
used in UK policing contexts, including operational support, investigations, intelligence
analysis, public contact, knowledge retrieval, workforce productivity, and corporate services.
These principles are intended to protect public trust, preserve legality and evidential
integrity, and ensure that AI-enabled services remain secure, accountable, interoperable, and
fit for policing use.

**Scope**: All technology projects, products, platforms, data flows, and suppliers delivering or
supporting generative AI capability for UK policing
**Authority**: Enterprise Architecture Review Board with Responsible AI Review Panel oversight
**Compliance**: Mandatory unless an exception is approved through the formal process in this
document

**Philosophy**: These principles are technology-agnostic. They define the required qualities,
constraints, and decision criteria for architecture. They do not prescribe a specific vendor,
model, hosting approach, framework, or tool.

---

## I. Strategic Principles

### 1. Public value, lawfulness, and proportionality

**Principle Statement**:
All generative AI capabilities MUST deliver a clear policing or public-service outcome and MUST
be lawful, necessary, and proportionate to the intended use.

**Rationale**:
UK policing operates under heightened public scrutiny and legal constraint. AI use that lacks a
clear public-interest case, legal basis, or proportionality test creates avoidable operational,
ethical, and reputational risk.

**Implications**:

- Define the policing outcome, legal basis, and decision boundary before solution design
- Use the least intrusive architecture that can achieve the required operational objective
- Distinguish clearly between assistive use, advisory use, and decision-support use
- Prohibit deployment where the benefit case is weak or the rights impact is excessive

**Validation Gates**:

- [ ] Documented use case, intended benefit, and affected user groups
- [ ] Legal basis and proportionality assessment completed
- [ ] Human rights, equality, and privacy impacts identified
- [ ] Clear statement of what the AI capability will not be used for

**Example Scenarios**:

- Good: A generative AI tool drafts internal summaries for investigators, with human review
  before any action is taken.
- Bad: A generative AI tool is introduced for frontline triage without a defined legal basis,
  rights assessment, or operational safeguards.

**Common Violations to Avoid**:

- Adopting AI because it is novel rather than because it solves a defined policing problem
- Expanding a low-risk assistant into a higher-risk operational use without reassessment
- Using sensitive data beyond the stated purpose of collection

---

### 2. Human accountability and contestability

**Principle Statement**:
All material decisions informed by generative AI MUST remain under accountable human authority,
and affected users MUST be able to challenge, review, and correct outputs where appropriate.

**Rationale**:
Policing powers and outcomes require accountable decision-making. Human oversight is essential to
prevent automation bias, inappropriate reliance, and unreviewable operational harm.

**Implications**:

- Define named accountable roles for business ownership, operational approval, and technical risk
- Ensure operators can inspect, reject, amend, or override AI outputs
- Prevent architectures that obscure who made the final operational decision
- Design review paths for contested outputs, inaccurate content, or harmful recommendations

**Validation Gates**:

- [ ] Human decision points documented for each workflow
- [ ] Named accountable owner assigned for each production use case
- [ ] User interfaces support rejection, correction, and escalation
- [ ] Audit trail records whether output was accepted, edited, or discarded

**Example Scenarios**:

- Good: An officer receives a draft generated response, edits it, and the final response is
  attributed to the officer.
- Bad: A generated recommendation is passed automatically into a case workflow with no human
  review or route for challenge.

**Common Violations to Avoid**:

- Treating generated outputs as authoritative facts
- Removing human sign-off from material operational workflows
- Failing to record who accepted or overrode an AI-assisted outcome

---

### 3. Security by design and least privilege

**Principle Statement**:
All generative AI architectures MUST apply defense-in-depth security, least privilege, separation
of duties, and continuous verification from the outset.

**Rationale**:
Policing data, operational workflows, and investigative context are high-value targets. GenAI
introduces additional attack surfaces through prompts, retrieval layers, agents, connectors, and
third-party supply chains.

**Implications**:

- Authenticate and authorize all human, service, and automated interactions
- Minimize access to policing data, prompts, logs, and model-management functions
- Isolate environments and data domains according to sensitivity and operational need
- Protect prompts, outputs, model settings, and orchestration rules as governed assets

**Validation Gates**:

- [ ] Threat model completed for model, data, integration, and user interaction paths
- [ ] Least-privilege access model defined and enforced
- [ ] Secrets, credentials, and privileged actions managed through controlled mechanisms
- [ ] Logging covers access, prompt handling, configuration change, and administrative actions
- [ ] Security testing includes misuse, prompt manipulation, and unauthorized data exposure

**Example Scenarios**:

- Good: Access to operational datasets, configuration settings, and release controls is separated
  by role and fully logged.
- Bad: A broad service identity can read all prompts, retrieve all case data, and change runtime
  behavior without independent approval.

**Common Violations to Avoid**:

- Granting model operators unrestricted access to all connected policing data
- Reusing privileged credentials across environments or teams
- Storing sensitive prompts, secrets, or outputs in uncontrolled locations

---

### 4. Resilience, continuity, and safe degradation

**Principle Statement**:
All generative AI services MUST fail safely, degrade gracefully, and preserve continuity of
policing operations when dependencies are unavailable or outputs are unreliable.

**Rationale**:
Generative AI services depend on multiple components that can fail independently. Policing
operations must continue without unsafe behavior, silent corruption, or uncontrolled fallback.

**Implications**:

- Design manual or non-AI fallback paths for critical workflows
- Bound the effect of upstream failure, latency, or degraded output quality
- Prevent cascading failures across operational systems and shared services
- Define recovery objectives for service restoration and for correction of generated artifacts

**Validation Gates**:

- [ ] Failure modes documented for model, retrieval, data, and integration dependencies
- [ ] Safe fallback behavior defined for critical workflows
- [ ] Recovery time and recovery point objectives documented where applicable
- [ ] Service degradation alerts and operator runbooks in place

**Example Scenarios**:

- Good: If retrieval or generation fails, the user is routed to a manual knowledge source and the
  failure is visible to operations.
- Bad: When the service times out, the application returns partial content as if it were complete
  and accurate.

**Common Violations to Avoid**:

- Designing a workflow with no manual fallback for operationally material actions
- Treating silent failure as acceptable because the interface still returns text
- Relying on a single untested dependency path for essential service delivery

---

### 5. Interoperability and federation

**Principle Statement**:
All generative AI capabilities MUST interoperate through well-defined interfaces, shared
information standards, and federated governance rather than through opaque point-to-point
coupling.

**Rationale**:
UK policing operates across multiple forces, partners, and systems. Interoperability reduces
duplication, supports force-level autonomy, and enables cross-force reuse without imposing a
single monolith.

**Implications**:

- Use published contracts for data exchange, prompt context assembly, and service integration
- Separate local implementation choices from common interface and policy obligations
- Prevent direct cross-system database dependence across organisational boundaries
- Design for reuse across forces where legal and operational constraints permit

**Validation Gates**:

- [ ] Interface contracts published and versioned
- [ ] Data ownership and stewardship defined for each integrated data domain
- [ ] Cross-force and partner integration dependencies documented
- [ ] Backward compatibility or migration strategy defined for interface changes

**Example Scenarios**:

- Good: A force-specific workflow consumes a shared case-summary service through a versioned
  contract and force-local policy layer.
- Bad: One system reads another system's internal storage directly because it is faster to build.

**Common Violations to Avoid**:

- Tight coupling through shared databases or unmanaged file exchange
- Embedding local business rules inside interfaces meant for national reuse
- Changing schemas or response formats without version control

---

## II. Data Principles

### 6. Lawful, purpose-bound, and minimized data use

**Principle Statement**:
All data used by generative AI MUST be collected, accessed, retained, and processed only for a
defined lawful purpose, with minimization applied at every stage of the architecture.

**Rationale**:
Generative AI can amplify the effect of over-collection and inappropriate reuse. Purpose
limitation and minimization are essential to preserve privacy, maintain legality, and reduce the
blast radius of error or misuse.

**Implications**:

- Use only the minimum data required for the specific outcome being delivered
- Restrict prompt context, retrieval scope, and retained outputs by role and purpose
- Differentiate between operational, investigative, intelligence, and corporate use cases
- Prevent uncontrolled reuse of prompts, outputs, or fine-tuning data across unrelated purposes

**Validation Gates**:

- [ ] Data inventory maps each dataset to a specific lawful purpose
- [ ] Minimization rules defined for retrieval, prompting, storage, and logging
- [ ] Special category and sensitive policing data handling rules documented
- [ ] Data reuse controls defined for testing, training, and analytics

**Example Scenarios**:

- Good: A summarization workflow retrieves only case fields needed for the task and discards
  transient working context after processing.
- Bad: Entire case files are routinely exposed to the model when only a small subset is needed.

**Common Violations to Avoid**:

- Using broad data access "just in case" it improves output quality
- Reusing production prompts and outputs in development without controls
- Logging sensitive personal data by default

---

### 7. Data quality, provenance, and evidential integrity

**Principle Statement**:
All data and generated outputs used in policing contexts MUST preserve provenance, quality
indicators, and evidential integrity appropriate to the use case.

**Rationale**:
Generative AI can disguise weak source quality behind fluent language. Policing requires the
ability to trace what source information informed an output and to distinguish fact, inference,
and generated text.

**Implications**:

- Record source systems, retrieval context, timestamps, and transformation steps
- Expose confidence, uncertainty, or evidence availability where this affects use
- Preserve original records separately from generated interpretations or summaries
- Prevent generated content from overwriting source material or evidential records

**Validation Gates**:

- [ ] Source provenance captured for generated outputs where operationally relevant
- [ ] Data quality checks defined for critical input datasets
- [ ] Generated artifacts clearly labeled as generated, derived, or source-backed
- [ ] Evidential record retention and chain-of-custody requirements considered

**Example Scenarios**:

- Good: A generated briefing links back to the underlying records and identifies where the source
  evidence is incomplete.
- Bad: A generated narrative is saved as if it were the original witness or case record.

**Common Violations to Avoid**:

- Blending generated content and source evidence without labeling
- Losing provenance when data moves between pipelines or environments
- Treating inferred text as if it were verified fact

---

### 8. Privacy, confidentiality, and data sovereignty

**Principle Statement**:
All generative AI architectures MUST protect privacy, confidentiality, and jurisdictional control
of policing data throughout storage, processing, transfer, and disposal.

**Rationale**:
Policing data may involve victims, witnesses, suspects, vulnerable persons, covert operations, or
legally restricted information. Mishandling creates acute operational and societal harm.

**Implications**:

- Classify data and apply controls that match its sensitivity and legal handling requirements
- Restrict cross-border transfer and onward sharing unless explicitly lawful and approved
- Ensure retention, deletion, and legal-hold arrangements are defined and executable
- Separate environments and controls for test, training, evaluation, and live operation

**Validation Gates**:

- [ ] Data classification completed for connected and generated datasets
- [ ] Residency and transfer constraints documented and enforced
- [ ] Retention and deletion rules implemented for prompts, outputs, logs, and caches
- [ ] Privacy impact assessment completed where required

**Example Scenarios**:

- Good: Sensitive operational data remains within approved jurisdictions and deletion controls
  apply to derived outputs and logs.
- Bad: Prompt and output logs containing sensitive policing content are retained indefinitely with
  no policy basis.

**Common Violations to Avoid**:

- Treating transient AI artifacts as exempt from data protection controls
- Ignoring location and onward-transfer implications for service components
- Retaining outputs longer than the underlying lawful purpose requires

---

## III. Integration Principles

### 9. Standard interfaces and loose coupling

**Principle Statement**:
Generative AI components MUST integrate through versioned interfaces and independent service
boundaries, avoiding hidden dependencies and shared mutable state.

**Rationale**:
Loose coupling reduces fragility, enables safer change, and allows forces and delivery teams to
evolve components independently while maintaining governance control.

**Implications**:

- Expose integration through controlled contracts rather than direct internal access
- Isolate prompt orchestration, retrieval, policy enforcement, and business workflows
- Avoid hidden dependencies on internal schemas, file layouts, or runtime state
- Design components to be replaceable without restructuring the entire estate

**Validation Gates**:

- [ ] Each integration point has a published contract and owner
- [ ] Shared mutable state is minimized and justified where unavoidable
- [ ] Interface versioning and deprecation rules defined
- [ ] Component replacement impact can be assessed without reverse engineering

**Example Scenarios**:

- Good: The application calls a governed generation service through a published contract and can
  substitute the implementation without breaking users.
- Bad: Business logic depends on undocumented prompt formats and internal storage structure.

**Common Violations to Avoid**:

- Direct dependency on another system's internal schema
- Embedding policy checks in multiple components inconsistently
- Allowing runtime behavior to depend on undocumented side effects

---

### 10. Controlled autonomy and policy guardrails

**Principle Statement**:
Any autonomous or semi-autonomous generative AI behavior MUST operate within explicit policy
guardrails, bounded permissions, and reversible actions.

**Rationale**:
Agentic patterns can increase capability but also magnify risk. In policing, actions taken on the
basis of generated reasoning must be constrained, reviewable, and safe to stop.

**Implications**:

- Define what the system may observe, propose, trigger, or modify
- Separate recommendation, execution, and approval stages for higher-risk actions
- Require stronger controls as autonomy, privilege, or potential harm increases
- Make policy enforcement externalized, testable, and consistently applied

**Validation Gates**:

- [ ] Autonomy level explicitly defined for each use case
- [ ] Guardrails documented for data access, tool use, and action execution
- [ ] High-impact actions require human approval before execution
- [ ] Kill switch, suspension, or rollback mechanisms exist for unsafe behavior

**Example Scenarios**:

- Good: The system drafts a task list and proposes next actions, but a supervisor approves any
  operational action before execution.
- Bad: The system can update case records, contact external parties, or trigger enforcement steps
  without bounded permissions or approval.

**Common Violations to Avoid**:

- Conflating advisory output with authority to act
- Expanding tool permissions faster than governance and testing mature
- Making autonomy irreversible or difficult to disable under pressure

---

### 11. Traceability, transparency, and auditability

**Principle Statement**:
All material generative AI interactions MUST be traceable, explainable to the degree required by
the use case, and auditable for review, learning, and challenge.

**Rationale**:
Public bodies must account for how decisions are influenced and how systems are governed.
Traceability underpins assurance, incident response, subject access handling, and public trust.

**Implications**:

- Record relevant prompts, context sources, policy decisions, user actions, and outputs
- Distinguish between source evidence, retrieved context, generated text, and final human outcome
- Produce transparency records suitable for internal review and, where required, public reporting
- Keep logs structured, queryable, and protected against tampering

**Validation Gates**:

- [ ] Audit events defined for generation, retrieval, override, approval, and configuration change
- [ ] Records support reconstruction of material workflow outcomes
- [ ] Transparency obligations assessed for each production use case
- [ ] Audit records are protected, retained, and reviewable by authorized teams

**Example Scenarios**:

- Good: An assurance reviewer can reconstruct which sources informed an output, which guardrails
  were applied, and who accepted the final result.
- Bad: Only the final generated text is stored, with no record of source context or human review.

**Common Violations to Avoid**:

- Keeping logs that are too sparse to support challenge or investigation
- Capturing rich audit detail without access control or retention policy
- Treating transparency as optional because the service is internal

---

## IV. Quality Attributes

### 12. Performance, accessibility, and usability

**Principle Statement**:
All generative AI services MUST meet defined performance targets and MUST be accessible, usable,
and inclusive for the full range of intended users.

**Rationale**:
Slow, inaccessible, or confusing systems drive unsafe workarounds and reduce adoption. In public
service settings, accessibility and usability are core quality requirements, not optional polish.

**Implications**:

- Define measurable targets for latency, throughput, availability, and user effort
- Design interfaces that make confidence, uncertainty, and next actions clear
- Meet accessibility obligations for digital public services and workforce tools
- Support varied operational contexts, including mobile, control room, and low-bandwidth use

**Validation Gates**:

- [ ] Performance targets documented and tested under realistic load
- [ ] Accessibility assessed against applicable public-sector expectations
- [ ] Critical user journeys tested with representative operational users
- [ ] Unsafe workarounds and usability failure modes identified and mitigated

**Example Scenarios**:

- Good: A call-handling assistant returns draft content within agreed limits and can be operated
  effectively with keyboard navigation and assistive technology.
- Bad: The service is only usable in ideal desktop conditions and hides uncertainty behind fluent
  prose.

**Common Violations to Avoid**:

- Optimizing for benchmark speed while ignoring operational usability
- Releasing inaccessible interfaces into frontline or public-facing contexts
- Treating uncertain output as complete because it is well phrased

---

### 13. Maintainability, portability, and change readiness

**Principle Statement**:
All generative AI architectures MUST be modular, documented, and portable enough to support safe
change, controlled replacement, and long-term maintainability.

**Rationale**:
The market, risk posture, and regulatory expectations for generative AI are changing quickly.
Architectures that lock the organisation into a single implementation path will accumulate risk and
cost.

**Implications**:

- Separate business rules, prompt assets, policy controls, and integration logic
- Maintain architecture records for significant design and assurance decisions
- Design for substitution of components with bounded change impact
- Document assumptions, limits, and operational dependencies alongside the implementation

**Validation Gates**:

- [ ] Architecture documentation and decision records are current
- [ ] Component boundaries and responsibilities are explicit
- [ ] Replacement or rollback strategy exists for critical components
- [ ] Operational assumptions and limits are documented for support teams

**Example Scenarios**:

- Good: Prompt assets, policies, retrieval rules, and business workflows can change independently
  under version control.
- Bad: Key behavior lives in undocumented manual settings known only to a small number of people.

**Common Violations to Avoid**:

- Hard-coding policies or prompts in places that are hard to review
- Allowing undocumented tribal knowledge to control production behavior
- Binding business processes to a single implementation with no exit path

---

## V. Development Practices

### 14. Assurance by default

**Principle Statement**:
All generative AI delivery MUST embed assurance activities by default, including security, privacy,
fairness, safety, legal, and operational review appropriate to the risk of the use case.

**Rationale**:
Assurance added late is expensive, partial, and easy to bypass. In policing, assurance must shape
architecture from the start, especially where rights, vulnerability, or operational outcomes are
affected.

**Implications**:

- Scale assurance depth according to impact, sensitivity, and autonomy
- Define acceptance criteria for factuality, harmful content, bias, and misuse resistance
- Use pre-production review gates before live deployment or scope expansion
- Retest when data, policy, workflow, or operating context changes materially

**Validation Gates**:

- [ ] Assurance plan documented and approved for the use case
- [ ] Test cases cover safety, misuse, fairness, and operational failure modes
- [ ] Material residual risks documented and owned
- [ ] Scope changes trigger reassessment before release

**Example Scenarios**:

- Good: The team defines assurance evidence for each release and blocks go-live until minimum
  controls are met.
- Bad: The service is piloted live first, with assurance deferred until after incidents occur.

**Common Violations to Avoid**:

- Treating a prototype as exempt once real users and real data are involved
- Limiting testing to generic functional checks
- Expanding use to higher-risk contexts without renewed assurance

---

### 15. Automation, testing, and controlled release

**Principle Statement**:
All generative AI solutions MUST use automated build, test, deployment, and rollback controls, with
release decisions gated by evidence rather than optimism.

**Rationale**:
Manual release processes create drift, weak auditability, and inconsistent assurance. Automated
controls improve repeatability and reduce the likelihood of unreviewed change reaching production.

**Implications**:

- Version all code, prompt assets, policies, datasets, and configuration changes
- Automate testing for functional, security, performance, and behavioral regression concerns
- Use staged rollout, rollback, and release approval controls proportionate to risk
- Prevent direct production changes outside governed pathways

**Validation Gates**:

- [ ] Delivery pipeline exists for code and non-code runtime assets
- [ ] Regression tests cover critical workflows and known failure patterns
- [ ] Release approvals and rollback procedures documented and tested
- [ ] Production changes are traceable to reviewed artifacts

**Example Scenarios**:

- Good: A policy change is versioned, tested, approved, and released through the same governed
  path as application code.
- Bad: Prompt and policy changes are made manually in production because they are "not really
  code."

**Common Violations to Avoid**:

- Treating prompts, retrieval rules, or safety settings as informal content rather than governed
  assets
- Deploying behavior changes without regression evidence
- Relying on manual rollback with no tested procedure

---

### 16. Supplier, model, and lifecycle governance

**Principle Statement**:
All external suppliers, internally built components, and model lifecycle activities MUST be
governed through explicit accountability, exit planning, and ongoing performance oversight.

**Rationale**:
Generative AI services often rely on layered suppliers, data processors, and model providers.
Without lifecycle governance, the organisation cannot manage lock-in, cost, performance decline,
or unacceptable changes in risk.

**Implications**:

- Define ownership for supplier risk, service changes, and operating model decisions
- Assess dependencies on third-party training, hosting, support, and sub-processing arrangements
- Maintain exit and substitution plans for critical externally supplied capabilities
- Monitor quality, cost, safety, and compliance over time rather than only at procurement

**Validation Gates**:

- [ ] Supplier and dependency inventory maintained for the service
- [ ] Commercial, legal, security, and assurance obligations documented
- [ ] Exit or substitution strategy exists for critical dependencies
- [ ] Ongoing service review covers performance, incidents, and material supplier change

**Example Scenarios**:

- Good: The service has a documented dependency map, clear contractual obligations, and a
  replacement plan for critical external components.
- Bad: A critical capability depends on a supplier with no defined exit path, no performance
  review, and unclear data handling responsibilities.

**Common Violations to Avoid**:

- Treating supplier onboarding as the end of governance
- Failing to monitor changes in supplier risk or service terms
- Building around an external dependency with no credible replacement path

---

### 17. Continuous monitoring, drift response, and improvement

**Principle Statement**:
All live generative AI services MUST be continuously monitored for quality, safety, security,
drift, misuse, and changing operational effectiveness, with defined triggers for intervention.

**Rationale**:
Generative AI behavior can shift over time due to data change, workflow change, user behavior, or
supplier change. Continuous monitoring is required to keep the service within acceptable bounds.

**Implications**:

- Track service health, output quality, error patterns, and user override behavior
- Define thresholds for retraining, reconfiguration, rollback, or suspension
- Review incidents, complaints, and contested outcomes as architecture feedback
- Use monitoring to drive iterative improvement, not just incident reporting

**Validation Gates**:

- [ ] Operational metrics, quality metrics, and safety indicators are defined
- [ ] Drift or degradation thresholds trigger investigation and action
- [ ] Incident response includes AI-specific containment and review steps
- [ ] Feedback from users, assurance teams, and operations is captured and acted on

**Example Scenarios**:

- Good: Rising override rates and repeated factual errors trigger controlled rollback and root
  cause analysis.
- Bad: Quality drifts for months because only uptime is monitored.

**Common Violations to Avoid**:

- Monitoring availability while ignoring output quality and harm indicators
- Leaving drift detection to ad hoc user complaint
- Treating live assurance issues as product backlog items with no operational urgency

---

## VI. Exception Process

### Requesting Architecture Exceptions

Principles are mandatory unless a documented exception is approved by the Enterprise Architecture
Review Board and, where relevant, the Responsible AI Review Panel.

**Valid Exception Reasons**:

- Legal, operational, or legacy constraints that temporarily prevent compliance
- Time-bound pilot conditions with enhanced safeguards
- Transitional architecture during migration or supplier exit
- National security or covert-operational handling constraints with compensating controls

**Exception Request Requirements**:

- [ ] Clear business and operational rationale for the exception
- [ ] Impacted principles and duration of non-compliance identified
- [ ] Compensating controls, residual risks, and monitoring arrangements documented
- [ ] Expiry date and remediation plan defined
- [ ] Named accountable owner accepts the residual risk

**Approval Process**:

1. Submit the exception request to the Enterprise Architecture function.
2. Review security, data protection, legal, and responsible AI impacts.
3. Obtain approval from the Enterprise Architecture Review Board.
4. Obtain senior approval for exceptions affecting critical principles or high-risk use cases.
5. Record the decision, expiry date, and remediation actions in project governance artifacts.
6. Re-review all active exceptions at least quarterly.

---

## VII. Governance and Compliance

### Architecture Review Gates

All projects must pass architecture reviews at key milestones:

**Discovery / Alpha**:

- [ ] Use case, public value, and legal basis are defined
- [ ] Initial risk, privacy, equality, and human oversight considerations captured
- [ ] Principles understood and obvious violations identified early

**Design / Beta**:

- [ ] Detailed architecture demonstrates compliance with each applicable principle
- [ ] Assurance plan, test strategy, and operational support model are documented
- [ ] Data governance, security controls, and transparency obligations are defined
- [ ] Exceptions are requested formally where needed

**Pre-Production**:

- [ ] Implementation matches the approved design and operating model
- [ ] Validation gates for all applicable principles are evidenced
- [ ] Rollback, incident response, and support arrangements are proven
- [ ] Responsible owners confirm readiness for live operation

**Live Operation**:

- [ ] Monitoring, drift management, and review cadence are in place
- [ ] Incidents, complaints, and assurance findings are fed back into design governance
- [ ] Material scope or context changes trigger reassessment before expansion

### Enforcement

- Architecture review is mandatory for all generative AI initiatives in scope.
- Material principle violations must be remediated or approved as time-bound exceptions before live
  use.
- Higher-risk use cases require stronger evidence for legality, assurance, and human oversight.
- Live services remain subject to retrospective review, incident-triggered review, and periodic
  reassessment.

### Reference Obligations

These principles should be applied alongside relevant legal, regulatory, and policy obligations,
including data protection, equality, human rights, public-sector accessibility, secure-by-design,
records management, and policing-specific governance requirements applicable to the use case.

---

## VIII. Appendix

### Principle Summary Checklist

| Principle | Category | Criticality | Validation |
|-----------|----------|-------------|------------|
| Public value, lawfulness, and proportionality | Strategic | CRITICAL | Use case, legal basis, proportionality assessment |
| Human accountability and contestability | Strategic | CRITICAL | Human decision points, override and challenge paths |
| Security by design and least privilege | Strategic | CRITICAL | Threat model, access controls, security testing |
| Resilience, continuity, and safe degradation | Strategic | HIGH | Failure analysis, fallback paths, runbooks |
| Interoperability and federation | Strategic | HIGH | Versioned interfaces, ownership, compatibility |
| Lawful, purpose-bound, and minimized data use | Data | CRITICAL | Data inventory, minimization rules, lawful purpose |
| Data quality, provenance, and evidential integrity | Data | CRITICAL | Provenance capture, source labeling, quality checks |
| Privacy, confidentiality, and data sovereignty | Data | CRITICAL | Classification, residency, retention, privacy controls |
| Standard interfaces and loose coupling | Integration | HIGH | Service boundaries, contracts, replaceability |
| Controlled autonomy and policy guardrails | Integration | CRITICAL | Autonomy definition, approval controls, kill switch |
| Traceability, transparency, and auditability | Integration | CRITICAL | Audit events, reconstruction, protected records |
| Performance, accessibility, and usability | Quality | HIGH | Performance tests, accessibility review, user testing |
| Maintainability, portability, and change readiness | Quality | HIGH | Documentation, modularity, replacement strategy |
| Assurance by default | Development | CRITICAL | Assurance plan, risk ownership, reassessment |
| Automation, testing, and controlled release | Development | HIGH | Version control, regression testing, rollback |
| Supplier, model, and lifecycle governance | Development | HIGH | Dependency inventory, exit plan, supplier review |
| Continuous monitoring, drift response, and improvement | Development | HIGH | Quality monitoring, thresholds, incident learning |

---

**Document Version History**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-03-07 | ArcKit AI | Initial draft for generative AI architecture principles in UK policing |

## External References

| Document | Type | Source | Key Extractions | Path |
|----------|------|--------|-----------------|------|
| No external governance documents provided at generation time | N/A | Local project context | Principles created from scratch and tailored to UK policing generative AI use | projects/000-global/policies/ |

---

**Generated by**: ArcKit `$arckit-principles` command
**Generated on**: 2026-03-07
**ArcKit Version**: 4.0.0
**Project**: GenAI for UK Policing (Project 000)
**AI Model**: GPT-5 Codex
