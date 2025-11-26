"""
Sidebar Component
=================

Sidebar filters and navigation for the dashboard.

Author: Plymouth Research Team
Date: 2025-11-26
"""

from typing import Dict, List, Any, Tuple
import streamlit as st
import pandas as pd


def render_sidebar(
    restaurants_df: pd.DataFrame,
    menu_df: pd.DataFrame,
    dietary_df: pd.DataFrame,
    view_mode: str = "Analytics"
) -> Dict[str, Any]:
    """
    Render the sidebar with all filters.

    Args:
        restaurants_df: Restaurant data
        menu_df: Menu items data
        dietary_df: Dietary tags data
        view_mode: Current view mode

    Returns:
        Dictionary of filter values
    """
    filters = {}

    st.sidebar.title("📍 Navigation")
    filters['view_mode'] = st.sidebar.radio(
        "Select View",
        options=["📊 Analytics Dashboard", "🗺️ Full-Screen Map"],
        index=0,
        help="Choose between analytics tabs (with map) or full-screen map view"
    )

    st.sidebar.divider()

    # Search & Filter section
    st.sidebar.header("🔍 Search & Filter")

    # Restaurant filter
    all_restaurants = sorted(restaurants_df['name'].unique().tolist())
    filters['restaurants'] = st.sidebar.multiselect(
        "Restaurants",
        options=all_restaurants,
        default=all_restaurants,
        help="Select one or more restaurants"
    )

    # Cuisine filter
    all_cuisines = sorted(menu_df['cuisine_type'].dropna().unique().tolist())
    filters['cuisines'] = st.sidebar.multiselect(
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

        filters['price_range'] = st.sidebar.slider(
            "Price (£)",
            min_value=0.0,
            max_value=max_price_db + 5.0,
            value=(min_price_db, max_price_db),
            step=0.50,
            help="Filter menu items by price"
        )
    else:
        filters['price_range'] = (0.0, 100.0)

    # Category filter
    all_categories = sorted(menu_df['category'].dropna().unique().tolist())
    filters['categories'] = st.sidebar.multiselect(
        "Categories",
        options=all_categories,
        default=all_categories,
        help="Filter by menu category (Starters, Mains, etc.)"
    )

    # Dietary filter
    all_dietary_tags = sorted(dietary_df['tag_name'].unique().tolist())
    filters['dietary'] = st.sidebar.multiselect(
        "🥗 Dietary Requirements",
        options=all_dietary_tags,
        help="Items must have ALL selected tags"
    )

    # Hygiene rating filter
    st.sidebar.subheader("⭐ Food Hygiene Rating")
    filters['min_hygiene'] = st.sidebar.select_slider(
        "Minimum Rating",
        options=[0, 1, 2, 3, 4, 5],
        value=0,
        format_func=lambda x: f"{x}★" if x > 0 else "Any",
        help="Filter restaurants by minimum FSA hygiene rating"
    )
    st.sidebar.caption("🏛️ Source: [Food Standards Agency](https://www.food.gov.uk/safety-hygiene/food-hygiene-rating-scheme)")

    # Google service options filters
    st.sidebar.subheader("🍽️ Service Options")
    filters['services'] = st.sidebar.multiselect(
        "Select Services",
        options=["Dine-in", "Takeout", "Delivery", "Reservations"],
        help="Filter restaurants by available services"
    )

    # Meal time filters
    st.sidebar.subheader("🍳 Meal Times")
    filters['meals'] = st.sidebar.multiselect(
        "Select Meal Times",
        options=["Breakfast", "Lunch", "Dinner"],
        help="Filter restaurants by meal service times"
    )

    # Food & beverage filters
    st.sidebar.subheader("🍷 Food & Beverages")
    filters['food_beverage'] = st.sidebar.multiselect(
        "Select Options",
        options=["Vegetarian Food", "Beer", "Wine"],
        help="Filter restaurants by food and beverage options"
    )

    # Business status filter
    filters['hide_closed'] = st.sidebar.checkbox(
        "Hide Closed Restaurants",
        value=True,
        help="Hide permanently and temporarily closed restaurants"
    )
    st.sidebar.caption("🌐 Service data from Google Places API")

    # Business rates filter
    st.sidebar.subheader("💷 Business Rates")
    filters['show_only_with_rates'] = st.sidebar.checkbox(
        "Show Only Restaurants with Business Rates Data",
        value=False,
        help="Filter to show only restaurants with business rates information"
    )
    st.sidebar.caption("💷 Rates data from Plymouth Business Rates Register (Nov 2025)")

    # Map-specific controls (shown only in Full-Screen Map View)
    if filters['view_mode'] == "🗺️ Full-Screen Map":
        st.sidebar.divider()
        st.sidebar.subheader("🗺️ Map Controls")

        filters['show_hygiene_colors'] = st.sidebar.checkbox("Color by Hygiene Rating", value=True)

        if filters.get('show_hygiene_colors', True):
            filters['min_hygiene_map'] = st.sidebar.select_slider(
                "Minimum Rating for Map",
                options=[1, 2, 3, 4, 5],
                value=1,
                format_func=lambda x: f"{x}★",
                help="Show only restaurants with this minimum rating on map"
            )
        else:
            filters['min_hygiene_map'] = 1

        filters['map_style'] = st.sidebar.selectbox(
            "Map Style",
            options=["Open Street Map", "Satellite"],
            index=0
        )

    return filters


def apply_filters(
    restaurants_df: pd.DataFrame,
    menu_df: pd.DataFrame,
    dietary_df: pd.DataFrame,
    filters: Dict[str, Any]
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Apply all filters to data.

    Args:
        restaurants_df: Restaurant data
        menu_df: Menu items data
        dietary_df: Dietary tags data
        filters: Dictionary of filter values

    Returns:
        Tuple of (filtered_restaurants, filtered_menu)
    """
    filtered_restaurants = restaurants_df.copy()
    filtered_menu = menu_df.copy()

    # Filter restaurants by selection
    if filters.get('restaurants'):
        filtered_restaurants = filtered_restaurants[
            filtered_restaurants['name'].isin(filters['restaurants'])
        ]

    # Filter menu by cuisine
    if filters.get('cuisines'):
        filtered_menu = filtered_menu[filtered_menu['cuisine_type'].isin(filters['cuisines'])]

    # Filter menu by price
    price_range = filters.get('price_range', (0, 1000))
    filtered_menu = filtered_menu[
        (filtered_menu['price_gbp'] >= price_range[0]) &
        (filtered_menu['price_gbp'] <= price_range[1])
    ]

    # Filter menu by category
    if filters.get('categories'):
        filtered_menu = filtered_menu[filtered_menu['category'].isin(filters['categories'])]

    # Filter by dietary tags
    if filters.get('dietary'):
        item_ids_with_tags = dietary_df[dietary_df['tag_name'].isin(filters['dietary'])]
        item_ids = item_ids_with_tags.groupby('item_id').size()
        item_ids = item_ids[item_ids == len(filters['dietary'])].index.tolist()
        filtered_menu = filtered_menu[filtered_menu['item_id'].isin(item_ids)]

    # Filter restaurants by hygiene rating
    min_hygiene = filters.get('min_hygiene', 0)
    if min_hygiene > 0:
        filtered_restaurants = filtered_restaurants[
            (filtered_restaurants['hygiene_rating'] >= min_hygiene) |
            (filtered_restaurants['hygiene_rating'].isna())
        ]

    # Filter by Google service options
    service_mapping = {
        "Dine-in": "google_dine_in",
        "Takeout": "google_takeout",
        "Delivery": "google_delivery",
        "Reservations": "google_reservable",
    }
    for service in filters.get('services', []):
        col = service_mapping.get(service)
        if col and col in filtered_restaurants.columns:
            filtered_restaurants = filtered_restaurants[filtered_restaurants[col] == 1]

    # Filter by meal times
    meal_mapping = {
        "Breakfast": "google_serves_breakfast",
        "Lunch": "google_serves_lunch",
        "Dinner": "google_serves_dinner",
    }
    for meal in filters.get('meals', []):
        col = meal_mapping.get(meal)
        if col and col in filtered_restaurants.columns:
            filtered_restaurants = filtered_restaurants[filtered_restaurants[col] == 1]

    # Filter by food & beverages
    fb_mapping = {
        "Vegetarian Food": "google_serves_vegetarian",
        "Beer": "google_serves_beer",
        "Wine": "google_serves_wine",
    }
    for fb in filters.get('food_beverage', []):
        col = fb_mapping.get(fb)
        if col and col in filtered_restaurants.columns:
            filtered_restaurants = filtered_restaurants[filtered_restaurants[col] == 1]

    # Filter by business status
    if filters.get('hide_closed') and 'google_business_status' in filtered_restaurants.columns:
        filtered_restaurants = filtered_restaurants[
            (filtered_restaurants['google_business_status'] == 'OPERATIONAL') |
            (filtered_restaurants['google_business_status'].isna())
        ]

    # Filter by business rates
    if filters.get('show_only_with_rates') and 'business_rates_rateable_value' in filtered_restaurants.columns:
        filtered_restaurants = filtered_restaurants[
            filtered_restaurants['business_rates_rateable_value'].notna()
        ]

    # Update menu to match filtered restaurants
    filtered_menu = filtered_menu[filtered_menu['restaurant_name'].isin(filtered_restaurants['name'])]

    return filtered_restaurants, filtered_menu
