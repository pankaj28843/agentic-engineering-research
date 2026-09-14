# 7. Prices Are Not Costs: Route-Level Unit Economics

## ELI5 hook

A supermarket advertises a cheap loaf. To decide whether lunch was cheap, you
also count the bus, the ingredients you threw away, the extra trip when the
loaf was stale, and the time spent fixing the sandwich. The shelf price is
real,
but it is not the cost of a successful lunch.

An LLM invoice is the shelf price. A route's economic result includes context
assembly, gateway and retrieval work, validators, failed attempts, retries,
fallbacks, local capacity, subscriptions, operations, and human rework. The
denominator is an accepted business outcome. If the route avoids a model call
through a valid cache, that is a route effect; if it returns a wrong answer
that someone repairs, the repair belongs in the path.

## Mechanism: one trace, several ledgers

Use one run ID, tenant binding, route policy version, and outcome key to join
separate ledgers. A practical proposed formula is:

```text
accepted_cost = model input units
              + model output and reasoning units where exposed
              + cache reads/writes and context construction
              + gateway, retrieval, tool, and evaluator work
              + retries, repairs, and fallbacks
              + allocated local/cloud capacity, support, and operations
              + material human review and rework

cost_per_accepted = accepted_cost / accepted outcomes
```

Keep three views distinct. **Provider accounting** reconciles invoices and
effective-dated rates. **Engineering attribution** assigns shared gateway,
GPU, observability, and evaluator capacity to traces. **Product economics**
asks whether the accepted outcome saves time, improves coverage, or reduces
risk. A route can improve one view and worsen another.

Acceptance is a contract event, not merely a successful provider response.
For an illustrative readonly policy answer, the rubric can require the right
document version and jurisdiction, preserved exceptions, and an explicit
not-established state when the document is silent. For a tool proposal,
schema and policy acceptance of a normalized action remains separate from
approval to execute it. State whether a corrected artifact qualifies as
accepted-with-rework or whether the first answer must pass; link rejected
attempts and later repairs to the same logical request.

Abstention is a policy-chosen block. Record its reason and its effect on
coverage; it is not an accepted outcome and must not enter that denominator.
Keep blocked requests distinct from produced answers that fail the rubric.
An indeterminate effect awaits reconciliation by the owning business system;
terminal failure means the permitted recovery path has ended without
acceptance. Neither is synonymous with a transport timeout. Report the
accepted count, coverage, rejected and blocked work, pending reconciliation,
repair, and terminal failures beside the ratio. A narrow service can be
intentional, but cannot claim universal savings by abstaining on difficult
long-context or multilingual requests.

