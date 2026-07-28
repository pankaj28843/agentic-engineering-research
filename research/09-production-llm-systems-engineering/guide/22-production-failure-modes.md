# 22. Production failure modes: when fluent output lies

Traditional failures often announce themselves with an exception or HTTP 500.
AI systems can return HTTP 200, valid JSON, plausible prose, and the wrong
tenant's state, an invented tool result, a stale policy, or a silently
incomplete task.

Reliability therefore includes semantic continuity: did the system do the
right task with the right state and evidence, not merely finish a request?

## ELI5: a delivery app says “delivered”

The server is healthy, the status is green, and the customer receives a photo.
Unfortunately, the driver swapped two addresses.

Transport succeeded. Meaning failed.

AI reliability needs checks on the parcel, address, recipient, and outcome—not
only the delivery API.

## Loud, silent, and latent failures

Classify manifestation:

- **loud:** exception, timeout, invalid schema, explicit refusal;
- **silent:** plausible output violates the intended task or state;
- **latent:** corrupted memory, cache, or corpus influences a later request;
- **amplified:** retries, agents, or tools turn a local fault into system load
  or side effects;
- **masked:** fallback produces an answer while hiding loss of capability.

The same root cause may move between classes under different error handling.
Swallowing a tool exception can turn a loud failure into a fluent fabricated
narrative.

## Map failures by layer and seam

### Input and policy

- malformed or adversarial input;
- missing authenticated context;
- instruction/policy version mismatch;
- locale, encoding, or truncation error;
- refusal or approval rule applied to the wrong action.

### Context, retrieval, and memory

- stale, missing, duplicated, or unauthorized chunk;
- wrong source version or failed tombstone;
- prompt assembly drops a critical instruction;
- context window truncates the wrong end;
- poisoned long-term memory;
- cache collision or stale personalized answer.

### Model and output

- hallucination, omission, or false confidence;
- structured but semantically invalid arguments;
- premature stop, repetitive loop, or length explosion;
- model alias changes behaviour;
- quantized/routed model regresses a tail slice.

### Tools and orchestration

- wrong tool or arguments;
- side effect succeeds but acknowledgment is lost;
- retry duplicates a non-idempotent action;
- tool schema or server changes after approval;
- planner assumes a failed result exists;
- budget expires after partial mutation;
- nested agents lose provenance or termination.

### Serving and concurrency

- queue starvation or retry storm;
- stream fragments assembled into the wrong call;
- request/session state contamination;
- leaked semaphore or resource counter;
- synchronous work blocks an asynchronous event loop;
- cancellation fails to release KV or tool resources.

### Environment and dependencies

- local/staging/production differences;
- missing package, binary, certificate, or permission;
- provider quota, region, or API drift;
- clock, file path, browser session, or network assumption;
- observability path fails with the component it observes.

The seams matter because model and software faults compose.

## Evidence from small but concrete taxonomies

