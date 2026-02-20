# Vendor Profile: Streamlit

| Field | Value |
|-------|-------|
| **Vendor Name** | Streamlit (Snowflake) |
| **Category** | Dashboard / Data Application Framework |
| **Website** | https://streamlit.io |
| **Confidence** | High |
| **Last Researched** | 2026-02-20 |
| **Projects Referenced In** | Project 001 — Plymouth Research Restaurant Menu Analytics |

## Overview

Streamlit is an open-source Python framework for building data applications and dashboards. It was acquired by Snowflake in March 2022. The framework enables data scientists to create interactive web applications using pure Python without front-end knowledge. The hosted platform is Streamlit Community Cloud.

## Products and Services

- **Streamlit OSS**: Open-source Python library (Apache-2.0). pip install streamlit.
- **Streamlit Community Cloud**: Free hosted platform for public Streamlit apps, GitHub-connected.
- **Streamlit in Snowflake**: Enterprise-grade deployment within Snowflake Data Cloud.

## Pricing Model

| Tier | Price | Limits |
|------|-------|--------|
| Community Cloud | Free | Public apps only, ~1 GB RAM, auto-sleep on inactivity |
| Streamlit in Snowflake | Snowflake compute pricing | Enterprise, contact for quote |

*Pricing verified February 2026 from https://streamlit.io/cloud*

## GitHub Statistics

- **Stars**: 43,600+
- **Licence**: Apache-2.0
- **Contributors**: 327
- **Status**: Actively maintained
- **URL**: https://github.com/streamlit/streamlit

## UK Government Presence

Not applicable — independent commercial research project. Streamlit Community Cloud is hosted on AWS (US regions). Data stored locally in SQLite, not uploaded to Streamlit servers.

## Strengths

- Zero cost for public apps on Community Cloud
- No front-end knowledge required (pure Python)
- Automatic HTTPS/TLS on Community Cloud
- GitHub push-to-deploy integration
- Built-in caching (configurable TTL)
- Rich component library: charts, maps (pydeck), tables, file upload
- Used by Fortune 500 companies (10,000+ organisations)

## Weaknesses

- App auto-sleeps on Community Cloud if not accessed (cold start ~5–10s)
- Public GitHub repo required for Community Cloud
- No built-in authentication or access control
- Limited URL routing for multi-page complex applications
- Memory limited to ~1 GB on Community Cloud free tier
- Script-based architecture not ideal for complex state management

## Compliance

- HTTPS/TLS provided automatically on Community Cloud
- Data stored in app's local filesystem (SQLite file) — not persisted on Streamlit servers
- No PII processed by Streamlit platform

## Competitive Alternatives

| Alternative | Price | Key Difference |
|-------------|-------|----------------|
| Plotly Dash OSS | Free (MIT) | More control, steeper learning curve, no free cloud tier |
| Panel (HoloViz) | Free (BSD-3) | More flexible layout, smaller community |
| Marimo | Free (Apache-2.0) | Reactive notebook-first, emerging framework |
| Flask/FastAPI | Free (MIT/Apache) | Full control, requires front-end work |

## Decision Notes

**Recommended**: Retain Streamlit for Plymouth Research Project 001. Current platform is fully implemented and functional. Migrate to Dash only if Phase 2 requires complex multi-page routing or 100+ concurrent users consistently. Community Cloud resolves the NFR-SEC-001 (HTTPS) gap at zero cost.
