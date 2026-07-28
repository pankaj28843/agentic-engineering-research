# 15. Evaluation systems: tests for a probabilistic product

An eval is an instrument that turns an input, system version, and acceptance
definition into recorded evidence. An evaluation **system** owns datasets,
rubrics, runners, judges, human calibration, slices, release gates, and
production feedback over time.

The goal is not one impressive benchmark. It is a regression loop that tells
engineers what changed, for whom, and whether the product should ship.

## ELI5: a weather station, not one thermometer

A thermometer can be precise and incorrectly calibrated. It can also measure
temperature perfectly while a farmer needs rainfall and wind.

An eval judge is a measuring instrument. First define the property, then
calibrate the instrument, then use several instruments where failure has
different dimensions.

## Start from failures and decisions

Write a failure taxonomy before selecting a framework:

- factual or grounded error;
- missing or wrong tool action;
- invalid structured output;
- instruction or policy violation;
- unsafe content or data disclosure;
- poor usefulness/style;
- excessive latency or cost;
- failure to abstain;
- multi-step trajectory failure.

For each, ask: what release decision would this measurement change? A metric
with no owner or action threshold becomes dashboard decoration.

## The evaluation pyramid

### Layer 1: deterministic contracts

Use code when the rule is exact:

- parse/schema validation;
- expected tool name and argument bounds;
- forbidden data or dependency;
- citation ID resolves;
- arithmetic and state invariants;
- latency/cost budgets;
- no mutation in a read-only run.

These checks are cheap, reproducible, and easy to debug.

### Layer 2: task golden set

Maintain human-curated examples with expected outcomes, relevant variants,
slice labels, consequence, and provenance. Include ordinary traffic, tails,
known incidents, unanswerable cases, adversarial cases, and ambiguous cases.

The provisional representative sets in Chapters 2 and 8 and the retrieval
records in Chapter 14 now become governed slices of this versioned dataset.

A small set is a CI sentinel, not a population reliability estimate. Grow it
from production failures without letting near-duplicates dominate.

### Layer 3: calibrated semantic evaluation

Use domain reviewers, pairwise preferences, rubrics, or LLM judges for
semantic qualities. Preserve disagreement rather than forcing every case into
false certainty.

### Layer 4: trajectory and system evaluation

Test tool faults, retries, state transitions, budgets, routing, retrieval,
recovery, and side effects. Final-answer quality alone can hide a dangerous
path.

### Layer 5: online outcomes

Shadow traffic, canaries, user corrections, task completion, escalation,
incidents, retention, and business outcomes test whether offline improvements
transfer.

## Golden-set design

Stratify by:

- task and user journey;
- language and locale;
- input length and complexity;
- tenant/product/version;
- answerable versus unanswerable;
- risk/consequence;
- model/tool/retrieval dependency;
- recent distribution and known failure classes.

Keep a stable regression core plus a rotating recent sample. Separate
development and holdout cases. Record label source, date, reviewer expertise,
and disagreement.

