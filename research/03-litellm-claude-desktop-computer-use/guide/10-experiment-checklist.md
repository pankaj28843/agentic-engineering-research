# 10. Experiment checklist and decision log

This chapter turns the research into a runnable checklist. The goal is to prevent ambiguous results. Each stage should have a clear pass, fail, or partial result.

Do not run these as one long session. Run them as separate gates.

## Stage 1: local proxy baseline

Purpose: prove the existing LiteLLM route is healthy before Desktop or computer-use experiments.

Record:

```text
Date:
Proxy repo commit:
Proxy health:
Model list includes target alias:
Claude Code model alias:
One-turn Claude Code request:
Usage/logging visible:
Warnings/errors:
```

Pass criteria:

```text
Proxy reachable.
Target model alias visible.
Claude Code text request succeeds.
No secret is printed into logs or research notes.
```

If this fails, stop. Fix the local proxy before testing Desktop.

Relevant source: LiteLLM documents Claude Code through `ANTHROPIC_BASE_URL` and an auth token against LiteLLM ([LiteLLM Claude Code quickstart](https://docs.litellm.ai/docs/tutorials/claude_responses_api)).

## Stage 2: LiteLLM key isolation

Purpose: avoid using a broad master key in persistent desktop or computer-use clients.

Record:

```text
Virtual key created:
Allowed aliases:
Budget/spend cap:
Expiration:
Usage attribution label:
Revocation tested:
```

Pass criteria:

```text
Desktop/computer-use experiments can use a constrained key.
Requests are attributed to that key.
The key can be revoked after testing.
```

LiteLLM's Claude Desktop docs specifically tell users to paste a LiteLLM virtual key into Claude Desktop's third-party inference settings ([LiteLLM Claude Desktop integration](https://docs.litellm.ai/docs/tutorials/claude_desktop_cowork)).

## Stage 3: Claude Desktop/Cowork text routing

Purpose: validate Desktop third-party inference through LiteLLM as a text path.

Record:

```text
Claude Desktop version:
Host OS:
Gateway URL tested:
Key used:
Prompt:
Response:
LiteLLM usage visible:
Model alias seen:
Errors:
```

Use a tiny prompt:

```text
Reply with exactly: desktop route ok
```

Pass criteria:

```text
Desktop accepts gateway/key.
Desktop returns normal response.
LiteLLM logs show request attributed to virtual key.
```

Partial pass:

```text
Desktop returns a response but logging/model attribution is unclear.
```

Fail:

```text
Desktop cannot connect, rejects gateway/key, or model alias resolution fails.
```

Relevant source: LiteLLM's Desktop/Cowork page documents Developer Mode, Configure Third-Party Inference, Gateway URL, virtual key, restart, and Dashboard verification ([LiteLLM Claude Desktop integration](https://docs.litellm.ai/docs/tutorials/claude_desktop_cowork)).

## Stage 4: official Anthropic computer-use control

Purpose: prove the official computer-use environment works without LiteLLM adaptation.

Record:

```text
Demo version/commit:
Model:
Beta header:
Tool version:
Container runtime:
Display resolution:
Network policy:
Prompt:
Tool_use observed:
Screenshot action:
Click/type action:
Final response:
Errors:
```

Use a local low-stakes prompt:

```text
Open the text editor, type "computer use control ok", take a screenshot, and stop.
```

Pass criteria:

```text
The demo emits and executes computer-use tool calls.
The sandbox returns screenshots/results.
The task completes without sensitive data exposure.
```

Relevant sources: Anthropic's docs define the beta header, tools, agent loop, and sandbox model ([Anthropic computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)); the Quickstarts repository identifies the Computer Use Demo as an official desktop-control quickstart ([Claude Quickstarts](https://github.com/anthropics/anthropic-quickstarts)).

## Stage 5: LiteLLM proxy-adapted computer-use run

Purpose: test whether the local ChatGPT-backed LiteLLM route can preserve the Anthropic computer-use contract.

Change only:

```text
Base URL
Auth token
Model alias
```

Keep the same:

```text
Demo version
Prompt
Sandbox
Display resolution
Tool versions
Network policy
```

Capture:

```text
Outgoing SDK request payload:
Headers:
LiteLLM incoming request:
Backend request/response if available:
LiteLLM outgoing response:
Demo parse result:
Tool execution result:
```

Pass criteria:

```text
The loop completes the same trivial task through LiteLLM.
```

Useful fail criteria:

```text
The exact unsupported header, field, tool type, response shape, or backend behavior is identified.
```

Do not call it a fail if container networking is wrong. Fix networking separately and rerun.

Relevant source: LiteLLM documents non-Anthropic provider translation for Claude Code ([LiteLLM non-Anthropic models](https://docs.litellm.ai/docs/tutorials/claude_non_anthropic_models)), but Anthropic computer use has a special beta tool contract ([Anthropic computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)).

## Stage 6: Codex Desktop comparison

Purpose: evaluate OpenAI's product-level Mac computer-use path separately.

Record:

```text
Codex app version:
Codex CLI version:
macOS version:
CPU architecture:
Region/account:
Computer Use settings state:
Plugin/helper state:
Accessibility permission:
Screen Recording permission:
First task:
Result:
Errors/logs:
```

Pass criteria:

```text
Codex Desktop can perform a trivial local desktop task.
Permissions and helper state are understood.
The user can interrupt or observe actions.
```

Known failure class: `openai/codex#18258` documents `Computer Use plugin unavailable`, cache/helper registration problems, region gating, and partial UI/backend mismatch ([openai/codex#18258](https://github.com/openai/codex/issues/18258)).

## Stage 7: open-source runtime comparison

Purpose: evaluate whether an open-source stack is a safer or more controllable path than product desktop automation.

Compare:

- [trycua/cua](https://github.com/trycua/cua)
- [e2b-dev/open-computer-use](https://github.com/e2b-dev/open-computer-use)
- [iFurySt/open-codex-computer-use](https://github.com/iFurySt/open-codex-computer-use)
- [OpenClaw Peekaboo-style architecture](https://github.com/openclaw/openclaw/issues/67776)

Record:

```text
Runtime:
Isolation model:
OS fidelity:
Permission model:
Cursor/focus behavior:
Model/provider support:
MCP/client integration:
Logging/replay:
Human stop control:
First task result:
```

Pass criteria:

```text
A stack can run a low-stakes task with better isolation, observability, or UX than the product/default path.
```

## Decision log template

Use one row per experiment:

| Date | Stage | Route/runtime | Result | Evidence | Next action |
|---|---|---|---|---|---|
| YYYY-MM-DD | Proxy baseline | LiteLLM `localhost:11435` | pass/fail/partial | health/model/request/log summary | next gate or fix |
| YYYY-MM-DD | Desktop 3P | Claude Desktop -> LiteLLM | pass/fail/partial | gateway/key/model/log summary | next gate or fix |
| YYYY-MM-DD | Anthropic control | official demo -> Claude API | pass/fail/partial | tool loop summary | next gate or fix |
| YYYY-MM-DD | Proxy adaptation | official demo -> LiteLLM | pass/fail/partial | raw boundary failure/pass | decide support |
| YYYY-MM-DD | Codex comparison | Codex Desktop | pass/fail/partial | plugin/permission/task summary | decide product path |
| YYYY-MM-DD | OSS comparison | Cua/E2B/MCP/etc. | pass/fail/partial | runtime/task summary | decide runtime path |

## Final decision rules

Support **Claude Desktop through LiteLLM** if Stage 3 passes.

Support **Anthropic computer use through real Claude** if Stage 4 passes with safe isolation.

Support **Anthropic computer use through the local LiteLLM proxy** only if Stage 5 passes or fails in a way that can be fixed with a small, auditable bridge change.

Support **Codex Desktop computer use** only as a product path after Stage 6, not as evidence for the Anthropic/LiteLLM path.

Support **open-source computer-use runtime work** if Stage 7 shows a safer or more controllable harness than either product path.

## The one-line operating rule

Every result should name the route it actually tested. "Computer use works" is too vague. "Official Anthropic demo with Claude API completed a local text-editor task in a disposable container" is useful.
