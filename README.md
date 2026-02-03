# Plymouth Restaurant Menu Analytics

A restaurant menu analytics platform for Plymouth, UK that scrapes restaurant websites, normalises menu data (items, prices, dietary tags), and presents insights through an interactive Streamlit dashboard. Managed with [ArcKit](https://github.com/tractorjuice/arc-kit) enterprise architecture governance.

## Tech Stack

Python 3.8+ | SQLite (dev) | Streamlit | Pandas | Plotly | Pydeck | BeautifulSoup

## Quick Start

```bash
# Install dependencies
pip install -r projects/001-plymouth-research-restaurant-menu-analytics/requirements.txt

# Run the Streamlit dashboard (http://localhost:8501)
streamlit run projects/001-plymouth-research-restaurant-menu-analytics/dashboard_app.py

# Run data collection and processing
python projects/001-plymouth-research-restaurant-menu-analytics/run_collection.py
python projects/001-plymouth-research-restaurant-menu-analytics/run_processing.py
```

## Application Architecture

The application follows a **collect → process → present** pipeline:

- **Collection** (`collection/`) — Fetchers for Google Places, Trustpilot, FSA hygiene data; scrapers with robots.txt compliance and rate limiting
- **Processing** (`processing/`) — ETL with fuzzy matching for linking restaurant records across data sources
- **Dashboard** (`dashboard/`) — Streamlit app with 8 tabs: Overview, Menus, Prices, Cuisine, Dietary, Hygiene, Reviews, Map
- **Shared** (`shared/`) — Configuration and dataclass models
- **Scripts** (`scripts/`) — Operational scripts: `fetchers/`, `matchers/`, `importers/`, `utilities/`, `scrapers/`

Database is SQLite (`plymouth_research.db`, ~20 MB). Core tables: `restaurants`, `menu_items`, `trustpilot_reviews`, `google_reviews`.

## Project Artifacts

### Global

| Document | Description |
|----------|-------------|
| [ARC-000-PRIN-v1.0](projects/000-global/ARC-000-PRIN-v1.0.md) | Enterprise architecture principles |

### Project 001 — Plymouth Restaurant Menu Analytics

| Document | Description |
|----------|-------------|
| [ARC-001-REQ-v1.0](projects/001-plymouth-research-restaurant-menu-analytics/ARC-001-REQ-v1.0.md) | Business and technical requirements |
| [ARC-001-STKE-v1.0](projects/001-plymouth-research-restaurant-menu-analytics/ARC-001-STKE-v1.0.md) | Stakeholder analysis |
| [ARC-001-RISK-v1.0](projects/001-plymouth-research-restaurant-menu-analytics/ARC-001-RISK-v1.0.md) | Risk register (Orange Book) |
| [ARC-001-DATA-v1.0](projects/001-plymouth-research-restaurant-menu-analytics/ARC-001-DATA-v1.0.md) | Data model with GDPR compliance |
| [ARC-001-DPIA-v1.0](projects/001-plymouth-research-restaurant-menu-analytics/ARC-001-DPIA-v1.0.md) | Data Protection Impact Assessment |
| [ARC-001-ANAL-v1.0](projects/001-plymouth-research-restaurant-menu-analytics/ARC-001-ANAL-v1.0.md) | Governance quality analysis |
| [ARC-001-BLOG-v1.0](projects/001-plymouth-research-restaurant-menu-analytics/ARC-001-BLOG-v1.0.md) | Product backlog |

### Cloud Platform Research

| Document | Platform | Estimated Cost | Summary |
|----------|----------|----------------|---------|
| [ARC-001-AZRS-v1.0](projects/001-plymouth-research-restaurant-menu-analytics/research/ARC-001-AZRS-v1.0.md) | Azure | ~£26/month | App Service + PostgreSQL Flexible Server + Azure Functions |
| [ARC-001-AWRS-v1.0](projects/001-plymouth-research-restaurant-menu-analytics/research/ARC-001-AWRS-v1.0.md) | AWS | ~£71/month (£31 optimised) | App Runner + RDS PostgreSQL + Lambda |
| [ARC-001-RSCH-001-v1.0](projects/001-plymouth-research-restaurant-menu-analytics/research/ARC-001-RSCH-001-v1.0.md) | General | — | Technology research and build vs buy |

## Repository Structure

```
├── .arckit/                  # Governance framework (templates, scripts, memory)
├── .claude/commands/         # ArcKit slash command definitions
├── .claude/agents/           # Agent configs (AWS, Azure, DataScout, research)
├── projects/
│   ├── 000-global/           # Global architecture principles
│   └── 001-plymouth-research-restaurant-menu-analytics/
│       ├── collection/       # Web scraping modules
│       ├── processing/       # ETL and data normalisation
│       ├── dashboard/        # Streamlit dashboard (8 tabs)
│       ├── shared/           # Config and models
│       ├── scripts/          # Operational scripts
│       ├── research/         # Cloud platform research (Azure, AWS)
│       ├── dashboard_app.py  # Main Streamlit entry point
│       └── ARC-001-*.md      # Architecture artifacts
├── DEPENDENCY-MATRIX.md      # ArcKit command execution order
└── docs/                     # Documentation and guides
```

## ArcKit Governance

Run ArcKit commands via `/arckit.<command>` in Claude Code, Gemini CLI, or Codex CLI. 43 commands available:

| Category | Commands |
|----------|----------|
| Planning | `plan`, `principles`, `stakeholders`, `risk`, `sobc` |
| Requirements | `requirements`, `data-model`, `adr`, `backlog` |
| Research | `research`, `azure-research`, `aws-research`, `datascout`, `wardley` |
| Procurement | `sow`, `dos`, `gcloud-search`, `gcloud-clarify`, `evaluate` |
| Design | `diagram`, `hld-review`, `dld-review`, `roadmap`, `platform-design` |
| Compliance | `secure`, `mod-secure`, `tcop`, `service-assessment`, `dpia`, `ai-playbook`, `atrs`, `jsp-936` |
| Operations | `devops`, `finops`, `mlops`, `servicenow`, `operationalize`, `data-mesh-contract` |
| Quality | `traceability`, `analyze`, `principles-compliance` |
| Reporting | `story`, `pages` |

See [DEPENDENCY-MATRIX.md](DEPENDENCY-MATRIX.md) for command execution order and critical paths.

## Documentation

- [ArcKit Framework](https://github.com/tractorjuice/arc-kit)
- [Command Guides](docs/guides/)
- [Dependency Matrix](DEPENDENCY-MATRIX.md)
- [Project CLAUDE.md](projects/001-plymouth-research-restaurant-menu-analytics/CLAUDE.md)
