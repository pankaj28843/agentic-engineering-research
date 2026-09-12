# Smart LLM Routing for Enterprise Economics

This theme teaches how to choose an LLM route for a request when quality,
privacy, latency, reliability, and total cost all matter. It is written for a
large regulated enterprise that already has coding-assistant adoption, managed
cloud access, and some in-house open-weight serving. The examples use a
fictional enterprise and keep provider selection subordinate to policy.

The durable reader artifact is the [14-chapter guide](guide/00-README.md).
The [briefing](briefing.md) gives the architectural verdict and migration
shape; the [source index](source-index.md) identifies the 75 retained source
records; and the [research log](research-log.md) records the bounded headed-CDP
collection, extraction, reviews, and limitations. The machine-readable source
catalog is [`sources.json`](sources.json).

The guide's central question is:

> For this request, why was this route eligible, why was it selected, what
> quality and latency did it buy, what did the whole path cost, and what
> evidence would make the policy change?

A route is a policy-qualified execution path. It includes the model or
deterministic handler, context and tool contract, data boundary, budget,
validation, retries, fallbacks, and outcome accounting. A model name by itself
is not a route and a low token price is not a low cost per accepted outcome.

## Reader contract

Each chapter explains one mechanism with an everyday analogy, a concrete
worked example, a failure drill, and exercises. Facts, measurements, vendor
claims, practitioner reports, community anecdotes, inferences, and proposals
are labelled separately. Numerical examples marked *illustrative* are teaching
assumptions; they are not provider prices or forecasts.

The guide assumes strong software, API, distributed-systems, security, and
observability experience, while introducing model-serving vocabulary from
first principles. It uses [Theme 09](../09-production-llm-systems-engineering/README.md)
as a technical floor for serving, caching, tools, evaluation, and safety, then
focuses on the route-specific economic and governance consequence.

## Evidence date and uncertainty

The source audit was performed on **2026-09-12**. Current prices, product
availability, and model capabilities are time-sensitive; consult the dated
official page in the [source index](source-index.md) before using them in a
decision. The labels **Astra**, **OASIS**, **DeepSeek Flash**, **GPT-5.6 Luna**,
and **Fable** came through the task context or noisy discovery material. This
packet keeps them as unresolved labels. It does not attribute them to a
provider, treat them as product names, or use them in a price or capability
comparison.

## Durable design rule

The proposed request path is:

```text
R0 ingress → R1 deterministic policy → (R2 bounded classifier)
  → R3 deterministic scorer → W model/local worker → V1 validation
  → (A1 approval) → O1 outcome ledger
```

`R1` owns identity, tenant, sensitivity, residency, authorization, tool
eligibility, and budgets. `R2` may return only a declared route enum and
reason. No model can grant itself authority, broaden a data boundary, or
discover an undeclared provider. This is a design proposal until replay,
shadow, canary, reliability, security, and rollback evidence passes.

## What the packet delivers

- an evidence-weighted routing and economics briefing;
- a typed graph and enterprise migration architecture;
- a cumulative workbook path from route card to rollout ADR;
- a companion home knowledge-base study page;
- a four-episode production-ready podcast series;
- private Markdown, EPUB, PDF, and available conversion outputs under
  `tmp/books/` after the publishing gate.
