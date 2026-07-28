# 21. Full-stack trade-offs: latency, quality, cost, reliability

An AI system is not “fast” or “cheap” in isolation. It serves a workload at a
quality and reliability level within a latency and cost envelope.

Optimizing one number at unconstrained load produces attractive but unusable
benchmarks. The engineering object is a Pareto frontier: configurations for
which no goal can improve without another getting worse.

## ELI5: run a restaurant, not a blender benchmark

A blender may process soup quickly. A restaurant still has seating, queues,
orders, allergens, cooks, delivery, mistakes, and refunds.

“Tokens per second” measures one appliance. The product question is whether a
customer receives the correct safe meal on time, at sustainable cost, even
during the dinner rush.

## Define the product envelope first

Write the service-level objectives and hard gates by journey:

- acceptable answer/task success by consequence and slice;
- time to first useful feedback;
- streaming cadence or time to complete;
- p50, p95, and p99 latency;
- availability and accepted-task success;
- safety, privacy, and authorization invariants;
- cost per attempt and accepted outcome;
- recovery and fallback behaviour;
- expected traffic and burst.

Interactive chat, autocomplete, background document extraction, and autonomous
research should not share one benchmark target. They value delay and
throughput differently.

## Decompose end-to-end latency

A request may spend time in:

```text
client + edge + authentication
+ application queue
+ prompt/context assembly
+ retrieval/reranking
+ model-server queue
+ model load/adapter switch
+ prefill
+ decode/stream
+ tool calls and repair loops
+ validation/persistence
+ delivery
```

Track both the sum and each component. An optimization to decode cannot fix a
retrieval timeout.

For model inference:

- **queue delay** grows with contention and scheduling;
- **prefill** processes the input and strongly affects time to first token;
- **decode** emits later tokens and affects inter-token latency;
- **network/stream assembly** changes what the user observes.

