# 12. Evaluate the Policy, Not Just the Models

## ELI5 hook

A school does not evaluate a bus service by testing only the engine in a
garage. It checks whether the right children board the right bus, whether the
bus arrives on time, whether the route obeys traffic rules, and whether a
child who misses a stop is helped. A model score is the engine test. A routing
policy evaluation tests the journey.

The policy chooses who gets which route, under which constraints, with which
fallback and acceptance threshold. Evaluation must therefore include policy
decisions, service conditions, outcomes, and counterfactual baselines. A
strong average model can be badly routed; a weaker model can be correct for a
small low-risk stratum.

## Mechanism: replay, shadow, canary, rollback

Freeze a stratified evaluation set with request IDs, context snapshots,
expected authority/data class, acceptance rubric, and provenance. Evaluate
the fixed baseline ladder and the candidate policy on the same set. Version
the route policy, registry, prompts, validators, judges, and price snapshot.

Use four stages:

1. **contract test:** unknown routes, missing identity, stale registry,
   invalid schema, privilege edges, budget reserve, and unreachable states;
2. **offline replay:** accepted outcomes, coverage, false-cheap and
   false-expensive decisions, latency/cost simulation, and slice uncertainty;
3. **shadow:** candidate decisions and traces beside live baseline with no
   user-visible effect; compare live queues, capacity, and cache behavior;
4. **canary:** named low-consequence cohort, fixed exposure, owner, stop
   thresholds, kill switch, and a tested return to the baseline.

The evaluator is a measurement instrument. A semantic judge needs examples,
human calibration, order and verbosity stress tests, and an independent
holdout. Use deterministic checks for schema, citations where machine-checkable,
authorization, and business invariants. Preserve `abstain`, `blocked`, and
`indeterminate`; a judge cannot turn them into successes merely because the
answer is fluent.

Report by stratum and route:

```text
coverage and acceptance
quality and safety failures
cost per accepted outcome
escalation, rework, and abstention
queue, p95/p99 latency, and capacity
cache hit/error and batch completion
policy, registry, and validator drift
```

