# 31. A middle path for coding inference

A smaller dedicated system, specialized coding host, neocloud deployment, or routed mix can be a credible middle path—but only for a measured workload whose quality, utilization, data control, latency, availability, integration, and exit requirements fit. The audited evidence does not show that such systems are generally cheaper than APIs or equally capable as frontier models.

The [Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf) suggests a future in which smaller dedicated hardware and coding-specialist hosts sit between hyperscalers and enterprise self-hosting. This is a useful design hypothesis from an anonymous practitioner discussion. The public evidence supplies conditional infrastructure comparisons, not a controlled coding-workload trial of that exact proposition.

## A plain-language model: choose a lane per trip

The middle path is not one provider category. It is an operating design that avoids sending every task through the most capable, expensive, or externally controlled lane.

Possible lanes include:

- a small or efficient managed model for routine, low-risk transformations;
- a frontier API for difficult reasoning or recovery;
- a dedicated tenant or specialized host for steadier demand or stronger isolation;
- a locally operated small model for sensitive, latency-critical, or offline work;
- deterministic search, parsing, tests, or static analysis where inference is unnecessary.

A router—software policy, a human choice, or both—selects a lane. The architecture is attractive when workloads differ enough for specialization to matter and predictable enough for routing to work.

Evaluate each lane using:

> full cost per accepted task at the required service and risk level

“Accepted” is essential. A cheap coding model that creates plausible but defective changes can shift cost into review, retries, incidents, and maintenance. “Required service” includes latency and availability, not only model output. “Risk level” includes data movement, permissions, retention, jurisdiction, and control.

## What public evidence can and cannot establish

