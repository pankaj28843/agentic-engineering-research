# Source Index

This index ranks evidence by how directly it supports claims in the guide. Search snippets are not used as evidence. Raw rendered pages, transcripts, comments, and source snapshots remain in `tmp/` or a local video-capsule directory outside this repository.

## Primary OpenAI Evidence

- [OpenAI harness engineering blog](https://openai.com/index/harness-engineering/) - primary official narrative. CDP extraction captured the article into `tmp/research-web-critical/openai-harness-engineering/openai-blog/pages/001-openai-com-index-harness-engineering/page.md`. This source supports the internal experiment claims: zero manually written code, roughly one million lines, about 1,500 PRs, per-worktree app instances, CDP wiring, local observability, repository knowledge as system of record, architecture invariants, custom lints, agent review, autonomy, cleanup, and unknowns.
- Local OpenAI diagrams under `assets/openai/` - primary visual evidence from the same blog. The visual reasoning pass supports durable diagram interpretations in [assets/README.md](assets/README.md) and the guide chapters.

## Public OpenAI Source Code

- [openai/symphony](https://github.com/openai/symphony) - public OpenAI source evidence for a scheduler/runner pattern. The README says Symphony turns project work into isolated, autonomous implementation runs and works best in harness-engineered codebases.
- [Symphony SPEC.md](https://github.com/openai/symphony/blob/main/SPEC.md) - source-backed specification for polling an issue tracker, creating per-issue workspaces, loading repo-owned `WORKFLOW.md`, running coding agents, tracking retries, and exposing logs/status.
- [Symphony Elixir](https://github.com/openai/symphony/tree/main/elixir) - source-backed implementation details. Inspected files show Codex app-server sessions, Linear GraphQL tooling, workspace hooks, default sandbox policies, retry/blocked state, a Phoenix dashboard/API, logging guidance, and token accounting.

## Video Capsules

Transcript evidence is stronger than comment evidence. All video capsules were captured with `uvx yt-dlp@latest`; warnings about skipped remote JS challenge solving are recorded in each `warnings.txt`.

| Video | Capsule | Transcript words | Comments | Evidence quality |
|---|---:|---:|---:|---|
| [Extreme Harness Engineering](https://www.youtube.com/watch?v=CeOXx-XTYek) | `CeOXx-XTYek` | 15372 | 53 | Strong transcript, weak comments |
| [Harness Engineering: How to Build Software When Humans Steer, Agents Execute](https://www.youtube.com/watch?v=am_oeAoUhew) | `am_oeAoUhew` | 7986 | 118 | Strong transcript, weak comments |
| [Build Hour: API & Codex](https://www.youtube.com/watch?v=rhsSqr0jdFw) | `rhsSqr0jdFw` | 11784 | 74 | Strong transcript, weak comments |
| [What OpenAI, Stripe & ElevenLabs Devs Do Differently Now](https://www.youtube.com/watch?v=OfsWo6zyt-4) | `OfsWo6zyt-4` | 13927 | 0 | Strong transcript |
| [Harness Engineering: A Disciplina Que Vai Substituir Engenharia de Software](https://www.youtube.com/watch?v=Vau831dxNZ0) | `Vau831dxNZ0` | 0 | 38 | Metadata/comment capsule only; no transcript |
| [Code Is Free: Securing Software](https://www.youtube.com/watch?v=U2O14Jd3MBU) | `U2O14Jd3MBU` | 4294 | 0 | Usable security transcript |

## Social Signal

- [Ryan Lopopolo on X](https://x.com/_lopopolo?lang=en) - accessible headed-CDP extraction saved to `tmp/research-web-critical/openai-harness-engineering/x-check/`. It showed public profile text and recent posts about Codex, `/goal`, Multipass, and Rust OSS AGENTS.md practices. This is only social signal. It is not official product evidence and is not used to prove private internal facts.

## Official Capability And Pricing Sources

- [OpenAI Codex pricing](https://developers.openai.com/codex/pricing/) - official docs extract fetched 2026-06-01. Used for the roughly USD 200/month OpenAI practitioner tier, with the important limitation that usage limits can change.
- [OpenAI Codex app features](https://developers.openai.com/codex/app/features/) - official docs extract fetched 2026-06-01. Used for app modes, worktrees, Git tools, skills, automations, integrated terminal, browser, and computer-use claims.
- [OpenAI Worktrees](https://developers.openai.com/codex/app/worktrees/) - official docs extract fetched 2026-06-01. Used for worktree isolation, handoff, cleanup, and `$CODEX_HOME/worktrees`.
- [OpenAI In-app browser](https://developers.openai.com/codex/app/browser/) - official docs extract fetched 2026-06-01. Used for browser-use and visual-comment boundaries.
- [OpenAI AGENTS.md guide](https://developers.openai.com/codex/guides/agents-md/) - official docs extract fetched 2026-06-01. Used for instruction discovery and layering.
- [OpenAI Skills](https://developers.openai.com/codex/skills/) - official docs extract fetched 2026-06-01. Used for progressive-disclosure skill mechanics.
- [OpenAI approvals and security](https://developers.openai.com/codex/agent-approvals-security/) - official docs extract fetched 2026-06-01. Used for sandbox, approval, and network-access guidance.
- [OpenAI computer use API guide](https://developers.openai.com/api/docs/guides/tools-computer-use) - official docs extract fetched 2026-06-01. Used for custom UI harness and isolated browser/VM safety guidance.
- [Claude Code](https://claude.com/product/claude-code) and [Claude Max](https://claude.com/pricing/max) - official Anthropic pages. Used only for high-level comparison around Claude Code surfaces and the USD 200/month Max 20x practitioner tier.
