# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an **ArcKit v0.9.1 test project** for Plymouth Research, a restaurant menu scraping and analytics platform. The repository contains both **enterprise architecture governance artifacts** and a **working implementation** (project 001).

**Key Context**:
- **Business Domain**: Web scraping, data analytics, restaurant menu aggregation
- **Tech Stack**: Python (BeautifulSoup/Scrapy), SQLite, Streamlit
- **Current Status**: 98 restaurants, 2,625 menu items, FSA hygiene ratings integrated
- **Target**: 150+ restaurants in Plymouth, UK; 10,000+ menu items
- **Phase**: MVP dashboard implemented with ongoing data collection

## Repository Structure

This repository is organized around **architecture governance artifacts**, not source code:

```
.arckit/
├── scripts/bash/        # 5 helper scripts for project management
│   ├── common.sh                    # Shared utilities
│   ├── create-project.sh           # Create new architecture projects
│   ├── list-projects.sh            # List and navigate projects
│   ├── check-prerequisites.sh      # Validate environment
│   └── generate-document-id.sh     # Generate unique doc IDs
└── templates/           # 37 document templates (ADR, DPIA, requirements, etc.)

.claude/commands/        # 35 slash commands for architecture governance
.codex/prompts/          # Codex CLI prompts (mirror of Claude commands)
.gemini/commands/        # Gemini CLI commands (mirror of Claude commands)

projects/                # Individual architecture projects
└── 001-plymouth-research-restaurant-menu-analytics/
    ├── dashboard_app.py              # Main Streamlit dashboard (1,687 lines)
    ├── fetch_hygiene_ratings_v2.py   # FSA data fetcher
    ├── plymouth_research.db          # SQLite database (excluded from git)
    ├── CLAUDE.md                     # Implementation-specific guide
    ├── HYGIENE_RATINGS_GUIDE.md      # FSA rating system documentation
    └── add_hygiene_columns.sql       # Database schema
```

**Important**: Project 001 contains a working implementation. For implementation details, see `projects/001-plymouth-research-restaurant-menu-analytics/CLAUDE.md`.

## ArcKit Slash Commands

This repository includes **35 slash commands** for enterprise architecture governance. All commands follow the pattern `/arckit.<command-name>`.

**Core Workflow Commands** (most commonly used):
1. `/arckit.principles` - Define architecture principles (API-first, cloud-native, etc.)
2. `/arckit.stakeholders` - Analyze stakeholders, drivers, and measurable outcomes
3. `/arckit.requirements` - Generate comprehensive business and technical requirements
4. `/arckit.data-model` - Create data models with GDPR compliance
5. `/arckit.research` - Research technology options (build vs buy analysis)
6. `/arckit.diagram` - Generate Mermaid architecture diagrams
7. `/arckit.backlog` - Convert requirements to prioritized user stories

**Governance & Compliance**:
- `/arckit.dpia` - Data Protection Impact Assessment (UK GDPR)
- `/arckit.tcop` - Technology Code of Practice (UK Government)
- `/arckit.secure` - Secure by Design assessment
- `/arckit.ai-playbook` - UK Government AI Playbook compliance
- `/arckit.atrs` - Algorithmic Transparency Recording Standard

**Strategic Planning**:
- `/arckit.wardley` - Wardley mapping for build vs buy decisions
- `/arckit.roadmap` - Multi-year capability roadmap
- `/arckit.plan` - Project plan with timeline and gates
- `/arckit.sobc` - Strategic Outline Business Case (Green Book 5-case model)

**Procurement & Vendor Management**:
- `/arckit.gcloud-search` - Search UK G-Cloud marketplace
- `/arckit.sow` - Statement of Work / RFP documents
- `/arckit.dos` - Digital Outcomes and Specialists procurement
- `/arckit.evaluate` - Vendor evaluation and scoring

**Design & Documentation**:
- `/arckit.adr` - Architectural Decision Records
- `/arckit.hld-review` - High-Level Design review
- `/arckit.dld-review` - Detailed Design review

**Analysis & Quality**:
- `/arckit.analyze` - Comprehensive governance quality analysis
- `/arckit.traceability` - Requirements-to-design-to-tests traceability matrix
- `/arckit.principles-compliance` - Assess compliance with architecture principles

## How ArcKit Commands Work

**Command Execution Pattern**:
1. User runs `/arckit.requirements Generate requirements for restaurant scraping`
2. Command reads the corresponding template from `.arckit/templates/requirements-template.md`
3. Command generates a structured document following UK Government/enterprise best practices
4. Output is saved to `projects/<project-name>/docs/<document-type>/<filename>.md`

**Key Behaviors**:
- Commands create the `projects/` directory structure on first use
- All commands use templates from `.arckit/templates/`
- Commands often read `.arckit/scripts/bash/common.sh` for shared utilities
- Output is always markdown with front matter metadata

## Project Context: Plymouth Research

**Business Requirements**:
- Scrape 150+ restaurant websites in Plymouth, UK
- Extract menu items, prices, descriptions, dietary tags (vegan, gluten-free)
- Normalize data (handle duplicate dishes, price formats)
- Build interactive dashboard for search and comparison
- Weekly automated refresh of menu data

