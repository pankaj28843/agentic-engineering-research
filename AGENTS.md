# Agent Instructions

This repository organizes thematic research on agentic engineering: using LLM-powered coding agents to do software engineering. Treat it as a durable, source-backed knowledge base, not a scratch transcript.

## Commands

- Validate repository structure and research metadata:

  ```bash
  uv run python scripts/validate_research.py
  ```

- Equivalent make target:

  ```bash
  make validate
  ```

## Repository structure

- `research/<NN-theme-slug>/` — durable themed research packets.
- `docs/` — repository operating model, glossary, and methodology.
- `.agents/skills/` — repo-local skills for repeating the research workflow.
- `scripts/` — lightweight validation/maintenance scripts.
- `tmp/` — gitignored browser/CDP/docsearch/socli scratch artifacts. Use this for bulky extraction output; do not commit rendered page dumps.

## Research rules

- Ground claims in extracted source content, not search snippets. Google SERP snippets are leads only.
- Use `cdp --browser-mode headed` for every live web read, including Hacker News; do not use direct HTTP or a headless fallback.
- Prefer primary/official sources, then practitioner reports, then community/social signals. Label vendor claims and skeptical counter-evidence separately.
- Keep `AGENTS.md` short. Put durable knowledge in `docs/` and theme folders; put bulky raw artifacts and article snapshots in `tmp/`.
- Each theme must be useful as personalized learning material: include a chapter-wise, source-linked, ELI5 deep-dive guide under `guide/`, not only a short briefing.
- When adding a theme, include `README.md`, `briefing.md`, `source-index.md`, `research-log.md`, `sources.json`, and `guide/00-README.md` plus chapter files.
- Use `scripts/extract_theme_articles.py` to post-process captured CDP `html.json` files into clean article Markdown under `tmp/` before writing long-form guide chapters.
- When a dated issue feeds audio production, materialize the `publish-ai-news` podcast handoff after final validation; downstream repositories own synthesis, TTS, audio, RSS, and human review.

## CDP daemon lifecycle guard

- Non-interactive agents may run exactly this daemon lifecycle check:

  ```bash
  cdp daemon status --json
  ```

- Do **not** run `cdp daemon start` without explicit human approval in the current turn.
- Do **not** run `cdp daemon restart` without explicit human approval in the current turn.
- Do **not** run `cdp daemon stop`, `cdp daemon keepalive`, or `cdp doctor --active-browser-probe` without explicit human approval in the current turn.
- These commands can require a Chrome remote-debugging permission prompt and need a human in the loop.
- If `cdp daemon status --json` is green/running, continue with normal CDP workflows. If it is not green/running, stop and ask the user to start or restart the daemon; do not try to repair it automatically.

## Git and publishing

- Keep `tmp/` out of git.
- Run `uv run python scripts/validate_research.py` before committing.
- Commit small, coherent changes with messages that state which theme or skill changed.
