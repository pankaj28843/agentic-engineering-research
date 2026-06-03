# 09 - Capabilities, Costs, And Unknowns

Harness engineering depends on product surfaces as well as local practice. A practitioner around USD 200/month in June 2026 can buy much more than a chat box, but the details change quickly. This chapter records current official sources and separates capability from guarantee.

The source dates matter. OpenAI docs in this packet were extracted on 2026-06-01 from official developer pages. Anthropic official pages were extracted earlier and also checked through official web search on 2026-06-03. Prices, model names, usage limits, and included features can change. Treat this as a dated research note, not buying advice.

## ELI5

Buying an agent subscription is like renting a car. The car matters, but so do roads, fuel, insurance, traffic laws, and where you are allowed to drive. A USD 200/month plan may give you more agent driving time, but your harness decides whether that time is useful or dangerous.

## OpenAI Practitioner Surface

OpenAI's official [Codex pricing](https://developers.openai.com/codex/pricing/) extract says Plus is USD 20/month and includes Codex on web, CLI, IDE extension, and iOS, cloud-based integrations like automatic code review and Slack integration, latest models, and credits. It says Pro starts at USD 100/month and offers 5x or 20x higher rate limits than Plus. The same extract states that Pro USD 200 includes 20x Plus on an ongoing basis and temporary higher five-hour Codex limits through May 31, 2026. Because that date is near the current research window, the guide records it as dated and volatile.

OpenAI's [Codex app features](https://developers.openai.com/codex/app/features/) page describes a desktop experience for Codex threads in parallel, with worktree support, automations, Git functionality, skills, local/worktree/cloud modes, integrated terminal, in-app browser, computer use, file previews, IDE sync, and web search. The [Worktrees](https://developers.openai.com/codex/app/worktrees/) docs describe background worktree isolation, handoff between local and worktree, cleanup behavior, and `$CODEX_HOME/worktrees`. The [In-app browser](https://developers.openai.com/codex/app/browser/) docs describe shared rendered pages, browser comments, and browser use for local dev servers and previews.

For harness engineering, the important OpenAI surfaces are:

- Local CLI and app work.
- Worktree isolation.
- Integrated terminal visibility.
- Local environment setup scripts and actions.
- Browser use for local dev pages.
- Computer use for desktop/browser workflows with safety cautions.
- GitHub review and cloud task surfaces.
- Skills for progressive workflows.
- AGENTS.md instruction layering.
- Sandbox, approval, and network controls.

Those surfaces map closely to the OpenAI blog's private harness concepts, though the public product is not the same as the internal system.

## Anthropic Practitioner Surface