**Legal & Ethical Constraints**:
- Must respect `robots.txt` and website Terms of Service
- Rate limiting: max 1 request per 5 seconds per domain
- GDPR compliance (UK): only public business data, no PII
- Copyright considerations: transformative use (analytics, not republication)

**Technical Architecture (Implemented)**:
- **Scraping**: Python (BeautifulSoup, Scrapy, Selenium for dynamic content)
- **Storage**: SQLite with full-text search indexes
- **Dashboard**: Streamlit (interactive web app)
- **ETL**: Custom Python pipeline for data normalization
- **Hygiene Ratings**: FSA Food Hygiene Rating Scheme integration via XML
- **Hosting**: Local development (production deployment TBD)

**Key NFRs**:
- Dashboard page load < 2 seconds
- Search query response < 500ms
- 10,000+ menu items, 150+ restaurants
- 99% uptime for dashboard
- 12 months data retention for trend analysis

## Common Workflows

**Starting a New Architecture Project**:
```bash
# Option 1: Use helper script
.arckit/scripts/bash/create-project.sh

# Option 2: Use slash commands directly
/arckit.principles Define web scraping ethics, data quality, performance
/arckit.stakeholders Identify consumers, restaurants, researchers
/arckit.requirements Document scraping, ETL, dashboard, API requirements
```

**Generating Documentation**:
```bash
# Generate a DPIA for web scraping
/arckit.dpia Assess GDPR risks for scraping restaurant menus

# Create Wardley map for build vs buy decision
/arckit.wardley Compare Scrapy vs BeautifulSoup, Streamlit vs Dash

# Generate architecture diagrams
/arckit.diagram Create data flow diagram for ETL pipeline
```

**Reviewing Existing Projects**:
```bash
# List all architecture projects
.arckit/scripts/bash/list-projects.sh

# Analyze governance quality
/arckit.analyze Review completeness of requirements and compliance docs
```

## Environment Variables

The repository includes `.envrc` (direnv) support:
- `CODEX_HOME="$PWD/.codex"` - Sets Codex CLI to use project-specific prompts

## File Naming Conventions

ArcKit follows strict naming patterns for generated documents:

**Document IDs**: `ARCKIT-<TYPE>-<YYYYMMDD>-<SEQ>-<PROJECT>`
- Example: `ARCKIT-REQ-20251115-001-PLYMOUTH-RESEARCH.md`

**Project Names**: Slugified, uppercase with hyphens
- Example: `PLYMOUTH-RESEARCH` (from "Plymouth Research")

**Document Types**: Abbreviations used in filenames
- `REQ` = Requirements
- `ADR` = Architectural Decision Record
- `DPIA` = Data Protection Impact Assessment
- `HLD` = High-Level Design
- `DLD` = Detailed Design

## Templates

All 37 templates in `.arckit/templates/` follow a common structure:

```markdown
---
documentId: <auto-generated>
version: 1.0
status: Draft
---

# Document Title

[Template content with placeholders for project-specific details]
```

**Most Important Templates**:
- `requirements-template.md` - Business and technical requirements
- `architecture-principles-template.md` - Organizational principles
- `data-model-template.md` - Database schema with GDPR annotations
- `dpia-template.md` - Data Protection Impact Assessment
- `adr-template.md` - Architectural Decision Records

## Git Workflow

The repository uses a simple git workflow:
- **Main branch**: `main`
- **Latest commit**: `cf10628 feat: integrate FSA Food Hygiene Rating Scheme data`

When making commits:
- Follow conventional commit format: `type: description`
- Common types: `feat`, `docs`, `chore`, `fix`

**Recent Updates**:
- FSA Food Hygiene Rating Scheme integration (2025-11-18)
- Dashboard with 7 tabs including hygiene ratings
- 98 restaurants, 2,625 menu items, 49 hygiene ratings

## ArcKit Version

- **Version**: v0.9.1
- **Commands**: 35
- **Templates**: 37
- **Bash Scripts**: 5

## When Working With This Repository

**DO**:
- Use `/arckit.*` commands to generate architecture documents
- Follow UK Government and enterprise architecture best practices
- Respect the project context (Plymouth Research, restaurant scraping)
- Generate documents in `projects/<project-name>/docs/` structure
- Use templates from `.arckit/templates/` as reference
- For project 001 implementation work, see `projects/001-plymouth-research-restaurant-menu-analytics/CLAUDE.md`

**DON'T**:
- Don't modify `.arckit/templates/` without understanding ArcKit versioning
- Don't ignore legal/ethical constraints (robots.txt, GDPR, copyright)
- Don't commit database files or large data files (use .gitignore)
- Don't skip FSA attribution when displaying hygiene ratings

## Key Principles for This Project

From the project context, these architecture principles should guide all decisions:

1. **Web Scraping Ethics**: Respect robots.txt, rate limits, and Terms of Service
2. **Data Quality**: 95%+ accuracy in menu categorization and normalization
3. **Performance**: Sub-500ms search queries, <2s dashboard load times
4. **Privacy**: Only public business data, no PII, GDPR compliant
5. **Transparency**: Clear attribution to original restaurant sources
6. **Scalability**: Support 150+ restaurants, 10,000+ menu items, room for growth
