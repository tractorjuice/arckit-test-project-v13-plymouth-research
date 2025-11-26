"""
Data Models for Plymouth Research
=================================

Dataclass models representing core entities used across
collection, processing, and dashboard layers.

Author: Plymouth Research Team
Date: 2025-11-26
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any


@dataclass
class Restaurant:
    """Restaurant entity model."""

    restaurant_id: Optional[int] = None
    name: str = ""
    cuisine_type: Optional[str] = None
    price_range: Optional[str] = None
    address: Optional[str] = None
    website_url: Optional[str] = None

    # Data provenance
    data_source: str = "synthetic"
    scraping_method: Optional[str] = None
    scraped_at: Optional[datetime] = None
    last_updated: Optional[datetime] = None
    is_active: bool = True

    # Hygiene rating
    hygiene_rating: Optional[int] = None
    hygiene_rating_date: Optional[str] = None
    fsa_id: Optional[int] = None
    hygiene_score_hygiene: Optional[int] = None
    hygiene_score_structural: Optional[int] = None
    hygiene_score_confidence: Optional[int] = None

    # Reviews
    trustpilot_url: Optional[str] = None
    trustpilot_review_count: Optional[int] = None
    trustpilot_avg_rating: Optional[float] = None
    google_review_count: Optional[int] = None
    google_avg_rating: Optional[float] = None

    # Location (from Google/FSA)
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for database operations."""
        return {
            'restaurant_id': self.restaurant_id,
            'name': self.name,
            'cuisine_type': self.cuisine_type,
            'price_range': self.price_range,
            'address': self.address,
            'website_url': self.website_url,
            'data_source': self.data_source,
            'scraping_method': self.scraping_method,
            'scraped_at': self.scraped_at.isoformat() if self.scraped_at else None,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'is_active': 1 if self.is_active else 0,
            'hygiene_rating': self.hygiene_rating,
            'hygiene_rating_date': self.hygiene_rating_date,
            'fsa_id': self.fsa_id,
            'trustpilot_url': self.trustpilot_url,
            'trustpilot_review_count': self.trustpilot_review_count,
            'trustpilot_avg_rating': self.trustpilot_avg_rating,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Restaurant':
        """Create from dictionary (e.g., database row)."""
        return cls(
            restaurant_id=data.get('restaurant_id'),
            name=data.get('name', ''),
            cuisine_type=data.get('cuisine_type'),
            price_range=data.get('price_range'),
            address=data.get('address'),
            website_url=data.get('website_url'),
            data_source=data.get('data_source', 'synthetic'),
            scraping_method=data.get('scraping_method'),
            is_active=bool(data.get('is_active', 1)),
            hygiene_rating=data.get('hygiene_rating'),
            hygiene_rating_date=data.get('hygiene_rating_date'),
            fsa_id=data.get('fsa_id'),
            trustpilot_url=data.get('trustpilot_url'),
            trustpilot_review_count=data.get('trustpilot_review_count'),
            trustpilot_avg_rating=data.get('trustpilot_avg_rating'),
            google_review_count=data.get('google_review_count'),
            google_avg_rating=data.get('google_avg_rating'),
            latitude=data.get('fsa_latitude') or data.get('google_latitude'),
            longitude=data.get('fsa_longitude') or data.get('google_longitude'),
        )


@dataclass
class MenuItem:
    """Menu item entity model."""

    item_id: Optional[int] = None
    restaurant_id: int = 0
    name: str = ""
    description: Optional[str] = None
    price_gbp: Optional[float] = None
    category: Optional[str] = None

    # Dietary information
    is_vegetarian: bool = False
    is_vegan: bool = False
    is_gluten_free: bool = False
    dietary_tags: List[str] = field(default_factory=list)
    allergen_info: Optional[str] = None

    # Data provenance
    source_url: Optional[str] = None
    source_html: Optional[str] = None
    scraped_at: Optional[datetime] = None
    last_updated: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for database operations."""
        return {
            'item_id': self.item_id,
            'restaurant_id': self.restaurant_id,
            'name': self.name,
            'description': self.description,
            'price_gbp': self.price_gbp,
            'category': self.category,
            'is_vegetarian': 1 if self.is_vegetarian else 0,
            'is_vegan': 1 if self.is_vegan else 0,
            'is_gluten_free': 1 if self.is_gluten_free else 0,
            'allergen_info': self.allergen_info,
            'scraped_at': self.scraped_at.isoformat() if self.scraped_at else None,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MenuItem':
        """Create from dictionary."""
        return cls(
            item_id=data.get('item_id'),
            restaurant_id=data.get('restaurant_id', 0),
            name=data.get('name', data.get('item_name', '')),
            description=data.get('description'),
            price_gbp=data.get('price_gbp'),
            category=data.get('category'),
            is_vegetarian=bool(data.get('is_vegetarian', 0)),
            is_vegan=bool(data.get('is_vegan', 0)),
            is_gluten_free=bool(data.get('is_gluten_free', 0)),
            allergen_info=data.get('allergen_info'),
        )


@dataclass
class Review:
    """Review entity model (Trustpilot/Google)."""

    review_id: Optional[int] = None
    restaurant_id: int = 0
    source: str = "trustpilot"  # "trustpilot" or "google"

    # Review content
    review_date: Optional[datetime] = None
    author_name: Optional[str] = None
    review_title: Optional[str] = None
    review_body: Optional[str] = None
    rating: Optional[float] = None

    # Author info
    author_location: Optional[str] = None
    author_review_count: Optional[int] = None

    # Metadata
    is_verified: bool = False
    helpful_count: int = 0
    reply_count: int = 0
    scraped_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for database operations."""
        return {
            'review_id': self.review_id,
            'restaurant_id': self.restaurant_id,
            'review_date': self.review_date.isoformat() if self.review_date else None,
            'author_name': self.author_name,
            'review_title': self.review_title,
            'review_body': self.review_body,
            'rating': self.rating,
            'author_location': self.author_location,
            'author_review_count': self.author_review_count,
            'is_verified_purchase': 1 if self.is_verified else 0,
            'helpful_count': self.helpful_count,
            'reply_count': self.reply_count,
            'scraped_at': self.scraped_at.isoformat() if self.scraped_at else None,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any], source: str = "trustpilot") -> 'Review':
        """Create from dictionary."""
        review_date = data.get('review_date')
        if review_date and isinstance(review_date, str):
            try:
                review_date = datetime.fromisoformat(review_date.replace('Z', '+00:00'))
            except ValueError:
                review_date = None

        return cls(
            review_id=data.get('review_id'),
            restaurant_id=data.get('restaurant_id', 0),
            source=source,
            review_date=review_date,
            author_name=data.get('author_name'),
            review_title=data.get('review_title'),
            review_body=data.get('review_body', data.get('review_text')),
            rating=data.get('rating'),
            author_location=data.get('author_location'),
            author_review_count=data.get('author_review_count'),
            is_verified=bool(data.get('is_verified_purchase', 0)),
            helpful_count=data.get('helpful_count', 0),
            reply_count=data.get('reply_count', 0),
        )


