# Graph and enterprise architecture: smart LLM routing

## Verdict

This packet conditionally approves two bounded graphs and rejects an
unconstrained autonomous graph. The research workflow benefits from bounded
fan-out and fan-in because distinct source lanes and reviewers reduce blind
spots. The production request path may use a router and bounded workers only
after a fixed baseline loses on a named cost, quality, latency, or coverage
measure. This document is a design contract, not runtime evidence.

## Goal and success predicate

Increase useful AI adoption while holding or reducing cost per accepted outcome
without weakening privacy, authorization, reliability, or auditability. A
candidate succeeds only when a fixed stratified replay and shadow/canary
comparison shows lower normalized accepted-outcome cost or more accepted work
at the same budget, while quality and safety gates, latency SLOs, capacity,
and rollback criteria pass.

The graph must not automatically select an undeclared provider, authorize an
irreversible action, decide data residency, or change its own topology. A
provider percentage or reviewer consensus is evidence to investigate, not a
production proof.

## Baseline and measurable graph benefit

Compare, on the same workload, deterministic direct workflow; one validated
model; one bounded tool loop; fixed cascade; deterministic parallel workers;
one model plus independent verifier; and router/supervisor-worker. Add a
router only when the simpler baseline fails a measured requirement and the
extra edge supplies a named benefit such as parallelism, context isolation,
capability separation, or bounded escalation.

For research, the measurable benefit is parallel collection with a reducer that
preserves provenance, missing branches, and dissent. For production, the
benefit must be a replayed Pareto improvement. A diagram alone is not a graph
benefit.

## Topology and alternatives

Research uses bounded fan-out/fan-in: a coordinator assigns source lanes,
workers return typed evidence packets, and a reducer deduplicates by canonical
URL and claim ID. Sequential research is a slower alternative; arbitrary peer
handoff is rejected because it makes ownership and provenance unclear.

Production uses a deterministic policy gate, optional bounded classifier,
deterministic scorer, declared worker, validator, approval gate, and outcome
ledger. Direct deterministic workflow and fixed single-route policies remain
the alternatives. No dynamic topology, recursive spawning, or route-model
self-editing is activated without versioning, review, approval, and rollback.

## Node contracts

| Node | Responsibility | Contract and authority |
|---|---|---|
| `R0/v1` | deterministic ingress | authenticated request and trusted tenant metadata become a canonical envelope; creates run and idempotency IDs; no business side effect |
| `R1/v1` | deterministic policy gate | owns identity, tenant, sensitivity, residency, authorization, allowed route set, tool eligibility, retention, budget, and capacity reservation; fails closed on missing facts |
| `R2/v1` | optional model classifier | sees only redacted permitted features and returns a clipped reason plus fixed route enum; no credentials and no ability to widen `R1` |
| `R3/v1` | deterministic route scorer | orders the eligible enum set using versioned price, quality, latency, capacity, and overhead; reserves before dispatch |
| `W/v1` | remote or local worker | returns a typed answer or side-effect-free proposal with usage and latency; least privilege; no direct irreversible effect |
| `V1/v1` | validator | checks schema, semantics, evidence, and domain invariants; bounded no-side-effect repair only |
| `A1/v1` | approval gate | human or narrow pre-approved policy authorizes exact normalized action with actor, expiry, and digest |
| `O1/v1` | outcome and cost ledger | owns workflow state, idempotent result, accepted-cost accounting, redaction, retention, and reconciliation |
| `H1/v1` | human gate | approves, denies, or lets an exact high-consequence proposal expire; no silent substitution |

Every boundary has a published schema. Children cannot inherit broader
authority or reset parent budgets. Shared prose is not an API. Adapter records
must include immutable route/model/runtime revision, account, region, context
and schema support, tool contract, usage/error semantics, and evidence date.

## Edge, routing, and join contracts

```text
R0 → R1 → (R2) → R3 → W → V1 → (A1) → O1
```

`R0→R1` carries the canonical envelope. `R1→R2` is conditional and is
permitted only after the classifier's own tenant and residency egress check.
`R1/R2→R3` carries the allowed set and one registry snapshot. `R3→W` carries
one declared route and a reserved budget. `W→V1` carries typed output and
usage. `V1→A1/O1` sends accepted proposals to approval or read-only results to
the ledger. A fallback edge exists only in the predeclared eligible set.

Every choice logs input, policy, registry, and capacity versions, candidates,
enum, reason, and fallback. A research join preserves late, missing, rejected,
and dissenting branches; a quorum is not proof. Late writes after finalization
are ignored operationally but retained as evidence.

## State, identity, checkpoint, and resume

`R0` creates `run_id`, `parent_run_id`, `tenant_id`, `request_id`,
`graph_version`, `policy_version`, and idempotency key. `O1` owns execution
state; the business system owns business state. Every state field has schema,
writer, reader, provenance, sensitivity, retention, consistency, and size
limits.

