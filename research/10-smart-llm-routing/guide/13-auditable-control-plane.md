# 13. The Auditable Routing Control Plane

## ELI5 hook

An airport control tower does more than point at a runway. It knows which
aircraft is authorized, which runway is open, who has priority, what fuel
remains, which radio instruction was given, and what happened when weather
closed a route. A flight log lets another operator reconstruct the decision.
The tower does not let a passenger choose a runway by saying a convincing
sentence.

The routing control plane is the tower. Its most important product is a
reconstructable decision: the request's trusted identity and policy envelope,
the eligible route set, the registry and capacity snapshot, the route selected,
the attempts and validations, the approval, and the accepted outcome. A model
can provide a useful signal inside this system. It cannot become the system's
authority.

## Mechanism: typed nodes and edges

Use explicit node contracts:

```text
R0 → R1 → (R2) → R3 → W → V1 → (A1) → O1
```

- `R0` creates the canonical request envelope, authenticated identity, tenant,
  consequence, sensitivity, residency, run ID, and idempotency key.
- `R1` owns route eligibility, data boundary, authorization, tools, budget,
  retention, and capacity reservation. It fails closed for missing policy
  facts.
- `R2` is an optional model-mediated classifier. It receives minimum allowed
  features and returns a fixed route enum, reason code, and clipped confidence.
  It cannot widen the `R1` set.
- `R3` deterministically scores eligible candidates using a versioned registry,
  live capacity, effective price, quality evidence, deadline, and route
  overhead. It reserves before dispatch.
- `W` performs a declared model or local service call. It returns an answer or
  a side-effect-free proposal with usage and latency telemetry.
- `V1` checks schema, semantics, evidence, and domain invariants. A repair is
  bounded and cannot turn a rejected action into authorization.
- `A1` requires a human or narrowly pre-approved policy for irreversible,
  privileged, destructive, financial, or externally visible effects.
- `O1` writes an idempotent outcome and cost ledger. It owns workflow state,
  final status, redaction, retention, and reconciliation.

Every edge has a schema, writer, readers, provenance, sensitivity, timeout,
budget consumption, and failure transition. Natural-language transcript is not
an API. Child workers cannot inherit broader authority or reset the parent
budget. The capsule's [graph-engineering packet](../briefing.md) contains the
full design contract; this chapter teaches the parts needed for routing.

Capability never widens eligibility. In an illustrative case, even 99%
confidence that a tool call is safe is not a permission token. An uncertain
`R2` returns a bounded enum or abstains; `R1` still owns the allowed set.
A qualified alternative, a blocked state, or a human path may be correct.
Measure the latency of this separation, and require a human gate only where
the action's contract calls for one; do not add one to readonly work merely
to make the graph look safer.

State must be explicit. Use `succeeded`, `partial`, `failed`, `blocked`,
`cancelled`, `awaiting-human`, `budget-exhausted`, and `indeterminate` where a
possible external effect has not yet been reconciled. A checkpoint records
completed nodes, input and version IDs, committed effects, remaining budgets,
and approval expiry. Resume revalidates identity, policy, registry freshness,
and action digest. A checkpoint cannot make an external API exactly once by
itself.

Budgets cover wall time, queue time, critical-path latency, model/tool calls,
input and output units, retries, fan-out, concurrency, output size, external
quota, and realized cost. Reserve child budget before dispatch. Every feedback
edge needs a progress predicate, iteration limit, deadline, stagnation check,
and circuit breaker. “The model says it is done” is not a termination proof.

Observability joins structured events to the outcome: run, parent, graph,
policy, node, edge, attempt, checkpoint, route, registry, provider/model pin,
input and output hashes, provenance, usage, queue/service latency, cache state,
retry/fallback reason, budget, approval, final status, and accepted result.
Content is redacted under a retention policy. The outcome ledger joins those
events to cost per request, cost per accepted task, rework, quality slices,
safety events, tails, capacity, and provider quota.

Approval provenance identifies the approving principal or control, authority
or delegation basis, normalized-action hash, decision, scope, expiry or
decision time, and correlation to any committed or indeterminate effect.
A bare “approved” flag cannot establish who authorized what. Stable run and
attempt keys connect these fields to validator result, tool state, first
useful response, fallback reason, and cost allocation. These are proposed
schema fields; the invariant is reconstruction of decision, work, authority,
and result. The decision edge must read the same policy and registry identities
that the evidence reports. A current registry label beside yesterday's cached
worker configuration is not reproducibility.

