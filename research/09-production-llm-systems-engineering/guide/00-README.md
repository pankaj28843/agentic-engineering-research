# Production LLM Systems Engineering: From Tokens to Trust

This is a systems book for experienced full-stack engineers who can already
ship APIs, databases, queues, frontends, and observable services, but have not
yet built an LLM product end to end.

Each chapter starts with a compact mental model, makes the hidden mechanism
concrete, then turns it into design choices, failure drills, and interview
reasoning. “ELI5” here means *make the causal chain visible*—never pretend the
reader is inexperienced at engineering.

## What you will be able to do

By the end, you should be able to:

- draw an LLM product as a versioned, observable workflow rather than one model
  call;
- explain prefill, decode, KV memory, scheduling, quantization, and speculative
  decoding well enough to interpret a serving benchmark;
- design typed tool and structured-output recovery contracts;
- bound an agent with budgets, termination, routing, fallback, and explicit
  degraded states;
- build and separately evaluate retrieval, generation, and citations;
- connect traces and bills to accepted business outcomes;
- enforce prompt-injection and tenant boundaries outside the model;
- choose prompting, ICL, RAG, tuning, or distillation from the measured gap;
- run a product-shaped latency/quality/cost/reliability comparison;
- turn silent production incidents into durable invariants and regression
  tests.

## How to use the book

For an application-oriented first pass, use this dependency-safe spine:

`1–3 → 9–18 → vocabulary interlude + 4–6 → 19–22`

This gets an experienced application engineer to structured boundaries, tools,
RAG, evaluation, and safety before the deeper serving branch, while still
teaching the cache and scheduler mechanics needed for multi-tenant inference.
Insert Chapters 7–8 after Chapter 6 when self-hosting or inference optimization
is material, or before Chapter 21 when it changes the benchmark. Inference and
platform readers can read 1–22 linearly.

For active study:

1. read the ELI5 model without taking notes;
2. cover the mechanics and explain the causal chain aloud;
3. sketch the worked example from memory;
4. do the capstone increment or the field exercise/failure drill;
5. answer the interview checkpoint in two minutes;
6. record the first assumption you could not defend, then follow its named
   source.

The everyday analogies are memory hooks, not substitutes for the engineering
model. Whenever the analogy and mechanism differ, trust the mechanism.

### A reusable interview-answer frame

For a 90-second answer, use five moves:

1. **Frame:** clarify the workload, authority or consequence, and product SLO.
2. **Mechanism:** explain the causal chain, not merely a product name.
3. **Boundary:** name the deterministic invariant and where code enforces it.
4. **Evidence:** name one metric, evaluation slice, and failure injection.
5. **Trade-off:** state what worsens, what remains assumed, or what must be
   measured next.

In a five-minute follow-up, draw the data and control paths, identify state and
version boundaries, walk one normal and one failure trajectory, and give a
rollback or degraded outcome. A senior answer does not list every concept; it
makes one defensible design conditional on a stated workload.

Two calibrated examples:

- **“Design production RAG.”** A 90-second core answer first asks about corpus
  freshness, ACLs, answer acceptance, and latency. It then walks versioned
  ingestion through authorization-constrained candidate generation, reranking,
  context construction, generation, and citation verification. The invariant
  is that no unauthorized or tombstoned chunk enters ranking/top-*k* or a model
  prompt. Measure candidate recall, answer acceptance, citation correctness,
  freshness lag, and tails separately; inject an unauthorized query and a
  deletion. The trade-off is recall/latency/cost under a fixed evidence and
  authorization envelope. **Follow-up:** “Why not filter after top-*k*?” A
  strong answer explains both lost authorized recall and exposure in
  retrieval-side caches, scores, timing, logs, or telemetry. **Red flag:**
  “Put documents in a vector database, use a large `top_k`, and tell the model
  to cite them.”
