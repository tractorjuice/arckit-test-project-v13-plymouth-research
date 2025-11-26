"""
Database Connection Module
===========================

SQLite connection manager with CRUD operations.

Author: Plymouth Research Team
Date: 2025-11-26
"""

import sqlite3
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Any

logger = logging.getLogger(__name__)


class Database:
    """
    SQLite database connection manager.

    Provides connection management and common CRUD operations
    for restaurants, menu items, reviews, and scraping logs.
    """

    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize database connection.

        Args:
            db_path: Path to SQLite database file. If None, uses default.
        """
        if db_path is None:
            from shared.config import get_db_path
            db_path = str(get_db_path())

        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None
        logger.info(f"Database initialized: {db_path}")

    def connect(self) -> sqlite3.Connection:
        """Establish database connection."""
        if not self.conn:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row  # Enable column access by name
            logger.info(f"✅ Connected to database: {self.db_path}")
        return self.conn

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
            logger.info("Database connection closed")

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    # ========================================================================
    # Restaurant Operations
    # ========================================================================

    def get_restaurants(self, active_only: bool = True) -> List[Dict[str, Any]]:
        """
        Get all restaurants.

        Args:
            active_only: If True, only return active restaurants

        Returns:
            List of restaurant dictionaries
        """
        conn = self.connect()
        cursor = conn.cursor()

        query = "SELECT * FROM restaurants"
        if active_only:
            query += " WHERE is_active = 1"
        query += " ORDER BY name"

        cursor.execute(query)
        return [dict(row) for row in cursor.fetchall()]

    def get_restaurant(self, restaurant_id: int) -> Optional[Dict[str, Any]]:
        """Get a single restaurant by ID."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM restaurants WHERE restaurant_id = ?",
            (restaurant_id,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None

    def insert_restaurant(self, restaurant_data: Dict[str, Any]) -> Optional[int]:
        """
        Insert or update restaurant.

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
                (restaurant_data.get('website_url'),)
            )
            existing = cursor.fetchone()

            if existing:
                # Update existing restaurant
                restaurant_id = existing[0]
                cursor.execute("""
                    UPDATE restaurants
                    SET name = ?, address = ?, cuisine_type = ?,
                        price_range = ?, last_updated = ?,
                        data_source = ?, scraping_method = ?
                    WHERE restaurant_id = ?
                """, (
                    restaurant_data['name'],
                    restaurant_data.get('address'),
                    restaurant_data.get('cuisine_type'),
                    restaurant_data.get('price_range'),
                    datetime.now().isoformat(),
                    restaurant_data.get('data_source', 'synthetic'),
                    restaurant_data.get('scraping_method', 'synthetic_generation'),
                    restaurant_id
                ))
                logger.info(f"Updated restaurant: {restaurant_data['name']} (ID: {restaurant_id})")
            else:
                # Insert new restaurant
                cursor.execute("""
                    INSERT INTO restaurants (
                        name, address, website_url, cuisine_type,
                        price_range, scraped_at, last_updated,
                        data_source, scraping_method
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    restaurant_data['name'],
                    restaurant_data.get('address'),
                    restaurant_data.get('website_url'),
                    restaurant_data.get('cuisine_type'),
                    restaurant_data.get('price_range'),
                    datetime.now().isoformat(),
                    datetime.now().isoformat(),
                    restaurant_data.get('data_source', 'synthetic'),
                    restaurant_data.get('scraping_method', 'synthetic_generation')
                ))
                restaurant_id = cursor.lastrowid
                logger.info(f"✅ Inserted restaurant: {restaurant_data['name']} (ID: {restaurant_id})")

            conn.commit()
            return restaurant_id

        except Exception as e:
            logger.error(f"❌ Failed to insert restaurant: {e}")
            return None

    def update_restaurant(self, restaurant_id: int, updates: Dict[str, Any]) -> bool:
        """
        Update a restaurant record.

        Args:
            restaurant_id: ID of restaurant to update
            updates: Dictionary of column -> value updates

        Returns:
            True if update succeeded
        """
        if not updates:
            return False

        # Filter out None values and build query
        filtered_updates = {k: v for k, v in updates.items() if v is not None}
        if not filtered_updates:
            return False

        set_clause = ", ".join(f"{k} = ?" for k in filtered_updates.keys())
        values = list(filtered_updates.values()) + [restaurant_id]

        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(
                f"UPDATE restaurants SET {set_clause} WHERE restaurant_id = ?",
                values
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Failed to update restaurant {restaurant_id}: {e}")
            return False

    # ========================================================================
    # Menu Item Operations
    # ========================================================================

    def get_menu_items(self, restaurant_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get menu items.

        Args:
            restaurant_id: Optional restaurant ID filter

        Returns:
            List of menu item dictionaries
        """
        conn = self.connect()
        cursor = conn.cursor()

        query = """
            SELECT mi.*, r.name as restaurant_name
            FROM menu_items mi
            JOIN restaurants r ON mi.restaurant_id = r.restaurant_id
        """
        params = []

        if restaurant_id:
            query += " WHERE mi.restaurant_id = ?"
            params.append(restaurant_id)

        query += " ORDER BY r.name, mi.category, mi.name"

        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

    def insert_menu_items(self, restaurant_id: int, menu_items: List[Dict[str, Any]]) -> int:
        """
        Insert menu items for a restaurant.

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
                    item.get('source_html', '')[:1000]
                ))

                item_id = cursor.lastrowid

                # Insert dietary tags if present
                if 'dietary_tags' in item and item['dietary_tags']:
                    for tag_name in item['dietary_tags']:
                        cursor.execute(
                            "SELECT tag_id FROM dietary_tags WHERE tag_name = ?",
                            (tag_name,)
                        )
                        tag_row = cursor.fetchone()
                        if tag_row:
                            cursor.execute("""
                                INSERT INTO menu_item_dietary_tags (item_id, tag_id)
                                VALUES (?, ?)
                            """, (item_id, tag_row[0]))

                inserted_count += 1

            conn.commit()
            logger.info(f"✅ Inserted {inserted_count} menu items for restaurant {restaurant_id}")
            return inserted_count

        except Exception as e:
            logger.error(f"❌ Failed to insert menu items: {e}")
            return 0

    # ========================================================================
    # Scraping Log Operations
    # ========================================================================

    def log_scraping_attempt(self, log_data: Dict[str, Any]):
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
                    restaurant_id, url, http_status_code,
                    robots_txt_allowed, rate_limit_delay_seconds,
                    user_agent, success, error_message, scraped_at
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
            logger.debug(f"📝 Scraping log recorded: {log_data['url']}")

        except Exception as e:
            logger.error(f"❌ Failed to log scraping attempt: {e}")

    # ========================================================================
    # Review Operations
    # ========================================================================

    def get_reviews(
        self,
        source: str = "trustpilot",
        restaurant_id: Optional[int] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get reviews.

        Args:
            source: "trustpilot" or "google"
            restaurant_id: Optional restaurant ID filter
            limit: Maximum reviews to return

        Returns:
            List of review dictionaries
        """
        conn = self.connect()
        cursor = conn.cursor()

        table = "trustpilot_reviews" if source == "trustpilot" else "google_reviews"

        query = f"""
            SELECT r.*, rest.name as restaurant_name
            FROM {table} r
            JOIN restaurants rest ON r.restaurant_id = rest.restaurant_id
        """
        params = []

        if restaurant_id:
            query += " WHERE r.restaurant_id = ?"
            params.append(restaurant_id)

        query += f" ORDER BY r.review_date DESC LIMIT {limit}"

        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

    # ========================================================================
    # Statistics
    # ========================================================================

    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics."""
        conn = self.connect()
        cursor = conn.cursor()

        stats = {}

        # Restaurant counts
        cursor.execute("SELECT COUNT(*) FROM restaurants WHERE is_active = 1")
        stats['total_restaurants'] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM restaurants WHERE is_active = 1 AND data_source = 'real_scraped'")
        stats['real_restaurants'] = cursor.fetchone()[0]

        # Menu items
        cursor.execute("SELECT COUNT(*) FROM menu_items")
        stats['total_menu_items'] = cursor.fetchone()[0]

        # Reviews
        cursor.execute("SELECT COUNT(*) FROM trustpilot_reviews")
        stats['trustpilot_reviews'] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM google_reviews")
        stats['google_reviews'] = cursor.fetchone()[0]

        # Hygiene ratings
        cursor.execute("SELECT COUNT(*) FROM restaurants WHERE hygiene_rating IS NOT NULL")
        stats['restaurants_with_hygiene'] = cursor.fetchone()[0]

        return stats
