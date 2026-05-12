# 08. Open-source computer-use stacks and Mac-native design choices

Open-source computer-use projects are useful because they separate the desktop-control runtime from any one model vendor. They also expose design choices that product docs often hide: sandboxing, cursor control, accessibility APIs, screenshots, streaming, permissions, and model-provider swapping.

The deeper GitHub and CDP pass found several relevant stacks. None of them proves Anthropic computer use works through LiteLLM. They are comparison paths and design references.

## trycua/cua

`trycua/cua` is the strongest open-source comparison signal found. Its README describes a stack for building, benchmarking, and deploying agents that use computers. It includes background macOS computer use, agent-ready sandboxes, benchmarks, Lume macOS virtualization, and tools such as `cuabot` ([trycua/cua](https://github.com/trycua/cua)).

The most relevant claim for this project is Cua Driver: it says agents can drive native macOS apps in the background without stealing the cursor, focus, or Space, including non-Accessibility surfaces like Chromium web content and canvas-heavy apps. That directly addresses one of the biggest UX problems with screenshot/click computer-use loops.

Cua also exposes a broader sandbox API:

```text
screenshot
mouse.click
keyboard.type
shell.run
Linux/macOS/Windows/Android sandboxes
local or cloud runtimes
```

That makes it useful for two different experiments:

- Mac-native automation comparison against Codex Desktop.
- Sandbox/runtime comparison against Anthropic's Docker reference.

The caveat is that Cua is its own stack. It may be a better runtime choice, but it does not answer whether `computer_20251124` survives LiteLLM translation.

## E2B open-computer-use

`e2b-dev/open-computer-use` provides a secure cloud Linux computer powered by E2B Desktop Sandbox and controlled by open-source LLMs ([e2b-dev/open-computer-use](https://github.com/e2b-dev/open-computer-use)). Its README emphasizes:

- secure desktop sandbox;
- keyboard, mouse, and shell commands;
- live display streaming;
- pause-and-prompt control;
- Ubuntu by default;
- support for many model providers;
- provider-swappable architecture.

This is a good isolation reference. If the goal is to avoid giving an agent access to the user's real desktop, an E2B-style disposable Linux desktop is safer than a local Mac desktop. It also models provider-swapping explicitly, with provider entries for OpenAI, Anthropic, Gemini, DeepSeek, Groq, Fireworks, OpenRouter, Moonshot, Mistral, and grounding models such as OS-Atlas/ShowUI.

The tradeoff is fidelity. A cloud Ubuntu desktop is not the user's macOS environment. It is excellent for web tasks, simple GUI tasks, and safe experiments. It is not enough for tasks that require the user's actual Mac apps, local accounts, or personal desktop context.

## open-codex-computer-use

`iFurySt/open-codex-computer-use` is an open-source Computer Use service wrapped as MCP. Its README says any AI agent or MCP client can use it to run Computer Use on macOS, Linux, and Windows, and that it was inspired by OpenAI Codex Computer Use ([open-codex-computer-use](https://github.com/iFurySt/open-codex-computer-use)).

The README is especially useful for integration clues:

- `open-computer-use install-codex-mcp`
- `open-computer-use install-codex-plugin`
- `open-computer-use install-claude-mcp`
- `open-computer-use install-gemini-mcp`
- `open-computer-use install-opencode-mcp`

It also explicitly says that on macOS, the user should run it once and grant Accessibility and Screen Recording. That mirrors the likely permission needs of product computer-use systems and makes the permission boundary visible.

This project is useful if the user wants an MCP-shaped computer-use layer that multiple agents can call. It should be reviewed carefully before trusting it with sensitive desktop access, but it is directly relevant to experiments involving Codex CLI/app and Claude Code.

## OpenClaw and Peekaboo-style architecture

The OpenClaw issue `Feature Request: Codex Computer Use integration for Mac desktop control` is not just a feature request. It contains a useful design discussion ([OpenClaw issue 67776](https://github.com/openclaw/openclaw/issues/67776)).

One comment warns that coordinate-based computer use, where the agent screenshots, clicks coordinates, and screenshots again, hijacks the user's cursor and focus. The commenter argues that Accessibility APIs can target many real Mac UI elements semantically, often faster and without cursor theft, falling back to screenshot/click for canvas-heavy apps.

The issue was later closed as implemented through OpenClaw's Peekaboo skill and PeekabooBridge path, which provides screen inspection, UI element targeting, input, app/window/menu control, and permission-aware local brokerage.

For this project, the lesson is architectural:

```text
Vision loop only -> simple but intrusive and brittle.
Accessibility/semantic control -> less intrusive, faster for many native Mac tasks.
Hybrid approach -> use semantic control when possible, screenshot/click as fallback.
```

That lesson should shape any Mac-native experiment, including Codex Desktop comparisons.

## Agent desktop and orchestration projects

The deeper search also found `lahfir/agent-desktop`, a native desktop automation CLI for AI agents, and `alekseyrozh/openclawdex`, an orchestration UI for Claude Code and Codex ([agent-desktop](https://github.com/lahfir/agent-desktop), [openclawdex](https://github.com/alekseyrozh/openclawdex)). These were lower-confidence sources than Cua/E2B/OpenClaw but useful ecosystem signals.

They show that the ecosystem is converging on a pattern:

- the LLM is not enough;
- a desktop-control server or MCP layer is needed;
- orchestration decides when to hand off to desktop control;
- permissions and local brokers matter;
- replay/logging matters for trust.

## How to compare open-source stacks

Use a matrix rather than a vibe check:

| Criterion | Why it matters |
|---|---|
| Isolation | Can the agent damage only a disposable environment? |
| Mac fidelity | Can it operate native Mac apps if needed? |
| Cursor/focus behavior | Can the human keep using the machine? |
| Permission model | Does it require Accessibility, Screen Recording, helper apps, or privileged brokers? |
| Model independence | Can it swap providers or does it assume one vendor? |
| MCP/client integration | Can Claude Code, Codex, Gemini, or OpenClaw call it cleanly? |
| Auditability | Are actions logged, replayed, or inspectable? |
| Safety controls | Can humans pause, approve, or constrain network/domains? |
| Maturity | Stars, issues, docs, releases, maintainers, and recent activity. |

## Recommended roles

A sensible role assignment is:

- **Anthropic demo:** control for Anthropic API contract.
- **Cua:** Mac-native/background-control comparison.
- **E2B open-computer-use:** isolated Linux sandbox comparison.
- **open-codex-computer-use:** MCP/product-interop experiment.
- **OpenClaw/Peekaboo:** architecture reference for semantic Mac UI control.
- **Codex Desktop:** product UX comparison.

This keeps each stack honest. It avoids forcing a single tool to answer every question.

## The main design lesson

Computer use is not just a model capability. It is a harness capability. The harness decides where the computer lives, what the agent can see, how actions are executed, whether the user can interrupt, and how much damage a bad instruction can cause.

Open-source stacks are valuable because they let you inspect and choose that harness rather than accepting a product's defaults blindly.
