"""
Configuration Module for Plymouth Research
==========================================

Centralized configuration for paths, constants, and settings
used across collection, processing, and dashboard layers.

Compatible with Streamlit Cloud deployment.

Author: Plymouth Research Team
Date: 2025-11-26
"""

import os
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field


def get_project_root() -> Path:
    """
    Get the project root directory.

    Works in multiple contexts:
    - Local development: finds project root from this file's location
    - Streamlit Cloud: uses current working directory
    """
    # First try: relative to this file
    config_based = Path(__file__).parent.parent
    if (config_based / "plymouth_research.db").exists():
        return config_based

    # Second try: current working directory (Streamlit Cloud)
    cwd = Path.cwd()
    if (cwd / "plymouth_research.db").exists():
        return cwd

    # Third try: check if we're in a subdirectory
    for parent in Path(__file__).parents:
        if (parent / "plymouth_research.db").exists():
            return parent

    # Fallback to config-based path
    return config_based


def get_db_path() -> Path:
    """Get the path to the SQLite database."""
    return get_project_root() / "plymouth_research.db"


def get_data_dir() -> Path:
    """Get the data directory path."""
    return get_project_root() / "data"


@dataclass
class ScrapingConfig:
    """Configuration for web scraping operations."""

    # Rate limiting
    min_delay_seconds: float = 5.0
    request_timeout: int = 30

    # User agent
    user_agent: str = "PlymouthResearchMenuScraper/1.0 (+https://plymouthresearch.uk; contact@plymouthresearch.uk)"

    # Retry settings
    max_retries: int = 3
    retry_delay_seconds: float = 10.0

    # Trustpilot specific
    trustpilot_page_delay: float = 2.5
    trustpilot_restaurant_delay: float = 5.0

    # Google Places API
    google_api_key: Optional[str] = field(default_factory=lambda: os.environ.get('GOOGLE_PLACES_API_KEY'))


@dataclass
class DatabaseConfig:
    """Configuration for database operations."""

    db_path: Path = field(default_factory=get_db_path)

    # Connection settings
    check_same_thread: bool = False
    timeout: int = 30

    # Cache settings (for Streamlit)
    cache_ttl_seconds: int = 3600  # 1 hour


@dataclass
class MatchingConfig:
    """Configuration for data matching operations."""

    # Confidence thresholds
    name_similarity_threshold: float = 0.60
    auto_match_threshold: float = 0.70
    high_confidence_threshold: float = 0.95

    # Scoring weights
    name_similarity_weight: float = 50.0
    postcode_match_bonus: float = 30.0
    address_similarity_weight: float = 20.0


@dataclass
class Config:
    """
    Main configuration container for Plymouth Research.

    Usage:
        config = Config()
        db_path = config.database.db_path
        rate_limit = config.scraping.min_delay_seconds
    """

    scraping: ScrapingConfig = field(default_factory=ScrapingConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    matching: MatchingConfig = field(default_factory=MatchingConfig)

    # Paths
    project_root: Path = field(default_factory=get_project_root)
    data_dir: Path = field(default_factory=get_data_dir)

    @property
    def raw_data_dir(self) -> Path:
        """Path to raw data directory."""
        return self.data_dir / "raw"

    @property
    def processed_data_dir(self) -> Path:
        """Path to processed data directory."""
        return self.data_dir / "processed"

    @property
    def manual_matches_dir(self) -> Path:
        """Path to manual matches directory."""
        return self.data_dir / "manual_matches"

    @property
    def logs_dir(self) -> Path:
        """Path to logs directory."""
        return self.project_root / "logs"


# Singleton instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get the global configuration instance."""
    global _config
    if _config is None:
        _config = Config()
    return _config


# ============================================================================
# Constants
# ============================================================================

# FSA Food Hygiene Rating thresholds
FSA_RATING_THRESHOLDS = {
    5: (0, 15),    # Very Good: 0-15 points
    4: (16, 20),   # Good: 16-20 points
    3: (21, 30),   # Satisfactory: 21-30 points
    2: (31, 40),   # Improvement Necessary: 31-40 points
    1: (41, 50),   # Major Improvement: 41-50 points
    0: (51, 999),  # Urgent Improvement: 50+ points
}

# Trustpilot rating labels
TRUSTPILOT_LABELS = {
    (4.5, 5.0): "Excellent",
    (3.5, 4.5): "Great",
    (2.5, 3.5): "Average",
    (1.5, 2.5): "Poor",
    (0.0, 1.5): "Bad",
}

# Supported cuisine types
CUISINE_TYPES = [
    "British", "Italian", "Indian", "Chinese", "Thai", "Mexican",
    "Japanese", "American", "French", "Spanish", "Mediterranean",
    "Greek", "Turkish", "Vietnamese", "Korean", "Fusion", "Other"
]

# Price range symbols
PRICE_RANGES = {
    "£": "Budget",
    "££": "Moderate",
    "£££": "Upscale",
    "££££": "Fine Dining",
}

# Dietary tags
DIETARY_TAGS = [
    "vegan", "vegetarian", "gluten-free", "dairy-free", "nut-free",
    "halal", "kosher", "pescatarian"
]
