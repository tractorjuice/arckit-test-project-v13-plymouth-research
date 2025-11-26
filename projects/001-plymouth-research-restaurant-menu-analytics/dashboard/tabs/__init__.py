"""
Dashboard Tabs
==============

Individual tab implementations for the dashboard.
"""

from .overview import render_overview_tab
from .menus import render_menus_tab
from .prices import render_prices_tab
from .hygiene import render_hygiene_tab
from .reviews import render_reviews_tab
from .map_tab import render_map_tab

__all__ = [
    'render_overview_tab',
    'render_menus_tab',
    'render_prices_tab',
    'render_hygiene_tab',
    'render_reviews_tab',
    'render_map_tab',
]
