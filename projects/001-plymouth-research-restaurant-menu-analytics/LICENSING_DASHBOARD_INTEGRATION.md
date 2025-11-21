# Licensing Data Dashboard Integration Guide

## Summary

Licensing data from Plymouth City Council is now available for 42 restaurants. This guide shows how to display it in the dashboard.

## Database Schema Added

New columns in `restaurants` table:
- `licensing_premises_id` - Plymouth licensing premises ID
- `licensing_premises_name` - Official name in licensing database
- `licensing_premises_address` - Official registered address
- `licensing_number` - License number (e.g., "PA0518")
- `licensing_url` - Link to official license page
- `licensing_dps_name` - Designated Premises Supervisor
- `licensing_activities` - JSON array of licensable activities
- `licensing_opening_hours` - JSON array of opening hours
- `licensing_scraped_at` - When data was collected
- `licensing_match_confidence` - Match confidence (0.0-1.0)

## Step 1: Add Helper Functions

Add these functions after the existing helper functions (around line 400):

```python
def get_licensing_badge(has_licensing: bool) -> str:
    """Get colored badge for licensing status."""
    if has_licensing:
        return '<span style="background: #4CAF50; color: white; padding: 2px 8px; border-radius: 3px; font-size: 0.85em;">✓ Licensed</span>'
    else:
        return '<span style="background: #9E9E9E; color: white; padding: 2px 8px; border-radius: 3px; font-size: 0.85em;">No License Data</span>'

def format_opening_hours(hours_json: str) -> str:
    """Format opening hours from JSON."""
    if not hours_json or hours_json == '[]':
        return "Not available"

    try:
        import json
        hours = json.loads(hours_json)
        if not hours:
            return "Not available"

        formatted = []
        for period in hours:
            days = period.get('days', '')
            time_from = period.get('time_from', '')
            time_to = period.get('time_to', '')

            if days and time_from and time_to:
                formatted.append(f"**{days}**: {time_from} - {time_to}")

        return "<br>".join(formatted) if formatted else "Not available"
    except:
        return "Error parsing hours"

def format_licensing_activities(activities_json: str) -> str:
    """Format licensing activities from JSON."""
    if not activities_json or activities_json == '[]':
        return "Not specified"

    try:
        import json
        activities = json.loads(activities_json)
        if not activities:
            return "Not specified"

        # Clean up empty strings
        activities = [a.strip() for a in activities if a and a.strip()]

        if not activities:
            return "Not specified"

        # Capitalize first letter
        activities = [a[0].upper() + a[1:] if a else a for a in activities]

        return "<br>• " + "<br>• ".join(activities)
    except:
        return "Error parsing activities"
```

## Step 2: Update Database Query

In the `get_restaurants_data()` function (around line 550), add the licensing columns to the SELECT query:

```python
def get_restaurants_data():
    """Fetch all restaurant data with caching."""
    conn = get_db_connection()

    query = """
        SELECT
            r.*,
            COUNT(DISTINCT m.item_id) as menu_item_count,
            -- ... existing columns ...
            r.licensing_premises_id,
            r.licensing_premises_name,
            r.licensing_premises_address,
            r.licensing_number,
            r.licensing_url,
            r.licensing_dps_name,
            r.licensing_activities,
            r.licensing_opening_hours,
            r.licensing_scraped_at,
            r.licensing_match_confidence
        FROM restaurants r
        -- ... rest of query ...
    """
```

## Step 3: Display Licensing Badge in Browse Menus Tab

In Tab 2 (Browse Menus), around line 800-850 where restaurant info is displayed, add:

```python
# Display licensing badge (after hygiene badge)
if pd.notna(restaurant_info.get('licensing_number')):
    license_badge = get_licensing_badge(True)
    st.markdown(f"{hygiene_badge} {license_badge}", unsafe_allow_html=True)

    # Show license number with link
    if pd.notna(restaurant_info.get('licensing_url')):
        st.markdown(
            f"📜 License: [{restaurant_info['licensing_number']}]({restaurant_info['licensing_url']}) "
            f"(Match: {restaurant_info.get('licensing_match_confidence', 0)*100:.0f}%)",
            unsafe_allow_html=True
        )
```

## Step 4: Add Licensing Section to Restaurant Profiles Tab

In Tab 8 (Restaurant Profiles), add a new expander for licensing information after the existing sections:

