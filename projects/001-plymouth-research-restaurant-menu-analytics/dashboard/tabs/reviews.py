"""
Reviews Tab
===========

Trustpilot and Google reviews analysis.

Author: Plymouth Research Team
Date: 2025-11-26
"""

import streamlit as st
import pandas as pd
import plotly.express as px

try:
    from dashboard.components.formatters import format_trustpilot_rating, get_trustpilot_badge
except ImportError:
    from ..components.formatters import format_trustpilot_rating, get_trustpilot_badge


def render_reviews_tab(
    restaurants_df: pd.DataFrame,
    trustpilot_df: pd.DataFrame,
    google_df: pd.DataFrame,
) -> None:
    """
    Render the reviews tab.

    Args:
        restaurants_df: Filtered restaurant data
        trustpilot_df: Trustpilot reviews data
        google_df: Google reviews data
    """
    st.header("📝 Customer Reviews")

    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        restaurants_with_reviews = restaurants_df['trustpilot_review_count'].notna().sum()
        st.metric(
            "Restaurants with Reviews",
            f"{restaurants_with_reviews}/{len(restaurants_df)}",
            help="Restaurants with Trustpilot reviews"
        )

    with col2:
        st.metric(
            "Trustpilot Reviews",
            f"{len(trustpilot_df):,}",
            help="Total Trustpilot reviews in database"
        )

    with col3:
        st.metric(
            "Google Reviews",
            f"{len(google_df):,}",
            help="Total Google reviews in database"
        )

    with col4:
        if not trustpilot_df.empty:
            avg_rating = trustpilot_df['rating'].mean()
            st.metric("Avg Trustpilot Rating", f"{avg_rating:.2f}/5")
        else:
            st.metric("Avg Rating", "N/A")

    st.divider()

    # Tabs for different review views
    review_tab1, review_tab2, review_tab3 = st.tabs(["📊 Analysis", "📝 Recent Reviews", "🔍 Correlation"])

    with review_tab1:
        render_review_analysis(restaurants_df, trustpilot_df)

    with review_tab2:
        render_recent_reviews(trustpilot_df, google_df)

    with review_tab3:
        render_correlation_analysis(restaurants_df)


