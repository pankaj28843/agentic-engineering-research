# 03. Claude Desktop and Cowork through LiteLLM

Claude Desktop/Cowork through LiteLLM is the cleanest near-term experiment because it matches a documented product path. It should be tested as a text-inference routing experiment first.

LiteLLM's Claude Desktop integration page says the purpose is to route Claude Desktop requests through LiteLLM Proxy for unified logging, budget controls, and access to any model. The quick reference is a Gateway URL and a LiteLLM virtual key. The documented UI path is: enable Developer Mode, open Configure Third-Party Inference, enter the LiteLLM Proxy URL, paste a virtual key, save, restart Claude Desktop, and verify requests in the LiteLLM Dashboard Usage view ([LiteLLM Claude Desktop integration](https://docs.litellm.ai/docs/tutorials/claude_desktop_cowork)).

That is enough evidence to try it. It is not enough evidence to skip a careful validation plan.

## What the Desktop experiment should answer

The first Desktop experiment should answer only these questions:

1. Can Claude Desktop reach the local LiteLLM gateway?
2. Does it accept a LiteLLM virtual key?
3. Does it send traffic that LiteLLM logs and attributes correctly?
4. Does a normal chat response come back?
5. Does the model route match the intended alias?

If all five pass, Desktop 3P text inference is working. That is valuable on its own. It means Desktop can become another client of the local model-routing lab, with usage logging and budget controls.

## What it should not answer yet

The Desktop experiment should not be used to decide whether Anthropic computer use works through LiteLLM.

Claude Desktop third-party inference is a client routing feature. Anthropic computer use is an API/tool-loop feature. The computer-use docs describe a loop where Claude emits tool-use requests, your application executes those requests in a sandbox, and your application returns results ([Anthropic computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)). The LiteLLM Desktop/Cowork page does not say that Claude Desktop exposes that loop through third-party inference.

So the right conclusion from a successful Desktop test is:

```text
Claude Desktop text requests can route through LiteLLM.
```

The wrong conclusion is:

```text
Claude computer use works through LiteLLM.
```

## Gateway URL uncertainty

The local proxy is on `http://localhost:11435`. LiteLLM's Desktop page shows a placeholder Gateway URL like `https://your-litellm-proxy.com` ([LiteLLM Claude Desktop integration](https://docs.litellm.ai/docs/tutorials/claude_desktop_cowork)). That does not prove local HTTP is rejected. It only means the docs are written for a general hosted proxy.

The experiment should record the exact Desktop behavior for:

- `http://localhost:11435`
- possibly `http://127.0.0.1:11435`
- a machine LAN address if Desktop cannot resolve the same localhost
- HTTPS/public tunnel only if needed and only with a constrained key

Do not widen network exposure just to make the test pass quickly. A local gateway plus broad key is lower risk than a public gateway plus broad key, but a local gateway plus constrained key is better than both.

## Virtual key preference

LiteLLM's Desktop docs say to get a virtual API key from the LiteLLM Dashboard, using Virtual Keys -> Create New Key, then paste that key into Desktop ([LiteLLM Claude Desktop integration](https://docs.litellm.ai/docs/tutorials/claude_desktop_cowork)). That is the right default for the experiment.

The current Claude Code setup can use an API-key helper and may have access to broad model routes. Desktop should not inherit more access than it needs. A good virtual key should be limited to:

- one or two text aliases needed for the Desktop run;
- a small spend cap or budget if LiteLLM supports it locally;
- logging/usage attribution;
- easy revocation after the experiment.

If a virtual key is not available, document that as a risk. Do not silently paste a master key into a persistent desktop app without noting the blast radius.

## Model alias expectations

The Desktop app may not expose the same model-selection behavior as Claude Code. Claude Code can be launched with explicit model names or environment defaults. Desktop third-party inference may use the configured gateway differently.

The test should record:

- which model Desktop asks for;
- whether LiteLLM remaps it;
- whether the request hits `chatgpt/gpt-5.5` or another alias;
- whether any default model variables matter;
- whether usage logs show the requested model or backend model.

This matters because the local proxy uses direct `chatgpt/` model names. If Desktop sends a native Claude model name and the proxy has no alias for it, the request may fail even though the gateway and key are correct.

## A safe Desktop validation script

Use a tiny prompt. The goal is not to benchmark model quality. It is to prove plumbing.

A good prompt:

```text
Reply with exactly: desktop route ok
```

Then record:

```text
Desktop input accepted: yes/no
Response exact enough: yes/no
LiteLLM usage log visible: yes/no
Virtual key attribution: yes/no
Model alias seen: <alias>
Any proxy warnings/errors: <summary>
```

If it works, run one slightly longer prompt that checks multi-turn state. If it fails, capture the error text and proxy logs before changing anything.

## Failure classes

Most Desktop failures will fall into one of these buckets:

- **Reachability:** Desktop cannot connect to `localhost:11435`.
- **Protocol:** Desktop rejects plain HTTP, path shape, or gateway response.
- **Authentication:** key format or virtual key setup is wrong.
- **Model alias:** Desktop asks for a model LiteLLM does not expose.
- **Backend:** LiteLLM reaches the backend but the ChatGPT route rejects the transformed payload.
- **Logging:** response succeeds but usage attribution is missing.

Do not fix these by changing multiple variables at once. Change one thing, retest, and update the decision log.

## Why this is still worthwhile without computer use

A working Desktop 3P text route is useful even if computer use never works through the ChatGPT-backed proxy. It gives the user another interface to the same model-routing layer, with LiteLLM logging and budget controls. It can also test whether Desktop's UX is good enough for non-code planning, research synthesis, or chat-heavy tasks while keeping local routing consistent.

The key is to keep the success label honest: **Claude Desktop text inference through LiteLLM**, not **Claude computer use through LiteLLM**.
