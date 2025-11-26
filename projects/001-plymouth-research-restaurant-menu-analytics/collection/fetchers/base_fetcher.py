"""
Base Fetcher Class
==================

Abstract base class for all data fetchers with common functionality.

Author: Plymouth Research Team
Date: 2025-11-26
"""

import logging
import sqlite3
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Dict, List, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class BaseFetcher(ABC):
    """
    Abstract base class for data fetchers.

    Provides common functionality:
    - Database connection management
    - Logging setup
    - Rate limiting hooks
    - Error handling patterns
    """

    def __init__(self, db_path: Optional[Path] = None):
        """
        Initialize base fetcher.

        Args:
            db_path: Path to SQLite database. If None, uses default.
        """
        if db_path is None:
            from shared.config import get_db_path
            db_path = get_db_path()

        self.db_path = db_path
        self._conn: Optional[sqlite3.Connection] = None
        self.stats = {
            "fetched": 0,
            "matched": 0,
            "errors": 0,
            "start_time": None,
            "end_time": None,
        }
        logger.info(f"{self.__class__.__name__} initialized with db: {db_path}")

    @property
    def conn(self) -> sqlite3.Connection:
        """Get database connection (lazy initialization)."""
        if self._conn is None:
            self._conn = sqlite3.connect(str(self.db_path))
            self._conn.row_factory = sqlite3.Row
        return self._conn

    def close(self):
        """Close database connection."""
        if self._conn:
            self._conn.close()
            self._conn = None
            logger.info(f"{self.__class__.__name__} database connection closed")

    @abstractmethod
    def fetch(self, **kwargs) -> List[Dict[str, Any]]:
        """
        Fetch data from external source.

        Args:
            **kwargs: Fetcher-specific arguments

        Returns:
            List of fetched records as dictionaries
        """
        pass

    @abstractmethod
    def process(self, data: List[Dict[str, Any]]) -> int:
        """
        Process fetched data (match, transform, store).

        Args:
            data: List of fetched records

        Returns:
            Number of records successfully processed
        """
        pass

    def run(self, **kwargs) -> Dict[str, Any]:
        """
        Execute full fetch-and-process pipeline.

        Args:
            **kwargs: Arguments passed to fetch()

        Returns:
            Statistics dictionary with results
        """
        self.stats["start_time"] = datetime.now()

        try:
            # Fetch data
            logger.info(f"Starting {self.__class__.__name__} fetch...")
            data = self.fetch(**kwargs)
            self.stats["fetched"] = len(data)
            logger.info(f"Fetched {len(data)} records")

            # Process data
            logger.info(f"Processing {len(data)} records...")
            processed = self.process(data)
            self.stats["matched"] = processed
            logger.info(f"Successfully processed {processed} records")

        except Exception as e:
            logger.error(f"Error in {self.__class__.__name__}: {e}")
            self.stats["errors"] += 1
            raise

        finally:
            self.stats["end_time"] = datetime.now()
            self.close()

        return self.stats

    def get_restaurants(self, active_only: bool = True) -> List[Dict[str, Any]]:
        """
        Get restaurants from database.

        Args:
            active_only: If True, only return active restaurants

        Returns:
            List of restaurant dictionaries
        """
        query = "SELECT * FROM restaurants"
        if active_only:
            query += " WHERE is_active = 1"
        query += " ORDER BY name"

        cursor = self.conn.cursor()
        cursor.execute(query)
        return [dict(row) for row in cursor.fetchall()]

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

        set_clause = ", ".join(f"{k} = ?" for k in updates.keys())
        values = list(updates.values()) + [restaurant_id]

        try:
            cursor = self.conn.cursor()
            cursor.execute(
                f"UPDATE restaurants SET {set_clause} WHERE restaurant_id = ?",
                values
            )
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Failed to update restaurant {restaurant_id}: {e}")
            return False
