# Vendor Profile: Plotly Dash

| Field | Value |
|-------|-------|
| **Vendor Name** | Plotly Inc. |
| **Category** | Data Application / Dashboard Framework |
| **Website** | https://plotly.com/dash/ |
| **Confidence** | Medium |
| **Last Researched** | 2026-02-20 |
| **Projects Referenced In** | Project 001 — Plymouth Research Restaurant Menu Analytics |

## Overview

Plotly Dash is a Python framework for building data applications and interactive dashboards. It uses a React.js front end, enabling complex, production-grade interactive UIs. The open source version (MIT licence) is self-hosted. Plotly Enterprise and Dash Enterprise offer managed cloud deployment with enterprise security features. Frequently compared to Streamlit as the more production-ready alternative with a steeper learning curve.

## Products and Services

- **Dash Open Source**: Free (MIT licence), self-hosted, full framework
- **Dash Enterprise**: Managed cloud deployment, enterprise auth, SSO — custom pricing
- **Plotly Cloud**: Managed deployment for Plotly/Dash apps

## Pricing Model

| Tier | Price | Notes |
|------|-------|-------|
| Dash OSS | Free (MIT) | Self-hosted, full framework |
| Dash Enterprise | Custom ($10K–$50K+/year estimated) | Enterprise only, contact Plotly |
| Plotly Cloud | Custom | Managed deployment |

*Enterprise pricing not publicly disclosed; estimated from market research.*

## GitHub Statistics

- **Stars**: 22,000+
- **Licence**: MIT
- **URL**: https://github.com/plotly/dash

## Key Features

- Component-based architecture (Dash Core Components, Dash HTML Components)
- Callback pattern: reactive UI with `@app.callback` decorators
- Multi-page apps: native URL routing (advantage over Streamlit)
- Better for complex interactivity than Streamlit
- Bootstrap/Mantine/Ant Design themes available
- 100% Python (no JavaScript required for standard use)
- Production-ready performance with React.js rendering

## UK Government Presence

Not applicable — Plotly is a US company. No G-Cloud listing.

## Strengths

- More production-ready than Streamlit for complex applications
- Native multi-page routing (important for Phase 2 public site)
- Better performance for complex interactivity
- Well-maintained, active community
- MIT licence for OSS version

## Weaknesses

- Steeper learning curve than Streamlit (callback pattern vs script)
- No free managed hosting equivalent to Streamlit Community Cloud
- More code required for same functionality vs Streamlit
- Enterprise pricing far exceeds Plymouth Research budget

## Competitive Alternatives

See Streamlit vendor profile for direct comparison.

## Decision Notes

**Not recommended for Phase 1**: Streamlit is already implemented and sufficient. Migration to Dash would require rewriting the entire dashboard (2,053 lines of `dashboard_app.py`) with no immediate benefit.

**Consider for Phase 2**: If public launch drives requirements for complex multi-page routing, proper URL-based navigation, or 100+ concurrent users, Dash OSS + Render deployment is a viable migration path at ~£5.50/month (Render Starter).
