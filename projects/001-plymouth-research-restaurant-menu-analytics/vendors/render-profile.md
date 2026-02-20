# Vendor Profile: Render

| Field | Value |
|-------|-------|
| **Vendor Name** | Render (Render Services Inc.) |
| **Category** | Cloud Application Hosting |
| **Website** | https://render.com |
| **Confidence** | Medium |
| **Last Researched** | 2026-02-20 |
| **Projects Referenced In** | Project 001 — Plymouth Research Restaurant Menu Analytics |

## Overview

Render is a cloud platform for deploying and scaling web services, background workers, cron jobs, and databases. It targets developers who want managed hosting with minimal DevOps overhead. It positions itself as a Heroku alternative with a modern pricing model.

## Products and Services

- **Web Services**: Deploy Python, Node.js, Ruby, Docker containers
- **Static Sites**: Host static files, SPA
- **Background Workers**: Long-running processes
- **Cron Jobs**: Scheduled tasks
- **Databases**: Managed PostgreSQL

## Pricing Model

| Tier | Price (monthly) | RAM | CPU | Notes |
|------|----------------|-----|-----|-------|
| Free | £0 | 512 MB | Shared | Auto-sleep after 15 min inactivity, 750 hours/month, 100 GB bandwidth |
| Starter | ~£5.50 | 512 MB | 0.5 vCPU | Always-on, no sleep, unlimited hours |
| Standard | ~£20 | 2 GB | 1 vCPU | Production workloads |
| Pro | ~£85 | 4 GB | 2 vCPU | High-traffic |

*Pricing verified February 2026 from https://render.com and https://www.freetiers.com/directory/render*

## Key Features

- Deploy from GitHub repository (push-to-deploy, like Streamlit Cloud)
- Free HTTPS/TLS on all tiers
- Custom domains on all tiers (including free)
- PostgreSQL managed database (free tier: 1 GB, deleted after 90 days)
- No Streamlit branding restriction (vs Streamlit Community Cloud which shows Streamlit badge)
- Environment variables / secrets management
- Automatic deploys on Git push
- Health checks and automatic restarts

## UK Government Presence

Not applicable. Render is a US company, data centres in multiple AWS regions. No UK-specific G-Cloud listing.

## Strengths

- Free tier comparable to Streamlit Community Cloud
- Starter plan at ~£5.50/month provides always-on service (resolves NFR-A-001 sleep issue)
- Deploy any Python/Docker app (not limited to Streamlit)
- Custom domains on free tier
- No credit card required for free account

## Weaknesses

- Free tier auto-sleeps after 15 minutes (similar limitation to Streamlit Cloud)
- Free PostgreSQL deleted after 90 days (not suitable for persistent DB)
- Fewer Python-specific features than Streamlit Community Cloud
- Limited compute on free tier (512 MB RAM) — may be tight for DuckDB + SQLite + Streamlit

## Compliance

- US-hosted (AWS infrastructure)
- SOC 2 Type II certified
- GDPR compliance available
- Acceptable for Plymouth Research (public data, no PII)

## Competitive Alternatives

| Alternative | Free Tier | Key Difference |
|-------------|-----------|----------------|
| Streamlit Community Cloud | Yes (unlimited public apps) | Streamlit-optimised, auto HTTPS, easier Streamlit deployment |
| Railway | No (credits only) | Better DX, no meaningful free tier |
| Fly.io | No (trial only) | Global deployment, complex pricing |
| Heroku | No meaningful free tier | Legacy platform, expensive |
| Hetzner VPS | No (paid from £3.60/month) | Cheapest paid but high maintenance |

## Decision Notes

**Recommended**: Pre-configure Render as deployment fallback for Plymouth Research Project 001. Current primary deployment is Streamlit Community Cloud (free). When public launch drives consistent traffic requiring always-on uptime (NFR-A-001), migrate to Render Starter at ~£5.50/month. Total Phase 2 cost remains well within £100/month budget (BR-003).
