# 8. Latency Has a Price: Queueing, Tails, and SLO-Constrained Routing

## ELI5 hook

A supermarket can have a cheap checkout that is excellent at noon and awful
when everyone arrives after work. A more expensive checkout with spare staff
may be the cheaper choice for a customer who will miss a train in ten minutes.
The store measures waiting time, service time, and the long tail of people
stuck in line. Average checkout time alone hides the experience.

LLM routes have the same queue shape. A model that is inexpensive at low
concurrency can become an expensive route when it saturates, triggers a
fallback, or makes a user abandon and retry. Route economics must contain a
latency budget and capacity state.

## Mechanism: decompose the tail

For each route, distinguish:

```text
queue delay + time to first useful response
  + generation/stream completion + validation/tool time
  + retry or escalation delay = user-visible path latency
```

Track p50, p95, and p99 rather than only the mean. Interactive work often
cares about time to first useful response and completion tail; batch work may
care about total job completion and cost per accepted item. A route policy can
send delay-tolerant work to a batch window while preserving interactive
capacity. It can also reserve headroom for high-consequence requests.

Queueing is nonlinear near saturation. Arrival rate, service time,
concurrency, batch shape, context length, and warm/cold state all matter. The
router should read a versioned capacity signal and reserve capacity before
dispatch. It must not treat a stale healthy heartbeat as available headroom.