def render_review_analysis(restaurants_df: pd.DataFrame, trustpilot_df: pd.DataFrame) -> None:
    """Render review analysis charts."""

    if trustpilot_df.empty:
        st.info("No Trustpilot reviews available.")
        return

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Rating Distribution")

        rating_counts = trustpilot_df['rating'].value_counts().sort_index()

        fig = px.bar(
            x=rating_counts.index,
            y=rating_counts.values,
            labels={'x': 'Rating', 'y': 'Number of Reviews'},
            title='Trustpilot Rating Distribution',
            color=rating_counts.index,
            color_continuous_scale=['#FF3722', '#FF8622', '#FFCE00', '#73CF11', '#00B67A']
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Reviews Over Time")

        reviews_by_month = trustpilot_df.copy()
        reviews_by_month['month'] = reviews_by_month['review_date'].dt.to_period('M').astype(str)
        monthly_counts = reviews_by_month.groupby('month').size().reset_index(name='count')

        fig = px.line(
            monthly_counts.tail(24),  # Last 24 months
            x='month',
            y='count',
            title='Monthly Review Volume (Last 24 Months)',
            labels={'month': 'Month', 'count': 'Reviews'}
        )
        st.plotly_chart(fig, use_container_width=True)

    # Top rated and bottom rated restaurants
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🏆 Highest Rated")

        top_rated = restaurants_df[restaurants_df['trustpilot_avg_rating'].notna()].nlargest(
            10, 'trustpilot_avg_rating'
        )[['name', 'trustpilot_avg_rating', 'trustpilot_review_count']]

        for _, row in top_rated.iterrows():
            badge = get_trustpilot_badge(row['trustpilot_avg_rating'], int(row['trustpilot_review_count']))
            st.markdown(f"**{row['name']}**: {badge}", unsafe_allow_html=True)

    with col2:
        st.subheader("📉 Lowest Rated")

        bottom_rated = restaurants_df[restaurants_df['trustpilot_avg_rating'].notna()].nsmallest(
            10, 'trustpilot_avg_rating'
        )[['name', 'trustpilot_avg_rating', 'trustpilot_review_count']]

        for _, row in bottom_rated.iterrows():
            badge = get_trustpilot_badge(row['trustpilot_avg_rating'], int(row['trustpilot_review_count']))
            st.markdown(f"**{row['name']}**: {badge}", unsafe_allow_html=True)


def render_recent_reviews(trustpilot_df: pd.DataFrame, google_df: pd.DataFrame) -> None:
    """Render recent reviews feed."""

    st.subheader("Recent Trustpilot Reviews")

    if trustpilot_df.empty:
        st.info("No reviews available.")
        return

    # Filters
    col1, col2, col3 = st.columns(3)

    with col1:
        restaurants = ['All'] + sorted(trustpilot_df['restaurant_name'].unique().tolist())
        selected_restaurant = st.selectbox("Restaurant", restaurants)

    with col2:
        rating_filter = st.selectbox("Rating", ['All', '5★', '4★', '3★', '2★', '1★'])

    with col3:
        limit = st.selectbox("Show", [10, 25, 50, 100])

    # Apply filters
    filtered = trustpilot_df.copy()

    if selected_restaurant != 'All':
        filtered = filtered[filtered['restaurant_name'] == selected_restaurant]

    if rating_filter != 'All':
        rating_val = int(rating_filter[0])
        filtered = filtered[filtered['rating'] == rating_val]

    # Display reviews
    for _, review in filtered.head(limit).iterrows():
        with st.container():
            col1, col2 = st.columns([4, 1])

            with col1:
                st.markdown(f"**{review['restaurant_name']}** - {review['author_name']}")
                if review.get('review_title'):
                    st.markdown(f"*{review['review_title']}*")
                if review.get('review_body'):
                    st.markdown(review['review_body'][:300] + ('...' if len(str(review['review_body'])) > 300 else ''))

            with col2:
                stars = '⭐' * int(review['rating'])
                st.markdown(f"{stars}")
                if pd.notna(review['review_date']):
                    st.caption(review['review_date'].strftime('%Y-%m-%d'))

            st.divider()


def render_correlation_analysis(restaurants_df: pd.DataFrame) -> None:
    """Render hygiene vs customer satisfaction correlation."""

    st.subheader("🔬 Hygiene vs Customer Satisfaction")

    # Get restaurants with both metrics
    both_metrics = restaurants_df[
        (restaurants_df['hygiene_rating'].notna()) &
        (restaurants_df['trustpilot_avg_rating'].notna())
    ].copy()

    if len(both_metrics) < 5:
        st.info("Not enough restaurants with both hygiene ratings and Trustpilot reviews for correlation analysis.")
        return

    st.markdown(f"**Analyzing {len(both_metrics)} restaurants with both metrics**")

    # Scatter plot
    fig = px.scatter(
        both_metrics,
        x='hygiene_rating',
        y='trustpilot_avg_rating',
        hover_name='name',
        title='Hygiene Rating vs Trustpilot Rating',
        labels={
            'hygiene_rating': 'FSA Hygiene Rating (★)',
            'trustpilot_avg_rating': 'Trustpilot Rating (★)'
        },
        color='hygiene_rating',
        color_continuous_scale='RdYlGn',
        size='trustpilot_review_count',
        size_max=30
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    # Key insight
    correlation = both_metrics['hygiene_rating'].corr(both_metrics['trustpilot_avg_rating'])

    if abs(correlation) < 0.3:
        insight = "weak"
    elif abs(correlation) < 0.6:
        insight = "moderate"
    else:
        insight = "strong"

    st.markdown(f"""
    **Key Finding**: There is a **{insight} correlation** ({correlation:.2f}) between hygiene ratings and
    customer satisfaction.

    This suggests that food safety compliance does {"not strongly predict" if abs(correlation) < 0.5 else "moderately predicts"}
    customer satisfaction - other factors like service quality, food taste, and value play significant roles.
    """)

    # Biggest gaps
    both_metrics['gap'] = both_metrics['hygiene_rating'] - both_metrics['trustpilot_avg_rating']

    st.markdown("**Biggest Gaps** (5★ hygiene but low reviews):")
    biggest_gaps = both_metrics[both_metrics['hygiene_rating'] == 5].nsmallest(5, 'trustpilot_avg_rating')

    for _, row in biggest_gaps.iterrows():
        st.markdown(f"- **{row['name']}**: 5★ hygiene, {row['trustpilot_avg_rating']:.1f}★ Trustpilot")
