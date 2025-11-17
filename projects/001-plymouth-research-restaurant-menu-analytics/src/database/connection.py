"""
Database Connection Module
===========================

SQLite connection for development/demo.
Production will use PostgreSQL.

Author: Plymouth Research Team
Date: 2025-11-17
"""

import sqlite3
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)


class Database:
    """SQLite database connection manager."""

    def __init__(self, db_path: str = "plymouth_research.db"):
        """
        Initialize database connection.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.conn = None
        logger.info(f"Database initialized: {db_path}")

    def connect(self):
        """Establish database connection."""
        if not self.conn:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row  # Enable column access by name
            logger.info(f"✅ Connected to database: {self.db_path}")
        return self.conn

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
            logger.info("Database connection closed")

    def log_scraping_attempt(self, log_data: Dict):
        """
        Log scraping attempt to E-006: Scraping Logs table.

        Args:
            log_data: Dictionary with scraping log fields
        """
        try:
            conn = self.connect()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO scraping_logs (
                    restaurant_id,
                    url,
                    http_status_code,
                    robots_txt_allowed,
                    rate_limit_delay_seconds,
                    user_agent,
                    success,
                    error_message,
                    scraped_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                log_data.get('restaurant_id'),
                log_data['url'],
                log_data.get('http_status_code'),
                1 if log_data.get('robots_txt_allowed') else 0,
                log_data.get('rate_limit_delay_seconds', 0),
                log_data['user_agent'],
                1 if log_data.get('success') else 0,
                log_data.get('error_message'),
                log_data.get('scraped_at', datetime.now().isoformat())
            ))

            conn.commit()
            logger.info(f"📝 Scraping log recorded: {log_data['url']}")

        except Exception as e:
            logger.error(f"❌ Failed to log scraping attempt: {e}")

    def insert_restaurant(self, restaurant_data: Dict) -> Optional[int]:
        """
        Insert or update restaurant in E-001: Restaurants table.

        Args:
            restaurant_data: Dictionary with restaurant fields

        Returns:
            restaurant_id if successful, None otherwise
        """
        try:
            conn = self.connect()
            cursor = conn.cursor()

            # Check if restaurant already exists
            cursor.execute(
                "SELECT restaurant_id FROM restaurants WHERE website_url = ?",
                (restaurant_data['website_url'],)
            )
            existing = cursor.fetchone()

            if existing:
                # Update existing restaurant
                restaurant_id = existing[0]
                cursor.execute("""
                    UPDATE restaurants
                    SET name = ?, address = ?, cuisine_type = ?,
                        price_range = ?, last_updated = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE restaurant_id = ?
                """, (
                    restaurant_data['name'],
                    restaurant_data.get('address'),
                    restaurant_data.get('cuisine_type'),
                    restaurant_data.get('price_range'),
                    datetime.now().isoformat(),
                    restaurant_id
                ))
                logger.info(f"Updated restaurant: {restaurant_data['name']} (ID: {restaurant_id})")
            else:
                # Insert new restaurant
                cursor.execute("""
                    INSERT INTO restaurants (
                        name, address, website_url, cuisine_type,
                        price_range, scraped_at, last_updated
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    restaurant_data['name'],
                    restaurant_data.get('address'),
                    restaurant_data['website_url'],
                    restaurant_data.get('cuisine_type'),
                    restaurant_data.get('price_range'),
                    datetime.now().isoformat(),
                    datetime.now().isoformat()
                ))
                restaurant_id = cursor.lastrowid
                logger.info(f"✅ Inserted restaurant: {restaurant_data['name']} (ID: {restaurant_id})")

            conn.commit()
            return restaurant_id

        except Exception as e:
            logger.error(f"❌ Failed to insert restaurant: {e}")
            return None

    def insert_menu_items(self, restaurant_id: int, menu_items: List[Dict]) -> int:
        """
        Insert menu items for a restaurant in E-002: Menu Items table.

        Args:
            restaurant_id: Restaurant ID
            menu_items: List of menu item dictionaries

        Returns:
            Number of items inserted
        """
        try:
            conn = self.connect()
            cursor = conn.cursor()
            inserted_count = 0

            for item in menu_items:
                cursor.execute("""
                    INSERT INTO menu_items (
                        restaurant_id, name, description, price_gbp,
                        category, scraped_at, last_updated, source_html
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    restaurant_id,
                    item['name'],
                    item.get('description'),
                    item.get('price_gbp'),
                    item.get('category'),
                    datetime.now().isoformat(),
                    datetime.now().isoformat(),
                    item.get('source_html', '')[:1000]  # Limit to 1000 chars
                ))

                item_id = cursor.lastrowid

                # Insert dietary tags if present
                if 'dietary_tags' in item and item['dietary_tags']:
                    for tag_name in item['dietary_tags']:
                        # Get tag_id
                        cursor.execute(
                            "SELECT tag_id FROM dietary_tags WHERE tag_name = ?",
                            (tag_name,)
                        )
                        tag_row = cursor.fetchone()
                        if tag_row:
                            tag_id = tag_row[0]
                            cursor.execute("""
                                INSERT INTO menu_item_dietary_tags (item_id, tag_id)
                                VALUES (?, ?)
                            """, (item_id, tag_id))

                inserted_count += 1

            conn.commit()
            logger.info(f"✅ Inserted {inserted_count} menu items for restaurant {restaurant_id}")
            return inserted_count

        except Exception as e:
            logger.error(f"❌ Failed to insert menu items: {e}")
            return 0

    def get_all_data(self) -> Dict:
        """Get all data from database for verification."""
        try:
            conn = self.connect()
            cursor = conn.cursor()

            # Get restaurants
            cursor.execute("SELECT * FROM restaurants")
            restaurants = [dict(row) for row in cursor.fetchall()]

            # Get menu items
            cursor.execute("""
                SELECT mi.*, r.name as restaurant_name
                FROM menu_items mi
                JOIN restaurants r ON mi.restaurant_id = r.restaurant_id
            """)
            menu_items = [dict(row) for row in cursor.fetchall()]

            # Get scraping logs
            cursor.execute("SELECT * FROM scraping_logs ORDER BY scraped_at DESC LIMIT 10")
            logs = [dict(row) for row in cursor.fetchall()]

            return {
                "restaurants": restaurants,
                "menu_items": menu_items,
                "scraping_logs": logs
            }

        except Exception as e:
            logger.error(f"❌ Failed to get data: {e}")
            return {}

    def get_menu_items_for_restaurant(self, restaurant_id: int) -> list:
        """Get all menu items for a specific restaurant."""
        try:
            conn = self.connect()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT * FROM menu_items
                WHERE restaurant_id = ?
            """, (restaurant_id,))

            menu_items = [dict(row) for row in cursor.fetchall()]
            return menu_items

        except Exception as e:
            logger.error(f"❌ Failed to get menu items for restaurant {restaurant_id}: {e}")
            return []
