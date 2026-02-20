# Vendor Profile: DuckDB

| Field | Value |
|-------|-------|
| **Vendor Name** | DuckDB Foundation |
| **Category** | Analytical In-Process Database |
| **Website** | https://duckdb.org |
| **Confidence** | High |
| **Last Researched** | 2026-02-20 |
| **Projects Referenced In** | Project 001 — Plymouth Research Restaurant Menu Analytics |

## Overview

DuckDB is an open-source, in-process OLAP (Online Analytical Processing) database system optimised for analytical queries. Unlike traditional client-server databases, DuckDB runs embedded within the host application process (similar to SQLite) and is specifically designed for fast aggregation, grouping, and analytical workloads. Version 1.0.0 was released in 2024, introducing a stable storage format with backwards compatibility guarantees.

## Products and Services

- **DuckDB OSS**: In-process SQL OLAP database (MIT licence)
- **DuckDB Python package**: pip install duckdb
- **DuckDB CLI**: Standalone command-line interface
- **DuckDB WASM**: Browser-based version
- **DuckDB UI**: Local web UI (released 2025, not open source — but core engine remains MIT)

Note: There is no enterprise version or commercial offering. DuckDB Foundation statutes guarantee the engine remains MIT-licensed in perpetuity.

## Pricing Model

| Tier | Price | Notes |
|------|-------|-------|
| DuckDB OSS | Free (MIT) | Core engine, Python/R/Java/WASM clients |
| DuckDB UI | Free download | Not open source, but free to use |
| Enterprise | N/A | No enterprise tier exists |

*All components of DuckDB are free. There is no commercial upsell.*

## GitHub Statistics

- **Stars**: 25,000+ (milestone reached December 2024; 20,000 stars in June 2024)
- **Licence**: MIT
- **Status**: Actively developed, stable 1.x series
- **URL**: https://github.com/duckdb/duckdb

## Performance Benchmarks (2024)

- Aggregation queries: 10–100x faster than SQLite for OLAP workloads
- Join speeds improved 4x over last 3 years
- Parquet export improved 4–5x since 2023
- ~20% year-over-year performance improvement in 2024 benchmarks
- At 4 vCores: DuckDB ~1.6x faster than Apache Spark with NEE

## Key Features

- Columnar storage: optimised for read-heavy analytical queries
- Reads SQLite, Parquet, CSV, JSON files directly (no import needed)
- Native Python/Pandas integration: query DataFrames with SQL
- Parallel query execution
- In-process: zero network overhead, same deployment model as SQLite
- Full SQL support including window functions, CTEs, lateral joins

## UK Government Presence

Not applicable — DuckDB is a library, not a hosted service. Data remains on local infrastructure.

## Strengths

- MIT licence — truly free, no enterprise upsell
- In-process: same deployment simplicity as SQLite (no server to manage)
- Reads existing SQLite database files directly
- Dramatically faster for analytics aggregations (price analysis, cuisine comparison)
- Zero infrastructure change to adopt
- Statutes guarantee open-source status permanently

## Weaknesses

- OLAP optimised: not ideal for high-concurrency write workloads (use SQLite for writes)
- DuckDB UI not open source (though CLI/Python API are)
- Newer ecosystem than PostgreSQL (fewer community resources)
- Storage format changes between major versions (stable from v1.0+)

## Compliance

- MIT licence: no restrictions on commercial or government use
- Data stored locally — no cloud transmission

## Competitive Alternatives

| Alternative | Price | Key Difference |
|-------------|-------|----------------|
| SQLite | Free (Public Domain) | Row-oriented, better for writes, slower analytics |
| PostgreSQL | Free (PostgreSQL Licence) | Server-based, multi-user, more complex deployment |
| Pandas | Free (BSD-3) | DataFrame operations, no SQL, less performant for aggregations |

## Decision Notes

**Recommended**: Add DuckDB as analytical query layer alongside existing SQLite for Plymouth Research Project 001. Replace pandas aggregations in Streamlit dashboard analytics tabs (Price Analysis, Cuisine Comparison, Dietary Options) with DuckDB SQL queries. SQLite remains the primary write/transactional database. Estimated 1 week implementation, zero cost, significant analytical performance improvement.
