#!/usr/bin/env python3
"""
Interactive Data Matcher - Streamlit Web App

Web-based interface for manually reviewing and selecting matches for restaurants
with missing data. Shows top 5 potential matches with visual scoring.

Author: Claude Code
Date: 2025-11-22
"""

import streamlit as st
import sqlite3
import json
import re
import difflib
from pathlib import Path
from typing import List, Dict, Optional
import pandas as pd
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Interactive Data Matcher",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Utility functions
def normalize_business_name(name: str) -> str:
    """Normalize business name for better matching."""
    if not name or pd.isna(name):
        return ""

    name = str(name).upper().strip()

    corporate_patterns = [
        r'\s+LIMITED\s*$', r'\s+LTD\.?\s*$', r'\s+PLC\.?\s*$',
        r'\s+HOLDINGS?\s*$', r'\s+\(UK\)\s*$', r'\s+UK\s*$',
        r'\s+GROUP\s*$', r'\s+RESTAURANTS?\s*$',
    ]
    for pattern in corporate_patterns:
        name = re.sub(pattern, '', name, flags=re.IGNORECASE)

    location_patterns = [
        r'\s+PLYMOUTH\s*$', r'\s+\(PLYMOUTH\)\s*$', r'\s+-\s+PLYMOUTH\s*$',
    ]
    for pattern in location_patterns:
        name = re.sub(pattern, '', name, flags=re.IGNORECASE)

    name = re.sub(r'[^\w\s&#]', '', name)
    name = re.sub(r'\s+', ' ', name).strip()

    return name

def calculate_name_similarity(name1: str, name2: str) -> float:
    """Calculate similarity between two names (0-100)."""
    norm1 = normalize_business_name(name1)
    norm2 = normalize_business_name(name2)

    if not norm1 or not norm2:
        return 0.0

    return difflib.SequenceMatcher(None, norm1, norm2).ratio() * 100

def extract_postcode(text: str) -> Optional[str]:
    """Extract UK postcode from text."""
    if not text:
        return None

    pattern = r'[A-Z]{1,2}\d{1,2}\s?\d[A-Z]{2}'
    match = re.search(pattern, text.upper())

    if match:
        postcode = match.group(0).replace(' ', '')
        return f"{postcode[:-3]} {postcode[-3:]}"

    return None

@st.cache_data
def load_unmatched_restaurants(data_source: str) -> pd.DataFrame:
    """Load unmatched restaurants for selected data source with Google Places data."""
    # Load unmatched restaurants
    if data_source == 'licensing':
        unmatched_df = pd.read_csv('data/processed/licensing_unmatched.csv')
    elif data_source == 'business_rates':
        unmatched_df = pd.read_csv('data/processed/business_rates_unmatched.csv')
    elif data_source == 'fsa':
        unmatched_df = pd.read_csv('data/processed/fsa_hygiene_unmatched.csv')

    # Enrich with Google Places data from database
    conn = sqlite3.connect('plymouth_research.db')

    restaurant_ids = ','.join(str(int(id)) for id in unmatched_df['restaurant_id'].tolist())

    query = f"""
        SELECT
            restaurant_id,
            google_formatted_address,
            google_latitude,
            google_longitude,
            google_phone_national,
            website_url,
            postcode as db_postcode,
            address as db_address
        FROM restaurants
        WHERE restaurant_id IN ({restaurant_ids})
    """

    google_df = pd.read_sql_query(query, conn)
    conn.close()

    # Merge with unmatched data
    enriched_df = unmatched_df.merge(google_df, on='restaurant_id', how='left')

    return enriched_df

