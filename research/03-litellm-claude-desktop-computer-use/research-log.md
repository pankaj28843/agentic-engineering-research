# Research log: LiteLLM Claude Desktop and computer use

_Last updated: 2026-05-12_

## Research question

How should the user's existing LiteLLM ChatGPT-subscription proxy be tested with Claude Desktop/Cowork, Anthropic computer use, Codex Desktop computer use, and open-source computer-use stacks?

The research focused on:

- the current local LiteLLM and Claude Code setup;
- whether Claude Desktop can route through LiteLLM;
- what Anthropic computer use actually requires;
- whether the ChatGPT-backed LiteLLM route is likely to support `computer_*` tools;
- Codex Desktop computer-use capabilities and failure modes;
- open-source alternatives for isolated or Mac-native computer use.

## Workflow used

This theme followed a browser-grounded and skeptical workflow:

1. Inspected local setup in redacted form:
   - `~/.claude/settings.json`
   - `~/.pi/agent/settings.json`
   - local LiteLLM proxy README and agent instructions
   - local LiteLLM proxy configuration
   - local proxy patch script
2. Confirmed the local proxy had been live during research with a liveness check returning success.
3. Created scratch workspace:

   ```text
   tmp/research-web-critical/litellm-claude-computer-use/
   ```

4. Ran browser-grounded Google/CDP SERP batches for Claude Desktop, LiteLLM, Anthropic computer use, Codex Desktop, and open-source computer-use queries. Google SERP collection used low parallelism to reduce blocking risk.
5. Extracted selected official docs, GitHub pages, OpenAI docs, practitioner posts, and open-source repositories into CDP `page.md` artifacts.
6. Queried HN Algolia for exact and expanded terms; exact LiteLLM/Desktop/computer-use combinations were sparse, while broader Claude/Codex/computer-use threads had useful social signal.
7. Queried local `socli` archives; exact-topic social hits were sparse.
8. Used `gh` for GitHub repository, issue, and code searches. The `gh --help` surface was checked before relying on flags.
9. Persisted an initial concise plan to `~/deep-research/litellm-claude-computer-use/`, then created this current-repo durable theme after the user clarified that the research should be committed here.

## Scratch artifacts

Key artifacts under `tmp/research-web-critical/litellm-claude-computer-use/`:

- `queries.txt`
- `candidates.json`
- `candidates.tsv`
- `serp-summary.json`
- `visit-urls.txt`
- `extract-summary.json`
- `pages/` initial CDP captures
- `queries-openai.txt`
- `candidates-openai.json`
- `serp-openai-summary.json`
- `visit-openai-urls.txt`
- `extract-openai-summary.json`
- `openai-pages/` Codex/OpenAI captures
- `queries-deep2.txt`
- `candidates-deep2.json`
- `deep2-serp/` deeper SERP captures
- `extract-deep2-summary.json`
- `deep2-pages/` deeper extraction captures
- `hn-stories.tsv`
- `hn-critical-comments.tsv`
- `hn-expanded-stories.tsv`
- `hn-item-41914989.json`
- `hn-item-41958550.json`
- `hn-item-41944637.json`
- `hn-item-47936312.json`
- `hn-item-47895892.json`
- `hn-item-47982708.json`
- `hn-item-47823501.json`
- `hn-item-42804933.json`
- `socli-search.json`
- `socli-report.md`
- `github/` GitHub search, issue, and README outputs

`tmp/` is intentionally gitignored and should not be committed.

## Local setup findings

The local setup already behaves like a Claude Code and Codex proxy lab:

- `~/.claude/settings.json` points Claude Code at `http://localhost:11435` and uses direct `chatgpt/` model names through LiteLLM.
- The Claude Code secret path uses an `apiKeyHelper`, so the proxy secret was not embedded in the research output.
- The local `litellm-proxy` repository documents a Docker daemon on `localhost:11435`, ChatGPT OAuth token persistence under `./data/chatgpt/`, Responses-mode model metadata, Codex Responses config, and Claude Code setup.
- `litellm_config.yaml` advertises `chatgpt/gpt-5.5`, `chatgpt/gpt-5.4`, `chatgpt/gpt-5.4-mini`, `chatgpt/gpt-5.3-codex`, `chatgpt/gpt-5.3-codex-spark`, and `chatgpt/gpt-5.2`, with `mode: responses` and explicit token limits.
- `patch_chatgpt_claude.py` normalizes Claude Code system text blocks so the ChatGPT subscription Responses backend receives string instructions rather than list-shaped system content.

Sensitive local key values were not written into this theme.

## SERP and extraction batches

### Initial batch

The first CDP batch covered:

