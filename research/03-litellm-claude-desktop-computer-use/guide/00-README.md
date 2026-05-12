# Guide: LiteLLM, Claude Desktop, and Computer Use

This guide answers a practical lab question: **How should you test Claude Desktop, Claude computer use, Codex Desktop computer use, and open-source computer-use stacks when your local coding-agent setup already routes through a LiteLLM ChatGPT-subscription proxy?**

The short version is simple: do not collapse all of these into one experiment. Claude Desktop text chat through LiteLLM, Anthropic API computer use, Codex Desktop computer use, and open-source computer-control runtimes have overlapping names but different contracts, risks, and validation gates.

## Reading path

1. [Quick verdict: three experiments, not one](01-quick-verdict.md)
2. [Local setup: what the current LiteLLM proxy already proves](02-local-setup-baseline.md)
3. [Claude Desktop and Cowork through LiteLLM](03-claude-desktop-cowork.md)
4. [Anthropic computer use as a beta tool loop](04-anthropic-computer-use-contract.md)
5. [Control first: running the official computer-use demo](05-control-demo-before-proxy.md)
6. [Proxy adaptation: what can fail through ChatGPT-backed LiteLLM](06-proxy-adaptation-risks.md)
7. [Codex Desktop computer use as a separate product path](07-codex-desktop-comparison.md)
8. [Open-source computer-use stacks and Mac-native design choices](08-open-source-computer-use-stacks.md)
9. [Security model and safe experiment harness](09-security-and-isolation.md)
10. [Experiment checklist and decision log](10-experiment-checklist.md)
11. [Request and response boundary debugging](11-request-response-boundary-debugging.md)
12. [Mac desktop UX: cursor, focus, permissions, and helpers](12-mac-desktop-ux.md)
13. [How to read and refresh the source set](13-reading-and-refreshing-sources.md)

## Current short answer

Start with the thing closest to your current setup: Claude Code through the local LiteLLM proxy. LiteLLM documents Claude Code using `ANTHROPIC_BASE_URL` and an auth token against the proxy ([LiteLLM Claude Code quickstart](https://docs.litellm.ai/docs/tutorials/claude_responses_api)), and your local setup already follows that shape with `localhost:11435`, direct `chatgpt/` model names, and a key helper. If that path is not green, everything downstream becomes noise.

Then test Claude Desktop/Cowork as a **text-chat third-party inference** path. LiteLLM documents the exact Desktop flow: enable Developer Mode, open Configure Third-Party Inference, enter the Gateway URL and LiteLLM virtual key, save, restart, and verify usage logs ([LiteLLM Claude Desktop integration](https://docs.litellm.ai/docs/tutorials/claude_desktop_cowork)). This is feasible enough to try, but it should be treated as its own validation gate.

Finally, treat Anthropic computer use as a different beast. Anthropic's docs describe a beta feature with a beta header, versioned tools such as `computer_20251124`, an application-run sandbox, and a loop where your code executes screenshots/clicks/typing and returns `tool_result` blocks ([Anthropic computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)). Making Claude Desktop talk to LiteLLM does not automatically prove this loop works.

## Source stance

Google result pages were used only for discovery. Claims in this guide are grounded in extracted official docs, local setup inspection, GitHub API results, GitHub READMEs, HN item payloads, and practitioner/security writeups recorded in [research-log.md](../research-log.md) and [source-index.md](../source-index.md).
