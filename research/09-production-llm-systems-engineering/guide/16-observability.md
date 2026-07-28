# 16. Observability: follow the request, not just the model

An AI system is observable when an engineer can start from a user-visible
outcome and reconstruct the path that produced it: retrieval, prompts, model
calls, tool calls, retries, routing, guardrails, costs, and final delivery.

That is broader than logging an API response. It is also narrower than
mechanistic interpretability: a trace can show what entered and left a model
without explaining what happened inside its weights.

## ELI5: a parcel tracker with a quality inspector

A parcel tracker records which depots handled a package and where it waited.
That helps find a late truck. It does not tell you whether the package contains
the item the customer ordered.

Production AI needs both views:

- **execution telemetry:** where the request went, how long it waited, what it
  called, and what it cost;
- **outcome evidence:** whether the answer was useful, grounded, safe, and
  accepted.

A green latency dashboard can coexist with a broken product.

## The unit of observation is a user action

Start a trace when the product accepts an action such as “summarize this case”
or “review this pull request,” not only when the SDK invokes a model. Give that
action a stable trace ID and attach child spans for:

1. authentication, policy, and tenant resolution;
2. input normalization and prompt construction;
3. retrieval queries, filters, reranking, and selected evidence;
4. router decisions and fallback attempts;
5. each model call, including prefill and generation where available;
6. tool validation, execution, result handling, and compensation;
7. retries, repair loops, and budget decisions;
8. final validation, streaming, persistence, and user delivery.

This trace shape answers questions that a model-call log cannot:

- Did retrieval return the wrong document, or did generation ignore the right
  one?
- Did the primary model fail, or did the fallback silently change behavior?
- Did a tool time out before or after a side effect?
- Did a cheap request become expensive through retries?

