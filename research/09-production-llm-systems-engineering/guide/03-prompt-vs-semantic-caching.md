# 3. Prompt caching versus semantic caching

Prompt caching and semantic caching operate at different layers.

- **Prompt or prefix caching** reuses provider-side computation for an exact
  token prefix. The model still generates a new continuation.
- **Semantic response caching** reuses an earlier application result for a new
  request judged similar enough. The model call may be skipped.

One saves repeated inference work. The other changes product behavior by
substituting an old answer. Treating them as interchangeable is a reliability
and security bug.

## ELI5: reuse the prep work or reuse the meal

A restaurant receives two orders.

For prompt caching, the kitchen has already chopped the same base ingredients.
It reuses that preparation but cooks a fresh dish.

For semantic caching, the kitchen decides the second order is “close enough”
to the first and serves a previously prepared dish.

The second choice can save much more work, but “close enough” has product
meaning. “Peanut-free noodles” and “no peanuts on the side” may be close in
**embedding space**—a numeric similarity space—and completely different in
consequence. Nearness is not equivalence or permission.

Where the analogy breaks: prompt caching reuses computed prefix state, not
literal prepared food; semantic caching returns a stored application result.

## Four caches that engineers routinely confuse

| Cache | Key | Cached value | Generation still runs? | Main risk |
| --- | --- | --- | --- | --- |
| Exact response | Canonical request bytes/config | Final response | No | Staleness and key omissions |
| Semantic response | Similarity + filters | Final response or reasoning artifact | Usually no | False semantic hit |
| Prompt/prefix | Exact token prefix and model conditions | Reusable inference state/billing class | Yes | Prefix mismatch or unsafe sharing |
| KV cache | Token state inside a serving engine | Per-layer attention keys/values | Yes | GPU memory pressure and leakage |

This chapter covers the first three at the application boundary. Chapter 4
opens the KV-cache machinery.

## Exact response caching

An exact cache is appropriate when the operation is deterministic enough and
the key captures every behavior-changing input.

```text
key = hash(
  tenant
  + authorization scope
  + model/version
  + canonical messages
  + tool/schema version
  + retrieval snapshot
  + decoding parameters  # generation settings such as temperature/output cap
  + safety-policy version
)
```

That is intentionally longer than `hash(user_prompt)`. A response can change
because the model alias moved, a tool schema changed, a document was updated,
or the caller has different permissions.

Exact caches are safest for stable, public, low-consequence transformations.
They are poor defaults for “What is my account balance?” or answers derived
from rapidly changing knowledge.

## Prompt or prefix caching

Many requests share a long stable beginning: system instructions, tool
definitions, examples, or a document corpus. A serving provider can recognize
an exact token prefix and reuse its previously computed state. The request’s
new suffix is processed and a fresh answer is decoded.

Design for prefix reuse by placing stable material first and volatile material
later. Avoid changing whitespace, ordering, timestamps, generated IDs, or
tool schemas in the stable prefix unless necessary. Observe cached-input usage
rather than assuming that visually identical text tokenizes identically.

