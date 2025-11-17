"""
The Boathouse Cafe Parser
=========================

Restaurant-specific HTML parser for The Boathouse Cafe menu format.

This demonstrates Sprint 2 functionality: table-based menu parsing.

HTML Pattern:
- <table class="menu-table">
- <td class="dish-name">, <td class="dish-description">, <td class="dish-price">
- Dietary tags in <span class="dietary-badge">

Author: Plymouth Research Team
Date: 2025-11-17
"""

import re
import logging
from typing import List, Dict
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class BoathouseParser:
    """Parser for The Boathouse Cafe table-based menu format."""

    # Dietary tag mapping from badge classes
    DIETARY_CLASS_MAP = {
        'vegan': 'vegan',
        'vegetarian': 'vegetarian',
        'gluten-free': 'gluten-free',
    }

    def parse_menu(self, html: str) -> List[Dict]:
        """
        Parse table-based menu HTML into structured menu items.

        Args:
            html: Raw HTML content

        Returns:
            List of menu item dictionaries
        """
        soup = BeautifulSoup(html, 'lxml')
        menu_items = []

        # Find all menu tables
        tables = soup.find_all('table', class_='menu-table')

        for table in tables:
            # Get category from preceding <h3>
            category_h3 = table.find_previous('h3')
            category = category_h3.get_text(strip=True) if category_h3 else 'Other'

            # Find all table rows (skip header row)
            rows = table.find('tbody').find_all('tr') if table.find('tbody') else table.find_all('tr')[1:]

            for row in rows:
                menu_item = self._parse_table_row(row, category)
                if menu_item:
                    menu_items.append(menu_item)

        logger.info(f"✅ Parsed {len(menu_items)} menu items from {len(tables)} tables")
        return menu_items

    def _parse_table_row(self, row_element, category: str) -> Dict:
        """
        Parse a single table row into a menu item.

        Args:
            row_element: BeautifulSoup <tr> element
            category: Menu category (Breakfast, Lunch, etc.)

        Returns:
            Dictionary with menu item data
        """
        try:
            cells = row_element.find_all('td')

            if len(cells) < 3:
                return None

            # Extract name (first column)
            name_cell = cells[0]
            name_text = name_cell.get_text(strip=True)

            # Remove dietary badges from name
            for badge in name_cell.find_all('span', class_='dietary-badge'):
                badge_text = badge.get_text(strip=True)
                name_text = name_text.replace(badge_text, '').strip()

            # Extract description (second column)
            desc_cell = cells[1]
            description = desc_cell.get_text(strip=True) if desc_cell else None

            # Extract price (third column)
            price_cell = cells[2]
            price_text = price_cell.get_text(strip=True) if price_cell else None
            price_gbp = self._normalize_price(price_text)

            # Extract dietary tags from badges
            dietary_tags = []

            # From dietary-badge spans
            badges = name_cell.find_all('span', class_='dietary-badge')
            for badge in badges:
                badge_text = badge.get_text(strip=True).lower()

                # Map badge text to standard tags
                if 'vg' in badge_text or 'vegan' in badge_text:
                    dietary_tags.append('vegan')
                elif 'v' in badge_text or 'vegetarian' in badge_text:
                    if 'vegan' not in dietary_tags:  # Don't add if already vegan
                        dietary_tags.append('vegetarian')
                if 'gf' in badge_text or 'gluten-free' in badge_text or 'gluten free' in badge_text:
                    dietary_tags.append('gluten-free')
                if 'df' in badge_text or 'dairy-free' in badge_text or 'dairy free' in badge_text:
                    dietary_tags.append('dairy-free')

            # Also check for dietary badge classes (CSS)
            for badge_class in ['vegan', 'vegetarian', 'gluten-free']:
                badge = name_cell.find('span', class_=badge_class)
                if badge and self.DIETARY_CLASS_MAP[badge_class] not in dietary_tags:
                    dietary_tags.append(self.DIETARY_CLASS_MAP[badge_class])

            return {
                'name': name_text[:255],  # DB column limit
                'description': description,
                'price_gbp': price_gbp,
                'category': category,
                'dietary_tags': dietary_tags,
                'source_html': str(row_element)
            }

        except Exception as e:
            logger.error(f"❌ Failed to parse table row: {e}")
            return None

    def _normalize_price(self, price_text: str) -> float:
        """
        Normalize price text to decimal GBP.

        Examples:
            "£12.50" -> 12.50
            "£9.95" -> 9.95
            "£5.50" -> 5.50

        Args:
            price_text: Raw price string

        Returns:
            Normalized price as float, or None if invalid
        """
        if not price_text:
            return None

        try:
            # Remove currency symbols and whitespace
            price_clean = price_text.replace('£', '').replace('$', '').strip()

            # Extract numeric value
            match = re.search(r'(\d+\.?\d*)', price_clean)
            if match:
                price_value = float(match.group(1))

                # Validate range (£0.50 - £150.00 per data model)
                if 0.50 <= price_value <= 150.00:
                    return round(price_value, 2)  # 2 decimal places
                else:
                    logger.warning(f"⚠️  Price out of range: £{price_value}")
                    return price_value  # Return anyway, flag for review

            return None

        except Exception as e:
            logger.error(f"❌ Failed to normalize price '{price_text}': {e}")
            return None


# ============================================================================
# Usage Example
# ============================================================================

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Read mock restaurant HTML
    with open('../test_data/mock_boathouse_cafe.html', 'r') as f:
        html = f.read()

    # Parse menu
    parser = BoathouseParser()
    items = parser.parse_menu(html)

    # Display results
    print(f"\n✅ Parsed {len(items)} menu items:\n")
    for i, item in enumerate(items, 1):
        print(f"{i}. {item['name']}")
        print(f"   Category: {item['category']}")
        print(f"   Price: £{item['price_gbp']:.2f}" if item['price_gbp'] else "   Price: N/A")
        if item['dietary_tags']:
            print(f"   Tags: {', '.join(item['dietary_tags'])}")
        if item['description']:
            print(f"   Description: {item['description'][:60]}...")
        print()
