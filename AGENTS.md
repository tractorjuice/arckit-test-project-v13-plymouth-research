# Repository Guidelines

## Project Structure & Module Organization
Top-level docs (`README.md`, `PROJECT-README.md`, `CLAUDE.md`) describe the Plymouth Research initiative. Templates for governance outputs live in `.arckit/templates`, while helper Bash utilities are under `.arckit/scripts/bash`. AI assistant slash-command specs reside in `.claude/commands` (Claude) and `.codex/prompts` (Codex); keep their filenames aligned because tooling derives command IDs from the stem. Git LFS is enforced through `.git/hooks/pre-push`. No application code is checked in yet, so new work should land inside a `projects/<id>-<slug>/` tree created by the helper script.

## Build, Test, and Development Commands
- `direnv allow` — loads `.envrc`, ensuring `CODEX_HOME=.codex` so CLI prompts resolve correctly.
- `bash ./.arckit/scripts/bash/check-prerequisites.sh` — confirms ArcKit memory files exist before generating artifacts.
- `bash ./.arckit/scripts/bash/create-project.sh --name "Menu Intelligence"` — scaffolds a numbered project directory with the recommended command flow.
- `rg "menu" projects/ -g'*.md'` — fastest way to update research artifacts.

## Coding Style & Naming Conventions
Markdown documents should keep headings sentence-case, wrap near 100 characters, and indent ordered lists with two spaces when outlining ArcKit command sequences. For slash-command files, reuse the `arckit.<topic>.md` stem and keep metadata blocks at the top. Bash utilities already enable `set -euo pipefail`; keep using snake_case helpers from `common.sh` and the shared log functions for consistent CLI output.

## Testing Guidelines
There is no compiled build, so validation focuses on documentation accuracy and script hygiene. Run `bash -n <script>` plus `shellcheck <script>` before proposing changes to `.arckit/scripts/bash`. For Markdown deliverables, preview in your editor and ensure referenced slash commands exist in both `.claude/commands` and `.codex/prompts`. After scaffolding new work, rerun `./.arckit/scripts/bash/list-projects.sh` to confirm numbering stays sequential.

## Commit & Pull Request Guidelines
Existing history uses Conventional Commit prefixes (example: `chore: initialize Plymouth Research test project v13`); continue with `feat:`, `docs:`, or `chore:` plus a concise summary. Every pull request should link to the relevant ArcKit decision record, describe which directories were touched, and include before/after screenshots if you updated templates. Verify Git LFS is installed locally so pushes pass the enforced `pre-push` hook.

## Security & Configuration Tips
Never commit secrets—`.envrc` only sets `CODEX_HOME`, so keep other credentials in your shell runtime. Respect site-specific policies embedded in the ArcKit documents (robots.txt compliance, rate limiting) when capturing new research data. When running helper scripts off-box, review prompts so project IDs or stakeholder names do not leak outside approved channels.
