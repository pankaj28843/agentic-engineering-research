# 17. Cost attribution: from tokens to accepted work

Cost attribution answers three different questions:

1. **Accounting:** who consumed the spend?
2. **Engineering:** which path created it?
3. **Product:** what useful outcome did it buy?

Token totals help with the first two. They do not answer the third. A production
team should optimize cost per accepted business action under quality,
reliability, latency, and safety constraints.

## ELI5: price the grocery delivery, not one bag

A grocery order uses bags, a picker, a van, fuel, payment processing, and
sometimes a redelivery. Making bags cheaper does not improve the business if
damaged orders double.

Likewise, an AI workflow may use retrieval, several model calls, tools,
retries, fallbacks, evaluation, and human review. Its meaningful unit is often
“resolved case” or “merged change,” not “one thousand tokens.”

## Build a cost event before building a dashboard

Every billable or allocated operation should emit a cost event joined to the
end-to-end trace. A useful event includes:

- timestamp, provider, account, region, and resolved SKU or model;
- application, environment, team, tenant, and use case;
- trace, workflow-run, model-call, and release IDs;
- input, output, cached-input, reasoning, embedding, and reranking units where
  the service exposes them;
- tool, search, storage, network, and evaluation usage;
- retry, route, and fallback reason;
- requested and actual batch or reservation context;
- provider price version and currency;
- estimated cost immediately, then reconciled billed cost later.

Do not rely on mutable display names. Preserve the raw provider usage record
and the normalization rule that produced the internal cost.

