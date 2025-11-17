"""
The Plymouth Grill Parser
=========================

Restaurant-specific HTML parser for The Plymouth Grill menu format.

This demonstrates Sprint 2 functionality: list-based menu parsing.

HTML Pattern:
- <ul class="menu-items">
- <li class="menu-item">
- <span class="item-name">, <span class="item-price">, <span class="item-description">
- <span class="tag tag-vegetarian">, <span class="tag tag-vegan">, etc.

Author: Plymouth Research Team
Date: 2025-11-17
"""

import re
import logging
from typing import List, Dict
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class PlymouthGrillParser:
    """Parser for The Plymouth Grill list-based menu format."""

    # Dietary tag mapping from CSS classes
    DIETARY_CLASS_MAP = {
        'tag-vegan': 'vegan',
        'tag-vegetarian': 'vegetarian',
        'tag-gluten-free': 'gluten-free',
        'tag-dairy-free': 'dairy-free',
        'tag-nut-free': 'nut-free',
    }

    def parse_menu(self, html: str) -> List[Dict]:
        """
        Parse list-based menu HTML into structured menu items.

        Args:
            html: Raw HTML content

        Returns:
            List of menu item dictionaries
        """
        soup = BeautifulSoup(html, 'lxml')
        menu_items = []

        # Find all menu categories (div.menu-category)
        categories = soup.find_all('div', class_='menu-category')

        for category_div in categories:
            # Get category from <h2>
            category_h2 = category_div.find('h2')
            category = category_h2.get_text(strip=True) if category_h2 else 'Other'

            # Find menu items list
            menu_list = category_div.find('ul', class_='menu-items')

            if menu_list:
                items = menu_list.find_all('li', class_='menu-item')

                for item in items:
                    menu_item = self._parse_list_item(item, category)
                    if menu_item:
                        menu_items.append(menu_item)

        logger.info(f"✅ Parsed {len(menu_items)} menu items across {len(categories)} categories")
        return menu_items

    def _parse_list_item(self, item_element, category: str) -> Dict:
        """
        Parse a single list item into a menu item.

        Args:
            item_element: BeautifulSoup <li> element
            category: Menu category (Starters, Steaks & Grills, etc.)

        Returns:
            Dictionary with menu item data
        """
        try:
            # Extract name
            name_elem = item_element.find('span', class_='item-name')
            name = name_elem.get_text(strip=True) if name_elem else None

            if not name:
                return None

            # Extract price
            price_elem = item_element.find('span', class_='item-price')
            price_text = price_elem.get_text(strip=True) if price_elem else None
            price_gbp = self._normalize_price(price_text)

            # Extract description
            desc_elem = item_element.find('div', class_='item-description')
            description = desc_elem.get_text(strip=True) if desc_elem else None

            # Extract dietary tags from <span class="tag tag-*">
            dietary_tags = []

            tag_container = item_element.find('div', class_='dietary-tags')
            if tag_container:
                tag_spans = tag_container.find_all('span', class_='tag')

                for tag_span in tag_spans:
                    # Check CSS classes for dietary type
                    tag_classes = tag_span.get('class', [])

                    for css_class in tag_classes:
                        if css_class in self.DIETARY_CLASS_MAP:
                            tag_name = self.DIETARY_CLASS_MAP[css_class]
                            if tag_name not in dietary_tags:
                                dietary_tags.append(tag_name)

                    # Also check text content (fallback)
                    tag_text = tag_span.get_text(strip=True).lower()
                    if 'vegan' in tag_text and 'vegan' not in dietary_tags:
                        dietary_tags.append('vegan')
                    elif 'vegetarian' in tag_text and 'vegetarian' not in dietary_tags and 'vegan' not in dietary_tags:
                        dietary_tags.append('vegetarian')
                    if 'gluten-free' in tag_text or 'gluten free' in tag_text:
                        if 'gluten-free' not in dietary_tags:
                            dietary_tags.append('gluten-free')
                    if 'dairy-free' in tag_text or 'dairy free' in tag_text:
                        if 'dairy-free' not in dietary_tags:
                            dietary_tags.append('dairy-free')
                    if 'nut-free' in tag_text or 'nut free' in tag_text:
                        if 'nut-free' not in dietary_tags:
                            dietary_tags.append('nut-free')

            return {
                'name': name[:255],  # DB column limit
                'description': description,
                'price_gbp': price_gbp,
                'category': category,
                'dietary_tags': dietary_tags,
                'source_html': str(item_element)
            }

        except Exception as e:
            logger.error(f"❌ Failed to parse list item: {e}")
            return None

    def _normalize_price(self, price_text: str) -> float:
        """
        Normalize price text to decimal GBP.

        Examples:
            "£12.50" -> 12.50
            "£32.95" -> 32.95
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
    with open('../test_data/mock_plymouth_grill.html', 'r') as f:
        html = f.read()

    # Parse menu
    parser = PlymouthGrillParser()
    items = parser.parse_menu(html)

    # Display results
    print(f"\n✅ Parsed {len(items)} menu items:\n")

    # Group by category
    from collections import defaultdict
    by_category = defaultdict(list)
    for item in items:
        by_category[item['category']].append(item)

    for category, category_items in by_category.items():
        print(f"\n{category} ({len(category_items)} items):")
        for i, item in enumerate(category_items, 1):
            print(f"  {i}. {item['name']}")
            print(f"     Price: £{item['price_gbp']:.2f}" if item['price_gbp'] else "     Price: N/A")
            if item['dietary_tags']:
                print(f"     Tags: {', '.join(item['dietary_tags'])}")
