# Source Index: OpenClaw in the Wild

This index labels source quality and explains how each source was used. Browser captures and extracted Markdown snapshots are under `tmp/search-web-cdp/openclaw-in-the-wild/` and are not committed.

## Quality labels

- **official** - OpenClaw documentation or official project material.
- **open-source** - GitHub repository or implementation.
- **open-source-sample** - sample application or deployment recipe.
- **open-source-integration** - connector/plugin/channel integration repository.
- **open-source-practitioner** - practitioner-built repo that shows a workflow or skill.
- **open-source-deployment** - packaging, deployment, or hardening repository.
- **open-source-research** - research-style or agent-training repository.
- **open-source-domain-skills** - domain-specific skill collection; use with extra safety caveats.
- **community-catalog** - curated list; good for breadth, weaker for individual proof.
- **community** - HN/Reddit/X discussion; used as sentiment, not proof.
- **community-question** - Stack Overflow or issue-style question; evidence of interest or friction.
- **video** - video page or official-showcase-linked video; cite only when rendered content or official summary supports the claim.

## Sources

| # | Quality | Source | Role | Extracted words | Artifact root |
|---:|---|---|---|---:|---|
| 1 | official | [OpenClaw Showcase](https://docs.openclaw.ai/start/showcase) | Official curated community examples and usage taxonomy | 224551 | `tmp/search-web-cdp/openclaw-in-the-wild/` |
| 2 | official | [Browser (OpenClaw-managed)](https://docs.openclaw.ai/tools/browser) | Browser automation architecture, security controls, config, and CLI reference | 3434 | `tmp/search-web-cdp/openclaw-in-the-wild/` |
| 3 | official | [openclaw browser CLI](https://docs.openclaw.ai/cli/browser) | Concrete browser CLI commands for profiles, tabs, snapshots, screenshots, navigation, click, and type | 1366 | `tmp/search-web-cdp/openclaw-in-the-wild/` |
| 4 | official | [OpenClaw CLI Automation](https://docs.openclaw.ai/start/wizard-cli-automation) | Non-interactive onboarding and agent setup commands | 348 | `tmp/search-web-cdp/openclaw-in-the-wild/` |
| 5 | open-source | [openclaw/openclaw](https://github.com/openclaw/openclaw) | Main OpenClaw repository and project self-description | 1771 | `tmp/search-web-cdp/openclaw-in-the-wild/` |
| 6 | open-source | [openclaw/clawhub](https://github.com/openclaw/clawhub) | Skill directory substrate for OpenClaw skills | 1132 | `tmp/search-web-cdp/openclaw-in-the-wild/` |
| 7 | community-catalog | [VoltAgent/awesome-openclaw-skills](https://github.com/VoltAgent/awesome-openclaw-skills) | Large categorized skill list from the OpenClaw skill ecosystem | 2109 | `tmp/search-web-cdp/openclaw-in-the-wild/` |
| 8 | community-catalog | [hesamsheikh/awesome-openclaw-usecases](https://github.com/hesamsheikh/awesome-openclaw-usecases) | Community collection of OpenClaw use cases | 1275 | `tmp/search-web-cdp/openclaw-in-the-wild/` |
| 9 | community-catalog | [AlexAnys/awesome-openclaw-usecases-zh](https://github.com/AlexAnys/awesome-openclaw-usecases-zh) | Chinese-language use-case catalog with office, content, DevOps, knowledge, and personal assistant scenarios | 901 | `tmp/search-web-cdp/openclaw-in-the-wild/` |
| 10 | open-source-sample | [AWS sample: host OpenClaw on Amazon Bedrock AgentCore](https://github.com/aws-samples/sample-host-openclaw-on-amazon-bedrock-agentcore) | Deployment-heavy sample with microVM isolation, Telegram/Slack routing, browser, guardrails, and CDK | 6610 | `tmp/search-web-cdp/openclaw-in-the-wild/` |
| 11 | open-source-integration | [DingTalk OpenClaw Connector](https://github.com/DingTalk-Real-AI/dingtalk-openclaw-connector) | Official DingTalk channel plugin for enterprise chat workflows | 515 | `tmp/search-web-cdp/openclaw-in-the-wild/` |
| 12 | open-source-integration | [Lark OpenClaw Connector](https://github.com/larksuite/openclaw-lark) | Lark/Feishu channel plugin | 650 | `tmp/search-web-cdp/openclaw-in-the-wild/` |
| 13 | open-source-integration | [openclaw-wechat](https://github.com/freestylefly/openclaw-wechat) | Personal WeChat connection for OpenClaw | 483 | `tmp/search-web-cdp/openclaw-in-the-wild/` |
| 14 | open-source-practitioner | [padel-cli](https://github.com/joshp123/padel-cli) | Availability checking and booking CLI showcased for OpenClaw automation | 508 | `tmp/search-web-cdp/openclaw-in-the-wild/` |
| 15 | open-source-practitioner | [xuezh Chinese learning](https://github.com/joshp123/xuezh) | Education and language-learning skill example | 1386 | `tmp/search-web-cdp/openclaw-in-the-wild/` |
| 16 | open-source-practitioner | [GoHome automation](https://github.com/joshp123/gohome) | Home automation system with OpenClaw as natural-language interface | 2017 | `tmp/search-web-cdp/openclaw-in-the-wild/` |
| 17 | open-source-practitioner | [Karakeep semantic search](https://github.com/jamesbrooksco/karakeep-semantic-search) | Knowledge and bookmark semantic search with Qdrant and embeddings | 659 | `tmp/search-web-cdp/openclaw-in-the-wild/` |
| 18 | open-source-practitioner | [Clawdia bridge](https://github.com/alejandroOPI/clawdia-bridge) | Phone/voice bridge between Vapi and OpenClaw | 566 | `tmp/search-web-cdp/openclaw-in-the-wild/` |
| 19 | open-source-practitioner | [OpenClaw Home Assistant add-on](https://github.com/ngutman/openclaw-ha-addon) | Home Assistant OS deployment add-on | 331 | `tmp/search-web-cdp/openclaw-in-the-wild/` |
| 20 | open-source-practitioner | [Linear CLI](https://github.com/Finesssee/linear-cli) | Developer productivity CLI integrated with agentic workflows including OpenClaw | 3196 | `tmp/search-web-cdp/openclaw-in-the-wild/` |
| 21 | open-source-practitioner | [Beeper CLI](https://github.com/blqke/beepcli) | Messaging automation via Beeper Desktop local MCP API | 1501 | `tmp/search-web-cdp/openclaw-in-the-wild/` |
| 22 | open-source-practitioner | [SNAG screenshot-to-Markdown](https://github.com/am-will/snag) | Screenshot region to Markdown workflow for dev/productivity tasks | 619 | `tmp/search-web-cdp/openclaw-in-the-wild/` |
| 23 | open-source-deployment | [nix-openclaw](https://github.com/openclaw/nix-openclaw) | Reproducible OpenClaw packaging and configuration through Nix | 3051 | `tmp/search-web-cdp/openclaw-in-the-wild/` |
| 24 | open-source-deployment | [openclaw-ansible](https://github.com/openclaw/openclaw-ansible) | Automated hardened installation with Tailscale, UFW, and Docker isolation | 1346 | `tmp/search-web-cdp/openclaw-in-the-wild/` |
| 25 | open-source-research | [OpenClaw-RL](https://github.com/Gen-Verse/OpenClaw-RL) | Research-style project for training agents by talking | 1264 | `tmp/search-web-cdp/openclaw-in-the-wild/` |
| 26 | open-source-domain-skills | [OpenClaw Medical Skills](https://github.com/FreedomIntelligence/OpenClaw-Medical-Skills) | Medical skill library for OpenClaw | 1866 | `tmp/search-web-cdp/openclaw-in-the-wild/` |
| 27 | open-source-integration | [Apify OpenClaw plugin](https://github.com/apify/apify-openclaw-plugin) | Data extraction and actor-platform integration signal | 1045 | `tmp/search-web-cdp/openclaw-in-the-wild/` |
| 28 | community | [HN discussion mentioning OpenClaw and Claude Code policy controversy](https://news.ycombinator.com/item?id=47963204) | Community sentiment and controversy signal | 40332 | `tmp/search-web-cdp/openclaw-in-the-wild/` |
| 29 | community | [Reddit OpenClaw policy/workaround discussion](https://www.reddit.com/r/openclaw/comments/1svmq20/psa_anthropic_clarified_the_openclaw_ban_you_can/) | OpenClaw community support and workaround discussion | 41 | `tmp/search-web-cdp/openclaw-in-the-wild/` |
| 30 | community-question | [Stack Overflow: OpenClaw with WordPress workflow automation](https://stackoverflow.com/questions/79918804/is-it-possible-to-integrate-openclaw-with-wordpress-to-automate-parts-of-the-dev) | Exploratory practitioner question about workflow automation | 0 | `tmp/search-web-cdp/openclaw-in-the-wild/` |
| 31 | community-question | [Stack Overflow: Boss wants us to add more AI to workflow](https://stackoverflow.com/questions/79928220/boss-wants-us-to-add-more-ai-to-our-workflow) | Adjacent agent workflow adoption concern in a Django/Docker/Celery stack | 0 | `tmp/search-web-cdp/openclaw-in-the-wild/` |
| 32 | video | [OpenClaw setup walkthrough by VelvetShark](https://www.youtube.com/watch?v=SaWSPZoPX34) | Official-showcase-linked setup walkthrough | 246 | `tmp/search-web-cdp/openclaw-in-the-wild/` |

## Source-selection notes

- Official documentation defines what OpenClaw claims to support, but the guide separates official curation from independent proof.
- GitHub repositories are the highest-value practitioner artifacts because they expose commands, config, deployment shape, and issue history.
- GitHub issues are noisy. Bot-generated trending issues were treated as attention signals only; setup failures, integration requests, and security/policy bypass reports were treated as higher-signal friction.
- HN, Reddit, X, Stack Overflow, and YouTube were used for discovery, sentiment, and friction. They were not used to inflate adoption claims.
- Browser automation/data-extraction comparables are included only when they sharpen OpenClaw lessons: screenshots to Markdown, Apify-style actor integrations, and CDP/browser profile configuration.
