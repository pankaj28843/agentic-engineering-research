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
not a token-cost win. If an owner reports only the 30% model line, the
dashboard is hiding the intervention's consequence.

Sensitivity analysis identifies the important unknowns. Vary escalation rate,
human hours, cache hit rate, evaluator calls, and local utilization one at a
time and together. Record a range when the input is uncertain. Show a break-
even line: for example, what maximum human rework keeps the routed policy
below the baseline? That question is actionable for product and operations.

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