@st.cache_data
def load_source_data(data_source: str):
    """Load source data for matching."""
    if data_source == 'licensing':
        with open('data/raw/plymouth_licensing_complete_fixed.json', 'r') as f:
            return json.load(f)
    elif data_source == 'business_rates':
        df = pd.read_csv('data/raw/plymouth_business_rates_source.csv')
        return df.to_dict('records')
    elif data_source == 'fsa':
        import xml.etree.ElementTree as ET

        # Parse FSA XML file
        tree = ET.parse('data/raw/plymouth_fsa_data.xml')
        root = tree.getroot()

        establishments = []

        for est_elem in root.findall('.//EstablishmentDetail'):
            # Get business type
            business_type = est_elem.find('BusinessType')
            business_type_text = business_type.text if business_type is not None else ''

            # Filter for restaurants/cafes/pubs/bars
            if not any(keyword in business_type_text.lower() for keyword in
                      ['restaurant', 'cafe', 'canteen', 'pub', 'bar', 'nightclub']):
                continue

            def get_text(elem, tag):
                node = elem.find(tag)
                return node.text if node is not None and node.text else ''

            # Get rating
            rating_value = get_text(est_elem, 'RatingValue')
            if rating_value in ['AwaitingInspection', 'Awaiting Inspection', 'Exempt']:
                rating_numeric = None
            else:
                try:
                    rating_numeric = int(rating_value) if rating_value else None
                except ValueError:
                    rating_numeric = None

            # Get scores
            scores_elem = est_elem.find('Scores')
            if scores_elem is not None:
                hygiene_score = get_text(scores_elem, 'Hygiene')
                structural_score = get_text(scores_elem, 'Structural')
                confidence_score = get_text(scores_elem, 'ConfidenceInManagement')
            else:
                hygiene_score = structural_score = confidence_score = None

            # Build address
            address_line1 = get_text(est_elem, 'AddressLine1')
            address_line2 = get_text(est_elem, 'AddressLine2')
            address_line3 = get_text(est_elem, 'AddressLine3')
            address_line4 = get_text(est_elem, 'AddressLine4')
            address_parts = [address_line1, address_line2, address_line3, address_line4]
            full_address = ', '.join([p for p in address_parts if p])

            establishment = {
                'fsa_id': int(get_text(est_elem, 'FHRSID')),
                'business_name': get_text(est_elem, 'BusinessName'),
                'business_type': business_type_text,
                'address': full_address,
                'address_line1': address_line1,
                'address_line2': address_line2,
                'address_line3': address_line3,
                'address_line4': address_line4,
                'postcode': get_text(est_elem, 'PostCode'),
                'rating': rating_numeric,
                'rating_date': get_text(est_elem, 'RatingDate'),
                'hygiene_score': int(hygiene_score) if hygiene_score else None,
                'structural_score': int(structural_score) if structural_score else None,
                'confidence_score': int(confidence_score) if confidence_score else None,
                'business_type_text': business_type_text,
                'local_authority': get_text(est_elem, 'LocalAuthorityName'),
            }

            establishments.append(establishment)

        return establishments

def find_top_matches(restaurant: Dict, source_data: List[Dict], data_source: str, n: int = 5) -> List[Dict]:
    """Find top N matches for a restaurant."""
    rest_name = restaurant['restaurant_name']

    # Prefer Google Places data for address and postcode
    google_address = restaurant.get('google_formatted_address', '')
    rest_address = restaurant.get('restaurant_address', '')
    rest_postcode = restaurant.get('restaurant_postcode', '')

    # Use Google address if available, fallback to basic address
    if pd.notna(google_address) and google_address:
        rest_address = str(google_address)
        # Extract postcode from Google address if basic postcode is missing
        if pd.isna(rest_postcode) or not rest_postcode:
            rest_postcode = extract_postcode(google_address) or ''
    else:
        # Handle NaN values for basic address
        if pd.isna(rest_address):
            rest_address = ''
        else:
            rest_address = str(rest_address)

    # Handle NaN for postcode
    if pd.isna(rest_postcode):
        rest_postcode = ''
    else:
        rest_postcode = str(rest_postcode)

    matches = []

    for source_item in source_data:
        if data_source == 'licensing':
            source_name = source_item.get('name', '')
            source_address = source_item.get('address', '')
        elif data_source == 'business_rates':
            source_name = source_item.get('Account Holder', '')
            source_address = source_item.get('Full Property Address', '')
        elif data_source == 'fsa':
            source_name = source_item.get('business_name', '')
            source_address = source_item.get('address', '')
        else:
            continue

        # Calculate similarity
        name_sim = calculate_name_similarity(rest_name, source_name)

        # Address similarity
        addr_score = 0
        if rest_address and source_address:
            rest_words = set(normalize_business_name(rest_address).split())
            source_words = set(normalize_business_name(source_address).split())
            common = rest_words & source_words
            addr_score = len(common) * 5

        # Postcode match
        postcode_match = False
        source_postcode = extract_postcode(source_address)
        if rest_postcode and source_postcode:
            if rest_postcode.replace(' ', '').upper() == source_postcode.replace(' ', '').upper():
                postcode_match = True

        total_score = name_sim + addr_score + (30 if postcode_match else 0)

        matches.append({
            'source_item': source_item,
            'source_name': source_name,
            'source_address': source_address,
            'source_postcode': source_postcode,
            'name_similarity': name_sim,
            'address_score': addr_score,
            'postcode_match': postcode_match,
            'total_score': total_score
        })

    matches.sort(key=lambda x: x['total_score'], reverse=True)
    return matches[:n]

