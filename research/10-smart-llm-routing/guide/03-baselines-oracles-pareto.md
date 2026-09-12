# 3. Prove the Router Earns Its Complexity

## ELI5 hook

Before buying a complicated conveyor belt, a warehouse measures the old
process, a simple conveyor, and a skilled worker. It also imagines a perfect
dispatcher who knows the future. The perfect dispatcher helps explain how much
room remains, but nobody can hire it. The new conveyor earns a place only when
it beats the simple options on the work that matters.

A router is a policy intervention with overhead: classification, feature
collection, registry lookup, logging, validation, and sometimes an extra model
call. Its diagram is not evidence. The comparison must use the same requests,
the same acceptance contract, the same price snapshot, and the same failure
accounting for every policy.

## Mechanism: a baseline ladder and an oracle gap

Start with a named ladder:

1. deterministic workflow where a model is unnecessary;
2. always-capable single model;
3. always-efficient or content-free fixed model that meets the minimum quality
   floor, often called the Always-Mid baseline;
4. fixed sequential cascade with a declared acceptance signal;
5. deterministic parallel or specialized workers where the workflow needs it;
6. one model plus an independent verifier;
7. candidate router or supervisor-worker policy.

The order matters. A router must beat the simplest fixed candidate that clears
the acceptance floor, not only a weak baseline selected for convenience. The
content-free baseline is a useful adversary: if it performs as well as a
semantic router, the semantic machinery may be unnecessary.

Run paired replay. Feed the same frozen request IDs to every policy, with
identical context snapshots and a recorded price, capacity, and model registry
version. Measure:

```text
acceptance rate by stratum
cost per attempted request
cost per accepted outcome
false-cheap failures and false-expensive choices
escalation, repair, human rework, and abstention rates
p50/p95/p99 latency and hard-gate violations
```

The **oracle** is a diagnostic policy that sees the best route outcome in
retrospect. Its cost-quality point can bound the opportunity gap. It is not
deployable because it uses information unavailable before execution. A
candidate router should narrow the oracle gap without turning hindsight into a
claim of capability.

Use uncertainty that matches the measure. Bootstrap request IDs within strata
when a simple interval is sufficient. Preserve rare high-consequence failures
even when they make the interval wide. “Not enough data” is a result. Do not
convert it into a confident ranking.

## Worked example: an illustrative 100-request replay

Assume a fixed workload of 100 requests: 60 routine summaries, 25 multilingual
policy lookups, and 15 readonly tool proposals. The following table uses an
arbitrary cost unit and **illustrative measurements**. Every policy sees all
100 requests; a failed or abstained attempt is not removed from the traffic
mix.

| Policy | Accepted outcomes | Total route cost | Cost per accepted outcome | p95 latency | Hard-gate violations |
|---|---:|---:|---:|---:|---:|
| Always-capable | 90 | 180 | 2.00 | 8.0 | 0 |
| Always-Mid, content-free | 84 | 84 | 1.00 | 4.2 | 0 |
| Fixed efficient→capable cascade | 87 | 113 | 1.30 | 6.1 | 0 |
| Candidate router | 90 | 120 | 1.33 | 5.4 | 0 |

Suppose the registered acceptance floor is 88% for this protected replay. The
Always-Mid policy is cheap but fails the floor. The cascade also fails it. The
candidate router ties Always-capable on accepted outcomes, clears the floor,
and lowers cost per accepted outcome from 2.00 to 1.33. Under these assumptions
it earns a shadow experiment. It has not yet earned production: the table says
nothing about distribution shift, live queues, cache isolation, side-effect
reconciliation, or an independent holdout.

Now add a second month with 80 routine requests and 20 policy lookups. The
Always-Mid policy may look better because the mix is easier. That does not
invalidate month one; it changes the denominator. Report both the stratum
results and a clearly declared traffic-weighted result. If a policy silently
rejects hard requests, its acceptance rate can look better while its useful
coverage falls. Require an acceptance-rate and coverage floor alongside cost.

