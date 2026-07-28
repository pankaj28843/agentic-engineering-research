# 5. Prefill versus decode: two workloads inside one request

An LLM request has two materially different inference phases.

- **Prefill** processes the input tokens, computes their representations, and
  builds the initial KV cache.
- **Decode** produces output tokens one at a time while repeatedly reading and
  extending that cache.

They use the same model but stress hardware differently. Treating “inference
latency” as one number hides the queueing and resource conflict users
experience.

## ELI5: study the case, then dictate the answer

A lawyer first reads a case file. Many pages can be reviewed and annotated in
parallel. That is prefill.

The lawyer then dictates an answer word by word. More precisely, each next
**token** depends on the tokens already present. That is decode.

A huge case file delays the first spoken word. A slow dictation pace makes the
answer feel sluggish after it starts. Optimizing one does not automatically
optimize the other.

Where the analogy breaks: prefill is parallel tensor computation and decode is
a sequential numerical next-token loop, not a model of human reading or legal
reasoning.

## The two user-facing clocks

Two primary measurements map to the phases:

```text
time to first token (TTFT)
  = admission/queue + prefill + first decode step + transport

inter-token latency (ITL), or time per output token (TPOT)
  ≈ repeated decode-step and streaming delay
```

End-to-end latency adds all output tokens and application work. Use percentile
distributions and segment by prompt length, output length, concurrency,
cache-hit state, model, and route. An average TTFT can conceal catastrophic
tail delay for long prompts.

## Why the hardware profile differs

Prefill processes a matrix of many input tokens. It often exposes substantial
parallel compute and benefits from efficient large matrix operations. Decode
usually advances each sequence by one token per iteration. It repeatedly reads
model weights and an expanding KV cache, making memory bandwidth and batching
especially important.

This is a mental model, not a universal label. Small prompts, giant batches,
mixture-of-experts models (which activate selected parameter groups),
quantization kernels (hardware routines for lower-precision math), and
particular hardware can move the bottleneck. Profile the actual
model-engine-hardware combination.

## Interference in a shared engine

Continuous serving mixes new prefills with active decodes. A long prefill can
occupy resources long enough to delay tokens for users already watching a
stream. If the scheduler always protects decode, new requests may wait too
long for their first token.

