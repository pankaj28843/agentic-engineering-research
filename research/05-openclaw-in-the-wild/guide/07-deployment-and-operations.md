# Deployment and Operations

## Always-on assistants are infrastructure

OpenClaw becomes more serious when it runs beyond a one-off local demo. An assistant that receives messages, controls a browser, reads files, manages calendars, and calls skills is infrastructure. It has ports, tokens, storage, logs, dependencies, process supervisors, browser profiles, and network boundaries. The public evidence shows practitioners wrestling with exactly this layer.

The strongest deployment artifact is [aws-samples/sample-host-openclaw-on-amazon-bedrock-agentcore](https://github.com/aws-samples/sample-host-openclaw-on-amazon-bedrock-agentcore). The captured repository page showed a multi-folder sample with CDK, Lambda, bridge code, tests, red-team material, docs, skills, browser support, guardrails, Telegram UX, Slack/Telegram routing, workspace persistence, AgentCore session storage, and browser IDs. This is not merely an install snippet. It is an attempt to host OpenClaw as a managed, isolated application substrate.

Other deployment artifacts include [openclaw/nix-openclaw](https://github.com/openclaw/nix-openclaw), [openclaw/openclaw-ansible](https://github.com/openclaw/openclaw-ansible), Docker images, Home Assistant add-ons, Android/Termux packaging, and Chinese Docker bundles for IM platforms. Together they show a practical demand: people want OpenClaw to be reproducible, remote, persistent, and available from the devices and channels they already use.

## Non-interactive setup and agents

The official [CLI automation docs](https://docs.openclaw.ai/start/wizard-cli-automation) are important because serious deployments cannot depend only on an interactive wizard. The docs show `openclaw onboard --non-interactive` with flags for local mode, API-key auth choices, secret input mode, gateway port, gateway bind, daemon installation, daemon runtime, and skill skipping. They also show provider-specific variants for Gemini, Z.AI, Vercel AI Gateway, Cloudflare AI Gateway, Moonshot, Mistral, OpenCode, Ollama, and custom providers.

The same page shows adding another agent with a separate workspace and channel binding:

```bash
openclaw agents add work   --workspace ~/.openclaw/workspace-work   --model openai/gpt-5.2   --bind whatsapp:biz   --non-interactive   --json
```

That command reveals the operational model. A deployment can have multiple agents, each with its own workspace and bindings. In practice, this means practitioners should think about agent boundaries. A personal finance agent, a work agent, a home automation agent, and a coding agent should not necessarily share the same workspace, memory, tools, or channel permissions.

## Nix, Ansible, and reproducibility

[nix-openclaw](https://github.com/openclaw/nix-openclaw) and [openclaw-ansible](https://github.com/openclaw/openclaw-ansible) represent two complementary approaches. Nix emphasizes reproducible packages and configuration. Ansible emphasizes automated setup and hardening, including ideas such as Tailscale VPN, UFW firewall, and Docker isolation. These projects matter because agent systems are hard to reconstruct by memory. If a personal assistant becomes useful, losing its exact configuration becomes painful.

A reproducible OpenClaw setup should record the OpenClaw version, model providers, gateway port and bind address, channel plugins, browser profiles, skill list, workspace paths, secrets strategy, and backup paths. It should avoid committing raw API keys. It should include a restore path. It should define how to update OpenClaw and how to roll back if a new version breaks a workflow.

This is boring infrastructure work, but it is what separates a weekend demo from a dependable assistant.

## Cloud and sandboxed deployments

The AWS Bedrock AgentCore sample is especially useful because it shows how OpenClaw might run in a managed cloud context. The public repo signals microVM/session isolation, workspace sync, custom skills, guardrails, browser enablement, file storage, cron scheduling, and chat routing. Those are exactly the concerns an organization would have before exposing an agent to users.

Cloud hosting changes the tradeoffs. It can improve availability and isolation, but it can make local browser access, local files, and personal session state harder. A cloud OpenClaw may need a node host for browser actions on a user's machine, a remote CDP provider, or explicit upload/download flows. It also needs identity and per-user state boundaries. If multiple users share one gateway, the system must prevent cross-user memory or file leakage.

A practical cloud deployment should start with one user or one team, not a broad open service. It should log tool calls, constrain skills, define where files are stored, and test guardrails with red-team cases. The AWS sample's inclusion of red-team and guardrail-related material is a positive signal because agent deployments need adversarial thinking from the start.

## Home Assistant and edge devices

[ngutman/openclaw-ha-addon](https://github.com/ngutman/openclaw-ha-addon) and [joshp123/gohome](https://github.com/joshp123/gohome) point to a different deployment environment: the home. Home deployments need persistence, local network access, and low maintenance. They may run on a Raspberry Pi, Home Assistant OS, a NAS, or a spare machine. They also control physical devices, so failure can have real-world consequences.

For home deployments, the safest design is layered. Home Assistant or another automation system remains the canonical device-control layer. OpenClaw becomes the natural-language interface and planner. It can ask Home Assistant for state, propose automations, or trigger safe predefined actions. It should not invent arbitrary low-level device commands without constraints.

The same principle applies to 3D printers, vacuums, cameras, and air purifiers. OpenClaw should route intent to a narrow skill with device-specific guardrails. A vacuum skill can clean a named room. A 3D printer skill can report status or pause a job. A camera skill can capture an image. The narrower the operation, the easier it is to trust.

## Docker, Android, and portability

GitHub search found Docker-oriented projects, Android/Termux packaging, and platform-specific installers. These are evidence that users want OpenClaw in unusual places: servers, home devices, mobile devices, and local app stacks. Portability increases reach, but it also multiplies failure modes. Browser support in Docker may require Playwright browsers, persisted browser caches, display/headless choices, and network permissions. Android or Termux setups may lack assumptions that desktop OpenClaw expects.

The [browser docs](https://docs.openclaw.ai/tools/browser) explicitly note that some browser features require Playwright and that Docker setups should install browser binaries carefully. They also explain remote CDP and node host proxy patterns. This is where deployment and browser automation meet: an always-on assistant needs a browser somewhere, but that somewhere might not be the gateway container.

## Operational checklist

A serious OpenClaw deployment should answer these questions before being trusted.

Where does the gateway bind: loopback, LAN, tailnet, or public internet? What token or password protects it? Where are API keys stored? Which channels can reach which agents? Which skills can read files, send messages, control browsers, or call external services? Which browser profile is the default? Are remote CDP URLs treated as secrets? How are workspaces backed up? How are logs retained? How are updates tested? How does the user stop the agent quickly?

If these questions feel excessive, the workflow is probably still a toy. If the assistant can send messages, place orders, update calendars, or control devices, these questions are the minimum.

## The operations lesson

OpenClaw's public ecosystem is not only about cool demos. It already contains deployment recipes, hardening attempts, cloud samples, package managers, channel plugins, and setup issues. That means practitioners should treat operational design as part of the product, not an afterthought. The best OpenClaw workflow is one that still works after reboot, update, expired login, model outage, and user correction.
