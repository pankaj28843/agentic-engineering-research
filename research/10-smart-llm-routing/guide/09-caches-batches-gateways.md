# 9. Caches, Batches, and Gateways: Change the Route Before Changing the Model

## ELI5 hook

A library lends the same textbook to many students. The librarian can place a
copy on the reserve shelf when the course edition is unchanged. They cannot
hand yesterday's answer sheet to a student whose class, permissions, or exam
has changed. A delivery company can also group non-urgent parcels into a
cheaper truck, but it must not put a same-hour medical delivery in that truck.

Caching and batching are routing decisions. They can avoid or reshape model
work, but their eligibility and freshness rules are part of the route. A
gateway can provide a common control point for traffic it actually sees; it
cannot magically govern a client product or a provider subscription outside
its path.

## Mechanism: reuse, defer, and intercept

Separate three mechanisms:

- **exact prefix or context caching** reuses a deterministic, versioned part
  of computation or context construction. Its benefit depends on repeated
  prefixes and the provider or serving contract. Cache accounting must include
  storage, reads, writes, expiry, and misses.
- **semantic response caching** reuses a previous answer for a supposedly
  equivalent request. Similarity is not permission or truth. It needs tenant,
  identity, sensitivity, policy, corpus, freshness, route, tool-state, and
  confidence rules, plus a safe miss path.
- **batching** changes the service-level contract. Delay-tolerant requests
  can share a batch window and capacity plan; interactive requests should not
  silently inherit batch latency or retry semantics.

The cache key should bind at least:

```text
tenant and authorization scope
sensitivity and residency class
policy, prompt, tool, schema, and route-registry versions
corpus snapshot and freshness requirement
request shape, model/weight pin, and relevant tool state
```

