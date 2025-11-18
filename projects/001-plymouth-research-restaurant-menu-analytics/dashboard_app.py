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


@st.cache_data(ttl=300)
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
            scraping_method
        FROM restaurants
        WHERE is_active = 1
        ORDER BY name
    """
    df = pd.read_sql_query(query, conn)
    return df


@st.cache_data(ttl=300)
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


@st.cache_data(ttl=300)
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


# ============================================================================
# Helper Functions
# ============================================================================

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

    # Load data
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

    # ========================================================================
    # Key Metrics
    # ========================================================================
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("🍽️ Restaurants", len(restaurants_df))

    with col2:
        real_count = (restaurants_df['data_source'] == 'real_scraped').sum()
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

    st.divider()

    # ========================================================================
    # Tabs
    # ========================================================================
    tab1, tab2, tab3, tab4 = st.tabs([
        "🍽️ Browse Menus",
        "📊 Price Analytics",
        "🏪 Restaurant Comparison",
        "📈 Statistics"
    ])

    # ------------------------------------------------------------------------
    # Tab 1: Browse Menus
    # ------------------------------------------------------------------------
    with tab1:
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

                    st.markdown(f"<span style='background: {badge_color}; color: white; padding: 3px 10px; border-radius: 3px; font-size: 0.85em; font-weight: bold;' title='{badge_title}'>{badge_text}</span>", unsafe_allow_html=True)
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

                    # Data source information
                    st.markdown(f"<small>📍 Source: <a href='{restaurant_info['website_url']}' target='_blank'>{restaurant_info['website_url']}</a></small>", unsafe_allow_html=True)

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
    # Tab 2: Price Analytics
    # ------------------------------------------------------------------------
    with tab2:
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
            st.plotly_chart(fig_category, use_container_width=True)

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
            st.plotly_chart(fig_restaurant, use_container_width=True)

            # Price histogram
            st.subheader("Price Distribution")
            fig_hist = px.histogram(
                filtered_menu.dropna(subset=['price_gbp']),
                x='price_gbp',
                nbins=20,
                title="Distribution of Menu Item Prices",
                labels={'price_gbp': 'Price (£)'}
            )
            st.plotly_chart(fig_hist, use_container_width=True)

    # ------------------------------------------------------------------------
    # Tab 3: Restaurant Comparison
    # ------------------------------------------------------------------------
    with tab3:
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

        st.plotly_chart(fig_counts, use_container_width=True)

        # Show outlier details if any exist
        if outlier_count > 0 and not exclude_outliers:
            with st.expander(f"⚠️ View {outlier_count} outlier restaurant(s) details"):
                outliers_df = restaurant_counts[restaurant_counts['is_outlier']][['restaurant_name', 'item_count']]
                outliers_df.columns = ['Restaurant', 'Menu Items']
                st.dataframe(outliers_df, hide_index=True, use_container_width=True)

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
            st.plotly_chart(fig_avg_price, use_container_width=True)

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

        st.plotly_chart(fig_category_dist, use_container_width=True)

    # ------------------------------------------------------------------------
    # Tab 4: Statistics
    # ------------------------------------------------------------------------
    with tab4:
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
                    use_container_width=True
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
                use_container_width=True
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
            st.plotly_chart(fig_tags, use_container_width=True)
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
            use_container_width=True,
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


# ============================================================================
# Run Dashboard
# ============================================================================

if __name__ == "__main__":
    main()
