# Guide: Smart LLM Routing for Enterprise Economics

This is a 14-chapter, ELI5-first book for engineers who need a routing policy
that can survive a finance review, a security review, an incident, and a
reader asking “what did this request actually cost?” Read the chapters in
order. Each one adds an artifact to the same decision record.

## The path through the book

```text
01 route card
  → 02 acceptance taxonomy and strata matrix
  → 03 baseline/oracle/Pareto sheet
  → 04 route envelope and capability registry
  → 05 cascade calculator
  → 06 router-family decision
  → 07 route cost ledger
  → 08 SLO and capacity curve
  → 09 cache/batch/gateway policy
  → 10 managed-versus-local TCO sheet
  → 11 portfolio migration map
  → 12 policy evaluation matrix
  → 13 auditable graph contract
  → 14 rollout ADR and decision lab
```

## Chapters

1. [The Restaurant With Several Kitchens](01-restaurant-several-kitchens.md)
2. [Good Enough Is a Contract](02-good-enough-contract.md)
3. [Prove the Router Earns Its Complexity](03-baselines-oracles-pareto.md)
4. [Hard Gates First](04-hard-gates-route-envelopes.md)
5. [Cascades and Escalation](05-cascades-escalation.md)
6. [Router Families](06-router-families.md)
7. [Prices Are Not Costs](07-prices-are-not-costs.md)
8. [Latency Has a Price](08-latency-queueing-slos.md)
9. [Caches, Batches, and Gateways](09-caches-batches-gateways.md)
10. [Managed APIs and In-House Open Weights](10-managed-vs-local-tco.md)
11. [The Existing Portfolio](11-copilot-bedrock-local.md)
12. [Evaluate the Policy](12-evaluate-the-policy.md)
13. [The Auditable Routing Control Plane](13-auditable-control-plane.md)
14. [Shadow to Sustainable Adoption](14-shadow-to-sustainable-adoption.md)

## Reading rules

“Fact” means the linked source directly supports the statement. “Measurement”
means a paper or independent benchmark with a bounded workload. “Vendor claim”
means an interested party's account whose method and transfer limits must be
read. “Anecdote” means a community observation useful for generating a test.
“Proposal” means the design in this book and is not production evidence.

Use the [source index](../source-index.md) to move from an ID to its canonical
URL and capture quality. Prices, model capabilities, and availability need an
official dated page at the time of use. The labels Astra, OASIS, DeepSeek
Flash, GPT-5.6 Luna, and Fable are deliberately left unresolved.

## Prerequisite floor

Theme 09's chapters on model-serving mechanics, caching, tools, observability,
evaluation, cost attribution, safety, and isolation are useful references.
This guide assumes those contracts and asks a narrower question: how does a
route policy change the quality, latency, authority, and accepted-outcome
economics of the whole request?

## A compact glossary

An **eligible route** is a declared path that has passed deterministic identity,
data, authority, capability, and budget checks. An **acceptance contract** is
the test that turns an attempt into an accepted business outcome. A **stratum**
is a workload slice whose risk, quality, or economics can differ enough to
change the route decision. A **cascade** is a bounded sequence in which an
observable signal decides whether to escalate; it is not an unlimited retry.

An **oracle** is a retrospective diagnostic that knows which route would have
worked best; it is not a deployable policy. A **route registry** is the
versioned, expiring record of pins, capabilities, regions, tools, prices,
capacity, and evidence. A **hard gate** removes an ineligible route. A **soft
score** ranks routes left after those removals. **Accepted-outcome cost** counts
the entire path and divides by accepted results. **Goodput** counts useful
accepted work per time, not tokens emitted. **Indeterminate** means a possible
external effect is not yet reconciled and therefore cannot be silently counted
as success or failure.

The graph names `R0` for trusted ingress, `R1` for deterministic policy, `R2`
for an optional bounded classifier, `R3` for deterministic scoring, `W` for a
declared worker, `V1` for validation, `A1` for approval, and `O1` for the
outcome ledger. These labels are contracts, not vendor products.

## How to use the evidence

When a chapter cites a primary page, ask what it establishes: a documented
price, product behavior, release description, serving metric, or governance
framework. When it cites a paper, read the dataset, objective, method, and
limitations. When it cites a vendor or practitioner account, separate the
mechanism from the incentive and transferability. When it cites HN or another
community source, treat it as an attributed anecdote that suggests a test.

For a real decision, copy the chapter's artifact into a working record. Put a
date and owner on each volatile field. Keep the baseline alongside the
candidate. Use the same request IDs and context versions in replay. Record
abstentions, blocks, partial results, repairs, human work, and indeterminate
effects. Then ask whether the observed gain remains after route eligibility,
latency, capacity, and privacy gates are applied.

The packet's proposed route can be summarized as:

```text
trusted facts → hard envelope → eligible enum set → bounded choice
  → typed execution → acceptance/approval → outcome and cost evidence
```

If the evidence does not support a choice, keep the simpler baseline or block
with a useful reason. The reader's final deliverable is a reversible decision,
not a permanent ranking of model names.

The exercises are part of the guide, because a route that cannot be explained
on paper is difficult to operate safely in production.