- **“Defend an agent against prompt injection.”** A 90-second core answer asks
  what the agent may read, what it may change, and what data may leave. It
  treats external language and model output as untrusted data, separates the
  reader from the actor, and puts authentication, resource authorization,
  scoped credentials, schema/semantic validation, egress policy, and exact
  approval digests in trusted code. Test a poisoned document, malicious tool
  result, stale approval, and attempted exfiltration; trace the denied
  boundary and safe UX. The trade-off is capability and diagnostic detail
  versus authority and data exposure. **Follow-up:** “What if a classifier is
  99.9% accurate?” A strong answer says a probabilistic detector reduces
  exposure but cannot mint authority or replace fail-closed policy. **Red
  flag:** “Use a stronger system prompt and another LLM as a guard.”

## Part I — Shape the application around uncertainty

1. [Harness engineering](01-harness-engineering.md) — make the environment,
   evidence, and feedback loop part of the product.
2. [Context engineering](02-context-engineering.md) — assemble the model's
   finite working set deliberately.
3. [Prompt caching versus semantic caching](03-prompt-vs-semantic-caching.md) —
   distinguish compute reuse from answer reuse.
   Before the serving chapters, read the short
   [minimum model vocabulary interlude](03a-minimum-model-vocabulary.md).
4. [KV cache](04-kv-cache.md) — understand the token-state memory behind
   generation and prefix reuse.
5. [Prefill versus decode](05-prefill-vs-decode.md) — separate two different
   latency and resource phases.
6. [Continuous batching and paged attention](06-continuous-batching-and-paged-attention.md)
   — schedule dynamic requests and manage KV blocks.
7. [Speculative decoding, quantization, and distillation](07-speculative-decoding-quantization-distillation.md)
   — compare three optimizations that change different things.
8. [INT8, INT4, FP8, AWQ, and GPTQ](08-quantization-formats-and-methods.md) —
   reason about formats, calibration, kernels, memory, and workload quality.

Chapters 7–8 are the serving-optimization branch. They are required for the
inference/platform route and conditional for an application engineer whose
measured bottleneck or deployment choice makes them relevant.

## Part II — Turn model proposals into bounded workflows

9. [Structured outputs and recovery](09-structured-outputs-and-recovery.md) —
   parse, validate, repair, and terminate without mistaking syntax for truth.
10. [Function calling and tool contracts](10-function-calling-and-tool-contracts.md)
    — keep proposal, authorization, execution, and side effects separate.
11. [Agent budgets and termination](11-agent-budgets-and-termination.md) —
    make progress, cost, time, retries, and stop states explicit.
12. [Routing, fallback, and degraded UX](12-routing-fallback-and-degraded-ux.md)
    — optimize a system only inside a measured quality envelope.

## Part III — Ground and measure the product

13. [RAG architecture](13-rag-architecture.md) — own the source-to-answer
    lifecycle, not just a vector query.
14. [Retrieval evaluation](14-retrieval-evaluation.md) — measure candidate
    recall, ranking, context construction, and citations separately.
15. [Evaluation systems](15-evaluation-systems.md) — build calibrated release
    evidence for a probabilistic product.
16. [Observability](16-observability.md) — trace the user action through
    retrieval, models, tools, retries, and outcomes.
17. [Cost attribution](17-cost-attribution.md) — price accepted work, including
    tails, rework, and shared infrastructure.

## Part IV — Establish trust and isolation

18. [Safety](18-safety.md) — treat instructions as data and keep authority in
    deterministic policy and constrained tools.
19. [Multi-tenant isolation](19-multi-tenant-isolation.md) — carry verified
    identity through data, caches, inference state, memory, and telemetry.

## Part V — Choose and operate the whole system

20. [Prompting, ICL, RAG, fine-tuning, and distillation](20-adaptation-choices.md)
    — choose the least irreversible intervention that fits the measured gap.