[NVIDIA Developer, “LLM Inference Benchmarking: Fundamental
Concepts”](https://developer.nvidia.com/blog/llm-benchmarking-fundamental-concepts/)
distinguishes load testing from model/server benchmarking, decomposes queue,
prefill, and generation, and separates system throughput from per-user token
rate. It is vendor guidance promoting NVIDIA tooling, so use its definitions
with an explicit formula and independent workload measurements.

## Define metrics so two teams compute the same thing

At minimum, publish:

- **TTFT:** timestamp of first received output minus accepted-request time;
- **end-to-end latency:** terminal usable result minus accepted-request time;
- **ITL:** how inter-token intervals are aggregated, including or excluding
  first token;
- **per-user generation rate:** output tokens over the specified decode window;
- **system throughput:** completed requests, input tokens, output tokens, or
  accepted outcomes per wall-clock second;
- **goodput:** throughput that also satisfies quality and latency SLOs;
- **cost:** included infrastructure, provider, tool, and human components;
- **error/abstention:** what counts as incorrect, incomplete, or safely
  escalated.

Name tokenizer, benchmark tool, warmup, measurement boundary, and whether
failed or cancelled requests enter denominators. Similar labels can hide
different arithmetic.

## Use a production-shaped workload

Sample or synthesize from measured distributions:

- input and output length, including tails;
- conversation turns and prefix overlap;
- retrieval and tool-call frequency;
- structured-output complexity;
- temperature and decoding parameters;
- model/adapter mix;
- tenant and priority mix;
- arrival pattern, burst, concurrency, and cancellation;
- cache warmth and hit eligibility;
- error, retry, fallback, and budget paths.

Keep a replayable workload manifest and a protected holdout. Remove sensitive
content while preserving performance-relevant shapes.

One short prompt at fixed concurrency is a microbenchmark. It cannot size an
agent product.

## Sweep concurrency and find the knee

At low concurrency, each request can be fast while expensive capacity sits
idle. Batching and continuous scheduling increase utilization and throughput.
Near saturation, queues grow non-linearly and tail latency rises.

Measure a curve:

1. warm the deployment under a declared cache state;
2. sweep arrival rate or concurrency;
3. record p50/p95/p99 TTFT, ITL, completion latency, errors, and throughput;
4. repeat for representative length and route slices;
5. identify the highest goodput point inside every hard gate;
6. test burst, failover, and degraded capacity;
7. reserve headroom appropriate to recovery time.

[NVIDIA Developer, “LLM Inference Benchmarking: How Much Does Your LLM
Inference Cost?”](https://developer.nvidia.com/blog/llm-inference-benchmarking-how-much-does-your-llm-inference-cost/)
recommends deriving a latency-throughput curve for a deployment unit and
choosing the highest-throughput point that remains inside the SLO. Its example
purchase and depreciation values are illustrative and NVIDIA has a direct
sales incentive; the method is more durable than its sample economics.

## Separate interactive and batch pools when goals conflict

Interactive work benefits from:

- low queue delay;
- predictable TTFT and ITL;
- headroom for bursts;
- bounded output and fast cancellation.

Asynchronous work can accept:

- larger batches;
- longer queue windows;
- throughput-oriented scheduling;
- spot or deferred capacity;
- progress checkpoints rather than token streaming.

[DigitalOcean, “The LLM Inference Trilemma: Throughput, Latency,
Cost”](https://www.digitalocean.com/blog/llm-inference-tradeoffs)
describes saturation, continuous batching, chunked prefill, and separately
tuned interactive/batch pools. DigitalOcean is a cloud vendor; its hardware,
FP8, energy, and hypothetical curve claims require workload-specific
verification.

One shared pool can work with isolation and priorities, but validate that large
prefills do not starve latency-sensitive decode and that batch tenants cannot
consume all cache or queue capacity.

## Quality belongs on every performance chart

A configuration is not faster if it silently does less useful work.
Performance changes can alter quality through:

- smaller routed models;
- quantization;
- truncated prompts or outputs;
- fewer retrieved passages;
- approximate or stale caches;
- speculative-decoding acceptance behaviour;
- timeout and fallback policy;
- batching or concurrency bugs;
- skipped evaluator or repair stages.

For each point on the curve, run a paired quality gate on relevant slices.
Report goodput or cost per accepted outcome, not raw tokens alone.

Do not average a severe authorization failure into a small style improvement.
Some qualities are hard constraints.

## Price mistakes, waiting, and abstention explicitly

[Michael J. Zellinger and Matt Thomson, “Economic Evaluation of
LLMs”](https://arxiv.org/html/2507.03834v1)
turns API cost, latency, errors, and abstention into use-case-specific reward.
The study evaluates six models on 1,500 MATH training questions, with a
train/test split for cascades and June 2025 prices. In that configuration,
reasoning models become preferable above a low assigned error cost and a single
larger model can beat cascades under some assumptions.

The numeric thresholds depend on math questions, possible dataset
contamination, a related model judge, provider endpoints, and user-assigned
dollar values. The durable technique is to make consequence explicit:

```text
net value
  = task value
  − inference/tool/platform cost
  − cost of delay
  − expected cost of error
  − expected escalation/remediation cost
```

Use ranges and sensitivity analysis when error cost is uncertain. A medical
triage error and a draft-email style defect do not share a price.

## Reliability changes capacity economics

Benchmark:

- cold starts and model loading;
- provider throttling and quota exhaustion;
- zone or provider loss;
- autoscaling delay;
- tool and retrieval dependency failure;
- retry amplification;
- cancellation and cleanup;
- cache loss;
- rollout and rollback;
- noisy-neighbour traffic.

A cluster that meets normal p99 at 95% utilization may have no failover
capacity. A redundant provider may improve availability but change tool
support, safety behaviour, structured-output success, locality, and price.

Measure the degraded product state, not only infrastructure recovery time:
which journeys continue, with what disclosure, and which must stop?

## Compare managed APIs and self-hosting honestly

For an API include:

- input/output/cached/reasoning/tool prices;
- rate limits and quota;
- retry and fallback spend;
- data and residency constraints;
- operational variability and version control.

For self-hosting include:

- accelerators, reservations, network, storage, and power;
- idle, fragmentation, and failover capacity;
- serving-engine and driver engineering;
- on-call and security work;
- model/adapter loading;
- useful throughput at the actual SLO;
- upgrade, rollback, and incident cost.

Avoid “GPU hourly cost divided by maximum tokens.” Size at the qualified
goodput point and include persistent shared capacity.

## A reproducible benchmark protocol

Publish:

1. decision and product SLO;
2. hardware, provider, region, software, model, tokenizer, and artifact hashes;
3. workload distributions and generation settings;
4. cache warm/cold policy;
5. arrival process, concurrency range, duration, and warmup;
6. exact metric formulas and timestamp boundaries;
7. retries, errors, cancellations, and timeouts;
8. quality/evaluation set and gates;
9. price version and allocated-cost method;
10. repeats, uncertainty, raw result location, and known limitations.

Randomize order where thermal, cache, or provider-time effects matter. Compare
paired workloads. Plot the complete latency-throughput-cost-quality frontier,
not one chosen point.

Attach a claim boundary to the card: sampled population and time window,
excluded cohorts, tenant and temporal slices, all resolved versions, hardware
or provider region, uncertainty, known missing dimensions such as cancellation
or cost, and explicit drift/invalidation triggers. A “winner” means best only
for that measured workload and configuration; it is not a portable engine,
provider, or model ranking.

### A useful comparison can still be incomplete

Mohammad Siavashi and colleagues, [“Blink: CPU-Free LLM Inference by
Delegating the Serving Stack to GPU and
SmartNIC”](https://arxiv.org/html/2604.07609v1), provide an unusually concrete
2026 comparison: one H100 server, four named models, ShareGPT traces, a
1–32-request/second sweep, versioned TensorRT-LLM, vLLM, and SGLang baselines,
and p99 TTFT/TPOT plus goodput under isolated and CPU-interference conditions.
That makes the paper useful for learning what a benchmark card should expose.

It does **not** establish a universal engine ranking. Blink is the authors'
proposed system; its frontend also uses a BlueField-3 DPU, several baseline
features are disabled because Blink does not implement them, cancellation and
cost are not evaluated, and the paper says code will be released upon
publication. Its rendered conference metadata still contains placeholder
text. Treat its ratios as preprint- and setup-specific evidence, and its
disclosures as a checklist for reproducing the comparison on your own
workload.

## Worked example: document-review product

The product has two journeys:

- a user uploads a document and expects first findings within five seconds;
- a nightly compliance sweep can finish within two hours.

The team:

1. measures real input-length and finding-count distributions;
2. isolates interactive and batch pools;
3. sweeps concurrency for each;
4. records retrieval, prefill, decode, tool, and validation time;
5. gates every configuration on missed-risk and citation slices;
6. chooses interactive capacity below the p99 knee with failover headroom;
7. heavily batches the nightly path;
8. reports cost per accepted review, including human escalation.

The highest token-throughput configuration loses interactive traffic and wins
batch traffic. There is no single “best server.”

## Field exercise: design a benchmark card

Choose one AI journey and write its:

- quality and safety gates;
- latency percentiles and boundary;
- workload distribution;
- concurrency sweep;
- failure/degraded scenarios;
- cost numerator and accepted-outcome denominator;
- versions and reproducibility artifacts.

Then identify one optimization that moves each axis in an unwanted direction.

## Interview checkpoint

**Question:** “How do you benchmark and optimize an LLM system?”

A strong answer starts from product SLOs and a production-shaped workload,
decomposes end-to-end queue/prefill/decode/tool latency, defines metric
formulas, sweeps concurrency to the goodput knee, gates configurations on
quality and safety, includes reliability headroom, and calculates cost per
accepted outcome. It reports a Pareto frontier rather than a single throughput
number.

**Explain it back:** Why can doubling maximum tokens per second reduce the
number of useful requests served within the product SLO?

## Capstone increment

Make the worked document-review product the capstone benchmark. The card must
import Chapter 5 phase budgets, Chapter 6 arrival/scheduler workload, Chapter
15 hard quality gates, Chapter 17 accepted-task denominator, Chapter 19 tenant
slices, and the Chapter 20 candidate. Sweep concurrency and failure states.

For deterministic portfolio core, publish all eleven request rows, exact
maxima, and the isolated-baseline slowdown; the population is too small to
support a useful p95. For live stretch, use at least 20 samples per reported
slice and the fixture's nearest-rank rule, and label those distributions as
live evidence rather than replacing the deterministic ledger.

**Definition of done:** publish a reproducible table or plot of the feasible
Pareto frontier. Any configuration outside a hard gate is excluded rather than
rewarded for throughput, and interactive and batch winners may differ. State
the sampled population/window, exclusions, resolved stack and region,
uncertainty, tenant/temporal slices, missing cancellation or cost dimensions,
and drift triggers; every winner is explicitly bounded to that card.

Next: [Production failure modes](22-production-failure-modes.md) turns the
whole stack into a continuous reliability-learning loop.