The [Uptime Institute’s 2026 comparison](https://journal.uptimeinstitute.com/neoclouds-a-cost-effective-ai-infrastructure-alternative/) is the strongest bounded infrastructure evidence in the audit. For equivalent DGX H100 capacity in US Northern Virginia at listed on-demand prices, it calculated averages of $98 per server-hour for three hyperscalers and $34 for three neoclouds. Under its dedicated-cluster model, dedicated capacity crossed the price comparison at roughly 22% utilization versus hyperscalers and 66% versus neoclouds.

That result proves neither a coding host’s quality nor a universal crossover. It excludes reserved and enterprise discounts, future price changes, serving staff, application integration, reliability, and exit cost. It compares a specific capacity unit, region, and date. It does show why utilization and provider class belong in a local test.

[Computer Weekly’s analyst reporting](https://www.computerweekly.com/news/366639689/Weighing-the-trade-offs-of-neoclouds-and-sovereign-clouds) describes the corresponding service trade: specialized providers may offer lower raw GPU prices while offering fewer managed services, regions, documentation, transparency, and enterprise-support capabilities. Hyperscalers may win through existing contracts, discounts, service integration, procurement, and data proximity. The reported savings headline is not inspectably derived, so the qualitative tradeoff is stronger than its percentage.

The [on-premise cost-model preprint](https://arxiv.org/html/2509.18101v1) demonstrates sensitivity to hardware purchase, electricity, throughput, workload mix, API price, and horizon. Its full-throughput assumption and omission of networks, storage, security, staff, failure, and maintenance make its break-even cases unsuitable as deployment rules. It also contains visible numerical inconsistencies. Its main lesson is methodological: assumptions can dominate a crossover.

The independent practitioner analysis [“Should You Self-Host Inference?”](https://theaiengineer.substack.com/p/should-you-self-host-inference) contributes a useful decision vocabulary—volume, model tier, utilization, sovereignty, staffing, hardware access, maturity, latency, and routing quality. Its token thresholds and savings are not reproducible and one reader calculation disputes a crossover premise. The author also recognizes that a hybrid router can classify tasks incorrectly. Again, use the dimensions, not the advertised cut points.

Current API cost is a moving baseline. Anthropic’s [Claude Sonnet 5 launch page](https://www.anthropic.com/news/claude-sonnet-5) records $2 per million input tokens and $10 per million output tokens through 31 August 2026, then $3 and $15, while effort and tokenizer changes affect consumption. This official vendor page is useful for a dated input, not for independent quality claims or application TCO. Any middle-path business case can age when providers, models, prices, or tokenizers change.

No audited source compares a dedicated coding host, a smaller local system, and a frontier API on the same repository tasks with equal permissions and end-to-end quality. That gap makes the conclusion conditional rather than negative: run the missing comparison locally.

## Seven tests for credible fit

### 1. Workload separability

Can the organization distinguish repetitive, bounded tasks from hard or ambiguous ones before spending heavily? Formatting, search, test generation, migration transforms, and constrained fixes may be more separable than architectural design or unfamiliar incident response. If difficulty becomes visible only after failure, include escalation cost.

### 2. Quality parity for the assigned lane

Parity is task-specific, not a generic benchmark score. Use repository tests plus blinded review for correctness, security, maintainability, and instruction compliance. Track silent defects and later rework. A lane need not match a frontier model on every task; it must meet the gate for work routed to it.

### 3. Productive utilization

Measure demand by hour and queue, not a monthly token total. Dedicated capacity loses value when idle and service when saturated. Batching may improve throughput while harming interactive latency. “GPU busy” is not enough; relate capacity use to accepted work.

### 4. Data-control fit

State whether the need is residency, jurisdiction, private networking, customer isolation, key control, offline continuity, or prevention of provider retention. A local system can improve some properties while creating patching, access, and physical-security duties. A specialized host may meet residency but not operational-control requirements.

### 5. Availability and integration

Include support hours, service objectives, failover, model rollout, observability, identity, policy enforcement, audit export, and developer-tool compatibility. A provider with a low accelerator price may require an internal team to rebuild missing services. A simple API may be a rational premium when it removes that work.

### 6. Routing accuracy

Record false-cheap routes, where a weak lane fails and escalates, and false-expensive routes, where routine work reaches a frontier model unnecessarily. Include repeated context and review after escalation. Give users an explicit override and capture why it was needed.

### 7. Portability and exit

Test whether prompts, tool contracts, evaluations, logs, policy, and models can move. Specialized optimizations may create lock-in through proprietary runtimes, model formats, caches, or integrations. Price the exit and maintain a degradation path for provider or hardware loss.

## The four-lane bake-off

Select twenty to fifty representative tasks from one coding workflow. Freeze input repositories and define an oracle: tests, security checks, and a review rubric. Include ordinary cases, tails, and tasks expected to need escalation.

Compare a current frontier API, a cheaper managed model, the proposed specialized or dedicated option, and the current non-agent workflow. If a local system is part of the proposal, include it as its own lane. Keep permissions, task instructions, and acceptance criteria equivalent.

For each run, capture:

1. first-pass and final acceptance;
2. defect severity, review minutes, retries, and escalation;
3. input, cached input, and output tokens plus non-token service charges;
4. queue, inference, tool, and end-to-end latency;
5. data path, retention, administrative access, and policy exceptions;
6. availability failures and operator effort;
7. cost per accepted task and per accepted task-hour saved.

Then simulate the router over the same task set. Compare it with an oracle router that knows the outcome in advance and with the simplest “always use one lane” baseline. A complex router that saves little or shifts errors into review is not a middle path; it is an extra system.

Set a reversible promotion rule. For example, promote a defined task class only if its quality floor holds, tail latency and availability meet the service target, data controls pass, operator load is owned, and total accepted-task cost stays within the locally chosen range. Do not copy these words into a universal numeric gate; set values from the workflow’s consequence and alternatives.

## Counterexamples

A low-volume team may rationally use a frontier API because fixed integration and operations dominate. A regulated organization may rationally pay more for dedicated control. A busy enterprise may still reject dedicated infrastructure if demand is spiky or models change faster than hardware can be amortized. A small model may outperform on a narrow, well-instrumented repository task while failing badly on novel work.

Routing can also erode developer trust when behavior varies invisibly. Make the selected lane, limits, and escalation visible. Otherwise users may repeat requests until they happen to reach a stronger model, destroying both the economics and the evaluation.

## Evidence judgment

- **Middle-path proposition:** conditionally supported as an architecture choice, not as a general market result.
- **Infrastructure-price evidence:** moderate for the named, dated scenarios and low for transfer to application TCO.
- **Coding-quality equivalence:** open. No audited same-workload comparison establishes it.
- **Routing benefit:** plausible but unmeasured in this corpus; misclassification is a known boundary.
- **Universal threshold:** absent. No token volume, utilization, or scale cut point generalizes across models, providers, contracts, and workloads.

A credible middle path is therefore discovered, not declared. It is the smallest lane system that passes a local quality, service, control, and exit test—and remains cheaper per accepted outcome after routing mistakes are counted.

Podcast hook: Four identical repository tasks enter four inference lanes. The cheap model wins twice, the frontier model rescues one, and the router quietly spends the savings on a bad escalation.

Continue reading: [Management interlude 31a, “Token and infrastructure economics as governance”](31a-management-token-governance.md), turns the trace, operating model, and lane test into accountable management decisions.
