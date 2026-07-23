# 44. Instrument the two clocks

> **Report point:** Team design, bullet 44, page 12 of the [Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf)
> **Evidence judgment:** This is a diagnostic instrument, not a validated queueing law or productivity score.

[Chapter 13](13-two-clocks.md) introduced a hypothesis: agents can shorten the time to produce a plausible candidate while clarification, review, integration, and acceptance continue on a different clock. The operational question is not whether that story sounds familiar. It is whether a team can locate its actual constraint without rewarding output volume or hiding work downstream.

The safest answer is a small measurement experiment. Trace ordinary changes from accepted intent to trusted operation, separate waiting from active work, and include rejected output, rework, and failures. Do not begin with a target ratio between the clocks. The audited sources provide no production dataset from which such a threshold could be justified.

## A plain-language model: arrivals, service, and consequences

Think of candidate changes as arrivals at a service desk. Reviewers, test systems, product decision-makers, and deployment controls provide different kinds of service. If candidates arrive faster than the constrained service can handle them, work waits or is rushed. If candidate creation is still slow or unreliable, the queue may stay empty and implementation remains the constraint.

This is only a model. A [Stack Overflow account of decision fatigue](https://stackoverflow.blog/2026/05/21/coding-agents-are-giving-everyone-decision-fatigue/) describes much more generated code and a need for several reviewers, but publishes no underlying queue telemetry. A separate [technical account of a multi-agent slowdown](https://towardsdatascience.com/why-adding-more-ai-agents-made-our-system-slower/) identifies fan-out, connection limits, and local compute as constraints in one tuned system. That is a useful counterexample to “more agents always means faster,” not evidence that human review is generally the bottleneck.

Measure three things separately:

- **Candidate time:** active elapsed time from starting implementation to the first candidate that enters an agreed acceptance path.
- **Commitment time:** clarification, waiting, review, validation, integration, and release work needed before the team accepts operational responsibility.
- **Consequence time:** repairs, reversions, incidents, and rediscovery caused after that acceptance.

The end-to-end clock begins when intent is actionable and ends at a predeclared point such as verified production behavior. Changing those boundaries after seeing the numbers makes comparisons meaningless.

## Before the pilot

Run this only where a team can observe work without turning individual activity into performance surveillance. Choose one service or product team, one ordinary class of changes, and a short window—typically enough to see at least a few dozen changes or several weeks of normal variation. Exclude emergency incidents, bulk migrations, and generated dependency updates if their paths differ materially; analyze them separately.

Write a one-page measurement contract with the team:

1. **Question:** for example, “Did faster candidate creation move delay into clarification and review for routine API changes?”
2. **Unit:** a change request, not a commit, prompt, line of code, or agent session.
3. **Start and end:** observable events that people can identify consistently.
4. **Uses:** workflow improvement and capacity planning only.
5. **Non-uses:** no individual ranking, prompt counting, utilization targets, or automated employment decisions.
6. **Retention:** keep aggregated flow data; delete unnecessary person-level traces on a stated schedule.
7. **Owner:** one person responsible for definitions and one team forum that can challenge them.

If these terms cannot be agreed, stop. Ambiguous or coercive telemetry will produce defensive behavior rather than a trustworthy map.

## Define a minimal event trail

Avoid elaborate process mining at first. Add seven timestamps or states to the work item:

| Event | Operational definition |
|---|---|
| Intent ready | Outcome, owner, constraints, and acceptance examples are sufficient to begin |
| Candidate started | Human or agent begins implementation work |
| Candidate submitted | First candidate enters the agreed review/validation path |
| Clarification requested | Work returns upstream because intent or constraints are unresolved |
| Review completed | Required human and automated evidence has been considered |
| Change accepted | Accountable owner authorizes integration or release |
| Outcome checked | Expected behavior is observed, or the observation window closes |

Record state transitions, not every keystroke. For each return loop, tag a small reason set: misunderstood intent, technical defect, missing test, integration conflict, policy failure, dependency, or changed decision. Allow “other” and revisit the categories; forcing every event into a preconceived bottleneck hides discovery.

Capture whether a candidate was substantially agent-produced, assisted, or not assisted only if that classification is reliable and useful. Tool presence is not a treatment assignment. Task mix, codebase familiarity, reviewer availability, and risk level can explain timing differences, so preserve them as context rather than claiming causality.

## Build the dashboard around flow, not output

Use distributions and counts, not a single average. Median and a high percentile make skew visible, while the count shows whether the sample is credible.

- **Candidate latency:** intent-ready to first candidate, split into active time and waiting where possible.
- **Commitment latency:** candidate submission to acceptance, with clarification, review, validation, and queue time separated.
- **End-to-end latency:** intent-ready to outcome check.
- **First-pass acceptance:** candidates accepted without a return loop, reported with the denominator.
- **Rejection and rework:** returned candidates, loops per change, and active repair time.
- **Queue age and work in progress:** how many changes wait at each state and for how long.
- **Batch size:** changed files or another domain-appropriate size measure; never reward line count.
- **Reviewer load:** concurrent reviews, interruption count, and sampled active review time at team level.
- **Quality guardrails:** rollback, escaped defect, incident, failed deployment, and support work within a declared observation window.

The classroom and interview evidence audited in [Chapter 13](13-two-clocks.md) observes changed workflow and help-seeking, not production queues. Its role is to justify looking for relocated work, not to define a dashboard threshold. No selected source jointly measures candidate volume, reviewer capacity, queue time, rejection, context switching, defects, rework, and end-to-end production delivery.

## Run a bounded four-step experiment

First, collect a baseline without asking people to work differently. Missing timestamps and disagreement about states are findings: they show that the team cannot yet distinguish candidate speed from trusted delivery.

Second, introduce one change at a time. Examples include limiting simultaneous candidates, moving an acceptance-example conversation earlier, assigning review capacity explicitly, or narrowing the agent’s task. Do not simultaneously change model, review policy, team structure, and deployment process; attribution will be impossible.

Third, compare matched work classes over repeated windows. Ask whether candidate latency, commitment latency, total latency, rework, downstream failure, and reviewer burden moved together. A shorter candidate clock with unchanged end-to-end time means work probably moved or another constraint dominates. A shorter total clock with stable quality guardrails is more encouraging. A faster merge followed by more repair is not an improvement.

Fourth, review five actual traces as a team. Aggregate charts reveal a pattern; traces explain it. Include at least one fast success, one slow change, one rejected candidate, one non-agent change, and one change that contradicted the favored story.

## Interpret combinations, not isolated numbers

If candidate latency falls while queue age, rework, and reviewer interruptions rise, reduce candidate work in progress or strengthen upstream specification before adding review labor. If both clocks improve and quality remains stable, preserve the practice but keep sampling consequence time. If candidate latency remains dominant, improve context, tools, task decomposition, or implementation capability rather than inventing a decision problem.

If commitment time is high because a required decision-maker is unavailable, more reviewers will not help. If validation systems dominate, invest in test speed and reliability. If clarification loops dominate, refine intent and examples. If defects dominate after acceptance, the measured end point is too early or the gate is weak.

These interpretations are hypotheses. The two clocks do not prove that a particular organizational intervention will work, and no selected source supplies a universal candidate-to-review ratio.

## Anti-gaming and failure signals

Every metric invites adaptation. Candidate time can be shortened by submitting rougher work. Review time can be shortened by rubber-stamping. Queue size can be reduced by keeping work invisible. Defect counts can fall when reporting becomes costly. Counter these incentives by reviewing metric pairs: speed with first-pass acceptance, merge time with downstream repair, and queue size with untracked work discovered in trace reviews.

Stop the pilot immediately if it becomes an individual leaderboard, encourages oversized batches, suppresses incident reporting, or requires collecting private prompt content unrelated to the flow question. Pause and repair definitions when more than a small, predeclared share of items cannot be classified consistently, or when teams route work around the instrument.

Rollback is simple: remove the added workflow fields, preserve only agreed aggregates, delete unneeded person-level data, and return to the prior work policy. If an intervention increased rework, failures, or reviewer burden across two review windows, restore the previous limit or gate before trying another change. Do not wait for statistical theater while operational harm accumulates.

## The practical artifact: a two-clock review card

At the end of each measurement window, complete this card:

- What work class and denominator did we observe?
- Which state held the oldest queue?
- Did active work or waiting dominate that state?
- What happened to rejections, rework, and consequence time?
- Which people or systems absorbed extra load?
- Which trace falsified our preferred explanation?
- What one change will we test next?
- What result triggers stop or rollback?

The result should be a local decision, such as “limit routine candidates to three because review age and rework rose,” not a claim that agents universally outrun teams. The evidence gap is the reason to instrument both clocks; the instrument must not be mistaken for evidence that the hypothesis is already true.

Podcast hook: When the patch arrives in minutes but the outcome arrives next week, which timestamp exposes the real constraint—and which metric merely rewards haste?

Continue reading: [Chapter 13: The two clocks of agentic delivery](13-two-clocks.md) explains the evidence and limits behind this operational instrument.
