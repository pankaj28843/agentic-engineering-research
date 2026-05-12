# 05. Control first: running the official computer-use demo

The official Anthropic computer-use demo should be treated as a control experiment. A control is not busywork. It tells you whether the basic environment works before you add the local LiteLLM/ChatGPT translation layer.

The Anthropic Quickstarts repository lists a Computer Use Demo as an environment and tools that Claude can use to control a desktop computer. The top-level README says it supports the latest `computer_use_20251124` tool version with zoom actions ([Claude Quickstarts](https://github.com/anthropics/anthropic-quickstarts)). Anthropic's computer-use docs also describe a reference implementation with a web interface, Docker container, example tool implementations, and an agent loop ([Anthropic computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)).

That is the right first computer-use run.

## Why the control matters

Without the control, a failed proxy-adapted demo can mean too many things:

- Docker cannot run the desktop.
- VNC/noVNC display wiring is broken.
- The browser inside the sandbox cannot start.
- The model route is wrong.
- The beta header is missing.
- LiteLLM strips a field.
- The backend cannot emit computer-use tool calls.
- The agent loop code expects a native Anthropic response and gets a translated response.
- The task is unsafe and gets blocked.

The control run removes many of those variables. If the official demo works with a real compatible Claude backend, then the environment, display, tool implementation, and loop are basically valid. The proxy adaptation can then focus on request/response compatibility.

## What the control should use

Use the smallest possible isolated setup:

- official quickstart code;
- real Anthropic API credentials or another officially supported provider path;
- Docker/container isolation;
- no host home directory mount;
- no real browser profile;
- no password manager;
- no production accounts;
- low-stakes local task;
- screen size close to the documented/reference setup.

Anthropic's docs emphasize dedicated virtual machines or containers, minimal privileges, avoiding sensitive data, domain allowlists, and human confirmation for consequential actions ([Anthropic computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)). Those are not optional niceties for the first run. They are part of making the result trustworthy.

## A good first task

Do not start with the open internet. Do not ask the agent to log into anything. Do not ask it to download files. Do not ask it to use credentials.

A good first task:

```text
Open the text editor, type "computer use control ok", take a screenshot, and stop.
```

A slightly richer second task:

```text
Open the browser to a local static HTML file in the container, click the button labeled Continue, and report the final page text.
```

The first task checks desktop visibility and typing. The second checks browser navigation and clicking without internet prompt-injection exposure.

## What to record

The control run should produce a small evidence ledger:

```text
Date/time:
Demo version/commit:
Model:
Beta header:
Tool version:
Container runtime:
Display resolution:
Ports exposed:
Task prompt:
Observed tool_use: yes/no
Screenshot returned: yes/no
Click/type worked: yes/no
Final response:
Errors/warnings:
```

The exact model and beta header matter because Anthropic lists different header versions for different model families ([Anthropic computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)). A later proxy test should use the closest possible request shape.

## What not to change in the control

Do not point the control run at `localhost:11435` yet. Do not edit the SDK base URL. Do not add LiteLLM-specific patches. Do not swap providers. Do not add a custom browser profile. Do not mount real files. Do not make the first task depend on network access.

A control run is valuable precisely because it is boring and close to official instructions.

## When the control fails

If the control fails, fix the control before touching LiteLLM. The failure is probably in one of these areas:

- credentials;
- model/version mismatch;
- beta header mismatch;
- Docker runtime;
- display server;
- browser startup;
- web UI port exposure;
- host networking;
- local permissions.

Those failures are still useful, but they are not evidence against LiteLLM. They are evidence that the computer-use environment is not ready.

## When the control passes

When the control passes, freeze the working configuration. Record the working model, header, tool version, demo commit, and task. That becomes the comparison target for the proxy-adapted run.

The proxy-adapted experiment should change as little as possible:

- same prompt;
- same sandbox;
- same display resolution;
- same tool implementation;
- same agent loop structure;
- only the base URL, auth token, and model alias change.

That discipline is what makes a later failure actionable.

## Why this is also a safety rehearsal

The control run is where the team practices not giving the agent too much authority. The ZombAIs report showed a computer-use host being induced by webpage content to download and execute a binary in an educational security demo ([ZombAIs](https://embracethered.com/blog/posts/2024/claude-computer-use-c2-the-zombais/)). The first control task should not expose the agent to that class of input.

Once the local loop is trusted, later tests can add internet access behind an allowlist and human confirmation. But the first goal is to prove the loop, not stress the safety boundary.

## Control pass criteria

The control is green when:

```text
The official demo starts.
The desktop view is visible.
Claude emits a computer-use tool request.
The sandbox executes screenshot/click/type actions.
The agent loop returns tool results correctly.
A trivial task completes.
No sensitive host data is exposed.
```

Only then is it time to test the local LiteLLM proxy adaptation.