The [IBM routing benchmark page](https://research.ibm.com/publications/large-language-model-routing-with-benchmark-datasets)
is useful for the idea that routing needs benchmark data, while the papers in
the [source index](../source-index.md) supply different empirical objectives.
Read [Aider's leaderboard](https://aider.chat/docs/leaderboards/) and
[Artificial Analysis](https://artificialanalysis.ai/leaderboards/providers) as
comparison surfaces with time, task, and method limits. They help choose what
to test; they are not an oracle for this enterprise.

## Failure drill: a 30% saving after the traffic changed

A report compares January's always-capable mix with February's routed mix and
claims 30% savings. January had many long policy questions; February had mostly
short summaries after a product launch changed the traffic. The policy was
also allowed to abstain on long requests. The comparison is confounded by mix
and coverage.

Re-run paired requests or reweight to a frozen reference mix. Show the result
by stratum and include abstentions, escalations, and human rework. If the
router is cheaper only when it declines the expensive work, call that a
coverage change, not an economic win. If the router's gain disappears against
Always-Mid, delete the router or find the specific unmet requirement that
justifies its overhead.

## Reader exercises

1. Make a five-row baseline table for one workflow. Name the candidate that
   must be beaten before a router is allowed into shadow.
2. From a toy replay, count false-cheap outcomes: requests for which a cheap
   route failed or escalated while a qualified alternative would have passed.
   Count false-expensive choices: accepted cheaply but sent to a more costly
   route.
3. Design an oracle diagnostic. Write down the information it uses that a
   production router cannot see. Remove that information from the candidate
   policy.
4. State the one measured condition that would justify adding the router's
   classification cost. Include an acceptance-rate floor and a coverage floor.

## From result table to decision record

A replay table is persuasive only when a reviewer can inspect the boundary
conditions. Attach the workload fixture, context snapshot, route and price
registry revisions, evaluator version, and exclusion rule. Record whether a
policy saw the same retrieval results and whether cache hits were replayed or
recomputed. A policy that gets a shorter prompt or warmer capacity is being
tested with an advantage that must be named.

State the promotion margin before reading the result. For example, require a
protected-stratum acceptance floor, no hard-gate violations, and a minimum
relative improvement in cost per accepted outcome against the content-free
baseline. The margin itself is a proposal that an owner must justify. If the
sample is too small to distinguish the policies, say so and expand the fixture
or run shadow traffic. Do not turn a noisy win into a release because the
router has already been built.

Inspect the shape of the Pareto frontier. A policy can have lower cost and
lower acceptance, lower latency and higher rework, or higher accepted volume
within the same budget. Choose the point that satisfies hard gates and makes
the business trade explicit. The frontier can change by stratum: a direct
capable route may be Pareto-efficient for high-consequence work while a fixed
efficient route is efficient for routine summaries.

Also measure router overhead as its own policy. The classifier call, feature
builder, registry lookup, trace writes, evaluator, and queue reservation have
cost and latency. Run a shadow policy that performs the deterministic envelope
and a fixed choice without semantic classification. If the router cannot beat
that simpler policy, its complexity has not earned a place. A route policy may
still be justified for a safety or resilience requirement, but then name that
requirement rather than presenting it as a cost saving.

Keep the rejected results. A discarded router experiment can reveal that the
traffic taxonomy is wrong, that a quality signal is uncalibrated, or that the
baseline is already strong. Preserve the failed fixture, decision, and reason
in the evidence ledger. Future work should be able to reproduce the rejection
and avoid re-running the same argument with a new model name.

## What a fair comparison records

The same request can cost different amounts under two policies because one
policy assembles a longer context, invokes a verifier, or waits in a different
queue. Those are legitimate route differences, but they need to be visible.
Record context tokens, cache state, evaluator and retry calls, queue time,
capacity reservation, and human disposition. Otherwise the comparison may
reward a policy for spending work outside the measured boundary.

State whether the baseline is allowed to abstain. A candidate that returns a
confident wrong answer and a baseline that asks for human help are not
comparable if the report counts only completed HTTP responses. Use the same
acceptance rubric and terminal vocabulary. If one policy supplies fewer
answers, show coverage next to cost per accepted result.

Finally, freeze the decision before inspection. Name the replay set, price
snapshot, traffic weights, and promotion rule in advance. This prevents a
team from discovering a convenient slice after seeing the result. A negative
result is an engineering output: it can show that fixed routing already
solves the problem or that the proposed router lacks an actionable signal.

## Checkpoint

The router has not earned complexity if the only evidence is a lower invoice or
a higher average score. A fair decision needs the same requests, same context,
same acceptance rubric, and named baseline. Put the candidate's overhead in
the table. Mark which outcomes are measured, estimated, or unknown. The
reader's artifact is a pre-registered comparison that can reject the router
without embarrassment. That is what makes the later shadow stage credible.

## Source slot

The core research slot is [RouteLLM](https://arxiv.org/html/2406.18665),
[FrugalGPT](https://arxiv.org/html/2305.05176), and the additional routing and
evaluation papers mapped in [sources.json](../sources.json). The independent
benchmark slot is [IBM Research](https://research.ibm.com/publications/large-language-model-routing-with-benchmark-datasets),
[SWE-bench](https://www.swebench.com/), and [Aider](https://aider.chat/docs/leaderboards/).
The numeric table is an illustrative teaching replay. Replace it with a frozen
enterprise fixture before making a decision.