Serving documentation makes the measurement surface concrete. [vLLM metrics](https://docs.vllm.ai/en/latest/serving/metrics.html)
documents runtime signals useful for local serving, and [vLLM engine arguments](https://docs.vllm.ai/en/latest/serving/engine_args.html)
shows why capacity is shaped by explicit runtime configuration. [SGLang documentation](https://docs.sglang.ai/)
provides a second serving-stack reference. These pages document systems; they
do not predict the enterprise's latency distribution. [NVIDIA's inference
benchmarking guidance](https://developer.nvidia.com/blog/llm-inference-benchmarking-how-much-does-your-llm-inference-cost/)
is useful for separating throughput and cost measurements.

Define SLOs per route class. A proposed interactive contract might include a
p95 first-useful-response target, a p95 completion target, a maximum queue
budget, and a fallback deadline. A proposed batch contract might include a
completion window, accepted-goodput floor, and maximum cost per accepted item.
Numbers require workload calibration. The same target should not be copied
from a benchmark with different context and concurrency.

## Worked example: support now, extraction overnight

The following is an **illustrative policy** for a generic enterprise. It has
an interactive support queue and a nightly document-extraction pool.

| Route class | Capacity policy | Queue budget | Acceptance and cost view |
|---|---|---|---|
| Interactive support | reserved managed or local capacity; one bounded fallback | p95 queue under 0.8 time units | first useful response and accepted answer; human escalation counts |
| Long policy lookup | capable route with residency-qualified capacity | p95 queue under 1.5 units | evidence and exception rubric; no cross-boundary fallback |
| Nightly extraction | batch pool with fixed concurrency and retry budget | completion by 06:00 | accepted fields per cost unit; human review included |

Suppose 80 interactive requests arrive in a burst. An efficient pool has
capacity for 40 concurrent requests and a nominal service time of one unit.
The first 40 complete quickly; the rest queue, and 12 time out. Those 12
fall back to a capable pool with service time three units. The efficient route
was cheaper per call, but its queue caused 12 additional capable calls and a
poor p95. A router that reserved 20 units of headroom or admitted work to the
capable pool could have a higher first-call price and lower accepted-path cost.

For the nightly pool, the same capacity can batch 200 documents during the
window. A small increase in completion time may reduce cost per accepted item,
provided the acceptance and completion-window contracts hold. The policy must
not use batch economics for an interactive request merely because its token
price is attractive.

## Failure drill: capacity looks like model quality

The efficient route's answer quality falls during a traffic peak. The model
weights did not change; queue time caused context truncation and client
timeouts, then retries duplicated work. The evaluation dashboard attributes
the regression to the model and lowers the route's quality score. The router
switches away permanently, leaving the capable pool overloaded too.

Separate model outcome from service state. Join queue depth, admission,
context construction, TTFT, completion, timeout, retry, and validator results
to the same route attempt. Inject a controlled load test and compare quality
at fixed service conditions. Add circuit breakers and a capacity reservation
for fallback. When a route is saturated, report `capacity-exhausted` or
`budget-exhausted` rather than pretending a second model call is free.

An availability fallback must still satisfy the route envelope. Residency,
tenant, schema, and authority constraints do not disappear under pressure. If
no eligible capacity exists, a transparent degraded response or blocked state
is safer than a cross-boundary guess.

## Reader exercises

1. Draw the latency path for one request and label queue, first token, decode,
   validation, tool, and retry time. Choose the tail metric that would change
   your route decision.
2. Build separate SLOs for interactive and batch traffic. Mark which numbers
   are proposed and what replay would calibrate them.
3. Design a capacity reservation for a primary and one fallback. Include
   admission failure, queue age, and budget consumption.
4. Create a failure injection where the model stays constant but queueing
   causes a quality or acceptance regression. List the telemetry that proves
   the cause.

## Capacity admission is an economic decision

The route scorer should not ask only “which endpoint has the lowest listed
price?” It should ask whether the endpoint can accept this request inside its
queue, latency, and fallback budget. Admission can be a simple deterministic
rule: reserve expected tokens and service time, keep protected headroom, and
reject a candidate when its queue age or capacity signal is too high. A more
complex predictor is useful only if it improves a measured decision over that
rule.

Record the difference between **service time** and **waiting time**. A local
runtime may produce tokens quickly once a request starts but wait behind a
long-context batch. A managed endpoint may have a higher unit price but spare
capacity. The user experiences their sum. The cost ledger sees the resulting
timeouts, retries, abandoned sessions, and human escalations. Route-level
economics must therefore join queue events to accepted outcomes.

Protect capacity by class. Interactive requests may reserve headroom that
batch work cannot consume. High-consequence proposals may have a smaller,
more reliable pool. Delay-tolerant extraction can use a window and a declared
completion state. This is a policy trade, so expose its opportunity cost: a
reserved lane may be idle during quiet periods, while a shared lane may breach
the tail during bursts.

Use load tests that resemble the request distribution. Sweep context length,
output length, concurrency, cache hit rate, and arrival burst. Report goodput
as accepted outcomes per unit time, not just generated tokens per second. If a
route produces more tokens but more rejected or repaired work, its goodput is
lower. Run failure injections with a saturated primary, unavailable fallback,
and delayed validator to verify the terminal state and budget behavior.

Capacity data has a freshness contract. A heartbeat can say a worker is alive,
not that it can accept a restricted request before its deadline. Include the
capacity snapshot in the route decision and expire it. If the signal is stale,
use the declared safe default or block. This keeps queue uncertainty from
becoming an unlogged provider hop.

## Read the route curve, not one latency point

Plot cost per accepted outcome against p95 latency while sweeping concurrency
and context shape. The curve may have a broad efficient region and then a
sharp tail as capacity saturates. A route that wins at concurrency 10 may lose
at concurrency 100. Mark the operating point, the protected headroom, and the
fallback trigger. The decision is a region of safe operation, not a benchmark
headline.

Measure first useful response separately from complete accepted response. A
stream can feel fast while validation or tool reconciliation takes longer. If
the product can safely show partial progress, define its contract. If not,
do not count the first token as success. Batch work needs its own completion
and expiration states.

Capacity reservation has an opportunity cost. Holding headroom for a rare
high-consequence route may reduce average utilization, but releasing it to
batch work can make the protected route unavailable at the worst time. Put
that choice in the SLO and cost decision, then revisit it with real arrival
data.

## Admission is a state transition

Treat capacity admission as part of the request state machine. A candidate
route starts as `eligible`, becomes `reserved` only after the worker or
provider quota acknowledges a bounded reservation, and becomes `dispatched`
only when the request is accepted. A timeout before acknowledgement is not a
successful attempt. It is an admission failure that may be retried on a
different eligible route, returned as a degraded state, or held for a batch
window. The ledger must distinguish those outcomes so a provider error does
not look like a model failure.

A reservation should have a lease, an estimated resource shape, and an owner.
The resource shape can include input tokens, output-token allowance, expected
tool calls, GPU seconds, or a provider concurrency slot. The lease prevents a
crashed router from holding capacity forever. Releasing a reservation after a
cancelled client is as important as acquiring it. If the downstream system
cannot confirm release, mark the capacity uncertain and use the conservative
budget until reconciliation completes. This avoids optimistic dispatch based
on capacity that may still be occupied.

The router also needs a fairness rule. A large long-context request can consume
the whole pool and starve many small requests; a stream of cheap requests can
starve a protected class. Choose a policy such as weighted queues, per-tenant
quotas, or class reservations. Record the choice as policy data. Fairness is
not achieved by hiding queue age in a single aggregate latency number. Report
the tail by tenant, class, context shape, and route revision while protecting
identifying content through the approved telemetry redaction policy.

Admission decisions should be explainable without exposing prompts. A compact
decision record can say `route=local-coder-2`, `capacity_snapshot=184`,
`reservation=32k-input/4k-output`, `queue_budget=0.8`, `fallback_set=[managed-coder-1]`,
and `reason=protected-class-headroom`. The record needs policy and registry
revision IDs, not raw sensitive text. A reviewer can then reproduce why a
request waited or fell back and compare that reason with the observed queue
and accepted outcome.

Cancellation deserves a separate test. A client may close a stream after the
first token, while the provider continues generating or a tool call continues
executing. The route must define whether generation is cancelled, whether a
tool side effect is allowed to finish, and how the remaining reservation is
released. For readonly work, the safe behavior may be to stop and record an
incomplete result. For an external action, the system must use the action's
idempotency and reconciliation contract rather than assuming that a cancelled
HTTP request cancelled the effect.

Use a small capacity experiment before trusting a predictor. Hold the prompt,
model pin, context builder, and validator constant. Sweep one variable at a
time through realistic context lengths, concurrency, burstiness, and output
limits. Compare a deterministic admission rule with the predictor on accepted
goodput, p95 and p99, false admissions, false rejections, fallback rate, and
cost per accepted outcome. Keep the predictor only if it wins on the protected
strata and fails safely when its signal is stale. A slightly less efficient
rule with bounded failure is preferable to a clever rule that silently sends
traffic outside its envelope.

The resulting capacity contract should answer five operational questions:
what is reserved, who owns the reservation, when it expires, what happens on
cancellation, and what terminal state is returned when no route can admit the
request. Those answers connect SLOs to the graph's budget and security
contracts. They also make capacity a reviewable control rather than an
implicit hope that the endpoint will be healthy.

## Checkpoint

The route is ready for a latency decision when the team can show its operating
curve across context, concurrency, arrival bursts, and cache state. Pick an
operating region with headroom, not the lowest isolated benchmark point. The
reader's artifact is an SLO curve that joins p95/p99, accepted goodput,
capacity reservation, and cost per accepted outcome. It also names the
fallback and the state returned when no eligible capacity remains.

## Source slot

The primary serving slots are [vLLM metrics](https://docs.vllm.ai/en/latest/serving/metrics.html),
[vLLM engine arguments](https://docs.vllm.ai/en/latest/serving/engine_args.html),
and [SGLang](https://docs.sglang.ai/). Pair them with [NVIDIA inference
cost](https://developer.nvidia.com/blog/llm-inference-benchmarking-how-much-does-your-llm-inference-cost/)
and the serving/routing research records S58–S62 in [sources.json](../sources.json).
The SLO targets and workload table are illustrative proposals.