- Claude Desktop MCP/custom API/base URL queries;
- Claude Code LiteLLM `ANTHROPIC_BASE_URL` queries;
- LiteLLM Anthropic proxy and computer-use tool queries;
- Claude computer-use API beta queries;
- OpenAI Codex Desktop computer-use queries;
- GitHub-targeted queries for Claude Desktop/LiteLLM/computer-use demos.

Key durable sources from this pass include LiteLLM Claude Desktop/Cowork docs, LiteLLM Claude Code docs, Anthropic computer-use docs, and Anthropic quickstart pages.

### OpenAI/Codex batch

A focused OpenAI batch extracted Codex docs and product pages around:

- Codex app computer use;
- Codex app features;
- Codex use cases and in-app browser / Chrome extension docs;
- OpenAI announcement context.

Some Codex documentation pages included heavy site chrome in extraction, so product claims were cross-checked against GitHub issues and official announcement pages.

### Deeper second batch

The deeper batch targeted:

- Claude Desktop third-party inference with LiteLLM virtual keys;
- Claude Cowork limitations;
- Anthropic computer-use custom base URL and LiteLLM compatibility;
- prompt-injection/security failure reports;
- Codex Desktop permissions and plugin failures;
- open-source computer-use implementations.

Important extracted pages included the ZombAIs security report, trycua/cua, e2b open-computer-use, open-codex-computer-use-related pages, OpenClaw issue pages, and Codex app coverage.

## HN research

Exact HN searches for the full LiteLLM plus Claude Desktop plus computer-use stack produced little high-signal discussion. Broader computer-use searches produced useful context:

