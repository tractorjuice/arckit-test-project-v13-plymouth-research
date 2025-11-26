"""
Formatting Functions
====================

HTML/text formatters for ratings, badges, and other display elements.

Author: Plymouth Research Team
Date: 2025-11-26
"""

import json
from typing import Optional
import pandas as pd


def format_hygiene_rating(rating: float, include_text: bool = False) -> str:
    """
    Format hygiene rating with stars and color.

    Args:
        rating: Hygiene rating (0-5)
        include_text: Whether to include descriptive text

    Returns:
        HTML formatted rating string
    """
    if pd.isna(rating):
        return "Not rated"

    rating = int(rating)
    stars = "⭐" * rating if rating > 0 else "❌"

    # Color coding
    if rating >= 5:
        color = "#4CAF50"  # Green
        text = "Very Good"
    elif rating >= 4:
        color = "#8BC34A"  # Light Green
        text = "Good"
    elif rating >= 3:
        color = "#FFC107"  # Yellow
        text = "Satisfactory"
    elif rating >= 2:
        color = "#FF9800"  # Orange
        text = "Improvement Necessary"
    elif rating >= 1:
        color = "#FF5722"  # Deep Orange
        text = "Major Improvement"
    else:
        color = "#F44336"  # Red
        text = "Urgent Improvement"

    if include_text:
        return f'<span style="color: {color}; font-weight: bold;">{stars} {text}</span>'
    else:
        return f'<span style="color: {color};">{stars}</span>'


def get_hygiene_badge(rating: float) -> str:
    """Get colored badge for hygiene rating."""
    if pd.isna(rating):
        return '<span style="background: #9E9E9E; color: white; padding: 2px 8px; border-radius: 3px; font-size: 0.85em;">No Rating</span>'

    rating = int(rating)

    if rating >= 5:
        bg_color = "#4CAF50"
        label = "5★ Very Good"
    elif rating >= 4:
        bg_color = "#8BC34A"
        label = "4★ Good"
    elif rating >= 3:
        bg_color = "#FFC107"
        label = "3★ Satisfactory"
    elif rating >= 2:
        bg_color = "#FF9800"
        label = "2★ Improvement Needed"
    elif rating >= 1:
        bg_color = "#FF5722"
        label = "1★ Major Improvement"
    else:
        bg_color = "#F44336"
        label = "0★ Urgent Action"

    return f'<span style="background: {bg_color}; color: white; padding: 2px 8px; border-radius: 3px; font-size: 0.85em;">{label}</span>'


def format_trustpilot_rating(rating: float, include_text: bool = False) -> str:
    """
    Format Trustpilot rating with stars and color.

    Args:
        rating: Trustpilot rating (1-5)
        include_text: Whether to include descriptive text

    Returns:
        HTML formatted rating string
    """
    if pd.isna(rating):
        return "No reviews"

    rating_int = int(rating)
    stars = "⭐" * rating_int

    # Color coding
    if rating >= 4.5:
        color = "#4CAF50"
        text = "Excellent"
    elif rating >= 3.5:
        color = "#8BC34A"
        text = "Good"
    elif rating >= 2.5:
        color = "#FFC107"
        text = "Average"
    elif rating >= 1.5:
        color = "#FF9800"
        text = "Below Average"
    else:
        color = "#F44336"
        text = "Poor"

    if include_text:
        return f'<span style="color: {color}; font-weight: bold;">{stars} {rating:.1f}/5 ({text})</span>'
    else:
        return f'<span style="color: {color};">{stars} {rating:.1f}/5</span>'


def format_google_rating(rating: float, include_text: bool = False) -> str:
    """
    Format Google rating with stars and color.

    Args:
        rating: Google rating (1-5)
        include_text: Whether to include descriptive text

    Returns:
        HTML formatted rating string
    """
    if pd.isna(rating):
        return "No reviews"

    rating_int = int(rating)
    stars = "⭐" * rating_int

    # Color coding (Google style)
    if rating >= 4.5:
        color = "#0F9D58"  # Google Green
        text = "Excellent"
    elif rating >= 3.5:
        color = "#4CAF50"
        text = "Good"
    elif rating >= 2.5:
        color = "#FFC107"
        text = "Average"
    elif rating >= 1.5:
        color = "#FF9800"
        text = "Below Average"
    else:
        color = "#F44336"
        text = "Poor"

    if include_text:
        return f'<span style="color: {color}; font-weight: bold;">{stars} {rating:.1f}/5 ({text})</span>'
    else:
        return f'<span style="color: {color};">{stars} {rating:.1f}/5</span>'


def get_trustpilot_badge(rating: float, review_count: Optional[int] = None) -> str:
    """Get colored badge for Trustpilot rating."""
    if pd.isna(rating):
        return '<span style="background: #9E9E9E; color: white; padding: 2px 8px; border-radius: 3px; font-size: 0.85em;">No Reviews</span>'

    if rating >= 4.5:
        bg_color = "#00B67A"  # Trustpilot green
        label = "Excellent"
    elif rating >= 3.5:
        bg_color = "#73CF11"
        label = "Great"
    elif rating >= 2.5:
        bg_color = "#FFCE00"
        label = "Average"
    elif rating >= 1.5:
        bg_color = "#FF8622"
        label = "Poor"
    else:
        bg_color = "#FF3722"
        label = "Bad"

    stars = "⭐" * int(rating)
    review_text = f" ({review_count} reviews)" if review_count else ""

    return f'<span style="background: {bg_color}; color: white; padding: 2px 8px; border-radius: 3px; font-size: 0.85em;">{stars} {rating:.1f}/5 {label}{review_text}</span>'


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
    except Exception:
        return "Error parsing hours"


def format_licensing_activities(activities_json: str) -> str:
    """Format licensing activities from JSON."""
    if not activities_json or activities_json == '[]':
        return "Not specified"

    try:
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
    except Exception:
        return "Error parsing activities"


def format_currency(value: float, currency: str = "£") -> str:
    """Format a value as currency."""
    if pd.isna(value):
        return "N/A"
    return f"{currency}{value:,.2f}"


def format_large_number(value: float) -> str:
    """Format a large number with K/M suffix."""
    if pd.isna(value):
        return "N/A"
    if value >= 1_000_000:
        return f"{value/1_000_000:.1f}M"
    elif value >= 1_000:
        return f"{value/1_000:.1f}K"
    else:
        return f"{value:.0f}"


def get_service_badges(restaurant: dict) -> str:
    """Get service option badges for a restaurant."""
    badges = []

    if restaurant.get('google_dine_in'):
        badges.append("🍽️ Dine-in")
    if restaurant.get('google_takeout'):
        badges.append("🥡 Takeout")
    if restaurant.get('google_delivery'):
        badges.append("🚚 Delivery")
    if restaurant.get('google_reservable'):
        badges.append("📅 Reservations")
    if restaurant.get('google_serves_breakfast'):
        badges.append("🍳 Breakfast")
    if restaurant.get('google_serves_lunch'):
        badges.append("🍴 Lunch")
    if restaurant.get('google_serves_dinner'):
        badges.append("🍷 Dinner")
    if restaurant.get('google_serves_vegetarian'):
        badges.append("🥗 Vegetarian")
    if restaurant.get('google_serves_beer'):
        badges.append("🍺 Beer")
    if restaurant.get('google_serves_wine'):
        badges.append("🍷 Wine")

    return " ".join(badges) if badges else ""
