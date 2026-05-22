# Practitioner Playbook

## Pick the first workflow by pain, not novelty

The public OpenClaw ecosystem is tempting because it contains many shiny examples: shopping autopilots, PR reviews in Telegram, health assistants, 3D printers, browser control, multi-agent swarms, and voice bridges. A practitioner should ignore most of them at first. Pick one workflow that is repeated, annoying, bounded, and easy to verify.

A good first workflow has four traits. It starts from a channel you already use. It calls one stable tool, skill, CLI, or browser task. It produces an inspectable result. It has low blast radius if it fails. Examples: summarize a PR and DM it to Telegram; read today's calendar and draft a morning briefing; convert a screenshot to Markdown; list Linear issues matching a query; check padel court availability; transcribe a voice note; search bookmarks semantically.

A poor first workflow is broad and irreversible: manage all my messages, run my whole day, buy groceries without confirmation, trade based on charts, control every home device, or autonomously merge PRs. Those may become possible later, but they are bad starting points.

## Choose the right integration surface

Use the narrowest reliable interface. If a service has an API, use a skill or CLI. If it has a local app API, wrap that. If it has no API but the task is visible in a web UI, use browser automation. If the task is naturally expressed in chat, expose it through a channel connector. If the task needs long-running state, give it a dedicated workspace.

This ordering comes directly from the evidence. [Linear CLI](https://github.com/Finesssee/linear-cli) and [Beeper CLI](https://github.com/blqke/beepcli) show the value of deterministic local commands. The [browser docs](https://docs.openclaw.ai/tools/browser) show how to use a browser when the UI is the only path. Channel plugins such as [DingTalk OpenClaw connector](https://github.com/DingTalk-Real-AI/dingtalk-openclaw-connector) show how chat becomes the entrypoint. Deployment artifacts such as [nix-openclaw](https://github.com/openclaw/nix-openclaw) and [openclaw-ansible](https://github.com/openclaw/openclaw-ansible) show how setup becomes reproducible.

## Build a thin first skill

A first skill should do less than you want. If the final dream is a personal finance assistant, start with read-only transaction categorization from a CSV. If the final dream is a shopping assistant, start by building a cart draft, not placing an order. If the final dream is Slack support, start by summarizing unanswered threads, not replying. If the final dream is home automation, start by reporting device state, not controlling devices.

The showcase's wine-cellar skill is a good pattern. The agent asks for a sample CSV and storage path, then builds and tests a local skill. This keeps the data shape visible. It also creates a reusable tool rather than relying on the agent to improvise every time. For many OpenClaw projects, the correct path is: one manual run, then a script, then a skill, then a chat command, then scheduling or automation.

## Add confirmation gates

Every workflow should have an action matrix. Read-only actions can run freely. Draft actions can run and ask for approval. External writes require confirmation. High-risk writes require confirmation plus a summary of consequences.

For example, a PR review workflow can read a diff and DM suggestions automatically. Posting a public PR comment requires approval. Approving or merging requires a stronger gate. A shopping workflow can search and build a cart automatically. Submitting the order requires confirmation. A calendar workflow can suggest reschedules. Sending invites or cancellations requires confirmation. A home workflow can report device state. Unlocking a door, starting machinery, or changing safety-related settings requires stricter controls or should be out of scope.

OpenClaw's power is that it can connect surfaces. Confirmation gates decide where that connection stops.

## Treat browser profiles as permissions

Browser profiles are not just technical settings. They are permission scopes. The isolated `openclaw` profile is a safer sandbox. The `user` profile has the user's real login state. Remote CDP profiles may expose cloud browsers or third-party browser providers. Existing-session attach requires user approval and should be used only when needed.

A practical setup might have separate profiles for public browsing, shopping, work dashboards, and experiments. Each profile should have the minimum login state needed. A workflow that only reads public docs should not use the user's signed-in browser. A workflow that books a delivery slot might need a shopping profile, but it should not share that profile with random web research.

## Make deployment boring

Use non-interactive setup where possible. Record versions. Keep secrets out of committed config. Bind gateways to loopback or a private network. Prefer Tailscale or similar private networking over public exposure. Back up workspaces. Log tool calls. Keep a stop command or process supervisor path. Test updates on a non-critical workflow first.

The official [CLI automation docs](https://docs.openclaw.ai/start/wizard-cli-automation) and deployment repositories such as [AWS AgentCore sample](https://github.com/aws-samples/sample-host-openclaw-on-amazon-bedrock-agentcore), [nix-openclaw](https://github.com/openclaw/nix-openclaw), and [openclaw-ansible](https://github.com/openclaw/openclaw-ansible) all point to the same lesson: if OpenClaw matters, automate its setup. Manual wizard state is fine for exploration. Durable assistants need reproducible infrastructure.

## Measure success with boring metrics

A workflow is working if it completes repeatedly, produces inspectable outputs, fails loudly, and saves human time. Track number of successful runs, number of confirmations, number of failures, average time saved, manual corrections, and near misses. For browser workflows, track login failures, CAPTCHA/bot-check events, stale refs, and final URL mismatches. For chat workflows, track duplicate messages, missed notifications, and wrong routing. For planner workflows, track stale data and rejected suggestions.

Do not measure success by how autonomous it feels on day one. Measure whether you still trust it after two weeks.

## Copyable starter projects

Starter one: PR review to Telegram. Trigger with a PR URL. OpenClaw reads the diff, runs the test command if available, summarizes high-confidence findings, and sends a private Telegram message. No public comments at first.

Starter two: calendar morning briefing. OpenClaw reads a CalDAV calendar and Todoist tasks, drafts a daily plan, cites sources, and asks before creating or moving anything.

Starter three: screenshot-to-Markdown. Use a tool like [SNAG](https://github.com/am-will/snag) or an OpenClaw skill to capture UI evidence and convert it into Markdown for bug reports, docs, or coding-agent prompts.

Starter four: Home Assistant status. OpenClaw reports device state and suggests actions. It does not control devices until the reporting workflow is stable.

Starter five: browser read-only monitor. OpenClaw opens a site in an isolated browser profile, extracts visible state, and reports changes. It does not click or submit until the observation path is reliable.

## When not to use OpenClaw

Do not use OpenClaw when a cron job, webhook, or simple script is enough. Do not use it for high-risk actions without confirmation and logging. Do not use browser automation when a stable API exists. Do not connect all personal accounts before you have one trusted workflow. Do not treat social showcase examples as operational proof.

OpenClaw is most valuable when human intent is fuzzy but the action boundary is clear. It is least valuable when both intent and action are vague.

## Final recommendation

Adopt OpenClaw like a power tool. Start with a small, useful cut. Wear safety glasses: isolated profiles, scoped secrets, private networking, logs, and confirmations. Keep the first workflows boring enough to trust. Then expand toward planner behavior, browser automation, and multi-agent orchestration only where the evidence from your own repeated runs says the system is ready.
