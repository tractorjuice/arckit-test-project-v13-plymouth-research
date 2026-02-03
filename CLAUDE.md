# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This repo has two layers: (1) an **ArcKit governance framework** that generates architecture artifacts via slash commands, and (2) a **Python application** — a restaurant menu analytics platform for Plymouth, UK that scrapes restaurant websites, normalizes menu data, and presents insights through a Streamlit dashboard.

**Tech Stack**: Python 3.8+, SQLite (dev), Streamlit, Pandas, Plotly, Pydeck, BeautifulSoup

## Repository Layout

- `.arckit/` — Governance framework: templates (44 document types), bash helper scripts, memory
- `.claude/commands/` — ArcKit slash command definitions (`/arckit.*`)
- `.claude/agents/` — Agent configs for research tasks (AWS, Azure, DataScout, general research)
- `projects/000-global/` — Global architecture principles (`ARC-000-PRIN-v1.0.md`)
- `projects/001-plymouth-research-restaurant-menu-analytics/` — Main application and project artifacts
- `DEPENDENCY-MATRIX.md` — Command execution order and critical paths for ArcKit workflows

The application code lives entirely under `projects/001-plymouth-research-restaurant-menu-analytics/`. That directory has its own detailed `CLAUDE.md` with schema docs, matching algorithms, and troubleshooting.

## Development Commands

```bash
# Load environment (sets CODEX_HOME=.codex)
direnv allow

# Install Python dependencies
pip install -r projects/001-plymouth-research-restaurant-menu-analytics/requirements.txt

# Run the Streamlit dashboard (opens at http://localhost:8501)
streamlit run projects/001-plymouth-research-restaurant-menu-analytics/dashboard_app.py

# Run data collection / processing
python projects/001-plymouth-research-restaurant-menu-analytics/run_collection.py
python projects/001-plymouth-research-restaurant-menu-analytics/run_processing.py

# Refresh FSA hygiene data
python projects/001-plymouth-research-restaurant-menu-analytics/scripts/fetchers/fetch_hygiene_ratings_v2.py

# Refresh Trustpilot reviews (incremental)
python projects/001-plymouth-research-restaurant-menu-analytics/scripts/fetchers/fetch_trustpilot_reviews.py --update

# ArcKit helpers
bash .arckit/scripts/bash/check-prerequisites.sh
bash .arckit/scripts/bash/create-project.sh --name "Project Name"
bash .arckit/scripts/bash/list-projects.sh
```

## Application Architecture

The application follows a **collect → process → present** pipeline:

- **Collection** (`collection/`) — Fetchers for Google Places, Trustpilot, FSA hygiene data; scrapers with robots.txt compliance and rate limiting (`rate_limiter.py`, `robots_parser.py`)
- **Processing** (`processing/`) — ETL with fuzzy matching (`fuzzy_matcher.py`) for linking restaurant records across data sources. Matching uses `difflib.SequenceMatcher` with configurable thresholds (0.60 minimum, 0.95 high confidence)
- **Dashboard** (`dashboard/`) — Streamlit app with 8 tabs (Overview, Menus, Prices, Cuisine, Dietary, Hygiene, Reviews, Map). Components split into `tabs/`, `components/`, and `data_loader.py`
- **Shared** (`shared/`) — `config.py` (singleton with scraping params, DB config, matching thresholds) and `models.py` (dataclass models)
- **Scripts** (`scripts/`) — Operational scripts organized by function: `fetchers/`, `matchers/`, `importers/`, `utilities/`, `scrapers/`

Database is SQLite (`plymouth_research.db`, ~20 MB). Core tables: `restaurants` (52 cols), `menu_items`, `trustpilot_reviews`, `google_reviews`. Schema migrations are `add_*.sql` files in the project root.

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
- **Git LFS**: Enforced via pre-push hook — ensure LFS is installed locally
