# Tech Note: Streamlit Application Deployment

| Field | Value |
|-------|-------|
| **Topic** | Streamlit: Deployment Options, Limits, and Best Practices |
| **Category** | Hosting / Deployment / Dashboard Framework |
| **Last Updated** | 2026-02-20 |
| **Relevance to Projects** | Project 001 — Plymouth Research Restaurant Menu Analytics |

## Summary

Streamlit is the currently deployed dashboard framework for Plymouth Research (43,600+ GitHub stars, Apache-2.0). Streamlit Community Cloud provides free public app hosting with automatic HTTPS. Key deployment constraints: apps sleep on inactivity, ~1 GB RAM limit, public GitHub repo required. Render is the recommended fallback for always-on deployment at £5.50/month.

## Key Findings

1. **Streamlit Community Cloud free tier**: Unlimited public apps, no memory/CPU cost, GitHub push-to-deploy, automatic HTTPS (resolves NFR-SEC-001 immediately). Apps auto-sleep after inactivity (~5–10 second cold start on next visit). Public GitHub repo required.

2. **Memory constraint**: ~1 GB RAM per app on Community Cloud. Plymouth Research's 20 MB SQLite database + Pandas + Plotly + Pydeck fits comfortably. Adding DuckDB adds ~50 MB. No constraint at Phase 1 scale.

3. **App sleep behaviour**: The primary limitation of Community Cloud free tier. Apps sleep when not accessed. For internal research use (NFR-A-001 allows 7.2 hours downtime/month), this is acceptable. For high-traffic public launch, migrate to Render Starter at £5.50/month for always-on hosting.

4. **GitHub integration**: Community Cloud automatically deploys on push to the connected repository branch. Commit → deploy cycle is ~2–3 minutes. No additional CI/CD configuration needed for deployment.

5. **SQLite on Community Cloud**: The SQLite file is local to the app's filesystem on Community Cloud. It persists between restarts but resets on new deployments. For a data-pipeline workflow (scrape locally, deploy pre-populated database), the file must be regenerated or stored externally (S3, GitHub LFS).

6. **Snowflake migration path**: Streamlit is owned by Snowflake. "Streamlit in Snowflake" provides enterprise-grade deployment but requires Snowflake contract — not relevant for Plymouth Research's £100/month budget.

## Deployment Architecture

```
Developer (local) ──→ GitHub push ──→ Streamlit Community Cloud
                                           ↓
                                   Auto-deploy (2–3 min)
                                           ↓
                                   Public URL (HTTPS)
                                           ↓
                                   app reads Plymouth_research.db
                                   (local filesystem on Cloud instance)
```

## Best Practices for Plymouth Research

1. **Caching**: Use `@st.cache_data(ttl=3600)` for database queries (1-hour TTL already implemented)
2. **Database connection**: Use `@st.cache_resource` for SQLite connection to avoid reconnection overhead
3. **Secrets**: Store API keys in Streamlit secrets: `.streamlit/secrets.toml` (gitignored) → Community Cloud Secrets UI
4. **Requirements**: `requirements.txt` must list only dashboard dependencies (scraping deps commented out — already correct per current setup)
5. **Health check**: Use UptimeRobot to monitor Community Cloud URL (5-min intervals, free)

## Migration to Render (Phase 2)

```dockerfile
# Dockerfile for Render deployment
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "dashboard_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Render detects Python apps and Dockerfiles automatically. Deploy from same GitHub repo.

## Competitive Alternatives

| Platform | Free Tier | Always-On Cost | Notes |
|----------|-----------|----------------|-------|
| Streamlit Community Cloud | Yes (unlimited public) | N/A (sleep only) | Streamlit-optimised |
| Render | Yes (sleep after 15 min) | £5.50/month | Any Python/Docker |
| Railway | No | ~£8–12/month | Better DX, no free tier |
| Fly.io | No (trial only) | ~£4–8/month | Container-based, complex |
| Hetzner VPS | No | £3.60/month | Cheapest paid, high maintenance |

## Relevance to Projects

**Project 001**: Streamlit Community Cloud is current deployment. Provides immediate HTTPS (NFR-SEC-001 gap resolution). Sleep behaviour acceptable for Phase 1 internal use. Render Starter recommended trigger: when public launch drives consistent daily traffic requiring reliable availability.

## References

- Streamlit Cloud docs: https://docs.streamlit.io/deploy/streamlit-community-cloud
- Streamlit GitHub: https://github.com/streamlit/streamlit
- Render deployment guide: https://pythonandvba.com/blog/deploy-your-streamlit-app-to-render-free-heroku-alternative/