21. [Full-stack latency, quality, cost, and reliability](21-full-stack-tradeoffs.md)
    — benchmark a product envelope and its Pareto frontier.
22. [Production failure modes](22-production-failure-modes.md) — catch fluent
    failures and turn incidents into reusable contracts.

## Focused reading routes

### Application and agent engineer

Read 1–3, 9–18, then the
[model-vocabulary interlude](03a-minimum-model-vocabulary.md) and Chapters 4–6
before 19–22. Insert 7–8 after Chapter 6 or before Chapter 21 only when
self-hosting, quantization, or another serving optimization is material. This
route includes Chapter 19 deliberately: tenant isolation depends on the cache
compatibility boundary in Chapter 4 and scheduler fairness in Chapter 6.

### Inference and platform engineer

Read 1–8, 11–12, 16–19, and 21–22. Chapter 15 supplies the quality gate that
keeps a throughput optimization honest. **Prerequisite vocabulary:** read the
four validity levels in Chapter 9 and the proposal-versus-effect boundary in
Chapter 10 before reviewing safety or failure recovery.

### RAG and evaluation engineer

Read 2–3, 9–10, 13–18, then the
[model-vocabulary interlude](03a-minimum-model-vocabulary.md) and the cache,
latency, and scheduling mechanics in Chapters 4–6 before 19–22. Chapter 19 is
not optional: authorization, invalidation, cache scope, and shared inference
capacity are retrieval architecture.

### Security and reliability engineer

Read 1–3, 9–12, 15–19, and 21–22. Use Chapters 4 and 6 before reviewing
multi-tenant inference caches. **Prerequisite vocabulary:** read the
[model-vocabulary interlude](03a-minimum-model-vocabulary.md), then Chapter 4's
cache compatibility boundary and Chapter 6's request lifecycle.

### Interview sprint

Read each ELI5 section, worked example, and interview checkpoint in order.
Then deep-read Chapters 2, 5, and 9–22. Chapters 16–17 are mandatory for
production/platform interviews: carry one end-to-end trace, one fail-safe
telemetry rule, and one cost-per-accepted-task denominator into the later
benchmark and incident answers. A strong 2026 answer connects model mechanics
to application and operating consequences; it does not recite tool names.

## First-seen vocabulary

This table is a safety rail, not a glossary to memorize.

| Term | Minimum meaning | First taught |
| --- | --- | --- |
| Token and context window | Model text unit; maximum token working set for one call | [Chapter 2](02-context-engineering.md) |
| Embedding | Numeric representation used for similarity, not proof of truth or permission | [Chapter 3](03-prompt-vs-semantic-caching.md) |
| Transformer and attention | Repeated representation layers; query/key matching combines value vectors | [Interlude](03a-minimum-model-vocabulary.md) |
| Weight versus activation | Mostly static learned state versus request-created dynamic state | [Interlude](03a-minimum-model-vocabulary.md) |
| KV state | Per-layer request state retained so earlier tokens need not be recomputed | [Interlude](03a-minimum-model-vocabulary.md) |
| Prefill and decode | Process supplied tokens; then generate one next token at a time | [Interlude](03a-minimum-model-vocabulary.md) |
| TTFT and ITL | Time to first token; delay between streamed tokens | [Chapter 5](05-prefill-vs-decode.md) |
| Tool proposal versus effect | Model proposes; trusted application code authorizes and executes | [Chapter 10](10-function-calling-and-tool-contracts.md) |
| Retrieval recall | How much required evidence the candidate stage found | [Chapter 13](13-rag-architecture.md) |
| Accepted goodput | Work completed inside latency and quality gates | [Chapter 21](21-full-stack-tradeoffs.md) |

## One capstone architecture

Build a tenant-aware document operations assistant:

