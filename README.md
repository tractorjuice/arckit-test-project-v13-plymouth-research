# ArcKit Test Project: Plymouth Research – Restaurant Menu Scraping & Analytics

## Overview
This repository demonstrates ArcKit v0.9.1 workflows for Plymouth Research’s restaurant menu scraping and analytics initiative. Use it to draft architecture principles, run governance commands, and capture research artifacts before implementation work begins. For the full business and technical brief, see `PROJECT-README.md`.

## Repository Layout
- `.arckit/templates/` – 37 Markdown templates used by ArcKit commands (ADR, backlog, DPIA, Wardley map, etc.).
- `.arckit/scripts/bash/` – helper scripts (`check-prerequisites.sh`, `create-project.sh`, `list-projects.sh`, etc.) all sourcing `common.sh`.
- `.claude/commands/`, `.codex/prompts/`, `.gemini/commands/` – slash-command definitions for Claude Code, Codex CLI, and Gemini CLI respectively; stems stay aligned (`arckit.<topic>.md`).
- `PROJECT-README.md` – deep dive on context, architecture, and success metrics.
- `AGENTS.md` – contributor guide that explains structure, style, and testing expectations.
- `projects/` – created automatically when you scaffold work with the helper script; holds numbered project directories.

## Workflow Essentials
1. Run `direnv allow` (or manually export `CODEX_HOME=.codex`) so the Codex CLI picks up repo prompts.
2. Execute `bash ./.arckit/scripts/bash/check-prerequisites.sh` to ensure architecture principles exist before generating documents.
3. Create delivery space via `bash ./.arckit/scripts/bash/create-project.sh --name "Menu Intelligence"`; it provisions `projects/<id>-<slug>/README.md` with the recommended command order.
4. Use your AI assistant to trigger slash commands such as `/arckit.principles`, `/arckit.stakeholders`, and `/arckit.requirements`, saving outputs inside the new project folder.

## ArcKit Slash Commands
ArcKit exposes 35 commands for architecture governance. Core ones for this project include:
- `/arckit.principles` – define web scraping ethics, data quality, and performance rules.
- `/arckit.stakeholders` – capture consumer, restaurant, researcher, and platform-owner outcomes.
- `/arckit.requirements` – document scraping, ETL, dashboard, and API requirements.
- `/arckit.data-model` – design GDPR-aware schemas for Restaurants, MenuItems, Categories.
- `/arckit.research` – compare build/buy options (Scrapy vs BeautifulSoup, Streamlit vs Dash).
- `/arckit.wardley` – map strategic components to guide sourcing decisions.
- `/arckit.diagram` – output Mermaid diagrams of the data ingestion and analytics flow.
- `/arckit.backlog` – generate the prioritized delivery backlog.
Run `/help` inside your AI interface to see the full catalog.

## Development Tips & Resources
- Follow `AGENTS.md` for coding style, testing steps (`bash -n`, `shellcheck`), and Conventional Commit conventions (`docs: update readme`).
- Use `rg "<term>" projects/ -g'*.md'` to update research artifacts quickly.
- Git LFS is enforced via `.git/hooks/pre-push`; install `git-lfs` locally before contributing.
- Keep sensitive details outside the repo—`.envrc` only exports `CODEX_HOME`.

## ArcKit Assets
- **Version**: v0.9.1
- **Commands**: 35
- **Templates**: 37
- **Bash Scripts**: 5 (with latest path fixes)

## License
This is a test repository for ArcKit demonstration purposes.
