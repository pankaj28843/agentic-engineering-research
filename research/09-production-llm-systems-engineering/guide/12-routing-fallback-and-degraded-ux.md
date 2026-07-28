# 12. Routing, fallback, and degraded UX

Routing chooses an execution lane for a request: model, provider, region,
precision, retrieval path, or deterministic implementation. Fallback chooses
what happens when that lane is unavailable or fails its acceptance gate.
Degraded UX tells the user what capability remains.

A resilient system needs all three. Silently replacing a strong model with a
weaker one is not graceful degradation if it changes the product promise.

## ELI5: triage, ambulance diversion, and honest signage

A hospital triages patients to different specialists. If the MRI is down, it
may use another site or a less informative test. Staff do not tell the patient
“nothing changed.” They explain the delay, limitation, and next step.

The router is triage. Fallback is the alternate path. Degraded UX is the
honest explanation and reduced-capability workflow.

Where the analogy breaks: deterministic residency, capability, and
authorization rules establish eligible lanes before any learned router.
Routing is policy-qualified selection, not clinical diagnosis.

## Routing is constrained optimization under uncertainty

For request features \(x\), choose a lane \(m\) that minimizes expected loss:

```text
expected total loss
  = inference cost
  + latency/SLO penalty
  + expected quality failure and rework
  + compliance/security penalty
  + availability risk
```

Subject to hard constraints such as data residency, model capability, context
length, tool support, customer tier, and deadline.

The hard constraints run before any learned quality/cost optimizer. A cheap
model outside the allowed region is not a candidate.

## Begin with explicit rules

A legible routing table often beats a premature learned router:

| Condition | Route | Reason |
| --- | --- | --- |
| Deterministic parser covers request | Code path | No inference needed |
| Sensitive tenant/region | Approved provider pool | Compliance boundary |
| Background batch | Throughput lane | No interactive deadline |
| Complex tool workflow | Capability-qualified model | Tool/recovery eval |
| Ordinary low-risk request | Efficient default | Cost/latency |

Rules should live in a versioned decision service, not scattered across UI and
backend conditionals. Log the matched rule and candidate exclusions.

