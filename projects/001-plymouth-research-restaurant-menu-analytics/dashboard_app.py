#!/usr/bin/env python3
"""
Plymouth Research Restaurant Menu Analytics Dashboard
=====================================================

Interactive Streamlit dashboard for exploring Plymouth restaurant menus.

Features:
- Search by cuisine, price range, dietary requirements
- Restaurant comparison
- Price analytics
- Menu item filtering

Author: Plymouth Research Team
Date: 2025-11-17
Sprint: Sprint 3 - Dashboard
"""

import sys
import sqlite3
from pathlib import Path
from typing import List, Dict, Tuple

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pydeck as pdk

# Page configuration
st.set_page_config(
    page_title="Plymouth Restaurant Menu Analytics",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))


# ============================================================================
# Database Functions
# ============================================================================

@st.cache_resource
def get_database_connection():
    """Get cached database connection."""
    db_path = Path(__file__).parent / "plymouth_research.db"
    if not db_path.exists():
        st.error(f"❌ Database not found: {db_path}")
        st.info("💡 Run `python batch_scrape_restaurants.py` to populate the database first.")
        st.stop()
    return sqlite3.connect(str(db_path), check_same_thread=False)


@st.cache_data(ttl=3600)  # 1 hour cache
def load_restaurants() -> pd.DataFrame:
    """Load all restaurants from database."""
    conn = get_database_connection()
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
            fsa_local_authority_business_id,
            fsa_rating_key,
            fsa_scheme_type,
            fsa_local_authority_website,
            fsa_new_rating_pending,
            trustpilot_review_count,
            trustpilot_avg_rating,
            google_review_count,
            google_avg_rating,
            company_number,
            company_name,
            company_status,
            company_type,
            incorporation_date,
            company_registered_address,
            company_sic_codes,
            fixed_assets_gbp,
            current_assets_gbp,
            net_current_assets_gbp,
            total_assets_gbp,
            net_assets_gbp,
            shareholders_equity_gbp,
            turnover_gbp,
            gross_profit_gbp,
            operating_profit_gbp,
            profit_loss_gbp,
            employees,
            accounts_period_end,
            financial_data_fetched_at,
            fixed_assets_gbp_prior,
            current_assets_gbp_prior,
            net_current_assets_gbp_prior,
            total_assets_gbp_prior,
            net_assets_gbp_prior,
            shareholders_equity_gbp_prior,
            turnover_gbp_prior,
            gross_profit_gbp_prior,
            operating_profit_gbp_prior,
            profit_loss_gbp_prior,
            employees_prior,
            net_assets_change_gbp,
            net_assets_change_pct,
            employee_change,
            financial_health_score,
            financial_rating,
            rating_description,
            licensing_premises_id,
            licensing_premises_name,
            licensing_premises_address,
            licensing_number,
            licensing_url,
            licensing_activities,
            licensing_opening_hours,
            licensing_scraped_at,
            licensing_match_confidence,
            business_rates_propref,
            business_rates_account_holder,
            business_rates_address,
            business_rates_postcode,
            business_rates_rateable_value,
            business_rates_net_charge,
            business_rates_category,
            business_rates_vo_description,
            business_rates_match_score,
            business_rates_match_reason,
            business_rates_matched_at
        FROM restaurants
        WHERE is_active = 1
        ORDER BY name
    """
    df = pd.read_sql_query(query, conn)
    return df


@st.cache_data(ttl=3600)  # 1 hour cache
def load_trustpilot_reviews() -> pd.DataFrame:
    """Load all Trustpilot reviews with restaurant info."""
    conn = get_database_connection()
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
    if not df.empty:
        df['review_date'] = pd.to_datetime(df['review_date'])
    return df


@st.cache_data(ttl=3600)  # 1 hour cache
def load_trustpilot_summary() -> pd.DataFrame:
    """Load Trustpilot summary stats per restaurant."""
    conn = get_database_connection()
    query = """
        SELECT * FROM restaurant_trustpilot_summary
        ORDER BY calculated_avg_rating DESC, actual_review_count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df


@st.cache_data(ttl=3600)  # 1 hour cache
def load_google_reviews() -> pd.DataFrame:
    """Load all Google reviews with restaurant info."""
    conn = get_database_connection()
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
    if not df.empty:
        df['review_date'] = pd.to_datetime(df['review_date'])
    return df


