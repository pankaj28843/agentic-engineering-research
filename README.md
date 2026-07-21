# Agentic Engineering Research

A private, source-backed research repository on **agentic engineering**: using LLM-powered coding agents to do software engineering.

The repository is organized as themed research packets. Each packet combines browser-grounded web research, official docs, practitioner reports, HN/social signals, skeptical synthesis, and a source-linked ELI5 deep-dive guide that should read like a small private book rather than a terse memo.

## Start here

- [AGENTS.md](AGENTS.md) — compact operating instructions for coding agents.
- [docs/repo-map.md](docs/repo-map.md) — repository structure.
- [docs/research-method.md](docs/research-method.md) — repeatable research workflow.
- [docs/glossary.md](docs/glossary.md) — working terminology.
- [research/01-harness-engineering/](research/01-harness-engineering/) — first theme.
- [research/02-hosted-open-weight-coding-llm-apis/](research/02-hosted-open-weight-coding-llm-apis/) — hosted open-weight coding LLM API evaluation.
- [research/03-litellm-claude-desktop-computer-use/](research/03-litellm-claude-desktop-computer-use/) — LiteLLM, Claude Desktop, Anthropic computer use, Codex Desktop, and open-source computer-use experiments.
- [research/07-july-2026-ai-catch-up/](research/07-july-2026-ai-catch-up/) — day-wise AI engineering catch-up for 1-21 July 2026.

## Themes

1. [Harness Engineering for Coding Agent Users](research/01-harness-engineering/) — feedforward guides, feedback sensors, context engineering, long-running agents, security boundaries, and human-on-the-loop control. Start with the [book-length guide](research/01-harness-engineering/guide/00-README.md).
2. [Hosted Open-Weight Coding LLM APIs](research/02-hosted-open-weight-coding-llm-apis/) — buyer's and evaluator's guide for cheaper hosted open-weight coding models versus Opus/GPT baselines.
3. [LiteLLM, Claude Desktop, and Computer Use](research/03-litellm-claude-desktop-computer-use/) — experiment plan for Claude Desktop/Cowork through LiteLLM, Anthropic computer-use loops, Codex Desktop, and open-source computer-use stacks.
4. [Formal Methods for Coding Agents](research/04-formal-methods-coding-agents/) — proof obligations, invariants, formal tools, and verification workflows for agent-written code.
5. [OpenClaw in the Wild](research/05-openclaw-in-the-wild/) — evidence-led analysis of OpenClaw adoption, practice, and failure modes.
6. [OpenAI Harness Engineering](research/06-openai-harness-engineering/) — OpenAI's internal account, public orchestration code, practitioner replication, and limits.
7. [July 2026 AI Engineering Catch-Up](research/07-july-2026-ai-catch-up/) — a 21-day chronological newspaper with original and Hacker News evidence.

## Commands

Validate the repository:

```bash
uv run python scripts/validate_research.py
```

or:

```bash
make validate
```

## Research artifact policy

- Commit durable synthesis, source indices, guide chapters, credited guide assets, query logs, and machine-readable metadata.
- Keep raw rendered pages, clean article snapshots, SERP dumps, screenshots, and CDP artifacts in `tmp/`.
- `tmp/` is gitignored and intentionally repo-root relative so CDP workflows and article-extraction post-processing can write there safely.

## Repo-local skills and scripts

- `.agents/skills/theme-deep-research/SKILL.md` — create or refresh a research theme.
- `.agents/skills/publish-ai-news/SKILL.md` — publish daily, weekly, monthly, or
  explicit-range AI engineering news editions through headed CDP and audited A4
  PDF output.
- `.agents/skills/source-audit/SKILL.md` — audit a theme before commit.
- `.agents/skills/guide-book-publish/SKILL.md` — publish individual or combined guide books with embedded images and optional MOBI handoff staging.
- `scripts/extract_theme_articles.py` — turn captured CDP `html.json` into clean article Markdown under `tmp/`.
- `scripts/build_theme_book.py` — publish one theme, all themes, or one combined guide book as Markdown/EPUB/PDF/MOBI with copied local images.

## CDP daemon rule

Only this daemon lifecycle command is allowed unattended:

```bash
cdp daemon status --json
```

Starting, restarting, stopping, keeping alive, or active-probing the CDP daemon requires explicit human approval because Chrome remote-debugging permission prompts need a human in the loop.
