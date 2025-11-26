"""
Data Loader Module
==================

Cached data loading functions for the Streamlit dashboard.

Uses st.cache_data for efficient caching with configurable TTL.

Author: Plymouth Research Team
Date: 2025-11-26
"""

import sqlite3
from pathlib import Path
from typing import Optional

import streamlit as st
import pandas as pd


class DataLoader:
    """
    Data loader with Streamlit caching.

    All load methods are cached with 1-hour TTL for performance.
    """

    def __init__(self, db_path: Optional[Path] = None):
        """
        Initialize data loader.

        Args:
            db_path: Path to SQLite database. If None, uses default.
        """
        if db_path is None:
            from shared.config import get_db_path
            db_path = get_db_path()

        self.db_path = db_path

    @st.cache_resource
    def get_connection(_self):
        """Get cached database connection."""
        if not _self.db_path.exists():
            st.error(f"❌ Database not found: {_self.db_path}")
            st.stop()
        return sqlite3.connect(str(_self.db_path), check_same_thread=False)


@st.cache_data(ttl=3600)
def load_restaurants(_db_path: str) -> pd.DataFrame:
    """
    Load all restaurants from database.

    Args:
        _db_path: Database path (underscore prefix for cache)

    Returns:
        DataFrame with restaurant data
    """
    conn = sqlite3.connect(_db_path, check_same_thread=False)

    query = """
        SELECT
            restaurant_id,
            name,
            cuisine_type,
            price_range,
            address,
            website_url,
            scraped_at,
            last_updated,
            data_source,
            scraping_method,
            hygiene_rating,
            hygiene_rating_date,
            fsa_id,
            hygiene_score_hygiene,
            hygiene_score_structural,
            hygiene_score_confidence,
            fsa_business_type,
            fsa_business_name,
            fsa_address_line1,
            fsa_address_line2,
            fsa_address_line3,
            fsa_address_line4,
            fsa_postcode,
            fsa_latitude,
            fsa_longitude,
            trustpilot_review_count,
            trustpilot_avg_rating,
            google_review_count,
            google_avg_rating,
            google_place_id,
            google_dine_in,
            google_takeout,
            google_delivery,
            google_reservable,
            google_serves_breakfast,
            google_serves_lunch,
            google_serves_dinner,
            google_serves_beer,
            google_serves_wine,
            google_serves_vegetarian,
            google_phone_national,
            google_website_url,
            google_formatted_address,
            google_latitude,
            google_longitude,
            google_maps_url,
            google_business_status,
            company_number,
            company_name,
            company_status,
            licensing_premises_id,
            licensing_activities,
            licensing_opening_hours,
            business_rates_rateable_value,
            business_rates_net_charge,
            business_rates_category
        FROM restaurants
        WHERE is_active = 1
        ORDER BY name
    """

    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


@st.cache_data(ttl=3600)
def load_menu_items(_db_path: str) -> pd.DataFrame:
    """Load all menu items with restaurant info."""
    conn = sqlite3.connect(_db_path, check_same_thread=False)

    query = """
        SELECT
            mi.item_id,
            mi.restaurant_id,
            r.name as restaurant_name,
            r.cuisine_type,
            r.price_range as restaurant_price_range,
            mi.name as item_name,
            mi.description,
            mi.price_gbp,
            mi.category,
            mi.scraped_at
        FROM menu_items mi
        JOIN restaurants r ON mi.restaurant_id = r.restaurant_id
        WHERE r.is_active = 1
        ORDER BY r.name, mi.category, mi.name
    """

    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


@st.cache_data(ttl=3600)
def load_dietary_tags(_db_path: str) -> pd.DataFrame:
    """Load menu items with dietary tags."""
    conn = sqlite3.connect(_db_path, check_same_thread=False)

    query = """
        SELECT
            mi.item_id,
            mi.name as item_name,
            r.name as restaurant_name,
            dt.tag_name
        FROM menu_items mi
        JOIN restaurants r ON mi.restaurant_id = r.restaurant_id
        JOIN menu_item_dietary_tags midt ON mi.item_id = midt.item_id
        JOIN dietary_tags dt ON midt.tag_id = dt.tag_id
        WHERE r.is_active = 1
    """

    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


@st.cache_data(ttl=3600)
def load_trustpilot_reviews(_db_path: str) -> pd.DataFrame:
    """Load all Trustpilot reviews with restaurant info."""
    conn = sqlite3.connect(_db_path, check_same_thread=False)

    query = """
        SELECT
            tr.review_id,
            tr.restaurant_id,
            r.name as restaurant_name,
            r.trustpilot_url,
            tr.review_date,
            tr.author_name,
            tr.review_title,
            tr.review_body,
            tr.rating,
            tr.author_location,
            tr.author_review_count,
            tr.is_verified_purchase,
            tr.helpful_count,
            r.hygiene_rating,
            r.cuisine_type,
            r.price_range
        FROM trustpilot_reviews tr
        JOIN restaurants r ON tr.restaurant_id = r.restaurant_id
        WHERE r.is_active = 1
        ORDER BY tr.review_date DESC
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    if not df.empty:
        df['review_date'] = pd.to_datetime(df['review_date'])

    return df


@st.cache_data(ttl=3600)
def load_google_reviews(_db_path: str) -> pd.DataFrame:
    """Load all Google reviews with restaurant info."""
    conn = sqlite3.connect(_db_path, check_same_thread=False)

    query = """
        SELECT
            gr.review_id,
            gr.restaurant_id,
            r.name as restaurant_name,
            gr.review_date,
            gr.author_name,
            gr.review_text,
            gr.rating,
            gr.google_author_url,
            gr.google_profile_photo_url,
            gr.language,
            gr.relative_time_description,
            r.hygiene_rating,
            r.cuisine_type,
            r.price_range
        FROM google_reviews gr
        JOIN restaurants r ON gr.restaurant_id = r.restaurant_id
        WHERE r.is_active = 1
        ORDER BY gr.review_date DESC
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    if not df.empty:
        df['review_date'] = pd.to_datetime(df['review_date'])

    return df


@st.cache_data(ttl=3600)
def load_directors(_db_path: str) -> pd.DataFrame:
    """Load all active directors from Companies House."""
    conn = sqlite3.connect(_db_path, check_same_thread=False)

    query = """
        SELECT
            director_id,
            restaurant_id,
            company_number,
            director_name,
            officer_role,
            appointed_date,
            nationality,
            occupation
        FROM company_directors
        WHERE resigned_date IS NULL OR resigned_date = ''
        ORDER BY restaurant_id, appointed_date
    """

    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


# Convenience function for loading all data
def load_all_data(db_path: str) -> dict:
    """
    Load all dashboard data at once.

    Args:
        db_path: Path to database file

    Returns:
        Dictionary with all DataFrames
    """
    return {
        'restaurants': load_restaurants(db_path),
        'menu_items': load_menu_items(db_path),
        'dietary_tags': load_dietary_tags(db_path),
        'trustpilot_reviews': load_trustpilot_reviews(db_path),
        'google_reviews': load_google_reviews(db_path),
        'directors': load_directors(db_path),
    }
