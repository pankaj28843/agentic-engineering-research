# Briefing: LiteLLM, Claude Desktop, and Computer Use

_Last refreshed: 2026-05-12_

## Executive verdict

The practical answer is to split this into three experiments, not one:

1. **Claude Code through LiteLLM is the baseline gate.** The local setup already points Claude Code at `http://localhost:11435` with direct `chatgpt/` model routes and an API-key helper. LiteLLM's Claude Code quickstart documents using `ANTHROPIC_BASE_URL` and `ANTHROPIC_AUTH_TOKEN` against its proxy, including unified and Anthropic pass-through endpoint styles ([LiteLLM Claude Code quickstart](https://docs.litellm.ai/docs/tutorials/claude_responses_api)). If this path regresses, Desktop and computer-use experiments are not ready.
2. **Claude Desktop/Cowork text chat through LiteLLM is feasible.** LiteLLM documents a Claude Desktop/Cowork flow: enable Developer Mode, open Configure Third-Party Inference, enter the LiteLLM Gateway URL and a virtual key, restart Desktop, and verify usage in the LiteLLM Dashboard ([LiteLLM Claude Desktop integration](https://docs.litellm.ai/docs/tutorials/claude_desktop_cowork)). Treat this as a text-chat and cost/logging experiment first.
3. **Anthropic computer use is a separate beta API/tool-loop contract.** The computer-use docs require a beta header, compatible Claude model, `computer_20251124` or older tool type, an application-run sandbox/VM/container, tool execution, and an agent loop that returns `tool_result` blocks ([Anthropic computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)). It is not proven by making Claude Desktop talk through LiteLLM.
4. **The current ChatGPT-backed LiteLLM route is a compatibility experiment, not a supported computer-use backend.** LiteLLM documents non-Anthropic model translation for Claude Code ([LiteLLM non-Anthropic models](https://docs.litellm.ai/docs/tutorials/claude_non_anthropic_models)), but the research did not find evidence that ChatGPT subscription Responses routes emit Anthropic-compatible `tool_use` blocks for schema-less `computer_*` tools or preserve the `anthropic-beta` computer-use semantics end to end.
5. **Codex Desktop computer use is a useful comparison path, not evidence for Anthropic compatibility.** OpenAI has Codex app computer-use documentation and product pages ([Codex computer use](https://developers.openai.com/codex/app/computer-use), [Codex features](https://developers.openai.com/codex/app/features)), while GitHub issues show real app/plugin/permission failure modes such as `Computer Use plugin unavailable` ([openai/codex#18258](https://github.com/openai/codex/issues/18258)). Evaluate it as a product-mediated Mac app capability.

## Recommended experiment sequence

| Stage | Goal | Pass condition | Do not proceed if |
|---|---|---|---|
| 1. Proxy baseline | Prove local LiteLLM is alive and Claude Code still works. | `/health/liveliness`, `/v1/models`, and a one-turn Claude Code text request succeed. | Proxy liveness, auth helper, or model aliasing is broken. |
| 2. Key isolation | Avoid exposing a master key to desktop apps. | A LiteLLM virtual key is limited to the needed aliases and visible in usage logs. | Only a broad master key is available and cannot be constrained. |
| 3. Claude Desktop 3P | Validate text chat via LiteLLM/Cowork. | Desktop sends traffic visible in LiteLLM usage and returns a normal response. | Desktop cannot reach local HTTP gateway or rejects the key/gateway. |
| 4. Anthropic control | Validate the official computer-use demo with a real Claude backend. | Demo can take screenshots, click/type, and complete a trivial task in an isolated desktop. | The demo or local container/VM setup fails before proxy adaptation. |
| 5. Proxy adaptation | Test whether LiteLLM preserves computer-use semantics. | Either completes a trivial tool loop or fails with captured request/response proving the unsupported field. | Failure is ambiguous because no control run exists. |
| 6. Product comparison | Compare Codex Desktop and open-source stacks. | Capabilities, permissions, isolation, and failure modes are recorded separately from Anthropic API results. | Product behavior is used as proof of Anthropic API compatibility. |

## Key risks

### Prompt injection and desktop authority

Anthropic's docs explicitly say computer use has unique risks, especially when interacting with the internet, and recommend dedicated VMs/containers, minimal privileges, avoiding sensitive data, domain allowlists, and human confirmation for consequential actions ([Anthropic computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)). A practitioner report demonstrated a prompt-injection path where Claude Computer Use downloaded and ran a binary and connected to command-and-control infrastructure in an educational security demo ([ZombAIs](https://embracethered.com/blog/posts/2024/claude-computer-use-c2-the-zombais/)).

### Translation gap between Anthropic and ChatGPT-backed routes

The local proxy is intentionally useful because LiteLLM can translate non-Anthropic providers into Anthropic-style client surfaces. That is enough to validate text chat and many Claude Code flows. Computer use is narrower: it depends on beta headers, versioned tool types such as `computer_20251124`, `text_editor_20250728`, and `bash_20250124`, and repeated `tool_use` / `tool_result` turns. The compatibility test should capture raw request/response fields rather than assume tool parity.

### Desktop app reachability and key scope

LiteLLM's Claude Desktop documentation uses a Gateway URL and virtual key, and the example URL is public HTTPS-shaped. A local `localhost:11435` HTTP gateway may work only if Claude Desktop runs on the same host and accepts local HTTP in third-party inference mode. If the Desktop app or managed configuration requires a different reachability model, use an explicit local-network or tunnel experiment with a constrained key rather than broadening access casually.

### Codex Desktop maturity and platform gating

Codex Desktop computer use is real enough to compare, but user reports show it can be unavailable or partially functional depending on plugin cache, bundled helper app registration, region/feature gates, architecture, and macOS permission state ([openai/codex#18258](https://github.com/openai/codex/issues/18258)). Any Codex experiment should record app version, region, permissions, helper state, and whether the failure is UI-only, backend-only, or end-to-end.

## Open-source comparison map

| Stack | What it is | Why it matters | Main caveat |
|---|---|---|---|
| [Anthropic computer-use demo](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo) | Official Docker/VNC/browser/tool-loop reference. | Best control for the Anthropic API contract. | Requires compatible Claude credentials or official cloud provider path for the control. |
| [trycua/cua](https://github.com/trycua/cua) | Computer-use agent stack with background macOS control, sandboxes, benchmarks, and Lume virtualization. | Strong Mac-native comparison path; explicitly targets not stealing cursor/focus. | Separate runtime and API; not proof that Anthropic `computer_*` works through LiteLLM. |
| [e2b-dev/open-computer-use](https://github.com/e2b-dev/open-computer-use) | Cloud Linux desktop sandbox controlled by multiple LLM providers. | Good isolation pattern and provider-swapping example. | Depends on E2B and provider keys; Linux desktop differs from Mac Desktop/Codex. |
| [iFurySt/open-codex-computer-use](https://github.com/iFurySt/open-codex-computer-use) | MCP-wrapped open Computer Use service for macOS/Linux/Windows, inspired by Codex. | Useful bridge for Codex/Claude/Gemini clients and permission model exploration. | Community project; evaluate maturity and security posture before trusting. |
| [OpenClaw Peekaboo discussion](https://github.com/openclaw/openclaw/issues/67776) | Mac desktop-control architecture discussion. | Highlights the real UX tradeoff: coordinate screenshot/click loops can steal cursor/focus; Accessibility-style semantic control helps. | OpenClaw's solution is its own bridge/skill path, not Codex-native or Anthropic-native compatibility. |

## Decision rule

Support the local LiteLLM setup for **Claude Code and Claude Desktop text chat** if the first three validation stages pass. Support **Anthropic computer use** only when the official control succeeds and the proxy-adapted run either succeeds or fails with a well-understood, documented incompatibility. Support **Codex Desktop computer use** as a separate Mac product comparison only after checking plugin availability, region/feature gates, helper registration, and macOS permissions.

## Open questions

- Does Claude Desktop 3P mode accept `http://localhost:11435` on this target machine, or does it require HTTPS/public reachability?
- Can the local LiteLLM proxy expose a safer virtual key limited to the desktop/computer-use aliases?
- Does LiteLLM's Anthropic gateway preserve `anthropic-beta` computer-use headers and schema-less `computer_*` tools for a `chatgpt/` Responses backend?
- Does the ChatGPT-backed model ever emit Anthropic-compatible `tool_use` blocks for `computer_*`, or does the bridge reject/strip them?
- Which Codex Desktop computer-use capabilities are product-only, and which can be reproduced through MCP/open-source runtimes?
