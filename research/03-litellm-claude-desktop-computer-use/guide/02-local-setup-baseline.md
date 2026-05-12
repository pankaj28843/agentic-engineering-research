# 02. Local setup: what the current LiteLLM proxy already proves

The local setup is not a generic LiteLLM install. It is already a working coding-agent proxy lab, and that matters because it gives the experiment a stable first gate.

The inspected setup showed Claude Code configured to use a local LiteLLM gateway at `http://localhost:11435`, direct `chatgpt/` model names, and an `apiKeyHelper` rather than an embedded key. The local `litellm-proxy` repository documents a Docker daemon on the same port, ChatGPT OAuth token persistence under `./data/chatgpt/`, Responses-mode model metadata, and setup snippets for Codex and Claude Code. The proxy configuration exposes aliases such as `chatgpt/gpt-5.5`, `chatgpt/gpt-5.4`, `chatgpt/gpt-5.4-mini`, `chatgpt/gpt-5.3-codex`, and related routes.

That local evidence is important, but it should be interpreted narrowly. It proves the user has already solved the basic problem of getting local coding clients to talk to a LiteLLM proxy. It does not prove that every Anthropic beta feature can pass through that proxy.

## The current baseline

The baseline is:

```text
Claude Code or Codex-ish client
        -> localhost:11435 LiteLLM proxy
        -> chatgpt/ provider route
        -> ChatGPT subscription Responses backend
```

LiteLLM's Claude Code docs support this general shape. They show Claude Code configured with `ANTHROPIC_BASE_URL` pointing at LiteLLM and `ANTHROPIC_AUTH_TOKEN` holding a LiteLLM key ([LiteLLM Claude Code quickstart](https://docs.litellm.ai/docs/tutorials/claude_responses_api)). The local setup uses an API-key helper rather than placing the key in a file, which is better for avoiding accidental disclosure in research artifacts.

The local proxy also contains a Claude-specific patch that normalizes system-message content. That is a useful clue: the ChatGPT subscription backend does not naturally accept every Anthropic-shaped payload exactly as Claude Code sends it. The text path can be made to work, but some translation details already require glue.

## What this proves

The current setup proves five things if the baseline smoke tests pass:

1. The proxy process is reachable from the host.
2. Authentication through the helper works for Claude Code.
3. The model aliases resolve to LiteLLM routes.
4. The ChatGPT subscription backend can return normal text completions through the Anthropic-ish surface.
5. The local repository already has operational knowledge for running and patching this proxy.

That is enough to justify a Claude Desktop text experiment. It is also enough to justify using Claude Code as the regression gate before any Desktop changes.

## What this does not prove

It does not prove Anthropic computer use works.

Computer use is not just normal text completion with a screen attached. Anthropic's docs describe a beta header, a versioned tool definition, a sandboxed environment, tool execution by the application, and repeated `tool_use` / `tool_result` turns ([Anthropic computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)). A proxy that can translate text messages may still fail on:

- preserving `anthropic-beta` headers;
- accepting schema-less or special `computer_*` tool definitions;
- mapping Anthropic tool use to a backend that does not know that tool type;
- returning Anthropic-compatible `tool_use` blocks;
- preserving the exact stop reasons needed for the agent loop;
- not dropping fields because of proxy `drop_params` behavior.

LiteLLM's non-Anthropic model tutorial says LiteLLM can translate between provider formats for Claude Code while maintaining the Anthropic Messages API shape ([LiteLLM non-Anthropic models](https://docs.litellm.ai/docs/tutorials/claude_non_anthropic_models)). That is useful evidence for text and ordinary compatibility. It is not direct evidence for this beta computer-use contract.

## Why Claude Code should stay the first gate

Claude Code is the closest thing to a known-good path. If a change to the proxy breaks Claude Code, that change should be fixed before testing Desktop or computer-use paths. Otherwise every later failure becomes ambiguous.

A good baseline run should record:

- proxy liveness result;
- `/v1/models` or equivalent model list;
- selected alias and backend route;
- Claude Code one-turn request success;
- whether usage/logging shows the request;
- any proxy warnings about dropped parameters or transformed payloads.

The goal is not to over-test text chat. The goal is to freeze a known-good starting point so that Desktop and computer-use failures can be localized.

## Why key scope matters

The existing Claude Code setup uses an API-key helper. Claude Desktop's LiteLLM docs, however, specifically refer to a LiteLLM virtual key for the Gateway URL setup ([LiteLLM Claude Desktop integration](https://docs.litellm.ai/docs/tutorials/claude_desktop_cowork)). That distinction matters.

A desktop app is a broader and more persistent surface than one terminal session. If possible, the Desktop test should use a constrained LiteLLM virtual key limited to the specific aliases needed for the experiment. The key should be visible in usage logs and easy to revoke.

The same principle becomes more important for computer use. A computer-use environment can browse, download, type, click, and sometimes run shell commands. If its model route is backed by a broad proxy key, the blast radius is larger than necessary.

## The local patch as a warning sign

The presence of a local `patch_chatgpt_claude.py` is not bad. It is evidence that the user already knows how to adapt LiteLLM's Anthropic bridge to the ChatGPT subscription backend. But it is also a warning: Anthropic-to-ChatGPT compatibility is not automatic at every edge.

Text system-message normalization is a small edge. Computer-use beta tools are a much larger edge. If the proxy-adapted computer-use run fails, the failure should be captured as raw request/response evidence, not hand-waved as "LiteLLM doesn't work."

Useful failure evidence includes:

- the outgoing `/v1/messages` payload;
- headers, especially beta headers;
- tool definitions after LiteLLM transformation;
- backend error response;
- whether `drop_params` removed anything;
- whether the model returned normal text instead of `tool_use`;
- whether a tool call was emitted in a different provider-native format.

## Baseline acceptance criteria

Before moving past the local setup stage, the lab should be able to say:

```text
The proxy is reachable.
The intended model aliases are listed.
Claude Code can complete a normal request.
The request is visible in logs/usage.
The key path is known and does not expose the master key in research notes.
No computer-use environment has access to sensitive host data.
```

If those are true, the next step is Claude Desktop/Cowork text routing. If those are false, fix the proxy path before opening any desktop-control surface.
