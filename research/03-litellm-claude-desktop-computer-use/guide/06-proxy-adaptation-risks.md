# 06. Proxy adaptation: what can fail through ChatGPT-backed LiteLLM

The proxy adaptation is the most interesting and least proven part of the project. It asks whether an Anthropic computer-use loop can run through a local LiteLLM proxy whose backend is a ChatGPT subscription Responses route.

The answer is not known from docs alone. It has to be tested.

LiteLLM documents Claude Code through LiteLLM and non-Anthropic models through Claude Code ([LiteLLM Claude Code quickstart](https://docs.litellm.ai/docs/tutorials/claude_responses_api), [LiteLLM non-Anthropic models](https://docs.litellm.ai/docs/tutorials/claude_non_anthropic_models)). Anthropic documents computer use as a beta tool loop with special headers and tools ([Anthropic computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)). The research did not find a source proving those two facts compose cleanly for a ChatGPT-backed `chatgpt/` route.

## The compatibility chain

For proxy-adapted computer use to work, all of these must be true:

1. The Anthropic SDK or demo code must be able to point at the LiteLLM base URL.
2. The request must include the right auth token for LiteLLM.
3. The request must name a model alias the proxy exposes.
4. LiteLLM must accept the computer-use beta header.
5. LiteLLM must preserve or correctly translate the beta header.
6. LiteLLM must accept the special `computer_20251124` tool definition.
7. LiteLLM must not drop required tool fields.
8. The ChatGPT-backed model must understand the task and produce a usable action request.
9. LiteLLM must convert the backend response into Anthropic-compatible `tool_use` blocks.
10. The demo loop must parse that response and execute the tool.

One broken link breaks the loop.

## Why normal Claude Code success is insufficient

Normal Claude Code success proves the proxy can handle text-heavy Anthropic-shaped requests. It may also prove ordinary tools can work in some cases. But computer use is special because Anthropic's docs use named tool types like `computer_20251124`, not just a normal JSON-schema function ([Anthropic computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)).

The backend is also not a native Claude model. It is a ChatGPT subscription route exposed through LiteLLM. Even if the backend has its own vision or computer-control capabilities elsewhere, the question here is narrower: does it behave like Anthropic's beta Messages API computer-use tool?

## Likely failure modes

### Header failure

The request may include `anthropic-beta: computer-use-2025-11-24`, but LiteLLM or the backend may reject, strip, ignore, or transform it. If the header disappears, the model may never see the computer-use contract.

### Tool definition failure

The `computer_20251124` tool may not look like a normal OpenAI/Responses tool. LiteLLM may expect a schema-bearing tool format for non-Anthropic providers. If it rejects the tool, the failure should be obvious. If it silently drops fields, the failure may be subtle.

### Model behavior failure

The backend model may answer in plain text instead of returning a tool call. That is still a useful result. It means the request reached a model, but the model did not operate as an Anthropic computer-use model.

### Response shape failure

The backend may emit a provider-native tool call. LiteLLM may not convert it into Anthropic `tool_use` content blocks. The demo loop may then fail to parse the response even though some tool intent exists.

### Loop continuation failure

The first tool call may work, but the second turn may fail when sending a `tool_result`. Multi-turn tool loops often expose incompatibilities that a single request does not.

### Safety classifier / confirmation mismatch

Anthropic's docs mention classifier defenses and user-confirmation behavior for possible prompt injections in screenshots ([Anthropic computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)). A non-native backend may not have the same safety layer or may represent it differently. That matters for any internet-facing test.

## How to run the adaptation cleanly

Start from the control demo that already passed. Change only the API route settings:

```text
Base URL: LiteLLM proxy as seen from inside the container
Auth token: constrained LiteLLM key
Model: one exposed LiteLLM alias
Prompt: same trivial control prompt
Sandbox: unchanged
Tool versions: unchanged
Display: unchanged
```

From inside a container, `localhost` usually means the container itself. The proxy may need `host.docker.internal`, host networking, or an explicit host IP. That is a networking concern, not an API compatibility conclusion. Record it separately.

## What to capture

The adaptation should capture raw evidence at each boundary:

```text
Anthropic SDK request payload
Request headers, especially beta headers
LiteLLM incoming request log
LiteLLM transformed/backend request if available
Backend response or error
LiteLLM outgoing Anthropic-shaped response
Demo loop parse result
Tool execution result
```

The goal is not just to get a green run. The goal is to know exactly where the bridge succeeds or fails.

## Possible outcomes

### Outcome A: full pass

The model emits Anthropic-compatible `tool_use`, the sandbox executes it, tool results are returned, and the trivial task completes. This would be strong evidence that the local proxy can support at least a minimal computer-use loop. It would still need broader safety and task testing.

### Outcome B: bridge rejects request

The request fails before reaching the backend because LiteLLM rejects the header/tool shape. This suggests a LiteLLM bridge limitation or configuration issue.

### Outcome C: backend rejects request

LiteLLM forwards enough of the request that the backend rejects it. This suggests the ChatGPT route does not support the translated computer-use tool shape.

### Outcome D: backend returns text

The model answers in natural language rather than tool calls. This suggests the backend is usable for reasoning about UI tasks but not as an Anthropic computer-use engine.

### Outcome E: partial tool shape

Some tool intent appears, but the demo cannot parse or execute it. This might be fixable with an adapter, but it should not be called support until the loop works.

## When to stop

Stop the adaptation if the only way forward is to remove safety boundaries, expose real credentials, mount a host browser profile, or give the sandbox broad host access. A green result produced by unsafe conditions is not useful.

Also stop if the proxy run fails ambiguously and the control has not been rerun recently. Re-establish the control before debugging the bridge.

## What productizing would require

If the proxy adaptation works, productizing still requires more than a demo:

- constrained virtual keys;
- request/response logging with secrets redacted;
- domain allowlists;
- sandbox lifecycle cleanup;
- human confirmation for consequential actions;
- prompt-injection handling;
- regression tests for tool shape;
- version pinning for LiteLLM and the demo;
- a clear statement that the backend is not native Anthropic Claude.

If it does not work, that is still a useful result. The project can keep Claude Desktop text routing as supported and evaluate computer use through either real Claude credentials, Codex Desktop, or open-source runtimes.