Every price record needs provider, account, region, currency, unit, effective
start and end, cache or batch treatment, and a source URL. Current official
lookup pages include [OpenAI API pricing](https://openai.com/api/pricing/),
[Claude pricing](https://platform.claude.com/docs/en/about-claude/pricing),
[Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing),
[DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing), and
[Bedrock pricing](https://aws.amazon.com/bedrock/pricing/). This packet does
not freeze values from those pages; an owner must refresh the registry before a
decision. [FinOps GenAI guidance](https://www.finops.org/wg/optimizing-genai-usage/)
is a useful source for allocation and optimization questions.

The source audit remains 2026-09-12; these links are dated evidence and lookup
locations, not a claim that rates have been checked again. Retain the endpoint
or model identifier, price-table version, attribution rule, and whether taxes,
platform fees, or internal allocations are included. Record the price category
that actually applied to each request or batch, including separate input,
output, cached, or batch work. A blended rate is interpretable only when its
category mix is visible.

Keep an immutable experiment record of attempts, measured work, acceptance,
latency, and failures separate from the projection that joins it to a named
price snapshot. A price change calls for repricing that work profile without
rewriting history. A model identifier or tokenizer change creates a new route
version. Capture deployment or endpoint revision, prompt/tool bundle, and run
date; if a provider cannot expose a stable version, record that uncertainty
as a rollout constraint. An observed invoice, a counterfactual estimate, and a
blended internal allocation are different evidence.

Include counterfactuals. If a routed request used the efficient endpoint, what
would the always-capable policy have cost under the same context and price
snapshot? If a cache hit avoided generation, what validation and storage work
remained? If a subscription fee is fixed, do not pretend it is a per-token
variable cost without supported usage and allocation data.

## Worked example: the false thirty-percent saving

The numbers below are **illustrative**. A support workflow handles 100
requests. The always-capable baseline has:

```text
model invoice                 100 units
gateway/retrieval/evaluation   20 units
human rework                    50 units
total                          170 units
accepted outcomes               90
cost per accepted outcome      1.89 units
```

The routed policy lowers model-token spend by 30%, so its model line is 70
units. But its route has more evaluator work, retries, local allocation, and
human repair:

```text
model invoice                  70 units
gateway/retrieval               20 units
evaluator                       12 units
retry and fallback              18 units
allocated platform              15 units
human rework                    80 units
total                           215 units
accepted outcomes                92
cost per accepted outcome       2.34 units
```

The routed policy accepted two more outcomes, but cost per accepted outcome
rose by roughly 24% on these assumptions. The decision could still favor it
for a different product value, safety coverage, or capacity reason, but it is
not an accepted-outcome cost win, despite the 30% token-cost reduction. If an
owner reports only the 30% model line, the dashboard is hiding the
intervention's consequence.

Sensitivity analysis identifies the important unknowns. Vary escalation rate,
human hours, cache hit rate, evaluator calls, and local utilization one at a
time and together. Record a range when the input is uncertain. Show a break-
even line: for example, what maximum human rework keeps the routed policy
below the baseline? That question is actionable for product and operations.

### The support work behind a cheap first call

In another explicitly invented example, 1,000 requests take an efficient first
route: 600 are accepted immediately, 300 are repaired by a capable route, and
100 become support cases consuming 12 minutes each. Keep those exact physical
observations before assigning money to them. The example does not establish
that every repair or support case eventually passes; record their final
acceptance instead of inferring it from arrival in a queue. A capable baseline
may avoid support work, but that is a counterfactual to test, not a result
established by the illustration.

Vary the loaded labor or opportunity cost per repair minute across an explicit
range. If the candidate wins only when attention is valued implausibly low,
the saving is fragile. Salaried attention can be an opportunity cost rather
than an invoice; if excluded from provider-cost reporting, show total service
effort separately. Count cases, active minutes, queue delay, reviewer role,
escalation, and final acceptance. Keep the repair admission rule, eligible
reviewers, and time budget fixed across baselines or label the difference.

False cheap omits work caused after the first call. False expensive can charge
a route for work it did not cause or call a capable attempt wasteful when it
prevented repair. Separate direct marginal work, allocated shared capacity,
and consequence scenarios. Observed correction minutes belong in the direct
ledger; possible incident costs belong in sensitivity or risk analysis unless
a consistent incident-allocation method exists. This avoids both omission
and double counting. Let a reader change the repair-minute assumption or
remove a shared allocation and see whether the recommendation survives.

## Failure drill: the invoice-only dashboard

A finance dashboard joins provider invoices to application volume but has no
route ID. It cannot see a repair loop, a fallback provider, a local GPU that
is reserved but idle, or a reviewer who fixes rejected output. A cheaper
provider appears to reduce spend while support time rises.

Add a trace-to-outcome key at ingress. Emit per-attempt model, route, token
usage where exposed, cache status, queue time, evaluator work, retry reason,
human disposition, and final state. Reconcile the sample against provider
invoices and payroll or review logs under a documented allocation rule. If a
cost cannot yet be attributed, label it unknown and include it in the risk
range. Do not allocate it as zero.

The [NVIDIA inference-cost discussion](https://developer.nvidia.com/blog/llm-inference-benchmarking-how-much-does-your-llm-inference-cost/)
helps expose serving cost drivers, while the [zero-cost fallacy analysis](https://www.thoughtworks.com/insights/blog/open-source/zero-cost-fallacy-agentic-era)
is a counter-evidence path for apparently free or open models. Neither source
supplies this enterprise's TCO; both support asking what the invoice omits.

## Reader exercises

1. Design a route cost event with run ID, attempt, model pin, input/output
   usage, cache status, queue time, evaluator, retry, human work, and outcome.
2. Choose the denominator for one workflow. Define accepted, partial,
   blocked, failed, cancelled, and indeterminate outcomes.
3. Run a one-variable sensitivity analysis for escalation, cache hit rate,
   and human rework. Identify the first unknown that deserves measurement.
4. Explain how a fixed subscription fee, shared gateway, or idle local GPU
   should appear in your allocation policy. Name the owner of each assumption.

## Reconciliation is part of the calculation

An accepted-cost number is only as trustworthy as its reconciliation path. At
ingress, create one idempotent run and outcome key. Every model, cache,
retrieval, evaluator, tool, retry, and human event references it. At the end,
join the route ledger to provider invoices, local utilization, gateway logs,
and review records. Compare a sample of traces to raw invoices and check that
the sum of route allocations does not exceed or mysteriously fall short of
the known account total.

Make allocation rules explicit. Shared GPU capacity can be allocated by
reserved hours, consumed tokens, weighted service time, or a hybrid. A gateway
can be allocated by requests or compute. Human review can use recorded time,
standard task minutes, or a range. The rule is less important than naming it,
using it consistently, and testing how the decision changes under alternatives.
Do not use an allocation rule to make an unmeasured cost disappear.

Separate marginal and fully loaded views. A route can be the cheapest next
request on already-paid capacity while being the most expensive annual choice
because it requires a larger reservation. It can also be valuable to keep a
second route for resilience even when its marginal cost is higher. Report
variable, allocated, and risk-adjusted views together so a manager does not
mistake one for the whole decision.

Outcome quality affects the denominator in a visible way. Define whether a
partial result counts, whether a human-corrected result is accepted with
rework, and how an indeterminate side effect is handled before reconciliation.
If the denominator changes between baseline and routed policy, publish both
coverage and cost per accepted result. A route that accepts fewer requests at
a lower ratio may be reducing service rather than improving economics.

The ledger should support a counterfactual report: same request, same context
and registry snapshot, alternate policy. Counterfactual cost is an estimate,
not an invoice. Mark it as such and give it an uncertainty range. This makes
the business question honest: how much did this policy change relative to the
fixed baseline under the same work?

Make that comparison reproducible with the baseline ladder in Chapter 5.
Freeze request identities or a declared stratified distribution, context and
redaction, tool contract, evaluator revision, acceptance rubric, deadline,
route evidence, and price window. Confidential work does not justify sending
every request to every model: permitted minimized shadow inputs, consented
redacted replay, rubric-based judging, or explicitly uncertain offline
estimates are distinct evidence options. A shift in live request mix needs
new uncertainty and coverage reporting, not credit to the routing policy.

Reconcile at the logical-request level, with accepted, terminal nonaccepted,
and still-pending populations accounted for. Break out rejection, block,
cancellation, and indeterminate effects without treating duplicates or repair
events as additional requests. Accepted-with-rework belongs inside accepted
outcomes; its attempts and correction cost remain visible. An unexplained
missing trace is an unknown, not zero cost. A reviewer should be able to move
from the ratio to one request's attempts and forward to its disposition.

## Allocation decisions need a reader

The cost ledger is not only a finance export. An engineer should be able to
look at one accepted outcome and see its attempts, cache decisions, evaluator,
queue, and rework. A product owner should be able to compare that outcome to
the value or coverage promised. A finance owner should be able to reconcile
the aggregate to known invoices and capacity. Give each view the same run and
outcome keys.

Make unknowns conspicuous. If a subscription has no supported per-request
usage, call the allocation estimate a range or exclude it from the route
comparison while stating the gap. If local power is not metered, use a
documented allocation and sensitivity range. A zero in the ledger should mean
measured zero, not “no one has looked.”

Review cost at the route revision boundary. A new validator, context builder,
cache policy, model pin, or fallback changes the path. Close the old cost
series, record the new revision, and preserve the counterfactual. That makes a
price change distinguishable from a quality or operational change.

For local inference, preserve physical accelerator or CPU time, memory
reservation, energy when available, operator time, and fixed-infrastructure
allocation separately. Low utilization and peak reservations can widen the
cost uncertainty even without a per-token invoice. Instrumentation also costs
work: a bounded workload and sampled traces are a reasonable first study,
provided sample size, missing traces, confidence or sensitivity ranges, and
the protected strata actually observed remain visible.

The release comparison needs more than a cheaper ratio: baseline and candidate
volume and uncertainty, protected acceptance floors, deadline compliance,
p95 latency, repair capacity, unresolved work, cache isolation, residency,
evidence age, and rollback ownership. An exact ledger describes observations;
it does not prove the next workload has the same mix. Require the cost
advantage to survive the declared uncertainty range and more than one time
window, with a current price snapshot and a denominator review date. Hold or
limit release to a named slice when those conditions are unproven.

## Checkpoint

An economic claim is ready when a reviewer can trace the numerator to real
work and the denominator to accepted outcomes. List every allocation and
unknown. Show the fixed baseline and a counterfactual under the same price
snapshot. The reader's artifact is a route cost ledger with effective dates,
reconciliation owner, and sensitivity range. It should make a false token
saving uncomfortable before finance or product has to discover it in a
quarterly report.

## Source slot

Use the dated official pricing pages [OpenAI](https://openai.com/api/pricing/),
[Anthropic](https://platform.claude.com/docs/en/about-claude/pricing/),
[Google](https://ai.google.dev/gemini-api/docs/pricing), [DeepSeek](https://api-docs.deepseek.com/quick_start/pricing),
and [AWS](https://aws.amazon.com/bedrock/pricing/) only for current lookup
facts. Pair them with [FinOps](https://www.finops.org/wg/optimizing-genai-usage/),
[NVIDIA](https://developer.nvidia.com/blog/llm-inference-benchmarking-how-much-does-your-llm-inference-cost/),
and [Thoughtworks](https://www.thoughtworks.com/insights/blog/open-source/zero-cost-fallacy-agentic-era)
for allocation and counter-evidence. The worked ledger is illustrative.
