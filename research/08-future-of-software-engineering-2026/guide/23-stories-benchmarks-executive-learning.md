# 23. Stories, benchmarks, and executive learning

Leaders need three kinds of evidence at once: a story that makes a mechanism understandable, a benchmark that bounds how often and how much it works, and local telemetry that shows whether it works in their organization. None can substitute for the other two.

The [Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf) argues for vivid storytelling, peer benchmarks, fact-checking of “10x” claims, and hands-on exercises that let executives encounter real limits. This is sensible practice advice from an anonymous participant synthesis. The audited corpus did not contain a controlled study showing that this particular executive-learning intervention improves investment decisions. The chapter therefore treats it as a design hypothesis and builds checks around its known failure modes.

## A plain-language model: story, rate, reality

A story answers, “How could this happen?” It carries sequence, context, and stakes. A live demonstration can reveal how an agent searches, guesses, calls tools, recovers from an error, or fails behind a polished interface.

A benchmark answers, “Under specified conditions, how often did this happen?” It requires a task set, baseline, participants or agents, model and tool configuration, oracle, trial count, quality gate, and uncertainty. It trades context for comparability.

Local telemetry answers, “What is happening here?” It connects adoption to review effort, queue time, escaped defects, incidents, spend, and business outcomes in the organization’s actual constraints.

Call this the **story–rate–reality triangle**. A story without a rate becomes an anecdote. A benchmark without a story invites false transfer from a narrow task. Local telemetry without either can identify a change without explaining it or establishing a counterfactual.

Executive learning should move around the triangle. The objective is not to make leaders prompt engineers for an afternoon. It is to improve the questions they ask before allocating money or changing risk.

## Why vivid evidence is powerful—and dangerous

