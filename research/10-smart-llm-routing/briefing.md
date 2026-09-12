# Briefing: Smart LLM Routing for Enterprise Economics

## Verdict

Routing is useful when it is a measurable policy intervention over a known
workload. It earns its complexity when a fixed baseline cannot meet the same
quality, safety, latency, or budget target and a route policy improves the
accepted-outcome frontier. A generic “send easy prompts to a cheap model” rule
is only a hypothesis. The accepted unit is a completed, correct, authorized,
and usable business outcome.

The research evidence supports a cautious design. Papers such as
[FrugalGPT](https://arxiv.org/html/2305.05176) and
[RouteLLM](https://arxiv.org/html/2406.18665) make routing and cascades
measurable on named datasets and objectives. Vendor and practitioner accounts
show practical patterns, gateways, and possible savings, but their percentages
are environment-specific claims. [FinOps guidance](https://www.finops.org/wg/optimizing-genai-usage/)
and the [zero-cost fallacy discussion](https://www.thoughtworks.com/insights/blog/open-source/zero-cost-fallacy-agentic-era)
support counting retries, platform capacity, operations, and human rework.
Community conversations are useful for failure hypotheses and operational
questions; they do not establish prevalence or ROI.

## The request path

```text
authenticated request
  → R0 canonical envelope
  → R1 identity, sensitivity, residency, authority, budget, and tool gates
  → optional R2 classifier over redacted features, fixed route enum only
  → R3 scorer over the eligible set and versioned registry
  → one declared worker or bounded fallback
  → deterministic schema/semantic validation
  → approval for irreversible effects
  → outcome, cost, quality, and audit ledger
```

The route registry is an expiring, versioned record of model capability,
supported schemas and tools, account and region, quota, latency evidence,
price facts, and policy restrictions. An API-compatible endpoint may still have
different context behavior, tool semantics, rate limits, retention, or quality.
The scorer must therefore choose an enum whose contract has already been
reviewed. When identity, policy, registry freshness, or residency is unknown,
the safe result is a declared degradation or a blocked request.

## Economics

Use one trace and one outcome key to join the complete path:

```text
accepted_cost = model input/output/cached/reasoning units
              + gateway, retrieval, tool, and evaluator work
              + retries and fallbacks
              + allocated platform capacity and operations
              + material human rework

cost_per_accepted = total route cost / accepted outcomes
```

This measure is proposed accounting policy, not a provider fact. Provider
price pages are effective-dated and must be checked at decision time, for
example [OpenAI API pricing](https://openai.com/api/pricing/),
[Claude pricing](https://platform.claude.com/docs/en/about-claude/pricing),
[Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing),
[DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing), and
[Amazon Bedrock pricing](https://aws.amazon.com/bedrock/pricing/). Cache and
batch terms change the route economics and the SLO, so they belong in the
route ledger rather than in a footnote. See the official
[OpenAI caching](https://platform.openai.com/docs/guides/prompt-caching),
[Anthropic caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching),
and [Gemini caching](https://ai.google.dev/gemini-api/docs/caching) pages.

An illustrative replay might send 100 requests through an always-capable
baseline, an always-efficient baseline, and a fixed cascade. If the cascade
has lower model spend but creates more repair and human-review work, it has not
won. Report accepted count, false-cheap failures, repair rate, p95 latency,
hard-gate violations, total cost, and cost per accepted outcome with the
traffic strata and uncertainty interval. A router's benefit must survive the
same requests and the same acceptance rubric.

## Enterprise migration

The migration starts with inventory, not provider shopping. Map four existing
lanes: coding-assistant subscriptions and IDE flows; managed cloud calls such
as Bedrock; in-house open-weight services; and deterministic workflows that
need no model. A gateway may centralize budgets, attribution, routing, and
traces for APIs it actually intercepts. It may not silently claim control over
IDE completion traffic or replace a subscription contract. Build a scope
matrix before promising one control plane.

1. **Observe:** freeze a workload taxonomy, current baseline, acceptance
   labels, data-boundary matrix, route registry, and trace schema. Capture
   cost and outcome joins without changing user-visible behavior.
2. **Shadow:** replay and shadow candidate policies with redacted traces. Test
   hard gates, route eligibility, quality slices, cache isolation, queue tails,
   and evaluator independence.
3. **Canary:** activate a named low-consequence cohort with an explicit kill
   switch, capacity reservation, rollback owner, and daily review. Keep the
   direct baseline available.
4. **Expand:** add strata only when acceptance, safety, latency, cost, and
   reconciliation gates hold. High-consequence side effects remain behind
   approval and exact action-digest checks.

Proposed SLOs must be calibrated to the workload. For example, an interactive
route may set a target p95 time to first useful response and a maximum queue
budget, while a batch route may trade completion latency for lower cost. Those
numbers are policy proposals, not universal targets. A rollback fires on a
hard safety violation, material acceptance regression in any protected stratum,
two consecutive latency-budget breaches, registry expiry, unexplained cost
increase, or reconciliation uncertainty after a possible side effect.

## Evidence boundaries

The packet distinguishes:

- **primary facts:** official pricing, capability, regulatory, or product
  pages, each linked and audited on 2026-09-12;
- **research measurements:** papers with their dataset, method, and objective;
- **vendor/practitioner claims:** useful mechanisms or case evidence with
  incentives and transfer limits stated;
- **community signal:** headed Hacker News and native social observations,
  retained as anecdotes and failure hypotheses;
- **proposal:** architecture, formulas, SLOs, and rollout gates awaiting
  replay/shadow/canary proof;
- **uncertainty:** unresolved transcript labels and unavailable or identity-
  mismatched pages that are not promoted into claims.

The source corpus contains 75 retained page records across primary, research,
practitioner, vendor, benchmark, and community lanes. The headed extractor
captured 78 initial selections, passed 71, and recovered four of seven quality
failures on the one permitted timing retry. Five pages remain unavailable for
clean article synthesis because they redirected to a generic or mismatched
surface or showed a security/site-shell response. Those limitations are part
of the result.

## Graph and governance

The [graph and enterprise architecture](architecture.md) carries the node,
edge, state, failure, budget, security, and observability contracts. `O1` owns
workflow state and the append-only outcome ledger. Policy, identity, approval,
and business side effects remain owned by deterministic systems. Every event
carries run, tenant, graph, policy, route registry, node, attempt, and outcome
identifiers, with content redaction and retention controls. Runtime status
remains **design-only** until the named validation gates pass. The fuller
capsule research packet remains the planning record outside this repository.

The guide turns this briefing into a sequence of working artifacts: a route
card, acceptance taxonomy, baseline/oracle sheet, route envelope and registry,
cascade calculator, router-family decision, route cost ledger, SLO curve,
cache/batch policy, managed-versus-local TCO sheet, portfolio map, policy
evaluation matrix, graph contract, and rollout ADR.
