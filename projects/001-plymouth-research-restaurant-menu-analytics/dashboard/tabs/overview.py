"""
Overview Tab
============

Dashboard overview with key statistics and quick insights.

Author: Plymouth Research Team
Date: 2025-11-26
"""

import streamlit as st
import pandas as pd
import plotly.express as px


def render_overview_tab(
    restaurants_df: pd.DataFrame,
    menu_df: pd.DataFrame,
) -> None:
    """
    Render the overview tab.

    Args:
        restaurants_df: Filtered restaurant data
        menu_df: Filtered menu items data
    """
    st.header("📊 Overview")

    # Quick stats
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Restaurant Distribution")

        # Cuisine distribution pie chart
        if not menu_df.empty:
            cuisine_counts = menu_df.groupby('cuisine_type').size().reset_index(name='count')
            fig = px.pie(
                cuisine_counts,
                values='count',
                names='cuisine_type',
                title='Menu Items by Cuisine Type',
                hole=0.4
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Data Sources")

        # Data source distribution
        if not restaurants_df.empty:
            source_counts = restaurants_df['data_source'].value_counts().reset_index()
            source_counts.columns = ['Source', 'Count']

            fig = px.bar(
                source_counts,
                x='Source',
                y='Count',
                title='Restaurants by Data Source',
                color='Source',
                color_discrete_map={
                    'real_scraped': '#4CAF50',
                    'synthetic': '#9E9E9E'
                }
            )
            st.plotly_chart(fig, use_container_width=True)

    # Hygiene rating overview
    st.subheader("⭐ Food Hygiene Ratings Distribution")

    rated_restaurants = restaurants_df[restaurants_df['hygiene_rating'].notna()]

    if not rated_restaurants.empty:
        rating_counts = rated_restaurants['hygiene_rating'].value_counts().sort_index()

        fig = px.bar(
            x=rating_counts.index.astype(int),
            y=rating_counts.values,
            labels={'x': 'Hygiene Rating', 'y': 'Number of Restaurants'},
            title=f'FSA Food Hygiene Ratings ({len(rated_restaurants)} restaurants)',
            color=rating_counts.index.astype(int),
            color_continuous_scale=['#F44336', '#FF5722', '#FF9800', '#FFC107', '#8BC34A', '#4CAF50']
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No hygiene rating data available for filtered restaurants.")

    # Price distribution
    st.subheader("💰 Price Distribution")

    if not menu_df['price_gbp'].isna().all():
        col1, col2 = st.columns(2)

        with col1:
            fig = px.histogram(
                menu_df.dropna(subset=['price_gbp']),
                x='price_gbp',
                nbins=30,
                title='Menu Item Prices',
                labels={'price_gbp': 'Price (£)'}
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Average price by cuisine
            avg_by_cuisine = menu_df.groupby('cuisine_type')['price_gbp'].mean().sort_values(ascending=False)

            fig = px.bar(
                x=avg_by_cuisine.index,
                y=avg_by_cuisine.values,
                title='Average Price by Cuisine',
                labels={'x': 'Cuisine', 'y': 'Average Price (£)'}
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No price data available for filtered items.")

    # Quick insights
    st.subheader("🔍 Quick Insights")

    insights = []

    # Most common cuisine
    if not menu_df.empty:
        top_cuisine = menu_df['cuisine_type'].value_counts().idxmax()
        cuisine_pct = (menu_df['cuisine_type'] == top_cuisine).mean() * 100
        insights.append(f"**Most common cuisine:** {top_cuisine} ({cuisine_pct:.1f}% of menu items)")

    # Average hygiene rating
    if not rated_restaurants.empty:
        avg_hygiene = rated_restaurants['hygiene_rating'].mean()
        insights.append(f"**Average hygiene rating:** {avg_hygiene:.2f}/5 across {len(rated_restaurants)} rated restaurants")

    # Price range
    if not menu_df['price_gbp'].isna().all():
        min_price = menu_df['price_gbp'].min()
        max_price = menu_df['price_gbp'].max()
        insights.append(f"**Price range:** £{min_price:.2f} - £{max_price:.2f}")

    # Coverage stats
    total_rest = len(restaurants_df)
    with_hygiene = restaurants_df['hygiene_rating'].notna().sum()
    with_reviews = restaurants_df['trustpilot_review_count'].notna().sum()

    insights.append(f"**Data coverage:** {with_hygiene}/{total_rest} have hygiene ratings, {with_reviews}/{total_rest} have reviews")

    for insight in insights:
        st.markdown(f"- {insight}")
