# 25. Productivity claims and the predicted bubble

No single defensible multiplier describes AI’s effect across the full software lifecycle. The best audited evidence shows heterogeneous effects on bounded tasks and real repositories, with material uncertainty about selection, quality, downstream work, and organizational transfer. The retreat’s “2–3x rather than 10x” estimate and its 12–18-month bubble forecast remain anonymous practitioner judgments, not measured ranges or validated forecasts.

The [Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf) is useful because it challenges extreme expectations and insists on the full lifecycle. It is not independent evidence for a replacement multiplier. Managing expectations downward from one unsupported number to another would preserve the measurement mistake.

## A plain-language model: the productivity ladder

“Productivity” changes meaning as it climbs a ladder:

1. **Output:** tokens, suggestions, lines, tests, or documents produced.
2. **Bounded task:** time and quality for a specified coding, refactoring, documentation, or debugging exercise.
3. **Work item:** elapsed time from accepted requirement to reviewed, integrated change.
4. **Team flow:** throughput, work in progress, queue time, coordination, and rework across many items.
5. **Lifecycle outcome:** release frequency, reliability, security, maintainability, and incident recovery.
6. **Business value:** revenue, cost removed, risk reduced, customer outcome, or strategic option created.

Evidence does not automatically travel upward. Faster first drafts can increase review queues. More code can increase integration and maintenance. A local slowdown can still create better quality or learning. A team-level gain can disappear if demand, approval, release, or operations is the bottleneck.

A useful accounting identity is:

> net lifecycle effect = local acceleration - displaced review, integration, rework, release, and incident cost

This is a conceptual model, not a formula with universally measurable units. Its purpose is to force the missing work back into the claim.

## Controlled and production-like evidence

