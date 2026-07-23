# Hybrid Evals and Councils of Judges

Deterministic checks are narrow but repeatable. Model judges can read broad intent but vary, bias, and sometimes reward persuasive nonsense. A hybrid evaluation system uses each where its evidence is strongest:

```text
hard deterministic gates
          ↓
structured semantic judgment
          ↓
disagreement and escalation
          ↓
human or production authority
```

The [2026 Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf) describes a workflow combining deterministic checks with a three-model “council of judges” and reports first-pass acceptance rising from roughly 60% to roughly 80%. The source does not name the system, task population, judges, rubric, aggregator, comparison period, trial count, uncertainty, cost, or downstream quality. This is **anonymous retreat evidence**. The increase must remain an anecdote, not a transferable effect.

The underlying design question is still important: when can several imperfect semantic evaluators add useful evidence after deterministic constraints?

## What a judge contributes

A deterministic gate answers questions that can be executed exactly:

- Did it compile?
- Did required tests pass?
- Was a forbidden file modified?
- Is the schema valid?
- Did the measured value stay below a declared threshold?

A judge can evaluate less reducible questions:

- Does the explanation address the user's actual concern?
- Is a UI flow coherent?
- Does the change appear unnecessarily broad?
- Is the evidence report sufficient for review?
- Which requirement seems omitted?

The judge should not be used merely because prose is present. Some semantic requirements can be converted into executable constraints; some remain accountable human decisions. A judge is an approximate sensor, not a source of authority by default.

## More votes are not automatically more evidence

If three judges make independent errors with known rates, aggregation can reduce error. Real model judges rarely satisfy that clean assumption. They may share:

- model family or training data;
- system prompts and rubrics;
- the generator's summary instead of raw artifacts;
- position, verbosity, and style biases;
- an incomplete requirement;
- tools and retrieval sources;
- the same evaluator benchmark used during selection.

Three outputs may therefore be one mistake repeated three times. Diversity of provider names is not proof of error independence.