def save_match(restaurant: Dict, selected_match: Dict, data_source: str):
    """Save a verified match to session state."""
    if 'verified_matches' not in st.session_state:
        st.session_state.verified_matches = []

    match_record = {
        'restaurant_id': restaurant['restaurant_id'],
        'restaurant_name': restaurant['restaurant_name'],
        'restaurant_address': restaurant.get('restaurant_address', ''),
        'restaurant_postcode': restaurant.get('restaurant_postcode', ''),
        'match_confidence': selected_match['total_score'],
        'match_reason': 'manual_selection',
        'matched_at': datetime.now().isoformat(),
    }

    if data_source == 'licensing':
        source_item = selected_match['source_item']
        details = source_item.get('details', {})
        match_record.update({
            'premises_id': source_item.get('premises_id'),
            'premises_name': source_item.get('name'),
            'premises_address': source_item.get('address'),
            'license_number': details.get('license_number'),
            'license_url': details.get('license_url'),
            'dps_name': details.get('dps_name'),
            'licensable_activities': json.dumps(details.get('licensable_activities', [])),
            'opening_hours': json.dumps(details.get('opening_hours', [])),
        })
    elif data_source == 'business_rates':
        source_item = selected_match['source_item']
        match_record.update({
            'business_rates_account_holder': source_item.get('Account Holder'),
            'business_rates_address': source_item.get('Full Property Address'),
            'business_rates_postcode': source_item.get('Postcode'),
            'business_rates_rateable_value': source_item.get('Rateable Value 2023'),
            'business_rates_category': source_item.get('Primary Liable party Description'),
        })
    elif data_source == 'fsa':
        source_item = selected_match['source_item']
        match_record.update({
            'fsa_id': source_item.get('fsa_id'),
            'fsa_business_name': source_item.get('business_name'),
            'fsa_address': source_item.get('address'),
            'fsa_address_line1': source_item.get('address_line1'),
            'fsa_address_line2': source_item.get('address_line2'),
            'fsa_address_line3': source_item.get('address_line3'),
            'fsa_address_line4': source_item.get('address_line4'),
            'fsa_postcode': source_item.get('postcode'),
            'hygiene_rating': source_item.get('rating'),
            'hygiene_rating_date': source_item.get('rating_date'),
            'hygiene_score_hygiene': source_item.get('hygiene_score'),
            'hygiene_score_structural': source_item.get('structural_score'),
            'hygiene_score_confidence': source_item.get('confidence_score'),
            'fsa_business_type': source_item.get('business_type_text'),
            'fsa_local_authority': source_item.get('local_authority'),
        })

    st.session_state.verified_matches.append(match_record)

def export_matches(data_source: str):
    """Export verified matches to CSV."""
    if 'verified_matches' not in st.session_state or not st.session_state.verified_matches:
        return None

    df = pd.DataFrame(st.session_state.verified_matches)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'{data_source}_manual_matches_{timestamp}.csv'

    return df, filename