The preprint
[Yukang Chen et al., “Towards High-Goodput LLM Serving with Prefill-decode Multiplexing” (MuxWise, arXiv:2504.14489)](https://arxiv.org/html/2504.14489v3)
studies this conflict under separate TTFT and time-between-token objectives.
It compares disaggregation and chunked-prefill approaches and proposes
intra-GPU resource sharing. Its benchmark results apply to its models,
hardware, baselines, and service-level objective (SLO) assumptions; the
durable lesson is that throughput without latency compliance is not useful
capacity.

Use **goodput** for the rate of requests or tokens that satisfy the applicable
service objectives. A server can report impressive raw throughput while
making interactive requests unusable.

## Three scheduling architectures

### 1. Co-located phases

Prefill and decode run on the same worker pool. This is operationally simple
and lets both phases share local model weights and KV memory.

The scheduler can use **chunked prefill**: divide a long prompt into smaller
chunks and interleave them with decode iterations. Smaller chunks protect
streaming latency, while large chunks use compute efficiently. The correct
chunk size depends on prompt distribution, batch state, hardware, and SLO.

### 2. Disaggregated prefill and decode

Separate worker pools specialize by phase. Prefill workers build KV state,
which must reach decode workers. This can isolate latency objectives and size
each pool independently.

The price is transfer and coordination:

- both pools need compatible model state;
- KV tensors can be large;
- network bandwidth and topology become part of TTFT;
- capacity ratios can be wrong as traffic changes;
- prefix reuse and failure recovery cross pool boundaries.

[vLLM documentation, “Disaggregated Prefilling (experimental)”](https://docs.vllm.ai/en/latest/features/disagg_prefill/)
explicitly warns that the feature is intended to control phase interference
and placement rather than automatically improving throughput. This is an
important production habit: read the implementation’s non-goals before
copying an architecture diagram.

The
[Hao AI Lab, “DistServe Retro”](https://haoailab.com/blogs/distserve-retro/)
describes how the disaggregated design evolved and why per-phase objectives
matter. It is a project retrospective, while
[AWS, “Disaggregated prefill and decode for LLM inference on SageMaker HyperPod”](https://aws.amazon.com/blogs/machine-learning/disaggregated-prefill-and-decode-for-llm-inference-on-sagemaker-hyperpod/)
shows one vendor’s deployment path. Both are design evidence; neither proves
that an extra network hop is worthwhile for your traffic.

### 3. Spatial multiplexing

A system can partition compute resources within a GPU so prefill and decode
progress independently while sharing memory. MuxWise explores this direction.
It can avoid some cross-worker KV transfers, but memory-bandwidth contention,
kernel support, profiling, and scheduling complexity remain.

These are not maturity levels. Co-location can be the best production choice
at modest scale.

## Admission control before clever scheduling

No scheduler can honor impossible demand. Estimate work before admission using
input length, requested maximum output, model, priority, cache overlap, and
current KV capacity.

A production policy might:

1. reject or defer prompts beyond the supported class;
2. reserve capacity for active decodes;
3. put bulk jobs in a different queue;
4. cap output length and concurrent sequences;
5. degrade to a smaller model or asynchronous result;
6. expose honest retry timing rather than silently queueing forever.

The browser request timeout is not admission control. By the time a client
times out, the server may still be spending GPU work on an answer nobody can
receive. Propagate deadlines and cancellation through the queue and engine.

## Worked example: chat plus document analysis

One endpoint serves ordinary chat prompts of 1–4K tokens and occasional
200K-token document analyses. If all requests share a first-in-first-out
queue, one document prefill can inflate interactive TTFT and interrupt active
streams.

A staged fix is:

1. instrument phase-level queue, prefill, decode, and transfer time;
2. classify long-context work at admission;
3. apply chunked prefill and reserve decode capacity;
4. give document jobs a separate concurrency budget;
5. offer asynchronous completion when the interactive SLO cannot hold;
6. test disaggregation only if measured interference remains large enough to
   repay KV transfer and operating complexity.

This is a product decision as much as a kernel decision. A visible “we will
notify you” path may be more reliable than pretending every 200K-token job is
interactive.

## Benchmark design

Use a matrix, not one prompt:

- short, medium, and long input distributions;
- short and long outputs;
- cold and warm prefixes;
- steady and bursty arrivals;
- interactive and batch priorities;
- failure and cancellation during each phase.

Capture p50/p95/p99 TTFT, ITL/TPOT, end-to-end latency, goodput, queue age,
cache hit tokens, KV transfer bytes, rejected work, and GPU memory. Replay
production-shaped arrivals; a maximum-throughput offline benchmark omits the
very interference being designed.

## Interview checkpoint

**Question:** “Why might disaggregating prefill and decode help?”

A strong answer explains their compute/memory and latency differences, phase
interference, separate scaling, and goodput. It then names the costs: KV
transfer, duplicated weights, topology, pool imbalance, prefix locality,
failure recovery, and operational complexity. It proposes measurement before
adoption.

**Explain it back:** A change improves total tokens per second but worsens p99
TTFT and ITL. Under what product SLO could it still be a win?

## Capstone increment

Define two assistant workload classes: interactive question/review and
asynchronous document batch. Give each queue, prefill, first-token, inter-token,
tool, and completion budgets plus an honest degraded state.

- **Hosted track:** fill the card from end-to-end traces and provider usage
  metadata, marking the unseen phase boundaries.
- **Self-hosted track:** replay the workload matrix and measure the phase
  distributions directly.

**Definition of done:** a long batch document cannot silently consume the
interactive SLO; it is admitted to a compatible lane or visibly deferred.

Next: [Continuous batching and paged attention](06-continuous-batching-and-paged-attention.md)
shows how a serving engine keeps useful work flowing while sequences start,
grow, and finish at different times.