- ingest versioned documents with provenance, ACLs, and tombstones;
- retrieve and cite evidence;
- call one read tool and one reversible write tool;
- stream structured progress;
- enforce a run budget and approval-bound commit;
- route or degrade explicitly;
- trace every model/retrieval/tool step;
- attribute cost per accepted task;
- test prompt injection, cache collisions, concurrency, and provider failure;
- shadow and canary a model or prompt upgrade.

Start from the [canonical capstone lab fixture](lab-fixture.md) and its
machine-readable `capstone-v2` bundle. It fixes the principals, documents,
tools, arrival trace, faults, evaluation records, gates, pricing, and golden
ledger so another engineer can recompute the result.

Choose one explicit completion level:

- **Study core:** deterministic simulation, local data, and a hosted model or
  model stub. Retain all fixed evaluation rows and authorization/safety hard
  gates; run one parameterized representative from each trajectory family and
  one fault from each failure family. Consolidate work into seven versioned
  evidence bundles: context/serving, workflow contracts, RAG/evaluation,
  trace/cost, safety/isolation, adaptation/benchmarking, and
  failure/postmortem.
- **Portfolio core:** keep every chapter delta individually traceable, execute
  every named deterministic variation, and run the integrated overload/fault
  campaign.
- **Live stretch:** repeat selected portfolio contracts with live hosted or
  self-hosted inference, a real queue/vector store/tool server,
  production-shaped load, and operational telemetry.

Simulation proves that you understand a contract; it does not prove live-system
capacity or safety.

For each chapter, add one invariant, metric, evaluation slice, or failure
injection to the same system. By Chapter 22 you have a portfolio design whose
trade-offs can be defended, not a collection of disconnected notebooks.
Completion demonstrates a source-backed, executable production design dossier.
It does not prove that a real deployment has passed its organization-specific
security, compliance, resilience, disaster-recovery, or operational-readiness
review.

Use this checklist as a traceability ladder. Study-core rows feed the seven
bundles; they are not 22 separately administered submissions:

| Chapter | Add to the same capstone |
| --- | --- |
| 1 | Harness/control-loop diagram and terminal evidence |
| 2 | Context inventory with provenance, trust, tenant, freshness, and budget |
| 3 | Cache eligibility, key, and invalidation policy |
| 4 | KV-capacity estimate and cache-isolation assumptions |
| 5 | Interactive and batch TTFT/ITL budgets |
| 6 | Admission, scheduling, cancellation, and numeric fairness test |
| 7 | Optimization hypothesis table: speculation versus quantization versus distillation |
| 8 | Conditional quantization decision/artifact card; independent quality result completed after Chapter 15 |
| 9 | Machine-readable JSON Schema, positive/negative instances, and typed recovery states |
| 10 | Trusted-registry read/write tool contracts and ambiguity reconciliation |
| 11 | Run state machine, cancellation phases, budget vector, and terminal evidence |
| 12 | Routing, fallback, and degraded-UX table |
| 13 | Ingestion and query planes with deletion propagation |
| 14 | Retrieval, evidence, and citation evaluation record |
| 15 | Release pyramid, golden set, and hard gates |
| 16 | End-to-end trace and fail-safe telemetry-policy contract |
| 17 | Terminal accounting matrix and accepted-task denominator |
| 18 | Authority/data-flow threat model and approval/tool-supply-chain attacks |
| 19 | Principal-aware isolation matrix and concurrent leakage tests |
| 20 | Adaptation ADR |
| 21 | Workload manifest and claim-bounded Pareto benchmark card |
| 22 | Integrated overload/fault campaign and postmortem-to-regression loop |

## Evidence and publication notes

The guide cites sources with author or organization and recognizable title so
the citation remains searchable in a non-clickable ebook. Search snippets were
used only to discover candidates. Claims come from headed-browser-extracted
source pages, native social/thread captures, or text-layer PDFs acquired through
the headed browser and converted with OCR disabled.

Exact source roles and limitations are indexed in
[the source catalog](../source-index.md); the browser and review trail is in
[the research log](../research-log.md).
