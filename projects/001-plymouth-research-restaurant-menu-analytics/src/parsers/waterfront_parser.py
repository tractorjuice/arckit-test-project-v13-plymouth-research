"""
The Waterfront Restaurant Parser
=================================

Restaurant-specific HTML parser for The Waterfront Restaurant menu format.

This demonstrates Sprint 2 functionality: custom parsers per restaurant.

Author: Plymouth Research Team
Date: 2025-11-17
"""

import re
import logging
from typing import List, Dict
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class WaterfrontParser:
    """Parser for The Waterfront Restaurant menu format."""

    # Dietary tag mappings
    DIETARY_TAG_MAP = {
        '(V)': 'vegetarian',
        '(VG)': 'vegan',
        '(GF)': 'gluten-free',
        '(DF)': 'dairy-free',
    }

    def parse_menu(self, html: str) -> List[Dict]:
        """
        Parse menu HTML into structured menu items.

        Args:
            html: Raw HTML content

        Returns:
            List of menu item dictionaries
        """
        soup = BeautifulSoup(html, 'lxml')
        menu_items = []

        # Find all menu sections (Starters, Mains, Desserts)
        sections = soup.find_all('div', class_='menu-section')

        for section in sections:
            # Get category from section header
            category_h2 = section.find('h2')
            category = category_h2.get_text(strip=True) if category_h2 else 'Other'

            # Find all menu items in this section
            items = section.find_all('div', class_='menu-item')

            for item in items:
                menu_item = self._parse_menu_item(item, category)
                if menu_item:
                    menu_items.append(menu_item)

        logger.info(f"✅ Parsed {len(menu_items)} menu items across {len(sections)} categories")
        return menu_items

    def _parse_menu_item(self, item_element, category: str) -> Dict:
        """
        Parse a single menu item element.

        Args:
            item_element: BeautifulSoup element for menu item
            category: Menu category (Starters, Mains, etc.)

        Returns:
            Dictionary with menu item data
        """
        try:
            # Extract name
            name_elem = item_element.find('span', class_='item-name')
            name = name_elem.get_text(strip=True) if name_elem else None

            if not name:
                return None

            # Extract description
            desc_elem = item_element.find('span', class_='item-description')
            description = desc_elem.get_text(strip=True) if desc_elem else None

            # Extract price
            price_elem = item_element.find('span', class_='item-price')
            price_text = price_elem.get_text(strip=True) if price_elem else None
            price_gbp = self._normalize_price(price_text)

            # Extract dietary tags
            dietary_tags = []

            # From explicit dietary-tag spans
            tag_elems = item_element.find_all('span', class_='dietary-tag')
            for tag_elem in tag_elems:
                tag = tag_elem.get_text(strip=True).lower()
                if tag in ['vegan', 'vegetarian', 'gluten-free', 'dairy-free', 'nut-free']:
                    dietary_tags.append(tag)

            # From dietary codes in name (V), (VG), (GF)
            for code, tag in self.DIETARY_TAG_MAP.items():
                if code in name:
                    if tag not in dietary_tags:
                        dietary_tags.append(tag)
                    # Clean name by removing code
                    name = name.replace(code, '').strip()

            return {
                'name': name[:255],  # DB column limit
                'description': description,
                'price_gbp': price_gbp,
                'category': category,
                'dietary_tags': dietary_tags,
                'source_html': str(item_element)
            }

        except Exception as e:
            logger.error(f"❌ Failed to parse menu item: {e}")
            return None

    def _normalize_price(self, price_text: str) -> float:
        """
        Normalize price text to decimal GBP.

        Examples:
            "£12.50" -> 12.50
            "£12.5" -> 12.50
            "12.50" -> 12.50
            "£12" -> 12.00

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
    with open('../test_data/mock_restaurant.html', 'r') as f:
        html = f.read()

    # Parse menu
    parser = WaterfrontParser()
    items = parser.parse_menu(html)

    # Display results
    print(f"\n✅ Parsed {len(items)} menu items:\n")
    for i, item in enumerate(items, 1):
        print(f"{i}. {item['name']}")
        print(f"   Category: {item['category']}")
        print(f"   Price: £{item['price_gbp']:.2f}" if item['price_gbp'] else "   Price: N/A")
        if item['dietary_tags']:
            print(f"   Tags: {', '.join(item['dietary_tags'])}")
        print()
