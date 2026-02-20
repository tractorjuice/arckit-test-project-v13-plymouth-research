# Vendor Profile: Sentry

| Field | Value |
|-------|-------|
| **Vendor Name** | Sentry (Functional Software Inc.) |
| **Category** | Application Performance Monitoring / Error Tracking |
| **Website** | https://sentry.io |
| **Confidence** | High |
| **Last Researched** | 2026-02-20 |
| **Projects Referenced In** | Project 001 — Plymouth Research Restaurant Menu Analytics |

## Overview

Sentry is an application monitoring platform specialising in error tracking, performance tracing, and alerting. It provides SDK integrations for Python and virtually all major programming languages. The Developer (free) plan supports solo developers with 5,000 error events per month and 30-day retention.

## Products and Services

- **Developer Plan**: Free tier for solo developers
- **Team Plan**: $29/month for teams, more events
- **Business Plan**: $89/month for advanced features
- **Self-Hosted**: Open source (via sentry/self-hosted GitHub repo, AGPL-3.0) — run on own infrastructure

## Pricing Model

| Tier | Price (monthly) | Users | Error Events | Retention |
|------|----------------|-------|-------------|-----------|
| Developer | £0 | 1 | 5,000/month | 30 days |
| Team | ~£23 | Unlimited | More events | 90 days |
| Business | ~£71 | Unlimited | More events | 90 days |

*Pricing verified February 2026 from https://sentry.io/pricing/*

## Python SDK Integration

```python
# Install: pip install sentry-sdk
import sentry_sdk
sentry_sdk.init(
    dsn="https://your-dsn@sentry.io/project-id",
    traces_sample_rate=1.0,
)
```

5 lines of code to instrument a Python application.

## Key Features

- **Error tracking**: Captures exceptions with full stack traces, request context, user context
- **Performance tracing**: Tracks slow database queries, dashboard load times
- **Alerting**: Alert rules (e.g., "alert if scraping job fails", "alert if error rate > 5%")
- **Issue grouping**: Automatically groups similar errors to reduce noise
- **Breadcrumbs**: Timeline of events leading to each error
- **Custom dashboards**: 10 dashboards on Developer plan
- **Integrations**: GitHub, Slack, email, PagerDuty, Jira

## UK Government Presence

Not applicable — SaaS platform hosted on Sentry's cloud infrastructure (US-based). No G-Cloud listing identified.

## Strengths

- Generous free tier (5,000 errors/month) — sufficient for Plymouth Research scale
- Python SDK is mature and well-documented
- Captures scraping pipeline failures automatically via `logger.catch()` equivalent
- 30-day retention provides debugging context
- Spike protection prevents unexpected billing

## Weaknesses

- 1 user limit on free plan (sufficient for single-developer context)
- Data hosted in US (not UK/EU) — acceptable for non-PII operational data
- Free tier errors count can be consumed quickly if scraping loops have unhandled exceptions

## Compliance

- Sentry processes stack traces and application data — no personal user data for Plymouth Research (no user login, public dashboard)
- GDPR-compliant data processing available
- For Plymouth Research: only technical error data (SQL queries, scraping failures) sent to Sentry — no restaurant patron PII

## Competitive Alternatives

| Alternative | Free Tier | Key Difference |
|-------------|-----------|----------------|
| Rollbar | 5,000 events/month free | Similar to Sentry |
| Bugsnag | 7,500 events/month free | Simpler UI |
| Datadog APM | No meaningful free tier | Enterprise focus, expensive |
| Prometheus + Grafana | Self-hosted free | More complex setup, no error tracking |
| Self-hosted Sentry | Free (infra cost) | Full control, higher maintenance |

## Decision Notes

**Recommended**: Adopt Sentry Developer (free) for Plymouth Research Project 001. Addresses NFR-O-002 (metrics/monitoring gap) at zero cost. Focus monitoring on: scraping pipeline failures, database query performance, and dashboard load time tracking. Single-developer constraint is met by the 1-user limit on the Developer plan.
