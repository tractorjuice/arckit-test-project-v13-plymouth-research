"""
Metrics Components
==================

Key metrics display components for the dashboard.

Author: Plymouth Research Team
Date: 2025-11-26
"""

import streamlit as st
import pandas as pd


def render_metrics_row(
    restaurants_df: pd.DataFrame,
    menu_df: pd.DataFrame
) -> None:
    """
    Render the main metrics row.

    Args:
        restaurants_df: Filtered restaurant data
        menu_df: Filtered menu items data
    """
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.metric("🍽️ Restaurants", len(restaurants_df))

    with col2:
        real_count = (restaurants_df['data_source'] == 'real_scraped').sum()
        st.metric("✓ Real Data", real_count, help="Restaurants with actual scraped menus")

    with col3:
        st.metric("📋 Menu Items", len(menu_df))

    with col4:
        if not menu_df['price_gbp'].isna().all():
            avg_price = menu_df['price_gbp'].mean()
            st.metric("💰 Avg Price", f"£{avg_price:.2f}")
        else:
            st.metric("💰 Avg Price", "N/A")

    with col5:
        unique_categories = menu_df['category'].nunique()
        st.metric("🏷️ Categories", unique_categories)

    with col6:
        rated_restos = restaurants_df[restaurants_df['hygiene_rating'].notna()]
        if len(rated_restos) > 0:
            avg_rating = rated_restos['hygiene_rating'].mean()
            st.metric(
                "⭐ Avg Hygiene",
                f"{avg_rating:.1f}/5",
                help=f"{len(rated_restos)} of {len(restaurants_df)} restaurants rated"
            )
        else:
            st.metric("⭐ Avg Hygiene", "N/A", help="No hygiene ratings available")


def render_business_rates_summary(restaurants_df: pd.DataFrame) -> None:
    """
    Render business rates summary row.

    Args:
        restaurants_df: Filtered restaurant data
    """
    if 'business_rates_rateable_value' not in restaurants_df.columns:
        return

    rates_restos = restaurants_df[restaurants_df['business_rates_rateable_value'].notna()]

    if len(rates_restos) == 0:
        return

    st.markdown("##### 💷 Business Rates Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📊 With Rates Data",
            f"{len(rates_restos)}/{len(restaurants_df)}",
            help="Restaurants with business rates information"
        )

    with col2:
        avg_rv = rates_restos['business_rates_rateable_value'].mean()
        st.metric(
            "💷 Avg Rateable Value",
            f"£{int(avg_rv):,}",
            help="Average property valuation"
        )

    with col3:
        if 'business_rates_net_charge' in rates_restos.columns:
            avg_charge = rates_restos['business_rates_net_charge'].mean()
            st.metric(
                "💰 Avg Annual Rates",
                f"£{int(avg_charge):,}",
                help="Average annual business rates (2025-26)"
            )

    with col4:
        max_rv = rates_restos['business_rates_rateable_value'].max()
        max_resto = rates_restos.loc[
            rates_restos['business_rates_rateable_value'] == max_rv, 'name'
        ].iloc[0]
        st.metric(
            "🏆 Highest RV",
            f"£{int(max_rv):,}",
            help=f"{max_resto}"
        )


def render_review_metrics(
    trustpilot_df: pd.DataFrame,
    google_df: pd.DataFrame
) -> None:
    """
    Render review metrics row.

    Args:
        trustpilot_df: Trustpilot reviews data
        google_df: Google reviews data
    """
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        restaurants_with_reviews = trustpilot_df['restaurant_id'].nunique()
        st.metric(
            "🏪 Restaurants Reviewed",
            restaurants_with_reviews,
            help="Restaurants with Trustpilot reviews"
        )

    with col2:
        st.metric(
            "📝 Trustpilot Reviews",
            f"{len(trustpilot_df):,}",
            help="Total Trustpilot reviews"
        )

    with col3:
        st.metric(
            "🔍 Google Reviews",
            f"{len(google_df):,}",
            help="Total Google reviews"
        )

    with col4:
        if not trustpilot_df.empty:
            avg_rating = trustpilot_df['rating'].mean()
            st.metric(
                "⭐ Avg Trustpilot Rating",
                f"{avg_rating:.2f}/5",
                help="Average Trustpilot rating"
            )
        else:
            st.metric("⭐ Avg Rating", "N/A")


def render_data_quality_metrics(
    restaurants_df: pd.DataFrame,
    menu_df: pd.DataFrame
) -> None:
    """
    Render data quality metrics.

    Args:
        restaurants_df: Restaurant data
        menu_df: Menu items data
    """
    st.markdown("##### 📊 Data Quality")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        # Completeness: restaurants with hygiene ratings
        with_hygiene = restaurants_df['hygiene_rating'].notna().sum()
        pct = (with_hygiene / len(restaurants_df) * 100) if len(restaurants_df) > 0 else 0
        st.metric(
            "🏥 Hygiene Coverage",
            f"{pct:.0f}%",
            help=f"{with_hygiene}/{len(restaurants_df)} restaurants"
        )

    with col2:
        # Completeness: restaurants with Trustpilot
        with_trustpilot = restaurants_df['trustpilot_review_count'].notna().sum()
        pct = (with_trustpilot / len(restaurants_df) * 100) if len(restaurants_df) > 0 else 0
        st.metric(
            "💬 Review Coverage",
            f"{pct:.0f}%",
            help=f"{with_trustpilot}/{len(restaurants_df)} restaurants"
        )

    with col3:
        # Menu items with prices
        with_price = menu_df['price_gbp'].notna().sum()
        pct = (with_price / len(menu_df) * 100) if len(menu_df) > 0 else 0
        st.metric(
            "💰 Price Coverage",
            f"{pct:.0f}%",
            help=f"{with_price}/{len(menu_df)} items"
        )

    with col4:
        # Real vs synthetic data
        real_count = (restaurants_df['data_source'] == 'real_scraped').sum()
        pct = (real_count / len(restaurants_df) * 100) if len(restaurants_df) > 0 else 0
        st.metric(
            "✓ Real Data",
            f"{pct:.0f}%",
            help=f"{real_count}/{len(restaurants_df)} restaurants"
        )