Final states are `succeeded`, `partial`, `failed`, `blocked`, `cancelled`,
`awaiting-human`, `budget-exhausted`, and `indeterminate`. The last state is
used when an external effect may have committed but acknowledgement is
missing. A checkpoint records completed nodes, input versions, committed
effects, remaining budget, and approval expiry. Resume revalidates policy,
identity, registry freshness, and action digest. Checkpointing alone does not
provide exactly-once external effects.

## Failure, retry, timeout, cancellation, and compensation

Transport and rate-limit failures have one retry owner, bounded backoff, and a
parent retry budget. Malformed output receives at most one no-side-effect
repair before rejection or escalation. Invalid authorization and residency
failures are not retried. A timeout with a possible effect enters
`indeterminate`; the owning business system reconciles the idempotency key
before another attempt. Cancellation stops new work, propagates cancellation,
and prevents late writes. Compensation belongs to the business system that
owns the effect.

## Budgets and termination

Budgets cover wall time, queue time, critical-path latency, model and tool
calls, input/output/reasoning units where exposed, output size, retries,
concurrency, fan-out, external quota, and realized cost. `R1` reserves the
classifier and worst-case worker budget before either spends. Feedback loops
need a measurable progress predicate, max iterations, deadline, remaining
budget check, repeated-state detection, and circuit breaker. The model cannot
declare its own completion.

## Security, authority, and human gates

User input, retrieval, tool output, memory, child output, and provider
responses are untrusted data. Deterministic code enforces tenant scope,
residency, egress, secrets, authorization, retention, and tool eligibility.
Secrets do not enter prompts, traces, or review packets. Irreversible,
privileged, destructive, financial, and externally visible effects require
`H1` or a narrowly pre-approved exact action policy. `R2` cannot grant
authority or select a provider outside the enum.

Policy fields should separate data class, purpose, tenant, residency,
retention, provider class, consequence, and unknown behavior. Missing or
contradictory policy facts fail closed. Cache keys and evaluator traces inherit
the same identity and sensitivity rules.

## Observability and evidence

Emit redacted structured events for run, parent, graph, policy, node, edge,
attempt, checkpoint, route, registry, provider/model pin, input/output hash,
provenance, usage, cache status, queue and service latency, retries, approval,
budget, final status, and outcome. Join them to provider invoices, local
capacity, gateway work, evaluator work, human rework, quality slices, and
accepted cost. Apply retention, deletion, and legal-hold policy.

## Validation and evaluation matrix

| Gate | Required evidence | Falsifier |
|---|---|---|
| static contract | schemas, enum, reachable graph, privilege and budget checks | unknown route, duplicate writer, privilege edge |
| replay | stratified fixture, fixed baseline, accepted-cost ledger | cheaper route creates rework or loses protected slice |
| shadow | same traffic, redacted traces, no user effect | registry/price/latency drift or hard-gate miss |
| canary | named cohort, owner, exposure, kill switch | quality, latency, safety, or cost threshold breach |
| reliability | timeout, duplicate, cancellation, resume, partial fan-in | unknown effect or late write |
| security | injection, cache isolation, exfiltration, approval tamper | route expands authority or data boundary |
| operations | quota, alert, chargeback, capacity, incident runbook | budget exhaustion or evaluator outage is hidden |

## Owners and status

### Release record and evidence independence

The release record should pin the evaluator identity and configuration,
calibration evidence, held-out cohort, and independence from the candidate
policy alongside the model, registry and policy revisions. This is a proposed
control: a stable aggregate score does not establish that the judge or protected
strata stayed stable. Contract tests check enforceable boundaries; replay
compares policies under frozen conditions; shadow exposes current traffic and
capacity without production side effects; canary introduces explicitly bounded
real exposure. Passing one does not substitute for the others.

A cross-tenant cache result is a data-isolation incident, not merely an
acceptance miss to average against good answers. Stop the affected path, preserve
appropriately scoped evidence and follow the incident process. For a timeout
after a possible external effect, restore routing separately from reconciling
business state: rollback cannot undo an unknown commit. Both cases need a named
owner and terminal-state rule, but their severity and response are not the same.

Platform owns the registry and control plane; SRE owns capacity and latency;
product owns accepted outcomes; domain owners calibrate quality; security and
legal own data boundaries; procurement owns terms; FinOps owns allocation;
audit owns evidence; and business systems reconcile effects. This separation is
part of the proposed contract. It is an illustrative responsibility map, not
a universal assignment of legal or organizational decision rights; the adopting
organization must name the actual accountable owners.

Runtime status is **design-only**. No production proof, current provider
behavior, or enterprise ROI is claimed until the named gates have passed.
