#!/usr/bin/env python3
"""
Plymouth Research Restaurant Menu Analytics Dashboard
=====================================================

Main entry point for the modular Streamlit dashboard.
Compatible with Streamlit Cloud deployment.

Usage:
    streamlit run dashboard/app.py
    # OR from project root:
    streamlit run streamlit_app.py

Author: Plymouth Research Team
Date: 2025-11-26
"""

import sys
from pathlib import Path

# ============================================================================
# Path Setup for Streamlit Cloud Compatibility
# ============================================================================
# Determine project root and add to path
_this_file = Path(__file__).resolve()
_dashboard_dir = _this_file.parent
_project_root = _dashboard_dir.parent

# Add project root to path for imports
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

# ============================================================================
# Imports
# ============================================================================
import streamlit as st
import pandas as pd
import sqlite3

# Import from our modules (now on path)
from dashboard.data_loader import (
    load_restaurants,
    load_menu_items,
    load_dietary_tags,
    load_trustpilot_reviews,
    load_google_reviews,
)
from dashboard.components.sidebar import render_sidebar, apply_filters
from dashboard.components.metrics import render_metrics_row, render_business_rates_summary
from dashboard.tabs.overview import render_overview_tab
from dashboard.tabs.menus import render_menus_tab
from dashboard.tabs.prices import render_prices_tab
from dashboard.tabs.hygiene import render_hygiene_tab
from dashboard.tabs.reviews import render_reviews_tab
from dashboard.tabs.map_tab import render_map_tab


# ============================================================================
# Database Path Resolution
# ============================================================================
def get_database_path() -> str:
    """
    Find the database file, checking multiple locations.

    Works for:
    - Local development (running from dashboard/ or project root)
    - Streamlit Cloud (running from repo root)
    """
    possible_paths = [
        _project_root / "plymouth_research.db",  # From dashboard/app.py
        Path.cwd() / "plymouth_research.db",     # Current directory
        Path("plymouth_research.db"),            # Relative
    ]

    for path in possible_paths:
        if path.exists():
            return str(path)

    # Return the expected path for error message
    return str(possible_paths[0])


# ============================================================================
# Page Configuration
# ============================================================================
st.set_page_config(
    page_title="Plymouth Restaurant Menu Analytics",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================================
# Main Application
# ============================================================================
def main():
    """Main dashboard application."""

    # Header
    st.title("🍽️ Plymouth Restaurant Menu Analytics")

    # Get database path
    db_path = get_database_path()

    # Check database exists
    if not Path(db_path).exists():
        st.error(f"❌ Database not found: {db_path}")
        st.info("The database file should be in the project root directory.")
        st.stop()

    # Load data with spinner
    with st.spinner("🔄 Loading restaurant data..."):
        try:
            restaurants_df = load_restaurants(db_path)
            menu_df = load_menu_items(db_path)
            dietary_df = load_dietary_tags(db_path)
            trustpilot_df = load_trustpilot_reviews(db_path)
            google_df = load_google_reviews(db_path)
        except Exception as e:
            st.error(f"❌ Failed to load data: {e}")
            st.exception(e)
            st.stop()

    # Dynamic subtitle
    st.markdown(f"**Discover and compare menus from {len(restaurants_df)} Plymouth restaurants**")

    # Render sidebar and get filters
    filters = render_sidebar(restaurants_df, menu_df, dietary_df)

    # Apply filters
    filtered_restaurants, filtered_menu = apply_filters(
        restaurants_df, menu_df, dietary_df, filters
    )

    # Key metrics row
    render_metrics_row(filtered_restaurants, filtered_menu)

    # Business rates summary (if applicable)
    render_business_rates_summary(filtered_restaurants)

    st.divider()

    # View mode handling
    if filters.get('view_mode') == "🗺️ Full-Screen Map":
        render_map_tab(filtered_restaurants, filters)
    else:
        # Tab-based analytics view
        tabs = st.tabs([
            "📊 Overview",
            "🍽️ Browse Menus",
            "💰 Price Analysis",
            "⭐ Hygiene Ratings",
            "📝 Reviews",
            "🗺️ Map",
            "ℹ️ About"
        ])

        with tabs[0]:
            render_overview_tab(filtered_restaurants, filtered_menu)

        with tabs[1]:
            render_menus_tab(filtered_restaurants, filtered_menu)

        with tabs[2]:
            render_prices_tab(filtered_restaurants, filtered_menu)

        with tabs[3]:
            render_hygiene_tab(filtered_restaurants)

        with tabs[4]:
            render_reviews_tab(filtered_restaurants, trustpilot_df, google_df)

        with tabs[5]:
            render_map_tab(filtered_restaurants, filters)

        with tabs[6]:
            render_about_tab()


def render_about_tab():
    """Render the about tab."""
    st.header("ℹ️ About")

    st.markdown("""
    ## Plymouth Research Restaurant Menu Analytics

    This dashboard provides comprehensive analytics for Plymouth restaurants, including:

    - **Menu Data**: 2,600+ menu items from 98 restaurants
    - **Hygiene Ratings**: FSA Food Hygiene Rating Scheme data
    - **Customer Reviews**: Trustpilot and Google reviews
    - **Business Data**: Licensing, business rates, and Companies House data

    ### Data Sources

    | Source | Description | Update Frequency |
    |--------|-------------|------------------|
    | Restaurant Menus | Web scraped menu data | Manual refresh |
    | FSA Hygiene | Food Standards Agency ratings | Weekly |
    | Trustpilot | Customer reviews | Manual refresh |
    | Google Places | Reviews, service options, contact info | Manual refresh |
    | Business Rates | Plymouth Council rates register | Annual |
    | Licensing | Plymouth licensing authority | Manual refresh |

    ### Technology Stack

    - **Frontend**: Streamlit
    - **Data**: SQLite, Pandas
    - **Visualization**: Plotly, Pydeck
    - **Architecture**: Modular (collection → processing → dashboard)

    ### Legal & Ethical Notes

    - Web scraping respects robots.txt and rate limits (5s per domain)
    - FSA data licensed under Open Government Licence v3.0
    - Review data used for analytics only (not republication)
    - GDPR compliant - only public business data collected

    ---

    *Dashboard Version: 2.0.0 (Modular Architecture)*
    *Last Updated: 2025-11-26*
    """)


# ============================================================================
# Entry Point
# ============================================================================
if __name__ == "__main__":
    main()
