# 09. Security model and safe experiment harness

Computer-use experiments should be treated as security experiments. A model that can see a screen, click buttons, type text, browse the web, and run commands can also be tricked into doing harmful things.

Anthropic's docs are explicit about this. They say computer use has unique risks, especially when interacting with the internet, and recommend a dedicated virtual machine or container with minimal privileges, avoiding sensitive data, limiting internet access to allowlisted domains, and asking humans to confirm consequential actions ([Anthropic computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)).

The ZombAIs writeup shows what can go wrong. In an educational demo, webpage prompt injection led a Claude computer-use host to download a file, find it, `chmod +x` it, and execute it, resulting in a command-and-control connection ([ZombAIs](https://embracethered.com/blog/posts/2024/claude-computer-use-c2-the-zombais/)). That is the threat model in one story.

## Threat model

The main threats are:

1. **Prompt injection from webpages or images.** The agent reads hostile instructions embedded in content.
2. **Credential exposure.** The agent sees passwords, tokens, browser sessions, or private files.
3. **Unwanted action.** The agent clicks, submits, buys, deletes, sends, or agrees to something.
4. **Code execution.** The agent downloads, writes, compiles, chmods, or runs code.
5. **Network abuse.** The agent contacts untrusted services or exfiltrates data.
6. **Host escape by configuration.** The sandbox has host mounts, secrets, or privileges that make escape unnecessary.
7. **Human interruption failure.** The user cannot see, pause, or stop what the agent is doing.

For this project, the biggest practical risk is not a sophisticated sandbox escape. It is accidentally giving the agent the user's real browser profile, real downloads folder, real shell credentials, or unrestricted network.

## Safe default environment

The safe default is a disposable desktop environment:

```text
No host home directory mounted.
No password manager.
No personal Chrome/Firefox profile.
No SSH keys.
No cloud credentials.
No production accounts.
No real email/messaging sessions.
No broad filesystem access.
Network disabled or allowlisted.
Human can watch and stop the run.
```

Anthropic recommends dedicated VMs or containers with minimal privileges and avoiding sensitive data ([Anthropic computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)). That recommendation should apply to the official demo, the LiteLLM-adapted demo, and open-source stacks.

## Network rules

The first control run should not need the open internet. It can use a local app or local static HTML page. Once the loop works, add network carefully.

A staged network plan:

1. No network.
2. Localhost only.
3. Allowlisted documentation domains.
4. One disposable login if absolutely needed.
5. Never production accounts during compatibility testing.

If the goal is to test prompt-injection handling, create a synthetic hostile page in a disposable environment. Do not use real malware, real command-and-control, or unauthorized systems. The ZombAIs article is useful evidence of risk; it is not an instruction to reproduce harmful behavior ([ZombAIs](https://embracethered.com/blog/posts/2024/claude-computer-use-c2-the-zombais/)).

## Human confirmation

Anthropic recommends human confirmation for decisions with meaningful real-world consequences and tasks requiring affirmative consent, such as accepting cookies, executing financial transactions, or agreeing to terms of service ([Anthropic computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)).

For the lab, require confirmation before:

- downloading a file from the internet;
- running any downloaded file;
- running shell commands that modify permissions;
- submitting a form;
- logging into an account;
- sending messages;
- deleting files;
- making purchases;
- changing settings outside the sandbox.

The first experiments should avoid these actions entirely.

## Key management

Claude Desktop/Cowork should use a LiteLLM virtual key if available, because the LiteLLM Desktop docs explicitly frame the setup around a virtual key ([LiteLLM Claude Desktop integration](https://docs.litellm.ai/docs/tutorials/claude_desktop_cowork)). The key should be limited, attributed, and revocable.

Computer-use experiments should use the narrowest possible key:

- one model alias;
- low budget;
- short lifetime if supported;
- logging enabled;
- no unrelated high-value routes;
- no secrets copied into durable research files.

The local Claude Code setup's `apiKeyHelper` pattern is good because it avoids embedding secrets in config snapshots. Keep that discipline.

## Filesystem rules

Do not mount the user's real home directory into the computer-use container. If files are needed, create a disposable directory with synthetic files.

Good mounts:

```text
tmp/computer-use-sandbox/input/
tmp/computer-use-sandbox/output/
```

Bad mounts:

```text
/home/user/
~/.ssh/
~/.config/google-chrome/
~/Downloads/
project root with real secrets
```

If a task needs a file, copy a redacted fixture into the sandbox input directory. If the agent creates output, copy it out after review.

## Browser profile rules

Never use the user's real browser profile for computer-use compatibility tests. A real profile contains cookies, sessions, autofill, browsing history, extensions, and sometimes password-manager integration.

For web tasks, use:

- the official demo's default browser profile;
- a disposable profile created inside the sandbox;
- a local test page;
- synthetic accounts only.

This is stricter than normal browser automation because computer use can read the screen and make arbitrary UI choices.

## Logging and replay

A computer-use run should be auditable. Record:

- prompt;
- model and route;
- tool calls;
- screenshots if safe;
- shell commands;
- clicked coordinates or UI element IDs;
- final response;
- whether a human approved any action.

Open-source stacks such as `trycua/cua` emphasize trajectory recording and benchmark tooling ([trycua/cua](https://github.com/trycua/cua)). That is a good design direction: if a desktop agent makes a surprising move, you need enough evidence to diagnose it.

## Stop conditions

Stop the run immediately if:

- the agent tries to access real credentials;
- the agent tries to download and run a file;
- the agent navigates outside the allowlist;
- the agent requests host filesystem access;
- the agent tries to send a message or submit a form unexpectedly;
- the sandbox boundary is unclear;
- the human cannot see or interrupt the run.

A stopped run is not a failure. It is a successful safety boundary.

## Security checklist

Before a computer-use run:

```text
Sandbox disposable: yes/no
Host home mounted: no
Real browser profile mounted: no
Secrets present: no
Network policy known: yes/no
Key constrained: yes/no
Task low stakes: yes/no
Human can observe: yes/no
Human can stop: yes/no
Logs captured: yes/no
```

If any answer is wrong, do not run the experiment yet.

## The security takeaway

The goal is not to make the model more obedient. The goal is to make the environment safe when the model is wrong, confused, or manipulated. For computer use, the harness is the security boundary.
