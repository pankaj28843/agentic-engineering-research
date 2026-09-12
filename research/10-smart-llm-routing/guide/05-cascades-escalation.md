# 5. Cascades and Escalation: Pay for Certainty When It Is Worth It

## ELI5 hook

A museum's first security check is quick. Most visitors pass it. A small
number carry an unusual object or trigger an unclear scan, so a specialist
opens the bag. The museum does not send every visitor to the specialist, and
it does not keep scanning the same bag forever. The first check needs a signal
that says “I need help,” a maximum number of handoffs, and a record of what was
already spent.

A model cascade has the same shape. Try a cheaper or faster route, measure an
acceptance signal, and escalate only when the expected benefit is greater than
the extra cost and delay. The signal may be a deterministic field check,
evidence coverage, an independent verifier, or a calibrated uncertainty
estimate. A cascade is a policy with a stop rule, not a sequence of hopeful
retries.

## Mechanism: first attempt, signal, bounded escalation

For a route (r_1), define:

```text
attempt cost = model + context + gateway + validator work
escalation cost = probability of escalation × (route 2 + extra validation)
expected accepted cost = all path cost / probability of an accepted outcome
```

The exact accounting should use observed values from the route ledger. The
simple formula is a thinking tool. Estimate the first-route pass probability
by workload stratum, not one global number. Include the cost of the signal
itself: a verifier call, retrieval, human review, or deterministic test.

Keep three transitions separate:

- **quality escalation:** the first answer is incomplete, ambiguous, or below
  a measured quality threshold, so an eligible stronger route may try;
- **availability fallback:** the chosen service is unavailable, rate-limited,
  or times out, so a predeclared route handles the request if its policy and
  quality contract still hold;
- **safety refusal or block:** the request is unauthorized, crosses a data
  boundary, or lacks required evidence. Another provider cannot launder that
  failure into permission.

The cascade needs a shared budget for model calls, tokens, elapsed time,
spend, and human work. Reserve the worst-case path before the first attempt.
The budget must not reset when the request changes route. Give every attempt
the same idempotency key. If a side effect may have happened before a timeout,
mark the outcome indeterminate and reconcile before another attempt.

Thresholds should be calibrated against held-out examples. A confidence score
is not automatically a probability of passing the acceptance rubric. The
threshold can depend on language, context length, consequence, and the cost of
review. A long-tail stratum may need an earlier escalation or a direct capable
route. A high-consequence refusal may need a human, not a larger model.

