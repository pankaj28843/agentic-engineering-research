# 14. Shadow to Sustainable Adoption: Make the Decision Reversible

## ELI5 hook

A bridge crew does not close the old bridge on the first day that a new bridge
looks complete. It measures the new structure, sends empty trucks across it,
opens one lane to light traffic, watches the joints, and keeps a barrier ready
to send cars back. The crew also decides who can close the lane, what evidence
counts as a failure, and how quickly the old path can resume.

A routing policy needs the same adoption discipline. The goal is not to launch
a clever classifier. The goal is to make a reversible, measurable change to
accepted work. A durable rollout has a fixed baseline, named owners, policy and
registry versions, protected strata, capacity reservations, a kill switch, and
an economic ledger.

## Mechanism: a staged decision lab

Use the cumulative artifacts from this book as a decision lab:

1. **Route card:** state the user journey, accepted outcome, consequence,
   allowed data, deadlines, and non-goals.
2. **Evidence and strata:** record the acceptance rubric, protected slices,
   current baseline, and uncertainty. Keep unresolved provider labels out of
   the registry.
3. **Baseline ladder:** compare deterministic, fixed single-model, cascade,
   verifier, and candidate router policies on the same replay.
4. **Policy envelope:** freeze identity, residency, tool, authority, budget,
   and route enums. Sign or otherwise version the registry and expiry.
5. **Shadow:** run candidate decisions beside production. Compare route mix,
   queues, cache behavior, quality, cost, and hard gates with no user effect.
6. **Canary:** choose a low-consequence cohort, reserve capacity, set exposure
   and stop limits, and publish the rollback owner and deadline.
7. **Expansion:** add one protected stratum or channel at a time. Recheck the
   scope matrix for Copilot, managed APIs, and local services. Reconcile the
   accepted-cost ledger before claiming a gain.

Treat the result as a rollout ADR. It should state the context and current
baseline, decision, alternatives rejected, route envelope, evidence, open
unknowns, owners, SLOs, rollback triggers, and review date. A “successful”
router without a review date becomes an unexamined dependency as prices,
models, workloads, contracts, and policies change.

Suggested owners are distributed: platform owns the route registry and
control plane; SRE owns capacity, latency, and incident response; product owns
the accepted-outcome contract; domain owners calibrate quality; security and
legal own data boundaries and regulatory interpretation; procurement owns
provider terms; FinOps owns allocation and reconciliation; audit owns evidence;
and the provider owner owns upstream changes. No single model team should own
all authority.

Proposed rollback triggers include a hard safety or residency violation; a
protected-stratum acceptance regression; two consecutive SLO breaches; an
expired or drifting registry pin; unexplained cost per accepted outcome;
capacity exhaustion that threatens the fallback; cache isolation failure; or
an unreconciled possible side effect. Rollback restores the named fixed
baseline, stops new candidate decisions, preserves traces, and opens an
incident. It does not delete evidence or silently retry into another boundary.

## Worked example: a ninety-day adoption plan

The schedule below is an **illustrative plan**, not a promise of duration.

**Weeks 1–3: observe.** The platform team inventories server-side Bedrock
traffic, local service calls, and the Copilot channel separately. Product
defines accepted resolution and rework. Security writes the data-class and
residency matrix. FinOps joins trace IDs to invoices where possible and marks
subscription allocation unknown where it cannot. No route changes.

**Weeks 4–6: replay and shadow.** The team freezes 1,000 stratified requests,
compares Always-Mid, direct capable, cascade, and candidate router policies,
then shadows the candidate on server-side traffic. Local capacity is load-
tested at projected peak. Cache isolation and indeterminate-effect tests run.
The candidate is rejected if it does not beat the content-free fixed baseline
at the required acceptance floor or if any hard gate fails.

**Weeks 7–9: canary.** A low-consequence, non-side-effect cohort receives the
policy. The exposure is fixed. An operator can disable the candidate and
restore the baseline. Daily review covers acceptance by stratum, p95 latency,
escalation, human work, provider and local capacity, cache errors, route
registry age, and cost per accepted outcome.

**Weeks 10–13: decide.** If the canary clears the gates, expand one workload
class. If the benefit is indistinguishable from Always-Mid, remove the router
overhead. If a restricted class has no qualified fallback, keep it on the
direct baseline or block when capacity fails. If Copilot remains outside the
gateway, publish a separate product-control decision rather than counting it
as routed traffic.

An ADR might conclude: “Adopt the policy for server-side low-consequence
readonly requests under registry v12; retain fixed capable routing for
restricted multilingual policy requests; keep account-state proposals behind
approval; leave Copilot IDE completion outside the gateway scope; review in 30
days.” That is a useful decision because it names boundaries and uncertainty.

## Failure drill: incentives defeat the gate

The platform team is measured on provider invoice reduction. Product is
measured on request completion. Reviewers are measured on response time. The
router lowers token spend by sending difficult cases to a cheap route, which
raises rework and causes product to hide abstentions. Each dashboard is green
for its owner while the user journey worsens.

