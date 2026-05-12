# Theme 03: LiteLLM, Claude Desktop, and Computer Use

This theme is an experiment guide for routing Claude-family desktop/coding clients through the user's local LiteLLM ChatGPT-subscription proxy, while separately evaluating Anthropic computer-use loops, Codex Desktop computer use, and open-source computer-use stacks.

## Start here

- [guide/00-README.md](guide/00-README.md) — chapter-wise guide and staged experiment path.
- [briefing.md](briefing.md) — evidence-weighted verdict and validation gates.
- [source-index.md](source-index.md) — source catalog with quality labels and caveats.
- [research-log.md](research-log.md) — CDP, HN, socli, GitHub, and local setup notes.
- [sources.json](sources.json) — machine-readable source metadata.

## One-sentence takeaway

Use the existing `localhost:11435` LiteLLM route first for Claude Code and Claude Desktop/Cowork text-chat validation, but treat Anthropic computer use as a separate beta API/tool-loop experiment that should be controlled with real Claude credentials before trying any ChatGPT-backed LiteLLM compatibility bridge.

## Current confidence

High confidence that Claude Desktop/Cowork can be pointed at a LiteLLM Gateway URL with a virtual key, because LiteLLM documents that path. High confidence that Anthropic computer use requires a sandbox, beta header, `computer_*` tool definitions, and an application-run agent loop. Medium-to-low confidence that the current ChatGPT-backed LiteLLM route can preserve Anthropic computer-use beta semantics, because the research found no strong proof that `computer_*` tool loops survive that translation path.

## Suggested experiment order

1. Baseline the local proxy and Claude Code text path.
2. Create or use a constrained LiteLLM key for desktop experiments.
3. Configure Claude Desktop/Cowork third-party inference and verify usage logging.
4. Run the official Anthropic computer-use demo unchanged as a control.
5. Only then adapt the demo to the local proxy and capture exact request/response failures.
6. Compare Codex Desktop and open-source stacks such as `trycua/cua`, `e2b-dev/open-computer-use`, and `open-codex-computer-use` as separate product/runtime choices.
