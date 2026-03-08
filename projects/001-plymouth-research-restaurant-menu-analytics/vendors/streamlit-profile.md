# Vendor Profile: Streamlit

> **Template Origin**: Official | **ArcKit Version**: 4.0.1

## Document Control

| Field | Value |
|-------|-------|
| **Document ID** | streamlit-profile |
| **Document Type** | Vendor Profile |
| **Project** | Plymouth Research Restaurant Menu Analytics (Project 001) |
| **Classification** | PUBLIC |
| **Status** | PUBLISHED |
| **Version** | 1.2 |
| **Created Date** | 2026-02-20 |
| **Last Modified** | 2026-03-08 |
| **Review Cycle** | On-Demand |
| **Next Review Date** | 2027-03-08 |
| **Owner** | Lead Developer |
| **Reviewed By** | PENDING |
| **Approved By** | PENDING |
| **Distribution** | Development Team |
| **Source Research** | ARC-001-RSCH-v1.0, ARC-001-RSCH-v2.0, ARC-001-RSCH-v2.1 |
| **Confidence** | High |

## Revision History

| Version | Date | Author | Changes | Approved By | Approval Date |
|---------|------|--------|---------|-------------|---------------|
| 1.0 | 2026-02-20 | AI Agent | Initial creation from `/arckit:research` command. | PENDING | PENDING |
| 1.1 | 2026-03-08 | AI Agent | Updated and validated against `ARC-001-RSCH-v2.0`. Confirmed pricing and features are current. | PENDING | PENDING |
| 1.2 | 2026-03-08 | AI Agent | Refreshed against `ARC-001-RSCH-v2.1`. Reconfirmed Streamlit as the primary dashboard and hosting choice. | PENDING | PENDING |

---

## Overview

Streamlit is an open-source Python framework for building data applications and dashboards. It was acquired by Snowflake in March 2022. The framework enables data scientists to create interactive web applications using pure Python without front-end knowledge. The hosted platform is Streamlit Community Cloud.

## Products and Services

- **Streamlit OSS**: Open-source Python library (Apache-2.0). `pip install streamlit`.
- **Streamlit Community Cloud**: Free hosted platform for public Streamlit apps, GitHub-connected.
- **Streamlit in Snowflake**: Enterprise-grade deployment within Snowflake Data Cloud.

## Pricing Model

| Tier | Price | Limits |
|------|-------|--------|
| Community Cloud | Free | Public apps only, ~1 GB RAM, auto-sleep on inactivity |
| Streamlit in Snowflake | Snowflake compute pricing | Enterprise, contact for quote |

*Pricing verified March 2026 from https://streamlit.io/cloud*

## GitHub Statistics

- **Stars**: 43,600+
- **Licence**: Apache-2.0
- **Contributors**: 327+
- **Status**: Actively maintained
- **URL**: https://github.com/streamlit/streamlit

## UK Government Presence

Not applicable. Streamlit Community Cloud is hosted on AWS (US regions). For UK Gov projects requiring UK data residency, self-hosting on a UK-based cloud provider would be necessary.

## Strengths

- Zero cost for public apps on Community Cloud.
- No front-end knowledge required (pure Python).
- Automatic HTTPS/TLS on Community Cloud (resolves NFR-SEC-001).
- GitHub push-to-deploy integration.
- Built-in caching (`@st.cache_data`) for performance.
- Rich component library: charts, maps, tables.
- Large and active community.

## Weaknesses

- App auto-sleeps on Community Cloud if not accessed (cold start ~5–10s).
- Public GitHub repo required for Community Cloud.
- Limited built-in authentication and complex state management.
- Memory limited to ~1 GB on Community Cloud free tier.

## Compliance

- HTTPS/TLS provided automatically on Community Cloud.
- Data stored in the app's local filesystem (e.g., the SQLite file) is not persisted on Streamlit servers between sessions, but is accessible during an active session.

## Competitive Alternatives

| Alternative | Price | Key Difference |
|-------------|-------|----------------|
| Plotly Dash OSS | Free (MIT) | More control, steeper learning curve, no free cloud tier |
| Panel (HoloViz) | Free (BSD-3) | More flexible layout, smaller community |
| Flask/FastAPI | Free (MIT/Apache) | Full control, requires front-end work |

## Projects Referenced In

- **Project 001 — Plymouth Research Restaurant Menu Analytics** (Evaluated in `ARC-001-RSCH-v1.0` and `ARC-001-RSCH-v2.0`)

## Decision Notes

**Recommended**: Retain Streamlit for Project 001. It is fully implemented and functional. The Community Cloud offering resolves the NFR-SEC-001 (HTTPS) gap at zero cost. Migration to another framework like Dash is only necessary if future requirements demand complex multi-page routing or guaranteed always-on performance.
