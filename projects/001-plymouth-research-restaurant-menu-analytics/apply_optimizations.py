#!/usr/bin/env python3
"""
Apply Dashboard Optimizations (Fixed)
======================================

Applies performance optimizations with correct syntax.
"""

import re

with open('dashboard_app.py', 'r') as f:
    content = f.read()

print("Applying optimizations...")

# 1. Change ttl=300 to ttl=3600 (outside parentheses)
content = re.sub(r'@st\.cache_data\(ttl=300\)', '@st.cache_data(ttl=3600)  # 1 hour cache', content)

# 2. Add company columns to load_restaurants SELECT
old_select = """            google_review_count,
            google_avg_rating
        FROM restaurants"""

new_select = """            google_review_count,
            google_avg_rating,
            company_number,
            company_name,
            company_status,
            company_type,
            incorporation_date,
            company_registered_address,
            company_sic_codes
        FROM restaurants"""

content = content.replace(old_select, new_select)

# 3. Add load_directors function after load_dietary_tags
insert_marker = """@st.cache_data(ttl=3600)  # 1 hour cache
def load_dietary_tags() -> pd.DataFrame:
    \"\"\"Load menu items with dietary tags.\"\"\"
    conn = get_database_connection()
    query = \"\"\"
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
    \"\"\"
    df = pd.read_sql_query(query, conn)
    return df"""

new_directors_func = """

@st.cache_data(ttl=3600)  # 1 hour cache
def load_directors() -> pd.DataFrame:
    \"\"\"Load all active directors from Companies House.\"\"\"
    conn = get_database_connection()
    query = \"\"\"
        SELECT
            director_id,
            restaurant_id,
            company_number,
            director_name,
            officer_role,
            appointed_date,
            nationality,
            occupation
        FROM company_directors
        WHERE resigned_date IS NULL OR resigned_date = ''
        ORDER BY restaurant_id, appointed_date
    \"\"\"
    df = pd.read_sql_query(query, conn)
    return df"""

if insert_marker in content:
    content = content.replace(insert_marker, insert_marker + new_directors_func)
    print("✓ Added load_directors() function")
else:
    print("✗ Could not find insert marker for load_directors()")

# 4. Replace inline directors query with cached version
old_query = """                # Directors
                directors_query = pd.read_sql_query(\"\"\"
                    SELECT director_name, officer_role, appointed_date, nationality, occupation
                    FROM company_directors
                    WHERE restaurant_id = ?
                    AND resigned_date IS NULL OR resigned_date = ''
                    ORDER BY appointed_date
                \"\"\", conn, params=(restaurant_id,))

                if not directors_query.empty:"""

new_query = """                # Directors (using cached data)
                all_directors = load_directors()
                directors_query = all_directors[all_directors['restaurant_id'] == restaurant_id]

                if not directors_query.empty:"""

if old_query in content:
    content = content.replace(old_query, new_query)
    print("✓ Replaced inline directors query with cached version")
else:
    print("✗ Could not find inline directors query")

# Write optimized file
with open('dashboard_app.py', 'w') as f:
    f.write(content)

print("\n✅ Optimizations applied!")
print("   • Cache TTL: 5 min → 1 hour")
print("   • Company data: Added to load_restaurants()")
print("   • Directors: New cached function + optimized query")
