# 19. Multi-tenant isolation: every reused byte has an owner

Multi-tenancy means sharing infrastructure without sharing authority or data.
In an AI system, the familiar database and object-store boundaries extend into
retrieval indexes, response caches, KV caches, schedulers, streaming buffers,
agent memory, tools, logs, and evaluation datasets.

The invariant is simple to say:

> A request may read, influence, reuse, or reveal only state permitted by its
> verified security context.

The engineering work is proving that invariant across every layer and every
asynchronous path.

## ELI5: an apartment building, not one large house

Residents may share the lobby, lift, and heating plant. They do not share
mailboxes, keys, diaries, or utility bills.

Writing “Apartment 7” on the web form is not identity. The building derives it
from the authenticated resident, carries it on the package, checks it at the
mailroom, and records who opened the box.

An AI platform needs the same chain of custody for tenant identity.

## Derive tenant identity once; enforce it many times

Tenant context must originate from verified authentication, never a
client-supplied `X-Tenant-ID` accepted on trust. Create an internal security
context containing:

- principal and tenant;
- roles, scopes, and policy version;
- data residency and retention class;
- workload or service identity;
- request and trace identity;
- expiry and delegation chain.

Propagate it through synchronous calls, queues, scheduled jobs, callbacks, and
tool invocations. At each resource boundary, enforce the relevant part again.
Do not assume middleware coverage automatically reaches migrations, batch
workers, admin scripts, or replay jobs.

The
[OWASP Cheat Sheet Series, “Multi-Tenant Security Cheat
Sheet”](https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html)
recommends tenant scope from the authenticated session, database enforcement,
composite resource identifiers, tenant-aware caches, quotas, prefixes, keys,
deletion, and audit logs. It is design guidance rather than an incident-rate
study.

## Build an isolation matrix

For every stateful component, record its isolation key and enforcement point:

| Surface | Minimum compatibility or authorization scope |
|---|---|
| relational/document data | tenant + resource + policy |
| object storage | tenant prefix/bucket + object policy |
| vector retrieval | tenant/corpus + ACL + source version |
| response/semantic cache | tenant/trust scope + permissions + all output-affecting versions |
| prompt/prefix cache | tenant/trust scope + model/tokenizer/adapter/policy |
| KV cache | request/session/tenant sharing policy + exact model state |
| queue and scheduler | tenant quota + workload class + request identity |
| stream assembler | connection/request + sequence identity |
| agent conversation/memory | tenant + user/session + writer provenance + policy |
| tool credential | tenant + principal + server + operation + expiry |
| logs/traces/evals | tenant access + redaction + retention |

“Global” is a deliberate trust domain, not the absence of a key. Truly public,
immutable system prefixes can be shared only after proving that their content,
model state, and timing behaviour fit the threat model.

## Response and semantic caches can return the wrong truth

A response cache key must include more than normalized text:

- tenant or approved sharing domain;
- authenticated permission fingerprint;
- model, prompt, tool, policy, and safety versions;
- retrieval corpus and source versions;
- locale and output contract;
- privacy class and personalization state.

Store the same scope inside the entry and verify it on read. Permission
changes, deletion, policy changes, and poisoned-source removal need invalidation
paths.

A semantic cache adds a second hazard: approximate matching may reuse an answer
across questions that look similar but have different authorization or intent.
Similarity can choose candidates only inside an already authorized partition.
It must not decide access.

## KV cache sharing creates a timing channel

During prefill, an inference server creates key/value tensors for prompt
tokens. Reusing a matching prefix can reduce time to first token. If mutually
untrusted users share that cache, the latency difference can reveal whether a
prefix was previously present.