@st.cache_data(ttl=3600)  # 1 hour cache
def load_google_summary() -> pd.DataFrame:
    """Load Google summary stats per restaurant."""
    conn = get_database_connection()
    query = """
        SELECT * FROM restaurant_google_summary
        ORDER BY calculated_avg_rating DESC, actual_review_count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df


@st.cache_data(ttl=3600)  # 1 hour cache
def load_menu_items() -> pd.DataFrame:
    """Load all menu items with restaurant info."""
    conn = get_database_connection()
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
    return df


@st.cache_data(ttl=3600)  # 1 hour cache
def load_dietary_tags() -> pd.DataFrame:
    """Load menu items with dietary tags."""
    conn = get_database_connection()
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
    return df

@st.cache_data(ttl=3600)  # 1 hour cache
def load_directors() -> pd.DataFrame:
    """Load all active directors from Companies House."""
    conn = get_database_connection()
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
    return df


# ============================================================================
# Helper Functions
# ============================================================================

def format_hygiene_rating(rating: float, include_text: bool = False) -> str:
    """
    Format hygiene rating with stars and color.

    Args:
        rating: Hygiene rating (0-5)
        include_text: Whether to include descriptive text

    Returns:
        HTML formatted rating string
    """
    if pd.isna(rating):
        return "Not rated"

    rating = int(rating)
    stars = "⭐" * rating if rating > 0 else "❌"

    # Color coding
    if rating >= 5:
        color = "#4CAF50"  # Green
        text = "Very Good"
    elif rating >= 4:
        color = "#8BC34A"  # Light Green
        text = "Good"
    elif rating >= 3:
        color = "#FFC107"  # Yellow
        text = "Satisfactory"
    elif rating >= 2:
        color = "#FF9800"  # Orange
        text = "Improvement Necessary"
    elif rating >= 1:
        color = "#FF5722"  # Deep Orange
        text = "Major Improvement"
    else:
        color = "#F44336"  # Red
        text = "Urgent Improvement"

    if include_text:
        return f'<span style="color: {color}; font-weight: bold;">{stars} {text}</span>'
    else:
        return f'<span style="color: {color};">{stars}</span>'


def get_hygiene_badge(rating: float) -> str:
    """Get colored badge for hygiene rating."""
    if pd.isna(rating):
        return '<span style="background: #9E9E9E; color: white; padding: 2px 8px; border-radius: 3px; font-size: 0.85em;">No Rating</span>'

    rating = int(rating)

    if rating >= 5:
        bg_color = "#4CAF50"
        label = f"5★ Very Good"
    elif rating >= 4:
        bg_color = "#8BC34A"
        label = f"4★ Good"
    elif rating >= 3:
        bg_color = "#FFC107"
        label = f"3★ Satisfactory"
    elif rating >= 2:
        bg_color = "#FF9800"
        label = f"2★ Improvement Needed"
    elif rating >= 1:
        bg_color = "#FF5722"
        label = f"1★ Major Improvement"
    else:
        bg_color = "#F44336"
        label = f"0★ Urgent Action"

    return f'<span style="background: {bg_color}; color: white; padding: 2px 8px; border-radius: 3px; font-size: 0.85em;">{label}</span>'


def format_trustpilot_rating(rating: float, include_text: bool = False) -> str:
    """
    Format Trustpilot rating with stars and color.

    Args:
        rating: Trustpilot rating (1-5)
        include_text: Whether to include descriptive text

    Returns:
        HTML formatted rating string
    """
    if pd.isna(rating):
        return "No reviews"

    rating_int = int(rating)
    stars = "⭐" * rating_int

    # Color coding (green for good, red for bad)
    if rating >= 4.5:
        color = "#4CAF50"  # Green
        text = "Excellent"
    elif rating >= 3.5:
        color = "#8BC34A"  # Light Green
        text = "Good"
    elif rating >= 2.5:
        color = "#FFC107"  # Yellow
        text = "Average"
    elif rating >= 1.5:
        color = "#FF9800"  # Orange
        text = "Below Average"
    else:
        color = "#F44336"  # Red
        text = "Poor"

    if include_text:
        return f'<span style="color: {color}; font-weight: bold;">{stars} {rating:.1f}/5 ({text})</span>'
    else:
        return f'<span style="color: {color};">{stars} {rating:.1f}/5</span>'


def format_google_rating(rating: float, include_text: bool = False) -> str:
    """
    Format Google rating with stars and color.

    Args:
        rating: Google rating (1-5)
        include_text: Whether to include descriptive text

    Returns:
        HTML formatted rating string
    """
    if pd.isna(rating):
        return "No reviews"

    rating_int = int(rating)
    stars = "⭐" * rating_int

    # Color coding (green for good, red for bad) - Google style
    if rating >= 4.5:
        color = "#0F9D58"  # Google Green
        text = "Excellent"
    elif rating >= 3.5:
        color = "#4CAF50"  # Green
        text = "Good"
    elif rating >= 2.5:
        color = "#FFC107"  # Yellow
        text = "Average"
    elif rating >= 1.5:
        color = "#FF9800"  # Orange
        text = "Below Average"
    else:
        color = "#F44336"  # Red
        text = "Poor"

    if include_text:
        return f'<span style="color: {color}; font-weight: bold;">{stars} {rating:.1f}/5 ({text})</span>'
    else:
        return f'<span style="color: {color};">{stars} {rating:.1f}/5</span>'


def get_trustpilot_badge(rating: float, review_count: int = None) -> str:
    """Get colored badge for Trustpilot rating."""
    if pd.isna(rating):
        return '<span style="background: #9E9E9E; color: white; padding: 2px 8px; border-radius: 3px; font-size: 0.85em;">No Reviews</span>'

    if rating >= 4.5:
        bg_color = "#00B67A"  # Trustpilot green
        label = "Excellent"
    elif rating >= 3.5:
        bg_color = "#73CF11"  # Light green
        label = "Great"
    elif rating >= 2.5:
        bg_color = "#FFCE00"  # Yellow
        label = "Average"
    elif rating >= 1.5:
        bg_color = "#FF8622"  # Orange
        label = "Poor"
    else:
        bg_color = "#FF3722"  # Red
        label = "Bad"

    stars = "⭐" * int(rating)
    review_text = f" ({review_count} reviews)" if review_count else ""

    return f'<span style="background: {bg_color}; color: white; padding: 2px 8px; border-radius: 3px; font-size: 0.85em;">{stars} {rating:.1f}/5 {label}{review_text}</span>'


def get_licensing_badge(has_licensing: bool) -> str:
    """Get colored badge for licensing status."""
    if has_licensing:
        return '<span style="background: #4CAF50; color: white; padding: 2px 8px; border-radius: 3px; font-size: 0.85em;">✓ Licensed</span>'
    else:
        return '<span style="background: #9E9E9E; color: white; padding: 2px 8px; border-radius: 3px; font-size: 0.85em;">No License Data</span>'


def format_opening_hours(hours_json: str) -> str:
    """Format opening hours from JSON."""
    if not hours_json or hours_json == '[]':
        return "Not available"

    try:
        import json
        hours = json.loads(hours_json)
        if not hours:
            return "Not available"

        formatted = []
        for period in hours:
            days = period.get('days', '')
            time_from = period.get('time_from', '')
            time_to = period.get('time_to', '')

            if days and time_from and time_to:
                formatted.append(f"**{days}**: {time_from} - {time_to}")

        return "<br>".join(formatted) if formatted else "Not available"
    except:
        return "Error parsing hours"


def format_licensing_activities(activities_json: str) -> str:
    """Format licensing activities from JSON."""
    if not activities_json or activities_json == '[]':
        return "Not specified"

    try:
        import json
        activities = json.loads(activities_json)
        if not activities:
            return "Not specified"

        # Clean up empty strings
        activities = [a.strip() for a in activities if a and a.strip()]

        if not activities:
            return "Not specified"

        # Capitalize first letter
        activities = [a[0].upper() + a[1:] if a else a for a in activities]

        return "<br>• " + "<br>• ".join(activities)
    except:
        return "Error parsing activities"


def filter_menu_items(
    menu_df: pd.DataFrame,
    dietary_tags_df: pd.DataFrame,
    restaurants: List[str] = None,
    cuisines: List[str] = None,
    min_price: float = None,
    max_price: float = None,
    categories: List[str] = None,
    dietary_filters: List[str] = None
) -> pd.DataFrame:
    """Filter menu items based on user criteria."""
    filtered = menu_df.copy()

    # Filter by restaurant
    if restaurants:
        filtered = filtered[filtered['restaurant_name'].isin(restaurants)]

    # Filter by cuisine
    if cuisines:
        filtered = filtered[filtered['cuisine_type'].isin(cuisines)]

    # Filter by price
    if min_price is not None:
        filtered = filtered[filtered['price_gbp'] >= min_price]
    if max_price is not None:
        filtered = filtered[filtered['price_gbp'] <= max_price]

    # Filter by category
    if categories:
        filtered = filtered[filtered['category'].isin(categories)]

    # Filter by dietary tags
    if dietary_filters:
        # Get item IDs that have ALL selected dietary tags
        item_ids_with_tags = dietary_tags_df[dietary_tags_df['tag_name'].isin(dietary_filters)]
        item_ids = item_ids_with_tags.groupby('item_id').size()
        item_ids = item_ids[item_ids == len(dietary_filters)].index.tolist()
        filtered = filtered[filtered['item_id'].isin(item_ids)]

    return filtered


# ============================================================================
# Dashboard UI
# ============================================================================

def main():
    """Main dashboard application."""

    # Header
    st.title("🍽️ Plymouth Restaurant Menu Analytics")

    # Load data with spinner
    with st.spinner("🔄 Loading restaurant data and caching for fast performance..."):
        try:
            restaurants_df = load_restaurants()
            menu_df = load_menu_items()
            dietary_df = load_dietary_tags()
        except Exception as e:
            st.error(f"❌ Failed to load data: {e}")
            st.stop()

    # Dynamic subtitle with restaurant count
    restaurant_count = len(restaurants_df)
    st.markdown(f"**Discover and compare menus from {restaurant_count} Plymouth restaurants**")

    # Sidebar - Filters
    st.sidebar.header("🔍 Search & Filter")

    # Restaurant filter
    all_restaurants = sorted(restaurants_df['name'].unique().tolist())
    selected_restaurants = st.sidebar.multiselect(
        "Restaurants",
        options=all_restaurants,
        default=all_restaurants,
        help="Select one or more restaurants"
    )

    # Cuisine filter
    all_cuisines = sorted(menu_df['cuisine_type'].dropna().unique().tolist())
    selected_cuisines = st.sidebar.multiselect(
        "Cuisine Type",
        options=all_cuisines,
        default=all_cuisines,
        help="Filter by cuisine type"
    )

    # Price filter
    st.sidebar.subheader("💰 Price Range")
    if not menu_df['price_gbp'].isna().all():
        min_price_db = float(menu_df['price_gbp'].min())
        max_price_db = float(menu_df['price_gbp'].max())

        price_range = st.sidebar.slider(
            "Price (£)",
            min_value=0.0,
            max_value=max_price_db + 5.0,
            value=(min_price_db, max_price_db),
            step=0.50,
            help="Filter menu items by price"
        )
    else:
        price_range = (0.0, 100.0)

    # Category filter
    all_categories = sorted(menu_df['category'].dropna().unique().tolist())
    selected_categories = st.sidebar.multiselect(
        "Categories",
        options=all_categories,
        default=all_categories,
        help="Filter by menu category (Starters, Mains, etc.)"
    )

    # Dietary filter
    all_dietary_tags = sorted(dietary_df['tag_name'].unique().tolist())
    selected_dietary = st.sidebar.multiselect(
        "🥗 Dietary Requirements",
        options=all_dietary_tags,
        help="Items must have ALL selected tags"
    )

    # Hygiene rating filter
    st.sidebar.subheader("⭐ Food Hygiene Rating")
    min_hygiene_rating = st.sidebar.select_slider(
        "Minimum Rating",
        options=[0, 1, 2, 3, 4, 5],
        value=0,
        format_func=lambda x: f"{x}★" if x > 0 else "Any",
        help="Filter restaurants by minimum FSA hygiene rating"
    )

    st.sidebar.caption("🏛️ Source: [Food Standards Agency](https://www.food.gov.uk/safety-hygiene/food-hygiene-rating-scheme)")

    # Google service options filters
    st.sidebar.subheader("🍽️ Service Options")
    service_filters = st.sidebar.multiselect(
        "Select Services",
        options=["Dine-in", "Takeout", "Delivery", "Reservations"],
        help="Filter restaurants by available services"
    )

    # Meal time filters
    st.sidebar.subheader("🍳 Meal Times")
    meal_filters = st.sidebar.multiselect(
        "Select Meal Times",
        options=["Breakfast", "Lunch", "Dinner"],
        help="Filter restaurants by meal service times"
    )

    # Dietary/beverage filters (Google-sourced)
    st.sidebar.subheader("🍷 Food & Beverages")
    fb_filters = st.sidebar.multiselect(
        "Select Options",
        options=["Vegetarian Food", "Beer", "Wine"],
        help="Filter restaurants by food and beverage options"
    )

    # Business status filter
    hide_closed = st.sidebar.checkbox(
        "Hide Closed Restaurants",
        value=True,
        help="Hide permanently and temporarily closed restaurants"
    )

    st.sidebar.caption("🌐 Service data from Google Places API")

    # Business rates filter
    st.sidebar.subheader("💷 Business Rates")
    show_only_with_rates = st.sidebar.checkbox(
        "Show Only Restaurants with Business Rates Data",
        value=False,
        help="Filter to show only the 41 restaurants with business rates information"
    )

    st.sidebar.caption("💷 Rates data from Plymouth Business Rates Register (Nov 2025) - 41 matched")

    # Apply filters
    filtered_menu = filter_menu_items(
        menu_df,
        dietary_df,
        restaurants=selected_restaurants if selected_restaurants else None,
        cuisines=selected_cuisines if selected_cuisines else None,
        min_price=price_range[0],
        max_price=price_range[1],
        categories=selected_categories if selected_categories else None,
        dietary_filters=selected_dietary if selected_dietary else None
    )

    # Apply hygiene rating filter to restaurants
    filtered_restaurants = restaurants_df.copy()
    if min_hygiene_rating > 0:
        # Filter out restaurants below minimum rating (include NaN as they may not have ratings yet)
        filtered_restaurants = filtered_restaurants[
            (filtered_restaurants['hygiene_rating'] >= min_hygiene_rating) |
            (filtered_restaurants['hygiene_rating'].isna())
        ]
        # Also filter menu items to only show items from qualifying restaurants
        filtered_menu = filtered_menu[filtered_menu['restaurant_name'].isin(filtered_restaurants['name'])]

    # Apply Google service options filters
    if service_filters:
        for service in service_filters:
            if service == "Dine-in" and 'google_dine_in' in filtered_restaurants.columns:
                filtered_restaurants = filtered_restaurants[filtered_restaurants['google_dine_in'] == 1]
            elif service == "Takeout" and 'google_takeout' in filtered_restaurants.columns:
                filtered_restaurants = filtered_restaurants[filtered_restaurants['google_takeout'] == 1]
            elif service == "Delivery" and 'google_delivery' in filtered_restaurants.columns:
                filtered_restaurants = filtered_restaurants[filtered_restaurants['google_delivery'] == 1]
            elif service == "Reservations" and 'google_reservable' in filtered_restaurants.columns:
                filtered_restaurants = filtered_restaurants[filtered_restaurants['google_reservable'] == 1]
        # Update menu items to match filtered restaurants
        filtered_menu = filtered_menu[filtered_menu['restaurant_name'].isin(filtered_restaurants['name'])]

    # Apply meal time filters
    if meal_filters:
        for meal in meal_filters:
            if meal == "Breakfast" and 'google_serves_breakfast' in filtered_restaurants.columns:
                filtered_restaurants = filtered_restaurants[filtered_restaurants['google_serves_breakfast'] == 1]
            elif meal == "Lunch" and 'google_serves_lunch' in filtered_restaurants.columns:
                filtered_restaurants = filtered_restaurants[filtered_restaurants['google_serves_lunch'] == 1]
            elif meal == "Dinner" and 'google_serves_dinner' in filtered_restaurants.columns:
                filtered_restaurants = filtered_restaurants[filtered_restaurants['google_serves_dinner'] == 1]
        # Update menu items to match filtered restaurants
        filtered_menu = filtered_menu[filtered_menu['restaurant_name'].isin(filtered_restaurants['name'])]

    # Apply food & beverage filters
    if fb_filters:
        for fb in fb_filters:
            if fb == "Vegetarian Food" and 'google_serves_vegetarian' in filtered_restaurants.columns:
                filtered_restaurants = filtered_restaurants[filtered_restaurants['google_serves_vegetarian'] == 1]
            elif fb == "Beer" and 'google_serves_beer' in filtered_restaurants.columns:
                filtered_restaurants = filtered_restaurants[filtered_restaurants['google_serves_beer'] == 1]
            elif fb == "Wine" and 'google_serves_wine' in filtered_restaurants.columns:
                filtered_restaurants = filtered_restaurants[filtered_restaurants['google_serves_wine'] == 1]
        # Update menu items to match filtered restaurants
        filtered_menu = filtered_menu[filtered_menu['restaurant_name'].isin(filtered_restaurants['name'])]

    # Apply business status filter
    if hide_closed and 'google_business_status' in filtered_restaurants.columns:
        filtered_restaurants = filtered_restaurants[
            (filtered_restaurants['google_business_status'] == 'OPERATIONAL') |
            (filtered_restaurants['google_business_status'].isna())
        ]
        # Update menu items to match filtered restaurants
        filtered_menu = filtered_menu[filtered_menu['restaurant_name'].isin(filtered_restaurants['name'])]

    # Apply business rates filter
    if show_only_with_rates and 'business_rates_rateable_value' in filtered_restaurants.columns:
        filtered_restaurants = filtered_restaurants[
            filtered_restaurants['business_rates_rateable_value'].notna()
        ]
        # Update menu items to match filtered restaurants
        filtered_menu = filtered_menu[filtered_menu['restaurant_name'].isin(filtered_restaurants['name'])]

    # ========================================================================
    # Key Metrics
    # ========================================================================
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.metric("🍽️ Restaurants", len(filtered_restaurants))

    with col2:
        real_count = (filtered_restaurants['data_source'] == 'real_scraped').sum()
        st.metric("✓ Real Data", real_count, help="Restaurants with actual scraped menus")

    with col3:
        st.metric("📋 Menu Items", len(filtered_menu))

    with col4:
        if not filtered_menu['price_gbp'].isna().all():
            avg_price = filtered_menu['price_gbp'].mean()
            st.metric("💰 Avg Price", f"£{avg_price:.2f}")
        else:
            st.metric("💰 Avg Price", "N/A")

    with col5:
        unique_categories = filtered_menu['category'].nunique()
        st.metric("🏷️ Categories", unique_categories)

    with col6:
        # Average hygiene rating for filtered restaurants
        rated_restos = filtered_restaurants[filtered_restaurants['hygiene_rating'].notna()]
        if len(rated_restos) > 0:
            avg_rating = rated_restos['hygiene_rating'].mean()
            st.metric("⭐ Avg Hygiene", f"{avg_rating:.1f}/5", help=f"{len(rated_restos)} of {len(filtered_restaurants)} restaurants rated")
        else:
            st.metric("⭐ Avg Hygiene", "N/A", help="No hygiene ratings available")

    # Business rates summary row
    if 'business_rates_rateable_value' in filtered_restaurants.columns:
        rates_restos = filtered_restaurants[filtered_restaurants['business_rates_rateable_value'].notna()]
        if len(rates_restos) > 0:
            st.markdown("##### 💷 Business Rates Summary")
            rates_col1, rates_col2, rates_col3, rates_col4 = st.columns(4)

            with rates_col1:
                st.metric(
                    "📊 With Rates Data",
                    f"{len(rates_restos)}/{len(filtered_restaurants)}",
                    help="Restaurants with business rates information"
                )

            with rates_col2:
                avg_rv = rates_restos['business_rates_rateable_value'].mean()
                st.metric(
                    "💷 Avg Rateable Value",
                    f"£{int(avg_rv):,}",
                    help="Average property valuation"
                )

            with rates_col3:
                if 'business_rates_net_charge' in rates_restos.columns:
                    avg_charge = rates_restos['business_rates_net_charge'].mean()
                    st.metric(
                        "💰 Avg Annual Rates",
                        f"£{int(avg_charge):,}",
                        help="Average annual business rates (2025-26)"
                    )

            with rates_col4:
                max_rv = rates_restos['business_rates_rateable_value'].max()
                max_resto = rates_restos.loc[rates_restos['business_rates_rateable_value'] == max_rv, 'name'].iloc[0]
                st.metric(
                    "🏆 Highest RV",
                    f"£{int(max_rv):,}",
                    help=f"{max_resto}"
                )

    st.divider()

    # ========================================================================
    # Tabs
    # ========================================================================
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
        "🗺️ Map View",
        "🍽️ Browse Menus",
        "📊 Price Analytics",
        "🏪 Restaurant Comparison",
        "🎯 Competitor Analysis",
        "🍹 Drinks Analysis",
        "⭐ Hygiene Ratings",
        "🏢 Restaurant Profiles",
        "💬 Reviews",
        "📈 Statistics"
    ])

    # ------------------------------------------------------------------------
    # Tab 2: Browse Menus
    # ------------------------------------------------------------------------
    with tab2:
        st.header("Browse Menu Items")

        if filtered_menu.empty:
            st.warning("⚠️ No menu items match your filters. Try adjusting the criteria.")
        else:
            # Group by restaurant
            for restaurant in filtered_menu['restaurant_name'].unique():
                restaurant_items = filtered_menu[filtered_menu['restaurant_name'] == restaurant]

                with st.expander(f"**{restaurant}** ({len(restaurant_items)} items)", expanded=False):
                    # Restaurant info
                    restaurant_info = restaurants_df[restaurants_df['name'] == restaurant].iloc[0]

                    # Data source badge
                    data_source = restaurant_info.get('data_source', 'synthetic')
                    if data_source == 'real_scraped':
                        badge_color = "#4CAF50"  # Green
                        badge_text = "✓ REAL DATA"
                        badge_title = f"Scraped Method: {restaurant_info.get('scraping_method', 'unknown')}"
                    else:
                        badge_color = "#FF9800"  # Orange
                        badge_text = "⚠ SYNTHETIC DATA"
                        badge_title = "This is test/demonstration data, not real menu information"

                    # Display data source and hygiene rating badges
                    badge_html = f"<span style='background: {badge_color}; color: white; padding: 3px 10px; border-radius: 3px; font-size: 0.85em; font-weight: bold;' title='{badge_title}'>{badge_text}</span>"

                    # Add hygiene rating badge
                    hygiene_rating = restaurant_info.get('hygiene_rating')
                    if pd.notna(hygiene_rating):
                        hygiene_badge = get_hygiene_badge(hygiene_rating)
                        badge_html += " " + hygiene_badge

                        # Add inspection date
                        hygiene_date = restaurant_info.get('hygiene_rating_date')
                        if pd.notna(hygiene_date):
                            date_str = str(hygiene_date)[:10]
                            badge_html += f" <small style='color: #666;'>(Inspected: {date_str})</small>"

                    # Add licensing badge
                    licensing_number = restaurant_info.get('licensing_number')
                    if pd.notna(licensing_number):
                        licensing_badge = get_licensing_badge(True)
                        badge_html += " " + licensing_badge

                        # Add license number with link
                        licensing_url = restaurant_info.get('licensing_url')
                        if pd.notna(licensing_url):
                            match_confidence = restaurant_info.get('licensing_match_confidence', 0) * 100
                            badge_html += f" <small style='color: #666;'>(<a href='{licensing_url}' target='_blank'>{licensing_number}</a>, {match_confidence:.0f}% match)</small>"

                    st.markdown(badge_html, unsafe_allow_html=True)
                    st.markdown("")  # Spacer

                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.markdown(f"**Cuisine:** {restaurant_info['cuisine_type']}")
                    with col_b:
                        st.markdown(f"**Price Range:** {restaurant_info['price_range']}")
                    with col_c:
                        # Parse timestamp and format nicely
                        import datetime
                        try:
                            scraped_date = datetime.datetime.fromisoformat(restaurant_info['scraped_at']).strftime('%Y-%m-%d')
                            st.markdown(f"**Scraped:** {scraped_date}")
                        except:
                            st.markdown(f"**Scraped:** {restaurant_info['scraped_at'][:10]}")

                    # Service icons/badges
                    service_badges = []
                    if restaurant_info.get('google_dine_in') == 1:
                        service_badges.append("🍽️ Dine-in")
                    if restaurant_info.get('google_takeout') == 1:
                        service_badges.append("🥡 Takeout")
                    if restaurant_info.get('google_delivery') == 1:
                        service_badges.append("🚚 Delivery")
                    if restaurant_info.get('google_reservable') == 1:
                        service_badges.append("📅 Reservations")
                    if restaurant_info.get('google_serves_breakfast') == 1:
                        service_badges.append("🍳 Breakfast")
                    if restaurant_info.get('google_serves_lunch') == 1:
                        service_badges.append("🍴 Lunch")
                    if restaurant_info.get('google_serves_dinner') == 1:
                        service_badges.append("🍷 Dinner")
                    if restaurant_info.get('google_serves_vegetarian') == 1:
                        service_badges.append("🥗 Vegetarian")
                    if restaurant_info.get('google_serves_beer') == 1:
                        service_badges.append("🍺 Beer")
                    if restaurant_info.get('google_serves_wine') == 1:
                        service_badges.append("🍷 Wine")

                    if service_badges:
                        badges_html = " ".join([
                            f"<span style='background: #E8F5E9; color: #2E7D32; padding: 2px 8px; border-radius: 3px; font-size: 0.85em; margin-right: 5px; display: inline-block; margin-top: 3px;'>{badge}</span>"
                            for badge in service_badges
                        ])
                        st.markdown(badges_html, unsafe_allow_html=True)
                        st.markdown("")  # Spacer

                    # Contact information and links
                    contact_links = []

                    # Phone number
                    phone = restaurant_info.get('google_phone_national')
                    if pd.notna(phone) and phone:
                        contact_links.append(f"📞 <a href='tel:{phone}'>{phone}</a>")

                    # Website
                    website = restaurant_info.get('google_website_url') or restaurant_info.get('website_url')
                    if pd.notna(website) and website:
                        contact_links.append(f"🌐 <a href='{website}' target='_blank'>Website</a>")

                    # Google Maps
                    maps_url = restaurant_info.get('google_maps_url')
                    if pd.notna(maps_url) and maps_url:
                        contact_links.append(f"📍 <a href='{maps_url}' target='_blank'>View on Google Maps</a>")

                    if contact_links:
                        contact_html = " • ".join(contact_links)
                        st.markdown(f"<small>{contact_html}</small>", unsafe_allow_html=True)

                    # Data source attribution
                    st.markdown(f"<small style='color: #999;'>Data from {restaurant_info.get('data_source', 'unknown')} source</small>", unsafe_allow_html=True)

                    # Group items by category
                    for category in restaurant_items['category'].unique():
                        st.subheader(category)

                        category_items = restaurant_items[restaurant_items['category'] == category]

                        for _, item in category_items.iterrows():
                            # Get dietary tags for this item
                            item_tags = dietary_df[dietary_df['item_id'] == item['item_id']]['tag_name'].tolist()

                            # Display item
                            col1, col2 = st.columns([4, 1])

                            with col1:
                                st.markdown(f"**{item['item_name']}**")
                                if pd.notna(item['description']):
                                    st.markdown(f"<small>{item['description']}</small>", unsafe_allow_html=True)
                                if item_tags:
                                    tags_html = " ".join([f"<span style='background: #4CAF50; color: white; padding: 2px 8px; border-radius: 3px; font-size: 0.8em; margin-right: 5px;'>{tag}</span>" for tag in item_tags])
                                    st.markdown(tags_html, unsafe_allow_html=True)

                            with col2:
                                if pd.notna(item['price_gbp']):
                                    st.markdown(f"**£{item['price_gbp']:.2f}**")

                            st.markdown("---")

    # ------------------------------------------------------------------------
    # Tab 3: Price Analytics
    # ------------------------------------------------------------------------
    with tab3:
        st.header("Price Analytics")

        if filtered_menu.empty or filtered_menu['price_gbp'].isna().all():
            st.warning("⚠️ No pricing data available for selected filters.")
        else:
            # Price distribution by category
            st.subheader("Price Distribution by Category")
            fig_category = px.box(
                filtered_menu.dropna(subset=['price_gbp']),
                x='category',
                y='price_gbp',
                color='category',
                title="Price Range by Menu Category",
                labels={'price_gbp': 'Price (£)', 'category': 'Category'}
            )
            st.plotly_chart(fig_category, width="stretch")

            # Price distribution by restaurant
            st.subheader("Price Distribution by Restaurant")
            fig_restaurant = px.box(
                filtered_menu.dropna(subset=['price_gbp']),
                x='restaurant_name',
                y='price_gbp',
                color='restaurant_name',
                title="Price Range by Restaurant",
                labels={'price_gbp': 'Price (£)', 'restaurant_name': 'Restaurant'}
            )
            st.plotly_chart(fig_restaurant, width="stretch")

            # Price histogram
            st.subheader("Price Distribution")
            fig_hist = px.histogram(
                filtered_menu.dropna(subset=['price_gbp']),
                x='price_gbp',
                nbins=20,
                title="Distribution of Menu Item Prices",
                labels={'price_gbp': 'Price (£)'}
            )
            st.plotly_chart(fig_hist, width="stretch")

    # ------------------------------------------------------------------------
    # Tab 4: Restaurant Comparison
    # ------------------------------------------------------------------------
    with tab4:
        st.header("Restaurant Comparison")

        # Menu item count by restaurant
        st.subheader("Menu Size Comparison")
        restaurant_counts = filtered_menu.groupby('restaurant_name').size().reset_index(name='item_count')
        restaurant_counts = restaurant_counts.sort_values('item_count', ascending=False)

        # Calculate statistics for outlier detection
        import numpy as np
        q1 = restaurant_counts['item_count'].quantile(0.25)
        q3 = restaurant_counts['item_count'].quantile(0.75)
        iqr = q3 - q1
        outlier_threshold = q3 + 1.5 * iqr
        median_count = restaurant_counts['item_count'].median()

        # Identify outliers
        restaurant_counts['is_outlier'] = restaurant_counts['item_count'] > outlier_threshold
        outlier_count = restaurant_counts['is_outlier'].sum()

        # Show statistics
        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
        with col_stat1:
            st.metric("Median Items", f"{int(median_count)}", help="Middle value - less affected by extremes")
        with col_stat2:
            st.metric("Max Items", f"{int(restaurant_counts['item_count'].max())}")
        with col_stat3:
            st.metric("Min Items", f"{int(restaurant_counts['item_count'].min())}")
        with col_stat4:
            st.metric("Outliers", f"{outlier_count}", help=f"Restaurants with >{int(outlier_threshold)} items")

        # Add visualization options
        use_log_scale = st.checkbox("Use logarithmic scale", value=False,
                                    help="Helpful when a few restaurants have significantly more items")
        exclude_outliers = st.checkbox(f"Exclude outliers (>{int(outlier_threshold)} items)", value=False,
                                      help="Focus on typical restaurant menu sizes")

        # Apply outlier filter if requested
        display_counts = restaurant_counts.copy()
        if exclude_outliers and outlier_count > 0:
            display_counts = display_counts[~display_counts['is_outlier']]
            st.info(f"ℹ️ Hiding {outlier_count} outlier restaurant(s) to improve visualization clarity")

        # Create bar chart with optional log scale
        fig_counts = px.bar(
            display_counts,
            x='restaurant_name',
            y='item_count',
            title="Number of Menu Items per Restaurant",
            labels={'restaurant_name': 'Restaurant', 'item_count': 'Menu Items'},
            color='is_outlier' if not exclude_outliers else 'item_count',
            color_discrete_map={True: '#FF6B6B', False: '#4ECDC4'} if not exclude_outliers else None,
            color_continuous_scale='Blues' if exclude_outliers or outlier_count == 0 else None,
            hover_data={'is_outlier': False}
        )

        if use_log_scale:
            fig_counts.update_yaxes(type='log', title='Menu Items (log scale)')

        # Add reference line for median
        fig_counts.add_hline(y=median_count, line_dash="dash", line_color="green",
                            annotation_text=f"Median: {int(median_count)}",
                            annotation_position="right")

        st.plotly_chart(fig_counts, width="stretch")

        # Show outlier details if any exist
        if outlier_count > 0 and not exclude_outliers:
            with st.expander(f"⚠️ View {outlier_count} outlier restaurant(s) details"):
                outliers_df = restaurant_counts[restaurant_counts['is_outlier']][['restaurant_name', 'item_count']]
                outliers_df.columns = ['Restaurant', 'Menu Items']
                st.dataframe(outliers_df, hide_index=True, width="stretch")

        # Average price by restaurant
        if not filtered_menu['price_gbp'].isna().all():
            st.subheader("Average Price Comparison")
            restaurant_avg_price = filtered_menu.groupby('restaurant_name')['price_gbp'].mean().reset_index()
            restaurant_avg_price.columns = ['restaurant_name', 'avg_price']

            fig_avg_price = px.bar(
                restaurant_avg_price,
                x='restaurant_name',
                y='avg_price',
                title="Average Menu Item Price per Restaurant",
                labels={'restaurant_name': 'Restaurant', 'avg_price': 'Average Price (£)'},
                color='avg_price',
                color_continuous_scale='Greens'
            )
            st.plotly_chart(fig_avg_price, width="stretch")

        # Category distribution by restaurant
        st.subheader("Menu Category Distribution")

        # Optionally filter out outlier restaurants from category view
        category_menu = filtered_menu.copy()
        if exclude_outliers and outlier_count > 0:
            outlier_restaurants = restaurant_counts[restaurant_counts['is_outlier']]['restaurant_name'].tolist()
            category_menu = category_menu[~category_menu['restaurant_name'].isin(outlier_restaurants)]

        category_dist = category_menu.groupby(['restaurant_name', 'category']).size().reset_index(name='count')

        # Add percentage option for better comparison
        use_percentage = st.checkbox("Show as percentage of restaurant menu", value=False,
                                     help="Compare relative category proportions instead of absolute counts")

        if use_percentage:
            # Calculate percentages
            restaurant_totals = category_dist.groupby('restaurant_name')['count'].sum().reset_index(name='total')
            category_dist = category_dist.merge(restaurant_totals, on='restaurant_name')
            category_dist['percentage'] = (category_dist['count'] / category_dist['total'] * 100).round(1)

            fig_category_dist = px.bar(
                category_dist,
                x='restaurant_name',
                y='percentage',
                color='category',
                title="Menu Categories by Restaurant (Percentage)",
                labels={'restaurant_name': 'Restaurant', 'percentage': 'Percentage of Menu (%)'},
                barmode='stack',
                hover_data={'count': True, 'total': True}
            )
        else:
            fig_category_dist = px.bar(
                category_dist,
                x='restaurant_name',
                y='count',
                color='category',
                title="Menu Categories by Restaurant",
                labels={'restaurant_name': 'Restaurant', 'count': 'Number of Items'},
                barmode='stack'
            )

        st.plotly_chart(fig_category_dist, width="stretch")

        # Customer Reviews Comparison
        st.subheader("💬 Customer Reviews Comparison")

        # Check if review columns exist
        has_trustpilot = 'trustpilot_review_count' in filtered_restaurants.columns
        has_google = 'google_review_count' in filtered_restaurants.columns

        if not has_trustpilot and not has_google:
            st.info("💡 No review data available. Reviews data requires Trustpilot and/or Google review columns in the database.")
            reviewed_restaurants = pd.DataFrame()  # Empty dataframe
        else:
            # Merge restaurant data with review statistics from both sources
            restaurants_with_reviews = filtered_restaurants.copy()

            # Calculate combined review stats
            tp_count = restaurants_with_reviews['trustpilot_review_count'].fillna(0) if has_trustpilot else 0
            g_count = restaurants_with_reviews['google_review_count'].fillna(0) if has_google else 0
            restaurants_with_reviews['total_reviews'] = tp_count + g_count

            # Calculate weighted average rating
            def calculate_combined_rating(row):
                tp_reviews = row.get('trustpilot_review_count', 0) if has_trustpilot and pd.notna(row.get('trustpilot_review_count')) else 0
                tp_rating = row.get('trustpilot_avg_rating', 0) if has_trustpilot and pd.notna(row.get('trustpilot_avg_rating')) else 0
                g_reviews = row.get('google_review_count', 0) if has_google and pd.notna(row.get('google_review_count')) else 0
                g_rating = row.get('google_avg_rating', 0) if has_google and pd.notna(row.get('google_avg_rating')) else 0

                total = tp_reviews + g_reviews
                if total == 0:
                    return None
                return (tp_reviews * tp_rating + g_reviews * g_rating) / total

            restaurants_with_reviews['combined_rating'] = restaurants_with_reviews.apply(calculate_combined_rating, axis=1)

            # Filter to restaurants with reviews
            reviewed_restaurants = restaurants_with_reviews[restaurants_with_reviews['total_reviews'] > 0].copy()

        if not reviewed_restaurants.empty:
            # Show metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Restaurants with Reviews", len(reviewed_restaurants))
            with col2:
                total_all_reviews = reviewed_restaurants['total_reviews'].sum()
                st.metric("Total Reviews", f"{int(total_all_reviews):,}")
            with col3:
                avg_combined = reviewed_restaurants['combined_rating'].mean()
                st.metric("Average Rating (All Sources)", f"{avg_combined:.2f}/5")

            # Sort by rating
            reviewed_restaurants_sorted = reviewed_restaurants.sort_values('combined_rating', ascending=False)

            # Bar chart of ratings
            fig_reviews = px.bar(
                reviewed_restaurants_sorted.head(20),
                x='name',
                y='combined_rating',
                title="Top 20 Restaurants by Customer Rating (Combined Trustpilot + Google)",
                labels={'name': 'Restaurant', 'combined_rating': 'Average Rating'},
                color='combined_rating',
                color_continuous_scale='RdYlGn',
                range_color=[1, 5],
                hover_data={
                    'trustpilot_review_count': True,
                    'google_review_count': True,
                    'total_reviews': True
                }
            )
            fig_reviews.update_xaxes(tickangle=-45)
            st.plotly_chart(fig_reviews, width="stretch")

            # Scatter plot: Rating vs Review Count
            fig_scatter = px.scatter(
                reviewed_restaurants,
                x='total_reviews',
                y='combined_rating',
                size='total_reviews',
                color='combined_rating',
                hover_name='name',
                title="Customer Rating vs Number of Reviews",
                labels={'total_reviews': 'Total Reviews', 'combined_rating': 'Average Rating'},
                color_continuous_scale='RdYlGn',
                range_color=[1, 5]
            )
            fig_scatter.update_layout(xaxis_type="log")
            st.plotly_chart(fig_scatter, width="stretch")

            # Detailed table
            with st.expander("📊 View Detailed Review Statistics"):
                review_table = reviewed_restaurants[['name', 'cuisine_type', 'trustpilot_review_count',
                                                     'trustpilot_avg_rating', 'google_review_count',
                                                     'google_avg_rating', 'combined_rating', 'total_reviews']].copy()
                review_table.columns = ['Restaurant', 'Cuisine', 'Trustpilot Reviews', 'Trustpilot Rating',
                                       'Google Reviews', 'Google Rating', 'Combined Rating', 'Total Reviews']
                review_table = review_table.sort_values('Combined Rating', ascending=False)

                # Format numeric columns
                review_table['Trustpilot Reviews'] = review_table['Trustpilot Reviews'].fillna(0).astype(int)
                review_table['Google Reviews'] = review_table['Google Reviews'].fillna(0).astype(int)
                review_table['Total Reviews'] = review_table['Total Reviews'].astype(int)
                review_table['Trustpilot Rating'] = review_table['Trustpilot Rating'].apply(lambda x: f"{x:.2f}" if pd.notna(x) else "-")
                review_table['Google Rating'] = review_table['Google Rating'].apply(lambda x: f"{x:.2f}" if pd.notna(x) else "-")
                review_table['Combined Rating'] = review_table['Combined Rating'].apply(lambda x: f"{x:.2f}")

                st.dataframe(review_table, hide_index=True, width="stretch")
        else:
            st.info("💡 No review data available for the filtered restaurants. Visit the Reviews tab to see all reviews.")

    # ------------------------------------------------------------------------
    # Tab 5: Competitor Analysis
    # ------------------------------------------------------------------------
    with tab5:
        st.header("🎯 Competitor Analysis")
        st.markdown("Select a restaurant to find its top 5 competitors based on cuisine type, pricing, menu size, and category overlap.")

        # Pre-compute restaurant metrics for fast lookups (cached outside selection)
        @st.cache_data(ttl=300)
        def compute_restaurant_metrics(menu_data, resto_data):
            """Pre-compute metrics for all restaurants for fast competitor analysis."""
            metrics = {}
            for _, resto in resto_data.iterrows():
                if resto['data_source'] != 'real_scraped':
                    continue

                resto_id = resto['restaurant_id']
                resto_menu = menu_data[menu_data['restaurant_id'] == resto_id]

                if len(resto_menu) == 0:
                    continue

                metrics[resto_id] = {
                    'name': resto['name'],
                    'cuisine_type': resto['cuisine_type'],
                    'item_count': len(resto_menu),
                    'avg_price': resto_menu['price_gbp'].mean() if not resto_menu['price_gbp'].isna().all() else 0,
                    'categories': set(resto_menu['category'].dropna().unique())
                }
            return metrics

        # Pre-compute metrics once
        all_metrics = compute_restaurant_metrics(menu_df, restaurants_df)
        restaurants_with_data = [m['name'] for m in all_metrics.values()]

        if not restaurants_with_data:
            st.warning("⚠️ No restaurants with real data available for competitor analysis.")
        else:
            # Set default to Honky Tonk Wine Library if it exists
            default_index = 0
            if 'Honky Tonk Wine Library' in restaurants_with_data:
                default_index = sorted(restaurants_with_data).index('Honky Tonk Wine Library')

            selected_restaurant = st.selectbox(
                "Select a restaurant:",
                options=sorted(restaurants_with_data),
                index=default_index,
                help="Choose a restaurant to analyze its competitors",
                key="competitor_analysis_selector"
            )

            if selected_restaurant:
                # Get selected restaurant data
                target = restaurants_df[restaurants_df['name'] == selected_restaurant].iloc[0]
                target_id = target['restaurant_id']
                target_metrics = all_metrics[target_id]

                target_item_count = target_metrics['item_count']
                target_avg_price = target_metrics['avg_price']
                target_categories = target_metrics['categories']

                # Calculate similarity scores using pre-computed metrics
                competitors = []

                for resto_id, comp_metrics in all_metrics.items():
                    # Skip self
                    if resto_id == target_id:
                        continue

                    comp_item_count = comp_metrics['item_count']
                    comp_avg_price = comp_metrics['avg_price']
                    comp_categories = comp_metrics['categories']

                    # Calculate similarity score (0-100)
                    score = 0

                    # 1. Cuisine Type Match (40 points) - PRIMARY differentiator
                    if pd.notna(target['cuisine_type']) and pd.notna(comp_metrics['cuisine_type']):
                        if target['cuisine_type'] == comp_metrics['cuisine_type']:
                            score += 40
                        else:
                            # Check for meaningful word overlap (exclude connectors)
                            stop_words = {'&', 'and', 'the', 'a', 'an', 'at', 'of', 'in', 'on', '/', '-', '+', 'with'}
                            target_words = {word.lower() for word in target['cuisine_type'].split() if word.lower() not in stop_words and len(word) > 1}
                            comp_words = {word.lower() for word in comp_metrics['cuisine_type'].split() if word.lower() not in stop_words and len(word) > 1}

                            # Check if any meaningful words match
                            if target_words & comp_words:
                                score += 20

                    # 2. Price Similarity (30 points) - CRITICAL competitive factor
                    # Restaurants at different price points don't compete for same customers
                    if target_avg_price > 0 and comp_avg_price > 0:
                        price_diff_pct = abs(target_avg_price - comp_avg_price) / target_avg_price
                        if price_diff_pct <= 0.10:
                            score += 30
                        elif price_diff_pct <= 0.20:
                            score += 25
                        elif price_diff_pct <= 0.35:
                            score += 20
                        elif price_diff_pct <= 0.50:
                            score += 15

                    # 3. Category Overlap (20 points) - Menu similarity matters
                    # Jaccard similarity: measures shared categories vs unique categories
                    if target_categories and comp_categories:
                        intersection = len(target_categories & comp_categories)
                        union = len(target_categories | comp_categories)
                        jaccard = intersection / union if union > 0 else 0
                        score += jaccard * 20

                    # 4. Menu Size Similarity (10 points) - LEAST important
                    # A restaurant with 30 vs 50 items can still be direct competitors
                    if target_item_count > 0:
                        size_diff_pct = abs(target_item_count - comp_item_count) / target_item_count
                        if size_diff_pct <= 0.20:
                            score += 10
                        elif size_diff_pct <= 0.50:
                            score += 7
                        elif size_diff_pct <= 1.00:
                            score += 3

                    competitors.append({
                        'name': comp_metrics['name'],
                        'cuisine_type': comp_metrics['cuisine_type'],
                        'avg_price': comp_avg_price,
                        'item_count': comp_item_count,
                        'categories': comp_categories,
                        'similarity_score': round(score, 1)
                    })

                # Sort by similarity score and get top 5
                competitors.sort(key=lambda x: x['similarity_score'], reverse=True)
                top_competitors = competitors[:5]

                if not top_competitors:
                    st.warning("⚠️ No competitors found for this restaurant.")
                else:
                    # Display target restaurant info
                    st.subheader(f"📍 Target Restaurant: {selected_restaurant}")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Cuisine", target['cuisine_type'] if pd.notna(target['cuisine_type']) else "Unknown")
                    with col2:
                        st.metric("Avg Price", f"£{target_avg_price:.2f}" if target_avg_price > 0 else "N/A")
                    with col3:
                        st.metric("Menu Items", target_item_count)
                    with col4:
                        st.metric("Categories", len(target_categories))

                    st.divider()

                    # Check if restaurant has unique positioning (low similarity scores)
                    max_similarity = top_competitors[0]['similarity_score'] if top_competitors else 0

                    if max_similarity < 50:
                        st.info(f"""
                        💡 **Unique Market Position Detected**

                        {selected_restaurant} appears to have a **unique concept** with no close direct competitors in the database.
                        The highest similarity score is only {max_similarity:.1f}%, indicating this restaurant occupies a distinct market niche.

                        **What this means:**
                        - **Low competition risk** - Few direct competitors for the same customer base
                        - **Unique value proposition** - Distinctive cuisine/concept in Plymouth market
                        - **Market opportunity** - Potentially underserved customer segment

                        The results below show the *closest* matches, but they may serve different customer needs.
                        """)

                        # Suggest alternatives based on attributes
                        suggestions = []

                        # Look for cuisine-type alternatives
                        if pd.notna(target['cuisine_type']):
                            cuisine_words = target['cuisine_type'].split()
                            similar_cuisines = restaurants_df[
                                (restaurants_df['data_source'] == 'real_scraped') &
                                (restaurants_df['restaurant_id'] != target_id)
                            ].apply(lambda x: any(word in str(x['cuisine_type']) for word in cuisine_words), axis=1)

                            if similar_cuisines.sum() > 0:
                                suggestions.append(f"**Try searching:** Restaurants with similar cuisine keywords: {', '.join(cuisine_words[:3])}")

                        # Look for price-range alternatives
                        if target_avg_price > 0:
                            price_label = "budget-friendly" if target_avg_price < 12 else "mid-range" if target_avg_price < 20 else "premium"
                            suggestions.append(f"**Price positioning:** This is a {price_label} restaurant (£{target_avg_price:.2f} avg). Consider comparing with other {price_label} establishments.")

                        # Suggest category-based search
                        if target_categories:
                            top_cats = list(target_categories)[:3]
                            suggestions.append(f"**Menu focus:** Look for restaurants serving: {', '.join(top_cats)}")

                        if suggestions:
                            with st.expander("💡 Suggested Alternative Comparisons", expanded=False):
                                for suggestion in suggestions:
                                    st.markdown(f"- {suggestion}")

                    # Display top 5 competitors
                    if max_similarity >= 50:
                        st.subheader("🏆 Top 5 Competitors")
                    else:
                        st.subheader("🔍 Closest Alternatives (Low Match)")

                    for i, comp in enumerate(top_competitors, 1):
                        with st.expander(f"#{i} - {comp['name']} (Similarity: {comp['similarity_score']}%)", expanded=(i==1)):
                            col_a, col_b, col_c = st.columns(3)

                            with col_a:
                                st.markdown("**Restaurant Details:**")
                                st.markdown(f"- **Cuisine:** {comp['cuisine_type']}")
                                st.markdown(f"- **Avg Price:** £{comp['avg_price']:.2f}")
                                st.markdown(f"- **Menu Items:** {comp['item_count']}")

                            with col_b:
                                st.markdown("**Comparison:**")
                                price_diff = ((comp['avg_price'] - target_avg_price) / target_avg_price * 100) if target_avg_price > 0 else 0
                                st.markdown(f"- **Price Diff:** {price_diff:+.1f}%")
                                item_diff = ((comp['item_count'] - target_item_count) / target_item_count * 100) if target_item_count > 0 else 0
                                st.markdown(f"- **Size Diff:** {item_diff:+.1f}%")

                                # Category overlap
                                shared_cats = target_categories & comp['categories']
                                st.markdown(f"- **Shared Categories:** {len(shared_cats)}/{len(target_categories)}")

                            with col_c:
                                st.markdown("**Similarity Breakdown:**")

                                # Determine match quality with color coding
                                score = comp['similarity_score']
                                if score >= 70:
                                    quality = "Strong Match"
                                    color = "#4CAF50"  # Green
                                elif score >= 50:
                                    quality = "Good Match"
                                    color = "#2196F3"  # Blue
                                elif score >= 40:
                                    quality = "Fair Match"
                                    color = "#FF9800"  # Orange
                                else:
                                    quality = "Weak Match"
                                    color = "#F44336"  # Red

                                st.markdown(f"<span style='background: {color}; color: white; padding: 2px 8px; border-radius: 3px; font-size: 0.85em;'>{quality}</span>", unsafe_allow_html=True)

                                # Show a simple progress bar for similarity
                                st.progress(comp['similarity_score'] / 100)
                                st.markdown(f"**Score: {comp['similarity_score']}/100**")

                    # Comparison chart
                    st.divider()
                    st.subheader("📊 Competitor Comparison Chart")

                    # Prepare data for visualization
                    comparison_data = []
                    comparison_data.append({
                        'Restaurant': selected_restaurant + ' (Target)',
                        'Avg Price (£)': target_avg_price,
                        'Menu Items': target_item_count,
                        'Categories': len(target_categories),
                        'Type': 'Target'
                    })

                    for comp in top_competitors:
                        comparison_data.append({
                            'Restaurant': comp['name'],
                            'Avg Price (£)': comp['avg_price'],
                            'Menu Items': comp['item_count'],
                            'Categories': len(comp['categories']),
                            'Type': 'Competitor'
                        })

                    comparison_df = pd.DataFrame(comparison_data)

                    # Multi-metric comparison
                    col_chart1, col_chart2 = st.columns(2)

                    with col_chart1:
                        fig_price = px.bar(
                            comparison_df,
                            x='Restaurant',
                            y='Avg Price (£)',
                            color='Type',
                            title="Average Price Comparison",
                            color_discrete_map={'Target': '#FF6B6B', 'Competitor': '#4ECDC4'}
                        )
                        fig_price.update_xaxes(tickangle=-45)
                        st.plotly_chart(fig_price, width="stretch")

                    with col_chart2:
                        fig_items = px.bar(
                            comparison_df,
                            x='Restaurant',
                            y='Menu Items',
                            color='Type',
                            title="Menu Size Comparison",
                            color_discrete_map={'Target': '#FF6B6B', 'Competitor': '#4ECDC4'}
                        )
                        fig_items.update_xaxes(tickangle=-45)
                        st.plotly_chart(fig_items, width="stretch")

    # ------------------------------------------------------------------------
    # Tab 6: Drinks Analysis
    # ------------------------------------------------------------------------
    with tab6:
        st.header("🍹 Drinks Analysis")

        # Filter for drink items
        drink_categories = ['Drinks', 'Kids Drinks', 'Cocktails', 'Beer', 'Beverages', 'Coffee']
        drinks_df = menu_df[menu_df['category'].isin(drink_categories)].copy()

        if drinks_df.empty:
            st.warning("⚠️ No drink data available in the database.")
        else:
            # Overview statistics
            st.subheader("📊 Overview")
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                total_drinks = len(drinks_df)
                st.metric("Total Drinks", f"{total_drinks:,}")

            with col2:
                restaurants_with_drinks = drinks_df['restaurant_name'].nunique()
                st.metric("Restaurants with Drinks", restaurants_with_drinks)

            with col3:
                avg_drink_price = drinks_df[drinks_df['price_gbp'] > 0]['price_gbp'].mean()
                st.metric("Avg Drink Price", f"£{avg_drink_price:.2f}")

            with col4:
                price_range = f"£{drinks_df[drinks_df['price_gbp'] > 0]['price_gbp'].min():.2f} - £{drinks_df[drinks_df['price_gbp'] > 0]['price_gbp'].max():.2f}"
                st.metric("Price Range", price_range)

            st.divider()

            # Classify drinks by type based on name
            def classify_drink(name: str, category: str) -> str:
                """Classify drink into subcategories based on name and category."""
                name_lower = name.lower()

                if category == 'Cocktails':
                    return 'Cocktails'
                elif category == 'Beer':
                    return 'Beer'
                elif category == 'Kids Drinks':
                    return 'Soft Drinks'

                # Coffee & Hot Drinks
                if any(word in name_lower for word in ['coffee', 'espresso', 'cappuccino', 'latte', 'americano', 'mocha', 'macchiato']):
                    return 'Coffee'
                elif any(word in name_lower for word in ['tea', 'hot chocolate', 'chai']):
                    return 'Hot Drinks'

                # Alcoholic
                elif any(word in name_lower for word in ['beer', 'lager', 'ale', 'ipa', 'stout', 'cider', 'pint']):
                    return 'Beer & Cider'
                elif any(word in name_lower for word in ['wine', 'prosecco', 'champagne', 'rosé', 'pinot', 'chardonnay', 'merlot', 'sauvignon']):
                    return 'Wine'
                elif any(word in name_lower for word in ['cocktail', 'margarita', 'mojito', 'martini', 'daiquiri', 'gin', 'vodka', 'rum', 'whisky', 'whiskey', 'tequila']):
                    return 'Cocktails & Spirits'

                # Non-alcoholic
                elif any(word in name_lower for word in ['juice', 'orange', 'apple', 'pineapple', 'cranberry', 'tomato']):
                    return 'Juice'
                elif any(word in name_lower for word in ['smoothie', 'milkshake', 'shake', 'frappe', 'frappuccino']):
                    return 'Smoothies & Shakes'
                elif any(word in name_lower for word in ['water', 'mineral', 'sparkling', 'still']):
                    return 'Water'
                elif any(word in name_lower for word in ['coke', 'cola', 'pepsi', 'fanta', 'sprite', 'lemonade', 'soda', 'fizzy', 'soft drink']):
                    return 'Soft Drinks'

                return 'Other Drinks'

            drinks_df['drink_type'] = drinks_df.apply(
                lambda row: classify_drink(row['item_name'], row['category']),
                axis=1
            )

            # Drink type distribution
            st.subheader("🥤 Drink Types Distribution")

            col_a, col_b = st.columns([2, 1])

            with col_a:
                type_counts = drinks_df['drink_type'].value_counts().reset_index()
                type_counts.columns = ['Drink Type', 'Count']

                fig_types = px.bar(
                    type_counts,
                    x='Drink Type',
                    y='Count',
                    title="Number of Drinks by Type",
                    color='Count',
                    color_continuous_scale='Blues'
                )
                fig_types.update_xaxes(tickangle=-45)
                st.plotly_chart(fig_types, width="stretch")

            with col_b:
                st.dataframe(
                    type_counts,
                    hide_index=True,
                    width="stretch"
                )

            st.divider()

            # Price analysis by drink type
            st.subheader("💰 Price Analysis by Drink Type")

            drinks_with_price = drinks_df[drinks_df['price_gbp'] > 0].copy()

            if not drinks_with_price.empty:
                col_c, col_d = st.columns(2)

                with col_c:
                    # Box plot by drink type
                    fig_price_box = px.box(
                        drinks_with_price,
                        x='drink_type',
                        y='price_gbp',
                        title="Price Distribution by Drink Type",
                        color='drink_type',
                        labels={'price_gbp': 'Price (£)', 'drink_type': 'Drink Type'}
                    )
                    fig_price_box.update_xaxes(tickangle=-45)
                    st.plotly_chart(fig_price_box, width="stretch")

                with col_d:
                    # Average prices by type
                    avg_prices = drinks_with_price.groupby('drink_type')['price_gbp'].agg(['mean', 'min', 'max', 'count']).reset_index()
                    avg_prices.columns = ['Drink Type', 'Avg Price', 'Min Price', 'Max Price', 'Count']
                    avg_prices['Avg Price'] = avg_prices['Avg Price'].apply(lambda x: f"£{x:.2f}")
                    avg_prices['Min Price'] = avg_prices['Min Price'].apply(lambda x: f"£{x:.2f}")
                    avg_prices['Max Price'] = avg_prices['Max Price'].apply(lambda x: f"£{x:.2f}")
                    avg_prices = avg_prices.sort_values('Count', ascending=False)

                    st.dataframe(
                        avg_prices,
                        hide_index=True,
                        width="stretch",
                        height=400
                    )

            st.divider()

            # Restaurant rankings
            st.subheader("🏆 Restaurant Rankings")

            col_e, col_f = st.columns(2)

            with col_e:
                st.markdown("**Top 10 Restaurants by Drink Count**")

                resto_counts = drinks_df.groupby('restaurant_name').agg({
                    'item_id': 'count',
                    'price_gbp': lambda x: x[x > 0].mean() if len(x[x > 0]) > 0 else 0
                }).reset_index()
                resto_counts.columns = ['Restaurant', 'Drink Count', 'Avg Price']
                resto_counts = resto_counts.sort_values('Drink Count', ascending=False).head(10)
                resto_counts['Avg Price'] = resto_counts['Avg Price'].apply(lambda x: f"£{x:.2f}" if x > 0 else "N/A")

                st.dataframe(
                    resto_counts,
                    hide_index=True,
                    width="stretch"
                )

            with col_f:
                st.markdown("**Most Expensive Drinks**")

                expensive_drinks = drinks_with_price.nlargest(10, 'price_gbp')[
                    ['item_name', 'price_gbp', 'drink_type', 'restaurant_name']
                ].copy()
                expensive_drinks.columns = ['Drink', 'Price', 'Type', 'Restaurant']
                expensive_drinks['Price'] = expensive_drinks['Price'].apply(lambda x: f"£{x:.2f}")

                st.dataframe(
                    expensive_drinks,
                    hide_index=True,
                    width="stretch"
                )

            st.divider()

            # Specific drink comparisons
            st.subheader("☕ Compare Common Drinks Across Restaurants")

            # Common drink search terms
            drink_search = st.selectbox(
                "Select a drink type to compare:",
                [
                    'Coffee (all types)',
                    'Cappuccino',
                    'Latte',
                    'Espresso',
                    'Beer/Pint',
                    'Wine',
                    'Cocktail',
                    'Coca Cola/Coke',
                    'Juice',
                    'Water'
                ]
            )

            # Map search terms to keywords
            search_mapping = {
                'Coffee (all types)': ['coffee', 'cappuccino', 'latte', 'americano', 'espresso', 'mocha'],
                'Cappuccino': ['cappuccino'],
                'Latte': ['latte'],
                'Espresso': ['espresso'],
                'Beer/Pint': ['beer', 'pint', 'lager', 'ale'],
                'Wine': ['wine'],
                'Cocktail': ['cocktail', 'margarita', 'mojito', 'martini'],
                'Coca Cola/Coke': ['coca cola', 'coke', 'cola'],
                'Juice': ['juice', 'orange juice', 'apple juice'],
                'Water': ['water', 'mineral water']
            }

            keywords = search_mapping[drink_search]

            # Filter drinks matching keywords
            matching_drinks = drinks_with_price[
                drinks_with_price['item_name'].str.lower().apply(
                    lambda x: any(keyword in x for keyword in keywords)
                )
            ].copy()

            if not matching_drinks.empty:
                col_g, col_h = st.columns([2, 1])

                with col_g:
                    # Bar chart of prices
                    comparison_df = matching_drinks.groupby('restaurant_name')['price_gbp'].mean().reset_index()
                    comparison_df.columns = ['Restaurant', 'Avg Price']
                    comparison_df = comparison_df.sort_values('Avg Price', ascending=False).head(15)

                    fig_comparison = px.bar(
                        comparison_df,
                        x='Restaurant',
                        y='Avg Price',
                        title=f"Average {drink_search} Price by Restaurant (Top 15)",
                        labels={'Avg Price': 'Price (£)'},
                        color='Avg Price',
                        color_continuous_scale='Viridis'
                    )
                    fig_comparison.update_xaxes(tickangle=-45)
                    st.plotly_chart(fig_comparison, width="stretch")

                with col_h:
                    # Statistics
                    st.metric("Restaurants Serving", matching_drinks['restaurant_name'].nunique())
                    st.metric("Total Items Found", len(matching_drinks))
                    st.metric("Cheapest", f"£{matching_drinks['price_gbp'].min():.2f}")
                    st.metric("Most Expensive", f"£{matching_drinks['price_gbp'].max():.2f}")
                    st.metric("Average", f"£{matching_drinks['price_gbp'].mean():.2f}")

                # Detailed list
                st.markdown(f"**All {drink_search} Items Found:**")
                detailed_list = matching_drinks[['item_name', 'price_gbp', 'restaurant_name']].copy()
                detailed_list.columns = ['Drink', 'Price', 'Restaurant']
                detailed_list['Price'] = detailed_list['Price'].apply(lambda x: f"£{x:.2f}")
                detailed_list = detailed_list.sort_values('Price')

                st.dataframe(
                    detailed_list,
                    hide_index=True,
                    width="stretch",
                    height=400
                )
            else:
                st.info(f"No {drink_search} items found in the database.")

            st.divider()

            # Dedicated beer comparison section
            st.subheader("🍺 Complete Beer & Cider Analysis")

            # Filter for beer and cider items (exclude food items)
            def is_beer_drink(row):
                """Check if item is actually a beer/cider drink (not food)."""
                name_lower = row['item_name'].lower()
                category_lower = str(row['category']).lower()

                # Exclude food categories
                if any(word in category_lower for word in ['burger', 'side', 'uncategorized', 'food', 'main', 'starter']):
                    return False

                # Check for beer/cider keywords
                beer_keywords = ['beer', 'pint', 'lager', 'ale', 'ipa', 'stout', 'cider', 'bitter']
                if any(keyword in name_lower for keyword in beer_keywords):
                    # Exclude food items that happen to have beer in the name
                    food_keywords = ['batter', 'crisp', 'chip', 'burger', 'chicken', 'wing', 'fries', 'onion ring']
                    if not any(food in name_lower for food in food_keywords):
                        return True

                return False

            beer_items = drinks_with_price[drinks_with_price.apply(is_beer_drink, axis=1)].copy()

            if not beer_items.empty:
                # Classify beer type
                def classify_beer(name: str) -> str:
                    """Classify beer into subcategories."""
                    name_lower = name.lower()

                    if any(word in name_lower for word in ['cider', 'scrumpy']):
                        return 'Cider'
                    elif any(word in name_lower for word in ['lager', 'pilsner', 'pilsen']):
                        return 'Lager'
                    elif any(word in name_lower for word in ['ipa', 'pale ale']):
                        return 'IPA/Pale Ale'
                    elif any(word in name_lower for word in ['stout', 'porter', 'guinness']):
                        return 'Stout/Porter'
                    elif any(word in name_lower for word in ['real ale', 'bitter', 'best bitter']):
                        return 'Real Ale/Bitter'
                    elif any(word in name_lower for word in ['craft beer', 'craft']):
                        return 'Craft Beer'
                    elif 'ale' in name_lower:
                        return 'Ale'
                    else:
                        return 'Beer (General)'

                beer_items['beer_type'] = beer_items['item_name'].apply(classify_beer)

                # Overview metrics
                col_beer1, col_beer2, col_beer3, col_beer4 = st.columns(4)

                with col_beer1:
                    st.metric("Total Beers/Ciders", len(beer_items))

                with col_beer2:
                    st.metric("Restaurants", beer_items['restaurant_name'].nunique())

                with col_beer3:
                    st.metric("Cheapest", f"£{beer_items['price_gbp'].min():.2f}")

                with col_beer4:
                    st.metric("Most Expensive", f"£{beer_items['price_gbp'].max():.2f}")

                # Beer type distribution
                col_type1, col_type2 = st.columns([2, 1])

                with col_type1:
                    beer_type_counts = beer_items['beer_type'].value_counts().reset_index()
                    beer_type_counts.columns = ['Beer Type', 'Count']

                    fig_beer_types = px.pie(
                        beer_type_counts,
                        names='Beer Type',
                        values='Count',
                        title="Beer & Cider Types Distribution",
                        hole=0.3
                    )
                    st.plotly_chart(fig_beer_types, width="stretch")

                with col_type2:
                    st.dataframe(
                        beer_type_counts,
                        hide_index=True,
                        width="stretch"
                    )

                st.markdown("**All Beers & Ciders Comparison:**")

                # Create comprehensive comparison table
                beer_comparison = beer_items[['item_name', 'price_gbp', 'beer_type', 'restaurant_name']].copy()
                beer_comparison.columns = ['Beer/Cider Name', 'Price (£)', 'Type', 'Restaurant']
                beer_comparison = beer_comparison.sort_values('Price (£)')

                # Add price formatting for display
                display_beer = beer_comparison.copy()
                display_beer['Price'] = display_beer['Price (£)'].apply(lambda x: f"£{x:.2f}")
                display_beer = display_beer[['Beer/Cider Name', 'Price', 'Type', 'Restaurant']]

                # Allow sorting
                st.dataframe(
                    display_beer,
                    hide_index=True,
                    width="stretch",
                    height=600
                )

                # Price comparison by type
                st.markdown("**Average Price by Beer Type:**")

                avg_by_type = beer_items.groupby('beer_type')['price_gbp'].agg(['mean', 'min', 'max', 'count']).reset_index()
                avg_by_type.columns = ['Beer Type', 'Avg Price', 'Min Price', 'Max Price', 'Count']
                avg_by_type = avg_by_type.sort_values('Avg Price', ascending=False)

                col_chart1, col_chart2 = st.columns([2, 1])

                with col_chart1:
                    fig_beer_price = px.bar(
                        avg_by_type,
                        x='Beer Type',
                        y='Avg Price',
                        title="Average Price by Beer Type",
                        labels={'Avg Price': 'Average Price (£)'},
                        color='Avg Price',
                        color_continuous_scale='YlOrBr',
                        text='Avg Price'
                    )
                    fig_beer_price.update_traces(texttemplate='£%{text:.2f}', textposition='outside')
                    fig_beer_price.update_xaxes(tickangle=-45)
                    st.plotly_chart(fig_beer_price, width="stretch")

                with col_chart2:
                    display_avg = avg_by_type.copy()
                    display_avg['Avg Price'] = display_avg['Avg Price'].apply(lambda x: f"£{x:.2f}")
                    display_avg['Min Price'] = display_avg['Min Price'].apply(lambda x: f"£{x:.2f}")
                    display_avg['Max Price'] = display_avg['Max Price'].apply(lambda x: f"£{x:.2f}")

                    st.dataframe(
                        display_avg,
                        hide_index=True,
                        width="stretch"
                    )

                # Best value analysis
                st.markdown("**💰 Best Value Beers (Cheapest Options by Type):**")

                cheapest_by_type = beer_items.loc[beer_items.groupby('beer_type')['price_gbp'].idxmin()]
                cheapest_display = cheapest_by_type[['beer_type', 'item_name', 'price_gbp', 'restaurant_name']].copy()
                cheapest_display.columns = ['Type', 'Beer/Cider', 'Price', 'Restaurant']
                cheapest_display['Price'] = cheapest_display['Price'].apply(lambda x: f"£{x:.2f}")
                cheapest_display = cheapest_display.sort_values('Type')

                st.dataframe(
                    cheapest_display,
                    hide_index=True,
                    width="stretch"
                )

            else:
                st.info("No beer or cider items found in the database.")

    # ------------------------------------------------------------------------
    # Tab 7: Hygiene Ratings
    # ------------------------------------------------------------------------
    with tab7:
        st.header("⭐ Food Hygiene Ratings")

        st.markdown("""
        Food hygiene ratings are provided by the [Food Standards Agency (FSA)](https://www.food.gov.uk/safety-hygiene/food-hygiene-rating-scheme)
        and reflect the hygiene standards found at the time of inspection.
        """)

        # Overview
        rated_restaurants = filtered_restaurants[filtered_restaurants['hygiene_rating'].notna()]

        if rated_restaurants.empty:
            st.warning("⚠️ No hygiene ratings available for the selected restaurants.")
        else:
            # Overview metrics
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Restaurants Rated", f"{len(rated_restaurants)} of {len(filtered_restaurants)}")

            with col2:
                avg_rating = rated_restaurants['hygiene_rating'].mean()
                st.metric("Average Rating", f"{avg_rating:.2f}/5")

            with col3:
                top_rated = (rated_restaurants['hygiene_rating'] == 5).sum()
                pct = top_rated / len(rated_restaurants) * 100
                st.metric("5★ (Very Good)", f"{top_rated} ({pct:.0f}%)")

            with col4:
                low_rated = (rated_restaurants['hygiene_rating'] <= 2).sum()
                if low_rated > 0:
                    st.metric("≤2★ (Needs Improvement)", f"{low_rated}", delta_color="inverse")
                else:
                    st.metric("≤2★ (Needs Improvement)", "0")

            st.divider()

            # Rating distribution
            st.subheader("📊 Rating Distribution")

            col_chart1, col_chart2 = st.columns([2, 1])

            with col_chart1:
                rating_counts = rated_restaurants['hygiene_rating'].value_counts().sort_index(ascending=False).reset_index()
                rating_counts.columns = ['Rating', 'Count']
                rating_counts['Stars'] = rating_counts['Rating'].apply(lambda x: "⭐" * int(x))

                fig_ratings = px.bar(
                    rating_counts,
                    x='Stars',
                    y='Count',
                    title="Number of Restaurants by Hygiene Rating",
                    color='Rating',
                    color_continuous_scale='RdYlGn',
                    text='Count'
                )
                fig_ratings.update_traces(textposition='outside')
                st.plotly_chart(fig_ratings, width="stretch")

            with col_chart2:
                display_counts = rating_counts.copy()
                display_counts['Percentage'] = (display_counts['Count'] / display_counts['Count'].sum() * 100).apply(lambda x: f"{x:.1f}%")
                st.dataframe(
                    display_counts[['Stars', 'Count', 'Percentage']],
                    hide_index=True,
                    width="stretch"
                )

            st.divider()

            # Detailed score breakdown
            st.subheader("📋 Detailed Scores Breakdown")

            st.markdown("""
            The FSA scores establishments in three areas (lower is better):
            - **Hygiene**: Food handling, preparation, cooking, storage
            - **Structural**: Cleanliness, layout, ventilation, pest control
            - **Confidence in Management**: Food safety systems, training, protocols
            """)

            # Show restaurants with detailed scores
            score_df = rated_restaurants[['name', 'fsa_business_name', 'fsa_postcode',
                                         'hygiene_rating', 'hygiene_score_hygiene',
                                         'hygiene_score_structural', 'hygiene_score_confidence',
                                         'hygiene_rating_date', 'fsa_new_rating_pending']].copy()

            # Format scores with color coding
            def format_score(score):
                if pd.isna(score):
                    return "N/A"
                score = int(score)
                if score == 0:
                    return f"✅ {score}"
                elif score <= 10:
                    return f"🟢 {score}"
                elif score <= 15:
                    return f"🟡 {score}"
                elif score <= 20:
                    return f"🟠 {score}"
                else:
                    return f"🔴 {score}"

            # Sort by rating descending
            score_df = score_df.sort_values('hygiene_rating', ascending=False)

            # Create interactive table with view profile buttons
            st.markdown("**📋 Detailed Scores - Click 👁️ to view restaurant profile**")

            # Header row
            header_cols = st.columns([2.5, 2, 1.2, 1.2, 1, 1, 1, 1.2, 0.8, 0.8])
            header_cols[0].markdown("**Restaurant**")
            header_cols[1].markdown("**FSA Name**")
            header_cols[2].markdown("**Postcode**")
            header_cols[3].markdown("**Rating**")
            header_cols[4].markdown("**Hygiene**")
            header_cols[5].markdown("**Structural**")
            header_cols[6].markdown("**Management**")
            header_cols[7].markdown("**Inspection**")
            header_cols[8].markdown("**Pending**")
            header_cols[9].markdown("**View**")

            st.markdown("---")

            # Create a container with scrollable content
            with st.container():
                # Data rows (limit to first 50 for performance, add pagination if needed)
                for idx, row in enumerate(score_df.itertuples()):
                    if idx >= 50:  # Limit display for performance
                        break

                    cols = st.columns([2.5, 2, 1.2, 1.2, 1, 1, 1, 1.2, 0.8, 0.8])

                    with cols[0]:
                        st.markdown(f"{row.name}")

                    with cols[1]:
                        fsa_name = row.fsa_business_name if pd.notna(row.fsa_business_name) else "N/A"
                        st.markdown(f"{fsa_name}")

                    with cols[2]:
                        postcode = row.fsa_postcode if pd.notna(row.fsa_postcode) else "N/A"
                        st.markdown(f"{postcode}")

                    with cols[3]:
                        rating = int(row.hygiene_rating)
                        # Color-code the rating
                        if rating == 5:
                            st.markdown(f"🟢 **{rating}**")
                        elif rating == 4:
                            st.markdown(f"🟢 **{rating}**")
                        elif rating == 3:
                            st.markdown(f"🟡 **{rating}**")
                        elif rating == 2:
                            st.markdown(f"🟠 **{rating}**")
                        elif rating == 1:
                            st.markdown(f"🔴 **{rating}**")
                        else:
                            st.markdown(f"❌ **{rating}**")

                    with cols[4]:
                        st.markdown(format_score(row.hygiene_score_hygiene))

                    with cols[5]:
                        st.markdown(format_score(row.hygiene_score_structural))

                    with cols[6]:
                        st.markdown(format_score(row.hygiene_score_confidence))

                    with cols[7]:
                        inspection_date = pd.to_datetime(row.hygiene_rating_date, format='ISO8601').strftime('%Y-%m-%d')
                        st.markdown(f"`{inspection_date}`")

                    with cols[8]:
                        if pd.notna(row.fsa_new_rating_pending) and str(row.fsa_new_rating_pending).lower() == 'true':
                            st.markdown("⏳")
                        else:
                            st.markdown("✓")

                    with cols[9]:
                        if st.button("👁️", key=f"view_profile_{idx}", help=f"View profile for {row.name}"):
                            st.session_state['selected_restaurant_profile'] = row.name
                            st.rerun()

                if len(score_df) > 50:
                    st.info(f"Showing first 50 of {len(score_df)} restaurants")

            st.divider()

            # Restaurants needing attention
            low_rated_restos = rated_restaurants[rated_restaurants['hygiene_rating'] <= 2]

            if not low_rated_restos.empty:
                st.subheader("🚨 Restaurants Requiring Attention (≤2★)")

                for idx, resto in enumerate(low_rated_restos.iterrows()):
                    _, resto = resto
                    rating = int(resto['hygiene_rating'])
                    stars = "⭐" * rating if rating > 0 else "❌"

                    with st.expander(f"{resto['name']}: {stars} ({rating})"):
                        st.markdown(f"**Inspected:** {str(resto['hygiene_rating_date'])[:10]}")
                        st.markdown(f"**Business Type:** {resto.get('fsa_business_type', 'N/A')}")

                        st.markdown("**Scores:**")
                        col_s1, col_s2, col_s3 = st.columns(3)

                        with col_s1:
                            hyg_score = resto.get('hygiene_score_hygiene')
                            if pd.notna(hyg_score):
                                st.metric("Hygiene", int(hyg_score))

                        with col_s2:
                            struct_score = resto.get('hygiene_score_structural')
                            if pd.notna(struct_score):
                                st.metric("Structural", int(struct_score))

                        with col_s3:
                            conf_score = resto.get('hygiene_score_confidence')
                            if pd.notna(conf_score):
                                st.metric("Management", int(conf_score))

                        # Calculate total and explain
                        if all(pd.notna([hyg_score, struct_score, conf_score])):
                            total = int(hyg_score) + int(struct_score) + int(conf_score)
                            st.markdown(f"**Total Score:** {total} points")

                            if total >= 50:
                                st.error("🔴 Urgent improvement required (50+ points)")
                            elif total >= 35:
                                st.warning("🟠 Improvement necessary (35-40 points)")

                        # Add "View Profile" button
                        if st.button(f"📍 View Full Profile for {resto['name']}", key=f"low_rated_profile_{idx}"):
                            st.session_state['selected_restaurant_profile'] = resto['name']
                            st.success(f"✅ Selected: {resto['name']}")
                            st.info("👆 Now go to the **🏢 Restaurant Profiles** tab to see the full profile!")

            st.divider()

            # FSA Attribution
            st.info("""
            **Data Source:** [Food Standards Agency - Food Hygiene Rating Scheme](https://www.food.gov.uk/safety-hygiene/food-hygiene-rating-scheme)

            Ratings are updated regularly. Last data fetch: 2025-11-15

            For the most current information, visit the [official FSA ratings website](https://ratings.food.gov.uk/).
            """)

    # ------------------------------------------------------------------------
    # Tab 1: Map View
    # ------------------------------------------------------------------------
    with tab1:
        st.header("🗺️ Restaurant Map")
        st.markdown("Interactive map showing restaurant locations with hygiene ratings and licensing information. Hover over markers for details.")

        # Filter restaurants with GPS coordinates
        restaurants_with_gps = filtered_restaurants[
            filtered_restaurants['fsa_latitude'].notna() &
            filtered_restaurants['fsa_longitude'].notna()
        ].copy()

        if restaurants_with_gps.empty:
            st.warning("⚠️ No restaurants have GPS coordinates available.")
        else:
            # Display count
            st.info(f"📍 Showing {len(restaurants_with_gps)} restaurants with GPS coordinates")

            # Filtering options
            col_filter1, col_filter2, col_filter3 = st.columns(3)

            with col_filter1:
                show_hygiene_filter = st.checkbox("Color by Hygiene Rating", value=True)

            with col_filter2:
                if show_hygiene_filter:
                    min_hygiene = st.selectbox(
                        "Minimum Hygiene Rating",
                        options=[1, 2, 3, 4, 5],
                        index=0,
                        help="Show only restaurants with this minimum rating"
                    )
                    restaurants_with_gps = restaurants_with_gps[restaurants_with_gps['hygiene_rating'] >= min_hygiene]

            with col_filter3:
                map_style = st.selectbox(
                    "Map Style",
                    options=["Open Street Map", "Satellite"],
                    index=0
                )

            # Prepare map data (include licensing and business rates columns)
            map_data = restaurants_with_gps[['restaurant_id', 'name', 'fsa_latitude', 'fsa_longitude', 'hygiene_rating',
                                             'fsa_business_name', 'fsa_address_line1', 'fsa_address_line2',
                                             'fsa_postcode', 'cuisine_type', 'price_range',
                                             'licensing_number', 'licensing_activities',
                                             'business_rates_rateable_value', 'business_rates_net_charge',
                                             'business_rates_category']].copy()

            # Rename columns for pydeck
            map_data = map_data.rename(columns={
                'fsa_latitude': 'lat',
                'fsa_longitude': 'lon'
            })

            # Spread overlapping markers in a circle pattern
            # Round coordinates to detect near-duplicates within ~2 meters (0.00001 degrees)
            import numpy as np
            map_data['lat_rounded'] = map_data['lat'].round(5)
            map_data['lon_rounded'] = map_data['lon'].round(5)

            coord_groups = map_data.groupby(['lat_rounded', 'lon_rounded']).size()
            duplicate_coords = coord_groups[coord_groups > 1].index

            # Apply circular spread to near-duplicate coordinates only
            for coord in duplicate_coords:
                mask = (map_data['lat_rounded'] == coord[0]) & (map_data['lon_rounded'] == coord[1])
                duplicate_rows = map_data[mask].copy()
                n_duplicates = len(duplicate_rows)

                # Calculate center point for this cluster
                center_lat = duplicate_rows['lat'].mean()
                center_lon = duplicate_rows['lon'].mean()

                # Spread in a circle (0.00002 degrees ≈ 2 meters radius)
                radius = 0.00002
                for i, (idx, row) in enumerate(duplicate_rows.iterrows()):
                    # Use restaurant_id for consistent angle assignment
                    angle = (2 * np.pi * hash(row['restaurant_id']) / (2**32)) + (2 * np.pi * i / n_duplicates)
                    map_data.loc[idx, 'lat'] = center_lat + radius * np.sin(angle)
                    map_data.loc[idx, 'lon'] = center_lon + radius * np.cos(angle)

            # Drop temporary rounding columns
            map_data = map_data.drop(columns=['lat_rounded', 'lon_rounded'])

            # Create color mapping for hygiene ratings
            def get_rating_color(rating):
                if pd.isna(rating):
                    return [150, 150, 150, 200]  # Gray
                rating = int(rating)
                if rating == 5:
                    return [0, 200, 0, 200]  # Green
                elif rating == 4:
                    return [100, 220, 0, 200]  # Light green
                elif rating == 3:
                    return [255, 200, 0, 200]  # Yellow
                elif rating == 2:
                    return [255, 100, 0, 200]  # Orange
                else:
                    return [200, 0, 0, 200]  # Red

            map_data['color'] = map_data['hygiene_rating'].apply(get_rating_color)

            # Create tooltip with licensing info
            def create_tooltip(row):
                tooltip = f"{row['name']}\n"
                tooltip += f"FSA: {row['fsa_business_name'] if pd.notna(row['fsa_business_name']) else 'N/A'}\n"
                tooltip += f"Rating: {'⭐' * int(row['hygiene_rating']) if pd.notna(row['hygiene_rating']) else 'N/A'}\n"
                tooltip += f"Address: {row['fsa_address_line1'] if pd.notna(row['fsa_address_line1']) else ''}, " + \
                          f"{row['fsa_postcode'] if pd.notna(row['fsa_postcode']) else ''}\n"
                tooltip += f"Cuisine: {row['cuisine_type'] if pd.notna(row['cuisine_type']) else 'N/A'}\n"
                tooltip += f"Price: {row['price_range'] if pd.notna(row['price_range']) else 'N/A'}\n"

                # Add licensing info if available
                if pd.notna(row.get('licensing_number')):
                    tooltip += f"📜 License: {row['licensing_number']}\n"

                    # Add activities if available
                    if pd.notna(row.get('licensing_activities')) and row.get('licensing_activities') != '[]':
                        try:
                            import json
                            activities = json.loads(row['licensing_activities'])
                            if activities and len(activities) > 0:
                                # Show first 2 activities
                                activities_display = ', '.join(activities[:2])
                                tooltip += f"Activities: {activities_display}\n"
                        except:
                            pass
                else:
                    tooltip += "📜 No license data\n"

                # Add business rates info if available
                if pd.notna(row.get('business_rates_rateable_value')):
                    rv = int(row['business_rates_rateable_value'])
                    tooltip += f"💷 Rateable Value: £{rv:,}\n"

                    if pd.notna(row.get('business_rates_net_charge')):
                        charge = float(row['business_rates_net_charge'])
                        tooltip += f"💷 Annual Rates: £{charge:,.0f}\n"

                    if pd.notna(row.get('business_rates_category')):
                        category = str(row['business_rates_category'])
                        tooltip += f"Category: {category}\n"

                return tooltip.rstrip()

            map_data['tooltip_text'] = map_data.apply(create_tooltip, axis=1)

            # Calculate center of map
            center_lat = map_data['lat'].mean()
            center_lon = map_data['lon'].mean()

            # Create pydeck layer
            layer = pdk.Layer(
                "ScatterplotLayer",
                data=map_data,
                get_position=["lon", "lat"],
                get_color="color",
                get_radius=50,
                radius_min_pixels=3,
                radius_max_pixels=10,
                pickable=True,
            )

            # Set map style
            if map_style == "Satellite":
                map_style_url = "mapbox://styles/mapbox/satellite-v9"
            else:
                map_style_url = None  # Default to Open Street Map

            # Create view state
            view_state = pdk.ViewState(
                latitude=center_lat,
                longitude=center_lon,
                zoom=12,
                pitch=0,
            )

            # Create deck
            deck = pdk.Deck(
                layers=[layer],
                initial_view_state=view_state,
                map_style=map_style_url,
                tooltip={"text": "{tooltip_text}"}
            )

            # Display map
            st.pydeck_chart(deck)

            # Legend
            st.markdown("### 🎨 Map Legend")
            legend_cols = st.columns(5)
            legend_cols[0].markdown("🟢 **5 Stars** (Very Good)")
            legend_cols[1].markdown("🟢 **4 Stars** (Good)")
            legend_cols[2].markdown("🟡 **3 Stars** (Satisfactory)")
            legend_cols[3].markdown("🟠 **2 Stars** (Improvement Necessary)")
            legend_cols[4].markdown("🔴 **1 Star** (Major Improvement)")

            # Statistics
            st.divider()
            st.subheader("📊 Map Statistics")
            stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

            with stat_col1:
                st.metric("Total Mapped", len(map_data))

            with stat_col2:
                avg_rating = map_data['hygiene_rating'].mean()
                st.metric("Avg Rating", f"{avg_rating:.2f}⭐")

            with stat_col3:
                if not map_data.empty:
                    top_area = map_data['fsa_postcode'].mode()[0] if len(map_data['fsa_postcode'].mode()) > 0 else "N/A"
                    st.metric("Top Area", top_area)

            with stat_col4:
                coverage_pct = (len(restaurants_with_gps) / len(filtered_restaurants) * 100) if len(filtered_restaurants) > 0 else 0
                st.metric("GPS Coverage", f"{coverage_pct:.1f}%")

    with tab9:
        st.header("💬 Customer Reviews")

        # Load both Trustpilot and Google data
        trustpilot_reviews_df = load_trustpilot_reviews()
        trustpilot_summary_df = load_trustpilot_summary()
        google_reviews_df = load_google_reviews()
        google_summary_df = load_google_summary()

        # Combine reviews from both sources
        if not trustpilot_reviews_df.empty and not google_reviews_df.empty:
            # Add source column and standardize columns
            trustpilot_reviews_df['source'] = 'Trustpilot'
            trustpilot_reviews_df['source_url'] = trustpilot_reviews_df['trustpilot_url']

            google_reviews_df['source'] = 'Google'
            google_reviews_df['source_url'] = google_reviews_df['google_author_url']
            google_reviews_df['review_title'] = ''  # Google doesn't have titles
            google_reviews_df['review_body'] = google_reviews_df['review_text']
            # Add Trustpilot-specific columns to Google reviews (with defaults)
            google_reviews_df['author_location'] = None
            google_reviews_df['is_verified_purchase'] = False
            google_reviews_df['helpful_count'] = 0

            # Select common columns
            common_cols = ['restaurant_id', 'restaurant_name', 'review_date', 'author_name',
                          'review_title', 'review_body', 'rating', 'source', 'source_url',
                          'hygiene_rating', 'cuisine_type', 'price_range',
                          'author_location', 'is_verified_purchase', 'helpful_count']

            reviews_df = pd.concat([
                trustpilot_reviews_df[common_cols],
                google_reviews_df[common_cols]
            ], ignore_index=True).sort_values('review_date', ascending=False)
        elif not trustpilot_reviews_df.empty:
            trustpilot_reviews_df['source'] = 'Trustpilot'
            reviews_df = trustpilot_reviews_df
        elif not google_reviews_df.empty:
            google_reviews_df['source'] = 'Google'
            google_reviews_df['review_title'] = ''
            google_reviews_df['review_body'] = google_reviews_df['review_text']
            google_reviews_df['author_location'] = None
            google_reviews_df['is_verified_purchase'] = False
            google_reviews_df['helpful_count'] = 0
            reviews_df = google_reviews_df
        else:
            reviews_df = pd.DataFrame()

        if reviews_df.empty:
            st.info("📊 No reviews have been collected yet.")
            st.markdown("""
            **To collect reviews:**
            - **Trustpilot**: Run `python fetch_trustpilot_reviews.py --all`
            - **Google**: Run `python fetch_google_reviews.py --all`

            See documentation for details.
            """)
        else:
            # Overview metrics
            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                total_reviews = len(reviews_df)
                st.metric("Total Reviews", f"{total_reviews:,}")

            with col2:
                trustpilot_count = len(reviews_df[reviews_df['source'] == 'Trustpilot'])
                st.metric("Trustpilot Reviews", f"{trustpilot_count:,}")

            with col3:
                google_count = len(reviews_df[reviews_df['source'] == 'Google'])
                st.metric("Google Reviews", f"{google_count:,}")

            with col4:
                avg_rating = reviews_df['rating'].mean()
                st.metric("Overall Avg Rating", f"{avg_rating:.2f}/5")

            with col5:
                # Reviews in last 30 days
                thirty_days_ago = pd.Timestamp.now() - pd.Timedelta(days=30)
                recent_reviews = reviews_df[reviews_df['review_date'] >= thirty_days_ago]
                st.metric("Recent (30 Days)", len(recent_reviews))

            # Source breakdown
            st.markdown("---")
            col1, col2, col3 = st.columns(3)

            with col1:
                st.subheader("📊 Review Sources")
                trustpilot_avg = reviews_df[reviews_df['source'] == 'Trustpilot']['rating'].mean() if trustpilot_count > 0 else 0
                google_avg = reviews_df[reviews_df['source'] == 'Google']['rating'].mean() if google_count > 0 else 0
                st.markdown(f"""
                - 💚 **Trustpilot**: {trustpilot_count:,} reviews (Avg: {trustpilot_avg:.2f}/5)
                - 🔍 **Google**: {google_count:,} reviews (Avg: {google_avg:.2f}/5)
                """)

            with col2:
                st.subheader("🏪 Restaurant Coverage")
                trustpilot_restaurants = len(trustpilot_reviews_df['restaurant_id'].unique()) if not trustpilot_reviews_df.empty else 0
                google_restaurants = len(google_reviews_df['restaurant_id'].unique()) if not google_reviews_df.empty else 0
                st.markdown(f"""
                - 💚 **Trustpilot**: {trustpilot_restaurants} restaurants
                - 🔍 **Google**: {google_restaurants} restaurants
                """)

            with col3:
                st.subheader("📈 Key Insights")
                if trustpilot_count > 0 and google_count > 0:
                    rating_diff = google_avg - trustpilot_avg
                    if rating_diff > 0.5:
                        st.success(f"✓ Google reviews are {rating_diff:.2f} stars higher on average")
                    elif rating_diff < -0.5:
                        st.warning(f"⚠ Trustpilot reviews are {abs(rating_diff):.2f} stars higher")
                    else:
                        st.info("~ Both sources show similar ratings")

            st.markdown("---")

            # Recent Reviews Feed
            st.subheader("📝 Recent Reviews")

            # Filter controls
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                source_filter = st.selectbox(
                    "Filter by Source",
                    options=["All", "Trustpilot", "Google"]
                )

            with col2:
                restaurant_filter = st.selectbox(
                    "Filter by Restaurant",
                    options=["All"] + sorted(reviews_df['restaurant_name'].unique().tolist())
                )

            with col3:
                rating_filter = st.selectbox(
                    "Filter by Rating",
                    options=["All", "5 Stars", "4 Stars", "3 Stars", "2 Stars", "1 Star"]
                )

            with col4:
                show_count = st.slider("Number of reviews to show", 5, 100, 20)

            # Apply filters
            filtered_reviews = reviews_df.copy()

            if source_filter != "All":
                filtered_reviews = filtered_reviews[filtered_reviews['source'] == source_filter]

            if restaurant_filter != "All":
                filtered_reviews = filtered_reviews[filtered_reviews['restaurant_name'] == restaurant_filter]

            if rating_filter != "All":
                rating_value = int(rating_filter.split()[0])
                filtered_reviews = filtered_reviews[filtered_reviews['rating'] == rating_value]

            # Display reviews (show all if filtered, otherwise use slider limit)
            if source_filter != "All" or restaurant_filter != "All" or rating_filter != "All":
                # When filtering, show all matching reviews
                reviews_to_display = filtered_reviews
                if len(reviews_to_display) > 0:
                    st.caption(f"Showing all {len(reviews_to_display)} matching reviews")
            else:
                # When showing all, use slider limit
                reviews_to_display = filtered_reviews.head(show_count)
                st.caption(f"Showing {len(reviews_to_display)} of {len(filtered_reviews)} total reviews")

            # Display reviews
            for idx, review in reviews_to_display.iterrows():
                with st.container():
                    col1, col2 = st.columns([3, 1])

                    with col1:
                        # Restaurant name, source badge, and rating
                        source_badge = "💚 Trustpilot" if review['source'] == 'Trustpilot' else "🔍 Google"
                        st.markdown(f"**{review['restaurant_name']}** • {source_badge}")

                        if review['source'] == 'Trustpilot':
                            st.markdown(format_trustpilot_rating(review['rating'], include_text=True), unsafe_allow_html=True)
                        else:
                            st.markdown(format_google_rating(review['rating'], include_text=True), unsafe_allow_html=True)

                    with col2:
                        # Date and author
                        st.caption(f"📅 {review['review_date'].strftime('%Y-%m-%d')}")
                        st.caption(f"👤 {review['author_name']}")

                    # Review title
                    if review['review_title']:
                        st.markdown(f"**{review['review_title']}**")

                    # Review body
                    body = review['review_body']
                    if len(body) > 300:
                        with st.expander("Read more..."):
                            st.write(body)
                        st.write(body[:300] + "...")
                    else:
                        st.write(body)

                    # Metadata
                    metadata_parts = []
                    if pd.notna(review['author_location']):
                        metadata_parts.append(f"📍 {review['author_location']}")
                    if review['is_verified_purchase']:
                        metadata_parts.append("✓ Verified")
                    if review['helpful_count'] > 0:
                        metadata_parts.append(f"👍 {review['helpful_count']} helpful")

                    if metadata_parts:
                        st.caption(" • ".join(metadata_parts))

                    st.markdown("---")

            st.markdown("---")

            # Rating Distribution
            st.subheader("📊 Rating Distribution")

            col1, col2 = st.columns(2)

            with col1:
                # Bar chart
                rating_counts = reviews_df['rating'].value_counts().sort_index()
                fig = px.bar(
                    x=rating_counts.index,
                    y=rating_counts.values,
                    labels={'x': 'Rating (Stars)', 'y': 'Number of Reviews'},
                    title="Reviews by Rating",
                    color=rating_counts.index,
                    color_continuous_scale='RdYlGn'
                )
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, width="stretch")

            with col2:
                # Pie chart
                fig = px.pie(
                    values=rating_counts.values,
                    names=[f"{r}★" for r in rating_counts.index],
                    title="Rating Proportion",
                    color_discrete_sequence=['#FF3722', '#FF8622', '#FFCE00', '#73CF11', '#00B67A']
                )
                st.plotly_chart(fig, width="stretch")

            st.markdown("---")

            # Restaurants by Review Count and Rating
            st.subheader("🏪 Restaurants by Reviews")

            if not trustpilot_summary_df.empty:
                # Filter to restaurants with reviews
                summary_with_reviews = trustpilot_summary_df[trustpilot_summary_df['actual_review_count'] > 0].copy()

                if not summary_with_reviews.empty:
                    # Display table
                    display_df = summary_with_reviews[[
                        'name', 'calculated_avg_rating', 'actual_review_count',
                        'newest_review_date', 'trustpilot_url'
                    ]].copy()

                    display_df.columns = ['Restaurant', 'Avg Rating', 'Review Count',
                                         'Latest Review', 'Trustpilot URL']

                    # Format rating column
                    display_df['Avg Rating'] = display_df['Avg Rating'].apply(
                        lambda x: f"{x:.2f}/5" if pd.notna(x) else "N/A"
                    )

                    # Format date
                    display_df['Latest Review'] = pd.to_datetime(display_df['Latest Review']).dt.strftime('%Y-%m-%d')

                    # Make URL clickable
                    display_df['Trustpilot URL'] = display_df['Trustpilot URL'].apply(
                        lambda x: f"[View]({x})" if pd.notna(x) else ""
                    )

                    st.dataframe(
                        display_df,
                        width="stretch",
                        hide_index=True
                    )

            st.markdown("---")

            # Hygiene vs Trustpilot Correlation
            st.subheader("🔬 Hygiene Rating vs Customer Reviews")

            # Merge hygiene and Trustpilot data
            correlation_df = trustpilot_summary_df.merge(
                restaurants_df[['restaurant_id', 'hygiene_rating']],
                on='restaurant_id',
                how='inner'
            )

            # Filter to restaurants with both ratings
            correlation_df = correlation_df[
                (correlation_df['actual_review_count'] > 0) &
                (correlation_df['hygiene_rating'].notna())
            ]

            if not correlation_df.empty:
                fig = px.scatter(
                    correlation_df,
                    x='hygiene_rating',
                    y='calculated_avg_rating',
                    size='actual_review_count',
                    hover_data=['name'],
                    labels={
                        'hygiene_rating': 'FSA Hygiene Rating (0-5)',
                        'calculated_avg_rating': 'Trustpilot Rating (1-5)',
                        'name': 'Restaurant'
                    },
                    title="Does Food Safety Predict Customer Satisfaction?",
                    color='calculated_avg_rating',
                    color_continuous_scale='RdYlGn'
                )

                fig.update_layout(
                    xaxis=dict(range=[0, 5.5]),
                    yaxis=dict(range=[0, 5.5])
                )

                st.plotly_chart(fig, width="stretch")

                # Calculate correlation
                if len(correlation_df) > 2:
                    corr = correlation_df['hygiene_rating'].corr(correlation_df['calculated_avg_rating'])
                    st.info(f"📈 Correlation coefficient: {corr:.3f}")

                    if corr > 0.5:
                        st.success("✓ Strong positive correlation: Better hygiene ratings tend to have better customer reviews!")
                    elif corr > 0.3:
                        st.info("~ Moderate correlation: Some relationship between hygiene and customer satisfaction.")
                    elif corr < 0:
                        st.warning("⚠️ Negative correlation: Interesting! This might warrant further investigation.")
                    else:
                        st.info("~ Weak correlation: Hygiene ratings and customer reviews appear independent.")
            else:
                st.info("Not enough restaurants with both hygiene ratings and Trustpilot reviews to show correlation.")

            # Attribution
            st.markdown("---")
            st.caption("💚 Trustpilot data from [Trustpilot.com](https://www.trustpilot.com) • 🔍 Google data from [Google Places API](https://developers.google.com/maps/documentation/places/web-service/overview) • For internal research use only")

    # ------------------------------------------------------------------------
    # ------------------------------------------------------------------------
    # Tab 9: Reviews (Trustpilot + Google)
    # ------------------------------------------------------------------------
    # (content already added above)

    # ------------------------------------------------------------------------
    # Tab 10: Statistics
    # ------------------------------------------------------------------------
    with tab10:
        st.header("Database Statistics")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📊 Overall Statistics")
            st.metric("Total Restaurants", len(restaurants_df))
            st.metric("Total Menu Items", len(menu_df))
            st.metric("Unique Categories", menu_df['category'].nunique())
            st.metric("Unique Dietary Tags", len(all_dietary_tags))

            if not menu_df['price_gbp'].isna().all():
                st.metric("Lowest Price", f"£{menu_df['price_gbp'].min():.2f}")
                st.metric("Highest Price", f"£{menu_df['price_gbp'].max():.2f}")
                st.metric("Average Price", f"£{menu_df['price_gbp'].mean():.2f}")

        with col2:
            st.subheader("🔍 Data Source Summary")

            # Count real vs synthetic data
            real_count = (restaurants_df['data_source'] == 'real_scraped').sum()
            synthetic_count = (restaurants_df['data_source'] == 'synthetic').sum()

            col_real, col_synth = st.columns(2)
            with col_real:
                st.metric("✓ Real Data", real_count, help="Restaurants with actual scraped menu data")
            with col_synth:
                st.metric("⚠ Synthetic Data", synthetic_count, help="Restaurants with test/demonstration data")

            # Show real data restaurants
            if real_count > 0:
                st.markdown("**Restaurants with Real Data:**")
                real_restaurants = restaurants_df[restaurants_df['data_source'] == 'real_scraped'][['name', 'scraping_method']].copy()
                real_restaurants.columns = ['Restaurant Name', 'Scraping Method']
                st.dataframe(
                    real_restaurants,
                    hide_index=True,
                    width="stretch"
                )

            st.subheader("🏪 Restaurant Details")
            # Create display dataframe with formatted dates
            display_df = restaurants_df[['name', 'cuisine_type', 'price_range', 'scraped_at', 'data_source']].copy()
            display_df['scraped_at'] = pd.to_datetime(display_df['scraped_at'], format='ISO8601').dt.strftime('%Y-%m-%d')
            display_df['data_source'] = display_df['data_source'].apply(lambda x: '✓ Real' if x == 'real_scraped' else '⚠ Synthetic')
            display_df.columns = ['Restaurant', 'Cuisine', 'Price Range', 'Data Collected', 'Data Type']
            st.dataframe(
                display_df,
                hide_index=True,
                width="stretch"
            )

        # Dietary tags distribution
        st.subheader("🥗 Dietary Tag Distribution")
        if not dietary_df.empty:
            tag_counts = dietary_df['tag_name'].value_counts().reset_index()
            tag_counts.columns = ['tag_name', 'count']

            fig_tags = px.pie(
                tag_counts,
                names='tag_name',
                values='count',
                title="Distribution of Dietary Tags Across All Menu Items"
            )
            st.plotly_chart(fig_tags, width="stretch")
        else:
            st.info("No dietary tag data available")

        # Data freshness and sources
        st.subheader("🕐 Data Provenance & Freshness")

        # Create source details table
        source_df = restaurants_df[['name', 'website_url', 'scraped_at']].copy()
        source_df['scraped_at'] = pd.to_datetime(source_df['scraped_at']).dt.strftime('%Y-%m-%d %H:%M')
        source_df.columns = ['Restaurant', 'Data Source', 'Last Updated']

        st.dataframe(
            source_df,
            hide_index=True,
            width="stretch",
            column_config={
                "Data Source": st.column_config.LinkColumn(
                    "Data Source",
                    help="Original source website",
                    max_chars=50
                )
            }
        )

        # Summary info
        latest_update = pd.to_datetime(restaurants_df['last_updated'], format='ISO8601').max()
        oldest_update = pd.to_datetime(restaurants_df['last_updated'], format='ISO8601').min()

        col_x, col_y = st.columns(2)
        with col_x:
            st.info(f"📅 Most recent update: {latest_update.strftime('%Y-%m-%d %H:%M')}")
        with col_y:
            st.info(f"📆 Oldest data: {oldest_update.strftime('%Y-%m-%d %H:%M')}")

        # ------------------------------------------------------------------------
        # Financial Analysis Section
        # ------------------------------------------------------------------------
        st.markdown("---")
        st.header("💰 Financial Analysis")

        # Check if financial data columns exist
        has_financial_data = 'net_assets_gbp' in restaurants_df.columns

        if not has_financial_data:
            st.info("💼 Financial data is not yet available in this deployment. Financial data is fetched from Companies House for UK-registered companies.")
            st.caption("To add financial data, run the `fetch_balance_sheets.py` script to populate the database with Companies House data.")
        else:
            # Filter restaurants with financial data
            financial_df = restaurants_df[restaurants_df['net_assets_gbp'].notna()].copy()

            if len(financial_df) > 0:
                # Overview metrics
                fin_metric_col1, fin_metric_col2, fin_metric_col3, fin_metric_col4 = st.columns(4)

                with fin_metric_col1:
                    st.metric("Companies with Financial Data", len(financial_df))

                with fin_metric_col2:
                    avg_net_assets = financial_df['net_assets_gbp'].mean()
                    if avg_net_assets >= 1_000_000:
                        st.metric("Average Net Assets", f"£{avg_net_assets/1_000_000:.2f}M")
                    elif avg_net_assets >= 1_000:
                        st.metric("Average Net Assets", f"£{avg_net_assets/1_000:.1f}k")
                    else:
                        st.metric("Average Net Assets", f"£{avg_net_assets:,.0f}")

                with fin_metric_col3:
                    companies_with_employees = financial_df[financial_df['employees'].notna() & (financial_df['employees'] > 0)]
                    if len(companies_with_employees) > 0:
                        avg_employees = companies_with_employees['employees'].mean()
                        st.metric("Average Employees", f"{avg_employees:.0f}")
                    else:
                        st.metric("Average Employees", "N/A")

                with fin_metric_col4:
                    total_employees = financial_df['employees'].sum()
                    if pd.notna(total_employees) and total_employees > 0:
                        st.metric("Total Employees", f"{int(total_employees)}")
                    else:
                        st.metric("Total Employees", "N/A")

                st.markdown("")

                # Net Assets Distribution
                st.subheader("📊 Net Assets Distribution")

                # Create bins for net assets
                financial_df['asset_category'] = pd.cut(
                    financial_df['net_assets_gbp'],
                    bins=[-float('inf'), 0, 50000, 100000, 500000, 1000000, float('inf')],
                    labels=['Negative', '£0-50k', '£50k-100k', '£100k-500k', '£500k-1M', '£1M+']
                )

                asset_dist = financial_df['asset_category'].value_counts().sort_index()

                fig_assets = px.bar(
                    x=asset_dist.index.astype(str),
                    y=asset_dist.values,
                    title=f"Net Assets Distribution ({len(financial_df)} companies)",
                    labels={'x': 'Net Assets Range', 'y': 'Number of Companies'},
                    color=asset_dist.values,
                    color_continuous_scale='Blues'
                )
                st.plotly_chart(fig_assets, width="stretch")

                # Two column layout for additional charts
                chart_col1, chart_col2 = st.columns(2)

                with chart_col1:
                    # Employees vs Hygiene Rating
                    st.subheader("👥 Employees vs Hygiene Rating")

                    hygiene_financial = financial_df[
                        (financial_df['hygiene_rating'].notna()) &
                        (financial_df['employees'].notna()) &
                        (financial_df['employees'] > 0)
                    ].copy()

                    if len(hygiene_financial) > 0:
                        # Don't use size parameter - net assets can be negative which causes errors
                        fig_hygiene_emp = px.scatter(
                            hygiene_financial,
                            x='employees',
                            y='hygiene_rating',
                            hover_data=['name', 'net_assets_gbp'],
                            title=f"Employees vs Hygiene Rating ({len(hygiene_financial)} companies)",
                            labels={'employees': 'Number of Employees', 'hygiene_rating': 'Hygiene Rating'},
                            color='hygiene_rating',
                            color_continuous_scale='RdYlGn'
                        )
                        st.plotly_chart(fig_hygiene_emp, width="stretch")
                    else:
                        st.info("Not enough data to show correlation between employees and hygiene ratings.")

                with chart_col2:
                    # Net Assets vs Review Scores
                    st.subheader("💷 Net Assets vs Customer Reviews")

                    review_financial = financial_df[
                        (financial_df['trustpilot_avg_rating'].notna()) |
                        (financial_df['google_avg_rating'].notna())
                    ].copy()

                    if len(review_financial) > 0:
                        # Calculate average rating from available sources
                        review_financial['avg_rating'] = review_financial[['trustpilot_avg_rating', 'google_avg_rating']].mean(axis=1, skipna=True)

                        # Don't use size parameter to avoid NaN issues - show all points equally
                        fig_assets_reviews = px.scatter(
                            review_financial,
                            x='net_assets_gbp',
                            y='avg_rating',
                            hover_data=['name', 'employees'],
                            title=f"Net Assets vs Review Scores ({len(review_financial)} companies)",
                            labels={'net_assets_gbp': 'Net Assets (£)', 'avg_rating': 'Average Rating'},
                            color='avg_rating',
                            color_continuous_scale='RdYlGn'
                        )
                        st.plotly_chart(fig_assets_reviews, width="stretch")
                    else:
                        st.info("Not enough data to show correlation between net assets and review scores.")

                # Top Restaurants Table
                st.subheader("🏆 Top Restaurants by Financial Metrics")

                # Create tabs for different rankings
                rank_tab1, rank_tab2, rank_tab3 = st.tabs(["By Net Assets", "By Employees", "By Total Assets"])

                with rank_tab1:
                    top_assets = financial_df.nlargest(10, 'net_assets_gbp')[
                        ['name', 'net_assets_gbp', 'employees', 'hygiene_rating']
                    ].copy()

                    top_assets['net_assets_gbp'] = top_assets['net_assets_gbp'].apply(
                        lambda x: f"£{x/1_000_000:.2f}M" if x >= 1_000_000 else f"£{x/1_000:.1f}k" if x >= 1_000 else f"£{x:,.0f}"
                    )
                    top_assets['employees'] = top_assets['employees'].apply(
                        lambda x: f"{int(x)}" if pd.notna(x) and x > 0 else "N/A"
                    )
                    top_assets['hygiene_rating'] = top_assets['hygiene_rating'].apply(
                        lambda x: f"{int(x)}★" if pd.notna(x) else "N/A"
                    )

                    top_assets.columns = ['Restaurant', 'Net Assets', 'Employees', 'Hygiene Rating']
                    st.dataframe(top_assets, hide_index=True, width="stretch")

                with rank_tab2:
                    top_employees = financial_df[financial_df['employees'].notna() & (financial_df['employees'] > 0)].nlargest(10, 'employees')[
                        ['name', 'employees', 'net_assets_gbp', 'hygiene_rating']
                    ].copy()

                    if len(top_employees) > 0:
                        top_employees['employees'] = top_employees['employees'].apply(lambda x: f"{int(x)}")
                        top_employees['net_assets_gbp'] = top_employees['net_assets_gbp'].apply(
                            lambda x: f"£{x/1_000_000:.2f}M" if x >= 1_000_000 else f"£{x/1_000:.1f}k" if x >= 1_000 else f"£{x:,.0f}"
                        )
                        top_employees['hygiene_rating'] = top_employees['hygiene_rating'].apply(
                            lambda x: f"{int(x)}★" if pd.notna(x) else "N/A"
                        )

                        top_employees.columns = ['Restaurant', 'Employees', 'Net Assets', 'Hygiene Rating']
                        st.dataframe(top_employees, hide_index=True, width="stretch")
                    else:
                        st.info("No employee data available.")

                with rank_tab3:
                    top_total_assets = financial_df[financial_df['total_assets_gbp'].notna()].nlargest(10, 'total_assets_gbp')[
                        ['name', 'total_assets_gbp', 'net_assets_gbp', 'employees']
                    ].copy()

                    if len(top_total_assets) > 0:
                        top_total_assets['total_assets_gbp'] = top_total_assets['total_assets_gbp'].apply(
                            lambda x: f"£{x/1_000_000:.2f}M" if x >= 1_000_000 else f"£{x/1_000:.1f}k" if x >= 1_000 else f"£{x:,.0f}"
                        )
                        top_total_assets['net_assets_gbp'] = top_total_assets['net_assets_gbp'].apply(
                            lambda x: f"£{x/1_000_000:.2f}M" if x >= 1_000_000 else f"£{x/1_000:.1f}k" if x >= 1_000 else f"£{x:,.0f}"
                        )
                        top_total_assets['employees'] = top_total_assets['employees'].apply(
                            lambda x: f"{int(x)}" if pd.notna(x) and x > 0 else "N/A"
                        )

                        top_total_assets.columns = ['Restaurant', 'Total Assets', 'Net Assets', 'Employees']
                        st.dataframe(top_total_assets, hide_index=True, width="stretch")
                    else:
                        st.info("No total assets data available.")

                # Data quality note
                st.markdown("---")
                st.caption(f"💼 Financial data from Companies House. Coverage: {len(financial_df)}/{len(restaurants_df)} restaurants ({len(financial_df)/len(restaurants_df)*100:.1f}%). Most restaurants file as micro-entities with limited disclosure.")

            else:
                st.info("No financial data available. Financial data is fetched from Companies House for UK-registered companies.")

        # ------------------------------------------------------------------------
        # Address Data Quality Section
        # ------------------------------------------------------------------------
        st.markdown("---")
        st.markdown("")
        st.subheader("📍 Address Data Quality")
        st.markdown("Cross-reference validation of addresses from FSA, scraped data, and Companies House.")

        # Filter restaurants with FSA data
        restaurants_with_fsa = restaurants_df[restaurants_df['fsa_id'].notna()].copy()

        if len(restaurants_with_fsa) == 0:
            st.warning("⚠️ No FSA hygiene data available to validate addresses.")
        else:
            # Helper function for address normalization
            def normalize_address_for_comparison(address):
                if not address or pd.isna(address):
                    return ""
                normalized = str(address).lower()
                normalized = normalized.replace("street", "st").replace("road", "rd").replace("avenue", "ave")
                normalized = normalized.replace("building", "bldg").replace("limited", "ltd").replace("plymouth", "")
                normalized = ''.join(c if c.isalnum() or c.isspace() else ' ' for c in normalized)
                normalized = ' '.join(normalized.split())
                return normalized

            # Helper function for similarity calculation
            def calculate_address_similarity(str1, str2):
                from difflib import SequenceMatcher
                norm1 = normalize_address_for_comparison(str1)
                norm2 = normalize_address_for_comparison(str2)
                if not norm1 or not norm2:
                    return 0.0
                return SequenceMatcher(None, norm1, norm2).ratio()

            # Build FSA address from components
            def build_fsa_full_address(row):
                parts = []
                for col in ['fsa_address_line1', 'fsa_address_line2', 'fsa_address_line3', 'fsa_address_line4', 'fsa_postcode']:
                    if col in row and pd.notna(row[col]) and row[col]:
                        parts.append(str(row[col]))
                return ', '.join(parts)

            # Calculate similarities
            consistency_data = []
            for idx, row in restaurants_with_fsa.iterrows():
                fsa_address = build_fsa_full_address(row)
                scraped_address = row['address'] if pd.notna(row['address']) else ""
                ch_address = row['company_registered_address'] if pd.notna(row.get('company_registered_address')) else ""

                # Calculate similarities
                fsa_vs_scraped = calculate_address_similarity(fsa_address, scraped_address) if fsa_address and scraped_address else 0.0
                fsa_vs_ch = calculate_address_similarity(fsa_address, ch_address) if fsa_address and ch_address else 0.0
                scraped_vs_ch = calculate_address_similarity(scraped_address, ch_address) if scraped_address and ch_address else 0.0

                # Average similarity
                valid_similarities = [s for s in [fsa_vs_scraped, fsa_vs_ch, scraped_vs_ch] if s > 0]
                avg_similarity = sum(valid_similarities) / len(valid_similarities) if valid_similarities else 0.0

                # Categorize
                if avg_similarity >= 0.9:
                    category = "Perfect"
                elif avg_similarity >= 0.7:
                    category = "Good"
                elif avg_similarity >= 0.5:
                    category = "Poor"
                else:
                    category = "Mismatch"

                consistency_data.append({
                    'name': row['name'],
                    'fsa_business_name': row['fsa_business_name'] if pd.notna(row.get('fsa_business_name')) else 'N/A',
                    'company_name': row['company_name'] if pd.notna(row.get('company_name')) else 'N/A',
                    'fsa_address': fsa_address,
                    'scraped_address': scraped_address,
                    'ch_address': ch_address,
                    'fsa_vs_scraped': fsa_vs_scraped,
                    'fsa_vs_ch': fsa_vs_ch,
                    'scraped_vs_ch': scraped_vs_ch,
                    'avg_similarity': avg_similarity,
                    'category': category,
                    'hygiene_rating': row['hygiene_rating'] if pd.notna(row.get('hygiene_rating')) else None
                })

            consistency_df = pd.DataFrame(consistency_data)

            # Overview metrics
            total_checked = len(consistency_df)
            perfect_count = len(consistency_df[consistency_df['category'] == 'Perfect'])
            good_count = len(consistency_df[consistency_df['category'] == 'Good'])
            poor_count = len(consistency_df[consistency_df['category'] == 'Poor'])
            mismatch_count = len(consistency_df[consistency_df['category'] == 'Mismatch'])

            # Display metrics
            addr_col1, addr_col2, addr_col3, addr_col4, addr_col5 = st.columns(5)

            with addr_col1:
                st.metric("Checked", total_checked)

            with addr_col2:
                st.metric("✅ Perfect", f"{perfect_count} ({perfect_count/total_checked*100:.0f}%)")

            with addr_col3:
                st.metric("✓ Good", f"{good_count} ({good_count/total_checked*100:.0f}%)")

            with addr_col4:
                st.metric("⚠️ Poor", f"{poor_count} ({poor_count/total_checked*100:.0f}%)")

            with addr_col5:
                st.metric("❌ Mismatch", f"{mismatch_count} ({mismatch_count/total_checked*100:.0f}%)")

            st.markdown("")

            # Visual distribution
            chart_col1, chart_col2 = st.columns(2)

            with chart_col1:
                category_counts = consistency_df['category'].value_counts()
                category_order = ['Perfect', 'Good', 'Poor', 'Mismatch']
                category_counts = category_counts.reindex(category_order, fill_value=0)

                fig_addr_bar = px.bar(
                    x=category_counts.index,
                    y=category_counts.values,
                    title=f"Address Match Quality Distribution ({total_checked} restaurants)",
                    labels={'x': 'Match Category', 'y': 'Number of Restaurants'},
                    color=category_counts.values,
                    color_continuous_scale=['green', 'lightgreen', 'orange', 'red']
                )
                st.plotly_chart(fig_addr_bar, width='stretch')

            with chart_col2:
                fig_addr_pie = px.pie(
                    values=category_counts.values,
                    names=category_counts.index,
                    title="Address Match Quality Breakdown",
                    color_discrete_sequence=['green', 'lightgreen', 'orange', 'red']
                )
                st.plotly_chart(fig_addr_pie, width='stretch')

            # Problematic restaurants table
            if poor_count + mismatch_count > 0:
                st.markdown("")
                st.subheader("🔍 Restaurants Requiring Review")
                st.markdown(f"Showing {poor_count + mismatch_count} restaurants with address inconsistencies.")

                problematic = consistency_df[consistency_df['category'].isin(['Poor', 'Mismatch'])].copy()
                problematic = problematic.sort_values('avg_similarity')

                # Display as expandable rows
                for idx, row in problematic.iterrows():
                    emoji = "⚠️" if row['category'] == "Poor" else "❌"
                    with st.expander(f"{emoji} {row['name']} ({row['avg_similarity']*100:.0f}% match - {row['category']})"):
                        exp_col1, exp_col2 = st.columns(2)

                        with exp_col1:
                            st.markdown(f"**Our Name:** {row['name']}")
                            st.markdown(f"**FSA Name:** {row['fsa_business_name']}")
                            st.markdown(f"**Company Name:** {row['company_name']}")

                            if pd.notna(row['hygiene_rating']):
                                stars = "⭐" * int(row['hygiene_rating'])
                                st.markdown(f"**Hygiene Rating:** {stars} ({int(row['hygiene_rating'])})")

                        with exp_col2:
                            st.markdown("**Similarity Scores:**")
                            st.markdown(f"FSA ↔ Scraped: {row['fsa_vs_scraped']*100:.0f}%")
                            st.markdown(f"FSA ↔ Companies House: {row['fsa_vs_ch']*100:.0f}%")
                            st.markdown(f"Scraped ↔ Companies House: {row['scraped_vs_ch']*100:.0f}%")
                            st.markdown(f"**Average: {row['avg_similarity']*100:.0f}%**")

                        st.markdown("**Addresses:**")
                        st.markdown(f"**FSA:** {row['fsa_address']}")
                        st.markdown(f"**Scraped:** {row['scraped_address'] if row['scraped_address'] else 'N/A'}")
                        st.markdown(f"**Companies House:** {row['ch_address'] if row['ch_address'] else 'N/A'}")

            # Download option
            st.markdown("")
            csv_data = consistency_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Full Address Consistency Report (CSV)",
                data=csv_data,
                file_name="address_consistency_report.csv",
                mime="text/csv"
            )

            st.caption("💡 Perfect (≥90%), Good (70-89%), Poor (50-69%), Mismatch (<50%). Lower scores may indicate incorrect FSA matches or address data issues.")

        # ============================================================
        # Licensing Data Statistics
        # ============================================================
        st.markdown("---")
        st.markdown("### 📜 Licensing Data Coverage")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            licensed_count = restaurants_df['licensing_number'].notna().sum()
            st.metric("Licensed Restaurants", licensed_count)

        with col2:
            license_coverage = (licensed_count / len(restaurants_df) * 100) if len(restaurants_df) > 0 else 0
            st.metric("License Coverage", f"{license_coverage:.1f}%")

        with col3:
            import json
            avg_hours = 0
            hours_count = 0
            for hours_json in restaurants_df[restaurants_df['licensing_opening_hours'].notna()]['licensing_opening_hours']:
                if hours_json and hours_json != '[]':
                    try:
                        hours = json.loads(hours_json)
                        avg_hours += len(hours)
                        hours_count += 1
                    except:
                        pass
            avg_hours = avg_hours / hours_count if hours_count > 0 else 0
            st.metric("Avg Opening Periods", f"{avg_hours:.1f}")

        with col4:
            alcohol_licenses = 0
            for activities_json in restaurants_df[restaurants_df['licensing_activities'].notna()]['licensing_activities']:
                if activities_json and 'alcohol' in str(activities_json).lower():
                    alcohol_licenses += 1
            st.metric("Alcohol Licenses", alcohol_licenses)

        st.caption("Licensing data from Plymouth City Council Licensing Register. Unmatched restaurants available in unmatched_licensing.json for manual review.")

    # ------------------------------------------------------------------------
    # Tab 8: Restaurant Profiles
    # ------------------------------------------------------------------------
    with tab8:
        st.header("🏢 Restaurant Profiles")
        st.markdown("View comprehensive details for each restaurant including menu, reviews, hygiene ratings, and location.")

        # Restaurant selector
        restaurant_names = sorted(restaurants_df['name'].unique())

        # Check if a restaurant was selected from another tab (e.g., Hygiene Ratings)
        if 'selected_restaurant_profile' in st.session_state and st.session_state['selected_restaurant_profile'] in restaurant_names:
            default_restaurant = st.session_state['selected_restaurant_profile']
            # Clear session state after using it
            del st.session_state['selected_restaurant_profile']
        else:
            # Default to Honky Tonk Wine Library if it exists
            default_restaurant = "Honky Tonk Wine Library"

        default_index = restaurant_names.index(default_restaurant) if default_restaurant in restaurant_names else 0

        # Pre-load all reviews once (cached, outside selection block for better performance)
        all_trustpilot = load_trustpilot_reviews()
        all_google = load_google_reviews()

        selected_restaurant = st.selectbox(
            "Select a Restaurant",
            restaurant_names,
            index=default_index,
            help="Choose a restaurant to view its detailed profile",
            key="restaurant_profile_selector"
        )

        if selected_restaurant:
            # Get restaurant data
            restaurant = restaurants_df[restaurants_df['name'] == selected_restaurant].iloc[0]
            restaurant_id = int(restaurant['restaurant_id'])  # Convert numpy.int64 to Python int

            # Filter data for selected restaurant (fast operations on cached data)
            # Use restaurant_id for numeric filtering (much faster than string comparison)
            restaurant_menu = menu_df[menu_df['restaurant_id'] == restaurant_id]
            trustpilot_reviews = all_trustpilot[all_trustpilot['restaurant_id'] == restaurant_id].head(10)
            google_reviews = all_google[all_google['restaurant_id'] == restaurant_id].head(10)

            # ================================================================
            # Header Section
            # ================================================================
            st.markdown(f"## {restaurant['name']}")

            # Status and badges row
            badge_html = []

            # Hygiene badge
            if pd.notna(restaurant.get('hygiene_rating')):
                rating = int(restaurant['hygiene_rating'])
                colors = {5: '#00AA00', 4: '#55CC00', 3: '#FFAA00', 2: '#FF6600', 1: '#CC0000', 0: '#990000'}
                color = colors.get(rating, '#CCCCCC')
                badge_html.append(
                    f'<span style="background: {color}; color: white; padding: 4px 12px; border-radius: 4px; font-weight: bold; margin-right: 8px;">Hygiene: {rating}★</span>'
                )

            # Business status badge
            if pd.notna(restaurant.get('google_business_status')):
                status = restaurant['google_business_status']
                if status == 'OPERATIONAL':
                    badge_html.append('<span style="background: #E8F5E9; color: #2E7D32; padding: 4px 12px; border-radius: 4px; font-weight: bold; margin-right: 8px;">✓ Open</span>')
                elif status == 'CLOSED_TEMPORARILY':
                    badge_html.append('<span style="background: #FFF3E0; color: #E65100; padding: 4px 12px; border-radius: 4px; font-weight: bold; margin-right: 8px;">⚠ Temporarily Closed</span>')
                elif status == 'CLOSED_PERMANENTLY':
                    badge_html.append('<span style="background: #FFEBEE; color: #C62828; padding: 4px 12px; border-radius: 4px; font-weight: bold; margin-right: 8px;">✗ Permanently Closed</span>')

            # Price range badge
            if pd.notna(restaurant.get('price_range')):
                badge_html.append(
                    f'<span style="background: #E3F2FD; color: #1565C0; padding: 4px 12px; border-radius: 4px; font-weight: bold; margin-right: 8px;">{restaurant["price_range"]}</span>'
                )

            # Cuisine badge
            if pd.notna(restaurant.get('cuisine_type')):
                badge_html.append(
                    f'<span style="background: #F3E5F5; color: #6A1B9A; padding: 4px 12px; border-radius: 4px; font-weight: bold;">{restaurant["cuisine_type"]}</span>'
                )

            if badge_html:
                st.markdown(' '.join(badge_html), unsafe_allow_html=True)

            st.markdown("---")

            # ================================================================
            # Quick Stats
            # ================================================================
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Menu Items", len(restaurant_menu))

            with col2:
                if pd.notna(restaurant.get('google_rating')):
                    st.metric("Google Rating", f"{restaurant['google_rating']:.1f}⭐")
                else:
                    st.metric("Google Rating", "N/A")

            with col3:
                if pd.notna(restaurant.get('trustpilot_avg_rating')):
                    st.metric("Trustpilot Rating", f"{restaurant['trustpilot_avg_rating']:.1f}⭐")
                else:
                    st.metric("Trustpilot Rating", "N/A")

            with col4:
                total_reviews = 0
                if pd.notna(restaurant.get('trustpilot_review_count')):
                    total_reviews += int(restaurant['trustpilot_review_count'])
                if pd.notna(restaurant.get('google_review_count')):
                    total_reviews += int(restaurant['google_review_count'])
                st.metric("Total Reviews", total_reviews)

            # ================================================================
            # Contact & Location Section
            # ================================================================
            st.subheader("📍 Contact & Location")

            col_left, col_right = st.columns(2)

            with col_left:
                # Address
                if pd.notna(restaurant.get('address')):
                    st.markdown(f"**Address:** {restaurant['address']}")
                elif pd.notna(restaurant.get('google_formatted_address')):
                    st.markdown(f"**Address:** {restaurant['google_formatted_address']}")

                # Phone
                if pd.notna(restaurant.get('google_phone_national')):
                    phone = restaurant['google_phone_national']
                    st.markdown(f"**Phone:** [{phone}](tel:{phone})")

                # Website
                website = restaurant.get('google_website_url') or restaurant.get('website_url')
                if pd.notna(website):
                    st.markdown(f"**Website:** [{website}]({website})")

            with col_right:
                # Google Maps link
                if pd.notna(restaurant.get('google_maps_url')):
                    st.markdown(f"[📍 View on Google Maps]({restaurant['google_maps_url']})")

                # Coordinates
                if pd.notna(restaurant.get('google_latitude')) and pd.notna(restaurant.get('google_longitude')):
                    st.markdown(f"**Coordinates:** {restaurant['google_latitude']:.6f}, {restaurant['google_longitude']:.6f}")

                # Trustpilot link
                if pd.notna(restaurant.get('trustpilot_url')):
                    st.markdown(f"[⭐ View on Trustpilot]({restaurant['trustpilot_url']})")

            # ================================================================
            # Service Options Section
            # ================================================================
            st.subheader("🍽️ Service Options")

            service_badges = []
            if restaurant.get('google_dine_in') == 1:
                service_badges.append("🍽️ Dine-in")
            if restaurant.get('google_takeout') == 1:
                service_badges.append("🥡 Takeout")
            if restaurant.get('google_delivery') == 1:
                service_badges.append("🚚 Delivery")
            if restaurant.get('google_reservable') == 1:
                service_badges.append("📅 Reservations")
            if restaurant.get('google_serves_breakfast') == 1:
                service_badges.append("🍳 Breakfast")
            if restaurant.get('google_serves_lunch') == 1:
                service_badges.append("🍴 Lunch")
            if restaurant.get('google_serves_dinner') == 1:
                service_badges.append("🍷 Dinner")
            if restaurant.get('google_serves_vegetarian') == 1:
                service_badges.append("🥗 Vegetarian")
            if restaurant.get('google_serves_beer') == 1:
                service_badges.append("🍺 Beer")
            if restaurant.get('google_serves_wine') == 1:
                service_badges.append("🍷 Wine")

            if service_badges:
                badges_html = " ".join([
                    f"<span style='background: #E8F5E9; color: #2E7D32; padding: 6px 12px; border-radius: 4px; font-size: 0.9em; margin-right: 8px; display: inline-block; margin-bottom: 8px;'>{badge}</span>"
                    for badge in service_badges
                ])
                st.markdown(badges_html, unsafe_allow_html=True)
            else:
                st.info("No service information available")

            # ================================================================
            # FSA Food Hygiene Data Section
            # ================================================================
            if pd.notna(restaurant.get('fsa_id')):
                st.subheader("🔍 FSA Food Hygiene Data")

                fsa_col1, fsa_col2 = st.columns(2)

                with fsa_col1:
                    # FSA Business Name
                    if pd.notna(restaurant.get('fsa_business_name')):
                        st.markdown(f"**FSA Business Name:** {restaurant['fsa_business_name']}")

                    # FSA Address
                    fsa_address_parts = []
                    if pd.notna(restaurant.get('fsa_address_line1')):
                        fsa_address_parts.append(restaurant['fsa_address_line1'])
                    if pd.notna(restaurant.get('fsa_address_line2')):
                        fsa_address_parts.append(restaurant['fsa_address_line2'])
                    if pd.notna(restaurant.get('fsa_address_line3')):
                        fsa_address_parts.append(restaurant['fsa_address_line3'])
                    if pd.notna(restaurant.get('fsa_address_line4')):
                        fsa_address_parts.append(restaurant['fsa_address_line4'])
                    if pd.notna(restaurant.get('fsa_postcode')):
                        fsa_address_parts.append(restaurant['fsa_postcode'])

                    if fsa_address_parts:
                        fsa_full_address = ", ".join(fsa_address_parts)
                        st.markdown(f"**FSA Address:** {fsa_full_address}")

                    # FSA GPS Coordinates
                    if pd.notna(restaurant.get('fsa_latitude')) and pd.notna(restaurant.get('fsa_longitude')):
                        lat = restaurant['fsa_latitude']
                        lon = restaurant['fsa_longitude']
                        st.markdown(f"**FSA GPS:** {lat:.6f}, {lon:.6f}")
                        # Google Maps link using FSA coordinates
                        maps_link = f"https://www.google.com/maps?q={lat},{lon}"
                        st.markdown(f"[🗺️ View FSA Location on Map]({maps_link})")

                with fsa_col2:
                    # Rating Key
                    if pd.notna(restaurant.get('fsa_rating_key')):
                        st.markdown(f"**Rating Key:** `{restaurant['fsa_rating_key']}`")

                    # Scheme Type
                    if pd.notna(restaurant.get('fsa_scheme_type')):
                        st.markdown(f"**Scheme:** {restaurant['fsa_scheme_type']}")

                    # New Rating Pending
                    if pd.notna(restaurant.get('fsa_new_rating_pending')):
                        pending = restaurant['fsa_new_rating_pending']
                        if pending == 'True' or pending == '1':
                            st.warning("⏳ **New rating pending** - Re-inspection scheduled")
                        else:
                            st.success("✓ **No pending inspection**")

                    # Local Authority Website
                    if pd.notna(restaurant.get('fsa_local_authority_website')):
                        la_website = restaurant['fsa_local_authority_website']
                        st.markdown(f"[🏛️ Local Authority Website]({la_website})")

                    # Local Authority Business ID
                    if pd.notna(restaurant.get('fsa_local_authority_business_id')):
                        st.markdown(f"**LA Business ID:** {restaurant['fsa_local_authority_business_id']}")

            # ================================================================
            # Menu Summary Section
            # ================================================================
            st.subheader("📋 Menu Summary")

            if not restaurant_menu.empty and len(restaurant_menu.columns) > 0:
                col_a, col_b, col_c, col_d = st.columns(4)

                with col_a:
                    st.metric("Total Items", len(restaurant_menu))

                with col_b:
                    if 'category' in restaurant_menu.columns:
                        categories = restaurant_menu['category'].nunique()
                        st.metric("Categories", categories)
                    else:
                        st.metric("Categories", "N/A")

                with col_c:
                    if 'price_gbp' in restaurant_menu.columns and not restaurant_menu['price_gbp'].isna().all():
                        avg_price = restaurant_menu['price_gbp'].mean()
                        st.metric("Avg Price", f"£{avg_price:.2f}")
                    else:
                        st.metric("Avg Price", "N/A")

                with col_d:
                    if 'is_vegetarian' in restaurant_menu.columns:
                        vegetarian = (restaurant_menu['is_vegetarian'] == 1).sum()
                        st.metric("Vegetarian", vegetarian)
                    else:
                        st.metric("Vegetarian", "N/A")

                # Menu items by category
                if 'category' in restaurant_menu.columns and not restaurant_menu['category'].isna().all():
                    st.markdown("**Menu Items by Category**")
                    category_counts = restaurant_menu['category'].value_counts().reset_index()
                    category_counts.columns = ['category', 'count']

                    fig_categories = px.bar(
                        category_counts,
                        x='category',
                        y='count',
                        title=f"Menu Categories at {selected_restaurant}",
                        labels={'category': 'Category', 'count': 'Number of Items'},
                        color='count',
                        color_continuous_scale='Blues'
                    )
                    st.plotly_chart(fig_categories, width="stretch")

                # Price distribution
                if 'price_gbp' in restaurant_menu.columns and not restaurant_menu['price_gbp'].isna().all():
                    st.markdown("**Price Distribution**")
                    fig_price = px.histogram(
                        restaurant_menu[restaurant_menu['price_gbp'].notna()],
                        x='price_gbp',
                        nbins=20,
                        title=f"Price Distribution at {selected_restaurant}",
                        labels={'price_gbp': 'Price (£)', 'count': 'Number of Items'},
                        color_discrete_sequence=['#1f77b4']
                    )
                    st.plotly_chart(fig_price, width="stretch")

                # Dietary options summary
                if 'is_vegetarian' in restaurant_menu.columns or 'is_vegan' in restaurant_menu.columns or 'is_gluten_free' in restaurant_menu.columns:
                    st.markdown("**Dietary Options**")
                    dietary_col1, dietary_col2, dietary_col3 = st.columns(3)
                    with dietary_col1:
                        if 'is_vegetarian' in restaurant_menu.columns:
                            veg_count = (restaurant_menu['is_vegetarian'] == 1).sum()
                            veg_pct = (veg_count / len(restaurant_menu) * 100) if len(restaurant_menu) > 0 else 0
                            st.metric("🥬 Vegetarian", f"{veg_count} ({veg_pct:.0f}%)")
                        else:
                            st.metric("🥬 Vegetarian", "N/A")
                    with dietary_col2:
                        if 'is_vegan' in restaurant_menu.columns:
                            vegan_count = (restaurant_menu['is_vegan'] == 1).sum()
                            vegan_pct = (vegan_count / len(restaurant_menu) * 100) if len(restaurant_menu) > 0 else 0
                            st.metric("🌱 Vegan", f"{vegan_count} ({vegan_pct:.0f}%)")
                        else:
                            st.metric("🌱 Vegan", "N/A")
                    with dietary_col3:
                        if 'is_gluten_free' in restaurant_menu.columns:
                            gf_count = (restaurant_menu['is_gluten_free'] == 1).sum()
                            gf_pct = (gf_count / len(restaurant_menu) * 100) if len(restaurant_menu) > 0 else 0
                            st.metric("🌾 Gluten-Free", f"{gf_count} ({gf_pct:.0f}%)")
                        else:
                            st.metric("🌾 Gluten-Free", "N/A")

            else:
                st.info("No menu items available for this restaurant. This restaurant was discovered via Google Places but menu data has not been scraped yet.")

            # ================================================================
            # Reviews Section
            # ================================================================
            st.markdown("---")
            st.subheader("💬 Customer Reviews")

            # Review sources tabs - Google first, then Trustpilot
            if not trustpilot_reviews.empty or not google_reviews.empty:
                review_tab1, review_tab2 = st.tabs(["Google Reviews", "Trustpilot Reviews"])

                with review_tab1:
                    if not google_reviews.empty:
                        st.markdown(f"**Latest {len(google_reviews)} Google Reviews**")
                        for _, review in google_reviews.iterrows():
                            with st.expander(f"{'⭐' * review['rating']} - {review['author_name']} ({review['review_date']})"):
                                st.markdown(review['review_text'])
                                if pd.notna(review.get('relative_time_description')):
                                    st.caption(f"Posted: {review['relative_time_description']}")
                    else:
                        st.info("No Google reviews available for this restaurant")

                with review_tab2:
                    if not trustpilot_reviews.empty:
                        st.markdown(f"**Latest {len(trustpilot_reviews)} Trustpilot Reviews**")
                        for _, review in trustpilot_reviews.iterrows():
                            with st.expander(f"{'⭐' * review['rating']} - {review['author_name']} ({review['review_date']})"):
                                if pd.notna(review.get('review_title')):
                                    st.markdown(f"**{review['review_title']}**")
                                st.markdown(review['review_body'])
                                if pd.notna(review.get('author_location')):
                                    st.caption(f"Location: {review['author_location']}")
                    else:
                        st.info("No Trustpilot reviews available for this restaurant")
            else:
                st.info("No reviews available for this restaurant")

            # ================================================================
            # Hygiene Rating Section
            # ================================================================
            if pd.notna(restaurant.get('hygiene_rating')):
                st.subheader("⭐ Food Hygiene Rating")

                hygiene_col1, hygiene_col2 = st.columns([1, 2])

                with hygiene_col1:
                    rating = int(restaurant['hygiene_rating'])
                    st.markdown(f"### {rating}★ / 5★")
                    if pd.notna(restaurant.get('hygiene_rating_date')):
                        rating_date = pd.to_datetime(restaurant['hygiene_rating_date'], format='ISO8601')
                        st.caption(f"Inspected: {rating_date.strftime('%Y-%m-%d')}")

                with hygiene_col2:
                    st.markdown("**Detailed Scores** (lower is better)")
                    score_data = []
                    if pd.notna(restaurant.get('hygiene_score_hygiene')):
                        score_data.append({'Category': 'Hygiene', 'Score': restaurant['hygiene_score_hygiene'], 'Max': 25})
                    if pd.notna(restaurant.get('hygiene_score_structural')):
                        score_data.append({'Category': 'Structural', 'Score': restaurant['hygiene_score_structural'], 'Max': 25})
                    if pd.notna(restaurant.get('hygiene_score_confidence')):
                        score_data.append({'Category': 'Confidence in Management', 'Score': restaurant['hygiene_score_confidence'], 'Max': 30})

                    if score_data:
                        score_df = pd.DataFrame(score_data)
                        st.dataframe(score_df, hide_index=True, width="stretch")

            # ================================================================
            # Licensing Information Section
            # ================================================================
            if pd.notna(restaurant.get('licensing_number')):
                st.markdown("---")
                st.subheader("📜 Licensing Information")

                lic_col1, lic_col2 = st.columns(2)

                with lic_col1:
                    st.markdown("**License Details**")
                    st.markdown(f"**License Number**: {restaurant['licensing_number']}")

                    if pd.notna(restaurant.get('licensing_premises_id')):
                        st.markdown(f"**Premises ID**: {restaurant['licensing_premises_id']}")

                    if pd.notna(restaurant.get('licensing_url')):
                        st.markdown(f"**Official License**: [View on Plymouth Council]({restaurant['licensing_url']})")

                    if pd.notna(restaurant.get('licensing_match_confidence')):
                        confidence = restaurant['licensing_match_confidence'] * 100
                        st.markdown(f"**Match Confidence**: {confidence:.0f}%")

                with lic_col2:
                    st.markdown("**Licensable Activities**")
                    activities_html = format_licensing_activities(
                        restaurant.get('licensing_activities', '[]')
                    )
                    st.markdown(activities_html, unsafe_allow_html=True)

                # Opening Hours (full width)
                st.markdown("**Official Opening Hours**")
                hours_html = format_opening_hours(
                    restaurant.get('licensing_opening_hours', '[]')
                )
                st.markdown(hours_html, unsafe_allow_html=True)

                # Official address
                if pd.notna(restaurant.get('licensing_premises_address')):
                    st.markdown("**Official Registered Address**")
                    st.info(restaurant['licensing_premises_address'])

                # Data attribution
                if pd.notna(restaurant.get('licensing_scraped_at')):
                    scraped_date = pd.to_datetime(restaurant['licensing_scraped_at'], format='ISO8601').strftime('%Y-%m-%d')
                    st.caption(f"Data from Plymouth City Council Licensing Register (Scraped: {scraped_date})")

            # ================================================================
            # Business Rates Section
            # ================================================================
            if pd.notna(restaurant.get('business_rates_rateable_value')):
                st.markdown("---")
                st.subheader("💷 Business Rates Information")

                rates_col1, rates_col2, rates_col3 = st.columns(3)

                with rates_col1:
                    st.metric(
                        label="Rateable Value",
                        value=f"£{int(restaurant['business_rates_rateable_value']):,}",
                        help="Property valuation for business rates calculation"
                    )

                with rates_col2:
                    if pd.notna(restaurant.get('business_rates_net_charge')):
                        annual_charge = float(restaurant['business_rates_net_charge'])
                        st.metric(
                            label="Annual Business Rates (2025-26)",
                            value=f"£{annual_charge:,.0f}",
                            help="Total business rates payable for the year"
                        )
                    else:
                        st.metric(label="Annual Business Rates", value="N/A")

                with rates_col3:
                    if pd.notna(restaurant.get('business_rates_category')):
                        st.markdown("**Property Category**")
                        st.info(restaurant['business_rates_category'])

                # Additional details
                rates_detail_col1, rates_detail_col2 = st.columns(2)

                with rates_detail_col1:
                    if pd.notna(restaurant.get('business_rates_vo_description')):
                        st.markdown("**Valuation Office Description**")
                        st.text(restaurant['business_rates_vo_description'])

                with rates_detail_col2:
                    if pd.notna(restaurant.get('business_rates_address')):
                        st.markdown("**Rates Register Address**")
                        st.text(restaurant['business_rates_address'])

                # Match quality
                if pd.notna(restaurant.get('business_rates_match_score')):
                    match_score = float(restaurant['business_rates_match_score'])
                    st.caption(f"📊 Match Confidence: {match_score:.0f}% | Data from Plymouth Business Rates Register (November 2025)")

            # ================================================================
            # Company Information Section
            # ================================================================
            if pd.notna(restaurant.get('company_number')):
                st.markdown("---")
                st.subheader("🏢 Business Information")

                # Company header with status badge
                company_name = restaurant.get('company_name', 'N/A')
                company_number = restaurant.get('company_number', '')
                company_status = restaurant.get('company_status', 'unknown')

                # Status badge
                if company_status == 'active':
                    status_badge = '<span style="background: #E8F5E9; color: #2E7D32; padding: 4px 12px; border-radius: 4px; font-weight: bold; margin-left: 10px;">✅ Active</span>'
                elif company_status == 'dissolved':
                    status_badge = '<span style="background: #FFEBEE; color: #C62828; padding: 4px 12px; border-radius: 4px; font-weight: bold; margin-left: 10px;">❌ Dissolved</span>'
                else:
                    status_badge = '<span style="background: #FFF3E0; color: #E65100; padding: 4px 12px; border-radius: 4px; font-weight: bold; margin-left: 10px;">⚠ Unknown</span>'

                st.markdown(f"**{company_name}** {status_badge}", unsafe_allow_html=True)

                # Company details in columns
                comp_col1, comp_col2, comp_col3 = st.columns(3)

                with comp_col1:
                    st.markdown("**Company Number**")
                    ch_link = f"https://find-and-update.company-information.service.gov.uk/company/{company_number}"
                    st.markdown(f"[{company_number}]({ch_link})")

                with comp_col2:
                    st.markdown("**Company Type**")
                    company_type = restaurant.get('company_type', 'N/A')
                    type_display = {
                        'ltd': 'Private Limited Company',
                        'plc': 'Public Limited Company',
                        'llp': 'Limited Liability Partnership',
                        'private-limited-guarant-nsc': 'Private Limited by Guarantee',
                        'charitable-incorporated-organisation': 'Charitable Incorporated Organisation'
                    }.get(company_type, company_type.upper() if company_type else 'N/A')
                    st.markdown(type_display)

                with comp_col3:
                    st.markdown("**Incorporated**")
                    inc_date = restaurant.get('incorporation_date')
                    if pd.notna(inc_date):
                        try:
                            inc_dt = pd.to_datetime(inc_date)
                            years_old = (pd.Timestamp.now() - inc_dt).days // 365
                            st.markdown(f"{inc_dt.strftime('%Y')} ({years_old} years)")
                        except:
                            st.markdown(inc_date)
                    else:
                        st.markdown("N/A")

                # Registered Address
                if pd.notna(restaurant.get('company_registered_address')):
                    st.markdown("**Registered Address**")
                    st.caption(restaurant['company_registered_address'])

                # Directors (using cached data)
                all_directors = load_directors()
                directors_query = all_directors[all_directors['restaurant_id'] == restaurant_id]

                if not directors_query.empty:
                    st.markdown("**Directors / Officers**")
                    for _, director in directors_query.iterrows():
                        director_name = director['director_name']
                        role = director['officer_role'] or 'Director'
                        details = []
                        if pd.notna(director.get('nationality')):
                            details.append(director['nationality'])
                        if pd.notna(director.get('occupation')):
                            details.append(director['occupation'])

                        detail_str = f" ({', '.join(details)})" if details else ""
                        st.markdown(f"• **{director_name}** - {role}{detail_str}")

                # SIC Codes
                if pd.notna(restaurant.get('company_sic_codes')) and restaurant['company_sic_codes']:
                    st.markdown("**Business Activities (SIC Codes)**")
                    st.caption(restaurant['company_sic_codes'])

                # Data freshness
                if pd.notna(restaurant.get('companies_house_fetched_at')):
                    fetch_date = pd.to_datetime(restaurant['companies_house_fetched_at'])
                    st.caption(f"Company data from Companies House, fetched {fetch_date.strftime('%Y-%m-%d')}")

            # ================================================================
            # Financial Overview Section
            # ================================================================
            if 'net_assets_gbp' in restaurant.index and pd.notna(restaurant.get('net_assets_gbp')):
                st.markdown("---")
                st.subheader("💰 Financial Overview")

                # Financial Rating Badge
                if pd.notna(restaurant.get('financial_rating')):
                    rating = restaurant['financial_rating']
                    score = restaurant.get('financial_health_score', 0)
                    description = restaurant.get('rating_description', '')

                    # Color code the rating
                    rating_colors = {
                        'A': '🟢',
                        'B': '🟢',
                        'C': '🟡',
                        'D': '🟠',
                        'E': '🟠',
                        'F': '🔴'
                    }
                    indicator = rating_colors.get(rating, '⚪')

                    st.markdown(f"### {indicator} Financial Rating: **{rating}** ({description}) - Score: {score}/100")

                # Helper function to format currency
                def format_currency(value):
                    if pd.isna(value):
                        return "N/A"
                    if value >= 1_000_000:
                        return f"£{value/1_000_000:.2f}M"
                    elif value >= 1_000:
                        return f"£{value/1_000:.1f}k"
                    elif value <= -1_000_000:
                        return f"-£{abs(value)/1_000_000:.2f}M"
                    elif value <= -1_000:
                        return f"-£{abs(value)/1_000:.1f}k"
                    else:
                        return f"£{value:,}"

                # Current vs Prior Year Comparison
                has_prior = pd.notna(restaurant.get('net_assets_gbp_prior'))

                if has_prior:
                    st.markdown("#### 📊 Year-over-Year Comparison")

                    # Build comparison data
                    period_end = pd.to_datetime(restaurant['accounts_period_end']) if pd.notna(restaurant.get('accounts_period_end')) else None
                    current_year = period_end.year if period_end else "Current"
                    prior_year = current_year - 1 if isinstance(current_year, int) else "Prior"

                    # Build rows - always show all metrics, use N/A for missing data
                    comparison_data = []

                    # Net Assets/Liabilities (always present)
                    net_assets_current = restaurant.get('net_assets_gbp', 0)
                    net_assets_prior = restaurant.get('net_assets_gbp_prior', 0)

                    # Use "Net Liabilities" if both years are negative, otherwise "Net Assets"
                    if net_assets_current < 0 and net_assets_prior < 0:
                        metric_label = 'Net Liabilities'
                    else:
                        metric_label = 'Net Assets'

                    comparison_data.append({
                        'Metric': metric_label,
                        str(current_year): format_currency(restaurant.get('net_assets_gbp')),
                        str(prior_year): format_currency(restaurant.get('net_assets_gbp_prior'))
                    })

                    # Employees (show if either year has data)
                    if pd.notna(restaurant.get('employees')) or pd.notna(restaurant.get('employees_prior')):
                        current_emp = f"{int(restaurant['employees'])} staff" if pd.notna(restaurant.get('employees')) else "N/A"
                        prior_emp = f"{int(restaurant['employees_prior'])} staff" if pd.notna(restaurant.get('employees_prior')) else "N/A"
                        comparison_data.append({
                            'Metric': 'Employees',
                            str(current_year): current_emp,
                            str(prior_year): prior_emp
                        })

                    # Total Assets (show if either year has data)
                    if pd.notna(restaurant.get('total_assets_gbp')) or pd.notna(restaurant.get('total_assets_gbp_prior')):
                        comparison_data.append({
                            'Metric': 'Total Assets',
                            str(current_year): format_currency(restaurant.get('total_assets_gbp')),
                            str(prior_year): format_currency(restaurant.get('total_assets_gbp_prior'))
                        })

                    # Display as DataFrame for better alignment
                    comparison_df = pd.DataFrame(comparison_data)
                    st.dataframe(comparison_df, hide_index=True, width="stretch")

                    # Year-over-year changes
                    st.markdown("#### 📈 Performance Metrics")

                    change_col1, change_col2 = st.columns(2)

                    with change_col1:
                        if pd.notna(restaurant.get('net_assets_change_gbp')):
                            change = restaurant['net_assets_change_gbp']
                            change_pct = restaurant.get('net_assets_change_pct', 0)
                            change_emoji = "📈" if change > 0 else "📉" if change < 0 else "➖"

                            # Use appropriate label based on whether we have assets or liabilities
                            change_label = f"{metric_label} Change"

                            st.metric(
                                change_label,
                                format_currency(change),
                                f"{change_pct:+.1f}%" if pd.notna(change_pct) else None,
                                delta_color="normal"
                            )

                    with change_col2:
                        if pd.notna(restaurant.get('employee_change')):
                            emp_change = int(restaurant['employee_change'])
                            change_emoji = "👥+" if emp_change > 0 else "👥-" if emp_change < 0 else "👥="

                            st.metric(
                                "Employee Change",
                                f"{emp_change:+d}",
                                "Growing" if emp_change > 0 else "Shrinking" if emp_change < 0 else "Stable",
                                delta_color="normal"
                            )
                else:
                    # No prior year data - just show current year
                    st.markdown("#### Current Year Data")
                    fin_col1, fin_col2, fin_col3 = st.columns(3)

                    with fin_col1:
                        # Use "Net Liabilities" if negative, otherwise "Net Assets"
                        net_assets_current = restaurant.get('net_assets_gbp', 0)
                        asset_label = "Net Liabilities" if net_assets_current < 0 else "Net Assets"
                        st.markdown(f"**{asset_label}**")
                        st.markdown(format_currency(restaurant.get('net_assets_gbp')))

                    with fin_col2:
                        st.markdown("**Employees**")
                        employees = restaurant.get('employees')
                        if pd.notna(employees) and employees > 0:
                            st.markdown(f"{int(employees)} staff")
                        else:
                            st.markdown("N/A")

                    with fin_col3:
                        st.markdown("**Total Assets**")
                        st.markdown(format_currency(restaurant.get('total_assets_gbp')))

                # Additional financial details
                if pd.notna(restaurant.get('turnover_gbp')) or pd.notna(restaurant.get('profit_loss_gbp')):
                    st.markdown("#### Additional Metrics")
                    extra_fin_col1, extra_fin_col2 = st.columns(2)

                    with extra_fin_col1:
                        if pd.notna(restaurant.get('turnover_gbp')):
                            turnover = restaurant['turnover_gbp']
                            st.caption(f"Turnover: {format_currency(turnover)}")

                    with extra_fin_col2:
                        if pd.notna(restaurant.get('profit_loss_gbp')):
                            profit = restaurant['profit_loss_gbp']
                            profit_emoji = "📈" if profit > 0 else "📉" if profit < 0 else "➖"
                            st.caption(f"{profit_emoji} Profit/Loss: {format_currency(profit)}")

                # Accounts period
                if pd.notna(restaurant.get('accounts_period_end')):
                    period_end = pd.to_datetime(restaurant['accounts_period_end'])
                    st.caption(f"📅 Accounts period ending {period_end.strftime('%B %Y')}")
                    st.caption(f"💼 Data from Companies House")

            # ================================================================
            # Financial Performance Chart (if both years available)
            # ================================================================
            if pd.notna(restaurant.get('net_assets_gbp')) and pd.notna(restaurant.get('net_assets_gbp_prior')):
                try:
                    import plotly.graph_objects as go

                    current_val = restaurant['net_assets_gbp']
                    prior_val = restaurant['net_assets_gbp_prior']
                    period_end = pd.to_datetime(restaurant['accounts_period_end']) if pd.notna(restaurant.get('accounts_period_end')) else None
                    current_year = period_end.year if period_end else "Current"
                    prior_year = current_year - 1 if isinstance(current_year, int) else "Prior"

                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=[prior_year, current_year],
                        y=[prior_val, current_val],
                        marker_color=['lightblue', 'green' if current_val > prior_val else 'red'],
                        text=[f"£{prior_val:,.0f}", f"£{current_val:,.0f}"],
                        textposition='auto',
                    ))

                    fig.update_layout(
                        title="Net Assets Trend",
                        xaxis_title="Year",
                        yaxis_title="Net Assets (£)",
                        height=300,
                        showlegend=False
                    )

                    st.plotly_chart(fig, width="stretch")
                except:
                    pass  # Silently fail if chart cannot be rendered

            # ================================================================
            # Data Freshness
            # ================================================================
            st.markdown("---")
            st.caption("**Data Last Updated:**")
            data_col1, data_col2, data_col3 = st.columns(3)
            with data_col1:
                if pd.notna(restaurant.get('last_updated')):
                    updated = pd.to_datetime(restaurant['last_updated'], format='ISO8601')
                    st.caption(f"Menu: {updated.strftime('%Y-%m-%d')}")
            with data_col2:
                if pd.notna(restaurant.get('hygiene_rating_fetched_at')):
                    updated = pd.to_datetime(restaurant['hygiene_rating_fetched_at'], format='ISO8601')
                    st.caption(f"Hygiene: {updated.strftime('%Y-%m-%d')}")
            with data_col3:
                if pd.notna(restaurant.get('trustpilot_last_scraped_at')):
                    updated = pd.to_datetime(restaurant['trustpilot_last_scraped_at'], format='ISO8601')
                    st.caption(f"Reviews: {updated.strftime('%Y-%m-%d')}")


# ============================================================================
# Run Dashboard
# ============================================================================

if __name__ == "__main__":
    main()
