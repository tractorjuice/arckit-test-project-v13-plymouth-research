# Vendor Profile: Render

> **Template Origin**: Official | **ArcKit Version**: 4.0.1

## Document Control

| Field | Value |
|-------|-------|
| **Document ID** | render-profile |
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
| **Confidence** | Medium |

## Revision History

| Version | Date | Author | Changes | Approved By | Approval Date |
|---------|------|--------|---------|-------------|---------------|
| 1.0 | 2026-02-20 | AI Agent | Initial creation from `/arckit:research` command. | PENDING | PENDING |
| 1.1 | 2026-03-08 | AI Agent | Updated and validated against `ARC-001-RSCH-v2.0`. Confirmed pricing and features are current. | PENDING | PENDING |

---

## Overview

Render is a cloud platform for deploying and scaling web services, background workers, cron jobs, and databases. It targets developers who want managed hosting with minimal DevOps overhead, positioning itself as a modern alternative to Heroku.

## Products and Services

- **Web Services**: Deploy Python, Node.js, Ruby, Docker containers.
- **Static Sites**: Host static files and Single Page Applications.
- **Background Workers**: Run long-running background processes.
- **Cron Jobs**: Execute scheduled tasks.
- **Databases**: Managed PostgreSQL.

## Pricing Model

| Tier | Price (monthly) | RAM | CPU | Notes |
|------|----------------|-----|-----|-------|
| Free | £0 | 512 MB | Shared | Auto-sleep after 15 min inactivity, 750 hours/month, 100 GB bandwidth |
| Starter | ~£5.50 | 512 MB | 0.5 vCPU | Always-on, no sleep, unlimited hours |
| Standard | ~£20 | 2 GB | 1 vCPU | Production workloads |
| Pro | ~£85 | 4 GB | 2 vCPU | High-traffic applications |

*Pricing verified March 2026 from https://render.com*

## Key Features

- Deploy directly from a GitHub repository.
- Free automatic HTTPS/TLS on all tiers.
- Custom domains supported on all tiers, including the free plan.
- Managed PostgreSQL database available (free tier has limitations).
- No platform-specific branding restrictions.
- Health checks and automatic restarts for services.

## UK Government Presence

Not applicable. Render is a US company using major cloud providers (AWS, GCP) for its infrastructure. It does not have a specific G-Cloud listing.

## Strengths

- The free tier is comparable to Streamlit Community Cloud, offering a good alternative.
- The 'Starter' plan at ~£5.50/month provides an "always-on" service, which resolves the NFR-A-001 (uptime) risk associated with free tiers that sleep.
- Platform agnostic: can deploy any Python/Docker application, not just Streamlit.
- Supports custom domains on the free tier.

## Weaknesses

- The free tier's auto-sleep functionality is a limitation for production services needing consistent availability.
- The free PostgreSQL tier is not suitable for production as it is deleted after 90 days.
- Limited compute resources on the free tier (512 MB RAM) may be insufficient for more complex applications.

## Compliance

- SOC 2 Type II certified.
- Provides GDPR compliance features.
- Suitable for hosting applications with public data, like the Plymouth Research project.

## Competitive Alternatives

| Alternative | Free Tier | Key Difference |
|-------------|-----------|----------------|
| Streamlit Community Cloud | Yes | Streamlit-optimised, but public repos only and app sleeps. |
| Railway | No (credits only) | Developer-focused but lacks a true free tier. |
| Fly.io | No (trial only) | Focused on global edge deployment, more complex pricing. |
| Heroku | No meaningful free tier | The legacy PaaS, now generally more expensive. |
| Self-hosted VPS (Hetzner) | No | Cheapest paid option, but requires significant manual server administration. |

## Projects Referenced In

- **Project 001 — Plymouth Research Restaurant Menu Analytics** (Evaluated in `ARC-001-RSCH-v1.0` and `ARC-001-RSCH-v2.0`)

## Decision Notes

**Recommended**: Render is the designated fallback hosting option for Project 001. The primary deployment will remain on Streamlit Community Cloud. If the public launch drives consistent traffic that requires an "always-on" service to meet uptime requirement NFR-A-001, the project should migrate to the Render 'Starter' plan. At ~£5.50/month, this remains well within the project's £100/month budget (BR-003).
