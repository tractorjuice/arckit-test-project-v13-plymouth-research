# Tech Note: GitHub Actions for Python CI/CD and Automation

| Field | Value |
|-------|-------|
| **Topic** | GitHub Actions: CI/CD, Cron Scheduling, Dependency Security |
| **Category** | CI/CD / Automation / DevSecOps |
| **Last Updated** | 2026-02-20 |
| **Relevance to Projects** | Project 001 — Plymouth Research Restaurant Menu Analytics |

## Summary

GitHub Actions is a CI/CD automation platform integrated with GitHub. For public repositories, it provides unlimited free minutes on standard Linux runners. It supports cron scheduling, enabling automated weekly data refresh pipelines. Combined with Dependabot, it provides a complete zero-cost CI/CD + dependency security solution for Python projects.

## Key Findings

1. **Free for public repos**: Plymouth Research repository is public on GitHub. GitHub Actions usage is free with unlimited standard runner minutes. The March 2026 platform fee of $0.002/min adds ~$0.12/month for a 1-hour weekly scraping job — negligible.

2. **Cron scheduling**: YAML `on.schedule.cron` supports standard cron syntax. A weekly Sunday 2am GMT job: `cron: '0 2 * * 0'`. Directly resolves BR-006 data freshness automation gap.

3. **Secrets management**: `${{ secrets.VARIABLE_NAME }}` stores API keys (Google Places, Companies House) encrypted in GitHub. Resolves hardcoded credential risk (NFR-SEC-001).

4. **Dependabot**: Free built-in dependency scanner. A 5-line `.github/dependabot.yml` enables automatic vulnerability PR creation. Supports Python (pip), GitHub Actions, Docker. 137% YoY adoption growth (GitHub Octoverse 2025).

5. **pip-audit**: Apache-2.0 Python dependency scanner by Trail of Bits + Google. Run as GitHub Actions step. Cross-references PyPI Advisory Database and OSV database. `--fix` flag auto-upgrades vulnerable packages.

6. **Runner specifications**: Ubuntu 22.04 LTS, 7 GB RAM, 14 GB SSD, 2 vCPU. Sufficient for scraping + data processing + pytest runs.

## Workflow Templates for Plymouth Research

### Weekly Data Refresh (BR-006 gap)

```yaml
# .github/workflows/weekly-refresh.yml
name: Weekly Data Refresh
on:
  schedule:
    - cron: '0 2 * * 0'   # Sundays at 2am GMT
  workflow_dispatch:        # Allow manual trigger

jobs:
  refresh:
    runs-on: ubuntu-latest
    timeout-minutes: 360    # 6-hour max
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'
      - run: pip install -r requirements.txt
      - name: Refresh FSA Hygiene Ratings
        run: python run_collection.py hygiene --xml data/raw/plymouth_fsa_data.xml
      - name: Refresh Trustpilot Reviews (incremental)
        run: python run_collection.py trustpilot --update
      - name: Refresh Google Places
        run: python run_collection.py google
        env:
          GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}
```

### Dependabot Configuration (NFR-SEC-003 gap)

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/projects/001-plymouth-research-restaurant-menu-analytics"
    schedule:
      interval: "weekly"
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "monthly"
```

### Test and Lint (NFR-M-002 gap)

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: '3.11'}
      - run: pip install -r requirements.txt pytest pytest-cov
      - run: pytest tests/ --cov=. --cov-report=xml
```

## Relevance to Projects

**Project 001**: Resolves 4 gaps identified in ARC-001-REQ-v2.0:
- BR-006/NFR-Q-003: Weekly cron data refresh automation
- NFR-M-002: pytest in CI on every PR
- NFR-M-003: Infrastructure workflows as code
- NFR-SEC-003: Dependabot + pip-audit dependency scanning

## References

- GitHub Actions billing: https://docs.github.com/billing/managing-billing-for-github-actions
- GitHub Actions 2026 pricing: https://resources.github.com/actions/2026-pricing-changes-for-github-actions/
- Dependabot: https://docs.github.com/en/code-security/dependabot
- pip-audit: https://github.com/pypa/pip-audit
