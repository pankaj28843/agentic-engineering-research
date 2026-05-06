# Chapter 08 — Production case studies: OpenAI Codex and Stripe Minions

**You'll learn:** what OpenAI and Stripe actually report building, which patterns generalize, and why their productivity numbers should be treated as evidence but not neutral truth.

Source jumps: OpenAI's [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/), Stripe's [Minions: Stripe's one-shot, end-to-end coding agents](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents), Böckeler's [memo response](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering-memo.html), and Fowler's main [harness article](https://martinfowler.com/articles/harness-engineering.html).

## Why case studies matter

Vendor and practitioner case studies are not scientific proof. OpenAI benefits if people believe Codex can maintain huge systems. Stripe benefits reputationally from showing engineering leverage. Both organizations have unusual talent, tooling, scale, and incentives. Their numbers should not be copied into your planning spreadsheet as expected ROI.

But these reports still matter. They describe real systems with users, CI, internal tooling, review loops, sandboxing, observability, failure modes, and trade-offs. The patterns are more generalizable than the numbers.

Read them the way an architect reads a postmortem: not “will this exact result happen to me?” but “what controls did they need before autonomy became tolerable?”

## OpenAI: no manually typed code as forcing function

OpenAI reports a five-month experiment building and shipping an internal beta product with **0 lines of manually written code**. The product had internal daily users and external alpha testers. The repository grew to roughly a million lines across application logic, infrastructure, tooling, documentation, observability, and internal developer utilities. They report about 1,500 PRs merged with a small team, estimating roughly one-tenth the time of writing code by hand.

The headline is flashy, but the forcing function is the real lesson. “No manually-written code” meant humans could not just patch around Codex when it failed. They had to ask: what capability is missing, and how do we make it legible and enforceable for the agent? That pushed human work up a level: systems, scaffolding, feedback loops, environment design, documentation, architecture constraints, and validation.

OpenAI's slogan is “Humans steer. Agents execute.” In practice, steering meant specifying intent, breaking goals down, creating tools, making app state observable, encoding feedback loops, and feeding lessons back into the repository.

## OpenAI: repository knowledge as system of record

One of OpenAI's earliest lessons was context management. Their one-big-`AGENTS.md` failed. The replacement was a short `AGENTS.md` as table of contents and a structured docs directory as the system of record.

The docs layout included design docs, execution plans, generated database schema references, product specs, design system references, quality score, reliability docs, and security docs. Plans were first-class artifacts: active plans, completed plans, progress, decisions, and technical debt were versioned and co-located.

This is not just documentation hygiene. It is agent legibility. The agent can reason over repository-local files. It cannot reason over what is only in Slack, Google Docs, or a human's head. OpenAI's team pushed more context into versioned artifacts so agents could operate without relying on hidden human memory.

## OpenAI: app and observability legibility

OpenAI made the application itself legible to Codex. Codex could boot one app instance per git worktree. It could drive the app with Chrome DevTools Protocol, inspect DOM snapshots, use screenshots, and navigate. It also had a local observability stack per worktree, with logs, metrics, and traces. Agents could query logs with LogQL and metrics with PromQL.

This turns vague quality goals into inspectable tasks. “Ensure startup completes in under 800ms” requires startup timing to be visible. “No span in these user journeys exceeds two seconds” requires traces. “Validate the UI fix” requires browser evidence. The harness converts invisible product state into context the agent can use.

For this repo, the analogous move is article extraction. Browser crawls in `tmp/` are not enough if the durable guide only uses vague summaries. Clean article Markdown snapshots make source content legible to future writing agents.

## OpenAI: architecture constraints and garbage collection

OpenAI's architecture story is rigid by design. Each business domain is divided into fixed layers with validated dependency directions and limited permissible edges. Cross-cutting concerns enter through explicit providers. Custom linters and structural tests enforce these rules.

They also enforce “taste invariants”: structured logging, naming conventions, file size limits, schema/type naming rules, and reliability requirements. Importantly, linter messages are written to teach Codex how to remediate.

As throughput grew, drift became a problem. Codex replicated existing patterns, including bad ones. The team initially spent Fridays cleaning up AI slop. That did not scale. They encoded “golden principles” and ran recurring cleanup tasks that scan for deviations, update quality grades, and open small refactoring PRs. They call this garbage collection.

The general pattern: when humans repeatedly clean the same kind of mess, promote the cleanup into the harness.

## Stripe: why build minions in-house?

Stripe's context is very different. Its codebase spans hundreds of millions of lines across a few large repos. Much of the backend is Ruby with Sorbet, not Rails, with many homegrown libraries. The stakes include more than $1 trillion per year of payment volume plus financial, regulatory, and compliance obligations.

Stripe says vibe coding a prototype from scratch is fundamentally different from contributing to a mature Stripe codebase. Generic agents are good at unconstrained greenfield work, but Stripe needs agents that understand its tools, code intelligence, environments, source control, CI, and internal systems. So it built Minions as a custom harness tightly integrated with developer productivity foundations.

Their principle: if it is good for humans, it is good for LLMs too. Minions use the same kind of devboxes and tooling that human Stripe engineers use.

## Stripe: the minion lifecycle

A typical minion run starts from Slack and ends in a PR that passes CI and is ready for human review. Engineers can kick off minions from Slack threads, internal docs, feature flag platforms, ticketing UIs, or flaky-test tickets. The minion can read the thread and linked context. Engineers can inspect the minion's decisions and actions in a web UI.

Under the hood, a minion starts in an isolated devbox. Devboxes are pre-warmed, can spin up quickly, include Stripe code and services, and are isolated from production resources and the internet. This permits unattended execution without human permission checks for every action.

The core loop runs on a fork of Block's `goose`, but Stripe interleaves agent loops with deterministic code for git operations, linters, testing, and required steps. Minions read the same coding-agent rule files as human-operated tools, but rules are mostly conditionally applied based on subdirectories. Stripe also uses MCP through an internal Toolshed server with more than 400 tools, exposing curated subsets for context such as docs, tickets, build statuses, and Sourcegraph code intelligence.

## Stripe: bounded feedback

Stripe's feedback strategy is pragmatic. Minions aim to one-shot tasks, but if they do not, automated feedback layers help them correct. The first layer is local: a heuristic executable selects relevant lints on each git push and runs quickly. The second layer is CI: selective tests from a huge battery, with autofixes where available. If a failure has no autofix, it goes back to the minion.

But Stripe stops after at most two CI rounds. This is a crucial detail. It acknowledges that full CI loops cost tokens, compute, and time, and that marginal returns decline. A good harness is not maximal autonomy; it is budgeted autonomy.

## What generalizes

Patterns that likely generalize:

- Short entry-point docs plus structured deeper docs.
- Repository-local plans and progress artifacts.
- App state made legible through browser, logs, metrics, traces, or equivalent tools.
- Isolated execution environments.
- Deterministic checks interleaved with agent loops.
- Agent-readable error messages.
- Architecture constraints as code.
- Continuous cleanup against drift.
- Fast local feedback before expensive CI.
- Bounded retries and human escalation.

Patterns that may not generalize easily:

- OpenAI's million-line, no-manual-code constraint.
- Stripe's devbox infrastructure and Toolshed scale.
- Throughput numbers such as 1,500 PRs or 1,000+ minion PRs per week.
- Minimal human review in contexts with weaker verification.
- Greenfield architecture rigidity in messy legacy systems.

## The skeptical reading

Böckeler's memo is appropriately skeptical. She notes OpenAI's vested interest and says the write-up focuses mostly on long-term internal quality and maintainability, while functional behaviour verification is less clear. That skepticism should be preserved.

The right conclusion is not “agents can now replace engineers.” The right conclusion is “agent throughput makes harness quality the bottleneck.” OpenAI and Stripe both show that serious autonomy required serious engineering around the model. The more code agents generate, the more important it becomes to design environments, feedback loops, control systems, and review evidence.

## Chapter takeaways

- OpenAI and Stripe provide important evidence, but their ROI numbers should not be treated as neutral or generally portable.
- OpenAI's strongest lesson is repository legibility, architecture enforcement, local observability, and continuous garbage collection.
- Stripe's strongest lesson is isolated devboxes, integration with existing developer tooling, fast local feedback, curated MCP context, and bounded CI retries.
- Both stories support the same thesis: autonomy depends on harness quality.
- Patterns generalize better than metrics.

**Next:** [Chapter 09 — Security boundaries](09-security-boundaries.md).
