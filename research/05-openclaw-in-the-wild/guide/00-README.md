# Guide: OpenClaw in the Wild

This guide is a practitioner-first map of how OpenClaw appears in public usage evidence. It is written for someone who wants to decide what OpenClaw is good for, what examples are real enough to copy, what remains demo-shaped, and what operational details matter before trusting it with personal or team automation.

## Reading order

1. [The Field Map](01-the-field-map.md) - what OpenClaw is in practice, and what evidence exists.
2. [Evidence Quality](02-evidence-quality.md) - how to read official showcases, GitHub repos, social posts, and issues without overclaiming.
3. [Chat-Native Workflows](03-chat-native-workflows.md) - Telegram, Slack, Lark, DingTalk, WeChat, Beeper, and the gateway pattern.
4. [Browser Automation](04-browser-automation.md) - when OpenClaw uses a browser, how profiles work, and why reliability/security matter.
5. [Developer Productivity](05-developer-productivity.md) - PR review, Linear, Beeper, Codex monitoring, screenshot-to-Markdown, and multi-agent loops.
6. [Personal Planner, Education, and Knowledge](06-personal-planner-education-knowledge.md) - calendars, Todoist, health, language learning, memory vaults, semantic search, and research-style work.
7. [Deployment and Operations](07-deployment-and-operations.md) - AWS, Nix, Ansible, Docker, Home Assistant, Android, and hardening.
8. [Friction and Reliability](08-friction-and-reliability.md) - setup failures, policy controversy, social noise, CDP extraction issues, and what to verify.
9. [Practitioner Playbook](09-practitioner-playbook.md) - how to choose a first OpenClaw project and keep it bounded.
10. [Use-Case Matrix](10-use-case-matrix.md) - evidence-weighted categories by trigger, surface, sensitivity, and reversibility.
11. [Security and Privacy](11-security-and-privacy.md) - gateway, browser, skills, secrets, prompt injection, and approval boundaries.
12. [Comparable Patterns](12-comparable-patterns.md) - browser/data-extraction patterns that sharpen OpenClaw design choices.
13. [Refresh Playbook](13-refresh-playbook.md) - how to update this research as OpenClaw changes.

## Core thesis

OpenClaw is not best understood as one more chatbot. In the public evidence, it behaves more like a self-hosted agent gateway: a way to bind messages from chat channels to skills, files, browsers, calendars, APIs, local tools, and deployment surfaces. The strongest evidence is concrete but uneven: official showcase entries, GitHub repositories, channel connectors, deployment recipes, and issue threads. The weakest evidence is broad adoption rhetoric without reproducible artifacts.

## Source posture

Every important claim should be read through its evidence type. The official [OpenClaw Showcase](https://docs.openclaw.ai/start/showcase) is valuable because it names projects and links to demos or repos, but it is still curated by the project. GitHub repositories such as [aws-samples/sample-host-openclaw-on-amazon-bedrock-agentcore](https://github.com/aws-samples/sample-host-openclaw-on-amazon-bedrock-agentcore), [DingTalk-Real-AI/dingtalk-openclaw-connector](https://github.com/DingTalk-Real-AI/dingtalk-openclaw-connector), [joshp123/gohome](https://github.com/joshp123/gohome), and [am-will/snag](https://github.com/am-will/snag) are stronger because they expose files, commands, architecture, or issues. Community discussions are useful for sentiment and friction, but they are not proof of stable usage by themselves.

14. [Two-Sentence Summary](14-two-sentence-summary.md) - compressed takeaways and starting advice.