[FrugalGPT](https://arxiv.org/html/2305.05176) is a primary research example
of combining adaptation, approximation, and cascades under an objective that
includes cost and quality. Its reported savings belong to the paper's tasks,
models, and method. [Tian Pan's practitioner account](https://tianpan.co/blog/2025/11/03/llm-routing-model-cascades)
is a useful implementation discussion, while [Sean Geng's guide](https://seangeng.com/writing/the-honest-guide-to-llm-routing)
is a skeptical reminder that a cascade needs a trustworthy quality signal.

## Worked example: a document extractor

Assume, illustratively, that a generic enterprise must extract six fields from
100 supplier documents. The efficient route costs 1 unit per attempt. The
capable route costs 5 units. A deterministic field validator costs 0.2 unit.
On a frozen sample, 80 documents pass the field and evidence checks on the
first attempt. Twenty escalate. Of those, 16 pass the capable route and four
remain blocked for human review. The numbers are teaching assumptions.

The efficient first pass costs 100 units. Validation costs 20 units. The
capable escalations cost 100 units. Suppose human review and final
reconciliation cost 12 units. Total route cost is 232 units. Ninety-six
documents are accepted, so cost per accepted document is 2.42 units. Sending
all 100 to the capable route plus the same validator would cost roughly 520
units and may still need review. Sending all to the efficient route would look
like 120 units but would fail the four blocked cases and any uncounted field
errors. The cascade is interesting because it preserves an acceptance signal
and spends capability on the uncertain tail.

Now change the traffic. In a new language, only 55 documents pass the first
route; 45 escalate. The same cascade costs 100 + 20 + 225 + 12 = 357 units.
If 38 are accepted, its accepted cost is 9.39 units. A direct capable route
may now be cheaper after rework. The policy should have a stratum-specific
threshold or a route rule that recognizes the language before creating a
longer queue.

The useful measurement is not the first-route pass percentage. It is the
whole path: accepted fields, evidence correctness, escalation, repair, human
review, latency, and cost. Preserve the four blocked records as outcomes; do
not remove them to improve the average.

## Failure drill: the threshold that creates a retry storm

An owner lowers the escalation threshold because the capable provider's
invoice rose. More answers are marked “confident,” but multilingual and
long-context cases now contain missing fields. Validators reject them. The
control plane repairs once, retries once, and escalates, so the supposed saving
becomes a fan-out of calls. Interactive latency breaches its SLO and the
capable queue saturates.

The repair is a policy change, not another prompt. Restore the hard acceptance
floor. Compare thresholds by stratum. Reserve capacity and worst-case budget
before accepting the new rule. Add a circuit breaker on escalation rate and
queue age. If the validator cannot distinguish a repairable output from an
unsafe one, stop and route to human review or a safe terminal state. The
fallback set must remain within the data and authority envelope.

## Reader exercises

1. Fill a three-route worksheet with first-attempt cost, pass probability,
   validator cost, escalation cost, and accepted-outcome probability. Compare
   a direct capable route with a cascade.
2. Choose one escalation signal. State what it measures, how it can be wrong,
   and which independent check calibrates it.
3. Write a condition that must stop escalation rather than try another
   provider. Include authorization failure, residency uncertainty, and an
   indeterminate side effect in your answer.
4. Design a shared budget for a first route, one escalation, one repair, and a
   human gate. Show where the budget is reserved and how a retry consumes it.

## When a cascade is the wrong shape

The cascade is attractive because it appears to buy capability only on demand.
It is a poor shape when the acceptance signal arrives too late, when the first
attempt changes the world, or when the uncertain tail is most of the workload.
It is also poor when a user experiences every handoff as a delay and cannot
benefit from a background escalation.

Ask four questions before adding a second route. Can the first route produce a
reliable no-side-effect signal? Is the signal available before a deadline or
irreversible effect? Is the second route independently eligible for the same
tenant, data class, and tool contract? Is the expected improvement larger than
the validator, queue, and human cost? If any answer is no, choose a direct
qualified route, a deterministic workflow, or a transparent block.

An escalation signal should be observable in the outcome. A deterministic
field validator can say which field is missing. An evidence check can say that
the answer cites an obsolete document. An independent reviewer can label an
ambiguity. A raw model confidence score is useful only after calibration. Log
the signal version and threshold so that a later policy change can explain why
the same request took a different path.

Do not conflate cascades with retries. A retry repeats a route after a
transient failure; an escalation changes the route because the acceptance
signal says the first route is insufficient. Both consume the same parent
budget. A failed transport response should not be treated as a semantic
failure, and a semantic failure should not be retried indefinitely as if the
network were broken.

For user experience, expose a meaningful state. “Working on a more detailed
answer” can be honest when the product supports asynchronous completion. For
an interactive request, return a bounded partial answer only if its contract
allows it. For a high-consequence proposal, show `awaiting-human` or
`blocked`, not a plausible-looking incomplete action. The route policy should
optimize the accepted journey, not just the number of final tokens.

## The economics of the threshold

An escalation threshold is a budget allocation. A low threshold spends more
on the capable route and may protect quality; a high threshold spends more on
repair, abstention, or user delay. Tune it against the cost of each error.
For a low-consequence summary, one extra capable call may be wasteful. For a
policy answer, a missed exception may cost much more than the call. The
threshold therefore belongs to a stratum and an acceptance contract.

Use a confusion table rather than a single curve. False-cheap means the first
route looked acceptable but required rework or caused a failure. False-
expensive means the policy escalated a result that would have passed. Add
abstention and indeterminate states. A threshold that improves one error while
creating a queue storm has not improved the whole route.

Escalation can also be parallel for a small, bounded verifier, but parallel
work changes cost and capacity. Choose sequential or parallel from the
measured acceptance and deadline requirement. Keep one retry owner, one parent
budget, and one final ledger writer. More attempts do not create more truth.

## Checkpoint

A cascade is ready for measurement when it has a first route, a signal, a
second eligible route, a shared budget, and a stop state. It is not ready when
the only rule is “try again if the answer feels weak.” Write the expected
cost by stratum and include the signal's own work. The reader's cascade
calculator should make it possible to see the traffic mix at which a direct
capable route becomes cheaper or safer.

## Source slot

The research slot is [FrugalGPT](https://arxiv.org/html/2305.05176) plus the
routing and cascade papers listed for Chapters 02, 03, and 05 in
[sources.json](../sources.json). The practitioner slots are [Tian Pan](https://tianpan.co/blog/2025/11/03/llm-routing-model-cascades)
and [Sean Geng](https://seangeng.com/writing/the-honest-guide-to-llm-routing).
Thresholds, budgets, and numbers in this chapter are proposed or illustrative;
validate them on a held-out, stratified enterprise workload.
