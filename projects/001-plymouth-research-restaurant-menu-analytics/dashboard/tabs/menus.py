"""
Browse Menus Tab
================

Menu browsing and search functionality.

Author: Plymouth Research Team
Date: 2025-11-26
"""

import streamlit as st
import pandas as pd

try:
    from dashboard.components.formatters import (
        get_hygiene_badge,
        get_trustpilot_badge,
        get_service_badges,
    )
except ImportError:
    from ..components.formatters import (
        get_hygiene_badge,
        get_trustpilot_badge,
        get_service_badges,
    )


def render_menus_tab(
    restaurants_df: pd.DataFrame,
    menu_df: pd.DataFrame,
) -> None:
    """
    Render the browse menus tab.

    Args:
        restaurants_df: Filtered restaurant data
        menu_df: Filtered menu items data
    """
    st.header("🍽️ Browse Menus")

    # Search box
    search_query = st.text_input(
        "🔍 Search menu items",
        placeholder="Search by dish name, description, or restaurant...",
        help="Search across all menu item names and descriptions"
    )

    # Apply search filter
    if search_query:
        search_lower = search_query.lower()
        menu_df = menu_df[
            menu_df['item_name'].str.lower().str.contains(search_lower, na=False) |
            menu_df['description'].str.lower().str.contains(search_lower, na=False) |
            menu_df['restaurant_name'].str.lower().str.contains(search_lower, na=False)
        ]

    st.markdown(f"**Showing {len(menu_df)} menu items from {menu_df['restaurant_name'].nunique()} restaurants**")

    # Group by restaurant
    restaurants_in_menu = menu_df['restaurant_name'].unique()

    for restaurant_name in sorted(restaurants_in_menu):
        # Get restaurant info
        rest_info = restaurants_df[restaurants_df['name'] == restaurant_name]

        if rest_info.empty:
            continue

        rest = rest_info.iloc[0]

        # Restaurant header with expander
        with st.expander(f"**{restaurant_name}** - {rest.get('cuisine_type', 'Unknown cuisine')}", expanded=False):
            # Restaurant info row
            col1, col2, col3 = st.columns([2, 2, 1])

            with col1:
                # Hygiene badge
                hygiene_badge = get_hygiene_badge(rest.get('hygiene_rating'))
                st.markdown(f"**Hygiene:** {hygiene_badge}", unsafe_allow_html=True)

                # Trustpilot badge
                if pd.notna(rest.get('trustpilot_avg_rating')):
                    tp_badge = get_trustpilot_badge(
                        rest['trustpilot_avg_rating'],
                        rest.get('trustpilot_review_count')
                    )
                    st.markdown(f"**Trustpilot:** {tp_badge}", unsafe_allow_html=True)

            with col2:
                # Service badges
                services = get_service_badges(rest.to_dict())
                if services:
                    st.markdown(f"**Services:** {services}")

                # Contact info
                if pd.notna(rest.get('google_phone_national')):
                    st.markdown(f"📞 [{rest['google_phone_national']}](tel:{rest['google_phone_national']})")

                if pd.notna(rest.get('website_url')):
                    st.markdown(f"🌐 [Website]({rest['website_url']})")

            with col3:
                # Price range
                price_range = rest.get('price_range', '')
                if price_range:
                    st.markdown(f"**Price:** {price_range}")

                # Google Maps link
                if pd.notna(rest.get('google_maps_url')):
                    st.markdown(f"📍 [Map]({rest['google_maps_url']})")

            st.divider()

            # Menu items for this restaurant
            rest_menu = menu_df[menu_df['restaurant_name'] == restaurant_name]

            # Group by category
            categories = rest_menu['category'].dropna().unique()

            for category in sorted(categories):
                st.markdown(f"**{category}**")

                cat_items = rest_menu[rest_menu['category'] == category]

                for _, item in cat_items.iterrows():
                    item_col1, item_col2 = st.columns([4, 1])

                    with item_col1:
                        name = item['item_name']
                        desc = item.get('description', '')

                        if pd.notna(desc) and desc:
                            st.markdown(f"- **{name}**: {desc[:100]}{'...' if len(str(desc)) > 100 else ''}")
                        else:
                            st.markdown(f"- **{name}**")

                    with item_col2:
                        price = item.get('price_gbp')
                        if pd.notna(price):
                            st.markdown(f"£{price:.2f}")

            # Items without category
            no_cat_items = rest_menu[rest_menu['category'].isna()]
            if not no_cat_items.empty:
                st.markdown("**Other Items**")
                for _, item in no_cat_items.iterrows():
                    price_str = f" - £{item['price_gbp']:.2f}" if pd.notna(item.get('price_gbp')) else ""
                    st.markdown(f"- {item['item_name']}{price_str}")

    if len(menu_df) == 0:
        st.info("No menu items match your filters. Try adjusting the sidebar filters.")