# Main app
def main():
    st.title("🔗 Interactive Data Matcher")
    st.markdown("Manually review and select matches for restaurants with missing data")

    # Sidebar - Data source selection
    with st.sidebar:
        st.header("⚙️ Configuration")

        data_source = st.selectbox(
            "Data Source",
            options=['licensing', 'fsa', 'business_rates'],
            format_func=lambda x: {
                'licensing': '📋 Licensing Data',
                'fsa': '🏥 FSA Hygiene Ratings',
                'business_rates': '💷 Business Rates',
            }[x]
        )

        st.divider()
        st.header("📊 Session Progress")

        if 'current_index' not in st.session_state:
            st.session_state.current_index = 0
        if 'verified_matches' not in st.session_state:
            st.session_state.verified_matches = []
        if 'skipped' not in st.session_state:
            st.session_state.skipped = []

        # Load data
        unmatched_df = load_unmatched_restaurants(data_source)
        total_unmatched = len(unmatched_df)

        st.metric("Total Unmatched", total_unmatched)
        st.metric("Current Position", f"{st.session_state.current_index + 1}/{total_unmatched}")
        st.metric("Verified Matches", len(st.session_state.verified_matches))
        st.metric("Skipped", len(st.session_state.skipped))

        progress = (st.session_state.current_index / total_unmatched) if total_unmatched > 0 else 0
        st.progress(progress)

        st.divider()

        # Export button
        if st.session_state.verified_matches:
            if st.button("💾 Export Verified Matches", type="primary", use_container_width=True):
                df, filename = export_matches(data_source)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=filename,
                    mime='text/csv',
                    use_container_width=True
                )
                st.success(f"✓ Ready to download {len(df)} matches")

        # Reset button
        if st.button("🔄 Reset Session", use_container_width=True):
            st.session_state.current_index = 0
            st.session_state.verified_matches = []
            st.session_state.skipped = []
            st.rerun()

    # Main content
    if st.session_state.current_index >= total_unmatched:
        st.success("🎉 All restaurants reviewed!")
        st.balloons()

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Verified Matches", len(st.session_state.verified_matches))
        with col2:
            st.metric("Skipped", len(st.session_state.skipped))

        if st.session_state.verified_matches:
            df, filename = export_matches(data_source)
            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download Verified Matches CSV",
                data=csv,
                file_name=filename,
                mime='text/csv'
            )
        return

    # Get current restaurant
    current_restaurant = unmatched_df.iloc[st.session_state.current_index].to_dict()

    # Display restaurant info
    st.header(f"Restaurant {st.session_state.current_index + 1}/{total_unmatched}")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader(current_restaurant['restaurant_name'])

        # Show Google Places address prominently
        google_address = current_restaurant.get('google_formatted_address', '')
        if pd.notna(google_address) and google_address:
            st.success(f"📍 **Google Address**: {google_address}")
        else:
            st.text(f"📍 {current_restaurant.get('restaurant_address', 'N/A')}")
            st.text(f"📮 {current_restaurant.get('restaurant_postcode', 'N/A')}")

        # Show phone if available
        phone = current_restaurant.get('google_phone_national', '')
        if pd.notna(phone) and phone:
            st.caption(f"📞 {phone}")

        st.caption(f"ID: {current_restaurant['restaurant_id']}")

    with col2:
        # Show coordinates if available
        lat = current_restaurant.get('google_latitude', '')
        lon = current_restaurant.get('google_longitude', '')

        if pd.notna(lat) and pd.notna(lon) and lat and lon:
            st.caption(f"📌 Coordinates:")
            st.caption(f"{lat}, {lon}")

            # Show map link
            maps_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
            st.markdown(f"[🗺️ View on Google Maps]({maps_url})")

    # Find top matches
    source_data = load_source_data(data_source)
    top_matches = find_top_matches(current_restaurant, source_data, data_source, n=5)

    # Display matches
    st.divider()
    st.subheader("Top 5 Potential Matches")

    if not top_matches:
        st.warning("No potential matches found")
    else:
        for i, match in enumerate(top_matches, 1):
            with st.container():
                # Score badge
                score = match['total_score']
                if score >= 90:
                    badge_color = "🟢"
                    confidence = "Very High"
                elif score >= 80:
                    badge_color = "🟡"
                    confidence = "High"
                elif score >= 70:
                    badge_color = "🟠"
                    confidence = "Medium"
                else:
                    badge_color = "🔴"
                    confidence = "Low"

                col1, col2, col3 = st.columns([3, 1, 1])

                with col1:
                    st.markdown(f"### {badge_color} Match {i}: {match['source_name']}")
                    st.text(f"📍 {match['source_address']}")

                    # Show specific details
                    if data_source == 'licensing':
                        details = match['source_item'].get('details', {})
                        license_num = details.get('license_number', 'N/A')
                        activities = details.get('licensable_activities', [])
                        st.caption(f"License: {license_num}")
                        if activities:
                            st.caption(f"Activities: {', '.join(activities[:3])}")

                    elif data_source == 'business_rates':
                        rv = match['source_item'].get('Rateable Value 2023', 'N/A')
                        category = match['source_item'].get('Primary Liable party Description', 'N/A')
                        if rv != 'N/A':
                            st.caption(f"💷 Rateable Value: £{int(float(rv)):,}")
                        st.caption(f"Category: {category}")

                    elif data_source == 'fsa':
                        source_item = match['source_item']
                        rating = source_item.get('rating')
                        business_type = source_item.get('business_type_text', 'N/A')
                        rating_date = source_item.get('rating_date', 'N/A')

                        if rating is not None:
                            stars = '⭐' * rating
                            st.caption(f"🏥 Hygiene Rating: {stars} ({rating}/5)")
                        else:
                            st.caption("🏥 Hygiene Rating: Awaiting Inspection")

                        st.caption(f"Type: {business_type}")
                        if rating_date != 'N/A':
                            st.caption(f"Rated: {rating_date[:10]}")

                with col2:
                    st.metric("Score", f"{score:.1f}", help=f"{confidence} confidence")
                    st.caption(f"Name: {match['name_similarity']:.0f}%")
                    st.caption(f"Postcode: {'✓' if match['postcode_match'] else '✗'}")
                    st.caption(f"Address: {match['address_score']}")

                with col3:
                    if st.button(f"✓ Select", key=f"select_{i}", use_container_width=True):
                        save_match(current_restaurant, match, data_source)
                        st.session_state.current_index += 1
                        st.success(f"✓ Match #{i} selected!")
                        st.rerun()

                st.divider()

    # Action buttons
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("⏭️ Skip (None Match)", use_container_width=True):
            st.session_state.skipped.append(current_restaurant)
            st.session_state.current_index += 1
            st.rerun()

    with col2:
        if st.button("⏮️ Previous", use_container_width=True, disabled=(st.session_state.current_index == 0)):
            st.session_state.current_index -= 1
            st.rerun()

    with col3:
        if st.button("⏭️ Next (Review Later)", use_container_width=True):
            st.session_state.current_index += 1
            st.rerun()

if __name__ == "__main__":
    main()
