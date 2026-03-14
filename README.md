# Plymouth Restaurant Menu Analytics

A restaurant data analytics platform for Plymouth, UK that aggregates data from 8 free public sources — food hygiene ratings, customer reviews, menu prices, company filings, and geographic data — and presents insights through an interactive Streamlit dashboard. Managed with [ArcKit](https://github.com/tractorjuice/arc-kit) enterprise architecture governance.

## Tech Stack

Python 3.8+ | SQLite | Streamlit | Pandas | Plotly | Pydeck | BeautifulSoup

## Data at a Glance

| Metric | Value |
|--------|-------|
| Restaurants tracked | 242 |
| Menu items scraped | 2,593 |
| Trustpilot reviews | 9,410 |
| Google reviews | 481 |
| FSA hygiene matches | 201 |
| Data sources | 8 (all free) |

## Quick Start

```bash
# Install dependencies
pip install -r projects/001-plymouth-research-restaurant-menu-analytics/requirements.txt

# Run the Streamlit dashboard (http://localhost:8501)
streamlit run projects/001-plymouth-research-restaurant-menu-analytics/dashboard_app.py

# Data collection (subcommands: hygiene, trustpilot, google, scrape)
python projects/001-plymouth-research-restaurant-menu-analytics/run_collection.py hygiene --xml data/raw/plymouth_fsa_data.xml
python projects/001-plymouth-research-restaurant-menu-analytics/run_collection.py trustpilot --restaurant-id 4 --max-pages 10
python projects/001-plymouth-research-restaurant-menu-analytics/run_collection.py google --restaurant-id 4
python projects/001-plymouth-research-restaurant-menu-analytics/run_collection.py scrape --restaurant-id 4 --url https://example.com/menu

# Data processing (subcommands: stats, match, import)
python projects/001-plymouth-research-restaurant-menu-analytics/run_processing.py stats
```

## Application Architecture

The application follows a **collect → process → present** pipeline:

- **Collection** (`collection/`) — Fetchers for FSA hygiene data, Trustpilot reviews, Google Places API; scrapers with robots.txt compliance and rate limiting
- **Processing** (`processing/`) — ETL with fuzzy matching (name similarity + postcode + address scoring) for linking records across data sources
- **Dashboard** (`dashboard/`) — Streamlit app with 8 tabs: Overview, Menus, Prices, Cuisine, Dietary, Hygiene, Reviews, About
- **Shared** (`shared/`) — Singleton config with path management, scraping params, matching thresholds
- **Scripts** (`scripts/`) — Operational scripts: `fetchers/`, `matchers/`, `importers/`, `utilities/`

Database is SQLite (`plymouth_research.db`, ~20 MB). Core tables: `restaurants` (52 cols), `menu_items`, `trustpilot_reviews`, `google_reviews`.

## Project Artifacts

### Global

| Document | Description |
|----------|-------------|
| [ARC-000-PRIN-v1.0](projects/000-global/ARC-000-PRIN-v1.0.md) | Enterprise architecture principles |

### Project 001 — Core Artifacts

| Document | Description |
|----------|-------------|
| [ARC-001-REQ-v2.0](projects/001-plymouth-research-restaurant-menu-analytics/ARC-001-REQ-v2.0.md) | Business and technical requirements |
| [ARC-001-STKE-v1.0](projects/001-plymouth-research-restaurant-menu-analytics/ARC-001-STKE-v1.0.md) | Stakeholder analysis |
| [ARC-001-RISK-v1.0](projects/001-plymouth-research-restaurant-menu-analytics/ARC-001-RISK-v1.0.md) | Risk register (Orange Book) |
| [ARC-001-DATA-v1.0](projects/001-plymouth-research-restaurant-menu-analytics/ARC-001-DATA-v1.0.md) | Data model with GDPR compliance |
| [ARC-001-DPIA-v1.0](projects/001-plymouth-research-restaurant-menu-analytics/ARC-001-DPIA-v1.0.md) | Data Protection Impact Assessment |
| [ARC-001-EVAL-v1.0](projects/001-plymouth-research-restaurant-menu-analytics/ARC-001-EVAL-v1.0.md) | Vendor evaluation criteria |
| [ARC-001-BKLG-v1.0](projects/001-plymouth-research-restaurant-menu-analytics/ARC-001-BKLG-v1.0.md) | Product backlog |
| [ARC-001-TRAC-v2.0](projects/001-plymouth-research-restaurant-menu-analytics/ARC-001-TRAC-v2.0.md) | Traceability matrix |
| [ARC-001-ANAL-v2.0](projects/001-plymouth-research-restaurant-menu-analytics/ARC-001-ANAL-v2.0.md) | Governance quality analysis |
| [ARC-001-DSCT-v1.0](projects/001-plymouth-research-restaurant-menu-analytics/ARC-001-DSCT-v1.0.md) | Data source discovery |

### Research & Decisions

| Document | Description |
|----------|-------------|
| [ARC-001-RSCH-v2.0](projects/001-plymouth-research-restaurant-menu-analytics/ARC-001-RSCH-v2.0.md) | Technology research and build vs buy |
| [ARC-001-AZRS-v1.0](projects/001-plymouth-research-restaurant-menu-analytics/research/ARC-001-AZRS-v1.0.md) | Azure research (~£26/month) |
| [ARC-001-AWRS-v1.0](projects/001-plymouth-research-restaurant-menu-analytics/research/ARC-001-AWRS-v1.0.md) | AWS research (~£71/month) |
| [ARC-001-GCRS-v1.0](projects/001-plymouth-research-restaurant-menu-analytics/research/ARC-001-GCRS-v1.0.md) | Google Cloud research |
| [ARC-001-ADR-001-v1.0](projects/001-plymouth-research-restaurant-menu-analytics/decisions/ARC-001-ADR-001-v1.0.md) | ADR-001: Architecture decision |
| [ARC-001-ADR-002-v1.0](projects/001-plymouth-research-restaurant-menu-analytics/decisions/ARC-001-ADR-002-v1.0.md) | ADR-002: Architecture decision |

### Articles

| Document | Description |
|----------|-------------|
| [Plymouth Restaurant Data Article](projects/001-plymouth-research-restaurant-menu-analytics/docs/articles/plymouth-restaurant-data-article.md) | Data journalism feature on 8-source restaurant analytics |

## Repository Structure

```
├── .arckit/                  # Governance framework (templates, scripts, memory)
├── projects/
│   ├── 000-global/           # Global architecture principles
│   └── 001-plymouth-research-restaurant-menu-analytics/
│       ├── collection/       # Web scraping modules
│       ├── processing/       # ETL and data normalisation
│       ├── dashboard/        # Streamlit dashboard (8 tabs)
│       ├── shared/           # Config and models
│       ├── scripts/          # Operational scripts
│       ├── research/         # Cloud platform research (Azure, AWS, GCP)
│       ├── decisions/        # Architecture Decision Records
│       ├── vendors/          # Vendor profiles and scoring
│       ├── docs/articles/    # Data journalism articles
│       ├── dashboard_app.py  # Main Streamlit entry point
│       └── ARC-001-*.md      # Architecture artifacts
├── DEPENDENCY-MATRIX.md      # ArcKit command execution order
└── docs/                     # Documentation site, guides, and health data
```

## ArcKit Governance

Run ArcKit commands via `/arckit.<command>` in Claude Code, Gemini CLI, or Codex CLI:

| Category | Commands |
|----------|----------|
| Planning | `plan`, `principles`, `stakeholders`, `risk`, `sobc`, `strategy`, `roadmap` |
| Requirements | `requirements`, `data-model`, `adr`, `backlog` |
| Research | `research`, `azure-research`, `aws-research`, `gcp-research`, `datascout`, `wardley` |
| Procurement | `sow`, `dos`, `gcloud-search`, `gcloud-clarify`, `evaluate`, `score` |
| Design | `diagram`, `hld-review`, `dld-review`, `design-review`, `platform-design` |
| Compliance | `secure`, `mod-secure`, `tcop`, `service-assessment`, `dpia`, `ai-playbook`, `atrs`, `jsp-936`, `conformance` |
| Operations | `devops`, `finops`, `mlops`, `servicenow`, `operationalize`, `data-mesh-contract` |
| Quality | `traceability`, `analyze`, `principles-compliance`, `health` |
| Reporting | `story`, `pages`, `presentation` |

See [DEPENDENCY-MATRIX.md](DEPENDENCY-MATRIX.md) for command execution order and critical paths.

## Documentation

- [ArcKit Framework](https://github.com/tractorjuice/arc-kit)
- [Command Guides](docs/guides/)
- [Documentation Site](docs/index.html)
- [Dependency Matrix](DEPENDENCY-MATRIX.md)
- [Project CLAUDE.md](projects/001-plymouth-research-restaurant-menu-analytics/CLAUDE.md)