A large 2026 preprint tested [21 LLM judges from nine providers](https://arxiv.org/html/2606.19544v1) across MT-Bench, JudgeBench, and RewardBench under agreement, repeatability, and bias protocols: 118 runs and roughly 541,000 individual judgments. Exact-match agreement exceeded chance-corrected Cohen's kappa by 33–41 percentage points on MT-Bench. Judge rankings shifted by as many as 14 positions across benchmarks. High test–retest consistency could coexist with serious position bias.

This is **large multi-benchmark judge evidence** showing that reliability has multiple dimensions. Its domain is English preference judgments, not code acceptance, production safety, or multi-judge councils. It does not estimate council uplift. It does show why “the judge agreed with humans 90% of the time” can mislead when label imbalance, benchmark choice, repeatability, and positional effects are not separated.

## Repeatability is not validity

A judge that returns the same wrong answer is repeatable. A council that unanimously endorses a shared misunderstanding is consistent. Evaluation needs at least four distinct questions:

1. **Agreement:** does judgment match an accountable reference on representative cases?
2. **Repeatability:** does the same judge decide similarly when irrelevant conditions change?
3. **Bias:** does position, verbosity, naming, style, or model identity change the verdict?
4. **Transfer:** does performance persist across task families, time, and generator versions?

The judge study above reports high test–retest figures alongside nontrivial verdict flips and benchmark-sensitive rankings. Those observations make exact protocol reporting essential. They do not imply that every judge is unusable.

[The Verification Horizon](https://arxiv.org/html/2606.26300v1), a Qwen Team paper, studies test rewards, frontend rubrics and interactive judges, user feedback, and an agent evaluator for long-horizon tasks. In the frontend work, ranking correlations could appear high while direct pairwise “battle” agreement between scorers was only about 34–41%. A 104-task long-horizon evaluator study found only moderate agreement and included unparseable reports.

This is **vendor-authored, partly private benchmark evidence**. Model relationships, internal datasets, evaluator prompts, and no independent replication constrain it. It supplies a valuable negative finding: evaluation quality changes with task, prompt, scorer, and protocol even when aggregate rankings look reassuring.

## A safer hybrid architecture

Use four layers of authority.

### 1. Deterministic vetoes

Compilation, permissions, invariant checks, artifact integrity, and critical tests should reject without being outvoted by a model council. A semantic judge must not explain away a failed access-control property.

### 2. Independent semantic views

Give each judge the evidence needed for one bounded rubric dimension. Where practical, vary model family, prompt structure, evidence order, and whether a judge sees the implementation or only behavior. Do not expose another judge's verdict before the independent pass.

### 3. Disagreement policy

Preserve individual scores and reasons. Escalate material disagreement; do not hide it behind an average. Require a judge to cite concrete artifacts, requirement clauses, tests, or runtime observations. “Looks good” is not evaluable evidence.

### 4. Accountable authority

Define what a council pass permits: additional testing, a draft PR, merge, staging, or production. High-consequence decisions retain an accountable owner even when routine semantic triage is automated.

This architecture is a **derived practice proposal**, not a validated universal design.

## Aggregation choices encode policy

Majority vote treats each judge as equally reliable and each error as equally costly. An average score assumes scales are comparable. Unanimity reduces approvals but can amplify one overly conservative judge. A weighted council requires weights that remain calibrated.

Choose aggregation from the error cost:

- use **veto** for a dimension where a false pass is unacceptable and the veto judge is qualified;
- use **majority** only for calibrated, sufficiently independent categorical judgments;
- use **median** for scores where outliers are common and scales align;
- use **escalation** when disagreement itself signals ambiguity;
- use **abstention** when evidence is missing or outside the judge's competence.

Never infer independence by multiplying each judge's headline accuracy. Estimate joint errors on the actual workload and inspect which cases all judges miss.

## Exercise: a shadow council protocol

Select 100–200 historical or live-but-nonauthoritative cases from one task class. Include passes, failures, ambiguous cases, and costly edge conditions. Secure accountable reference labels or adjudications, while recording when humans disagree.

Before running:

- freeze the rubric and evidence packet;
- choose at least two judge configurations with a reason for their difference;
- randomize answer order and remove irrelevant authorship/model labels;
- define pass, fail, abstain, and escalation;
- declare the aggregation rule;
- set cost and latency budgets;
- keep the council in shadow mode.

Measure each judge and the council:

| Dimension | Measurement |
|---|---|
| False pass | bad cases accepted, weighted by consequence |
| False fail | acceptable cases rejected |
| Chance-corrected agreement | kappa or a suitable class-aware alternative |
| Repeatability | reruns with seeds, time, and equivalent formatting |
| Bias | swapped position, verbosity, names, and styles |
| Joint error | cases all judges miss or all reject incorrectly |
| Abstention quality | whether uncertainty concentrates on hard cases |
| Cost | tokens, elapsed time, retries, and human adjudication |

Do not tune indefinitely on the same evaluation set. Split development, validation, and a genuinely untouched test period. Re-run after a generator, judge, rubric, or task-population change. Archive prompts and raw individual verdicts so a result can be reproduced.

Promotion should require a specified improvement over the existing process—perhaps lower human triage while keeping severity-weighted false passes below a threshold. “Acceptance went from 60 to 80” is uninterpretable unless acceptance quality and workload stability travel with the number.

## Failure modes and counterexamples

A council is a poor fit when deterministic rules cover the requirement, when no credible reference exists, when the decision is a nondelegable policy judgment, or when latency and cost exceed the value. A single qualified human may be better than three uncalibrated models. Conversely, one well-validated judge can outperform a decorative council if its rubric, evidence access, and abstention path match the task.

Councils can also cause **automation deference**: a reviewer sees unanimity and searches less for counterevidence. Interface design should surface disagreement, evidence citations, and known blind spots before the aggregate verdict.

The audited conclusion is conditional:

> Hybrid evaluations can combine repeatable hard constraints with broader semantic review, and multiple judges may add value when their joint errors, biases, and costs are measured on the target task. The corpus does not validate the retreat's 60-to-80 increase, prove model independence, or justify replacing accountable human acceptance.

The council's most useful output may not be a vote. It may be a structured disagreement that tells a human exactly where the specification, evidence, or artifact remains ambiguous.

Podcast hook: When three models agree, have you gained three witnesses—or just heard one shared blind spot speaking with three voices?

Continue reading: [Chapter 9 — Manual Code Review Evidence](09-manual-code-review-evidence.md), then Chapters 10–12 for auditability and ownership.