```python
# Licensing Information Section
if pd.notna(restaurant.get('licensing_number')):
    with st.expander("📜 Licensing Information", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### License Details")
            st.markdown(f"**License Number**: {restaurant['licensing_number']}")

            if pd.notna(restaurant.get('licensing_premises_id')):
                st.markdown(f"**Premises ID**: {restaurant['licensing_premises_id']}")

            if pd.notna(restaurant.get('licensing_url')):
                st.markdown(f"**Official License**: [View on Plymouth Council]({restaurant['licensing_url']})")

            if pd.notna(restaurant.get('licensing_dps_name')):
                # Clean up DPS name (sometimes has footer text)
                dps = restaurant['licensing_dps_name']
                if 'Copyright' not in dps and 'Idox' not in dps:
                    st.markdown(f"**Designated Premises Supervisor**: {dps}")

            if pd.notna(restaurant.get('licensing_match_confidence')):
                confidence = restaurant['licensing_match_confidence'] * 100
                st.markdown(f"**Match Confidence**: {confidence:.0f}%")

        with col2:
            st.markdown("### Licensable Activities")
            activities_html = format_licensing_activities(
                restaurant.get('licensing_activities', '[]')
            )
            st.markdown(activities_html, unsafe_allow_html=True)

        # Opening Hours (full width)
        st.markdown("### Official Opening Hours")
        hours_html = format_opening_hours(
            restaurant.get('licensing_opening_hours', '[]')
        )
        st.markdown(hours_html, unsafe_allow_html=True)

        # Official address
        if pd.notna(restaurant.get('licensing_premises_address')):
            st.markdown("### Official Registered Address")
            st.info(restaurant['licensing_premises_address'])

        # Data attribution
        st.caption(
            "Data from Plymouth City Council Licensing Register. "
            f"Scraped: {pd.to_datetime(restaurant.get('licensing_scraped_at')).strftime('%Y-%m-%d') if pd.notna(restaurant.get('licensing_scraped_at')) else 'Unknown'}"
        )
else:
    with st.expander("📜 Licensing Information", expanded=False):
        st.info("No licensing data available for this restaurant.")
        st.caption(
            "This restaurant may not require a premises license, or the data "
            "has not been matched yet. Check unmatched_licensing.json for manual matching."
        )
```

## Step 5: Add Licensing Statistics to Statistics Tab

In Tab 10 (Statistics), add licensing metrics:

```python
# Licensing Statistics
st.markdown("### 📜 Licensing Data")

col1, col2, col3, col4 = st.columns(4)

with col1:
    licensed_count = restaurants_df['licensing_number'].notna().sum()
    st.metric("Licensed Restaurants", licensed_count)

with col2:
    license_coverage = (licensed_count / len(restaurants_df) * 100)
    st.metric("License Coverage", f"{license_coverage:.1f}%")

with col3:
    avg_hours = restaurants_df[restaurants_df['licensing_opening_hours'].notna()]['licensing_opening_hours'].apply(
        lambda x: len(json.loads(x)) if x and x != '[]' else 0
    ).mean()
    st.metric("Avg Opening Periods", f"{avg_hours:.1f}")

with col4:
    alcohol_licenses = restaurants_df[restaurants_df['licensing_activities'].notna()]['licensing_activities'].apply(
        lambda x: 'alcohol' in str(x).lower() if x else False
    ).sum()
    st.metric("Alcohol Licenses", alcohol_licenses)
```

## Testing

After making these changes:

1. Restart the dashboard: `streamlit run dashboard_app.py`
2. Navigate to Tab 8 (Restaurant Profiles)
3. Select a restaurant with licensing data (e.g., "Himalayan Spice")
4. Verify the licensing expander shows:
   - License number with link
   - Opening hours (formatted nicely)
   - Licensable activities
   - Official address

## Example Output

For **Himalayan Spice** (License PA0518), you should see:

**License Details:**
- License Number: PA0518
- Premises ID: 644
- Official License: [View on Plymouth Council](link)
- Match Confidence: 100%

**Licensable Activities:**
• Sale and supply of alcohol

**Official Opening Hours:**
- **Monday to Saturday**: 10:00 - 00:00
- **Sunday**: 12:00 - 23:30

**Official Registered Address:**
31 New Street, Plymouth, Devon, PL1 2NA

## Files Created

1. `add_licensing_columns.sql` - Database schema
2. `import_licensing_data.py` - Data import script
3. `restaurant_licensing_data.json` - 42 matched restaurants
4. `unmatched_licensing.json` - 201 restaurants for manual review
5. `plymouth_licensing_premises_list.json` - All 2,232 Plymouth premises

## Data Quality Notes

- 42/243 restaurants (17.3%) automatically matched
- Match confidence ranges from 80% to 100%
- Some DPS names contain footer text (filter with "Copyright" check)
- Opening hours are official registered hours (may differ from actual practice)

## Future Enhancements

1. Manual matching of the 201 unmatched restaurants
2. Add opening hours comparison (Google vs Licensing)
3. License expiry date tracking
4. Alert for licenses requiring renewal
5. Map overlay showing licensed vs unlicensed premises