[FinOps Foundation, “FinOps for AI: Tools & Services
Considerations”](https://www.finops.org/wg/finops-for-ai-tools-services-considerations/)
recommends connecting all calls in multi-call workflows and tagging dimensions
such as application, team, use case, model, token class, errors, and retries.
This is industry working-group guidance, not a controlled savings study.

## Four ledgers, one reconciliation

AI costs arrive at different times and granularities. Maintain:

### Usage ledger

The operational estimate from provider responses, gateways, and self-hosted
telemetry. It is fast enough for budgets and debugging but may omit discounts,
rounding, failed-request policy, or later adjustments.

### Price catalogue

A versioned effective-dated table for input, output, cached input, batch,
storage, tool, and other prices. Never recalculate old runs with today's price
unless the report explicitly models a counterfactual.

### Billing ledger

Invoices and provider cost exports are the financial authority. Reconcile
operational estimates to them and retain the unexplained difference.

### Allocation ledger

Shared gateway, GPU, observability, vector store, and platform costs need an
allocation rule. Label direct, shared, idle, and unallocated spend separately.
An allocation rule is a policy decision, not a measurement fact.

If a provider invoice says €100, the usage estimate says €92, and the dashboard
silently reports €92, the system is precise-looking rather than accountable.

## Choose a denominator that represents value

The
[FinOps Foundation, “Unit
Economics”](https://www.finops.org/framework/capabilities/unit-economics/)
distinguishes resource units from business units. Use a ladder:

- cost per input/output/cached token;
- cost per model call;
- cost per workflow attempt;
- cost per completed workflow;
- cost per **accepted** or correctly completed workflow;
- cost per downstream outcome, such as a resolved case without recontact.

The later units are harder to join but harder to game.

For one cohort:

```text
total workflow cost
────────────────────────────────────────────
accepted outcomes that pass the quality gate
```

Include human review, escalation, and remediation when material. A smaller
model can have a lower call cost and a higher accepted-outcome cost if it
creates more retries or support work.

Definitions must be versioned. If “resolved case” changes midway through a
trend, annotate the break rather than drawing a smooth line.

## A workflow has a distribution, not one price

Agentic paths fan out:

```text
expected run cost
  = base path
  + Σ P(route i) × cost(route i)
  + expected retries
  + expected tool and evaluation costs
```

That expectation is useful for planning but insufficient for protection.
Also model:

- p50, p95, p99, and maximum run cost;
- input-length and output-length buckets;
- calls and retries per run;
- expensive-route probability;
- loop-depth and tool fan-out;
- tenant and use-case slices;
- incomplete and abandoned runs.

The native Hacker News thread
[“Ask HN: How are people forecasting AI API costs for agent
workflows?”](https://news.ycombinator.com/item?id=47332177)
contains practitioner preferences for workflow budgets, path composition, and
explicit cap outcomes. It is recent, self-selected anecdotal evidence with
some vendor promotion; use it as a hypothesis list, not a benchmark.

## Forecast with scenarios, then learn from traces

For a new workflow:

1. enumerate routes and termination states;
2. estimate traffic by cohort and time period;
3. use measured token distributions from a representative sample;
4. attach current effective prices;
5. model normal, growth, incident, and abuse scenarios;
6. include evaluation, storage, tools, platform, and human work;
7. run sensitivity analysis on the uncertain variables;
8. replace assumptions with production trace distributions;
9. reconcile estimates to invoices.

Do not present a single forecast without its assumptions. Output length,
context length, cache hit rate, retry rate, and model route frequently dominate
more than traffic count alone.

For self-hosting, replace “tokens × API price” with capacity economics:

- accelerators and reservations;
- idle and fragmentation cost;
- power and network;
- serving, scaling, and on-call labour;
- model-loading and storage;
- failed capacity and disaster recovery;
- utilization at the latency SLO;
- accepted tokens or outcomes per provisioned hour.

Full GPU utilization is not automatically good economics if queues violate the
product SLO.

## Budgets are runtime controls, not monthly surprises

Enforce budgets at several scopes:

- per model call: maximum input and output;
- per run: calls, tokens, elapsed time, tool attempts, and spend;
- per user or tenant: rate and rolling spend;
- per feature: daily and monthly allocation;
- system-wide: provider and capacity guardrails.

Approaching a cap should trigger a designed state:

- summarize progress and ask permission to continue;
- switch to a bounded cheaper route if its quality envelope permits;
- return partial evidence with explicit limitations;
- queue work for a batch path;
- escalate to a human;
- terminate without committing side effects.

A raw provider error is not an acceptable budget policy. Connect these controls
to [Chapter 11](11-agent-budgets-and-termination.md).

## Optimize the causal driver, not the invoice line

[FinOps Foundation, “Optimizing GenAI
Usage”](https://www.finops.org/wg/optimizing-genai-usage/)
frames optimization across cost, technical performance, and business impact.
Candidate interventions include:

- remove irrelevant context;
- improve retrieval so fewer documents travel into generation;
- cap pathological output and loops;
- route eligible tasks to a smaller model;
- batch delay-tolerant work;
- cache only when identity, version, and safety rules permit;
- improve tool reliability to avoid repeated model calls;
- use accepted-output evaluation to prevent false savings;
- adjust self-hosted capacity and scheduling.

Published percentage-saving ranges in guidance are leads, not promises. Each
intervention changes behaviour as well as spend. Evaluate it on the actual
workload with paired quality, latency, and reliability measurements.

## Detect the expensive failure that still returns 200

Useful FinOps alerts include:

- calls per successful run rise after a prompt change;
- cached-token share drops after a template-version change;
- one tenant's p99 spend spikes without traffic growth;
- fallback traffic shifts to a more expensive provider;
- output tokens grow while accepted quality is flat;
- reconciliation variance exceeds tolerance;
- budget terminations or abandoned paid work increase;
- evaluator spend grows faster than evaluated production volume.

Join the alert to exemplars. “Tokens rose 20%” is less actionable than “tool
timeouts caused two repair calls on the checkout workflow after release
`tool-17`.”

## Worked example: the cheaper router loses

A support product changes from one strong model to a router:

- routine cases go to a small model;
- uncertain cases go to the strong model;
- failed answers receive one repair attempt.

Call-level spend falls 30%. Yet trace-level analysis finds:

- more routine cases are incorrectly marked complete;
- agents reopen them, increasing human handling time;
- repair calls concentrate on multilingual cases;
- accepted first-contact resolutions fall;
- total cost per accepted resolution rises.

The team recalibrates the router on the multilingual slice, makes uncertainty
an escalation signal, and measures paired accepted-resolution cost. It does
not declare routing bad or good in the abstract.

## Field exercise: make a unit-economics worksheet

Take one AI feature and write:

- the accepted outcome and its rejection conditions;
- every direct and allocated cost component;
- the join key from usage to outcome;
- normal and tail path composition;
- quality, safety, latency, and reliability gates;
- run and tenant budgets;
- reconciliation source and owner.

Now change one assumption at a time. Which variable most changes p95 run cost?
Which “saving” merely shifts work to a person?

## Interview checkpoint

**Question:** “How would you attribute and optimize LLM cost?”

A strong answer describes trace-linked usage events, effective-dated prices,
invoice reconciliation, tenant/team/use-case allocation, workflow cost
distributions, cost per accepted business outcome, runtime budgets, and
quality/latency/safety gates. It explains that API price, self-hosted capacity,
and human rework are different forms of the same unit-economics problem.

**Explain it back:** How can a change reduce token cost by 40% and make the
product more expensive?

## Capstone increment

Make the worksheet the assistant's cost model. Define one cost event joined to
Chapter 16's trace ID, one Chapter 11 run/tenant budget, and the Chapter 15
accepted-task gate. Include normal and tail routes, provider or allocated
capacity, retrieval/tools/evals, retries, and human review.

Add a terminal accounting matrix:

| Joined state | Usage and billing | Allocation and remediation | Outcome |
| --- | --- | --- | --- |
| attempt/run succeeded; effect committed | reconcile metered and invoiced usage | charge the tenant/feature plus shared allocation | accepted or rejected by the product gate |
| client disconnected or cancellation in progress | retain work and partial provider charges after disconnect | allocate cleanup and reconciliation | not yet terminal |
| run cancelled; effect not committed | retain consumed retrieval/model/tool/eval work | allocate wasted work and any human handling | rejected, never silently discarded |
| retry or fallback | retain every attempt and partial charge | attribute amplification to the causal route/error | only the final qualified result may be accepted |
| side effect `unknown` | retain usage and provisional billing | expose reconciliation and human-remediation cost | pending until the effect ledger resolves |

**Definition of done:** in deterministic portfolio core, every cost row and the
exact maximum per attempt and accepted task reconcile across attempt, run,
task, side-effect, usage, billing, allocation, remediation, and
accepted-outcome ledgers. Do not label a percentile over the fixture's tiny
population. In live stretch, publish p50/p95/p99 only with the sampled
population, window, quantile rule, and uncertainty. A cheaper rejected result,
partial charge, post-disconnect call, retry, fallback, unknown commit, or human
repair cannot disappear from unit economics.

## Part III checkpoint

- **Explain from memory:** retrieval recall, answer acceptance, API success,
  and business acceptance have different denominators.
- **Update the capstone:** follow one evaluation record through its trace and
  cost event to an accepted or rejected outcome.
- **Keep unresolved:** can untrusted language or shared state cross an
  authority boundary? Part IV tests trust and tenant isolation.

Next: [Safety](18-safety.md) treats every instruction and tool result as data
crossing a trust boundary.
