# Use-Case Matrix

## Why a matrix helps

OpenClaw examples are easy to overgeneralize because they look like one broad category: personal AI assistant. A practitioner needs a more useful map. The important dimensions are not only domain names such as shopping, health, or coding. The important dimensions are trigger, action surface, data sensitivity, reversibility, and evidence quality.

A workflow triggered by a Telegram message that reads a public GitHub diff is very different from a workflow that attaches to a signed-in browser and buys groceries. A workflow that summarizes bookmarks is different from a workflow that posts to Slack. A workflow that controls a vacuum is different from one that controls a printer or unlocks a door. The public [OpenClaw Showcase](https://docs.openclaw.ai/start/showcase) mixes these examples together because it is showing breadth. A practitioner should separate them before copying.

## Messaging and notification workflows

This is the safest and most obvious entry category. OpenClaw receives a message, runs a tool, and returns a message. Examples include PR review to Telegram, Todoist skill generation in Telegram, Slack support notifications, voice-note delivery, and Beeper-style message management. Channel connector repositories such as [DingTalk-Real-AI/dingtalk-openclaw-connector](https://github.com/DingTalk-Real-AI/dingtalk-openclaw-connector), [larksuite/openclaw-lark](https://github.com/larksuite/openclaw-lark), and [freestylefly/openclaw-wechat](https://github.com/freestylefly/openclaw-wechat) show that this pattern is important across regions and workplace cultures.

The trigger is usually a human message or a channel event. The action surface is a channel API or local connector. The data sensitivity depends on the channel, but can be high because private messages and attachments may be involved. The reversibility is usually good for read-only summaries and poor for sent messages. Evidence quality is medium to high when a connector repo exists, medium when it is only a showcase post.

The best first implementation is read-only: summarize, classify, notify, or draft. The next step is controlled write: send a message only after confirmation. The dangerous version is autonomous reply across personal or company channels without review. A useful channel bot can become a social liability if it replies with the wrong tone or leaks context.

## Coding and engineering workflows

Coding workflows are appealing because developers can inspect artifacts and build guardrails. Examples include PR review to Telegram, Linear issue management, Codex session monitoring, screenshot-to-Markdown, multi-agent orchestration, and browser-based UI verification. [Finesssee/linear-cli](https://github.com/Finesssee/linear-cli), [am-will/snag](https://github.com/am-will/snag), and [adam91holt/orchestrated-ai-articles](https://github.com/adam91holt/orchestrated-ai-articles) are useful evidence because they expose a developer workflow shape rather than only a demo.

The trigger can be a PR, issue, chat command, terminal event, or scheduled check. The action surface can be GitHub, Linear, local files, a code agent, a browser, or chat. Data sensitivity is usually medium to high because source code and internal issues may be private. Reversibility depends on whether the workflow only reads or also comments, pushes, merges, or deploys. Evidence quality is high when the workflow has repo code and commands.

The best first implementation is a private summary loop: read diff, run tests, send findings. The next level is draft public comments or issue updates. The risky level is autonomous merging, deploying, or broad refactoring without human review. OpenClaw should reduce coordination overhead, not bypass engineering controls.

## Browser and web-task workflows

Browser workflows are for services without suitable APIs. Showcase examples include Tesco shopping, ParentPay school meal booking, TradingView analysis, and other no-API automation. The [browser docs](https://docs.openclaw.ai/tools/browser) are the strongest technical source here because they describe profiles, snapshots, refs, actions, downloads, storage, cookies, remote CDP, and debugging.

The trigger is usually a user request or scheduled task. The action surface is a web UI. Data sensitivity is often high because the browser may be logged into accounts. Reversibility varies. Reading a page is reversible. Posting, buying, booking, or submitting is not. Evidence quality is medium when examples are showcased but not linked to code; high for the browser tool contract itself.

The safe version observes and drafts. It logs final URLs and screenshots. It asks before checkout, booking, posting, deleting, or sending. It uses the isolated `openclaw` profile by default and the signed-in `user` profile only when necessary. The unsafe version gives an agent broad access to a live browser and tells it to handle vague goals.

## Home and physical automation

Home and hardware examples include GoHome, Roborock, Home Assistant, Bambu printers, Winix air purifiers, and camera snapshots. [joshp123/gohome](https://github.com/joshp123/gohome) and [ngutman/openclaw-ha-addon](https://github.com/ngutman/openclaw-ha-addon) are stronger evidence than a simple post because they show implementation or packaging.

The trigger can be chat, schedule, sensor, or device state. The action surface is usually Home Assistant, a device API, a local network service, or a CLI. Data sensitivity is mixed: home presence, cameras, and routines are sensitive, while some device status is low risk. Reversibility can be poor if a physical action causes damage or safety issues. Evidence quality is medium to high depending on repository depth.

The safe version reports state, suggests actions, and controls low-risk devices with explicit commands. The risky version lets a general agent decide physical actions from vague prompts. A practical pattern is to define narrow skills: `vacuum kitchen`, `pause printer`, `show camera snapshot`, `report air quality`. Do not expose arbitrary device control unless the device layer already enforces safety.

## Planner, memory, and knowledge workflows

Planner workflows include Todoist, CalDAV, morning briefings, Oura health assistant behavior, WhatsApp memory vaults, and Karakeep semantic search. [jamesbrooksco/karakeep-semantic-search](https://github.com/jamesbrooksco/karakeep-semantic-search) is a good example of structured knowledge retrieval. [joshp123/xuezh](https://github.com/joshp123/xuezh) shows an education-oriented memory and feedback loop.

The trigger can be schedule, chat, new data, or periodic review. The action surface is a calendar, task manager, notes archive, vector database, or messaging export. Data sensitivity is high because personal memory and calendar data reveal habits, relationships, and plans. Reversibility depends on whether the workflow only summarizes or writes back. Evidence quality is medium because public examples often show possibility but not long-term reliability.

The safe version summarizes, drafts, and cites. The risky version silently rewrites memory, reschedules people, or treats health data as diagnostic. The practitioner should keep raw data, derived notes, and agent beliefs separate. Provenance is the difference between useful memory and confident distortion.

## Deployment and operations workflows

Deployment workflows include AWS hosting, Nix packaging, Ansible hardening, Docker images, Home Assistant add-ons, Android/Termux packaging, and channel-specific bundles. [aws-samples/sample-host-openclaw-on-amazon-bedrock-agentcore](https://github.com/aws-samples/sample-host-openclaw-on-amazon-bedrock-agentcore), [openclaw/nix-openclaw](https://github.com/openclaw/nix-openclaw), and [openclaw/openclaw-ansible](https://github.com/openclaw/openclaw-ansible) are high-value sources because they show operational concerns.

The trigger is usually startup, deployment, cron, or channel events. The action surface is infrastructure: gateways, containers, cloud services, browsers, storage, logs, and secrets. Data sensitivity is high because the deployment holds credentials and user state. Reversibility is mixed. Config changes can be rolled back if recorded; leaked secrets cannot. Evidence quality is high when repositories include files and issue history.

The safe version binds to loopback or private networks, stores secrets outside committed config, logs tool calls, and separates agents/workspaces. The risky version exposes a gateway publicly, stores tokens inline, or mixes personal and work channels in one unrestricted workspace.

## How to choose from the matrix

Pick the workflow with the best combination of pain, boundedness, evidence, and reversibility. If two workflows are equally painful, choose the one with a stronger API or CLI surface. If a workflow requires browser automation, start read-only. If it writes to other people or physical devices, add confirmation. If it handles secrets, make deployment and storage part of the first design, not a later cleanup.

This matrix turns the showcase from a list of exciting possibilities into an adoption plan. The question is not, can OpenClaw do everything? The useful question is, which specific workflow has a narrow enough surface that OpenClaw can help today without becoming a liability?
