# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Plymouth Research is developing a restaurant menu analytics platform for Plymouth, UK. The platform scrapes restaurant websites, normalizes menu data (items, prices, dietary tags), and presents insights through an interactive Streamlit dashboard.

**Tech Stack**: Python, PostgreSQL (SQLite for dev), BeautifulSoup/Scrapy, Streamlit, Pandas

## Project Structure

```
projects/001-plymouth-research-restaurant-menu-analytics/
├── src/                    # Core application code
├── collection/             # Web scraping modules
├── processing/             # ETL and data normalization
├── dashboard/              # Streamlit dashboard components
├── database/               # Schema migrations and DB utilities
├── scripts/                # Utility scripts
├── docs/                   # Project documentation
├── plymouth_research.db    # SQLite database (dev)
├── dashboard_app.py        # Main Streamlit entry point
├── requirements.txt        # Python dependencies
└── *.md                    # ArcKit-generated architecture artifacts
```

## Development Commands

```bash
# Install dependencies
pip install -r projects/001-plymouth-research-restaurant-menu-analytics/requirements.txt

# Run the Streamlit dashboard
streamlit run projects/001-plymouth-research-restaurant-menu-analytics/dashboard_app.py

# Run data collection
python projects/001-plymouth-research-restaurant-menu-analytics/run_collection.py

# Run data processing/ETL
python projects/001-plymouth-research-restaurant-menu-analytics/run_processing.py

# Check ArcKit prerequisites
bash .arckit/scripts/bash/check-prerequisites.sh

# Create new project (if needed)
bash .arckit/scripts/bash/create-project.sh --name "Project Name"
```

## ArcKit Slash Commands

This project uses ArcKit for architecture governance. Key generated artifacts in `projects/001-*/`:
- `requirements.md` - Business and technical requirements
- `stakeholder-drivers.md` - Stakeholder analysis
- `data-model.md` - Database schema design
- `risk-register.md` - Risk assessment
- `dpia.md` - Data Protection Impact Assessment
- `backlog.md` - Product backlog/user stories

Run ArcKit commands via: `/arckit.<command>` (e.g., `/arckit.requirements`, `/arckit.diagram`)

See `DEPENDENCY-MATRIX.md` for command execution order.

## Key Principles (from architecture-principles.md)

1. **Ethical Web Scraping (NON-NEGOTIABLE)**: Respect robots.txt, rate limit (5s/request), honest User-Agent
2. **Privacy by Design (NON-NEGOTIABLE)**: No PII collection, UK GDPR compliance
3. **Data Quality First**: Validate all scraped data before storage
4. **Open Source Preferred**: Use OSS tools unless justified otherwise

## Database

Development uses SQLite (`plymouth_research.db`). Schema migrations are in `database/` and `add_*.sql` files.

Key tables: `restaurants`, `menu_items`, `categories`, `dietary_tags`
