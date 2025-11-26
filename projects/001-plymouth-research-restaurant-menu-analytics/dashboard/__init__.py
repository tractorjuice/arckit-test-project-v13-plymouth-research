"""
Dashboard Layer for Plymouth Research
======================================

Modular Streamlit dashboard for restaurant menu analytics.

Components:
- app.py: Main entry point and page routing
- data_loader.py: Cached data loading functions
- components/: Reusable UI components (sidebar, metrics, formatters)
- tabs/: Individual tab implementations
"""

from .data_loader import DataLoader

__all__ = ['DataLoader']
