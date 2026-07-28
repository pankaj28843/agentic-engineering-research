# Briefing: Production LLM Systems Engineering

## Thesis

Production AI engineering is systems engineering around a probabilistic
component. The model proposes tokens; the surrounding system controls context,
authority, state, evidence, cost, and recovery.

The practical architecture is:

```text
authenticated request
  → context and retrieval
  → model proposal
  → typed validation and policy
  → bounded tools or response
  → evaluation and outcome
  → trace, cost, and learning loop
```

Every arrow is a contract and every shared state needs an identity. Fluent text
does not relax distributed-systems, data, or security requirements.

## How to read this briefing

This page is a map, not the prerequisite lesson. Read it once to see the whole
system, expect some terms to be previews, and revisit it after Part III when
the compressed relationships should feel obvious. The guide teaches:

- [KV state, prefill, and decode](guide/03a-minimum-model-vocabulary.md) before
  the serving chapters;
- [RAG, embeddings, and reranking](guide/13-rag-architecture.md) in Chapter 13;
- [judges, shadow tests, and canaries](guide/15-evaluation-systems.md) in
  Chapter 15;
- [TTFT and ITL](guide/05-prefill-vs-decode.md) in Chapter 5, then
  [goodput and Pareto trade-offs](guide/21-full-stack-tradeoffs.md) in
  Chapter 21.

## The decision map

### Shape the context before blaming the model

A model sees only the context assembled for the current call. Give it the
smallest sufficient, authoritative working set; preserve provenance; version
prompts, tools, policies, and retrieved data; and compact by explicit utility
rather than arbitrary age. Context engineering is an information-allocation
problem, not simply “use a larger window.”

Prompt caching reuses deterministic prefix computation. Semantic caching reuses
an answer judged similar. The latter needs an authorization, version,
freshness, and confidence policy because similarity is not permission or
equivalence.

### Read serving metrics causally

Prefill processes the input in parallel and largely drives time to first token;
decode produces tokens sequentially and drives inter-token experience. KV cache
avoids recomputing prior token state but consumes scarce memory. Paged
allocation and continuous batching reduce waste and schedule dynamic
sequences; they do not abolish queueing, fragmentation, or tenant risk.

Speculative decoding changes the generation algorithm, quantization changes
numeric representation, and distillation changes the model or reusable
knowledge artifact. Benchmark them separately on production-shaped length,
concurrency, quality, and latency distributions.

### Treat model output as an untrusted proposal

Structured decoding can make JSON syntactically valid. It cannot establish
that an account belongs to the user or that a refund is safe. Parse and schema
validate, then apply semantic invariants, authorization, side-effect controls,
and bounded repair. A tool call should flow through proposal, canonicalization,
policy, approval where necessary, scoped execution, result reconciliation, and
audit.

Agent loops need budgets for calls, tokens, elapsed time, spend, tool attempts,
and progress. Termination is a product state: complete, partial, escalated,
denied, budget exhausted, or failed safely. Routing is useful only when the
quality estimator works for the relevant slices; fallback must disclose
meaningful capability loss.

### Own RAG as a data product

RAG spans ingestion, parsing, chunks, embeddings, indexes, retrieval, reranking,
context construction, generation, citation, access control, and deletion.
Evaluate candidate recall before answer quality so a generation score cannot
hide missing evidence. Measure ranking and context construction separately.
Grounding does not automatically produce correct citation attribution.

Use retrieval for changing, private, attributable, permissioned, or deletable
knowledge. Use fine-tuning for measured stable behaviour. Use in-context
examples when adaptation belongs to one request or tenant. Use context or model
distillation when repeated capable behaviour is too expensive. Hybrid systems
are common because knowledge gaps and behaviour gaps are different.

### Evaluate the system, then observe the outcome

Start with deterministic contracts, a stratified versioned golden set, human
rubrics, and calibrated semantic judges. A consistent LLM judge can still be
invalid. Stress-test answer order, rubric order, verbosity, and slices, then use
shadow and canary evidence before broad rollout.

Trace the whole user action: authentication, retrieval, routing, model calls,
tools, retries, validation, and delivery. Separate service health from answer
quality. Store content only under an explicit redaction, access, and retention
policy.

Attribute cost to the trace and ultimately to an accepted business outcome.
Token price is not unit economics when a cheaper call creates retries,
escalation, or human rework.

### Keep authority and identity outside natural language

Prompt injection exists because trusted instructions and untrusted data share a
language channel. Treat webpages, documents, retrieved chunks, tool output,
model output, and memory as untrusted. Deterministic code owns authorization,
least-privilege credentials, egress policy, sandboxing, and transaction-bound
approval.

Tenant identity comes from authentication and must survive databases, vector
stores, response and semantic caches, KV cache policy, queues, tools, memory,
traces, evaluations, and deletion. A response can leak another tenant's state
through timing even when it contains none of their text.

### Benchmark accepted work, not an appliance

Define product SLOs and hard quality/safety gates, decompose end-to-end latency,
use real length and route distributions, and sweep concurrency. Report
TTFT, ITL, completion tails, throughput, accepted goodput, and cost with exact
formulas. Choose from the Pareto frontier; one “best” configuration rarely fits
both interactive and batch traffic.

Reliability testing must cover fluent HTTP-200 failures: wrong retrieval,
cross-session state, interleaved stream fragments, ambiguous side effects,
retry storms, poisoned memory, evaluator outage, and masked fallback. Every
postmortem should yield a generalized invariant plus regression, fuzz, or
sabotage test.

## Ten durable interview claims

1. The model is one probabilistic component inside a deterministic control
   plane.
2. Context is a versioned working set with provenance, authority, and a budget.
3. Prefill, decode, and queue time have different causes and optimizations.
4. Valid structure is not valid meaning or authorized action.
5. An agent without explicit budgets and stop states is an unbounded retry
   system.
6. RAG quality begins with retrieval recall and corpus lifecycle, not answer
   fluency.
7. An LLM judge must be calibrated for validity, not admired for consistency.
8. Observability follows the user action; unit economics prices the accepted
   outcome.
9. Natural language never grants authorization, and similarity never grants
   cross-tenant reuse.
10. A production AI failure can be completely fluent; semantic invariants and
    feedback loops make it detectable.

## Evidence posture

The series uses primary/official mechanisms first, empirical papers for bounded
results, vendor guidance as labelled implementation evidence, and community
threads only as practitioner signal. Exact benchmark numbers remain attached
to their workload, model, and method. Search-result text is never used as
substantive evidence.

The full learning path is in the [guide](guide/00-README.md).