[LogRocket, “LLM routing: choosing the right model for requests”](https://blog.logrocket.com/llm-routing-right-model-for-requests/)
is a practical application overview that recommends beginning simply and
making decisions visible. Its numerical heuristics and product comparisons are
practitioner/vendor-market claims; use the architecture patterns rather than
copying thresholds.

## Learned routers need an outcome label

A classifier cannot route for “quality” until quality is operationalized. It
might predict:

- whether a cheap lane will pass a task-specific evaluator;
- expected score for every candidate;
- request complexity;
- probability of escalation;
- cost at a required quality floor.

[Jasper Dekoninck et al., “A Unified Approach to Routing and Cascading for LLMs” (RouteLLM, arXiv:2410.10347)](https://arxiv.org/html/2410.10347v3)
studies cost-quality routing and cascading.
[Zhongzhan Huang et al., “RouterEval: A Comprehensive Benchmark for Routing LLMs to Explore Model-level Scaling Up in LLMs” (arXiv:2503.10657)](https://arxiv.org/html/2503.10657)
tests routers across tasks and highlights generalization weaknesses. The latter
was acquired as a browser PDF, converted from its text layer with OCR disabled,
and cross-checked against arXiv HTML. Both are research benchmarks; neither
proves that a router trained on public preference data predicts acceptance for
your product.

[IBM Research, “Large Language Model Routing With Benchmark Datasets”](https://research.ibm.com/publications/large-language-model-routing-with-benchmark-datasets)
shows how benchmark datasets can train model selection and explicitly notes
utility and limits. A benchmark label is useful only if it resembles the
production decision.

## False-cheap and false-expensive routes

Compare a router with three baselines:

- always use the capable model;
- always use the efficient model;
- an **oracle**—an impossible comparison that knows each outcome in advance.

Track:

- **false-cheap:** an insufficient lane fails, retries, or causes harm;
- **false-expensive:** a costly lane handles work a cheaper path would accept;
- router latency and cost;
- quality after fallback, not just first route;
- repeated context and tool cost during escalation;
- user corrections and abandonment.

A cheap first attempt plus expensive retry can cost more and feel slower than
starting with the stronger lane.

## Fallback is a compatibility problem

Providers and models differ in:

- tokenizer and context limit;
- tool and schema support;
- refusal and safety behavior;
- streaming event format;
- system-message precedence;
- regional and data-processing terms;
- latency, rate limits, and model aliases.

Use a canonical internal request/response model and capability registry.
Adapters must surface unsupported features instead of silently deleting them.
Re-evaluate the fallback on the same product tests; “API-compatible” does not
mean behavior-compatible.

## Error-directed fallback

Do not cascade every error through every provider.

| Failure | Appropriate response |
| --- | --- |
| Rate limit or transient outage | Retry budget, circuit breaker, compatible provider |
| Context too long | Compact/retrieve, long-context lane, or user-visible limit |
| Schema unsupported | Compatible schema/model or deterministic recovery |
| Safety refusal | Do not evade policy by provider hopping |
| Permission/policy denial | Stop |
| Low semantic confidence | Stronger lane, more grounding, or human review |
| Global dependency failure | Static/read-only degraded experience |

Provider hopping after a refusal can become policy laundering. Preserve the
product’s safety contract across lanes.

## Circuit breakers and retry storms

When a provider is unhealthy:

1. classify failures by provider/model/region;
2. open the circuit after a bounded threshold;
3. stop feeding predictable failure;
4. probe recovery with controlled traffic;
5. respect a global retry and deadline budget;
6. shed low-priority work before saturating every fallback.

Independent-looking providers can share a cloud region, model host, gateway,
DNS path, or quota. Test correlated failure and know which dependencies are
actually diverse.

## Design degraded UX as a product state

Examples:

- search results are available, but synthesis is temporarily disabled;
- a draft is shown without automated citations and is clearly labelled;
- the user can submit a background job instead of waiting interactively;
- read-only inspection remains while mutating tools are unavailable;
- a concise answer is offered because the long-context model is unavailable;
- the system preserves work and lets the user resume.

Show what changed, what was not completed, and what happens next. Do not expose
provider trivia unless useful, but do not imply the normal quality guarantee
still holds.

## Worked example: customer-support assistant

Normal lane: grounded response with account tools and a capable model.

Fallback plan:

1. if the model provider is transiently unavailable, use a compatible model
   only after tool/schema evals pass;
2. if account tools are down, prohibit account-specific assertions and show
   public help plus an incident message;
3. if retrieval is stale, cite the snapshot date and avoid policy decisions;
4. if all inference is down, preserve the conversation and create a human
   support ticket with user consent;
5. never route private account data to an unapproved provider.

This is more resilient than a chain that merely tries Model A, B, and C.

## Interview checkpoint

**Question:** “How would you reduce cost with model routing?”

A strong answer defines a task-specific acceptance label, hard policy
constraints, simple baselines, shadow evaluation, false-cheap/false-expensive
rates, end-to-end cost after retry, observable route reasons, capability-aware
fallback, circuit breakers, and degraded UX. It asks whether routing complexity
is justified at current volume.

**Explain it back:** Why can a fallback increase availability while reducing
the correctness of the product unless the UI and acceptance gates change too?

## Capstone increment

Build a route table for the assistant with normal lane, deterministic
eligibility filters, compatibility gate, error-directed fallback, lost
capabilities, exact UI disclosure, retry budget, and stop condition. Include
provider outage, stale retrieval, unavailable tools, and insufficient evidence.
Reuse Chapter 11's terminal states and budgets. Add a dependency-scoped circuit
breaker and one global retry budget shared across the preferred lane and every
fallback so provider hopping cannot multiply load.

**Definition of done:** every injected lane failure reaches a compatible
fallback or an honest degraded/terminal state; no private document crosses an
unapproved provider boundary, and exhausting the global retry budget cannot
create a fallback cascade.

## Part II checkpoint

- **Explain from memory:** valid syntax is not valid meaning; a model proposes
  tool intent; budgets and routes are orchestrator-enforced state.
- **Update the capstone:** walk one read and one ambiguous write from proposal
  through authorization, recovery, budget, and degraded UX.
- **Keep unresolved:** how do we make the external evidence lifecycle and its
  quality measurable? Part III builds that data and evaluation plane.

Next: [RAG architecture](13-rag-architecture.md) develops the data path that
grounds many routed model calls.
