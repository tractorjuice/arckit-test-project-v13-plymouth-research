"""
Price Analysis Tab
==================

Price analytics and comparisons.

Author: Plymouth Research Team
Date: 2025-11-26
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def render_prices_tab(
    restaurants_df: pd.DataFrame,
    menu_df: pd.DataFrame,
) -> None:
    """
    Render the price analysis tab.

    Args:
        restaurants_df: Filtered restaurant data
        menu_df: Filtered menu items data
    """
    st.header("💰 Price Analysis")

    if menu_df['price_gbp'].isna().all():
        st.warning("No price data available for the filtered items.")
        return

    # Filter to items with prices
    priced_items = menu_df.dropna(subset=['price_gbp'])

    # Summary statistics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Min Price", f"£{priced_items['price_gbp'].min():.2f}")

    with col2:
        st.metric("Max Price", f"£{priced_items['price_gbp'].max():.2f}")

    with col3:
        st.metric("Median Price", f"£{priced_items['price_gbp'].median():.2f}")

    with col4:
        st.metric("Avg Price", f"£{priced_items['price_gbp'].mean():.2f}")

    st.divider()

    # Charts row 1
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Price Distribution")

        fig = px.histogram(
            priced_items,
            x='price_gbp',
            nbins=30,
            title='Distribution of Menu Item Prices',
            labels={'price_gbp': 'Price (£)', 'count': 'Number of Items'},
            color_discrete_sequence=['#4CAF50']
        )
        fig.add_vline(
            x=priced_items['price_gbp'].mean(),
            line_dash="dash",
            annotation_text=f"Mean: £{priced_items['price_gbp'].mean():.2f}"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Price by Cuisine")

        avg_by_cuisine = priced_items.groupby('cuisine_type')['price_gbp'].agg(['mean', 'count']).reset_index()
        avg_by_cuisine.columns = ['Cuisine', 'Average Price', 'Item Count']
        avg_by_cuisine = avg_by_cuisine.sort_values('Average Price', ascending=True)

        fig = px.bar(
            avg_by_cuisine,
            x='Average Price',
            y='Cuisine',
            orientation='h',
            title='Average Price by Cuisine Type',
            labels={'Average Price': 'Average Price (£)'},
            color='Average Price',
            color_continuous_scale='RdYlGn_r'
        )
        st.plotly_chart(fig, use_container_width=True)

    # Charts row 2
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Price by Category")

        avg_by_category = priced_items.groupby('category')['price_gbp'].agg(['mean', 'count']).reset_index()
        avg_by_category.columns = ['Category', 'Average Price', 'Item Count']
        avg_by_category = avg_by_category.sort_values('Average Price', ascending=False)

        fig = px.bar(
            avg_by_category,
            x='Category',
            y='Average Price',
            title='Average Price by Menu Category',
            labels={'Average Price': 'Average Price (£)'},
            color='Average Price',
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Price Range Distribution")

        # Create price range buckets
        bins = [0, 5, 10, 15, 20, 30, 50, 100, float('inf')]
        labels = ['£0-5', '£5-10', '£10-15', '£15-20', '£20-30', '£30-50', '£50-100', '£100+']
        priced_items = priced_items.copy()
        priced_items['price_bucket'] = pd.cut(priced_items['price_gbp'], bins=bins, labels=labels, right=False)

        bucket_counts = priced_items['price_bucket'].value_counts().sort_index()

        fig = px.pie(
            values=bucket_counts.values,
            names=bucket_counts.index,
            title='Menu Items by Price Range',
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)

    # Most expensive items
    st.subheader("🏆 Most Expensive Items")

    top_expensive = priced_items.nlargest(10, 'price_gbp')[['item_name', 'restaurant_name', 'category', 'price_gbp']]
    top_expensive.columns = ['Item', 'Restaurant', 'Category', 'Price']
    top_expensive['Price'] = top_expensive['Price'].apply(lambda x: f"£{x:.2f}")

    st.dataframe(top_expensive, use_container_width=True, hide_index=True)

    # Best value items (by category)
    st.subheader("💎 Best Value (Lowest Prices by Category)")

    best_value = priced_items.loc[
        priced_items.groupby('category')['price_gbp'].idxmin()
    ][['item_name', 'restaurant_name', 'category', 'price_gbp']]
    best_value.columns = ['Item', 'Restaurant', 'Category', 'Price']
    best_value['Price'] = best_value['Price'].apply(lambda x: f"£{x:.2f}")

    st.dataframe(best_value, use_container_width=True, hide_index=True)
