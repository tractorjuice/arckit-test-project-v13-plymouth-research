# Vendor Profile: Sentry

> **Template Origin**: Official | **ArcKit Version**: 4.0.1

## Document Control

| Field | Value |
|-------|-------|
| **Document ID** | sentry-profile |
| **Document Type** | Vendor Profile |
| **Project** | Plymouth Research Restaurant Menu Analytics (Project 001) |
| **Classification** | PUBLIC |
| **Status** | PUBLISHED |
| **Version** | 1.1 |
| **Created Date** | 2026-02-20 |
| **Last Modified** | 2026-03-08 |
| **Review Cycle** | On-Demand |
| **Next Review Date** | 2027-03-08 |
| **Owner** | Lead Developer |
| **Reviewed By** | PENDING |
| **Approved By** | PENDING |
| **Distribution** | Development Team |
| **Source Research** | ARC-001-RSCH-v1.0, ARC-001-RSCH-v2.0 |
| **Confidence** | High |

## Revision History

| Version | Date | Author | Changes | Approved By | Approval Date |
|---------|------|--------|---------|-------------|---------------|
| 1.0 | 2026-02-20 | AI Agent | Initial creation from `/arckit:research` command. | PENDING | PENDING |
| 1.1 | 2026-03-08 | AI Agent | Updated and validated against `ARC-001-RSCH-v2.0`. Confirmed pricing and features are current. | PENDING | PENDING |

---

## Overview

Sentry is an application monitoring platform specialising in error tracking, performance tracing, and alerting. It provides SDK integrations for Python and virtually all major programming languages. The Developer (free) plan is ideal for solo developers or small projects.

## Products and Services

- **Developer Plan**: Free tier for solo developers.
- **Team Plan**: $29/month for teams with more events.
- **Business Plan**: $89/month for advanced features.
- **Self-Hosted**: Open source (AGPL-3.0) option to run on own infrastructure.

## Pricing Model

| Tier | Price (monthly) | Users | Error Events | Retention |
|------|----------------|-------|-------------|-----------|
| Developer | £0 | 1 | 5,000/month | 30 days |
| Team | ~£23 | Unlimited | 50k-1M events | 90 days |
| Business | ~£71 | Unlimited | 100k-4M events | 90 days |

*Pricing verified March 2026 from https://sentry.io/pricing/*

## Python SDK Integration

```python
# Install: pip install sentry-sdk
import sentry_sdk
sentry_sdk.init(
    dsn="YOUR_SENTRY_DSN",
    traces_sample_rate=1.0,
)
```
Integration is trivial, requiring only a few lines of code to instrument a Python application.

## Key Features

- **Error tracking**: Captures exceptions with full stack traces and request context.
- **Performance tracing**: Tracks slow database queries and dashboard load times.
- **Alerting**: Configurable rules (e.g., "alert if scraping job fails").
- **Issue grouping**: Automatically groups similar errors to reduce noise.
- **Integrations**: GitHub, Slack, email, PagerDuty, Jira.

## UK Government Presence

Not applicable. Sentry is a US-hosted SaaS platform with no specific G-Cloud listing. Data is hosted in the US, which is acceptable for the non-PII operational data of this project.

## Strengths

- Very generous free tier (5,000 errors/month) is more than sufficient for the Plymouth Research project's scale.
- Mature and well-documented Python SDK.
- Can automatically capture failures in the scraping pipeline.
- Provides immediate visibility into application health with minimal setup.

## Weaknesses

- 1 user limit on the free plan (but sufficient for a single-developer project).
- Data hosted in the US, not UK/EU.
- The self-hosted version is complex to maintain.

## Compliance

- Sentry processes stack traces and application data. For this project, this means technical error data (SQL queries, scraping failures), not personal user data.
- Sentry is GDPR-compliant.

## Competitive Alternatives

| Alternative | Free Tier | Key Difference |
|-------------|-----------|----------------|
| Rollbar | 5,000 events/month free | Similar to Sentry. |
| Bugsnag | Free for 1 user, 7,500 events | Similar functionality. |
| Datadog APM | No meaningful free tier | Enterprise-focused and expensive. |

## Projects Referenced In

- **Project 001 — Plymouth Research Restaurant Menu Analytics** (Evaluated in `ARC-001-RSCH-v1.0` and `ARC-001-RSCH-v2.0`)

## Decision Notes

**Recommended**: Adopt Sentry Developer (free) for Project 001. It fully addresses the NFR-O-002 (metrics/monitoring) gap at zero cost. The single-developer constraint is met by the 1-user limit on the free plan.