[AWS, “Optimize LLM response costs and latency with effective caching”](https://aws.amazon.com/blogs/database/optimize-llm-response-costs-and-latency-with-effective-caching/)
distinguishes exact and semantic application caches and discusses prompt-cache
economics. It is useful architecture guidance from a cloud vendor; its cost
examples depend on named services, prices, and workloads and should be
recomputed locally.

Prompt caching normally preserves the semantics of a fresh model call, but it
still needs isolation. A provider or self-hosted engine must not expose one
tenant’s prefix or timing information to another. Model version, adapter,
tokenizer, and relevant decoding state also belong to the compatibility
boundary.

## Semantic response caching

A semantic cache embeds or otherwise represents the new request, retrieves
candidate past requests, applies metadata filters, and returns a cached answer
if a policy accepts the match.

```text
query
  → normalize
  → embed
  → tenant/policy filter
  → nearest candidates
  → similarity + risk decision
  → cached answer OR fresh generation
```

The similarity threshold is not a tuning detail. It defines a classifier:

- a threshold that is too permissive creates **false hits**—fast, confident,
  wrong reuse;
- a threshold that is too strict creates **false misses**—safe but fewer
  savings.

[Portkey, “Semantic caching thresholds”](https://portkey.ai/blog/semantic-caching-thresholds)
is an operational explanation of this trade-off. It is also written by a
gateway vendor, so treat its threshold examples as starting hypotheses rather
than portable constants.

Recent preprint by
[Varun Chillara et al., “SemanticALLI: Caching Reasoning, Not Just Responses, in Agentic Systems” (arXiv:2601.16286)](https://arxiv.org/html/2601.16286v1)
explores reuse beyond final text. That broadens the design space but also the
verification burden: a reusable plan can contain assumptions, authority, and
intermediate state that no longer hold. Benchmark gains in a paper do not
establish safety for a payment, health, or tenant-specific workflow.

## Invalidation is a domain decision

Time-to-live is only one invalidation signal. A cache entry may become invalid
when:

- the underlying document or database row changes;
- the model, tokenizer, adapter, prompt, tool, or safety policy changes;
- an entitlement changes;
- the user corrects a preference;
- the answer contains a time-relative statement;
- a previous output is later marked unsafe or low quality.

Use dependency tags and versioned namespaces where possible. “Delete every
cache entry” is safe but destroys the value; “let TTL handle it” is simple but
can serve known-bad data until expiry.

For retrieval-grounded answers, store the source IDs and versions alongside
the response. Reuse only when those dependencies remain valid. If freshness
cannot be proved cheaply, miss the cache.

## A risk-tiered policy

Semantic reuse should depend on consequence, not only similarity.

| Class | Example | Reasonable default |
| --- | --- | --- |
| Public and timeless | Explain HTTP status 404 | Semantic cache with evaluation and TTL |
| Public but changing | Product documentation | Dependency-aware cache with short TTL |
| Personalized | Summarize my project status | Tenant/user partition plus strict inputs |
| Transactional | Approve refund or transfer | Do not reuse a prior decision |
| Safety critical | Medication or legal eligibility | Fresh authoritative retrieval and review |

The cache can also store a *candidate* that the model must validate against
fresh facts, rather than an answer returned directly.

## Worked example: developer documentation assistant

Assume ten thousand users ask variations of “How do I rotate an API key?”

A robust design can combine layers:

1. a prompt cache reuses stable system instructions and tool definitions;
2. retrieval resolves the documentation version and product edition;
3. a semantic cache searches only entries with the same product, version,
   locale, and public-access class;
4. an acceptance policy requires high similarity and valid source versions;
5. the response includes the current documentation citation;
6. a miss invokes the model and stores only answers that pass validation;
7. a security bulletin invalidates dependent entries immediately.

Never use a cached answer to reveal whether another tenant previously asked a
sensitive question. Cache metrics and debug endpoints need the same isolation
as the content.

## Evaluate the classifier, not just the hit rate

A seductive dashboard shows “70% cache hit rate” and “60% cost reduction.”
Neither says whether the hits were correct.

Build labelled pairs:

- paraphrases that should reuse;
- near-neighbours that must not reuse;
- negations and changed quantities;
- time-sensitive variants;
- different tenant/role/locale combinations;
- adversarial requests designed to cross a policy boundary.

Measure false-hit rate by consequence tier, false-miss rate, latency, saved
cost, stale-answer rate, and user correction. Use a shadow mode first: compute
the proposed cache decision but still generate a fresh answer, then compare.

[PyImageSearch, “Semantic Caching for LLMs: TTLs, Confidence, and Cache Safety”](https://pyimagesearch.com/2026/05/04/semantic-caching-for-llms-ttls-confidence-and-cache-safety/)
offers a current implementation-oriented discussion of these controls. It is
useful practitioner guidance, not a substitute for a domain-labelled test set.

## Failure drill

Suppose the cache serves “Your cancellation takes effect next month” after a
policy changed to immediate cancellation.

Trace the failure through:

1. key and metadata filters;
2. source dependency/version;
3. similarity decision;
4. TTL and event invalidation;
5. model/prompt version;
6. response provenance shown to the user;
7. purge and replay capability.

If the system cannot answer those questions, the cache is not production
ready.

## Interview checkpoint

**Question:** “Would you add semantic caching to reduce LLM cost?”

A strong answer asks about repeat rate, answer stability, tenant boundaries,
consequence of a false hit, invalidation events, source dependencies, and
labelled evaluation. It distinguishes semantic response reuse from exact
prefix computation reuse and proposes shadow evaluation before serving hits.

**Explain it back:** Why can prompt caching remain useful for a transactional
request even when semantic response caching is prohibited?

## Capstone increment

Specify the assistant's exact-response, semantic-response, prompt-prefix, and
KV-cache eligibility as four separate policies. For each, record key fields,
tenant/authorization scope, source dependencies, version compatibility,
invalidation events, observability, and a safe miss path. Reuse Chapter 2's
context provenance in every dependency-bearing entry.

Run the policy-change failure drill above once. **Definition of done:** the old
answer is rejected or purged for an observable reason without affecting an
unrelated tenant.

Next: read the
[minimum model vocabulary interlude](03a-minimum-model-vocabulary.md), then
[KV cache](04-kv-cache.md) explains the per-token state that makes prefix reuse
possible inside an inference engine—and why it becomes a memory and isolation
problem.
