# Source index

_Last refreshed: 2026-05-12_

This index summarizes the evidence base for the LiteLLM Claude Desktop and computer-use experiment guide. The machine-readable list is in [sources.json](sources.json) with 26 sources. Raw CDP pages, HN JSON, GitHub API results, and socli artifacts live under `tmp/research-web-critical/litellm-claude-computer-use/` and are intentionally not committed.

## Source quality legend

- **official** — product owner documentation, official repository, official announcement, or official API docs.
- **practitioner** — independent technical/security writeup or field report.
- **community** — HN, GitHub issue, social archive, or repository ecosystem signal.
- **vendor** — product/provider page that is not the primary standard/API owner.

Google SERP snippets were used only for discovery. Durable claims here are grounded in extracted pages, GitHub API responses, HN item payloads, local setup inspection, and source-linked content.

## Highest-priority sources

| Source | Quality | Why it matters |
|---|---|---|
| [LiteLLM Claude Desktop (Cowork) Integration](https://docs.litellm.ai/docs/tutorials/claude_desktop_cowork) | official | Directly documents routing Claude Desktop requests through LiteLLM Proxy, using a Gateway URL and LiteLLM virtual key, then verifying usage attribution. |
| [LiteLLM Claude Code Quickstart](https://docs.litellm.ai/docs/tutorials/claude_responses_api) | official | Confirms the supported Claude Code proxy pattern using `ANTHROPIC_BASE_URL` and `ANTHROPIC_AUTH_TOKEN`; this is the baseline validation gate. |
| [LiteLLM non-Anthropic model tutorial](https://docs.litellm.ai/docs/tutorials/claude_non_anthropic_models) | official | States that LiteLLM translates supported non-Anthropic provider formats while maintaining Anthropic Messages API shape for Claude Code. This supports text compatibility but not necessarily computer-use beta tools. |
| [Anthropic Computer Use Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool) | official | Defines the beta headers, compatible model/tool versions, required sandbox, agent loop, tool execution responsibility, and security precautions. |
| [Anthropic Claude Quickstarts](https://github.com/anthropics/anthropic-quickstarts) | official | Confirms the official Computer Use Demo as an environment and tools that Claude can use to control a desktop computer, including support for the latest `computer_use_20251124` version. |

## Claude Desktop and LiteLLM sources

| Source | Quality | Key data used |
|---|---|---|
| [LiteLLM Claude Desktop (Cowork)](https://docs.litellm.ai/docs/tutorials/claude_desktop_cowork) | official | Developer Mode, Configure Third-Party Inference, Gateway URL, LiteLLM virtual key, restart, verify Dashboard Usage. |
| [Microsoft Foundry: Configure Claude Desktop](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/how-to/configure-claude-desktop) | official | Independent confirmation that Claude Desktop has a third-party inference configuration surface and can be managed per-device or by configuration. |
| [LiteLLM Claude Code Quickstart](https://docs.litellm.ai/docs/tutorials/claude_responses_api) | official | Unified endpoint and Anthropic pass-through endpoint patterns, plus use of virtual key or master key. |
| [LiteLLM non-Anthropic model tutorial](https://docs.litellm.ai/docs/tutorials/claude_non_anthropic_models) | official | Translation claim for non-Anthropic models through Anthropic Messages API shape in Claude Code. |
| Local `~/.claude/settings.json` and `litellm-proxy` repo | local setup | Showed the current user setup already uses `http://localhost:11435`, direct `chatgpt/` route names, API-key helper indirection, Responses-mode model info, and a patch for Claude Code system-message translation. Local paths are not external source records in `sources.json`. |

## Anthropic computer-use sources

| Source | Quality | Key data used |
|---|---|---|
| [Anthropic Computer Use Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool) | official | Beta headers `computer-use-2025-11-24` and `computer-use-2025-01-24`; `computer_20251124`, `text_editor_20250728`, `bash_20250124`; sandbox/VM/container and agent-loop requirements. |
| [Anthropic computer-use demo](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo) | official | Reference implementation for a containerized desktop, tool implementations, and web UI. |
| [Claude Quickstarts repository](https://github.com/anthropics/anthropic-quickstarts) | official | Confirms the Computer Use Demo as a maintained quickstart and notes support for latest tool version with zoom actions. |
| [ZombAIs security writeup](https://embracethered.com/blog/posts/2024/claude-computer-use-c2-the-zombais/) | practitioner | Demonstrates why internet-facing computer use must be isolated: prompt injection can cause downloads, permission changes, and command execution in a vulnerable setup. |
| [Simon Willison: Computer Use](https://simonwillison.net/2024/Oct/22/computer-use/) | practitioner | Practitioner framing and launch-era implications around Claude computer use. |
| [HN item 41914989](https://hn.algolia.com/api/v1/items/41914989) | community | Large launch discussion used as social/practitioner signal, not primary proof. |
| [HN item 41958550](https://hn.algolia.com/api/v1/items/41958550) | community | HN discussion of the prompt-injection-to-C2 writeup. |

## Codex Desktop sources

| Source | Quality | Key data used |
|---|---|---|
| [OpenAI Codex app computer use](https://developers.openai.com/codex/app/computer-use) | official | Official Codex documentation surface for product-level computer use. |
| [OpenAI Codex app features](https://developers.openai.com/codex/app/features) | official | Official app feature context, including in-app browser and extension/app workflow surfaces. |
| [OpenAI Codex for almost everything](https://openai.com/index/codex-for-almost-everything/) | official | Product announcement context for Codex Desktop capabilities. |
| [openai/codex#18258](https://github.com/openai/codex/issues/18258) | community | Strong failure-mode evidence: `Computer Use plugin unavailable`, region gating, helper registration/cache paths, partial backend/UI mismatch. |
| [openai/codex#18507](https://github.com/openai/codex/issues/18507) | community | macOS permission / Apple event failure signal. |
| [openai/codex#18896](https://github.com/openai/codex/issues/18896) | community | Approval/elicitation failure signal. |
| [openai/codex#19305](https://github.com/openai/codex/issues/19305) | community | Platform gap signal for full Windows support. |
| [HN item 47895892](https://hn.algolia.com/api/v1/items/47895892) | community | Practitioner reverse-engineering/social signal for Codex background computer use. |

## Open-source implementation sources

| Source | Quality | Key data used |
|---|---|---|
| [trycua/cua](https://github.com/trycua/cua) | official/community | Background macOS control, sandboxes across OSes, benchmark tooling, `cuabot`, `cua-sandbox`, and Lume virtualization. |
| [e2b-dev/open-computer-use](https://github.com/e2b-dev/open-computer-use) | official/community | Secure cloud Linux desktop sandbox using keyboard/mouse/shell, live stream, pause/prompt, and multi-provider LLM support. |
| [iFurySt/open-codex-computer-use](https://github.com/iFurySt/open-codex-computer-use) | community | MCP-wrapped Computer Use service for macOS/Linux/Windows; Codex, Claude, Gemini install commands; macOS Accessibility and Screen Recording requirement. |
| [OpenClaw issue 67776](https://github.com/openclaw/openclaw/issues/67776) | community | Architecture discussion: coordinate screenshot/click loops can steal cursor/focus; Accessibility API targeting and permission-aware brokerage are important Mac design patterns. |
| [lahfir/agent-desktop](https://github.com/lahfir/agent-desktop) | community | Native desktop automation CLI for AI agents discovered through deeper SERP/GitHub pass. |
| [alekseyrozh/openclawdex](https://github.com/alekseyrozh/openclawdex) | community | Adjacent orchestration UI signal for Claude Code and Codex. |

## Coverage gaps

- The research did not prove whether Claude Desktop third-party inference accepts local plain HTTP `localhost:11435` in this exact environment.
- No captured source proved Anthropic `computer_*` beta tools work through LiteLLM's Anthropic gateway when the backend is `chatgpt/` Responses.
- The official computer-use demo source was captured, but the current repo has not run the control demo live.
- Codex Desktop docs were extracted, but some OpenAI docs pages included heavy site chrome; GitHub issues and product announcement sources carry much of the concrete failure-mode detail.
- Open-source computer-use stacks were assessed from README/issues/source pages, not installed or audited locally.
- Local settings and proxy repository evidence were inspected but not committed into this repo because they may contain sensitive or machine-local configuration.

## Refresh priority

Before running real experiments, refresh these first:

1. LiteLLM Claude Desktop/Cowork integration docs.
2. Anthropic computer-use tool docs and quickstart repository.
3. Local `litellm-proxy` README/config and current `~/.claude/settings.json` redacted state.
4. OpenAI Codex app computer-use docs and `openai/codex` issue state.
5. `trycua/cua`, `e2b-dev/open-computer-use`, and `open-codex-computer-use` README/issue status.
