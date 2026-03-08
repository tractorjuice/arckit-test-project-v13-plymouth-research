# Tech Note: GitHub Actions for Python CI/CD and Automation

> **Template Origin**: Official | **ArcKit Version**: 4.0.1

## Document Control

| Field | Value |
|-------|-------|
| **Document ID** | github-actions-ci-cd |
| **Document Type** | Tech Note |
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

## Revision History

| Version | Date | Author | Changes | Approved By | Approval Date |
|---------|------|--------|---------|-------------|---------------|
| 1.0 | 2026-02-20 | AI Agent | Initial creation from `/arckit:research` command. | PENDING | PENDING |
| 1.1 | 2026-03-08 | AI Agent | Updated and validated against `ARC-001-RSCH-v2.0`. Added more detailed workflow examples. | PENDING | PENDING |

---

## Summary

GitHub Actions is a CI/CD and automation platform natively integrated into GitHub. For public repositories, it provides a generous free tier with unlimited build minutes on standard Linux runners, making it the default choice for most open-source and public-code projects. It supports cron scheduling for automated jobs, secrets management for credentials, and integrates seamlessly with other GitHub features like Dependabot for a complete, zero-cost CI/CD and DevSecOps solution.

## Key Findings

1.  **Cost-Effective**: GitHub Actions is free for public repositories. A new minor platform fee introduced in March 2026 has a negligible cost impact for this project's scale (approx. £0.10/month for a weekly 1-hour job).

2.  **Cron Scheduling**: The `on.schedule.cron` trigger in a workflow file allows for automated, recurring jobs. This is the ideal solution for the weekly data refresh requirement (BR-006).

3.  **Secrets Management**: The `${{ secrets.VARIABLE_NAME }}` syntax provides a secure way to use API keys and other credentials in workflows without hardcoding them in the repository, a critical security practice.

4.  **Dependabot Integration**: GitHub's free, built-in dependency scanner can be enabled with a simple `.github/dependabot.yml` file. It automatically creates pull requests to fix vulnerable dependencies, addressing requirement NFR-SEC-003.

5.  **Python Native**: The `actions/setup-python` action makes it trivial to set up a specific Python version and cache dependencies, making it a highly efficient environment for running Python tests and scripts.

## Workflow Templates for Project 001

### Weekly Data Refresh (addresses BR-006)

This workflow runs every Sunday at 2 AM to refresh key data sources automatically.

```yaml
# .github/workflows/weekly-refresh.yml
name: Weekly Data Refresh
on:
  schedule:
    - cron: '0 2 * * 0'   # Sundays at 2am GMT
  workflow_dispatch:        # Allows manual trigger from the GitHub UI

jobs:
  refresh:
    runs-on: ubuntu-latest
    timeout-minutes: 360    # 6-hour maximum job time
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: pip install -r projects/001-plymouth-research-restaurant-menu-analytics/requirements.txt

      - name: Refresh FSA Hygiene Ratings
        run: python projects/001-plymouth-research-restaurant-menu-analytics/run_collection.py hygiene

      - name: Refresh Trustpilot Reviews
        run: python projects/001-plymouth-research-restaurant-menu-analytics/run_collection.py trustpilot --update

      - name: Refresh Google Places Data
        run: python projects/001-plymouth-research-restaurant-menu-analytics/run_collection.py google
        env:
          GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}
```

### Continuous Integration Testing (addresses NFR-M-002)

This workflow runs on every push and pull request to ensure code quality and prevent regressions.

```yaml
# .github/workflows/test.yml
name: Test and Lint
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'
      - run: pip install -r projects/001-plymouth-research-restaurant-menu-analytics/requirements.txt
      - run: pip install pytest pytest-cov ruff
      - name: Lint with Ruff
        run: ruff check .
      - name: Run Pytest
        run: pytest projects/001-plymouth-research-restaurant-menu-analytics/tests/ --cov=projects/001-plymouth-research-restaurant-menu-analytics --cov-report=xml
```

## Relevance to Projects

- **Project 001 — Plymouth Research Restaurant Menu Analytics**: GitHub Actions is the recommended solution for closing several key gaps identified in `ARC-001-REQ-v2.0`:
    -   **BR-006 / NFR-Q-003**: The weekly cron job provides data freshness automation.
    -   **NFR-M-002**: The `test.yml` workflow provides automated testing on every PR.
    -   **NFR-M-003**: The YAML workflow files provide "Infrastructure as Code" for the CI/CD process.
    -   **NFR-SEC-003**: Enabling Dependabot provides automated dependency scanning.

---
**Generated by**: ArcKit `/arckit.research` agent
**Generated on**: 2026-03-08
**ArcKit Version**: 4.0.1
**Project**: Plymouth Research Restaurant Menu Analytics (Project 001)
**Model**: gemini-1.5-pro-001
