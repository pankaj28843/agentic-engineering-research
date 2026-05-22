# Security and Privacy

## The threat model starts with usefulness

OpenClaw is risky for the same reason it is useful. It connects an agent to channels, skills, browsers, files, calendars, local tools, and remote services. A system that can read messages, control a browser, upload files, post to chat, and run skills is not a normal chatbot. It is a control plane. The public evidence includes serious operational artifacts, such as [openclaw-ansible](https://github.com/openclaw/openclaw-ansible), [nix-openclaw](https://github.com/openclaw/nix-openclaw), and the [AWS Bedrock AgentCore sample](https://github.com/aws-samples/sample-host-openclaw-on-amazon-bedrock-agentcore), because practitioners quickly discover that deployment and safety matter.

The first security lesson is to scope the assistant by workflow, not by ambition. A general personal assistant with access to every account is hard to reason about. A PR-review assistant with read-only GitHub access and Telegram DM output is much easier. A calendar assistant that drafts updates is easier than one that can reschedule meetings automatically. A browser assistant that uses an isolated profile is safer than one attached to the user's daily browser.

## Gateway exposure

The [browser documentation](https://docs.openclaw.ai/tools/browser) notes that browser control is loopback-only and routes through Gateway auth or node pairing. That is the right default. A gateway that can trigger tools should not be casually exposed to the public internet. Use loopback for local-only setups. Use a private network such as a tailnet for remote access. If public exposure is unavoidable, put strong authentication, rate limits, logging, and narrow skills in front of it.

Gateway tokens and passwords are powerful. If a token can send messages to the agent, invoke tools, or reach browser routes, treat it like an application secret. Do not paste it into screenshots, issue bodies, or committed config. Rotate it if exposed. Prefer environment references or file-backed secret stores over inline plaintext when possible.

## Browser profile risk

Browser profiles are permission scopes. The `openclaw` profile is intended as an isolated agent browser. The `user` profile attaches to a real signed-in Chrome session through Chrome DevTools MCP. Remote CDP profiles connect to local or hosted browser endpoints. Each profile implies different access.

The isolated profile should be the default for public browsing, testing, and low-risk automation. It can hold only the cookies needed for a workflow. The signed-in user profile should be rare and explicit. It may contain banking, email, admin dashboards, personal messages, cloud consoles, and social accounts. The docs note that existing-session attach requires user approval and that this path is higher risk. Practitioners should treat it like giving a contractor access to their unlocked computer.

Remote CDP endpoints are also sensitive. A Browserless or Browserbase-style token can expose a full browser session. Store it as a secret. Prefer HTTPS or WSS. Avoid long-lived tokens in config. If a workflow uses remote CDP, log which profile and endpoint were used so mistakes are traceable.

## Prompt injection and page content

Browser automation introduces prompt injection from web pages. A page can contain text that tells the agent to ignore instructions, reveal secrets, click a button, or send data elsewhere. The OpenClaw docs warn that browser `evaluate` and wait predicates execute JavaScript in the page context and can be disabled with `browser.evaluateEnabled=false`. That is a useful hardening knob. If a workflow does not need arbitrary page JS, disable it.

Even without JS evaluation, page text can manipulate an agent. A safe browser workflow distinguishes data from instruction. The page content is evidence to inspect, not authority to obey. If a page says, send your token to this URL, the agent should not comply. If a page includes hidden text or malicious labels, the workflow should rely on scoped skills and confirmation gates rather than free-form obedience.

## SSRF and network boundaries

The browser docs describe SSRF policy controls, including private-network restrictions and allowlists. This matters because a browser controlled by an agent can request internal URLs. If the gateway runs on a network with admin panels, metadata services, local dashboards, or private APIs, a malicious prompt could try to route the browser there. Strict SSRF policy and hostname allowlists reduce that risk.

Practitioners often think of SSRF as a server-side web vulnerability, but agentic browsers recreate the risk in a new form. The agent can be induced to navigate. The browser can see internal pages. Screenshots or page text can leak content. Therefore a workflow that browses untrusted pages should not have unrestricted access to private network destinations.

## Skills and least privilege

Skills are OpenClaw's extension unit, but each skill should have a narrow contract. A skill that can list calendar events is safer than one that can read and write every calendar. A skill that uploads one selected file to R2 is safer than one that can browse the whole filesystem. A skill that reports Home Assistant state is safer than one that can call arbitrary service actions.

Skill catalogs such as [ClawHub](https://github.com/openclaw/clawhub) and [VoltAgent/awesome-openclaw-skills](https://github.com/VoltAgent/awesome-openclaw-skills) are useful discovery tools, but every third-party skill should be reviewed before installation. Check what commands it runs, what files it reads, what network endpoints it calls, how it handles secrets, and whether it has tests or issue history. Popularity is not a sandbox.

Domain-specific skills need extra caution. [OpenClaw Medical Skills](https://github.com/FreedomIntelligence/OpenClaw-Medical-Skills) may be useful for organization or information retrieval, but medical domains require professional boundaries. Health, finance, legal, hiring, and safety-critical workflows should default to advice-preparation and summarization, not autonomous decisions.

## Logs, memory, and retention

OpenClaw workflows can create sensitive logs. A chat request may include private data. A browser screenshot may include account details. A tool call may include a file path or token. A memory workflow may transform personal history into summaries. If logs are retained indefinitely, the assistant becomes a data lake.

Define retention early. What logs are kept? Where? For how long? Who can read them? Are screenshots stored? Are transcripts stored? Are failed tool calls stored? Can the user delete memory? Can the user inspect derived beliefs? A personal assistant that cannot forget is not personal; it is a liability.

## Human approval as a security control

Human-in-the-loop is not only a UX choice. It is a security control. Approval gates protect against prompt injection, mistaken identity, stale data, and tool bugs. The approval message should be specific: what will be done, where, under which account, and what the consequence is. Asking approve? after a long hidden chain is not enough.

Use approval for purchases, bookings, public posts, message sends, file deletion, permission changes, device control, health/finance/legal actions, and any action that affects other people. Over time, narrow low-risk actions can become automatic, but only after logs show they are reliable.

## Security posture for first deployment

A safe first OpenClaw deployment uses loopback or tailnet access, one channel, one agent workspace, one model provider, one skill, and the isolated browser profile. It stores secrets outside committed config, logs tool calls, and requires confirmation for external writes. It avoids the signed-in browser profile until needed. It has a documented stop path. It has backup and restore for any useful state.

This posture may sound conservative, but it is how a powerful assistant earns trust. Expand after evidence. Add channels, skills, browser profiles, and autonomy one at a time. Each expansion should come with a new threat model.
