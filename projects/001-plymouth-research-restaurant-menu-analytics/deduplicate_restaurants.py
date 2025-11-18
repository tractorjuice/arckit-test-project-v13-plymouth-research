#!/usr/bin/env python3
"""
Deduplicate Restaurants Script
===============================

Finds and merges duplicate restaurant entries in the database.

Duplicates identified by:
- Similar restaurant names (ignoring "The" and "Plymouth")
- Same website domain

For each duplicate set:
1. Keep the entry with the most menu items
2. Merge unique menu items from other entries
3. Delete duplicate entries

Author: Plymouth Research Team
Date: 2025-11-18
"""

import sqlite3
from pathlib import Path
from typing import List, Dict, Set
import re


def normalize_name(name: str) -> str:
    """Normalize restaurant name for comparison."""
    normalized = name.lower()
    normalized = re.sub(r'\bthe\b', '', normalized)
    normalized = re.sub(r'\bplymouth\b', '', normalized)
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    return normalized


def get_domain(url: str) -> str:
    """Extract domain from URL."""
    if not url:
        return ""
    # Remove protocol
    domain = re.sub(r'^https?://', '', url)
    # Remove www
    domain = re.sub(r'^www\.', '', domain)
    # Take first 30 chars for comparison
    return domain[:30].lower()


def find_duplicates(conn: sqlite3.Connection) -> Dict[str, List[int]]:
    """Find duplicate restaurant entries."""
    cursor = conn.cursor()

    # Get all real_scraped restaurants
    cursor.execute("""
        SELECT restaurant_id, name, website_url
        FROM restaurants
        WHERE data_source = 'real_scraped'
        ORDER BY restaurant_id
    """)

    restaurants = cursor.fetchall()

    # Group by normalized name and domain
    groups: Dict[str, List[int]] = {}

    for resto_id, name, url in restaurants:
        # Create key from normalized name
        key = normalize_name(name)

        if key not in groups:
            groups[key] = []
        groups[key].append(resto_id)

    # Filter to only duplicates (groups with > 1 entry)
    duplicates = {k: v for k, v in groups.items() if len(v) > 1}

    return duplicates


def get_restaurant_info(conn: sqlite3.Connection, resto_id: int) -> Dict:
    """Get restaurant details including menu item count."""
    cursor = conn.cursor()

    cursor.execute("""
        SELECT r.restaurant_id, r.name, r.website_url,
               COUNT(mi.item_id) as item_count
        FROM restaurants r
        LEFT JOIN menu_items mi ON r.restaurant_id = mi.restaurant_id
        WHERE r.restaurant_id = ?
        GROUP BY r.restaurant_id
    """, (resto_id,))

    row = cursor.fetchone()
    return {
        'id': row[0],
        'name': row[1],
        'url': row[2],
        'item_count': row[3]
    }


def merge_duplicates(conn: sqlite3.Connection, duplicate_ids: List[int]) -> int:
    """
    Merge duplicate restaurant entries.

    Returns: ID of the kept restaurant
    """
    cursor = conn.cursor()

    # Get info for all duplicates
    infos = [get_restaurant_info(conn, rid) for rid in duplicate_ids]

    # Sort by item count (descending) - keep the one with most items
    infos.sort(key=lambda x: x['item_count'], reverse=True)

    keeper = infos[0]
    to_delete = infos[1:]

    print(f"\n📍 Merging: {keeper['name']}")
    print(f"   Keeping ID {keeper['id']} ({keeper['item_count']} items)")

    for dup in to_delete:
        print(f"   Deleting ID {dup['id']} ({dup['item_count']} items)")

        # Move unique menu items from duplicate to keeper
        cursor.execute("""
            UPDATE menu_items
            SET restaurant_id = ?
            WHERE restaurant_id = ?
            AND name NOT IN (
                SELECT name FROM menu_items WHERE restaurant_id = ?
            )
        """, (keeper['id'], dup['id'], keeper['id']))

        moved = cursor.rowcount
        if moved > 0:
            print(f"      → Moved {moved} unique items to keeper")

        # Delete remaining duplicate items
        cursor.execute("DELETE FROM menu_items WHERE restaurant_id = ?", (dup['id'],))

        # Delete duplicate restaurant
        cursor.execute("DELETE FROM restaurants WHERE restaurant_id = ?", (dup['id'],))

    return keeper['id']


def main():
    """Main deduplication process."""
    db_path = Path(__file__).parent / "plymouth_research.db"

    if not db_path.exists():
        print(f"❌ Database not found: {db_path}")
        return

    conn = sqlite3.connect(str(db_path))

    try:
        # Find duplicates
        print("🔍 Searching for duplicate restaurants...")
        duplicates = find_duplicates(conn)

        if not duplicates:
            print("✅ No duplicates found!")
            return

        print(f"\n📊 Found {len(duplicates)} restaurant names with duplicates:")

        total_entries = sum(len(ids) for ids in duplicates.values())
        entries_to_remove = total_entries - len(duplicates)

        print(f"   • {total_entries} total duplicate entries")
        print(f"   • {entries_to_remove} entries will be removed")
        print(f"   • {len(duplicates)} restaurants will remain")

        # Show summary
        print("\n📋 Duplicate sets:")
        for norm_name, resto_ids in list(duplicates.items())[:10]:
            infos = [get_restaurant_info(conn, rid) for rid in resto_ids]
            print(f"   • {infos[0]['name']}: {len(resto_ids)} entries")

        if len(duplicates) > 10:
            print(f"   ... and {len(duplicates) - 10} more")

        # Confirm
        response = input("\n⚠️  Proceed with deduplication? (yes/no): ")
        if response.lower() != 'yes':
            print("❌ Cancelled")
            return

        # Process each duplicate set
        print("\n🔄 Merging duplicates...")

        kept_ids = []
        for norm_name, resto_ids in duplicates.items():
            keeper_id = merge_duplicates(conn, resto_ids)
            kept_ids.append(keeper_id)

        # Commit changes
        conn.commit()

        # Show results
        print("\n" + "="*60)
        print("✅ Deduplication Complete!")
        print("="*60)

        cursor = conn.cursor()

        # Count remaining restaurants
        cursor.execute("SELECT COUNT(*) FROM restaurants WHERE data_source = 'real_scraped'")
        remaining = cursor.fetchone()[0]

        # Count total menu items
        cursor.execute("SELECT COUNT(*) FROM menu_items")
        total_items = cursor.fetchone()[0]

        print(f"\n📊 Final Statistics:")
        print(f"   • Restaurants (real data): {remaining}")
        print(f"   • Duplicate entries removed: {entries_to_remove}")
        print(f"   • Total menu items: {total_items}")

    except Exception as e:
        conn.rollback()
        print(f"\n❌ Error: {e}")
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    main()