[Guanlong Wu and colleagues, “I Know What You Asked: Prompt Leakage via
KV-Cache Sharing in Multi-Tenant LLM
Serving”](https://www.ndss-symposium.org/ndss-paper/i-know-what-you-asked-prompt-leakage-via-kv-cache-sharing-in-multi-tenant-llm-serving/)
introduces PromptPeek and evaluates chosen requests against multi-tenant serving
setups. The authors report about 99% average success in their studied scenarios
and a 60-request example for one targeted recovery. These are results under the
paper's prior-knowledge, scheduler, workload, model, and deployment assumptions,
not a universal attack rate.

The important threat-model fact is that an attacker can use ordinary API calls
and observe service order or timing; host compromise is not required.

Safe defaults are:

- private per-request or per-tenant reuse;
- no cross-tenant observability of cache identifiers or detailed hit state;
- rate and anomaly controls for chosen-prefix probing;
- workload tests that search for statistically distinguishable hit/miss timing;
- cache compatibility keys that include exact model, tokenizer, adapter,
  quantization, and policy state.

Adding random jitter is not a proof. Repeated measurements may recover a
distributional difference, while heavy padding destroys the latency benefit.

## Selective sharing is a security/performance trade

[Kexin Chu and colleagues, “Selective KV-Cache Sharing to Mitigate Timing
Side-Channels in LLM
Inference”](https://arxiv.org/html/2508.08438v2)
describes SafeKV: blocks begin private, an asynchronous pipeline assesses
whether content is safe to share, and a memory manager promotes eligible
blocks while monitoring reuse diversity. The paper reports that full partition
baselines increase time to first token—up to roughly 38.9% for one evaluated
70B configuration—and reduce reuse in its workloads.

That does not establish a generally safe classifier or a universal isolation
tax. Detection can be wrong, workload overlap changes the benefit, and
provider scheduling changes the signal. Use the work to frame a design space:

- full isolation;
- within-tenant reuse;
- narrowly approved public-prefix reuse;
- selective promotion with an explicit residual risk;
- timing mitigation plus monitoring.

Security policy chooses which point is allowed. A benchmark then measures its
cost.

## Shared schedulers and buffers are state too

Application-layer tenant filters do not protect an inference engine from:

- stale KV blocks reused after an incompatible transition;
- one request's tokens entering another stream;
- request-ID collisions or assembler bugs;
- cancellation cleanup racing with block reuse;
- a noisy tenant exhausting queue slots or cache space;
- scheduler liveness failure from valid concurrent workloads;
- adapter or model state crossing a request boundary.

[Yunze Zhao and colleagues, “Continuous Discovery of Vulnerabilities in LLM
Serving Systems with Fuzzing”](https://arxiv.org/html/2605.11202v1)
uses timed multi-request greybox traces against vLLM and SGLang. Eight-hour
campaigns with one small Qwen model produced reported state-isolation,
performance, and crash findings, including ten developer confirmations and two
CVEs. The paper says 15 potential vulnerabilities while the visible category
counts sum to 13, so do not repeat the total without that qualification. Two
engines and one main model do not measure ecosystem-wide prevalence.

The transferable testing idea is concurrency-aware:

- generate overlapping valid request sequences;
- vary cancellation, streaming, cache pressure, adapters, and priorities;
- observe outputs, timings, log probabilities, and resource state;
- replay candidates repeatedly;
- compare against isolated baselines;
- run the suite on every serving-engine or driver upgrade.

Single malformed-input fuzzing misses bugs created only by interaction between
ordinary requests.

## Agent context needs provenance partitions

Isolation also fails above the serving engine. A platform may flatten messages
from several applications, tools, or agents into one context where provenance
does not constrain influence.

[Chao Wang, Somesh Jha, and Zhiqiang Lin, “Confused ChatGPT: Cross-App Context
Poisoning via First-Party APIs”](https://arxiv.org/html/2606.00485v1)
reverse-engineers a 2026 application runtime, inspects 806 widget bundles, and
demonstrates cross-app influence on author-controlled apps across six tested
models. No examined third-party bundle used the undocumented parameters, the
demonstration redirected a benign task rather than exfiltrating data, and the
platform can change quickly. It is evidence of a flat-context mechanism, not a
claim that every app was exploiting it.

Protect compositional systems with:

- immutable origin on every message and tool result;
- per-app or per-agent context partitions;
- explicit permitted flows between partitions;
- provenance-aware rendering and decision rules;
- no ability for one component to mint another's privileged role;
- user-visible approval for meaningful cross-app delegation.

Names in a prompt are not namespaces.

## Persistent memory is a database with an unusual writer

Long-term memory creates durable cross-request influence. Treat each memory
item as a record with:

- tenant, subject, session, and purpose;
- writer and source provenance;
- created, updated, and expiry times;
- sensitivity and confidence;
- content and schema version;
- integrity hash and audit trail;
- review, deletion, and rollback status.

Authorize both reads and writes. A user may be allowed to use a shared company
policy memory but not rewrite it. Keep snapshots and tombstones, propagate
deletion to embeddings and caches, and support tenant-scoped rollback after
poisoning.

The
[OWASP project, “Agent Memory
Guard”](https://owasp.org/www-project-agent-memory-guard/)
proposes integrity hashes, access policy, anomaly detection, snapshots, and
rollback. As captured in July 2026, it is a roadmap with a first release
planned later in 2026, not validated software or proof that no other solution
exists.

## Isolation includes availability and accounting

Confidentiality gets attention, but a tenant can also affect neighbours through:

- queue starvation;
- cache eviction;
- context or output amplification;
- tool fan-out;
- evaluator load;
- vector-index hotspots;
- provider quota exhaustion.

Use per-tenant quotas, weighted scheduling, concurrency limits, circuit
breakers, spend budgets, and fair capacity pools. Observe tail latency,
eviction, cancellations, and budget termination by tenant class without
exposing one tenant's details to another.

Allocation and isolation should align: if usage cannot be attributed to a
tenant or shared pool, neither abuse control nor unit economics is trustworthy.

## Test the invariant, not only the configuration

Create at least three synthetic principals: two in one tenant with disjoint
roles and object ACLs, plus one in another tenant. Give them deliberately
overlapping identifiers, prompts, documents, and timing. Test:

- horizontal ID guessing and forged headers;
- background jobs with missing tenant context;
- vector retrieval and citations under different ACLs;
- exact and approximate cache collisions;
- permission revocation after planning and while work is queued, plus deletion
  propagation;
- KV-prefix probes and cross-request output contamination;
- streaming cancellation and reconnect;
- adapter/model/version switches;
- memory poisoning and rollback;
- traces, exports, and evaluation datasets;
- noisy-neighbour limits.

Run tests concurrently and after failures. Isolation often breaks in cleanup,
retry, migration, and administrative paths rather than the happy request.
For every surface, preserve an evidence row naming the enforcement point,
concurrent negative test, cleanup/failure-path result, measurable pass
threshold, and residual risk.

## Worked example: similar HR questions, different permissions

Two employees ask, “What is the severance policy?” One is in Denmark and may
read a local policy; the other is a manager in another country.

A safe system:

1. derives tenant and role from authenticated sessions;
2. filters retrieval by region and role before vector search results reach the
   model;
3. keys semantic-cache candidates by authorization fingerprint, corpus
   version, locale, and prompt/model policy;
4. shares no private KV prefix across tenants;
5. resolves citations under the requesting principal;
6. stores memory and traces in the same tenant boundary;
7. invalidates chunks, cached answers, and embeddings when policy changes.

The sentences are semantically similar. The permitted truths are not.

## Field exercise: chase one tenant ID

Take a request and follow its tenant identity through:

- edge authentication;
- service-to-service calls;
- queue and retry;
- database and vector query;
- every cache;
- model server;
- tool credential;
- memory write;
- trace, log, and evaluation export;
- deletion and offboarding.

At each hop, name the enforcement point and a test that fails if context is
missing. “It is in middleware” is not an end-to-end proof.

## Interview checkpoint

**Question:** “How do you prevent cross-tenant leakage in an LLM platform?”

A strong answer derives identity from authentication, propagates and
re-enforces it at every state boundary, partitions retrieval, response and
semantic caches, KV reuse, memory, tools, telemetry, and budgets, and tests
concurrent failure paths. It identifies timing side channels and availability
isolation, not only wrong database rows, and explains the measured
security/performance trade of broader cache reuse.

**Explain it back:** Why can a response contain no other user's text and still
leak another user's prompt through a shared cache?

## Capstone increment

Turn the field exercise into the assistant's end-to-end isolation proof. Run
the [lab fixture's](lab-fixture.md) `core-isolation-overload` three-principal
scenario: two same-tenant principals with disjoint roles/ACLs and one
other-tenant principal, all using overlapping document names and semantically
similar prompts concurrently. Test retrieval and citation resolution, response
and semantic caches, KV reuse policy, memory, tools, stream assembly,
trace/eval export, queued/retried work, budgets, permission revocation, and
deletion/offboarding.

Portfolio core uses the fixed identities, ACLs, expanded arrival trace,
isolated South baseline, deterministic maximum completion times, and slowdown
gate so results are comparable. It does not call the eleven-request fixture a
p95 study. Live stretch repeats the proof against real shared stores, queues,
inference state, and telemetry under load, with at least the fixture's declared
minimum sample size and quantile rule.

**Definition of done:** both cross-tenant isolation and same-tenant
principal/role authorization pass as hard gates with zero unauthorized
objects, citations, cache hits, stream bytes, tool effects, or telemetry
records. Timing behavior is assessed rather than ignored, and one tenant's
burst cannot consume the other's reserved service envelope.

## Part IV checkpoint

- **Explain from memory:** natural language is data, authorization is code,
  and every reused byte needs a verified owner and compatibility scope.
- **Update the capstone:** attach the security context and enforcement/test
  point to every arrow in the architecture.
- **Keep unresolved:** which adaptation and deployment configuration best fits
  the now-measured, tenant-safe product? Part V compares those choices.

Next: [Adaptation choices](20-adaptation-choices.md) decides whether changing
context, retrieval, weights, or a smaller student is the right intervention.
