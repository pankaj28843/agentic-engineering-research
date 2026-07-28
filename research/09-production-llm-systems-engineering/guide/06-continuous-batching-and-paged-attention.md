# 6. Continuous batching and paged attention

Continuous batching and paged KV memory solve related but different serving
problems.

- **Continuous batching** changes which live sequences share each decode
  iteration. Finished requests leave immediately and waiting requests can join
  without waiting for an entire static batch.
- **Paged attention** lets each sequence’s KV cache occupy non-contiguous
  fixed-size memory blocks, reducing reservation waste and fragmentation.

Together they raise concurrency and throughput, but they also introduce a
scheduler whose fairness, tail latency, and memory policy become product
behavior.

## ELI5: a lift that changes passengers at every floor

A static batch is a tour bus: it waits for a fixed group, then the whole group
finishes together. One slow passenger delays the bus’s reuse.

Continuous batching is an elevator. At every floor, finished passengers leave
and new passengers enter. Capacity is reused immediately.

Paged memory is the luggage system. Instead of reserving one enormous,
contiguous locker for each passenger’s unknown future bags, the system hands
out small lockers as bags arrive and keeps a map of which lockers belong to
whom.

Where the analogy breaks: passengers do not consume equal resources. Prompt
length, output growth, priority, and KV blocks determine each sequence's cost.

## The request lifecycle

A modern engine repeatedly performs roughly this loop:

```text
admit requests
  → choose prefill/decode work within token and memory budgets
  → allocate KV blocks
  → run model step
  → sample tokens
  → stream results
  → free finished/cancelled sequences
  → repeat
```

