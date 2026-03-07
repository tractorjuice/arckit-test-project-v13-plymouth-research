# GEMINI.md

## Project Overview

This project is a restaurant menu analytics platform for Plymouth, UK. It scrapes restaurant websites, normalises menu data (items, prices, dietary tags), and presents insights through an interactive Streamlit dashboard. The project is managed with ArcKit enterprise architecture governance.

The application follows a "collect → process → present" pipeline:

*   **Collection** (`collection/`): Fetches data from Google Places, Trustpilot, FSA hygiene data, and scrapes restaurant websites.
*   **Processing** (`processing/`): ETL with fuzzy matching for linking restaurant records across data sources.
*   **Dashboard** (`dashboard/`): Streamlit app with multiple tabs for different analyses.
*   **Shared** (`shared/`): Configuration and data models.
*   **Database**: SQLite (`plymouth_research.db`)

## Building and Running

**1. Install Dependencies:**

```bash
pip install -r projects/001-plymouth-research-restaurant-menu-analytics/requirements.txt
```

**2. Run Data Collection and Processing (Optional):**

These scripts populate and process the data in the `plymouth_research.db` database.

```bash
python projects/001-plymouth-research-restaurant-menu-analytics/run_collection.py
python projects/001-plymouth-research-restaurant-menu-analytics/run_processing.py
```

**3. Run the Streamlit Dashboard:**

This command starts the interactive dashboard.

```bash
streamlit run projects/001-plymouth-research-restaurant-menu-analytics/dashboard_app.py
```

The dashboard will be available at `http://localhost:8501`.

## Development Conventions

*   The project is written in Python 3.8+.
*   It uses a SQLite database for data storage. The main database file is `plymouth_research.db`.
*   The dashboard is built with Streamlit. The main entry point is `dashboard_app.py`.
*   The project is structured into modules for data collection, processing, and dashboard presentation.
*   The `ArcKit` framework is used for enterprise architecture governance, with artifacts stored in the `projects/` directory.