Make the accepted outcome and protected strata shared gates. Publish one route
ledger with cost, quality, latency, safety, rework, and coverage. Require a
fixed baseline and a route-policy owner to sign the ADR. Count `blocked`,
`abstain`, `partial`, and `indeterminate` as visible states. A cheaper
provider is not a successful policy if the enterprise must repair the result
or cannot prove where the data went.

Revisit the decision after provider price changes, model or runtime updates,
workload shifts, policy changes, incidents, and material cache or context
changes. The [FinOps GenAI guidance](https://www.finops.org/wg/optimizing-genai-usage/)
supports this ongoing accountability. [OpenAI harness engineering](https://openai.com/index/harness-engineering/)
and [Fowler's independent account](https://martinfowler.com/articles/harness-engineering.html)
support the broader operational lesson that feedback surfaces and repository
or environment design alter agent outcomes. Neither is proof of a router's
ROI.

## Reader exercises

1. Draft a one-page rollout ADR. Include baseline, route envelope, evidence,
   SLO, owners, open unknowns, rollback triggers, and review date.
2. Create a shadow-to-canary checklist for one low-consequence workload. Add
   the failure injection that would cause an immediate rollback.
3. Draw an owner map across platform, SRE, product, domain, security, legal,
   procurement, FinOps, audit, and provider operations. Identify an authority
   gap.
4. Write the decision you would make if the router saves tokens but loses
   against Always-Mid on cost per accepted outcome, or if it wins economics
   but fails one residency test.

## The decision lab scorecard

At the end of a shadow or canary, hold a review that starts with the baseline
and the protected strata. A useful scorecard is deliberately balanced:

```text
coverage: which requests received a useful path?
quality: which outcomes passed each contract?
safety: did any authority or data-boundary gate fail?
latency: did route-class tails meet the SLO?
economics: what did each accepted outcome cost?
operations: what queue, capacity, retry, and review work appeared?
evidence: which claims are measured, unknown, or vendor-supplied?
reversibility: can the exact baseline be restored and proved?
```

Require a written disposition for each row: adopt, keep in shadow, revise,
or reject. “Adopt” should include a scope, registry revision, exposure, review
date, and rollback command or control. “Keep in shadow” is a real outcome when
the sample is too small or the traffic is unrepresentative. “Reject” should
name the failed assumption so another team does not repeat the experiment with
a different model alias.

The scorecard should include disagreement. A product owner may see more useful
answers while FinOps sees higher accepted cost. Security may reject a fallback
that the latency report prefers. Resolve the conflict by returning to the
route envelope and the stated success predicate. Do not average an authority
violation into a positive score. A hard gate is a constraint, not a weighted
preference.

Set the next measurement before closing the meeting. If local utilization is
the dominant unknown, schedule a production-shaped load test. If Copilot
scope is unobserved, assign a product-control investigation. If judge
agreement is weak, expand human calibration. If a provider price is stale,
expire the registry route. The review creates the next experiment rather than
turning a provisional result into permanent folklore.

A sustainable policy has a change budget. Limit how many route, prompt,
registry, evaluator, and context changes can enter one release. Otherwise a
quality improvement and a price change arrive together and the team cannot
identify causality. Keep old policy revisions and route traces long enough to
compare the before and after under the retention policy. This is operational
discipline for a probabilistic dependency.

## Keeping adoption healthy

Adoption is sustainable when the route remains understandable to the people
who operate and use it. Publish a short route explanation at the right level:
the user sees the outcome and any meaningful uncertainty; the operator sees
route, policy, capacity, and fallback state; the auditor sees versions,
approval, retention, and evidence. Do not expose implementation detail that
does not help a user make a decision.

Train support and incident teams on terminal states. A blocked residency case,
an abstained answer, and an indeterminate write need different responses. If
all three are shown as “AI failed,” the organization will either bypass the
control plane or pressure it to hide uncertainty. A clear state reduces that
pressure.

Review incentives with the scorecard. The team responsible for invoice
reduction must see accepted cost and rework. The team responsible for latency
must see capacity reservation and quality. The team responsible for safety
must see every fallback and cache boundary. Shared gates make local
optimization harder to game.

Finally, make retirement normal. A route can be removed when a simpler fixed
baseline wins, a provider contract expires, local utilization is too low, or
the acceptance rubric changes. Preserve the evidence and the decision. A
smaller route portfolio is often easier to govern and cheaper to operate.

## Checkpoint

Adoption is ready to expand when the decision lab can show protected-stratum
quality, accepted cost, latency, safety, capacity, ownership, and a tested
return to baseline. The reader's artifact is a rollout ADR with a review date,
not a permanent “smart routing enabled” flag. If a simpler policy wins, retire
the router and preserve the evidence. Reversibility is part of the product
contract.

## Source slot

The staged architecture is a proposal derived from the capsule graph packet
and [the theme briefing](../briefing.md). Use [FinOps](https://www.finops.org/wg/optimizing-genai-usage/)
for cost accountability, [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework)
and the [EU framework](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)
for governance context, and [OpenTelemetry](https://opentelemetry.io/blog/2026/genai-observability/)
for evidence signals. The ninety-day plan, SLOs, and rollback triggers are
illustrative proposals. Adoption is complete only after replay, shadow,
canary, security, reliability, reconciliation, and rollback evidence passes.