[Vishal Pandey and Gopal Singh, “FailureAtlas: A Taxonomy of Failure Modes in
Multi-Provider LLM Serving
Infrastructure”](https://arxiv.org/html/2607.17525v1)
classifies transport, streaming, state/session, model, and governance/cost
origins along loud/silent manifestation. Its five verified entries include
concurrent state loss or contamination that still returns HTTP 200, an
SSE tool-call index collision, a leaked semaphore counter, sync I/O blocking an
event loop, and a fixed-interval retry storm. Two entries are first-hand stress
tests and three come from public bug reports; five cases cannot estimate
prevalence or exhaust the field.

[Wei Wu, “When Errors Become Narratives: A Longitudinal Taxonomy of Silent
Failures in a Production LLM Agent
Runtime”](https://arxiv.org/html/2606.14589v1)
studies one personal-assistant runtime over eight weeks: roughly 40 scheduled
jobs, eight providers, 4,286 tests, 827 checks, and 22 postmortemed incidents.
About 70% were first found from the human user view, four involved fabricated
narratives from polluted context, and silent periods ranged from 13 hours to
60 days. This is a single operator/system, collaboratively classified with AI,
and includes only completed silent-failure postmortems; its frequencies are
not population rates.

These sources establish mechanisms and useful questions. They do not justify
“70% of all AI incidents are user-discovered.”

## The reliability stack needs semantic contracts

Add invariants at boundaries:

- every request, stream fragment, tool call, and memory write has one trace,
  tenant, session, and sequence identity;
- retrieved evidence is authorized, versioned, and resolvable;
- a tool result cannot exist unless execution produced a recorded outcome;
- a side effect has an idempotency key and reconciliation path;
- retries have bounded attempts, jitter, and a common run budget;
- cancellation and exceptions release resources in `finally`-equivalent paths;
- fallbacks declare capability loss;
- final output satisfies deterministic and sampled semantic checks;
- an evaluator failure cannot silently become a passing score.

Assertions should fail close to the violated boundary. A final “looks plausible”
judge is too late to locate state corruption.

## Streaming is a state machine

Server-sent events or incremental tool calls may arrive as fragments. Assemble
them with:

- request and choice identity;
- tool-call index and stable call ID;
- explicit start/update/finish transitions;
- duplicate, missing, and out-of-order handling;
- size and time bounds;
- terminal validation before execution.

Test interleaved streams from many sessions, cancellation mid-argument,
reconnect, provider-specific empty deltas, and two simultaneous tool calls.
Valid final JSON from the wrong fragments is a silent failure.

## Retry only when the operation and failure permit it

Fixed immediate retries synchronize clients and amplify outages.

For each operation define:

- retryable errors;
- maximum attempts and elapsed budget;
- exponential backoff with jitter;
- concurrency and global retry budget;
- idempotency or deduplication key;
- whether the previous attempt may have committed;
- circuit-breaker and recovery condition;
- user-visible degraded outcome.

An agent loop is a retry system with semantic state. A second model call should
not repeat a payment merely because the first acknowledgment was malformed.

## Test environment grounding

[Mehil B. Shah, Mohammad Mehdi Morovati, Mohammad Masudur Rahman, and Foutse
Khomh, “Characterizing Faults in Agentic AI: A Taxonomy of Types, Symptoms,
and Root Causes”](https://arxiv.org/html/2603.06847v1)
mines 13,602 closed issues and merged pull requests from 40 open-source agent
repositories and manually codes a stratified sample of 385. It reports five
fault dimensions, 13 symptom classes, 12 root-cause categories, and substantial
dependency/integration and data/type handling within the coded sample. A survey
of 145 developers reports broad recognition of the taxonomy.

The automated prefilter, subjective coding, Python/popular-repository sample,
and correlational associations limit generalization. The rendered 2009 date is
an extraction error; use the arXiv 2603 version. The work supports a practical
lesson: record and test external assumptions.

For every tool or runtime dependency, capture:

- binary/package/model/schema version;
- filesystem and permission assumption;
- environment variables by name, never secret value;
- region, endpoint, and network policy;
- clock/timezone and locale;
- synchronous/asynchronous behaviour;
- startup, health, and cleanup contract.

“Works in the agent's shell” is not proof of the production environment.

## Offline evaluation is one stage, not reality

A static test set misses:

- temporal and policy drift;
- new users and long-tail inputs;
- load, queue, and concurrency interactions;
- live provider and tool changes;
- user adaptation;
- integration and permission state.

[GrowthBook, “Why Your AI Model Performs Great Offline But Fails
Production”](https://www.growthbook.io/insights/why-your-ai-model-performs-great-offline-but-fails-production)
proposes golden queries, staging, canary exposure, production outcomes, and
feeding novel failures back into the set. It is vendor/practitioner guidance
with no original controlled sample. The sequence is useful when combined with
explicit rollback and causal comparison.

Use this loop:

1. deterministic contracts and a stable regression core in CI;
2. broader trajectory, adversarial, and load tests before release;
3. shadow on recent production-shaped traffic;
4. canary only for eligible low-blast-radius cohorts;
5. observe semantic and business outcomes;
6. roll back or expand by predeclared gates;
7. add novel failures and their generalized invariant to the suite.

## Sabotage the observer

Do not assume telemetry detects the incident. Deliberately inject:

- a stale retrieval index;
- missing tenant context in a background job;
- a tool timeout after committing;
- malformed and interleaved stream fragments;
- a provider 429 burst;
- a poisoned memory record;
- an evaluator outage;
- a disk, queue, or cache capacity limit;
- dropped traces or redaction failure.

Verify the signal originates independently enough to survive the component
failure. Exercise on-call access, trace reconstruction, rollback, credential
revocation, memory/index restore, and user notification.

Chaos without an expected invariant is theatre. Write the detection and safe
outcome before injecting the fault.

## Postmortem for reusable learning

A useful AI-system postmortem records:

- user-visible semantic impact and affected scope;
- first bad event, detection time, and silent period;
- versions of model, prompt, corpus, tools, router, and code;
- causal timeline, including retries and fallbacks;
- why existing tests and telemetry missed it;
- data, side effects, and tenant exposure;
- recovery, reconciliation, and notification;
- point fix;
- generalized contract or invariant;
- regression, fuzz, or sabotage test;
- owner and verification date.

Do not stop at “the model hallucinated.” Identify the missing evidence,
unchecked transition, swallowed error, or authority path that allowed the
hallucination to become a product outcome.

## Choose durable foundations under framework churn

The Hacker News thread
[“Agent design is still hard”](https://news.ycombinator.com/item?id=46013935)
contains competing views: concrete agent patterns may have a short half-life,
while building them teaches lasting engineering skills; deeper investment may
make more sense when agent behaviour is the product's core value. It is an
informal discussion, not reliability evidence, and one revenue claim is
unaudited.

Keep framework-specific orchestration replaceable. Invest durably in:

- contracts and idempotency;
- trace and version lineage;
- eval datasets and human calibration;
- tenant and authority boundaries;
- workload replay;
- incident and rollback machinery;
- cost and outcome attribution.

Those survive changes in model and framework names.

## Worked example: a tool call that never happened

A financial assistant returns:

> Transfer completed successfully.

The model produced valid structured output, but the bank tool timed out before
execution. An error handler replaced the exception with a friendly string,
which entered context as if it were a tool result.

The repair:

1. tool results become typed states: `committed`, `not_committed`, or
   `unknown`;
2. only the tool adapter can mint a committed receipt;
3. the final response contract forbids success without that receipt;
4. unknown outcomes reconcile by idempotency key before retry;
5. the incident trace becomes a regression and injected-fault test;
6. the user receives a clear pending state rather than a narrative.

The model was the last storyteller, not the root cause.

## Field exercise: pre-mortem one workflow

Consume the capstone artifacts from Chapters 1–21. At minimum, inject one
failure from each family: context/retrieval, model/output, tools/orchestration,
serving/concurrency, tenant isolation, and evaluator/telemetry.

For the core submission, use the canonical
[lab-fixture trajectories](lab-fixture.md) and add one bounded manifestation
per family. For the stretch submission, expand every material layer and seam
with:

- one loud failure;
- one plausible HTTP-200 failure;
- one delayed contamination;
- one retry-amplified failure.

For each, name detection, safe user outcome, rollback/reconciliation, and the
test that will prevent recurrence.

## Interview checkpoint

**Question:** “What production failures are unique or especially dangerous in
LLM systems?”

A strong answer says many failures are ordinary distributed-system faults made
silent by plausible generation. It covers wrong retrieval/context, semantic
schema errors, cross-request state and streaming assembly, retries and
side-effect ambiguity, environment/provider drift, model/routing changes,
poisoned memory, and evaluator failure. It proposes semantic invariants,
trajectory/concurrency tests, shadow-canary rollout, sabotage, and a
postmortem-to-regression loop.

**Explain it back:** Why is converting every exception into a friendly model
message sometimes worse than returning an error?

## Capstone increment

Turn the pre-mortem into injected-fault records. Each record must name trigger,
boundary invariant, detection, safe UX, cancellation or
rollback/reconciliation, owner, and the regression/fuzz/sabotage test added
afterward. Feed the failed evaluation and trace back into Chapters 15–16.

Make one record an end-to-end overload campaign that imports Chapter 6's
scheduling artifact. Declare bounded queues and admission/load-shedding policy
at ingress, retrieval, tools, model providers, persistence, evaluators, and
background workers; propagate deadlines and Chapter 11's cancellation states;
enforce per-tenant fairness, one global retry budget, circuit breakers, cleanup,
and Chapter 12's honest degraded UX. Concurrently inject slow retrieval, a tool
timeout after commit, provider 429s, evaluator backlog, client disconnect, and
a noisy tenant. Start with the fixture's `core-isolation-overload`,
`core-provider-429`, and `core-commit-unknown` events; extensions vary scale and
infrastructure without silently changing their expected invariants.

**Definition of done:** each of the six failure families produces observable
terminal evidence, cannot silently report success, and leaves one durable
regression. The overload campaign passes predeclared numeric fairness and SLO
thresholds, has no orphan work or retry cascade, and does not declare terminal
`cancelled` until in-flight effects are reconciled or durably ledgered. A
redaction failure drops or quarantines unsafe content and emits only a
metadata-safe alarm.

## Part V checkpoint and capstone defense

Without notes, defend:

- the authenticated request's context, evidence, and tenant chain;
- serving phase/capacity assumptions and their measured limits;
- every model-to-effect boundary and terminal state;
- retrieval, release, trace, and accepted-cost denominators;
- the adaptation and Pareto decision plus rejected alternatives;
- six injected failures and how each became a regression.

If a claim has no artifact, trace, test, or named source, mark it as an
assumption rather than improvising certainty. This defense is a source-backed,
executable production design dossier, not proof of deployment-specific
security, compliance, resilience, or operational readiness. Then return to the
[reading map](00-README.md) for a focused review route.