Benchmark surfaces such as [SWE-bench](https://www.swebench.com/), [Aider](https://aider.chat/docs/leaderboards/),
and [Artificial Analysis](https://artificialanalysis.ai/leaderboards/providers)
can inform task or provider comparisons. Their results are time- and
method-dependent. [Mastra's evaluation account](https://mastra.ai/articles/ai-agent-evaluation)
is a practitioner prompt to treat evaluation as a system. None replaces the
enterprise acceptance contract.

## Worked example: a policy release gate

Assume a **proposed** release policy for a server-side assistant. The frozen
set contains 1,000 requests across routine, multilingual, long-context, and
tool-proposal strata. The fixed Always-Mid baseline clears the acceptance floor
on routine work but misses the multilingual and proposal floors. The candidate
router may choose efficient or capable readonly routes after `R1`; proposals
remain on the capable route and require approval.

The release gate could require:

| Gate | Proposed threshold | Evidence |
|---|---|---|
| coverage | no protected stratum loses more than a pre-registered small margin | paired replay with abstentions counted |
| acceptance | each protected floor holds; no unauthorized effect | deterministic and human-calibrated checks |
| economics | cost per accepted outcome improves against Always-Mid and direct capable baseline where both pass | route ledger with price snapshot and rework |
| latency | p95 route class remains within its proposed budget | shadow load with production-shaped contexts |
| integrity | zero cross-tenant cache or residency violations | injected identity, policy, and cache tests |
| rollback | kill switch returns to the fixed baseline within the stated deadline | canary exercise and incident log |

Suppose the replay passes, but the shadow run shows a 20% escalation increase
for long-context requests because the live context builder adds retrieved
policy pages. The release does not pass. The offline model result was valid for
its frozen context; the policy is not ready for live traffic. Add the context
shape to the route features or change the route envelope, then rerun the
replay and shadow. Preserve the failed evidence.

## Failure drill: a green aggregate and a red protected slice

The canary reports 93% aggregate acceptance, above a 90% target. A restricted
residency slice has two blocked requests routed to an unqualified fallback
because the evaluator did not include that policy combination. An average
quality score and a green latency chart mask a hard boundary violation.

Make protected slices first-class release gates. The policy gate must run before
the model and fallback. Add cross-tenant, residency, and stale-registry cases
to the frozen set. A hard-gate violation rolls back even when aggregate
economics improve. If the exact failure's effect is uncertain, enter the
indeterminate state, stop new side effects, and reconcile with the owning
system.

The [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
and [EU AI regulatory framework](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)
provide governance context for documenting risk and controls. They are not a
substitute for legal advice or a test of this particular route. [OpenTelemetry
GenAI observability](https://opentelemetry.io/blog/2026/genai-observability/)
supports trace vocabulary; the enterprise still decides redaction and
retention.

## Reader exercises

1. Write a policy release matrix with four strata, five baseline policies,
   acceptance floors, cost, latency, and safety gates.
2. Design an independent evaluator test. Vary answer order, verbosity,
   rubric wording, and model judge. State what remains human-calibrated.
3. Add one live-only failure to the shadow plan: changed context length,
   queue saturation, cache policy update, or provider rate limit.
4. Write three rollback triggers and the exact baseline they restore. Include
   registry expiry and an indeterminate side effect.

## Independent evidence and drift

A policy evaluation needs independence at several levels. The baseline should
be frozen before the candidate result is read. The semantic evaluator should
not be the same prompt or route that produced the answer when its judgment
would determine promotion. The holdout should contain examples that the
router did not use for threshold tuning. The human rubric owner should be
able to inspect disagreements rather than receiving only an aggregate score.

Use an evidence ledger with a row for every release claim:

```text
claim → route/policy version → source or fixture → metric
      → workload scope → uncertainty → owner → expiry/review date
```

For a claim such as “the routed policy reduces cost,” the row must name the
baseline, traffic mix, accepted denominator, retry and human-work treatment,
price snapshot, and confidence range. For “the route is residency safe,” the
row must point to the policy and contract test that checks every classifier,
worker, fallback, cache, and trace egress. A benchmark score alone cannot
support either claim.

Drift has several forms. Traffic drift changes strata proportions. Context
drift changes length, retrieval, language, or tool shape. Provider drift
changes price, rate limits, or model behavior. Label drift changes the
acceptance rubric. Operational drift changes queue and capacity. Detect each
with the signal it can actually observe, and map an alarm to a response:
recalibrate, reduce exposure, return to the baseline, or block a protected
class.

Canary evidence should remain reversible. Keep the old route available until
the accepted-cost and quality ledger has settled over enough representative
traffic. A temporary win during an easy launch week is not a durable result.
If the candidate wins only when the evaluator is generous or users do the
repair invisibly, record that finding and reject promotion. A failed policy
test is valuable because it tells the next owner which assumption was false.

## Promotion review as a scientific record

At promotion time, keep the hypothesis, data, method, result, and limitation
together. The hypothesis might be “routing low-ambiguity readonly requests
will reduce accepted cost while holding coverage.” The data names the frozen
set and live shadow. The method names the baseline, route registry, rubric,
price snapshot, and exposure. The result gives the stratum table and
uncertainty. The limitation says what was not observed.

This structure prevents a benchmark or vendor claim from becoming a local
forecast. It also helps future owners understand why a route was accepted even
if prices or models change. A review date is part of the result because the
policy's inputs are not static.

If evidence disagrees, preserve the disagreement. An evaluator may show a
quality win while users spend more time correcting outputs. A latency test may
favor a managed route while security excludes it for a protected class. The
decision should state which hard constraint resolved the conflict and what
measurement could reopen it.

## Checkpoint

The policy evaluation is ready when a candidate can lose cleanly. The frozen
baseline, holdout, protected slices, hard gates, evaluator calibration, and
rollback test must all be visible. The reader's artifact is a release matrix
where cost, quality, latency, coverage, security, and state reconciliation
have separate columns. An aggregate green result cannot override a single
unacceptable boundary violation.

## Source slot

Use [SWE-bench](https://www.swebench.com/), [Aider](https://aider.chat/docs/leaderboards/),
and [Artificial Analysis](https://artificialanalysis.ai/leaderboards/providers)
for bounded comparison context; [Mastra](https://mastra.ai/articles/ai-agent-evaluation)
for evaluation practice; [NIST](https://www.nist.gov/itl/ai-risk-management-framework)
and the [EU framework](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)
for governance context; and [OpenTelemetry](https://opentelemetry.io/blog/2026/genai-observability/)
for observability vocabulary. The release gates are proposals until executed.
