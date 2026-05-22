# Chat-Native Workflows

## Why chat is the natural front door

The most repeated OpenClaw pattern is not browser automation or skill packaging by itself. It is chat-native control. A user wants to send a message from Telegram, Slack, DingTalk, Lark, WeChat, WhatsApp-like surfaces, Discord, or a terminal and have useful work happen somewhere else. This matters because the hardest part of personal automation is not writing the script once. It is remembering to run it, finding the right interface, passing the right context, and checking the result. Chat is already where many people coordinate tasks, share links, send screenshots, leave voice notes, and ask for help.

The official [OpenClaw Showcase](https://docs.openclaw.ai/start/showcase) is full of examples where chat is the visible interface and the useful work happens behind it. PR review feedback goes to Telegram. A Todoist skill is generated directly in Telegram. A personal site is rebuilt through Telegram while the user stays away from the laptop. Slack auto-support watches a company channel and forwards notifications. A morning briefing returns as a generated scene. Voice notes and phone bridges turn speech into agent entrypoints. Even examples that are not purely chat, such as shopping or browser analysis, often end in a channel response.

Practitioners should read this as an interface lesson. OpenClaw becomes compelling when it can live where intent is already expressed. If the user already sends themselves reminders in Telegram, a Telegram OpenClaw workflow can become a planner. If a support team already uses Slack, a Slack OpenClaw workflow can become triage or escalation. If a company in China already runs DingTalk or Lark, a channel plugin is not optional polish; it is the adoption path.

## Enterprise chat connectors

The strongest chat evidence comes from connector repositories. [DingTalk-Real-AI/dingtalk-openclaw-connector](https://github.com/DingTalk-Real-AI/dingtalk-openclaw-connector) is positioned as an official OpenClaw DingTalk channel plugin. The captured repository page described OpenClaw compatibility, DingTalk messaging features, and installation/setup shape. It is important because DingTalk is not a generic demo channel. It is a workplace tool with messages, attachments, calendars, approvals-like workflows, and enterprise identity expectations.

The [Lark connector](https://github.com/larksuite/openclaw-lark) plays a similar role for Lark/Feishu. [freestylefly/openclaw-wechat](https://github.com/freestylefly/openclaw-wechat) shows the consumer/personal messaging side. The Chinese-language ecosystem also includes catalogs and Docker-style bundles aimed at Chinese IM platforms. The GitHub search results included projects for Feishu/Lark, DingTalk, QQ, WeCom, and WeChat. Not every repository is equally mature, but the pattern is clear: OpenClaw users want the assistant to be reachable inside local messaging norms, not only inside a web app.

From a design perspective, channel connectors must solve more than send and receive. They need to map users to agents, preserve conversation context, route attachments, handle markdown or rich cards, support multi-agent selection, and avoid leaking tokens. They also need a failure mode: what should happen if OpenClaw is down, the model call times out, a skill errors, or the channel rejects a message? A chat integration that cannot report failure clearly is dangerous because the user may assume a task ran.

## Developer chat loops

Developer productivity examples show why chat-native OpenClaw is not only a consumer assistant story. The showcase's PR review to Telegram example describes an OpenCode-generated change followed by OpenClaw reviewing the diff and replying in Telegram with suggestions and a merge verdict. That pattern turns code review into an asynchronous notification loop. The developer does not need to poll a terminal session or manually summarize a diff. The agent can inspect the change, judge severity, and message the result.

This is powerful but easy to overtrust. A good PR review workflow should state whether it found high-confidence bugs, what tests ran, and whether it is making a merge recommendation or only a review suggestion. The user still needs a repository policy: can OpenClaw comment publicly, only DM, open PRs, merge, or just summarize? The public examples are strongest when they keep a human in the loop. A Telegram verdict is useful because it gets attention. It should not become an invisible auto-merge gate without additional checks.

Other developer-facing chat loops include Linear issue management, Beeper chat automation, Codex session monitoring, and multi-agent orchestration. [Finesssee/linear-cli](https://github.com/Finesssee/linear-cli) is not just an OpenClaw repo; it is a CLI that fits agentic workflows where issue trackers become tool surfaces. [blqke/beepcli](https://github.com/blqke/beepcli) uses Beeper Desktop's local API so agents can read, send, and archive messages across many chat networks. These examples sharpen the lesson: OpenClaw does not have to own every integration if a local CLI exposes it safely.

## Personal assistant and planner chat

The personal planner pattern appears in examples such as Todoist skill generation, CalDAV calendar integration, Oura ring health assistant behavior, job search, accounting intake, morning briefings, and WhatsApp memory vaults. The user sends an intent, and OpenClaw reads or updates personal state. This is the dream version of a personal AI assistant, but it is also the riskiest version because personal state is messy and sensitive.

A useful planner needs three boundaries. First, read-only summarization should be easy and safe. Asking for today's calendar, unread messages, recent health trends, or job matches is lower risk than changing them. Second, write actions should have confirmation for anything costly, public, financial, medical, or hard to undo. Booking a delivery slot, sending a message, submitting a job application, or changing a calendar should not happen silently. Third, memory updates should be inspectable. If the assistant learns preferences from chat, the user needs a way to review, correct, or delete them.

The showcase's wine-cellar skill is a small but instructive case. The agent asks for a sample CSV export and where to store it, then creates and tests a local skill for a collection of 962 bottles. That is a grounded planner pattern: it starts from user data, asks for storage location, builds a reusable capability, and tests it. The same pattern can apply to recipes, books, subscriptions, home inventory, workouts, or travel documents. The trick is to keep the data boundary explicit.

## What chat-native workflows need operationally

Chat-native workflows need identity, routing, persistence, and notifications. Identity answers who sent this message and which agent/workspace should respond. Routing answers which skill, browser profile, model, or node host should act. Persistence answers what the agent remembers across sessions. Notifications answer how the user learns a long-running task finished, failed, or needs approval.

The [CLI automation docs](https://docs.openclaw.ai/start/wizard-cli-automation) show that OpenClaw can add another agent with a separate workspace and channel binding using commands like `openclaw agents add work --workspace ~/.openclaw/workspace-work --model openai/gpt-5.2 --bind whatsapp:biz --non-interactive --json`. That command is a big clue. A serious OpenClaw deployment may not be one assistant. It may be multiple named agents with separate workspaces, models, channels, and policies.

For a practitioner, the safest first chat-native project is narrow. Pick one channel, one workflow, and one result. For example: send a Telegram message with a GitHub PR URL and receive a read-only review summary; send a Slack command and receive a list of matching Linear issues; send a voice note and receive a transcript; send a school meal booking request and receive a draft before final confirmation. Do not begin with a global assistant that can read every chat and control every browser. That is how a useful gateway becomes an unbounded liability.

## Success criteria

A chat-native OpenClaw workflow is successful when the user can describe it in one sentence, repeat it without remembering commands, inspect what happened, and recover from failure. It is not successful merely because it responded once. The public examples show the promise. The practitioner's job is to add boring guarantees: scoped tokens, private networking, clear confirmation boundaries, logs, and a fallback when the channel or model fails.