## Worked example: one restricted proposal

The following is an **illustrative trace**. A user asks the system to propose
a change to a customer account. `R0` authenticates the user and creates
`run-884`, binds tenant `t-17`, and marks the request restricted and high
consequence. `R1` permits only a residency-qualified proposal route, reserves
one classifier slot (which is not needed) and one worker plus one bounded
repair, and requires approval.

`R3` selects the immutable local route pin `local-proposal-v3` because it is in
the allowed set and has current capacity. `W` returns a normalized proposal;
it does not call the account tool. `V1` finds the amount field valid but the
resource scope ambiguous. The state becomes `awaiting-human` with a preview
and exact digest. A human corrects the scope, reviews the digest and expiry,
and `A1` allows the owning business service to commit. `O1` records the
accepted outcome and every attempt.

If the worker timed out after the business service may have committed, the
trace would be `indeterminate`, not failed or accepted. The system would query
the owner using the idempotency key, reconcile the effect, then close the
ledger. A fallback model cannot run until that uncertainty is resolved. The
route's economic denominator also waits for reconciliation; otherwise a
duplicate effect can make a cheap route look falsely efficient.

The corrected scope needs its own normalized-action digest, with approval
bound to that exact proposal and expiry. If reconciliation is unavailable,
retain `indeterminate` with run key, attempt key, action digest, and owning
business system; alert the owner and stop further side effects for that
workflow. A human escalation or bounded status response can remain available.
If the effect did not occur, the owner can close the state or authorize a
bounded retry. If it did occur, record the accepted or rejected business
result. Missing acknowledgement is never permission for provider fallback.

## Failure drill: the graph is typed on paper only

In this **illustrative drill**, an engineer adds a fallback edge from `W` to
a provider in another region
without updating `R1`. The fallback is declared only in a prompt. During an
outage, the worker times out, a retry crosses the boundary, and the gateway
logs a successful HTTP response. No event contains the route registry pin or
the policy version, so the incident cannot be reconstructed.

Repair the graph at the contract boundary. The fallback set belongs to `R1`
and `R3`, is enumerated and residency-qualified, and has its own capacity and
cost reservation. The retry owner is singular. A timeout with possible effect
enters indeterminate reconciliation. The event schema requires route, policy,
registry, attempt, tenant, and outcome IDs. Add a static check for an edge
that can broaden privilege or leave the declared region. If the edge cannot
pass, the graph fails closed and reports a bounded degradation.

Security follows data across every edge. User input, retrieved text, tool
results, child output, memory, and provider responses are untrusted data.
Secrets never enter model context, traces, or review packets. Deterministic
code owns egress, tenant scope, retention, and approval. [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework)
and the [EU AI regulatory framework](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)
provide governance references for recording risk and control evidence.

## Reader exercises

1. Write the input, output, authority, side-effect, and budget contract for
   `R0`, `R1`, `R2`, `R3`, `W`, `V1`, `A1`, and `O1`.
2. Draw an edge that handles a timeout after a possible side effect. Include
   idempotency, reconciliation, indeterminate status, and the retry owner.
3. List every field needed to replay a route decision. Include policy,
   registry, capacity, price, prompt, tool, and acceptance versions.
4. Create an observability table with event name, redaction, retention,
   correlation IDs, owner, and alert for a budget or residency violation.

## State and recovery table

The graph becomes reviewable when each transition has a named owner and a
terminal meaning. A compact state table might be:

| State | Meaning | Next allowed action | Owner |
|---|---|---|---|
| succeeded | validated response or approved effect is recorded | close or deliver | outcome ledger and product |
| partial | some declared work is accepted and some is missing | deliver with contract or resume | product and workflow owner |
| failed | no accepted result and no uncertain external effect | bounded retry or incident | control plane/SRE |
| blocked | policy, identity, residency, or capacity prevents a safe path | supply evidence or remain blocked | policy owner |
| awaiting-human | exact proposal awaits named approval | approve, deny, or expire | human gate owner |
| budget-exhausted | parent ceiling prevents more work | return bounded result or incident | platform/FinOps |
| cancelled | caller or policy stopped work | reconcile late attempts | workflow owner |
| indeterminate | an effect may have committed but acknowledgement is missing | reconcile by idempotency key | owning business system |