| HN item | Signal | Why it matters |
|---|---:|---|
| [41914989](https://hn.algolia.com/api/v1/items/41914989) | 1454 points / 735 comments | Major launch discussion for Claude computer use and Claude model updates. |
| [41958550](https://hn.algolia.com/api/v1/items/41958550) | 166 points | Discussion of the ZombAIs prompt-injection-to-C2 report. |
| [41944637](https://hn.algolia.com/api/v1/items/41944637) | 82 points | Notes on Anthropic's computer-use ability. |
| [47936312](https://hn.algolia.com/api/v1/items/47936312) | 192 points | trycua/cua background macOS computer-use signal. |
| [47895892](https://hn.algolia.com/api/v1/items/47895892) | 10 points | Codex background computer-use reverse-engineering signal. |
| [47982708](https://hn.algolia.com/api/v1/items/47982708) | 99 points | Native desktop automation CLI signal. |
| [47823501](https://hn.algolia.com/api/v1/items/47823501) | 7 points | OpenClawdex orchestration signal. |
| [42804933](https://hn.algolia.com/api/v1/items/42804933) | 9 points | E2B open-computer-use signal. |

HN was used as practitioner/social signal and link discovery, not as proof of API compatibility.

## GitHub research

GitHub searches covered repositories, issues, and code examples for Claude Desktop third-party inference, LiteLLM compatibility, Anthropic computer-use demo adaptations, Codex Desktop computer use, OpenClaw, and open-source computer-use stacks.

Important repositories at capture:

| Repo | Stars at capture | Role |
|---|---:|---|
| [openai/codex](https://github.com/openai/codex) | 82,040 | Codex CLI/app ecosystem and issue tracker for product-level computer-use failures. |
| [BerriAI/litellm](https://github.com/BerriAI/litellm) | 46,659 | LiteLLM proxy and Anthropic/OpenAI gateway implementation source. |
| [anthropics/anthropic-quickstarts](https://github.com/anthropics/anthropic-quickstarts) | 16,565 | Official computer-use demo and Claude API quickstarts. |
| [trycua/cua](https://github.com/trycua/cua) | 16,093 | Mac-native/background computer-use stack, sandbox SDK, benchmark tooling. |
| [e2b-dev/open-computer-use](https://github.com/e2b-dev/open-computer-use) | 2,004 | Isolated Linux desktop sandbox controlled by multiple LLM providers. |
| [iFurySt/open-codex-computer-use](https://github.com/iFurySt/open-codex-computer-use) | 723 | MCP-wrapped open Computer Use service with Codex/Claude/Gemini integration commands. |
| [coasty-ai/open-computer-use](https://github.com/coasty-ai/open-computer-use) | 569 | Community open computer-use implementation signal. |
| [PallavAg/claude-computer-use-macos](https://github.com/PallavAg/claude-computer-use-macos) | 293 | Claude computer-use on macOS implementation signal. |
| [Yambr/open-computer-use](https://github.com/Yambr/open-computer-use) | 70 | Community implementation signal. |

Key issues:

- [openai/codex#18258](https://github.com/openai/codex/issues/18258) — `Computer Use plugin unavailable`, bundled plugin/helper/cache/region-gate and partial-functionality reports.
- [openai/codex#18507](https://github.com/openai/codex/issues/18507) — macOS permission / Apple event error signal.
- [openai/codex#18896](https://github.com/openai/codex/issues/18896) — approval denied through MCP elicitation signal.
- [openai/codex#19305](https://github.com/openai/codex/issues/19305) — request for full Windows support.
- [openclaw/openclaw#67776](https://github.com/openclaw/openclaw/issues/67776) — Mac desktop-control orchestration discussion, including a warning that coordinate-only screenshot/click loops can hijack cursor/focus and that Accessibility API targeting can be faster and less intrusive.

GitHub API issue encountered and fixed: `gh search issues` rejected JSON field `comments`; the correct field is `commentsCount`.

## Key source-backed findings

### Claude Desktop/Cowork can use LiteLLM as a third-party inference gateway

LiteLLM's docs explicitly say Claude Desktop requests can be routed through LiteLLM Proxy for unified logging, budget controls, and access to any model. The documented setup uses Developer Mode, Configure Third-Party Inference, a Gateway URL, a LiteLLM virtual key, restart, and Dashboard Usage verification ([LiteLLM Claude Desktop integration](https://docs.litellm.ai/docs/tutorials/claude_desktop_cowork)).

### Claude Code is the baseline local validation gate

The current local setup already matches LiteLLM's Claude Code docs conceptually: point Claude Code at a LiteLLM endpoint using `ANTHROPIC_BASE_URL` and `ANTHROPIC_AUTH_TOKEN` or equivalent key helper ([LiteLLM Claude Code quickstart](https://docs.litellm.ai/docs/tutorials/claude_responses_api)). If the existing Claude Code route fails, Desktop experiments should pause.

### Computer use is an API/tool-loop contract

Anthropic computer use requires a beta header, supported model/tool versions, a sandboxed computing environment, tool implementations, and an agent loop. Claude does not directly control the machine; the application receives tool-use requests, executes them, captures screenshots/outputs, and returns tool results ([Anthropic computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)).

### The ChatGPT-backed proxy path is unproven for Anthropic computer-use beta tools

LiteLLM's non-Anthropic model docs support the idea that normal text/tool-ish Claude Code calls can be translated through non-Anthropic backends ([LiteLLM non-Anthropic models](https://docs.litellm.ai/docs/tutorials/claude_non_anthropic_models)). The research did not find evidence that the current `chatgpt/` Responses backend preserves `anthropic-beta` computer-use headers, accepts schema-less `computer_*` tool definitions, or emits Anthropic-compatible computer-use `tool_use` blocks.

### Security isolation is mandatory

Anthropic recommends dedicated VMs/containers, minimal privileges, no sensitive accounts/data, domain allowlists, and human confirmation for meaningful real-world consequences ([Anthropic computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)). The ZombAIs report is a concrete warning that prompt injection can lead an autonomous computer-use host into downloading and executing untrusted code when the environment is too permissive ([ZombAIs](https://embracethered.com/blog/posts/2024/claude-computer-use-c2-the-zombais/)).

### Codex Desktop computer use is separate and currently operationally finicky

Codex app computer use should be evaluated as OpenAI product functionality, not as an Anthropic API proxy proof. `openai/codex#18258` shows multiple users hitting plugin-unavailable states, missing cache paths, helper app registration problems, region gating, build/architecture issues, and partial functionality where backend behavior and settings UI disagree ([openai/codex#18258](https://github.com/openai/codex/issues/18258)).

### Open-source stacks show better isolation and Mac-native design options

`trycua/cua` emphasizes background macOS control without stealing cursor/focus, plus sandboxes and benchmarks ([trycua/cua](https://github.com/trycua/cua)). `e2b-dev/open-computer-use` provides a cloud Linux desktop sandbox with live display and multi-provider model support ([e2b-dev/open-computer-use](https://github.com/e2b-dev/open-computer-use)). `open-codex-computer-use` wraps computer use as MCP and explicitly calls out macOS Accessibility and Screen Recording permissions ([iFurySt/open-codex-computer-use](https://github.com/iFurySt/open-codex-computer-use)).

## Current recommendation rationale

The least risky sequence is to keep the local LiteLLM proxy focused on text-client validation first, because that is already aligned with the current setup and LiteLLM docs. Anthropic computer use should be controlled with official Claude credentials before introducing a translation layer. Codex Desktop and open-source Mac/Linux computer-use stacks should be compared as separate runtime choices with their own permission, isolation, and failure-mode ledgers.

## Validation command

Before commit/finalization, run:

```bash
uv run python scripts/validate_research.py
```

If validation fails, fix structure/metadata/guide depth before final handoff.
