# 11. The Existing Portfolio: Copilot, Bedrock, and Local Services

## ELI5 hook

An airport already has a train, taxis, and a rental-car desk. Building one new
traffic controller does not mean every passenger now travels through the same
road. The train has its own operator and ticket controls, taxis have a curb,
and rental cars have a contract. First map where the controller can observe
and enforce rules. Then improve the lanes that are actually in its reach.

A large enterprise often has three visible AI paths: a coding-assistant
product used in an IDE, managed cloud API calls such as Bedrock, and in-house
open-weight endpoints. They have different control surfaces, cost contracts,
identities, and telemetry. A provider-neutral route graph should begin with a
scope matrix, not the assumption that a gateway intercepts them all.

## Mechanism: channel scope before route scope

For each channel, document:

```text
who chooses the model
where authentication and tenant identity enter
what request/usage/billing data is observable
which policy controls are available
whether a gateway can intercept the call
what data boundary and retention contract applies
what rollback action the owner can execute
```

**Copilot or IDE flow** may have client-side model selection, seat or credit
controls, and product-specific governance. A central gateway should not claim
per-request control unless the current product and admin evidence proves it.
The [GitHub Copilot changelog entry for Kimi K2.7](https://github.blog/changelog/2026-07-01-kimi-k2-7-is-now-available-in-github-copilot/)
is a dated primary product-availability record; it is not proof that an
enterprise can route or meter every completion through its own control plane.
The migration action may be a separate product-configuration and usage-
attribution workstream.

**Bedrock or another managed cloud API** may expose a server-side integration
point for a gateway, with provider, account, region, quota, and price terms.
The [Bedrock pricing page](https://aws.amazon.com/bedrock/pricing/) and official
Bedrock documentation in the [source index](../source-index.md) are current
lookup surfaces as audited on 2026-09-12. They must be refreshed before a
policy or budget is changed.

**Local open-weight service** gives the enterprise more control over region,
runtime, weights, and telemetry, while shifting capacity and operational
ownership inward. The route registry must bind the weight, runtime, hardware
pool, schema, tool contract, and measured acceptance evidence. A local endpoint
should fail closed for a restricted class if its residency or identity proof is
missing.

Use one route taxonomy across channels only where the contract is genuinely
shared. An `interactive-coding-completion` route may not be treated as the
same object as a `server-side-code-change-proposal` route. The latter can pass
through `R0` and `A1`; the former may be governed by product settings and
post-hoc usage signals.

Assign the ownership chain explicitly. The product owns user intent, local
authority, and the promise to the user. The gateway owns routing under the
right contract within its intercepted scope. The managed provider owns its
service implementation, regional availability, contract, and invoice. The
local platform owns weights, runtime, accelerators, scheduling, monitoring,
patches, capacity, incidents, and retirement. The domain owner decides whether
the result meets the business acceptance rubric and what consequence follows.
An answered health check or returned bytes cannot discharge all five roles.

Group the gateway's proposed contract into four checks:

| Check | Controls for traffic actually intercepted |
|---|---|
| Identity and policy | tenant propagation, data class, residency, route eligibility |
| Accounting and safety | budgets, attribution, idempotency |
| Request plumbing | request/response schemas, trace correlation, cache scope, provider adapters |
| Capacity and recovery | capacity admission, declared fallbacks, terminal states |

The route record should group identity (route ID, owner, model or weight pin,
runtime revision, account, region), contract (data classes, schemas, tools,
quota, capacity pool), evidence (latency, quality, cache owner, price snapshot,
fallback set, expiry), and recovery (the rollback action). Process health and
a loaded model are useful signals, but eligibility requires the identity,
boundary, runtime, schema, tool, capacity, and acceptance evidence to agree.
Mark missing evidence unknown or blocked for the affected request class;
successful admission still does not guarantee an accepted terminal outcome.

## Worked example: three migration lanes

These are **illustrative planning choices** for a generic enterprise.

| Workflow | Current path | First migration step | Route authority and rollback |
|---|---|---|---|
| IDE completion | Copilot client and subscription | build a scope/usage matrix; configure allowed product settings; do not proxy blindly | product owner controls settings; disable new model or cohort if acceptance or spend signal regresses |
| Server-side document assistant | Bedrock API | put a thin gateway in front of server calls; preserve region and tenant binding; shadow fixed baseline and cascade | platform `R1` owns route eligibility; switch to the fixed managed baseline |
| Restricted batch extraction | in-house open-weight service | instrument queue, capacity, quality, and accepted-cost ledger; test deterministic batch policy | platform and security owners can stop local pool; restricted traffic blocks if no qualified capacity |

The first migration does not need one router for all three. It needs common
vocabulary: workload strata, acceptance contract, route ID, policy version,
cost event, and final outcome. The scope matrix prevents a dashboard from
presenting Copilot product usage as gateway request volume.

After observation, run shadow decisions. For Bedrock traffic, candidate routing
can be computed beside the current baseline without changing the response. For
local batch traffic, replay the same documents under capacity limits. For
Copilot, compare supported product-level controls and accepted coding outcomes
where instrumentation permits. Do not invent per-request attribution from a
seat fee.

For an **illustrative staged migration**, first freeze workload strata,
acceptance labels, route IDs, trace fields, and current baselines while
observing the unchanged user-visible path. Next shadow the candidate policy
using redacted or approved data. Then qualify the alternative against the
same schemas, tools, capacity, and acceptance rubric. Canary a low-consequence,
reversible cohort with a kill switch and named rollback owner. Expand by data
class and workflow only after quality, safety, latency, cost, reconciliation,
and capacity gates hold. For the first server-side migration, keep the stable
managed path as **Always-Mid**, a direct baseline with one known rollback
switch. Copilot remains in its product-specific experiment and denominator.

## Failure drill: the universal gateway story

In this **illustrative** failure drill, a program manager announces that all
AI traffic now passes through the enterprise gateway. A developer's IDE calls
the hosted coding assistant directly, while a local service bypasses the
gateway during an incident. The
cost dashboard counts only server-side requests and claims a broad savings
rate. A later policy incident exposes that the observed population was not the
portfolio.

Repair the language and the control. Label each channel's observation boundary
and denominator. Assign an owner for Copilot product settings, Bedrock
integration, and local service admission. Keep a direct fixed baseline for
server-side traffic. Treat unobservable channels as a separate governance
workstream until the product exposes sufficient evidence. This is a scope
correction, not a reason to route outside a data boundary.

Also remove the gateway itself. It is another capacity and failure domain,
with its own availability and rollback plan. A read-only server route may
have a bounded direct baseline only when the required policy can be proved at
the edge. A protected request may have to block. Replicating the control plane
does not replace a declared safe degraded state, and a direct rollback path
must not become permission to bypass identity or residency checks. Native
product traffic retains its product-native recovery controls.

## Reader exercises

1. Create a three-channel scope matrix for your portfolio. Fill observation,
   policy, billing, data-boundary, and rollback columns.
2. Write one route enum for each channel and list the contract differences that
   prevent them from sharing a single route record.
3. Design a migration sequence from observation to shadow to canary. Name the
   owner and the fixed baseline at each step.
4. Choose a Copilot-style subscription metric and explain what it can and
   cannot prove about per-request routing or accepted coding outcomes.

## The migration evidence pack

For each channel, preserve five artifacts. The **scope statement** says which
requests the control plane can see and change. The **current baseline** says
what users receive today and how its cost or usage is measured. The **route
contract** names data class, capabilities, SLO, fallback, and accepted
outcome. The **evidence pack** contains replay, shadow, or product-specific
measurements. The **rollback note** names the owner and the exact action that
restores the prior behavior.

This pack prevents a common category error: applying a server-side routing
metric to a client-side subscription. A Copilot user may select among models
through product controls; a Bedrock API call may have a gateway boundary; a
local endpoint may expose full route telemetry but carry all capacity risk.
The common vocabulary makes them comparable without pretending their control
surfaces are identical.

For Copilot, a useful first deliverable can be a product-control map: allowed
models, organization settings, seat or credit usage, audit data, and coding
outcome sample. If per-request selection cannot be observed or constrained,
leave the channel outside the route-enum experiment. A product owner can still
run a separate adoption and configuration experiment with its own denominator.

For managed traffic, start with a thin gateway that preserves provider error
semantics and region binding. Route only calls that already pass through the
server boundary. Shadow the candidate policy, record the current provider
model pin, and compare accepted results. For local traffic, add capacity and
runtime evidence before expanding load. A route that works in an idle lab is
not yet a production candidate.

Make the first canary concrete without mistaking its design for a result.
An **illustrative pilot** chooses a read-only, low-consequence document
workflow with a stable acceptance rubric, keeps the current Bedrock path as
Always-Mid, shadows a gateway adapter, and qualifies one local route pinned
to its weight, runtime, region, capacity pool, and cache scope. Replay the same
request classes and measure accepted goodput, p95 and p99 latency, queue
delay, cost per accepted outcome, cache isolation, support minutes, and
rollback time. Preserve protected strata in every comparison.

Write stop conditions before moving traffic: a hard data-boundary or
authority violation; material acceptance regression in a protected stratum;
**two consecutive latency-budget breaches**; registry expiry; unexplained
cost growth; a capacity failure that removes the declared fallback; or
reconciliation uncertainty after a possible side effect. These are proposed
pilot conditions, not a claim that this deployment has passed them. Keep
high-consequence tool proposals out of this first canary: approval and
action-digest reconciliation require their own test, and read-only success
does not transfer authority to cause an irreversible effect.

Run across more than one demand window, including the relevant peak. Freeze
the baseline and price snapshot for the comparison and refresh volatile facts
separately. Inspect the local queue during deployment and failure, sample
human rework, exercise the fallback, and deliberately expire route evidence.
The evidence pack must join each request's policy revision, route revision,
model or weight, runtime image, cache decision, capacity snapshot, reservation
lease, transition reason, and terminal state. At population level retain
accepted outcomes, rejected results, blocked requests, indeterminate effects,
queue delay, fallback usage, and cost. A savings claim needs that joined
population, not merely successful responses.

The portfolio review should happen at a fixed cadence and after material
events. Check provider terms, product controls, model and runtime updates,
local utilization, acceptance drift, queue tails, and unobserved channels.
Retire a gateway route if it adds cost without improving a named decision.
Retain a more expensive route when it is the only eligible path for a
protected class, and record that as a policy constraint rather than an
optimization failure.

## Channel-specific control is still one portfolio

The portfolio can share an outcome vocabulary even when its controls differ.
For coding assistance, an accepted outcome may be a patch that passes tests
and review. For a document assistant, it may be a sourced answer. For a local
batch, it may be a reconciled set of fields. Put these contracts beside the
channel's usage and rollback evidence.

A common registry can still hold separate route classes. Give a client product
an entry that says what is observable and which product controls apply. Give a
Bedrock route the provider account, region, API, and gateway boundary. Give a
local route the weight, runtime, capacity pool, and incident owner. The shared
schema makes gaps visible; it does not force false uniformity.

Within that registry, four **illustrative planning categories** make the
managed/local choice inspectable without asserting a provider ranking:

| Candidate row | Evidence and constraint to record |
|---|---|
| Managed burst | public, low-consequence interactive scope; provider, region, price snapshot, quota, latency, cache terms, concentration |
| Managed restricted-region | mandatory region and contract; narrower eligible fallback set |
| Local efficient | weight pin, quantization, runtime, pool, utilization, queue, accepted quality |
| Local capable | potentially higher cost; reservation for a protected quality or consequence class |

Each row needs an owner, data classes, model or weight pin, runtime revision,
region, schema and tool support, capacity signal, interactive or batch SLO,
cache owner, fallback set, all five cost layers, evidence expiry, and rollback
target. Add the accepted-outcome definition and protected strata. Write
unknown in an unproved cell; a cheaper blank is missing evidence. A
high-consequence tool proposal still requires approval and action-digest
reconciliation regardless of which row supplies the model.

Cache ownership is another boundary that a common registry must expose. The
gateway may coordinate exact or prefix reuse while a provider or local
runtime maintains a different cache. Name the owner of each layer, which
identity, tenant, sensitivity, policy revision, corpus version, route revision,
and tool state participate in its key, who can invalidate it, its retention,
and what a route change does to existing entries. A hit is an execution
shortcut, not evidence that reuse remains authorized.

The [OpenAI prompt-caching documentation](https://platform.openai.com/docs/guides/prompt-caching),
[Anthropic prompt-caching documentation](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching),
and [Gemini context-caching documentation](https://ai.google.dev/gemini-api/docs/caching),
checked in the source audit on **2026-09-12**, describe provider-specific
mechanisms. The [AWS caching discussion](https://aws.amazon.com/blogs/database/optimize-llm-response-costs-and-latency-with-effective-caching/)
offers practitioner framing for cost and latency trade-offs. None establishes
the gateway's isolation, retention, invalidation, or authority contract. Begin
with narrow exact or explicitly qualified reuse and prove invalidation.
Semantic equivalence is itself an inference: similar wording can conceal
different tenant scope, sensitive context, policy, source freshness, or
side-effect state. An unexplained semantic hit leaves risk outside the
apparent saving. Charge storage, lookup, invalidation, refresh, validation,
and stale-reuse repair to the ledger described in
[Chapter 10](10-managed-vs-local-tco.md).

When ownership changes, update the migration map before the traffic. A team
that inherits a local service inherits its capacity and security obligations.
A gateway team that adds a provider inherits compatibility and retry behavior.
The exact rollback action belongs in the channel record.

## Checkpoint

The migration map is ready when each channel has a truthful observation and
rollback boundary. Shared vocabulary is useful; shared interception is an
empirical fact that must be proved. The reader's artifact is a portfolio map
that separates Copilot product controls, server-side managed traffic, and
local service operations. It can recommend a common policy vocabulary while
leaving channel-specific authority with the owner who actually controls it.

## Source slot

Use the dated [GitHub Copilot changelog](https://github.blog/changelog/2026-07-01-kimi-k2-7-is-now-available-in-github-copilot/)
for that product-availability fact, and [Bedrock pricing](https://aws.amazon.com/bedrock/pricing/)
for a current managed-service lookup. Pair them with [vLLM metrics](https://docs.vllm.ai/en/latest/serving/metrics.html),
[FinOps](https://www.finops.org/wg/optimizing-genai-usage/), and the
portfolio records in [sources.json](../sources.json). Scope, authority,
rollback, and migration choices are enterprise proposals.