Do not let a worker write all these states. `W` can report an attempt result;
`V1` can report validation; `A1` can record approval; `O1` owns the workflow
state transition. This prevents a model response from overwriting a business
fact. Store state history append-only with writer, timestamp, version,
provenance, and retention class. A current-state view can be materialized, but
the history is what makes an incident or replay possible.

Keep rejection and abstention visible as validation or policy decisions too;
neither is equivalent to an uncertain external commit. `unknown` describes
missing evidence, such as stale capacity or unavailable attribution, and must
not silently become a healthy route or accepted workflow outcome.

For cancellation, stop new work, propagate cancellation to eligible workers,
and ignore late writes after finalization while retaining their evidence. For
partial fan-out, declare whether all, any, or a named subset is required.
Missing branches remain visible. A quorum is a join rule, not proof that the
missing branch was irrelevant. For a human resume, revalidate approval expiry,
policy version, identity, and the exact normalized action rather than replaying
old natural language.

This contract also helps cost accounting. A failed attempt consumes resources.
A partial outcome may count only under a product rule. An indeterminate effect
cannot be counted as accepted until reconciliation. Without these states, the
route can improve its ratio by classifying uncertainty as success or by
dropping late branches.

## Audit reconstruction in ordinary language

An operator should be able to answer six questions from the trace without
reading a model transcript. What did the trusted system say about the user and
data? Which policy revision and registry snapshot constrained the choices?
Which routes were eligible and why was one selected? What work happened,
including retries, cache, queue, validation, and approval? What state did the
business system reach? What did the accepted outcome cost?

If a field is unavailable, the trace should say unknown and name the owner.
For example, an opaque subscription may provide aggregate usage but no
per-request model identity. That is an attribution limitation, not a reason to
invent a route ID. A local runtime may expose tokens and queue time but not
human review minutes. Keep the missing cost in the uncertainty range.

Keep audit records tamper-evident, append-only, access-controlled, and subject
to retention, deletion, and legal-hold policy. Do not store secrets or raw
regulated content just to make a dashboard convenient. Hash or reference
content under an approved redaction design. The audit trail must support an
incident and a replay while respecting the data boundary it is meant to prove.

Audit metadata and raw content may have different retention schedules. Where
applicable, an authorized legal hold can pause an approved deletion schedule;
access control and redaction still apply. Record deletion itself without
exposing deleted content. Policy, security, legal, and audit owners must agree
on this design before an incident makes copying content elsewhere tempting.
Required approval evidence must be retainable under the organization's
applicable retention and access rules.

Hashes and references do not make content harmless: a small input space can
be reversible, a reference can create an access path, and filenames or error
strings can disclose a tenant. Minimize first, test redaction, log sensitive
debugging access, and enforce expiry. If permitted evidence cannot support
required reconstruction, declare an observability gap. OpenTelemetry supplies
vocabulary, not permission to retain data; NIST and the EU framework provide
governance context, not route certification or a legal classification for the
proposed system. The source audit remains 2026-09-12.

## Checkpoint

The graph contract is ready when each node has one responsibility, each edge
has a schema and failure rule, each state has an owner, and each budget has a
termination condition. The reader's artifact is a typed graph packet that an
operator can replay without trusting a free-form transcript. Treat every
runtime claim as design-only until static, replay, shadow, canary, reliability,
security, and rollback evidence exists.

## Source slot

This chapter's node and edge contracts are a design proposal from the capsule
graph packet, summarized in [the theme briefing](../briefing.md). Governance
context comes from [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework)
and the [EU framework](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai).
Use [OpenTelemetry GenAI observability](https://opentelemetry.io/blog/2026/genai-observability/)
for telemetry vocabulary and [vLLM metrics](https://docs.vllm.ai/en/latest/serving/metrics.html)
for a local serving signal surface. Runtime status remains design-only until
the contract, replay, shadow, failure-injection, and rollback gates pass.
