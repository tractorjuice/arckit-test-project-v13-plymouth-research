"""
Map Tab
=======

Interactive map visualization of restaurants.

Author: Plymouth Research Team
Date: 2025-11-26
"""

import streamlit as st
import pandas as pd
import numpy as np

try:
    import pydeck as pdk
    PYDECK_AVAILABLE = True
except ImportError:
    PYDECK_AVAILABLE = False


def render_map_tab(
    restaurants_df: pd.DataFrame,
    filters: dict = None
) -> None:
    """
    Render the map tab.

    Args:
        restaurants_df: Filtered restaurant data
        filters: Optional filter settings
    """
    st.header("🗺️ Restaurant Map")

    if not PYDECK_AVAILABLE:
        st.error("Map visualization requires pydeck. Install with: pip install pydeck")
        return

    # Get restaurants with GPS coordinates
    map_restaurants = restaurants_df[
        (restaurants_df['fsa_latitude'].notna()) &
        (restaurants_df['fsa_longitude'].notna())
    ].copy()

    if map_restaurants.empty:
        st.warning("No restaurants have GPS coordinates available for mapping.")
        st.info("GPS coordinates are available for restaurants matched with FSA hygiene data.")
        return

    st.markdown(f"**Showing {len(map_restaurants)} restaurants with GPS coordinates**")

    # Prepare map data
    map_data = map_restaurants[[
        'restaurant_id', 'name', 'fsa_latitude', 'fsa_longitude',
        'hygiene_rating', 'cuisine_type', 'price_range',
        'trustpilot_avg_rating', 'trustpilot_review_count'
    ]].copy()

    map_data = map_data.rename(columns={
        'fsa_latitude': 'lat',
        'fsa_longitude': 'lon'
    })

    # Handle overlapping coordinates
    map_data = spread_overlapping_markers(map_data)

    # Add colors based on hygiene rating
    map_data['color'] = map_data['hygiene_rating'].apply(get_rating_color)

    # Create tooltip
    map_data['tooltip'] = map_data.apply(create_tooltip, axis=1)

    # Calculate map center
    center_lat = map_data['lat'].mean()
    center_lon = map_data['lon'].mean()

    # Create pydeck layer
    layer = pdk.Layer(
        'ScatterplotLayer',
        data=map_data,
        get_position='[lon, lat]',
        get_color='color',
        get_radius=50,
        pickable=True,
        auto_highlight=True,
    )

    # Create view
    view = pdk.ViewState(
        latitude=center_lat,
        longitude=center_lon,
        zoom=13,
        pitch=0
    )

    # Create deck
    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view,
        tooltip={
            'html': '{tooltip}',
            'style': {
                'backgroundColor': 'steelblue',
                'color': 'white',
                'padding': '10px'
            }
        },
        map_style='mapbox://styles/mapbox/light-v9'
    )

    st.pydeck_chart(deck)

    # Legend
    render_map_legend()

    # Restaurant list
    st.subheader("📍 Restaurants on Map")

    display_df = map_data[[
        'name', 'hygiene_rating', 'cuisine_type', 'trustpilot_avg_rating'
    ]].copy()

    display_df.columns = ['Restaurant', 'Hygiene', 'Cuisine', 'Trustpilot']
    display_df['Hygiene'] = display_df['Hygiene'].apply(
        lambda x: '⭐' * int(x) if pd.notna(x) else 'N/A'
    )
    display_df['Trustpilot'] = display_df['Trustpilot'].apply(
        lambda x: f"{x:.1f}★" if pd.notna(x) else 'N/A'
    )

    st.dataframe(display_df, use_container_width=True, hide_index=True)


def spread_overlapping_markers(map_data: pd.DataFrame) -> pd.DataFrame:
    """
    Spread markers that have the same or very close coordinates.

    Args:
        map_data: DataFrame with lat/lon columns

    Returns:
        DataFrame with adjusted coordinates
    """
    # Round to find near-duplicates
    map_data['lat_rounded'] = map_data['lat'].round(5)
    map_data['lon_rounded'] = map_data['lon'].round(5)

    coord_groups = map_data.groupby(['lat_rounded', 'lon_rounded']).size()
    duplicate_coords = coord_groups[coord_groups > 1].index

    # Spread duplicates in a circle
    for coord in duplicate_coords:
        mask = (map_data['lat_rounded'] == coord[0]) & (map_data['lon_rounded'] == coord[1])
        duplicate_rows = map_data[mask].copy()
        n_duplicates = len(duplicate_rows)

        center_lat = duplicate_rows['lat'].mean()
        center_lon = duplicate_rows['lon'].mean()

        radius = 0.00015  # Small offset in degrees

        for i, (idx, row) in enumerate(duplicate_rows.iterrows()):
            angle = (2 * np.pi * i / n_duplicates)
            map_data.loc[idx, 'lat'] = center_lat + radius * np.sin(angle)
            map_data.loc[idx, 'lon'] = center_lon + radius * np.cos(angle)

    # Drop temporary columns
    map_data = map_data.drop(columns=['lat_rounded', 'lon_rounded'])

    return map_data


def get_rating_color(rating: float) -> list:
    """
    Get RGB color for hygiene rating.

    Args:
        rating: Hygiene rating (0-5)

    Returns:
        RGB color as list [r, g, b, a]
    """
    if pd.isna(rating):
        return [150, 150, 150, 200]  # Gray

    rating = int(rating)

    colors = {
        5: [0, 200, 0, 200],      # Green
        4: [100, 220, 0, 200],    # Light green
        3: [255, 200, 0, 200],    # Yellow
        2: [255, 150, 0, 200],    # Orange
        1: [255, 100, 0, 200],    # Dark orange
        0: [255, 0, 0, 200],      # Red
    }

    return colors.get(rating, [150, 150, 150, 200])


def create_tooltip(row: pd.Series) -> str:
    """
    Create HTML tooltip for map marker.

    Args:
        row: Restaurant row

    Returns:
        HTML string for tooltip
    """
    name = row['name']
    cuisine = row.get('cuisine_type', 'Unknown')
    hygiene = int(row['hygiene_rating']) if pd.notna(row.get('hygiene_rating')) else None
    trustpilot = row.get('trustpilot_avg_rating')

    html = f"<b>{name}</b><br>"
    html += f"Cuisine: {cuisine}<br>"

    if hygiene is not None:
        stars = '⭐' * hygiene
        html += f"Hygiene: {stars}<br>"

    if pd.notna(trustpilot):
        html += f"Trustpilot: {trustpilot:.1f}★"

    return html


def render_map_legend() -> None:
    """Render color legend for map."""
    st.markdown("**Legend (Hygiene Rating)**")

    legend_items = [
        ("🟢 5★ Very Good", "#00C800"),
        ("🟢 4★ Good", "#64DC00"),
        ("🟡 3★ Satisfactory", "#FFC800"),
        ("🟠 2★ Needs Improvement", "#FF9600"),
        ("🟠 1★ Major Improvement", "#FF6400"),
        ("🔴 0★ Urgent Action", "#FF0000"),
        ("⚫ No Rating", "#969696"),
    ]

    cols = st.columns(len(legend_items))
    for col, (label, _) in zip(cols, legend_items):
        col.caption(label)
