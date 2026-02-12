# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This repo has two layers: (1) an **ArcKit governance framework** that generates architecture artifacts via slash commands, and (2) a **Python application** — a restaurant menu analytics platform for Plymouth, UK that scrapes restaurant websites, normalizes menu data, and presents insights through a Streamlit dashboard.

**Tech Stack**: Python 3.8+, SQLite, Streamlit, Pandas, Plotly, Pydeck, BeautifulSoup

## Repository Layout

- `.arckit/` — Governance framework: templates (44 document types), bash helper scripts, memory
- `.claude/commands/` — ArcKit slash command definitions (`/arckit.*`)
- `.claude/agents/` — Agent configs for research tasks (AWS, Azure, DataScout, general research)
- `projects/000-global/` — Global architecture principles (`ARC-000-PRIN-v1.0.md`)
- `projects/001-plymouth-research-restaurant-menu-analytics/` — Main application and project artifacts
- `DEPENDENCY-MATRIX.md` — Command execution order and critical paths for ArcKit workflows

All application code lives under `projects/001-plymouth-research-restaurant-menu-analytics/` (referred to as `APP_DIR` below). That directory has its own detailed `CLAUDE.md` with schema docs, matching algorithms, and troubleshooting.

## Development Commands

```bash
# Load environment (sets CODEX_HOME=.codex)
direnv allow

# Install Python dependencies (dashboard-only; scraping deps are commented out)
pip install -r APP_DIR/requirements.txt

# Run the Streamlit dashboard (http://localhost:8501)
streamlit run APP_DIR/dashboard_app.py

# Data collection (subcommands: hygiene, trustpilot, google, scrape)
python APP_DIR/run_collection.py hygiene --xml data/raw/plymouth_fsa_data.xml
python APP_DIR/run_collection.py trustpilot --restaurant-id 4 --max-pages 10
python APP_DIR/run_collection.py google
python APP_DIR/run_collection.py scrape --url https://example.com/menu

# Data processing (subcommands: stats, match, import)
python APP_DIR/run_processing.py stats
python APP_DIR/run_processing.py match
python APP_DIR/run_processing.py import

# Interactive matching UI (Streamlit app for manual data matching)
streamlit run APP_DIR/interactive_matcher_app.py

# Refresh FSA hygiene data
python APP_DIR/scripts/fetchers/fetch_hygiene_ratings_v2.py

# Refresh Trustpilot reviews (incremental)
python APP_DIR/scripts/fetchers/fetch_trustpilot_reviews.py --update

# ArcKit helpers
bash .arckit/scripts/bash/check-prerequisites.sh
bash .arckit/scripts/bash/create-project.sh --name "Project Name"
bash .arckit/scripts/bash/list-projects.sh
```

There is no test suite or test runner configured. Testing is manual/exploratory.

## Application Architecture

The application follows a **collect → process → present** pipeline:

```
External Data (FSA XML, Trustpilot, Google Places API)
    → Fetchers (collection/fetchers/)
    → Fuzzy Matching (processing/matchers/)
    → Database Import (processing/database/)
    → SQLite (plymouth_research.db)
    → Cached Data Loading (dashboard/data_loader.py)
    → Streamlit Dashboard (dashboard_app.py)
```

### Key architectural patterns

- **Singleton config** — `shared/config.py` exposes `get_config()` returning a global `Config` instance with path management (handles local dev, Streamlit Cloud, subdirectory contexts), scraping params, DB config, and matching thresholds
- **Pluggable fetcher architecture** — `collection/fetchers/base_fetcher.py` defines an abstract `BaseFetcher` with `fetch()` → `process()` → `run()` lifecycle. Concrete implementations: `HygieneFetcher`, `TrustpilotFetcher`, `GooglePlacesFetcher`
- **Multi-factor fuzzy matching** — `processing/matchers/fuzzy_matcher.py` scores on name similarity (0-100 pts via `difflib.SequenceMatcher`), postcode bonus (50 pts), and address similarity (0-30 pts). Thresholds: 0.60 minimum, 0.70 auto-match, 0.95 high confidence
- **Modular dashboard** — Tabs in `dashboard/tabs/`, reusable components in `dashboard/components/`, cached queries in `dashboard/data_loader.py` (1-hour TTL)
- **SQLite with triggers/views** — Auto-updating restaurant stats via triggers on review insert/delete; pre-aggregated views for dashboard performance

### Database

SQLite (`plymouth_research.db`, ~20 MB). Core tables: `restaurants` (52 cols), `menu_items`, `trustpilot_reviews`, `google_reviews`. Schema migrations are `add_*.sql` files in the application root. Data files and the database are `.gitignored`, not tracked in the repo.

### Deployment

`requirements.txt` includes only dashboard dependencies (streamlit, pandas, plotly, pydeck, validators) for Streamlit Cloud deployment. Scraping dependencies (requests, beautifulsoup4, lxml) are commented out and must be installed separately for local data collection.

## Key Principles (NON-NEGOTIABLE)

From `projects/000-global/ARC-000-PRIN-v1.0.md`:

1. **Ethical Web Scraping**: Respect robots.txt, rate limit (5s minimum between requests), honest User-Agent (`PlymouthResearchMenuScraper/1.0`), 30s timeout, max 3 retries
2. **Privacy by Design**: No PII collection, UK GDPR compliance, DPIA documented
3. **Data Quality First**: Validate at ingestion, duplicate detection, quarantine failed validation
4. **Open Source Preferred**: Evaluate OSS first, avoid vendor lock-in

## ArcKit Governance

Run ArcKit commands via `/arckit.<command>` (e.g., `/arckit.requirements`, `/arckit.diagram`). Artifacts use Document ID naming: `ARC-{PROJECT_ID}-{TYPE}-v*.md`.

See `DEPENDENCY-MATRIX.md` for the full dependency structure. The typical project path is:
```
plan → principles → stakeholders → risk → sobc → requirements → data-model → research → ...
```

Requirements (`ARC-*-REQ-*.md`) is the central artifact consumed by 37+ downstream commands. Principles (`ARC-000-PRIN-v*.md`) is the governance foundation consumed by 20+ commands.

## Conventions

- **Commits**: Conventional Commit prefixes (`feat:`, `docs:`, `chore:`)
- **Markdown**: Sentence-case headings, ~100 char line wrap
- **Bash scripts**: `set -euo pipefail`, use snake_case helpers from `.arckit/scripts/bash/common.sh`
- **Script validation**: `bash -n <script>` and `shellcheck <script>` before changes
- **Slash commands**: Filenames use `arckit.<topic>.md` stem; keep `.claude/commands/` and `.codex/prompts/` aligned
