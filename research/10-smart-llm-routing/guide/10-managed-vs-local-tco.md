# 10. Managed APIs and In-House Open Weights: Compare the Whole Portfolio

## ELI5 hook

You can buy bread from a bakery or bake it in your own kitchen. The bakery
charges per loaf and carries some equipment and staffing. Your kitchen may
make each loaf cheaply at high utilization, but you pay for the oven, power,
ingredients, maintenance, empty capacity, training, and the person who fixes a
broken mixer. The right choice depends on demand, quality, freshness, and who
must be able to inspect the kitchen.

Managed APIs and in-house open-weight serving have the same trade. A provider
invoice is visible and variable. Local serving exposes hardware, power,
capacity, software, support, security, model updates, and quality work. A
route policy should choose a portfolio, not declare one side universally
cheaper.

## Mechanism: five TCO layers

Compare candidates using five layers:

1. **variable inference:** input, output, cached, reasoning, batch, and
   evaluator units under an effective-dated price record;
2. **capacity:** reserved or on-demand infrastructure, GPUs, memory, storage,
   network, utilization, headroom, and idle time;
3. **platform operations:** deployment, observability, security patches,
   registry, incident response, provider integration, and on-call;
4. **quality and product work:** evaluation, data curation, prompt or harness
   maintenance, rework, escalation, and domain review;
5. **risk and optionality:** residency, contractual controls, outage impact,
   portability, switching work, opportunity cost, and the cost of being unable
   to scale at the demand peak.

