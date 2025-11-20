#!/usr/bin/env python3
"""
Reorder Dashboard Tabs
======================
Moves Restaurant Profiles to tab 1.
"""

with open('dashboard_app.py', 'r') as f:
    content = f.read()

# Step 1: Reorder tab list
old_tabs = '''    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
        "🍽️ Browse Menus",
        "📊 Price Analytics",
        "🏪 Restaurant Comparison",
        "🎯 Competitor Analysis",
        "🍹 Drinks Analysis",
        "⭐ Hygiene Ratings",
        "💬 Reviews",
        "📈 Statistics",
        "🏢 Restaurant Profiles"
    ])'''

new_tabs = '''    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
        "🏢 Restaurant Profiles",
        "🍽️ Browse Menus",
        "📊 Price Analytics",
        "🏪 Restaurant Comparison",
        "🎯 Competitor Analysis",
        "🍹 Drinks Analysis",
        "⭐ Hygiene Ratings",
        "💬 Reviews",
        "📈 Statistics"
    ])'''

content = content.replace(old_tabs, new_tabs)

# Step 2: Replace tab references (use unique temp placeholders)
replacements = [
    ('with tab9:', 'with tabTEMP1:'),  # Restaurant Profiles
    ('with tab1:', 'with tabTEMP2:'),  # Browse Menus
    ('with tab2:', 'with tabTEMP3:'),  # Price Analytics
    ('with tab3:', 'with tabTEMP4:'),  # Restaurant Comparison
    ('with tab4:', 'with tabTEMP5:'),  # Competitor Analysis
    ('with tab5:', 'with tabTEMP6:'),  # Drinks Analysis
    ('with tab6:', 'with tabTEMP7:'),  # Hygiene Ratings
    ('with tab7:', 'with tabTEMP8:'),  # Reviews
    ('with tab8:', 'with tabTEMP9:'),  # Statistics
]

for old, new in replacements:
    content = content.replace(old, new)

# Step 3: Replace temp placeholders with final values
final_replacements = [
    ('with tabTEMP1:', 'with tab1:'),  # Restaurant Profiles → tab1
    ('with tabTEMP2:', 'with tab2:'),  # Browse Menus → tab2
    ('with tabTEMP3:', 'with tab3:'),  # Price Analytics → tab3
    ('with tabTEMP4:', 'with tab4:'),  # Restaurant Comparison → tab4
    ('with tabTEMP5:', 'with tab5:'),  # Competitor Analysis → tab5
    ('with tabTEMP6:', 'with tab6:'),  # Drinks Analysis → tab6
    ('with tabTEMP7:', 'with tab7:'),  # Hygiene Ratings → tab7
    ('with tabTEMP8:', 'with tab8:'),  # Reviews → tab8
    ('with tabTEMP9:', 'with tab9:'),  # Statistics → tab9
]

for old, new in final_replacements:
    content = content.replace(old, new)

# Step 4: Update comment labels
comment_replacements = [
    ('# Tab 9: Restaurant Profiles', '# Tab 1: Restaurant Profiles'),
    ('# Tab 1: Browse Menus', '# Tab 2: Browse Menus'),
    ('# Tab 2: Price Analytics', '# Tab 3: Price Analytics'),
    ('# Tab 3: Restaurant Comparison', '# Tab 4: Restaurant Comparison'),
    ('# Tab 4: Competitor Analysis', '# Tab 5: Competitor Analysis'),
    ('# Tab 5: Drinks Analysis', '# Tab 6: Drinks Analysis'),
    ('# Tab 6: Hygiene Ratings', '# Tab 7: Hygiene Ratings'),
    ('# Tab 7: Reviews', '# Tab 8: Reviews'),
    ('# Tab 8: Statistics', '# Tab 9: Statistics'),
]

for old, new in comment_replacements:
    content = content.replace(old, new)

with open('dashboard_app.py', 'w') as f:
    f.write(content)

print("✅ Tab reordering complete!")
print("\nNew tab order:")
print("  Tab 1: 🏢 Restaurant Profiles")
print("  Tab 2: 🍽️ Browse Menus")
print("  Tab 3: 📊 Price Analytics")
print("  Tab 4: 🏪 Restaurant Comparison")
print("  Tab 5: 🎯 Competitor Analysis")
print("  Tab 6: 🍹 Drinks Analysis")
print("  Tab 7: ⭐ Hygiene Ratings")
print("  Tab 8: 💬 Reviews")
print("  Tab 9: 📈 Statistics")
