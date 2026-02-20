# Vendor Profile: GitHub Actions

| Field | Value |
|-------|-------|
| **Vendor Name** | GitHub (Microsoft) |
| **Category** | CI/CD Automation Platform |
| **Website** | https://github.com/features/actions |
| **Confidence** | High |
| **Last Researched** | 2026-02-20 |
| **Projects Referenced In** | Project 001 — Plymouth Research Restaurant Menu Analytics |

## Overview

GitHub Actions is the native CI/CD automation platform built into GitHub. It enables workflows triggered by events (push, pull request, cron schedule) or manual dispatch. For public repositories, GitHub Actions is free with unlimited minutes on standard Linux runners. The project repository for Plymouth Research is on GitHub (confirmed by git status).

## Products and Services

- **GitHub Actions**: Core CI/CD (free for public repos)
- **GitHub-hosted runners**: Managed Linux, Windows, macOS VMs
- **Self-hosted runners**: Install on own infrastructure
- **Dependabot**: Dependency vulnerability scanning (separate, bundled with GitHub)
- **GitHub Packages**: Container registry for Docker images

## Pricing Model

| Context | Price | Minutes |
|---------|-------|---------|
| Public repositories | Free | Unlimited (standard Linux runners) |
| Private repos — GitHub Free | Free | 2,000 min/month, then $0.008/min (Linux) |
| Private repos — GitHub Pro | Free | 3,000 min/month |
| Platform fee (from March 2026) | $0.002/min | Applies to public repos too |

**Plymouth Research impact**: Public repo → free unlimited minutes. New platform fee from March 2026: a 1-hour weekly scraping job costs $0.12/month (~£0.10) — negligible.

*Pricing verified February 2026 from https://docs.github.com/en/actions and https://resources.github.com/actions/2026-pricing-changes-for-github-actions/*

## Key Features

- **YAML workflow files**: `.github/workflows/*.yml` committed to repository
- **Cron scheduling**: `schedule: - cron: '0 2 * * 0'` for weekly Sunday 2am runs
- **Secrets management**: `${{ secrets.GOOGLE_API_KEY }}` for API keys (resolves hardcoded credential risk)
- **Environment**: Ubuntu 22.04, Python 3.x available via `actions/setup-python@v5`
- **Matrix strategy**: Test across multiple Python versions
- **Artefact upload**: Store outputs (scraping logs, database backups)
- **Status checks**: Block PRs if tests fail
- **15+ GB SSD, 7 GB RAM**: Sufficient for scraping + data processing jobs

## UK Government Presence

Not applicable — global developer platform. No G-Cloud listing.

## Key Workflows for Plymouth Research

```yaml
# Weekly data refresh
name: Weekly Data Refresh
on:
  schedule:
    - cron: '0 2 * * 0'  # Sundays at 2am GMT
jobs:
  refresh:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: '3.11'}
      - run: pip install -r requirements.txt
      - run: python run_collection.py hygiene
      - run: python run_collection.py trustpilot
      env:
        GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}
```

## Strengths

- Zero cost for public repositories
- Already in use (project is on GitHub)
- No new platform to learn — YAML workflows are industry standard
- Dependabot integration for automatic security updates
- Secrets management for API keys (resolves NFR-SEC-001 risk)
- 137% year-over-year adoption growth (2025 Octoverse)
- Extensive marketplace: 30,000+ pre-built Actions

## Weaknesses

- YAML syntax can be verbose for complex workflows
- Platform fee introduced March 2026 (minimal impact at Plymouth Research scale)
- Execution environment resets between jobs (no persistent file system — need to upload/download database)
- 6-hour job timeout limit (sufficient for weekly scraping)

## Compliance

- Secrets stored encrypted in GitHub's key management
- Workflow logs may contain non-sensitive operational data
- Public repo: workflow results visible publicly (acceptable for operational scripts)

## Decision Notes

**Recommended**: Adopt GitHub Actions for Plymouth Research Project 001 for:
1. Weekly cron data refresh (BR-006 high-priority gap — automated FSA, Trustpilot, Google Places refresh)
2. pytest on pull requests (NFR-M-002 gap)
3. pip-audit on schedule (NFR-SEC-003 gap)
4. Dependabot enabled via `.github/dependabot.yml` (NFR-SEC-003 gap)

Total implementation: 1–2 days. Total cost: £0 (plus ~£0.10/month platform fee from March 2026).
