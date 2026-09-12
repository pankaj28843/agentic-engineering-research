# 4. Hard Gates First: Route Envelopes and Capability Registries

## ELI5 hook

A train station has a timetable and a platform gate. The timetable can choose
the fastest train, but it cannot send a passenger to a track that does not
serve their destination, accept their ticket, or meet a dangerous cargo rule.
The platform gate checks those facts first. A clever timetable operating on an
invalid set of tracks is still unsafe.

The route envelope is the station gate. It defines what a request is allowed
to do and which route enums may be considered. A model-mediated classifier can
help rank the permitted trains; it cannot open a new platform, rewrite the
ticket, or waive a residency restriction.

## Mechanism: R0, R1, optional R2, and R3

Use a small control plane with distinct ownership:

```text
R0 ingress
  → R1 deterministic policy envelope
  → (R2 bounded classifier over allowed features)
  → R3 deterministic route scorer
  → worker → validator → approval/outcome ledger
```

`R0` authenticates and canonicalizes. It creates a run ID, request ID,
idempotency key, tenant binding, sensitivity label, consequence class, and
schema-validated request. It rejects missing identity or malformed input.

`R1` owns authorization, data class, residency, provider and region allowlist,
tool eligibility, retention, budget, queue and capacity reservation, and the
allowed route set. It must reserve worst-case classifier and worker budget
before either spends. A hosted classifier is itself a data-egress point, so
its features must pass the same tenant and residency checks as the worker.

`R2` is optional. It sees only the minimum redacted features needed to choose
among the existing set. Its output is a strict enum, a bounded reason code,
and a clipped confidence or rank. An invalid, unknown, or low-confidence
output falls back to a deterministic policy. `R2` has no credentials and no
authority to widen `R1`.

`R3` reads the eligible enum set and a versioned route registry. It scores
quality evidence, effective price, queue and capacity, deadline, and route
overhead. It reserves the selected route before dispatch and logs the
candidates, policy version, registry version, reason, and fallback set.

The registry must not be a bag of provider aliases. Each entry needs an
immutable model or weight identity, provider and account, region, supported
context and schema, tool contract, data handling class, quota, measured
latency and quality evidence, effective-dated price, and expiry. A `latest`
alias may be resolved at registry-ingest time, but route time must use the
resolved pin. Otherwise the same policy can produce a different model with no
auditable route change.

