# Tech Note: DuckDB as an Embedded Analytics Engine

| Field | Value |
|-------|-------|
| **Topic** | DuckDB: In-Process OLAP for Python Analytics |
| **Category** | Database / Analytics |
| **Last Updated** | 2026-02-20 |
| **Relevance to Projects** | Project 001 — Plymouth Research Restaurant Menu Analytics |

## Summary

DuckDB is a free, open-source, in-process OLAP database optimised for analytical queries. It runs embedded within a Python application (like SQLite), requires no server, and delivers 10–100x faster aggregation queries than SQLite for analytical workloads. Version 1.0.0 (2024) guarantees stable storage format. MIT licence with statutes ensuring permanent open-source status.

## Key Findings

1. **Performance**: DuckDB is 10–100x faster than SQLite for aggregation-heavy queries (GROUP BY, COUNT, SUM, AVG). For Plymouth Research dashboard analytics tabs (Price Analysis, Cuisine Comparison), replacing pandas aggregations with DuckDB SQL queries would significantly reduce load times.

2. **In-process deployment**: Like SQLite, DuckDB runs within the Python process — no server to manage, no network overhead. Compatible with Streamlit Cloud (runs in same Python process as dashboard_app.py).

3. **SQLite interoperability**: DuckDB can query SQLite database files directly using `ATTACH 'plymouth_research.db' AS prd (TYPE sqlite)` — no migration needed. Use DuckDB for reads, SQLite for writes.

4. **MIT licence, no commercial version**: DuckDB Foundation statutes guarantee the engine remains MIT-licensed permanently. No enterprise tier exists. "DuckDB is free for everyone, forever."

5. **GitHub stars**: 25,000+ (December 2024 milestone). 20,000 stars in June 2024. Rapid community growth.

6. **2024 benchmarks**: ~20% year-over-year performance improvement; joins 4x faster over 3 years; Parquet export 4–5x faster since 2023.

7. **Python integration**: Native DuckDB Python API, integrates with Pandas DataFrames. Query a DataFrame with SQL: `duckdb.query("SELECT * FROM df WHERE price > 10").fetchdf()`.

## Plymouth Research Use Cases

| Dashboard Tab | Current Implementation | DuckDB Enhancement |
|---------------|----------------------|-------------------|
| Price Analysis (FR-003) | Pandas groupby + Plotly | DuckDB `SELECT cuisine_type, AVG(price) FROM menu_items GROUP BY cuisine_type` |
| Cuisine Comparison | Pandas crosstab | DuckDB multi-table join with SQLite data |
| Dietary Options | Pandas boolean filter | DuckDB columnar scan with filter |
| Reviews Correlation (UC-007) | Pandas merge | DuckDB join across trustpilot_reviews + restaurants |

## Implementation Pattern

```python
# pip install duckdb
import duckdb

# Query SQLite database directly (no import needed)
conn = duckdb.connect()
conn.execute("ATTACH 'plymouth_research.db' AS prd (TYPE sqlite)")

# Analytical query — much faster than pandas equivalent
result = conn.execute("""
    SELECT cuisine_type,
           AVG(price) as avg_price,
           COUNT(*) as item_count
    FROM prd.menu_items m
    JOIN prd.restaurants r ON m.restaurant_id = r.restaurant_id
    WHERE r.is_active = 1
    GROUP BY cuisine_type
    ORDER BY avg_price DESC
""").fetchdf()
```

## Architecture Recommendation

**SQLite + DuckDB Hybrid**:
- SQLite: primary write/transactional store (scraping results, opt-out updates, manual matches)
- DuckDB: analytical query engine for dashboard read queries
- Same file: DuckDB reads from SQLite file directly — single source of truth maintained

## References

- DuckDB website: https://duckdb.org/why_duckdb
- DuckDB GitHub: https://github.com/duckdb/duckdb
- DuckDB Python docs: https://duckdb.org/docs/api/python/overview
- DuckDB benchmarks: https://duckdb.org/2024/06/26/benchmarks-over-time
- SQLite interop: https://duckdb.org/docs/extensions/sqlite
