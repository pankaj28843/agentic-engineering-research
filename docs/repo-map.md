# Repository Map

This repository is an agent-readable research base for agentic engineering.

## Top-level layout

| Path | Purpose |
|---|---|
| `AGENTS.md` | Short operating map loaded by coding agents. Keep it compact. |
| `.agents/skills/` | Repo-local repeatable workflows for deep theme research and source audits. |
| `docs/` | Methodology, glossary, and repository conventions. |
| `research/<NN-theme-slug>/` | One durable research packet per theme. |
| `scripts/` | Validation and maintenance utilities run through `uv`. |
| `tmp/` | Gitignored scratch space for CDP, Google SERPs, rendered page extracts, HN/socli artifacts, and experiments. |

## Theme packet layout

Each theme should contain:

- `README.md` — entry point and navigation.
- `briefing.md` — evidence-weighted synthesis.
- `source-index.md` — human-readable source catalog.
- `research-log.md` — queries, extraction notes, tool outputs, limitations.
- `sources.json` — machine-readable source catalog validated by `scripts/validate_research.py`.

Optional files:

- `open-questions.md` — follow-up research agenda.
- `notes/` — smaller focused memos when a theme grows.
- `diagrams/` — Mermaid or ASCII diagrams checked into markdown.

## Durable vs scratch content

Commit synthesis, source lists, query sets, and audit trails. Do not commit bulk rendered page dumps or browser artifacts; keep those under `tmp/` and reference the rerunnable workflow in `research-log.md`.