The reproducible preprint
[Daniel Commey, “When Generic Prompt Improvements Hurt: Evaluation-Driven Iteration for LLM Applications”](https://arxiv.org/html/2601.22025v2)
demonstrates that generic prompt additions can improve one suite and regress
another. In one small local setup, a RAG compliance slice fell from 26/30 to
9/30 under a changed condition. The exact result is bounded by two quantized
models, synthetic expansions, and its checks; the mechanism supports
task-specific regression testing, not a universal prompt rule.

## Validate the judge

An LLM judge can be:

- consistent but systematically wrong;
- correlated overall but poor on a critical slice;
- sensitive to answer order, rubric order, label names, or verbosity;
- changed silently by a hosted endpoint update.

[Justin D. Norman, Michael U. Rivera, and D. Alex Hughes, “Reliability without Validity”](https://arxiv.org/html/2606.19544v1)
evaluates 21 judges across three benchmarks using 541,000 judgments. It shows
that raw exact agreement can look much better than chance-corrected agreement
and that rankings shift by benchmark. The study is large for its protocol but
still covers English text and inherited labels over a five-week hosted-model
window.

Use:

- a human-labelled calibration set;
- Cohen’s kappa, Krippendorff’s alpha, or another chance-aware agreement
  measure in addition to raw agreement;
- repeated judgments;
- answer-order swaps;
- rubric-order and label-renaming metamorphic tests;
- slice-level false-positive/false-negative review;
- version-pinned judge prompt and endpoint metadata.

The preprint
[Qingquan Li and colleagues, “Evaluating Scoring Bias in LLM-as-a-Judge”](https://arxiv.org/html/2506.22316v4)
demonstrates large score changes under semantically irrelevant rubric
perturbations for some judges. Its stress-test rates are not normal production
failure rates. They are a recipe for falsifying an unsafe assumption.

## Recompute what code can recompute

If a judge returns subscores and a weighted total, calculate the total in code.
If it returns JSON, schema validate it. If a rubric says “zero when no
citation,” enforce that rule deterministically.

[Hamid Ona on Microsoft Tech Community, “Evaluating the Evaluator”](https://techcommunity.microsoft.com/blog/educatordeveloperblog/evaluating-the-evaluator-how-to-test-an-llm-judge-with-microsoft-agent-framework/4516639)
provides a transparent small example: a judge was repeatable and structurally
well behaved but only moderately calibrated to ten human-labelled examples.
The tiny, author-labelled sample prevents generalization; the separation of
process reliability from validity is the useful pattern.

## A release comparison, not a score dump

For candidate versus baseline, report:

- paired outcome per case;
- wins, losses, unchanged, and severity;
- confidence interval or bootstrap uncertainty where meaningful;
- results by predeclared slice;
- deterministic contract failures;
- latency and cost distributions;
- route, retry, and fallback effects;
- new failure examples for human inspection.

Do not average safety and style into one score that permits a prettier answer
to offset data leakage. Some dimensions are hard gates.

Account for repeated sampling. Temperature zero does not guarantee identical
hosted-model output. When variance matters, run enough repeats to estimate it
or choose a robust paired protocol.

## CI, shadow, canary, monitor

An evaluation progression:

1. **Local/PR:** fast deterministic tests and small regression core.
2. **Pre-merge or nightly:** broader semantic and adversarial suite.
3. **Shadow:** run the candidate on sampled production inputs without serving
   its output.
4. **Canary:** expose a small eligible population with rollback.
5. **Production:** monitor task outcomes, drift, sampled quality, and incident
   signals.

Each gate records prompt, model, retrieval, tool, router, dataset, judge, and
code versions. A model alias without a resolved revision weakens
reproducibility.

The Hacker News thread
[“About AI Evals”](https://news.ycombinator.com/item?id=44430117)
contains practitioner reports that apparently stronger model releases can
regress tuned applications. The thread is anecdotal and includes product
affiliations; it supports local measurement, not any named tool.

Suraj Sharma’s X post,
[@suraj_sharma14, “Golden datasets and evaluation systems”](https://x.com/suraj_sharma14/status/2081273315901964705),
is retained as a July 2026 curriculum/adoption signal. Its long checklist is
not evidence that every framework or activity should be adopted at once. The
learning order in this chapter deliberately starts with contracts and a
golden set before judge pipelines and public dashboards.

## Worked example: support summarization release

A candidate model is cheaper and scores higher with an LLM judge.

Before routing traffic:

1. run deterministic checks for missing case IDs, invented actions, and
   forbidden personal data;
2. compare paired human labels on common, long, multilingual, and severe-case
   slices;
3. calibrate the judge and run order/verbosity perturbations;
4. measure whether the candidate compresses rare severe issues into generic
   prose;
5. shadow recent traffic and compare escalation recommendations;
6. canary with rollback and monitor agent correction time, not only thumbs-up.

The cheaper model wins only if accepted-summary cost and operational outcomes
improve within hard safety gates.

## Interview checkpoint

**Question:** “How would you build evals for an LLM application?”

A strong answer begins with task and failure taxonomy, then layers
deterministic checks, a stratified versioned golden set, human rubrics,
calibrated/stress-tested LLM judges, trajectory tests, paired release
comparisons, shadow/canary rollout, and online business outcomes. It separates
reliability of the measurement from its validity.

**Explain it back:** How can a judge have 95% repeatability and still be unsafe
as a release gate?

## Capstone increment

Build the assistant's release plan: deterministic schema/policy/ACL gates, a
stratified versioned core set, calibrated semantic review, trajectory and
concurrency faults, paired comparison, shadow, canary, rollback, and online
outcomes. Import Chapter 14's records and mark high-consequence failures as
hard gates rather than averaging them away.

**Definition of done:** one deliberately unsafe candidate scores well on an
aggregate metric but is correctly blocked by a named hard gate, with dataset,
runner, judge, and system versions recorded.

Next: [Observability](16-observability.md) connects every evaluation and
failure to the request path that produced it.