@dataclass
class ScrapingLog:
    """Scraping audit log entry."""

    log_id: Optional[int] = None
    restaurant_id: Optional[int] = None
    url: str = ""

    # Request details
    http_status_code: Optional[int] = None
    robots_txt_allowed: bool = True
    rate_limit_delay_seconds: float = 0.0
    user_agent: str = ""

    # Result
    success: bool = False
    error_message: Optional[str] = None
    scraped_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for database operations."""
        return {
            'log_id': self.log_id,
            'restaurant_id': self.restaurant_id,
            'url': self.url,
            'http_status_code': self.http_status_code,
            'robots_txt_allowed': 1 if self.robots_txt_allowed else 0,
            'rate_limit_delay_seconds': int(self.rate_limit_delay_seconds),
            'user_agent': self.user_agent,
            'success': 1 if self.success else 0,
            'error_message': self.error_message,
            'scraped_at': self.scraped_at.isoformat() if self.scraped_at else datetime.now().isoformat(),
        }


@dataclass
class MatchResult:
    """Result of a data matching operation."""

    source_id: Any  # ID from source data (e.g., FSA ID)
    target_id: Optional[int] = None  # restaurant_id if matched

    # Matching scores
    confidence_score: float = 0.0
    name_similarity: float = 0.0
    address_similarity: float = 0.0
    postcode_match: bool = False

    # Match metadata
    match_type: str = "unmatched"  # "exact_name", "similar_name", "partial_name", "unmatched"
    match_reason: Optional[str] = None
    matched_at: Optional[datetime] = None

    @property
    def is_matched(self) -> bool:
        """Check if this is a successful match."""
        return self.target_id is not None and self.confidence_score > 0