The official [Claude Code](https://claude.com/product/claude-code) page says Claude Code is available in terminal, desktop app, IDEs, web/iOS research preview, and Slack. The extracted page says Claude Code is included in Pro, Max 5x, Max 20x, Team, and Enterprise plans, with Max 20x at USD 200/month on that page. The official [Max plan](https://claude.com/pricing/max) result says Max offers up to 20x higher usage limits and a USD 200/month maximum-flexibility tier.

Anthropic's surface is therefore comparable at the broad practitioner level: terminal coding, desktop multi-tasking, IDE integration, web/mobile task delegation, Slack, and larger usage tiers. The packet does not claim feature parity. It records that a roughly USD 200/month practitioner can choose a high-usage coding-agent plan from either vendor and then still needs a harness.

## Comparison At Roughly USD 200/Month

| Dimension | OpenAI Codex Pro 20x evidence | Anthropic Claude Max 20x evidence | Harness implication |
|---|---|---|---|
| Price | Official Codex pricing extract records Pro USD 200 and 20x Plus ongoing | Official Claude Code/Max pages record Max 20x at USD 200/month | Budget can buy high usage, not automatic quality |
| Local coding | Codex app, CLI, IDE extension, local/worktree modes | Claude Code terminal and desktop app | Both still need repo docs, validation, and safety |
| Parallel work | Codex app threads, worktrees, cloud mode | Claude desktop parallel tasks and web/mobile delegation | Work isolation and artifact discipline matter |
| Browser/UI | Codex in-app browser, browser use, computer use | Claude desktop/web claims local machine app/browser interaction | UI harness should be isolated and evidence-backed |
| Review | Codex GitHub code review and automatic reviews | Claude Code page emphasizes PR status and working PRs; review details differ | Review policy is a repo harness responsibility |
| Skills/instructions | OpenAI skills and AGENTS.md official docs | Claude Code has its own docs and memory conventions, not analyzed deeply here | This packet focuses on OpenAI; do not overgeneralize |
| Safety | OpenAI sandbox/approval/network docs are detailed in the captured set | Anthropic page mentions Auto mode and product surfaces; detailed Claude Code security docs were not the focus | Treat both as requiring explicit local policy |

The comparison is intentionally conservative. The user's request asked for current official OpenAI/Anthropic docs for roughly USD 200/month practitioner capabilities, not a full product review.

## Autonomy Boundaries

The OpenAI blog says humans remain in the loop at a different abstraction layer. Official OpenAI [approvals and security](https://developers.openai.com/codex/agent-approvals-security/) docs say sandbox mode controls what Codex can technically do, while approval policy controls when it must ask. They also say local workspace-write defaults have network access off unless enabled. The [computer use guide](https://developers.openai.com/api/docs/guides/tools-computer-use) recommends isolated browser or VM environments and explicit confirmation policies for risky actions.

A practical autonomy boundary:

- Let agents read code, edit workspace files, run tests, run local dev servers, inspect unauthenticated local pages, and produce review artifacts.
- Let agents open PRs only after validation evidence exists.
- Let agents merge only in low-risk repos or after explicit approval policy.
- Stop agents before external side effects such as sending messages, making purchases, deleting data, changing permissions, accepting browser permission prompts, installing untrusted software, or handling secrets outside the scoped environment.
- Require human judgment for ambiguous product decisions, legal/security risk, production incidents, and irreversible actions.

The boundary is part of the harness. If it lives only in a human's head, the agent cannot reliably obey it.

## Unknowns From OpenAI

OpenAI's article explicitly says they do not yet know how architectural coherence evolves over years in a fully agent-generated system. That unknown is not cosmetic. It is the central long-term risk. A million lines can be generated quickly. Keeping those lines coherent, understandable, secure, and evolvable over years is the hard part.

Other unknowns:

- Which parts of OpenAI's private internal harness are essential versus incidental.
- How much of the reported velocity depends on model capability versus harness maturity.
- How well the approach works in brownfield codebases with deep legacy constraints.
- How agent-generated code behaves under long-term product pivots.
- How to measure quality beyond PR count, line count, and local validation.
- How to prevent cleanup agents from creating churn or hiding deeper design problems.
- How to audit agent-to-agent review when both agents share blind spots.

These unknowns should make practitioners more disciplined, not less interested.

## Vendor Incentives

OpenAI and Anthropic official pages are primary for product claims, but they are vendor claims. They have incentives to emphasize capability and understate operational cost. The OpenAI blog is unusually concrete and includes caveats, but it is still OpenAI telling a success story about Codex. The Anthropic pages are product pages. Treat both as credible for what they say their products offer, not as neutral proof that your team will get the same outcome.

The neutral evidence in this packet is mostly structural:

- Public source code in Symphony.
- Local extracted artifacts.
- Validation requirements in this repository.
- Concrete replication steps.

The more a claim matters to operational risk, the more it should be proven in your own environment.

## What To Measure Locally

Do not measure only "lines generated" or "PRs opened." Measure:

- Time from issue to validated PR.
- Human minutes spent per accepted PR.
- Rework rate.
- Review finding severity.
- Validation failure categories.
- Flake rate.
- Post-merge bug rate.
- Cleanup PR volume.
- Architecture lint violations over time.
- Token/cost per accepted change.
- Number of tasks blocked by missing context, missing tools, or missing permissions.

These metrics tell you whether the harness is improving. If human attention per accepted PR falls while post-merge bugs stay flat or improve, the harness is working. If PR count rises while cleanup and bugs rise faster, the harness is producing debt.

## Refresh Procedure

Before making spend or autonomy decisions, refresh:

```bash
cd /home/pankaj/Personal/Code/agentic-engineering-research
cdp daemon status --json
```

If CDP is healthy and headed mode is available, extract official pages again:

- OpenAI Codex pricing.
- OpenAI Codex app features.
- OpenAI worktrees.
- OpenAI browser/computer use.
- OpenAI approvals/security.
- Anthropic Claude Code.
- Anthropic Max/pricing.

Keep rendered pages in `tmp/`. Update `sources.json`, `source-index.md`, and this chapter with fetch dates. Do not cite snippets.

## Final Synthesis

The OpenAI-centered answer is this: harness engineering is the discipline that turns agent capability into engineering throughput by making the work environment legible, bounded, observable, reviewable, and self-cleaning. Product subscriptions buy access to models and surfaces. They do not buy the harness. The harness is the repo, tools, docs, tests, browser evidence, observability, review policy, orchestration, cleanup, and safety boundary you build around the agent.

That is why the replication advice is practical rather than mystical. Start with worktrees, docs, validation, browser evidence, logs, lints, review loops, and cleanup. Then increase autonomy only where evidence proves the loop is safe.

## Spend Decisions For Practitioners

At roughly USD 200/month, the mistake is to ask only "which model is best?" A better purchasing question is: which surface fits my workflow, can I run multiple isolated tasks, can the agent inspect my app and validation artifacts, can I review changes quickly, can I control network and filesystem boundaries, can I extend the agent with repo-local instructions, and can I recover long-running work after context loss?

If the answer is no, higher usage limits may just produce more low-quality attempts. Spend the first month building the harness around a few high-value tasks. Then increase usage if the evidence shows lower human attention per accepted change.

## Capability Is Not Capacity

Capability means the agent can do a task in principle. Capacity means your local system can support the work repeatedly. OpenAI's blog is about capacity as much as capability. Codex could write code, but the team still needed per-worktree apps, CDP, observability, docs, lints, review, and cleanup.

A product page can tell you about capability. Your harness metrics tell you about capacity: how many concurrent worktrees your machine can run, how many dev servers avoid port or database conflicts, how fast browser evidence collects, how often review findings are real, how often agents block on missing docs, and how often humans need to rescue a run.

Capacity is local and empirical. Measure it.

## Governance For Autonomy

Write an autonomy table:

| Action | Default | Escalation |
|---|---|---|
| Edit workspace files | Allowed | Human if outside workspace |
| Run tests/lints | Allowed | Human if installing privileged tools |
| Use local unauthenticated browser | Allowed with evidence | Human if browser asks for permissions |
| Use signed-in browser | Deny by default | Human-approved scoped session |
| Use network | Deny by default | Allowlist by task |
| Open PR | Allowed after validation | Human if validation incomplete |
| Merge PR | Deny by default | Allowed only by low-risk repo policy |
| Delete data | Deny | Human approval required |
| Change secrets/permissions | Deny | Human approval required |

This table should live in `docs/SECURITY.md` or the equivalent. It should be referenced by `AGENTS.md`, loop prompts, and scheduler config. If you build a Symphony-like runner, make the table part of `WORKFLOW.md`.

## What Would Prove Completion In A Local Harness

For your own project, do not declare "we do harness engineering" because docs exist. Prove that a new agent can read `AGENTS.md` and find the right docs, a new task gets its own worktree, the app boots in that worktree, the agent can collect browser or runtime evidence, `make validate` covers the changed behavior, a review agent can find real issues without drowning the author in noise, a cleanup agent can identify stale docs or invariant violations, a resumed agent can recover from the plan file, and human approval boundaries are explicit and tested.

The proof is operational. A harness is real when it changes how a task completes.

## Open Questions For Future Research

Future refreshes of this packet should investigate how OpenAI's self-improving tax-agent work relates to this harness post, whether public Codex app worktrees and local environments converge further with the internal blog pattern, whether Symphony gains hardened sandbox modes or non-Linear tracker adapters, how Claude Code's desktop/web/mobile/Slack surfaces compare in source-backed detail, how practitioners measure long-term architecture coherence, which cleanup loops produce net quality improvement, and how browser/computer-use prompt injection defenses evolve.

These are not blockers for the current packet. They are the next research frontier.
