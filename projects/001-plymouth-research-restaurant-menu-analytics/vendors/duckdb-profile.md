# Vendor Profile: DuckDB

> **Template Origin**: Official | **ArcKit Version**: 4.0.1

## Document Control

| Field | Value |
|-------|-------|
| **Document ID** | duckdb-profile |
| **Document Type** | Vendor Profile |
| **Project** | Plymouth Research Restaurant Menu Analytics (Project 001) |
| **Classification** | PUBLIC |
| **Status** | PUBLISHED |
| **Version** | 1.1 |
| **Created Date** | 2026-02-20 |
| **Last Modified** | 2026-03-08 |
| **Review Cycle** | On-Demand |
| **Next Review Date** | 2027-03-08 |
| **Owner** | Data Architect |
| **Reviewed By** | PENDING |
| **Approved By** | PENDING |
| **Distribution** | Development Team |
| **Source Research** | ARC-001-RSCH-v1.0, ARC-001-RSCH-v2.0 |
| **Confidence** | High |

## Revision History

| Version | Date | Author | Changes | Approved By | Approval Date |
|---------|------|--------|---------|-------------|---------------|
| 1.0 | 2026-02-20 | AI Agent | Initial creation from `/arckit:research` command. | PENDING | PENDING |
| 1.1 | 2026-03-08 | AI Agent | Updated and validated against `ARC-001-RSCH-v2.0`. Added detail on SQLite interoperability. | PENDING | PENDING |

---

## Overview

DuckDB is an open-source, in-process OLAP (Online Analytical Processing) database system optimised for analytical queries. Unlike traditional client-server databases, DuckDB runs embedded within the host application process (similar to SQLite) and is specifically designed for fast aggregation, grouping, and analytical workloads. Version 1.0.0 was released in 2024, introducing a stable storage format.

## Products and Services

- **DuckDB OSS**: The core in-process SQL OLAP database engine (MIT licence).
- **Python Package**: The primary interface for Python applications (`pip install duckdb`).
- **DuckDB CLI**: A standalone command-line interface for database management.

Note: There is no commercial enterprise version. The DuckDB Foundation's statutes guarantee the engine remains MIT-licensed in perpetuity.

## Pricing Model

| Tier | Price | Notes |
|------|-------|-------|
| DuckDB OSS | Free (MIT) | Core engine and all clients (Python, R, Java, etc.) are free. |
| Enterprise | N/A | No enterprise tier exists. |

*DuckDB is completely free, with no commercial upsell.*

## GitHub Statistics

- **Stars**: 25,000+ (as of Dec 2024)
- **Licence**: MIT
- **Status**: Actively developed, stable 1.x series.
- **URL**: https://github.com/duckdb/duckdb

## Key Features

- **Columnar Storage**: Optimized for read-heavy analytical queries by reading only the necessary columns.
- **Vectorized Execution**: Processes data in batches (vectors) for high performance.
- **Direct Data Reading**: Can query SQLite files, Parquet files, CSVs, and Pandas DataFrames directly without an import/ETL step.
- **In-process**: Zero network overhead and simple deployment, as it runs within the application.
- **Full SQL Support**: Supports complex SQL including window functions, CTEs, and joins.

## UK Government Presence

Not applicable. DuckDB is a library, not a hosted service, so data remains on the project's own infrastructure.

## Strengths

- **MIT Licence**: Truly free with no restrictions and no enterprise upsell.
- **Performance**: 10-100x faster than row-stores like SQLite for analytical queries.
- **Simplicity**: As easy to deploy as SQLite (no server to manage).
- **Interoperability**: Can read the existing `plymouth_research.db` SQLite file directly, allowing for a hybrid analytical approach without data migration.
- **Guaranteed Open Source**: The DuckDB Foundation's statutes ensure it will always be open source.

## Weaknesses

- Not optimized for high-concurrency, write-heavy (OLTP) workloads; SQLite or PostgreSQL are better for that.
- The ecosystem is newer and smaller than that of PostgreSQL.
- Storage format can change between major versions (though stable since v1.0.0).

## Compliance

- The MIT licence is permissive and has no restrictions on commercial or government use.
- As it's self-hosted, data residency and compliance are the responsibility of the implementer.

## Competitive Alternatives

| Alternative | Price | Key Difference |
|-------------|-------|----------------|
| SQLite | Free | Row-oriented, better for writes, but much slower for analytics. |
| PostgreSQL | Free | Server-based, better for multi-user writes, but more complex to deploy. |
| Pandas | Free | In-memory DataFrame operations, but generally less performant for large aggregations and lacks a SQL interface. |

## Projects Referenced In

- **Project 001 — Plymouth Research Restaurant Menu Analytics** (Evaluated in `ARC-001-RSCH-v1.0` and `ARC-001-RSCH-v2.0`)

## Decision Notes

**Recommended**: Add DuckDB as the analytical query layer for Project 001, sitting alongside the existing SQLite database. It should be used to replace the pandas-based aggregations in the Streamlit dashboard's analytics tabs. This is a zero-cost, low-effort (est. 1 week) change that will yield significant performance improvements for analytical queries.
