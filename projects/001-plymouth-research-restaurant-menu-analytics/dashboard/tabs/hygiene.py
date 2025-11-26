"""
Hygiene Ratings Tab
===================

FSA Food Hygiene Rating analysis and display.

Author: Plymouth Research Team
Date: 2025-11-26
"""

import streamlit as st
import pandas as pd
import plotly.express as px

try:
    from dashboard.components.formatters import get_hygiene_badge
except ImportError:
    from ..components.formatters import get_hygiene_badge


def render_hygiene_tab(restaurants_df: pd.DataFrame) -> None:
    """
    Render the hygiene ratings tab.

    Args:
        restaurants_df: Filtered restaurant data
    """
    st.header("⭐ Food Hygiene Ratings")

    # Filter to rated restaurants
    rated = restaurants_df[restaurants_df['hygiene_rating'].notna()].copy()

    if rated.empty:
        st.warning("No hygiene rating data available for the filtered restaurants.")
        st.info("Hygiene ratings are sourced from the Food Standards Agency (FSA) Food Hygiene Rating Scheme.")
        return

    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Rated Restaurants",
            f"{len(rated)}/{len(restaurants_df)}",
            help="Number of restaurants with FSA ratings"
        )

    with col2:
        avg_rating = rated['hygiene_rating'].mean()
        st.metric(
            "Average Rating",
            f"{avg_rating:.2f}/5",
            help="Average FSA hygiene rating"
        )

    with col3:
        five_star = (rated['hygiene_rating'] == 5).sum()
        st.metric(
            "5★ Restaurants",
            five_star,
            help="Restaurants with 'Very Good' rating"
        )

    with col4:
        needs_improvement = (rated['hygiene_rating'] <= 2).sum()
        st.metric(
            "Needs Improvement",
            needs_improvement,
            help="Restaurants rated 2★ or below"
        )

    st.divider()

    # Rating distribution chart
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Rating Distribution")

        rating_counts = rated['hygiene_rating'].value_counts().sort_index()

        # Color mapping
        colors = {
            0: '#F44336',
            1: '#FF5722',
            2: '#FF9800',
            3: '#FFC107',
            4: '#8BC34A',
            5: '#4CAF50'
        }

        fig = px.bar(
            x=rating_counts.index.astype(int),
            y=rating_counts.values,
            labels={'x': 'Hygiene Rating (Stars)', 'y': 'Number of Restaurants'},
            title='Distribution of FSA Hygiene Ratings',
            color=[colors.get(int(r), '#9E9E9E') for r in rating_counts.index],
            color_discrete_map='identity'
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Rating Breakdown")

        # Rating labels
        rating_labels = {
            5: "5★ Very Good",
            4: "4★ Good",
            3: "3★ Satisfactory",
            2: "2★ Improvement Needed",
            1: "1★ Major Improvement",
            0: "0★ Urgent Action"
        }

        breakdown = rated['hygiene_rating'].value_counts().sort_index(ascending=False)

        for rating, count in breakdown.items():
            pct = count / len(rated) * 100
            label = rating_labels.get(int(rating), f"{int(rating)}★")
            st.markdown(f"**{label}**: {count} ({pct:.1f}%)")

    # Scores breakdown
    st.subheader("📊 Detailed Scores")

    st.markdown("""
    FSA hygiene ratings are based on three components:
    - **Hygiene** (0-25): Food handling, preparation, and cooking
    - **Structural** (0-25): Cleanliness and condition of facilities
    - **Confidence in Management** (0-30): Food safety management systems

    Lower scores are better. A total of 0-15 points = 5★ rating.
    """)

    # Show restaurants with detailed scores
    scores_df = rated[
        ['name', 'hygiene_rating', 'hygiene_score_hygiene', 'hygiene_score_structural', 'hygiene_score_confidence', 'hygiene_rating_date']
    ].copy()

    scores_df.columns = ['Restaurant', 'Rating', 'Hygiene Score', 'Structural Score', 'Confidence Score', 'Inspection Date']

    # Format rating as stars
    scores_df['Rating'] = scores_df['Rating'].apply(lambda x: '⭐' * int(x) if pd.notna(x) else 'N/A')

    # Sort by total score (sum of components)
    scores_df['Total'] = scores_df['Hygiene Score'].fillna(0) + scores_df['Structural Score'].fillna(0) + scores_df['Confidence Score'].fillna(0)
    scores_df = scores_df.sort_values('Total', ascending=True).drop(columns=['Total'])

    st.dataframe(scores_df, use_container_width=True, hide_index=True)

    # Restaurants needing attention
    needs_attention = rated[rated['hygiene_rating'] <= 2]

    if not needs_attention.empty:
        st.subheader("⚠️ Restaurants Requiring Attention")
        st.markdown("These restaurants have hygiene ratings of 2★ or below:")

        for _, rest in needs_attention.iterrows():
            badge = get_hygiene_badge(rest['hygiene_rating'])
            st.markdown(f"- **{rest['name']}**: {badge}", unsafe_allow_html=True)

    # FSA attribution
    st.divider()
    st.caption("""
    🏛️ **Data Source**: [Food Standards Agency](https://www.food.gov.uk/safety-hygiene/food-hygiene-rating-scheme) -
    Food Hygiene Rating Scheme (FHRS) data for Plymouth City (Authority Code 891).
    Licensed under the [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).
    """)