Narratives can move decisions before the underlying capability is settled. Reuters reported that [IBM shares fell 13.2% on February 24, 2026](https://www.reuters.com/business/ibm-posts-steepest-daily-drop-since-2000-after-anthropic-says-ai-can-modernize-2026-02-24/) after Anthropic published a claim about reducing the COBOL modernization cost barrier. The market reaction is observable; it does not validate the modernization claim or establish why every investor traded. It is evidence that a vivid capability narrative can produce material responses.

Demonstrations are selected performances. A presenter chooses the task, prepares the environment, knows the successful path, and may omit failed runs. Even a candid executive exercise creates only a sample of one. A leader who struggles with an unfamiliar repository may infer that agents are useless; one who generates an attractive prototype may infer that production delivery is solved.

The right response is not to ban stories. Stories make invisible work legible: missing context, permissions, flaky environments, review, integration, and rollback become concrete. The safeguard is to attach an **evidence card** and a **counter-story**. Show a success beside a representative failure or boundary case. Tell the audience what was selected, what was rehearsed, what the system could access, and what happened after the visible output.

## Benchmarks change meaning when their unit changes

The audited studies illustrate why leaders must inspect the measurement contract.

[RepoRescue](https://arxiv.org/html/2607.01213v1) evaluated agents on 193 Python and 122 Java repositories. Environment access improved repair outcomes, and different agents succeeded on different repositories. Yet manual audit of 34 apparently successful unmaintained Python projects found that only 12 contained meaningful compatibility patches; five regressed and seven failed a more realistic scenario. The benchmark is valuable precisely because it distinguishes source-only and full-environment conditions and then audits the oracle. It measures repository compatibility rescue, not new-product delivery or organizational productivity.

[*Articulate but Wrong*](https://arxiv.org/html/2605.21537v1) ran 1,980 translations of 60 tiny Python 2 snippets with 11 models. Semantic drift occurred even when outputs were fluent, and same-model self-review missed nearly a third of identified drift cases. This is strong evidence for one failure mechanism under a type-strict oracle. It is not a rate for enterprise migration because the programs were hand-crafted and at most ten lines long.

An ACM paper on [LLM-generated documentation in five BNP Paribas applications](https://dl.acm.org/doi/full/10.1145/3786170.3788390) separated fidelity and functional-vocabulary coverage. Single-pass summaries could score highly on fidelity while covering almost none of the functional vocabulary; orchestration improved coverage but introduced cascading abstraction risk. The result concerns retrospective documentation, not code correctness. Its executive lesson is that one attractive aggregate can conceal a missing dimension.

METR’s [2026 uplift update](https://metr.org/blog/2026-02-24-uplift-update/) is unusually useful for measurement humility. Its broader study involved 57 experienced open-source developers, more than 800 prespecified tasks, and randomized AI-allowed or AI-disallowed conditions. The early result estimated that AI lengthened work by 19%, with uncertainty from +2% to +39%. Later-source estimates suggested possible speedups for some groups, but METR judged the later signal unreliable because participation, task selection, and time tracking changed; confidence intervals crossed zero. The organization did not protect a neat headline from inconvenient validity problems.

McKinsey reports a [study of more than 40 developers](https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/unleashing-developer-productivity-with-generative-ai) performing three task types over several weeks. Documentation and new-code tasks were substantially faster, while complex tasks saw gains below 10%, and some less-experienced developers were slower. The study used judges and automated quality checks, but the published account lacks raw data and enough design detail for reproduction. It supports task heterogeneity, not a full-lifecycle estimate.

These studies do not conflict merely because their headline numbers differ. They ask different questions with different people, tasks, tools, oracles, and time boundaries.

## The missing evidence for executive exercises

The retreat suggests structured hands-on exercises. In the audited source set, no study randomized leaders to a demo, a benchmark briefing, a hands-on exercise, or a combined intervention and then measured decision quality. We therefore do not know whether hands-on exposure improves calibration, for whom, for how long, or under what facilitation.

A defensible exercise should be treated as a local experiment. Measure calibration rather than delight. Before the exercise, ask participants to predict completion time, review burden, failure modes, and deployability. Afterward, ask them to revise those predictions and explain the evidence. Revisit the same forecasts after independent review or production use. A more confident answer is not necessarily a better-calibrated one.

Executives should not be asked to impersonate experienced engineers. Give them a decision role: approve a deployment after inspecting evidence, choose which claim needs replication, or allocate a capped pilot budget. That tests whether the communication changes governance behavior rather than prompt dexterity.

## The evidence translation card

Attach this card to every demo, benchmark slide, and capability story:

### Claim

- What exact decision is this evidence meant to inform?
- Is the claim about task speed, output quality, team flow, cost, risk, or business value?
- Is it an observation, causal estimate, inference, forecast, or recommendation?

### Population and task

- Who or what was tested, on which task set?
- How were tasks and examples selected?
- What system, model, tools, context, and permissions were available?
- How similar is the target organization?

### Comparison and oracle

- Compared with what baseline and over what period?
- How many trials or participants were included?
- Who judged success, and could the output compile, run, pass scenarios, and survive review?
- What uncertainty or distribution sits behind the average?

### Full boundary

- Were setup, prompting, retries, human review, integration, release, rework, and incidents counted?
- What cost and token boundary was used?
- Which quality, security, and operational outcomes were omitted?

### Narrative controls

- What was rehearsed or selected?
- Show one failure, counterexample, or excluded case.
- What result would change the recommendation?
- When will local telemetry replace the borrowed benchmark?

For a practical meeting exercise, give small groups the same agent demonstration but three different cards: complete, incomplete, and misleading. Ask each group for an investment decision and confidence level, then reveal the differences. The exercise tests sensitivity to evidence quality. It does not claim to prove durable executive learning.

## Evidence judgment

- **Communication mechanism:** moderate confidence that combining mechanism-rich stories, bounded benchmarks, and local telemetry produces a more inspectable argument than any one alone.
- **Effect of hands-on executive exercises:** low confidence. The audited corpus contains a recommendation, not an outcome evaluation.
- **Benchmark lesson:** high confidence that task, oracle, environment, selection, and lifecycle boundary materially change interpretation; multiple empirical sources demonstrate this directly.
- **Counterevidence:** vivid stories can amplify selection bias; aggregate benchmarks can conceal dimensions; hands-on trials can create a fresh anecdote rather than a base rate.
- **Unresolved question:** which communication intervention produces better-calibrated executive decisions when tested against later program outcomes?

The management skill is not choosing stories over metrics. It is making every story carry its measurement contract—and making every metric answer a real decision.

Podcast hook: Put an executive, a dazzling agent demo, and a benchmark with an incomplete oracle in the same room; the mystery is not whether the demo works, but which investment story survives the evidence card.

Continue reading: [Chapter 25a, “Manage the story, not just the metric”](25a-management-story.md), turns this evidence discipline into a management routine; [Chapter 25](25-productivity-hype-bubble.md) audits lifecycle-productivity claims.