Current price pages are evidence that a provider publishes a price surface,
not permission to hard-code a number in the policy. Keep [Amazon Bedrock
pricing](https://aws.amazon.com/bedrock/pricing/), [OpenAI API pricing](https://openai.com/api/pricing/),
[Claude pricing](https://platform.claude.com/docs/en/about-claude/pricing),
[Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing), and
[DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing) as
dated lookup references. Their terms and product surfaces can change.

## Worked example: three envelopes

These are **illustrative design records**, not provider capability claims.

**Public, low-risk summary.** `R1` marks sensitivity public, consequence low,
and no tool needed. The eligible set contains a deterministic extract route,
an efficient readonly route, and a capable readonly route. `R2` may classify
context length or language. `R3` weighs the measured quality floor and queue.

**Sensitive, residency-restricted lookup.** `R1` binds the tenant to a region
and excludes routes whose contract cannot prove that boundary. A cheaper
cross-region route never enters the set. If the registry has no fresh
residency evidence, the result is blocked or a declared local degradation.
The classifier cannot suggest a provider outside the set.

**Account-state proposal.** `R1` requires proposal schema, named tool
eligibility, and approval. The eligible set contains only proposal-capable
routes that return a normalized action without executing it. `V1` validates
the structure and business invariants. `A1` checks the exact action digest,
actor, resource, policy version, and expiry before any side effect.

The route record for the second request might look like:

```text
tenant = t-17                 policy = regulated-eu-v4
sensitivity = restricted     residency = region-r
allowed_routes = {local-readonly-v3, managed-region-r-readonly-v7}
classifier = none             reason = missing-fresh-registry-proof
terminal = blocked            next = registry-owner review
```

The blocked state is more useful than a guessed route. It tells the registry
owner what evidence is missing and protects the user from a silent boundary
change.

## Failure drill: undeclared route and stale registry

The classifier emits `provider-cheapest` because its prompt was influenced by a
retrieved article. There is no such enum. The deterministic decoder rejects
the output, records the input and policy versions, and applies the predeclared
safe route or fails closed. It does not call a provider based on the string.

In a second incident, a registry entry still says an endpoint is available,
but its price or capability evidence has expired. `R3` must not make an
unbounded guess. It can use an explicitly approved stale-data grace policy
only for a route class whose risk allows it; otherwise it blocks, degrades, or
returns to the fixed baseline. An expired registry is a control-plane failure,
not a reason to let the model choose.

The [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
and the [European Commission AI regulatory framework](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)
are governance references for risk management and regulatory context. They do
not prescribe this exact graph or establish legal advice for a specific
enterprise; legal and security owners must map the policy to the applicable
jurisdiction and contract.

## Reader exercises

1. Write a route-envelope schema with tenant, sensitivity, residency,
   consequence, deadline, allowed enums, budget, and registry version. Mark
   which fields can come from user input and which must come from a trusted
   system.
2. List five features a classifier may use and five fields it may never own.
   Include identity, residency, authorization, tool authority, and budget in
   the second list.
3. Define the result for a missing tenant, an expired registry entry, an
   unknown route enum, and a saturated local candidate.
4. Describe how to resolve an upstream alias into an immutable route pin and
   how a replay would prove that the pin did not drift.

## Authority boundary in practice

It helps to draw two boxes around the route. The inner box is the **choice
box**: route enums, quality estimates, queue state, price snapshot, and
deadline. The outer box is the **authority box**: identity, tenant, data
residency, legal basis, tool permission, budget, approval, and retention. The
choice box can optimize only after the authority box has narrowed the world.

This distinction survives model upgrades. A new model may be better at
classifying a difficult summary, but it cannot inspect a secret it was not
permitted to see. A new provider may be cheaper, but it cannot enter a
restricted route set without a contract and registry evidence. A local model
may be faster, but it cannot execute a write because a classifier gave it a
high confidence score.

Make the boundary testable with negative cases. Feed `R2` a route name that is
not in the set. Change the tenant after the classifier returns. Expire the
residency evidence between policy evaluation and dispatch. Exhaust the parent
budget before the optional classifier. Saturate the local pool. In each case,
the expected result is a deterministic rejection, safe declared degradation,
or block. A natural-language explanation is useful for the operator; it is
not the enforcement mechanism.

The registry needs an owner and expiry policy. Platform may maintain model and
runtime metadata, but security or legal must approve data-boundary fields, and
FinOps must own price and allocation assumptions. A route should carry the
registry revision it used. When a price changes, do not rewrite history; close
the old effective interval, create a new revision, and rerun the decision
fixture. When a capability claim cannot be refreshed, the route becomes
unknown according to its risk class.

Prefer fail-closed for authority and fail-soft for user experience only where
the policy permits it. A missing optional style preference can use a default.
A missing tenant or residency class cannot use a guessed default. This is why
the route envelope is a product artifact as much as an engineering schema: it
defines which uncertainty is tolerable and which must stop the journey.

## Registry expiry and route ownership

Treat registry freshness like certificate expiry. Each field has an owner and
an evidence date. Price may be refreshed by FinOps or procurement; capability
and schema by platform; region and data handling by security or legal; quality
and latency by evaluation and SRE. A route becomes stale when the relevant
evidence expires, even if a different field is current.

The route scorer should receive a snapshot, not query several mutable systems
mid-decision. Log that snapshot. If a worker starts after the reservation but
the policy changes, the control plane chooses whether the old revision may
complete or must stop. For a side-effect proposal, the approval gate checks
the current policy and exact digest again. For a read-only response, a bounded
grace window may be acceptable if the data class allows it.

This ownership model keeps “the model” from becoming the default owner of
facts no one maintains. The model can be replaced; the contract and registry
still say what the route is allowed to do.

## Checkpoint

At this stage, the route enum should be smaller than the provider catalog. The
registry should be versioned, owned, and expiring. The policy should say what
happens when identity, residency, capacity, price, or capability evidence is
missing. If the answer is “ask the model,” the boundary has leaked. The
reader's artifact is a route envelope that a static checker can validate and
an operator can explain during an outage.

## Source slot

The architecture is a proposal grounded in the capsule's graph contract and
the governance references [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework)
and the [EU framework](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai).
The source catalog's official pricing pages provide dated lookup evidence for
registry design, while [vLLM engine arguments](https://docs.vllm.ai/en/latest/serving/engine_args.html)
and [SGLang documentation](https://docs.sglang.ai/) illustrate why a local
runtime needs explicit version and capacity metadata. The contract remains
design-only until the route registry, security, replay, and shadow gates pass.