METR’s [2026 uplift update](https://metr.org/blog/2026-02-24-uplift-update/) is unusually transparent about unstable measurement. The underlying randomized study involved 57 experienced open-source developers, 143 repositories, and more than 800 prespecified tasks with AI allowed or disallowed. Participants had a median of ten years’ experience. An early analysis estimated that AI use made work 19% longer, with an interval from 2% to 39% longer.

Later-source estimates moved toward possible speedups: -18% time for returning developers and -4% for new developers, with both uncertainty intervals crossing zero. METR judged those later estimates unreliable because recruitment, task choice, participation, compensation, and time tracking changed; developers selectively omitted many tasks. This is not evidence that AI has one negative or positive rate. It is evidence that randomized real-work studies remain vulnerable to selection and protocol drift—and that conclusions should weaken when validity weakens.

McKinsey’s [developer study](https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/unleashing-developer-productivity-with-generative-ai) involved more than 40 developers in the United States and Asia over several weeks, using three task categories and both human judges and automated quality checks. Documentation and new-code tasks were reported as substantially faster, refactoring showed large gains, but complex tasks improved by less than 10%; some less-experienced developers were 7–10% slower. The published account does not provide raw data, full assignment details, uncertainty, or downstream maintenance outcomes. It supports task and experience heterogeneity, not a portfolio multiplier.

[RepoRescue](https://arxiv.org/html/2607.01213v1) evaluated real Python and Java repositories rather than timed developer work. Agent success varied with environment access and by agent; combined attempts covered more repositories. Manual audit of apparently successful repairs exposed regressions and scenario failures behind green inherited tests. This is capability and quality evidence, not productivity evidence. It shows why completion counts need a stronger oracle before entering a productivity numerator.

The tiny translation study [*Articulate but Wrong*](https://arxiv.org/html/2605.21537v1) found semantic drift across model-generated Python translations and showed that same-model self-review missed 83 of 262 drift cases. The hand-crafted snippets cannot predict enterprise defect rates. They demonstrate a pathway by which apparent speed becomes human verification and rework.

Consulting and survey evidence adds organizational context but weaker causal force. [Bain](https://www.bain.com/insights/from-pilots-to-payoff-generative-ai-in-software-development-technology-report-2025/) reports rollout and productivity ranges from client work and argues that value depends on changing the broader delivery system. Its public article does not provide the sampling, baselines, or raw outcome data needed to treat those ranges as independent benchmarks. A [Pragmatic Engineer survey](https://newsletter.pragmaticengineer.com/p/the-impact-of-ai-on-software-engineers-2026) gathered more than 900 self-selected responses about tool impact, cost, and limits; it measures perceptions, not controlled lifecycle outcomes. A [systematic mapping and practitioner survey](https://arxiv.org/html/2603.16975v1) synthesized 63 sources and surveyed 65 people, only 30 of them professional developers, with regional and age skews. It illuminates reported practice, not a universal productivity rate.

## Why the studies should not be averaged

Pooling these numbers would create false precision. Their numerators include time saved, tasks completed, repositories repaired, or perceived impact. Their denominators include tiny snippets, prespecified open-source tasks, three experimental task types, and self-selected respondents. Their quality gates range from type-strict semantic oracles to inherited tests, expert judgments, or self-report.

They also answer different causal questions. “Can the tool help on this task?” differs from “Does allowing the tool change experienced-developer completion time?” and from “Did the organization deliver more valuable software?” There is no audited full-lifecycle dataset that turns these into a defensible cross-industry range.

This does not mean nothing can be measured. It means a range belongs to a defined population, workflow, time horizon, and quality contract. An organization can estimate its own distribution; it should not label that distribution “software engineering.”

## Can the bubble be timed?

The retreat predicts that the gap between extreme marketing and delivered value could force a reset within 12–18 months. The audit found no forecasting model, historical base-rate analysis, participant track record, market dataset, or falsification rule supporting that window. It is speculation.

Market reactions do show sensitivity to capability stories. Reuters documented a sharp [IBM share-price fall following Anthropic’s COBOL modernization announcement](https://www.reuters.com/business/ibm-posts-steepest-daily-drop-since-2000-after-anthropic-says-ai-can-modernize-2026-02-24/). That event says narratives can rapidly affect valuation; it cannot reveal the timing or shape of an industry correction.

“Bubble bursts” also lacks an operational definition. It could mean lower vendor valuations, slower spending growth, cancelled pilots, reduced model prices, consolidation, or merely more skeptical messaging while usage keeps rising. Without a defined outcome and observation date, the forecast cannot be scored.

A better planning response is scenario robustness:

- **Capability compounds:** model and tool improvements continue, making verification and organizational absorption the constraints.
- **Expectations reset:** funding becomes more selective, rewarding measured local value and lower operating cost.
- **Uneven absorption:** some workflows improve materially while high-risk or coordination-heavy work remains resistant.

None is assigned a probability here. Verification, cost observability, representative evaluation, and reversible investment retain value in all three.

## The productivity-claim stress test

Before a productivity number reaches an investment case, complete these fields:

- **Unit:** output, task, work item, team flow, lifecycle, or business value.
- **Population:** roles, experience, teams, repositories, and exclusions.
- **Intervention:** model, tools, autonomy, context, training, and permission level.
- **Baseline:** same people and tasks, historical trend, randomized control, or unmatched comparison.
- **Selection:** who chose tasks, who declined, and what was omitted.
- **Time boundary:** setup through first draft, review through merge, or operation after release.
- **Quality contract:** compile, tests, independent scenario audit, security, reliability, maintainability, and user outcome.
- **Displacement:** review, integration, waiting, rework, incidents, and future maintenance.
- **Cost:** licenses, tokens, infrastructure, enablement, oversight, and failed attempts.
- **Distribution:** median, tails, confidence interval, and subgroup effects—not only an average.
- **Decision rule:** what result expands, changes, or stops the intervention.

Then perform a boundary climb. For every claimed gain, ask what evidence permits moving it one rung up the ladder. If a fast coding task has no review or release evidence, stop at “bounded task.” Repeat the measurement after the novelty period and after the tool or policy changes.

## Evidence judgment

- **Bounded-task effects:** moderate confidence that effects are real but highly heterogeneous by task, developer, model, environment, and oracle.
- **Full-lifecycle multiplier:** low confidence; no audited source establishes a transferable range.
- **Retreat’s 2–3x and 10x comparison:** unverified anonymous estimate, not a benchmark.
- **12–18-month reset:** speculation without an auditable forecast method.
- **Durable conclusion:** measure at the decision’s level, preserve quality and displacement costs, report distributions, and plan across scenarios rather than around a date.

The honest answer to “how productive is AI?” begins with “for whom, doing what, under which quality gate, and measured until when?” A responsible range comes after those answers, not before them.

Podcast hook: Two studies point in opposite directions, a vendor promises a multiplier, and a market watcher starts a countdown. The episode rebuilds each claim rung by rung on the productivity ladder.

Continue reading: [Chapter 23, “Stories, benchmarks, and executive learning”](23-stories-benchmarks-executive-learning.md), explains how to communicate bounded results; [Management interlude 25a](25a-management-story.md) governs the narrative without inventing a replacement estimate.