[James Newton-King, “Inside the LLM Call: GenAI Observability with
OpenTelemetry”](https://opentelemetry.io/blog/2026/genai-observability/)
shows an `invoke_agent` span containing model-chat and tool-execution spans.
It is a useful reference architecture, not evidence that every framework emits
complete or compatible traces.

## A practical signal model

### Service health

Measure the ordinary distributed-system signals:

- request and dependency rate;
- error and timeout rate;
- queue delay, time to first token, inter-token latency, and total latency;
- p50, p95, and p99 rather than averages alone;
- cancellations and stream interruptions;
- CPU, GPU, memory, cache, and connection saturation.

Segment by model, route, region, tenant tier, input-size bucket, output-size
bucket, and release version. Aggregates hide noisy neighbours and long-context
tails.

### Workflow behaviour

Record:

- model and provider actually selected;
- prompt-template, policy, tool, retriever, and index versions;
- input, output, reasoning, and cached-token counts when the provider exposes
  them;
- retrieval candidate count, selected document IDs, scores, filters, and
  corpus version;
- tool name, argument-validation outcome, result class, retry count, and
  side-effect status;
- route reason, fallback reason, stop reason, and budget consumed;
- cache eligibility, scope, and hit class without exposing another tenant's
  key material.

Prefer bounded enums and identifiers over arbitrary high-cardinality text in
metrics. Keep detailed events in traces or controlled logs.

### Outcome quality

Attach delayed outcomes to the originating trace:

- deterministic contract checks;
- citation and groundedness checks;
- sampled human or calibrated-judge labels;
- user correction, retry, abandonment, or escalation;
- task completion and downstream business outcome;
- safety event and incident severity.

[Amazon Web Services, “Comprehensive observability for Amazon SageMaker AI LLM
inference: From GPU utilization to LLM
quality”](https://aws.amazon.com/blogs/machine-learning/comprehensive-observability-for-amazon-sagemaker-ai-llm-inference-from-gpu-utilization-to-llm-quality/)
usefully separates serving quantity from response quality. It is AWS product
guidance, not a controlled demonstration that its dashboard prevents
incidents. Its LLM-judge example still needs the calibration described in
[Chapter 15](15-evaluation-systems.md).

## Use a common vocabulary, but pin it

The
[OpenTelemetry project, “Gen AI semantic
attributes”](https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/)
defines fields for operation, provider, model, finish reason, conversation,
token usage, messages, and tool calls. A shared vocabulary makes instrumentation
more portable across backends and libraries.

Treat the convention like a versioned API:

- record the semantic-convention and instrumentation-library versions;
- test that required attributes are populated, not merely declared;
- normalize provider-specific token and finish-reason meanings;
- document deprecated or renamed fields;
- avoid dashboards that silently combine incompatible versions.

A standard specifies labels. It does not guarantee that two providers measure
the same event at the same boundary.

## Content telemetry is a controlled hazardous material

Prompts, retrieved passages, tool arguments, tool results, and model outputs
are excellent debugging evidence. They can also contain credentials, health
data, source code, private messages, or another tenant's records.

Use a deliberate capture policy:

1. keep content capture off by default;
2. record safe metadata and hashes or references first;
3. allow narrowly scoped, sampled capture only for an explicit purpose;
4. redact or tokenize sensitive fields before export;
5. encrypt in transit and at rest;
6. enforce tenant-aware access control;
7. separate operational access from product-data access;
8. set short, documented retention and deletion paths;
9. audit who viewed or exported content;
10. prevent observability vendors from becoming an unreviewed data processor.

The OpenTelemetry tutorial deliberately leaves prompts and tool arguments off
by default. That is a sound privacy posture, but it creates a diagnostic
trade-off. Design an incident-time escalation path before the first incident,
including who may enable capture, for which tenant, for how long, and how the
result will be deleted.

Never place raw prompt text, user IDs, document bodies, or tool arguments in
metric labels. Besides privacy risk, unbounded cardinality can make the
telemetry system itself expensive or unreliable.

## Correlation without accidental identity

Use several identifiers with different purposes:

- **trace ID:** one attempted product action;
- **run ID:** one agent or workflow execution;
- **conversation ID:** a continuing interaction, preferably pseudonymous;
- **tenant ID:** an opaque, access-controlled allocation key;
- **release IDs:** resolved versions of model, prompt, index, tools, and code;
- **evaluation case ID:** joins offline evidence without embedding case text.

Do not overload a global user identifier into every vendor span. Join sensitive
identity in a protected system only when investigation requires it.

## Dashboards are the map; exemplars are the street view

A useful operating view links:

- rate, errors, duration, and saturation;
- token, cache, and accepted-task cost;
- route, retry, fallback, and termination distributions;
- retrieval and answer-quality signals;
- safety and privacy events;
- release annotations.

From a histogram spike, an engineer should be able to open an authorized trace
exemplar and see the causal path. From a failed evaluation or user report, the
same engineer should find the matching production shape.

Alert on actionable symptoms and budgets, not every metric twitch. Examples:

- p95 time to first token exceeds the SLO for long-context requests;
- tool timeouts cause budget exhaustion above a threshold;
- groundedness falls only on the new index version;
- fallback traffic rises while top-line success remains flat;
- cost per accepted workflow climbs because repair loops doubled.

## Keep conventional tools where they work

The Hacker News discussion
[“Show HN: You don’t need to adopt new tools for LLM
observability”](https://news.ycombinator.com/item?id=39371297)
includes a practitioner report of using Jaeger and Prometheus and objections to
new integration overhead. It is a self-selected discussion with vendor
participants, not an adoption survey.

The durable lesson is architectural: LLM-specific evaluation and trace fields
can extend ordinary metrics, logs, and distributed traces. A separate platform
must earn its place through capabilities such as controlled content review,
dataset curation, or trajectory evaluation—not through a claim that normal
observability no longer applies.

## Worked example: the answer is wrong but everything is green

A support assistant suddenly cites obsolete refund policy. API latency, error
rate, and GPU utilization are normal.

The request trace shows:

1. the new index version was selected;
2. retrieval returned the old policy with a high score;
3. the old document lacked a tombstone because deletion propagation failed;
4. the model accurately summarized the retrieved text;
5. the citation resolver succeeded because the document still existed;
6. sampled policy-correctness evaluation failed.

The incident belongs to corpus lifecycle, not model availability. The repair
is to fix deletion/version invariants, rebuild the affected index, replay the
failed slice, and monitor policy-version distribution. “Tune the prompt” would
hide the cause.

## Field exercise: write one trace contract

For a workflow you know, draw the parent span and every dependency. For each
span, specify:

- mandatory attributes;
- timing boundary;
- failure and cancellation states;
- content-capture rule;
- tenant and release correlation;
- metric derived from it;
- retention and owner.

Then answer: can you distinguish wrong retrieval, wrong reasoning, wrong tool
execution, and wrong final delivery without storing every prompt?

## Interview checkpoint

**Question:** “What would you instrument in a production LLM application?”

A strong answer starts with an end-to-end user-action trace, then separates
service health, workflow behaviour, answer quality, and business outcome. It
mentions model/tool/retrieval/retry/fallback spans, tail latency and token
metrics, resolved release versions, controlled content capture, tenant-aware
access and retention, and joining offline eval failures back to production.

**Explain it back:** Why can an LLM endpoint have 99.99% availability while
the AI product is effectively down?

## Capstone increment

Make the field exercise the assistant's trace contract. The parent action must
carry tenant and release identity and link route, recovery, budget, retrieval,
evaluation, tool, and terminal-state IDs from Chapters 9–15. Apply a content
policy that makes source references debuggable without retaining raw private
document text by default.

Materialize a telemetry-policy artifact that classifies fields and states the
pre-export redaction rule, content-capture default, sampling policy,
tenant/operator access, retention, trace-loss detector, and redaction-failure
state. Seed secret canaries into prompts, retrieved text, tool arguments,
results, exceptions, and evaluation exports; inspect every configured log,
trace, evaluation, and vendor sink.

**Definition of done:** begin with one failed Chapter 14–15 evaluation case and
locate the corresponding production-shaped trace and failing stage, while an
unauthorized operator cannot view sensitive content. If redaction fails,
quarantine or drop the content and emit a separate metadata-only alarm; never
export the raw payload merely to preserve a trace.

Next: [Cost attribution](17-cost-attribution.md) turns the same trace into unit
economics and enforceable budgets.
