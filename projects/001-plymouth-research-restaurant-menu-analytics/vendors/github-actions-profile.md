# Vendor Profile: GitHub Actions

> **Template Origin**: Official | **ArcKit Version**: 4.0.1

## Document Control

| Field | Value |
|-------|-------|
| **Document ID** | github-actions-profile |
| **Document Type** | Vendor Profile |
| **Project** | Plymouth Research Restaurant Menu Analytics (Project 001) |
| **Classification** | PUBLIC |
| **Status** | PUBLISHED |
| **Version** | 1.2 |
| **Created Date** | 2026-02-20 |
| **Last Modified** | 2026-03-08 |
| **Review Cycle** | On-Demand |
| **Next Review Date** | 2027-03-08 |
| **Owner** | Lead Developer |
| **Reviewed By** | PENDING |
| **Approved By** | PENDING |
| **Distribution** | Development Team |
| **Source Research** | ARC-001-RSCH-v1.0, ARC-001-RSCH-v2.0, ARC-001-RSCH-v2.1 |
| **Confidence** | High |

## Revision History

| Version | Date | Author | Changes | Approved By | Approval Date |
|---------|------|--------|---------|-------------|---------------|
| 1.0 | 2026-02-20 | AI Agent | Initial creation from `/arckit:research` command. | PENDING | PENDING |
| 1.1 | 2026-03-08 | AI Agent | Updated and validated against `ARC-001-RSCH-v2.0`. Confirmed pricing and features are current. | PENDING | PENDING |
| 1.2 | 2026-03-08 | AI Agent | Refreshed against `ARC-001-RSCH-v2.1`. Reconfirmed GitHub-native automation as the default CI and scheduling path. | PENDING | PENDING |

---

## Overview

GitHub Actions is the native CI/CD automation platform built into GitHub. It enables workflows triggered by repository events such as code pushes, pull requests, or on a schedule (cron). For public repositories, GitHub Actions is free with generous limits, making it the default choice for open-source projects or projects with public codebases.

## Products and Services

- **GitHub Actions**: The core CI/CD platform (free for public repos).
- **GitHub-hosted runners**: Managed Linux, Windows, and macOS virtual machines for running jobs.
- **Dependabot**: Integrated dependency vulnerability scanning and automated pull requests.
- **GitHub Packages**: Integrated container registry for Docker images.

## Pricing Model

| Context | Price | Minutes |
|---------|-------|---------|
| Public repositories | Free | Unlimited (standard Linux runners) |
| Private repos — GitHub Free | Free | 2,000 min/month, then $0.008/min (Linux) |
| Platform fee (from March 2026) | $0.002/min | A minor fee applicable to public repos. |

**Impact for Plymouth Research**: As a public repository, usage is free and effectively unlimited. A weekly 1-hour scraping job would cost approximately £0.10/month, which is negligible.

*Pricing verified March 2026.*

## Key Features

- **YAML Workflows**: CI/CD pipelines are defined as code in `.github/workflows/*.yml`.
- **Cron Scheduling**: `schedule: - cron: '0 2 * * 0'` enables automated weekly jobs, perfect for data refresh tasks.
- **Secrets Management**: `${{ secrets.API_KEY }}` provides secure storage for API keys and other credentials.
- **Standardized Environments**: GitHub-hosted runners provide consistent Ubuntu, Windows, and macOS environments with pre-installed software.
- **Marketplace**: A vast marketplace of over 30,000 pre-built Actions for common tasks.

## UK Government Presence

Not applicable. GitHub Actions is a global developer platform with no specific G-Cloud listing.

## Strengths

- Zero cost for public repositories.
- Natively integrated into the GitHub platform where the project code already resides.
- Industry-standard YAML syntax for defining workflows.
- Integrated secrets management resolves risks associated with hardcoded credentials.
- Free and automatic dependency scanning via the integrated Dependabot service.

## Weaknesses

- YAML syntax can become complex for very elaborate pipelines.
- Runner environments are ephemeral; data does not persist between jobs without using artifacts.
- Subject to a 6-hour timeout limit per job, though this is ample for most use cases.

## Compliance

- Secrets are stored encrypted within GitHub.
- As the repository is public, workflow logs and results are also public, which is acceptable for this project's non-sensitive operational scripts.

## Projects Referenced In

- **Project 001 — Plymouth Research Restaurant Menu Analytics** (Evaluated in `ARC-001-RSCH-v1.0` and `ARC-001-RSCH-v2.0`)

## Decision Notes

**Recommended**: GitHub Actions is the definitive choice for CI/CD and automation for Project 001. It directly addresses three critical gaps identified in the requirements:
1.  **BR-006**: Automates the weekly data refresh via cron scheduling.
2.  **NFR-M-002**: Automates the execution of `pytest` on every pull request.
3.  **NFR-SEC-003**: Automates dependency security scanning via Dependabot and `pip-audit`.

The implementation is low-effort (1–2 days) and the cost is zero, making it a high-value addition to the project.
