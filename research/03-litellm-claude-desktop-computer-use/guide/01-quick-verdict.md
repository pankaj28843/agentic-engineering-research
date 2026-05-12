# 01. Quick verdict: three experiments, not one

The main mistake to avoid is thinking there is one switch called "computer use" that can be enabled across Claude Desktop, Claude Code, LiteLLM, ChatGPT subscription routes, and Codex Desktop. The names overlap, but the underlying contracts are different.

Think of the space as three layers:

1. **Client routing.** Can a client send normal model requests through your local LiteLLM proxy?
2. **Tool-loop compatibility.** Can a model and gateway preserve the exact tool schema, beta headers, and stop reasons needed for computer use?
3. **Desktop execution.** Can some isolated runtime actually see a screen, click, type, scroll, run commands, and report results safely?

Claude Code through your local proxy mostly tests layer 1. Claude Desktop/Cowork third-party inference through LiteLLM also mostly tests layer 1. Anthropic computer use needs layers 2 and 3. Codex Desktop computer use is a product that bundles its own version of layers 2 and 3, but that product path does not prove the Anthropic API path works.

## What is ready to test first

The first test should be boring: make sure the local LiteLLM proxy is alive, lists the expected model aliases, and can answer a one-turn Claude Code request. LiteLLM's Claude Code quickstart describes pointing Claude Code at LiteLLM with `ANTHROPIC_BASE_URL` and `ANTHROPIC_AUTH_TOKEN` ([LiteLLM Claude Code quickstart](https://docs.litellm.ai/docs/tutorials/claude_responses_api)). Your local setup already has the same shape: a proxy on `localhost:11435`, direct `chatgpt/` model names, and an API-key helper instead of an embedded secret.

That first test matters because it isolates the proxy from Desktop and computer-use complexity. If Claude Code cannot do a text request through the proxy, a Claude Desktop failure will not tell you anything new. It might be a Desktop 3P problem, an auth problem, a model alias problem, a proxy problem, or a backend problem.

## What is feasible but narrower than it sounds

Claude Desktop/Cowork through LiteLLM is feasible as a third-party inference experiment. LiteLLM's docs say Claude Desktop requests can route through LiteLLM Proxy for unified logging, budget controls, and access to any model. The documented path is: enable Developer Mode, open Configure Third-Party Inference, enter the LiteLLM Gateway URL and virtual key, save, restart, then verify traffic in the LiteLLM Dashboard ([LiteLLM Claude Desktop integration](https://docs.litellm.ai/docs/tutorials/claude_desktop_cowork)).

But this only proves that Desktop can send normal inference traffic to LiteLLM. It does not prove Claude Desktop will expose Anthropic computer-use tools. It also does not prove a ChatGPT subscription backend can produce Anthropic-shaped `tool_use` blocks for a `computer_20251124` tool.

For the local experiment, the unknowns are concrete:

- Does Claude Desktop accept a local plain-HTTP `http://localhost:11435` Gateway URL?
- Does the Desktop app run on the same host/network namespace as the proxy?
- Does it require a LiteLLM virtual key rather than a broad master key?
- Does the model selector use LiteLLM aliases the same way Claude Code does?
- Does the LiteLLM Dashboard attribute traffic to the expected key?

Those are good Desktop/Cowork questions. They are not computer-use questions yet.

## What needs a control before proxy adaptation

Anthropic computer use is a beta API/tool-loop feature. The docs say it requires beta headers such as `computer-use-2025-11-24`, compatible models, and tools such as `computer_20251124`, `text_editor_20250728`, and `bash_20250124` ([Anthropic computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)). The application must provide a sandboxed computing environment and execute the actions Claude requests. Claude returns a tool request; your code performs the screenshot/click/type/command; your code returns results.

That means the official demo should be run unchanged first. The Anthropic quickstarts repository identifies the Computer Use Demo as an environment and tools Claude can use to control a desktop computer, with latest `computer_use_20251124` support ([Claude Quickstarts](https://github.com/anthropics/anthropic-quickstarts)). If the official demo does not run with real Claude credentials, adapting it to the local LiteLLM proxy is premature.

The control run tells you whether Docker/VNC/browser/display wiring works. The proxy run tells you whether LiteLLM plus the backend preserves the Anthropic beta contract. Without the control, you cannot separate environment failures from API translation failures.

## What Codex Desktop can and cannot prove

Codex Desktop computer use is worth comparing because it targets the same user desire: an agent that can operate a computer. OpenAI has official Codex app computer-use documentation and related app feature docs ([Codex computer use](https://developers.openai.com/codex/app/computer-use), [Codex features](https://developers.openai.com/codex/app/features)). But Codex Desktop is product-mediated. It has its own app, plugins, helpers, permissions, feature gates, and UX.

GitHub issue reports show why this matters. `openai/codex#18258` documents users seeing `Computer Use plugin unavailable`, missing cache paths, bundled helper registration problems, region/feature gating, and partial states where the backend appears alive while the UI still says unavailable ([openai/codex#18258](https://github.com/openai/codex/issues/18258)). That is not the same failure class as Anthropic `computer_*` tool translation through LiteLLM.

Codex can answer: "Is OpenAI's app computer-use product useful for my Mac workflow?" It cannot answer: "Does Anthropic computer use work through my ChatGPT-backed LiteLLM proxy?"

## The recommended order

Run the work in this order:

1. **Proxy baseline.** Health, models, Claude Code one-turn text request.
2. **Desktop 3P text.** Claude Desktop/Cowork through LiteLLM with a constrained key.
3. **Computer-use control.** Official Anthropic demo with real Claude credentials in an isolated desktop.
4. **Computer-use proxy adaptation.** Same demo pointed at the LiteLLM proxy, with raw request/response capture.
5. **Codex comparison.** Codex Desktop on macOS with plugin, helper, permission, and region checks.
6. **Open-source comparison.** trycua/cua, E2B open-computer-use, open-codex-computer-use, and OpenClaw-style Mac automation patterns.

That order minimizes ambiguity. It also prevents the most dangerous failure: giving a half-understood computer-use agent too much access just because a text proxy worked.

## Bottom line

Support the local LiteLLM route for Claude Code and Claude Desktop text experiments first. Treat Anthropic computer use as a separate beta tool-loop experiment that must be controlled with a real Claude backend before any proxy adaptation. Treat Codex Desktop computer use and open-source computer-use stacks as product/runtime comparisons, not compatibility evidence for the Anthropic API.