[vLLM, “Anatomy of vLLM”](https://vllm.ai/blog/2025-09-05-anatomy-of-vllm)
walks through this lifecycle, including request preprocessing, scheduling,
block allocation, execution, and output. It is the project’s own explanation
and should be checked against the version deployed. The
[vLLM GitHub repository](https://github.com/vllm-project/vllm) is the ultimate
implementation reference for flags and behavior; blog terminology can outlive
code.

## Why static batching wastes capacity

Suppose four sequences enter together and require 5, 12, 40, and 200 output
tokens. A static batch remains shaped by the longest sequence or requires
awkward regrouping. Completed positions no longer produce useful output.

Continuous batching removes a sequence when it reaches an end condition and
uses the free slot for queued work. Different engines call this iteration-level
or in-flight batching. The
[Hugging Face, “Continuous batching”](https://huggingface.co/blog/continuous_batching)
tutorial gives a first-principles model and implementation sketch. It is
educational code, not a production scheduler with all cancellation, fairness,
and memory corner cases.

## The token budget is more useful than “batch size”

Sequences have unequal lengths. A batch of 16 one-token decode steps is not
equivalent to a batch containing thousands of prefill tokens.

Schedulers commonly limit some combination of:

- active sequences;
- tokens processed in an iteration;
- batched prefill tokens or chunk size;
- KV blocks available;
- model/adapter compatibility;
- per-request priority and deadline.

Larger batches can improve hardware utilization but extend queue and step time.
A high-throughput offline configuration can violate interactive ITL.

## How paged KV allocation works

The engine divides available KV memory into physical blocks. Each request has a
logical sequence of token blocks and a mapping table to physical locations.
As tokens arrive, the allocator assigns more blocks. On completion, it returns
them to the free pool.

Benefits include:

- less up-front reservation for unknown output length;
- reduced external fragmentation;
- rapid reuse when requests finish;
- block-granular prefix sharing and copy-on-write opportunities;
- a natural unit for swapping or eviction.

Costs include:

- unused space in a sequence’s final partially filled block;
- block tables and lookup machinery;
- allocation and copy complexity;
- sensitivity to block size;
- more intricate failure and isolation paths.

“Paged attention” is therefore not simply “FlashAttention with pages.”
FlashAttention primarily reorganizes attention computation and memory traffic
within a kernel. Paged KV management virtualizes where retained keys and
values live across requests. A serving stack may use both.

## Scheduling policy leaks into UX

Consider three policies:

- **throughput-first:** admit as much work as fits;
- **latency-first:** protect small interactive requests and active streams;
- **fairness-first:** prevent a user or long request from monopolizing
  capacity.

No policy dominates. Shortest-job-first improves many users’ latency but can
starve long prompts. Strict FIFO feels fair by arrival but allows
head-of-line blocking. Priority queues can be gamed unless admission and
tenant quotas enforce them.

Use aging, per-tenant budgets, deadline propagation, maximum sequence lengths,
and a batch lane for work that cannot meet an interactive objective.

## Preemption is not free

Under KV pressure, an engine might:

1. pause and later resume a sequence with cache intact;
2. evict/offload its blocks and reload them;
3. discard its blocks and recompute the prefix;
4. reject or terminate the request.

Each option trades memory, bandwidth, compute, delay, and user impact.
Repeatedly preempting a large request can create a livelock in which it pays
overhead but never completes. Track preemptions and useful progress per
request, not only global throughput.

## Worked example: the misleading load test

A team runs 1,000 identical 128-token prompts with fixed 64-token outputs and
reports excellent tokens per second. Production traffic then performs poorly.

The benchmark omitted:

- variable arrival times;
- long-tail prompts and outputs;
- cancellations when browser clients leave;
- prefix-cache hits and misses;
- multiple tenants and priorities;
- schema-constrained decoding;
- tool pauses and multi-turn sessions.

Build a trace-replay test with the real joint distribution of input length,
output length, arrival, tenant, model, and cache state. Add synthetic tails and
bursts. Capacity planning must use goodput under p95/p99 targets, not the
throughput of a perfectly rectangular batch.

## Read comparative studies carefully

The preprint
[Saicharan Kolluru, “Comparative Analysis of Large Language Model Inference Serving Systems: A Performance Study of vLLM and HuggingFace TGI” (arXiv:2511.17593)](https://arxiv.org/html/2511.17593v1)
reports results for selected models, hardware, versions, and workload
parameters. It is evidence that implementation choices matter, not a timeless
league table. Engine releases, kernels, quantization backends, and defaults can
change the ranking.

## Operational checklist

Instrument:

- queue age and admitted tokens by class;
- active sequences and batch composition per step;
- KV blocks allocated, free, fragmented, evicted, and swapped;
- TTFT, ITL, end-to-end latency, and goodput percentiles;
- cancellations that reached the engine;
- preemptions and recomputation;
- fairness by tenant and request size;
- out-of-memory and admission-rejection reasons.

Run failure drills: cancel during prefill, kill a worker with active sequences,
exhaust KV blocks, submit a maximum-length prompt, and overload one tenant.

## Interview checkpoint

**Question:** “How does continuous batching improve LLM serving?”

A strong answer explains iteration-level admission and removal of sequences,
then connects it to sequential decode. It distinguishes scheduling from paged
KV allocation and acknowledges queueing, fairness, preemption, and tail-latency
trade-offs.

**Explain it back:** Why might increasing the maximum batched-token budget
improve throughput while worsening both TTFT and inter-token latency?

## Capstone increment

Extend Chapter 5's workload card with admission limits, scheduling class,
deadline/cancellation propagation, per-tenant fairness, preemption outcome, and
KV-block budget. Run three explicit drills: cancel during prefill, burst one
noisy tenant, and exhaust the configured block budget.

The input is a mixed interactive/batch arrival trace. The output is a timeline
of queue age, admitted tokens, active sequences, blocks, cancellation, and
accepted goodput. Preserve this scheduling artifact as a required input to
Chapter 21's end-to-end benchmark rather than replacing it with an aggregate
tokens-per-second number. **Definition of done:** cancellation reaches the
engine, cancelled work stops consuming capacity after a stated cleanup bound,
and the noisy tenant cannot violate numeric fairness and SLO thresholds chosen
before the run.

Next: [Speculative decoding, quantization, and distillation](07-speculative-decoding-quantization-distillation.md)
separates three frequently conflated ways to make inference cheaper or faster.
