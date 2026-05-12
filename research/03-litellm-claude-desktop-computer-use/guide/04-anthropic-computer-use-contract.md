# 04. Anthropic computer use as a beta tool loop

Anthropic computer use is best understood as a contract between four things:

1. a compatible Claude model;
2. a beta API request with versioned tools;
3. an application loop that executes tool requests;
4. a sandboxed computer environment.

If any of those pieces is missing, there is no real Anthropic computer-use experiment.

## The API surface

Anthropic's docs say computer use is in beta and requires a beta header. For current Claude 4-family models, the documented header is `computer-use-2025-11-24`; for older supported models, the older `computer-use-2025-01-24` header is listed as deprecated ([Anthropic computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)).

The example request includes tools like:

```text
computer_20251124
text_editor_20250728
bash_20250124
```

The `computer_20251124` tool includes a display width, display height, and display number. That tells Claude what kind of screen it is operating. The API response can stop with `tool_use`, which means Claude is asking the application to perform an action.

This is different from ordinary function calling. The tool type is not just a JSON schema you invented for your application. It is a special versioned Anthropic tool type with beta semantics.

## The agent loop

The docs describe the core loop clearly:

1. Send Claude a prompt and the computer-use tools.
2. Claude decides whether to use a tool.
3. The API response has `stop_reason: tool_use`.
4. Your application extracts the tool name and input.
5. Your application executes the action inside a computer environment.
6. Your application sends a new message containing a `tool_result` block.
7. Claude either requests another tool or finishes with text.

Anthropic calls the repetition of steps 3 and 4 the agent loop ([Anthropic computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)).

That loop means Claude is not magically connected to a desktop. Claude sees screenshots and asks for actions. The application owns the dangerous part: clicks, typing, commands, screenshots, files, browser access, and network access.

## The computing environment

Anthropic says computer use requires a sandboxed computing environment. The reference setup includes a virtual display server, desktop environment, applications, tool implementations, and an agent loop. The docs mention a virtual X11 display using Xvfb, a lightweight desktop, preinstalled Linux applications, and a Docker container with port mappings for viewing and interacting with the environment ([Anthropic computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)).

That matters because a safe computer-use setup is not just a browser tab. It is a deliberately isolated machine-like environment that Claude can damage without damaging the user's real machine.

A good environment has:

- no password manager;
- no personal browser profile;
- no host home directory mount;
- no real SSH keys;
- no production credentials;
- a disposable filesystem;
- allowlisted network access if internet is needed;
- screen resolution close to the reference recommendation.

## Why the model backend matters

The backend model must know how to use the computer tool. The docs list compatible Claude models and tool versions. A backend that can answer Anthropic Messages text requests is not automatically a backend that can reason over screenshot/action loops or emit the special `computer_*` tool calls.

This is the central risk for the local LiteLLM proxy. The local backend route is a ChatGPT subscription Responses provider exposed through LiteLLM. LiteLLM can translate many request formats, and its docs explicitly describe using non-Anthropic models through Claude Code while maintaining the Anthropic Messages API shape ([LiteLLM non-Anthropic models](https://docs.litellm.ai/docs/tutorials/claude_non_anthropic_models)). But the computer-use contract includes special Anthropic beta tools and headers.

There are two separate questions:

```text
Can LiteLLM accept and forward the request shape?
Can the backend model produce the right Anthropic-style tool_use blocks?
```

Both must be true for the proxy-adapted loop to work.

## Security is part of the contract

Anthropic's docs treat security as a first-class part of computer use. They warn that the feature has unique risks, especially when interacting with the internet, and recommend dedicated VMs or containers, minimal privileges, avoiding sensitive data, limiting internet access, and asking a human to confirm consequential actions ([Anthropic computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)).

They also warn that Claude may follow commands found in content, such as webpages or images, even when those commands conflict with the user's instructions. That is prompt injection in a visual/action environment.

The ZombAIs writeup demonstrates why that warning should be taken literally. In that report, a malicious webpage caused a computer-use setup to download a file, locate it, change permissions with `chmod +x`, and execute it, producing a command-and-control connection in an educational security demonstration ([ZombAIs](https://embracethered.com/blog/posts/2024/claude-computer-use-c2-the-zombais/)).

This is not a reason to avoid all computer-use research. It is a reason to run it like a security experiment, not a convenience demo.

## What counts as a real pass

A real Anthropic computer-use pass is not "the model wrote some text about clicking." A pass means:

- the request includes the correct beta header;
- the model returns `stop_reason: tool_use`;
- the tool request is well formed;
- the sandbox executes the requested action;
- the sandbox returns screenshot/output results;
- the model continues or finishes correctly;
- the task is completed without escaping the sandbox or touching sensitive data.

A minimal pass can be very simple:

```text
Open the text editor in the sandbox, type hello, take a screenshot, and tell me when done.
```

That checks screenshot, click/type, and loop continuation without browsing the internet or touching accounts.

## What counts as a useful fail

A useful failure is one that identifies the broken contract boundary. Examples:

- The API rejects the beta header.
- LiteLLM strips the beta header.
- LiteLLM rejects `computer_20251124` because it expects a normal tool schema.
- The backend returns normal text instead of `tool_use`.
- The backend emits provider-native tool calls that the Anthropic loop cannot parse.
- The sandbox executes actions but screenshots are not returned in the expected format.
- The loop works until a prompt-injection classifier or safety confirmation step is triggered.

Those failures are all valuable if captured cleanly. They tell you whether the next step is a LiteLLM bridge patch, a different backend model, a different tool-loop adapter, or abandoning the proxy adaptation.

## The core takeaway

Anthropic computer use is not a Desktop setting. It is a beta model/tool/runtime contract. Validate it with the official control path first, then test whether the local LiteLLM proxy can preserve that contract. Do not infer success from ordinary text routing.