Invalidate on a policy or authority change that affects the answer. Keep the
cache content-free in traces where possible and test cross-tenant leakage,
poisoned retrieval, stale policy, and partial writes. [OpenAI prompt caching](https://platform.openai.com/docs/guides/prompt-caching),
[Anthropic prompt caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching),
and [Gemini context caching](https://ai.google.dev/gemini-api/docs/caching) are
official sources for provider-specific behavior and terms as audited on
2026-09-12. They are lookup references, not interchangeable semantics.

For batch contracts, consult [OpenAI Batch API](https://platform.openai.com/docs/guides/batch),
[Anthropic Message Batches](https://docs.anthropic.com/en/docs/build-with-claude/batch-processing),
and [Gemini Batch API](https://ai.google.dev/gemini-api/docs/batch-api). The
route registry should record whether a candidate supports the required batch
shape, retention, completion window, cancellation, and result reconciliation.

A gateway adds policy, accounting, retries, registry lookup, and observability.
It also adds a hop, a failure domain, an ownership burden, and a compatibility
surface. The gateway can govern server-side API traffic that is routed through
it. It may have no per-request control over an IDE completion channel. Declare
the scope instead of claiming one universal router.

## Worked example: a repeated policy corpus

The following **illustrative calculation** covers 100 requests in a policy
assistant. Each request includes a large, unchanged approved handbook prefix.
An exact cache serves 60 requests after the first context preparation. Cache
reads and writes consume 0.1 unit per request; a model attempt consumes 1 unit;
validation consumes 0.2 unit. Assume the 60 hits still perform authorization,
freshness, and answer validation.

Without caching, context and model work cost 100 units and validation costs 20,
for 120 units before any rework. With caching, 40 misses consume 40 model
units, 100 cache operations consume 10 units, and validation remains 20: 70
units. The saving is meaningful only if all 60 hits were eligible and accepted;
if 10 hits are stale or cross a tenant boundary, the apparent 50-unit saving
is a safety incident and the cache policy has failed.

Now imagine 100 delay-tolerant extractions. A batch window reduces gateway and
provider overhead under its documented terms, but the work is not counted as
interactive success until results are reconciled. If 8 jobs expire and are
retried, their costs and completion-window misses remain in the route ledger.
The batch route can be economically better while being categorically invalid
for a request whose user is waiting.

The gateway's route record should say whether the result came from an exact
cache, semantic cache, batch, primary worker, fallback, or deterministic path.
Without that label, the team cannot compare routes or explain an answer that
was generated under an earlier registry version.

## Failure drill: the poisoned cache and the invisible client

An operator changes a policy for one tenant. The response cache key contains
only normalized prompt text, so another tenant receives the old answer. A
second team routes all traffic through a gateway and assumes Copilot IDE
completion is now observable. It is not; the client path is outside the
gateway. Both teams report healthy gateway metrics.

Fix the cache key and invalidate affected entries. Add a cross-tenant replay
with identical text but different identity, policy, and residency. For each
portfolio channel, write `intercepted`, `partially observable`, or `outside
scope` in the migration matrix. Never use an unobserved subscription or IDE
path as the denominator for gateway savings.

The [AWS caching discussion](https://aws.amazon.com/blogs/database/optimize-llm-response-costs-and-latency-with-effective-caching/)
is a practitioner source for cache cost and latency patterns; it is not proof
that semantic caching is safe for a regulated workload. [OpenTelemetry's GenAI
observability guidance](https://opentelemetry.io/blog/2026/genai-observability/)
helps define the trace fields, but content retention still belongs to the
enterprise's privacy and governance policy.

## Reader exercises

1. Write a cache key for one tenant-bound workflow. Include identity,
   sensitivity, policy version, registry pin, corpus freshness, route, and
   tool state. Define which changes invalidate it.
2. Split a workload into interactive, nearline, and batch classes. Give each a
   completion contract, queue budget, cancellation behavior, and cost ledger.
3. Draw the traffic boundary for Copilot, Bedrock, and a local API. Mark which
   calls a proposed gateway can see and which require product-level controls.
4. Design a cache-poisoning test with two tenants and one policy update. State
   the evidence that proves the old entry was not served.

## A route contract for reuse

For every reuse mechanism, write a small matrix with four questions: what is
reused, who may receive it, how fresh it must be, and what happens on a miss
or invalidation. This prevents a cache hit from becoming an unexamined
provider choice.

An exact prefix cache usually has a narrow equivalence claim: the approved
prefix and relevant construction inputs are identical under a known version.
The response after that prefix can still depend on tenant, current policy,
tool state, or user identity, so the later stage needs its own boundary. A
semantic cache has a much stronger equivalence claim. It should be limited to
low-consequence, read-only, permission-safe work unless a domain owner can
prove freshness and meaning. “The embeddings are close” cannot authorize a
cross-tenant answer.

Batching changes the failure state. A synchronous call that times out may be
retried under an idempotency key. A batch job may be accepted by the provider
but partially complete, expire, or return results after a policy version has
changed. Reconcile each item and decide whether old results can still be
accepted. If not, mark them stale and apply the current route policy.

Gateway ownership needs similar precision. The gateway owns the contracts it
can enforce: authentication handoff, route enums, registry, usage events,
budgets, and retries for server-side traffic. The product owner owns a client
surface the gateway cannot intercept. A gateway can provide common policy
metadata without pretending it is the authority for an opaque subscription.

Use route IDs that distinguish `exact-cache-hit`, `semantic-cache-hit`,
`batch-worker`, and `live-worker`. This makes a later quality or cost
regression diagnosable. A cache hit that bypasses a validator should be a
different route contract from a cache hit that still runs freshness and
authority checks.

## Freshness and invalidation are route choices

Every cache policy needs a freshness sentence a user can understand. “This
answer is from the approved handbook revision at time T” is different from
“this answer is similar to a previous answer.” The first can often be checked
with a versioned prefix. The second needs semantic equivalence, authorization,
and current corpus evidence. If those checks are too expensive, bypass the
semantic cache.

Invalidate by policy and data event, not only by elapsed time. A revoked user,
tenant change, deleted document, new jurisdictional rule, or tool-state change
can make a previously valid answer unusable. Keep an audit event for the
invalidation and a miss reason. A high miss rate may be a cost problem, but a
low miss rate can be a privacy problem if the key is too broad.

For batch, record item-level identity and policy version. A job can be accepted
while one item fails, and a policy can change while results wait. The result
ledger needs enough information to decide whether to deliver, re-run, or ask a
human. Batch economics are real only after that join.

## Checkpoint

Reuse is ready when equivalence, authority, freshness, invalidation, and miss
behavior are explicit. Batch is ready when its completion and partial-result
contract is explicit. A gateway is ready when its observation boundary is
honest. The reader's artifact is a cache, batch, and gateway policy matrix
with route IDs and tests for tenant, policy, corpus, and tool changes. Lower
miss cost never compensates for an unbounded data leak.

## Source slot

Use the official cache and batch pages for current documented behavior:
[OpenAI caching](https://platform.openai.com/docs/guides/prompt-caching),
[Anthropic caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching),
[Gemini caching](https://ai.google.dev/gemini-api/docs/caching), [OpenAI batch](https://platform.openai.com/docs/guides/batch),
[Anthropic batch](https://docs.anthropic.com/en/docs/build-with-claude/batch-processing),
and [Gemini batch](https://ai.google.dev/gemini-api/docs/batch-api). Pair them
with [AWS caching](https://aws.amazon.com/blogs/database/optimize-llm-response-costs-and-latency-with-effective-caching/)
and [OpenTelemetry](https://opentelemetry.io/blog/2026/genai-observability/).
Cache keys, scope claims, and calculations are proposals or illustrative.