Measure each route at production-shaped context lengths and concurrency. A
local model with low utilization can have a high accepted-outcome cost. A
managed service with an attractive unit price can become costly through
queueing, retries, or a quality gap. The [NVIDIA inference-cost guide](https://developer.nvidia.com/blog/llm-inference-benchmarking-how-much-does-your-llm-inference-cost/)
provides a vendor-practitioner method for exposing serving drivers. Its
methodology is a starting point, not this enterprise's TCO.

Local serving also requires a capability registry. Record immutable weight and
runtime versions, quantization or serving configuration, supported context,
schemas, tools, regions, capacity state, and measured quality. [vLLM engine
arguments](https://docs.vllm.ai/en/latest/serving/engine_args.html), [vLLM
metrics](https://docs.vllm.ai/en/latest/serving/metrics.html), and [SGLang](https://docs.sglang.ai/)
show why serving configuration and runtime telemetry belong to the route
contract. They do not establish that any particular open weight meets a
business acceptance rubric.

Open model release pages may describe intended capabilities. For example,
[Qwen3-Coder](https://qwenlm.github.io/blog/qwen3-coder/), [Kimi K2](https://moonshotai.github.io/Kimi-K2/),
and [Leanstral 1.5](https://mistral.ai/news/leanstral-1-5/) are primary pages
that can be consulted for their own dated release descriptions. Keep release
claims tied to those pages and test actual route behavior separately. The
unresolved labels Astra, OASIS, DeepSeek Flash, GPT-5.6 Luna, and Fable have
no identity in this packet and must not be inserted into the comparison.

## Worked example: a mixed portfolio

The following annual table is **illustrative** and deliberately uses cost
units rather than currency. A portfolio handles 1.2 million requests. A
managed route has variable inference and provider support; a local route has
reserved hardware and a smaller variable line.

| Cost layer | Managed route | Local open-weight route |
|---|---:|---:|
| variable inference or serving | 420 | 180 |
| reserved/idle capacity | 40 | 260 |
| gateway, registry, and telemetry | 70 | 90 |
| operations and on-call | 35 | 210 |
| evaluation, rework, and review | 110 | 150 |
| residency/portability risk allowance | 25 | 35 |
| total | 700 | 925 |
| accepted outcomes | 1,000,000 | 1,040,000 |
| cost per accepted outcome | 0.70 | 0.89 |

The local route accepts more outcomes in this fictional scenario but costs
more per accepted result. That could still be rational for a restricted data
class, outage independence, or a contractual requirement. Conversely, a
second scenario with sustained high utilization and lower rework could make
local service win. The decision must show the utilization and quality curves,
not a single point estimate.

Use a sensitivity table for utilization, peak headroom, evaluator/rework,
power, staff allocation, and model refresh. Record confidence and the owner of
each assumption. A zero line for platform work is not an optimistic estimate;
it is an omitted cost.

## Failure drill: “open” means zero-cost

An in-house candidate is selected for all restricted requests because its
license line is zero. Its queue saturates at peak, the quality rubric fails on
long documents, and the on-call team spends a week tuning runtime settings.
The gateway retries into the same pool, increasing cost and delaying users.

Add capacity admission to `R1` and `R3`. Test a capable managed route only if
the data-boundary matrix permits it; otherwise fail closed or use a declared
local degradation. Include power, hardware depreciation, support, evaluation,
and rework in the route ledger. The [Thoughtworks zero-cost fallacy article](https://www.thoughtworks.com/insights/blog/open-source/zero-cost-fallacy-agentic-era)
is a counter-evidence reading for this mistake. [FinOps GenAI guidance](https://www.finops.org/wg/optimizing-genai-usage/)
helps frame shared allocation and accountability.

## Reader exercises

1. Build a managed-versus-local TCO sheet with the five layers. Put a range
   around utilization, quality rework, and peak capacity.
2. Define a local route registry record. Include weight pin, runtime image,
   configuration, region, tools, schemas, quota, latency, and acceptance
   evidence.
3. Draw the decision boundary for three data classes: public, restricted
   residency, and high-consequence. Which routes can each class use?
4. Find the break-even utilization at which local accepted-outcome cost would
   fall below managed cost. State which operational assumption dominates it.

## Portfolio decision boundaries

The choice does not have to be “managed everywhere” or “local everywhere.”
Define a boundary by workload and data class. Public, low-consequence,
bursty work may favor a managed route because variable capacity matters.
Restricted work may require a local or contract-qualified region even when its
unit economics are worse. Stable high-volume batch work may favor reserved
local capacity if measured utilization and accepted quality support it.

Add a resilience question: what happens when the preferred route is down? A
second managed provider, a local route, or a deterministic degraded response
may be available for one class and forbidden for another. Record the fallback
set per data class. Do not make a generic “provider independent” claim when a
residency-bound tenant can use only one local pool.

Quality evidence must travel with the route. The official release page for an
open model can document what its publisher says about the model and its date.
It cannot stand in for a coding patch acceptance test, a policy rubric, or a
tool proposal safety test. Evaluate the exact weight, quantization, runtime,
prompt, context builder, and queue shape. A managed endpoint also needs its
actual model pin, region, account, and versioned API behavior in the registry.

Model refresh is an economic event. A new weight may improve acceptance but
require new hardware, re-indexing, evaluator calibration, or a prompt change.
A provider price change may alter the route frontier but not the quality
contract. Treat both as registry revisions with replay and a rollback path.

Finally, include opportunity cost. Engineers maintaining local infrastructure
are not free capacity for application reliability. A managed dependency may
reduce operations work but increase provider concentration or contract risk.
The decision sheet should allow an owner to say “we choose the more expensive
route because this data boundary or outage requirement is mandatory,” then
measure whether the assumption remains true.

## TCO uncertainty and optionality

Do not collapse TCO uncertainty into one invented point. Create low, central,
and high cases for utilization, demand, quality rework, support load, power,
and provider price. Ask which decision changes across the cases. If local is
cheaper only at an unlikely utilization, its optionality may still matter for
residency or outage independence; write that as a separate reason.

Optionality has a cost too. Keeping a second provider or local pool can reduce
outage risk but requires registry, test, and operational work. A provider
switch may require prompt, tool, quality, and contract migration. Include the
cost of maintaining the fallback even when it receives little traffic. An
unexercised fallback is a hypothesis, not resilience evidence.

Review local and managed candidates with the same accepted-outcome rubric.
Otherwise a route can win its TCO comparison by accepting a looser definition
of success. Review quality by context, language, and consequence; then join
the result to capacity and full-cost views.

## Build the decision sheet from observable units

Start with a unit that product and finance can recognize: one accepted
outcome for a defined request class. Then write the cost equation in layers:

```text
accepted-outcome cost =
  provider or inference variable cost
  + evaluator and retrieval work
  + gateway, storage, and observability allocation
  + reservation and support cost
  + expected rework and incident cost
  divided by accepted outcomes
```

This equation does not claim that every term can be measured precisely on day
one. It gives each unknown a place, an owner, and a sensitivity range. For a
managed route, variable input and output tokens may be visible while minimum
commitments, support, egress, cache storage, or evaluator calls sit elsewhere.
For a local route, the model license may be zero while accelerators, power,
cooling, capacity engineering, runtime upgrades, on-call, and idle headroom
are real. [FinOps guidance](https://www.finops.org/wg/optimizing-genai-usage/)
helps frame allocation, and [NVIDIA's inference cost methodology](https://developer.nvidia.com/blog/llm-inference-benchmarking-how-much-does-your-llm-inference-cost/)
helps separate throughput measurements from a complete enterprise TCO.

Use at least three cases. In the low case, demand is modest, quality rework
is high, and local utilization is low. In the central case, use the observed
traffic mix and measured acceptance. In the high case, stress peak demand,
context length, support burden, and provider price exposure. A decision that
changes across those cases is a conditional decision. Write the condition
beside the choice: “local is cheaper after sustained utilization reaches the
measured break-even range and the fallback pool remains funded.” This is more
useful than a single annual number with false precision.

Imagine an illustrative restricted-document workload with 10,000 monthly
requests. A managed route costs 0.04 currency units in visible inference
charges per request. It adds 0.01 for evaluation and retrieval, and a monthly
shared-platform allocation of 1,000 units. If 8,500 results are accepted, the
visible and allocated total is 1,500 units, or about 0.176 per accepted result,
before human rework. The numbers are invented to show the calculation; they
are not a provider quote. A local route may show 0.02 in marginal inference
cost, but if its monthly reservation, power, runtime support, and allocated
engineering total 3,000 units, its 3,200-unit total divided by the same
acceptance count is about 0.376. It loses economically in that traffic band
even though its marginal token cost is lower.

Now vary acceptance. If local quality raises acceptance from 8,500 to 9,600,
its denominator changes and its outcome cost falls to about 0.333. That may
still lose to managed, but it identifies the measurements that could change
the decision. If local quality is better only for a residency-protected slice,
compare that slice separately. The route can be mandatory for a policy reason
while remaining more expensive; that is a valid constraint, not an economic
win. Do not average it with public traffic until the hard boundary and the
business purpose are both preserved.

The decision sheet should include a capacity shadow price. If local capacity
is reserved for a protected class, ask what batch work it displaces. If a
managed commitment has a minimum, ask what utilization is required before the
commitment is rational. If keeping a fallback doubles operational testing,
include that cost even when the fallback receives almost no traffic. A route
that is never exercised may be cheaper in the spreadsheet and weaker during an
outage.

Migration costs also belong in the comparison. Moving from a Copilot-only
workflow or a single Bedrock integration to a controlled portfolio can require
adapter work, prompt and tool regression tests, data-boundary review, user
training, and a period of dual running. Moving to local weights can add model
acquisition, quantization validation, runtime deployment, capacity testing,
and incident ownership. Amortize those costs over a stated horizon, then show
the unamortized first-year view beside the steady-state view. A route that wins
only after an unrealistic horizon should not be presented as an immediate
saving.

Finally, record confidence next to every term. “Provider tokens” can be
invoice-reconciled. “Human rework” may be sampled. “Incident risk” may be a
range supported by history and failure drills. “Engineering opportunity cost”
may remain qualitative. A qualitative term should not be silently assigned a
zero. The decision remains useful when it shows which unknowns need a pilot
and which constraints make the economic comparison irrelevant.

## Checkpoint

The portfolio choice is ready when the team can show low, central, and high
TCO cases, quality by protected stratum, peak capacity, fallback eligibility,
and the operational owner. A license price or a provider invoice is one line
of that sheet. The reader's artifact is a managed-versus-local decision with
an explicit reason for every mandatory constraint and a review date for every
volatile assumption.

## Source slot

Primary serving references are [vLLM metrics](https://docs.vllm.ai/en/latest/serving/metrics.html),
[vLLM engine arguments](https://docs.vllm.ai/en/latest/serving/engine_args.html),
and [SGLang](https://docs.sglang.ai/). Pair [NVIDIA's cost methodology](https://developer.nvidia.com/blog/llm-inference-benchmarking-how-much-does-your-llm-inference-cost/)
with [FinOps](https://www.finops.org/wg/optimizing-genai-usage/) and
[Thoughtworks](https://www.thoughtworks.com/insights/blog/open-source/zero-cost-fallacy-agentic-era)
for counter-evidence. Provider/model release pages are linked only for their
own dated claims. The table is illustrative.
