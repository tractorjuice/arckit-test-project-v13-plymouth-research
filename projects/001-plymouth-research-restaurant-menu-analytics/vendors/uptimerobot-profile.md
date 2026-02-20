# Vendor Profile: UptimeRobot

| Field | Value |
|-------|-------|
| **Vendor Name** | UptimeRobot |
| **Category** | Website Uptime Monitoring |
| **Website** | https://uptimerobot.com |
| **Confidence** | High |
| **Last Researched** | 2026-02-20 |
| **Projects Referenced In** | Project 001 — Plymouth Research Restaurant Menu Analytics |

## Overview

UptimeRobot is a cloud-based website uptime monitoring service. It provides periodic checks of websites, APIs, and services, alerting operators when services go down. The free tier is notably generous with 50 monitors — far more than most competitors offer at zero cost.

## Products and Services

- **Free plan**: 50 monitors, 5-minute check intervals
- **Pro plan**: 10 monitors, 60-second intervals, SSL monitoring
- **Team plan**: 100 monitors, team collaboration
- **Public Status Pages**: Available on all plans

## Pricing Model

| Tier | Price (monthly) | Monitors | Check Interval | Features |
|------|----------------|---------|----------------|---------|
| Free | £0 | 50 | 5 minutes | HTTP, port, ping, keyword, heartbeat; basic status pages; 5 integrations |
| Pro | ~£6 | 10 | 60 seconds | SSL/domain expiry; advanced alerts |
| Team (popular) | ~£23 | 100 | 60 seconds | 3 team members, API access |

*Pricing verified February 2026 from https://uptimerobot.com/pricing/*

## Key Features

- Monitor types: HTTP(S), keyword, ping, port, heartbeat
- Alert channels: email, SMS, Slack, Discord, Telegram, webhooks (15+ integrations)
- Public status page: share uptime metrics with users
- SSL certificate monitoring (Pro+)
- Domain expiry monitoring (Pro+)
- API for programmatic access to monitor data

## UK Government Presence

Not applicable — SaaS monitoring service. No special UK Government pricing or G-Cloud listing identified.

## Strengths

- Generous free tier (50 monitors vs 1–5 for most competitors)
- Zero configuration required — set up a monitor in 2 minutes
- Reliable notification system with multiple channels
- Public status page useful for communicating dashboard status
- No credit card required for free tier
- Long-established service (founded 2010), trusted uptime history

## Weaknesses

- Free tier check interval is 5 minutes (not real-time)
- No advanced analytics or historical trending on free plan
- Limited to 5 integrations on free plan

## Compliance

- Cloud-based service hosted in US
- Stores no sensitive data (only URL to monitor, not application data)
- GDPR: data processing agreement available

## Competitive Alternatives

| Alternative | Free Tier | Key Difference |
|-------------|-----------|----------------|
| Better Uptime | 10 monitors free | Better UI, incident management |
| Freshping | 50 monitors free | Similar to UptimeRobot |
| Uptime.com | 1 monitor free | Enterprise focus, expensive |
| StatusCake | 10 checks free | UK-based company |
| Grafana Cloud | Synthetic monitoring | More complex setup |

## Decision Notes

**Recommended**: Adopt UptimeRobot Free for Plymouth Research Project 001. Directly addresses NFR-A-001 (uptime monitoring) gap identified as high-priority in requirements document. Implementation time: 30 minutes. Cost: £0. Configure one monitor for the Streamlit Community Cloud URL with email + Slack notifications to the Research Director.
