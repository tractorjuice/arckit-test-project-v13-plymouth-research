# Tech Note: SQLite for Analytics Applications

| Field | Value |
|-------|-------|
| **Topic** | SQLite: Capabilities, Limits, and Optimisation for Analytics |
| **Category** | Database |
| **Last Updated** | 2026-02-20 |
| **Relevance to Projects** | Project 001 — Plymouth Research Restaurant Menu Analytics |

## Summary

SQLite is a public domain, serverless, embedded relational database. It is the world's most widely deployed database engine. For Plymouth Research's current scale (243 restaurants, 2,625 menu items, 9,410 reviews), SQLite is entirely appropriate and performs well. At 1,000+ restaurants with concurrent multi-user writes, migration to PostgreSQL should be evaluated.

## Key Findings

1. **Current scale is well within SQLite's capabilities**: SQLite theoretical max is 2^64 rows per table. At 1 million rows, well-optimised SQLite queries complete in milliseconds. Plymouth Research's 20 MB database is trivially small.

2. **Performance ceiling**: At 100,000+ menu items (10x current scale), SQLite remains viable with:
   - Covering indexes on `cuisine_type`, `price`, dietary boolean fields
   - FTS5 (Full-Text Search) virtual table for text search across menu items
   - WAL (Write-Ahead Logging) mode for concurrent read/write access
   - ANALYZE and VACUUM periodic maintenance

3. **Single-writer limitation**: SQLite allows only one write transaction at a time (single-writer, multiple-reader). This is not a concern for Plymouth Research (batch scraping runs sequentially, dashboard is read-only).

4. **Python integration**: Built-in `sqlite3` module — no pip install. Pandas `.to_sql()` and `.read_sql()` work natively with SQLite connections.

5. **Streamlit Cloud compatibility**: SQLite database file is included in the deployed app's filesystem. However, it is reset on each deployment — requires external storage (GitHub LFS, S3) for persistence. Current approach: SQLite file regenerated from scraping data.

6. **Benchmark (DuckDB vs SQLite vs Pandas on 1M rows)**: SQLite is slowest for aggregations (DuckDB is 10–100x faster), but for Plymouth Research's query patterns and data size, the difference is imperceptible (<100ms vs <1ms).

## Optimisation Checklist for Plymouth Research

```sql
-- Enable WAL mode for concurrent reads during scraping
PRAGMA journal_mode=WAL;

-- Critical covering indexes (already partially implemented)
CREATE INDEX IF NOT EXISTS idx_menu_cuisine_price
  ON menu_items(restaurant_id, price, is_vegan, is_vegetarian, is_gluten_free);

CREATE INDEX IF NOT EXISTS idx_restaurants_active_cuisine
  ON restaurants(is_active, cuisine_type, hygiene_rating);

-- FTS5 for menu item search
CREATE VIRTUAL TABLE IF NOT EXISTS menu_items_fts
  USING fts5(item_name, description, content=menu_items, content_rowid=item_id);

-- Periodic maintenance (run quarterly)
PRAGMA optimize;
VACUUM;
ANALYZE;
```

## Migration Trigger: When to Move to PostgreSQL

| Trigger | Threshold |
|---------|-----------|
| Restaurant count | > 1,000 restaurants |
| Menu items | > 100,000 items (with heavy concurrent queries) |
| Concurrent writers | > 1 (e.g., multiple scraping workers, restaurant owner portal) |
| Page load time | > 2s consistently (NFR-P-001 breach) |
| User count | > 100 concurrent dashboard users (NFR-S-002) |

## Migration Path

When migration is needed: Supabase Free (London region) — 500 MB free, PostgreSQL-compatible, REST API.

## References

- SQLite limits: https://sqlite.org/limits.html
- SQLite FTS5: https://sqlite.org/fts5.html
- DuckDB vs SQLite benchmark: https://www.kdnuggets.com/we-benchmarked-duckdb-sqlite-and-pandas-on-1m-rows-heres-what-happened
