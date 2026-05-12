# 11. Request and response boundary debugging

The LiteLLM proxy-adapted computer-use experiment should be debugged as a boundary problem. A boundary problem asks: **what did each component receive, what did it send, and where did the contract change?**

That framing is better than asking whether "LiteLLM supports computer use" in the abstract. The local setup has multiple boundaries:

```text
Anthropic demo code
  -> Anthropic SDK request object
  -> HTTP request to LiteLLM
  -> LiteLLM Anthropic gateway
  -> LiteLLM provider transformation
  -> ChatGPT subscription Responses backend
  -> LiteLLM response transformation
  -> Anthropic demo parser
  -> computer-use tool executor
```

A failure at any boundary can look like "computer use failed." The job is to name the exact boundary.

## Boundary 1: demo configuration

The first boundary is the demo's own configuration. Before touching LiteLLM, confirm how the official demo selects:

- API provider;
- base URL;
- model name;
- beta header;
- tool version;
- max tokens;
- tool list;
- loop policy;
- display size.

Anthropic's docs show a request that includes `model`, `max_tokens`, a `tools` list with `computer_20251124`, and `betas=["computer-use-2025-11-24"]` ([Anthropic computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)). The proxy-adapted run should start as close to that request as possible.

A common mistake is changing the model, base URL, task prompt, tool version, and display resolution all at once. That makes the result impossible to interpret. Change only the route settings after the control passes.

## Boundary 2: SDK to HTTP

SDKs often hide important details. The Python object may look right, but the HTTP request may differ in headers, JSON field names, or endpoint path.

Capture or log:

```text
HTTP method
URL path
Authorization header shape, with secret redacted
anthropic-beta or beta field
Content-Type
model value
tools array
tool type strings
messages array
system field shape
```

Do not commit secrets. Redact keys before writing durable notes.

This boundary matters because the local proxy already needed a patch for Claude Code system-message content. That patch normalized text-block system content for a ChatGPT Responses backend. It is a reminder that payload shape matters.

## Boundary 3: HTTP reachability from the sandbox

If the demo runs in a container, `localhost` inside the container is not the host's `localhost`. A failed request to `http://localhost:11435` from inside the container may mean the container is calling itself, not the host proxy.

Record the actual route:

```text
Host OS:
Container runtime:
Proxy host path from container:
Resolved address:
Port reachable:
TLS/plain HTTP:
```

If networking fails, do not call it an Anthropic/LiteLLM compatibility failure. Fix networking, then rerun the same request.

Possible routes include:

- `host.docker.internal` if available;
- host networking where appropriate;
- an explicit host LAN IP;
- a local reverse proxy;
- a tunnel only if necessary and only with constrained keys.

The safest route is still the least exposed route that works.

## Boundary 4: LiteLLM incoming request

Once the request reaches LiteLLM, capture what LiteLLM thinks it received:

- model;
- route;
- endpoint path;
- headers passed through;
- tools present;
- dropped parameters;
- warnings;
- request ID;
- virtual key attribution.

LiteLLM's Claude Code docs describe both a unified endpoint and provider-specific Anthropic pass-through endpoint ([LiteLLM Claude Code quickstart](https://docs.litellm.ai/docs/tutorials/claude_responses_api)). If one endpoint path fails, testing the other may be useful, but only after recording the first failure.

The incoming request should still look Anthropic-like at this boundary. If the beta header or computer tool is already gone, the failure is before or at LiteLLM ingress.

## Boundary 5: LiteLLM provider transformation

This is the central unknown. LiteLLM can translate requests to non-Anthropic providers for Claude Code ([LiteLLM non-Anthropic models](https://docs.litellm.ai/docs/tutorials/claude_non_anthropic_models)), but the research did not find evidence that the special computer-use beta request transforms cleanly to a `chatgpt/` Responses backend.

Questions to answer:

- Does LiteLLM preserve the `computer_20251124` tool at all?
- Does it convert it into an OpenAI Responses tool?
- Does it reject it because no schema exists?
- Does `drop_params` silently remove fields?
- Does the backend request include screenshots or display metadata in a meaningful way?
- Does the backend request contain enough information for the model to choose actions?

If the transformed backend request cannot represent a computer-use tool, then the backend cannot produce a valid Anthropic computer-use loop without additional shim work.

## Boundary 6: backend response

The backend can fail in several ways:

```text
HTTP error
provider error message
normal text answer
provider-native tool call
malformed tool call
valid tool call but wrong schema
empty response
safety refusal
```

A normal text answer is not a useless result. It tells you the backend understood the user task as a conversation, not as a computer-use tool contract.

A provider-native tool call is more interesting. It may suggest that a custom adapter could map provider-native actions into Anthropic `tool_use` blocks. But until that adapter exists and the loop works, the result should be marked partial, not pass.

## Boundary 7: LiteLLM response transformation

If the backend emits any tool-like structure, LiteLLM must transform it back into Anthropic Messages content. The demo loop expects a particular shape: a response with a `tool_use` stop reason and content blocks it knows how to evaluate.

Capture:

- final response status;
- final JSON body;
- stop reason;
- content block types;
- tool names;
- tool input shape;
- any LiteLLM transformation warnings.

If the final response is valid JSON but the demo parser rejects it, the boundary is response-shape compatibility, not necessarily model capability.

## Boundary 8: tool execution

If a valid `tool_use` block reaches the demo, the problem shifts to the executor. Does the requested action map to a supported action? Does screenshot return the right media type? Does click coordinate scaling match the display size? Does keyboard input work?

Anthropic's docs emphasize that the application executes the tool in a VM/container and returns results; Claude does not directly operate the environment ([Anthropic computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)). That means tool-executor bugs are part of the app, not the model.

Useful executor logs:

```text
tool name
tool input
action attempted
screen size
action result
screenshot captured
error text
next message sent to model
```

## Boundary 9: loop continuation

A single tool request is not the whole experiment. The loop must continue after a `tool_result`. Many adapters work on the first request but fail when a tool result containing screenshot data is sent back.

The second turn tests:

- whether tool results are accepted;
- whether image/screenshot content is preserved;
- whether the model can reason from the returned screenshot;
- whether stop reasons remain correct;
- whether the final answer is emitted.

A pass requires at least one complete action/result/follow-up cycle.

## Minimal debug packet

For a failed run, save a redacted packet with:

```text
control run summary
proxy run summary
route settings
request headers, redacted
request body, redacted if needed
LiteLLM warnings
backend error or response
final response body
demo parser error
tool executor logs if reached
classification of boundary
```

Do not commit bulky raw logs or secrets. Keep raw artifacts under `tmp/` and summarize durable findings in the decision log.

## Classification labels

Use consistent labels:

- `network-unreachable`
- `auth-failed`
- `model-alias-missing`
- `beta-header-rejected`
- `tool-definition-rejected`
- `tool-definition-dropped`
- `backend-text-only`
- `backend-provider-tool-shape`
- `anthropic-response-shape-invalid`
- `demo-parser-failed`
- `executor-failed`
- `loop-continuation-failed`
- `security-stop`
- `pass-minimal-loop`

These labels make later refreshes and fixes easier.

## Debugging principle

Never fix a boundary you have not observed. If the model returns text, do not start editing the executor. If the request never reaches LiteLLM, do not patch the Anthropic bridge. If Desktop cannot reach localhost, do not conclude anything about computer-use tools.

The value of the experiment is the boundary map. A green run is great, but a precisely classified failure is almost as useful.
