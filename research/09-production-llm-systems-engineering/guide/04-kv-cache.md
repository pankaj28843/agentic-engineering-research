# 4. KV cache: the model’s per-token working memory

During autoregressive generation, a transformer repeatedly attends to earlier
tokens. Recomputing every earlier token at every step would waste enormous
work. The KV cache stores the attention **keys** and **values** already
computed for those tokens, once per layer, so the next token can reuse them.

It is not a cache of answers and not ordinary application memory. It is
model-specific tensor state, usually living in scarce accelerator memory,
whose size grows with active sequence length and concurrency.

## ELI5: keep the index cards

Imagine reading a mystery one word at a time. Before choosing the next word,
you write two index cards for every prior word:

- a **key** describing what kind of information that word can be matched
  against;
- a **value** containing the information to use when it matches.

Without a cache, you rewrite every old card before reading each new word. With
a KV cache, you keep the cards and create only the new pair. Generation gets
faster, but a long book read by many people fills the room with cards.

Where the analogy breaks: keys and values are learned numeric vectors per
layer, not notes containing human-readable facts.

## From attention to memory pressure

[The minimum model vocabulary interlude](03a-minimum-model-vocabulary.md)
defines token, attention, weights, KV state, prefill, and decode. With that
bridge in place, the capacity formula is straightforward.

For one decoder layer and one token, attention projects the token
representation into a query, key, and value. The query is needed for the
current attention operation. Earlier keys and values will be needed again, so
the engine retains them.

A useful sizing approximation is:

```text
KV bytes per request
  ≈ 2 × layers × tokens × KV_heads × head_dimension × bytes_per_element
```

The leading `2` is for keys and values. Architectures using grouped-query or
multi-query attention have fewer KV heads than query heads, which reduces the
cache. Implementations add block metadata, alignment, fragmentation, and
temporary buffers, so confirm the actual engine metric.

For a toy model with 32 layers, 8 KV heads, head dimension 128, and BF16
elements (a two-byte numeric format):

```text
per token = 2 × 32 × 8 × 128 × 2 bytes = 128 KiB
32K tokens ≈ 4 GiB for one request
```

This is an illustrative calculation, not a specification for a named model.
Multiply by concurrent live sequences and memory can be dominated by KV state
rather than weights.

## Why prefill and decode use the cache differently

During **prefill**, the engine processes the supplied prompt and creates KV
entries for all prompt tokens. This phase can exploit parallel matrix
operations and is often compute intensive.

During **decode**, the engine generates a token, appends its new KV state, and
reads the existing cache. Decode is sequential and often constrained by memory
bandwidth. Chapter 5 develops this distinction; for now, remember that a long
prompt creates a large cache before the first output token appears.

## Prefix reuse

If two requests begin with exactly the same tokens under compatible model
conditions, the engine may reuse KV blocks for their common prefix. Examples
include a shared system prompt, tool definitions, or repeated conversation
history.

The value depends on three things:

1. the prefix is actually identical after tokenization;
2. its blocks are still resident or cheaply recoverable;
3. the request reaches a worker that can find them.

Round-robin routing can destroy locality. Cache-aware routing weighs reusable
prefix overlap against queue and decode load. A perfect cache hit on an
overloaded worker may still be slower than recomputation elsewhere.

[NVIDIA Dynamo, “Agentic Inference”](https://docs.nvidia.com/dynamo/dev/digest/agentic-inference)
describes this problem for long-running tool-using agents and presents
NVIDIA’s router, distributed storage, priority, and lifecycle direction. Its
reported hit rates and latency gains are vendor measurements on particular
agent workloads. Treat them as design evidence and reproduce them before
capacity planning.

## Allocation: why paging matters

Requests do not arrive with equal lengths, and generated length is unknown.
Naively reserving one large contiguous region per request wastes space and
creates fragmentation.

Paged KV memory divides cache storage into fixed-size blocks and maps a
sequence’s logical blocks to available physical blocks, much like virtual
memory pages. The engine allocates as the sequence grows and can reclaim
blocks when it finishes. This enables higher useful occupancy and underpins
continuous batching, but it does not make memory free: block size, metadata,
copying, prefix sharing, and eviction remain trade-offs.

## Four pressure valves

### 1. Evict or retain selectively

Least-recently-used eviction is simple but does not understand value. A system
prompt reused on every agent turn may be more valuable than recent reasoning
tokens from a completed subagent. Workload-aware policies can consider
frequency, recomputation cost, session lifecycle, priority, and expected next
use.

The recent preprints
[Jiantong Jiang et al., “Towards Efficient Large Language Model Serving: A Survey on System-Aware KV Cache Optimization” (arXiv:2607.08057)](https://arxiv.org/html/2607.08057v1)
and
[Oteo Mamo et al., “Comparative Characterization of KV Cache Management Strategies for LLM Inference” (arXiv:2604.05012)](https://arxiv.org/html/2604.05012v1)
map eviction, sparsification, quantization, offload, and placement choices.
They are useful current syntheses, but the latter’s comparative results are
configuration-specific and both are recent preprints. No single policy wins
for every retention-sensitive, throughput-sensitive, and long-context load.

### 2. Offload through a memory hierarchy

Cold blocks can move from GPU HBM to host memory, local storage, or remote
storage. This preserves more state but adds transfer latency and operational
complexity. Prefetch can hide some latency when the system predicts reuse—for
example, while an agent waits for a tool—but a wrong prediction consumes
bandwidth and capacity.

### 3. Quantize the cache

Lower-precision keys and values reduce bytes and can raise batch capacity.
Accuracy loss is not uniform: outliers, model architecture, context length,
and task sensitivity matter. The
[r/LocalLLaMA discussion, “KV Cache is huge and bottlenecks LLM inference”](https://www.reddit.com/r/LocalLLaMA/comments/1ap3bkt/kv_cache_is_huge_and_bottlenecks_llm_inference_we/)
summarizes KIVI’s claimed memory, throughput, and quality results and contains
practitioner discussion. It is a useful lead, not a replacement for the paper,
engine compatibility check, and local workload evaluation.

### 4. Reduce or compress retained tokens

Some systems drop low-value tokens, use attention sinks, summarize history, or
change the model architecture. This can produce the largest memory savings and
the most semantic risk. A retention policy that works on ordinary chat may
erase the one early instruction needed by an agent.

## Cache lifecycle for an agent

An agent request pattern is unlike independent chat traffic:

```text
long prefill → short decode → tool wait → longer prefix → decode → repeat
```

During the tool wait, cache blocks may age out. When a subagent terminates,
its private blocks have little future value. When history is compacted, the
old prefix may never be referenced again.

Expose lifecycle hints carefully:

- session and parent identifiers;
- expected resume and deadline;
- priority;
- immutable shared-prefix ID;
- terminal event for reclaim;
- tenant and authorization partition.

Hints are optimization signals, not permission to merge state across trust
boundaries.

## Multi-tenant isolation

Prefix reuse creates a tempting optimization across users. It also creates
three attack surfaces:

1. **content leakage:** a bug returns or exposes another request’s state;
2. **timing leakage:** hit/miss latency reveals whether a victim used a
   prefix;
3. **lifecycle leakage:** stale blocks survive a tenant, model, or adapter
   transition.

At minimum, compatibility keys must include tenant/trust domain, model and
adapter identity, tokenizer, relevant configuration, and policy version.
Access checks must precede lookup. Debug and cache-observability endpoints
must not reveal raw prompts or cross-tenant block identifiers.

Chapter 19 examines evidence including the browser-acquired, text-layer
version of
[Guanlong Wu and colleagues, “I Know What You Asked: Prompt Leakage via
KV-Cache Sharing in Multi-Tenant LLM
Serving”](https://www.ndss-symposium.org/ndss-paper/i-know-what-you-asked-prompt-leakage-via-kv-cache-sharing-in-multi-tenant-llm-serving/).
For now, the safe default is no cross-tenant reuse unless a threat model and
measurement justify a narrower shared public prefix.

## What to measure

Do not tune from GPU utilization alone. Record:

- KV bytes used, reserved, fragmented, and evicted;
- active sequences and tokens by model/tenant class;
- prefix hit tokens, miss tokens, and recomputation time;
- time to first token and inter-token latency;
- queue delay and preemption;
- offload/prefetch bytes and stall time;
- request completion, quality, and out-of-memory failures.

Calculate value per retained byte. A 99% “hit rate” over tiny prefixes can be
less useful than preserving one expensive long prefix.

## Interview checkpoint

**Question:** “Why does increasing context length reduce serving capacity?”

A strong answer derives KV growth across layers, tokens, KV heads, head
dimension, precision, and concurrent sequences. It distinguishes static model
weights from dynamic per-request state, then discusses paging, prefix reuse,
eviction, offload, quantization, cache-aware routing, quality, and isolation.

**Explain it back:** Why is an application semantic cache unable to solve GPU
KV-cache pressure for a mostly unique workload?

## Field exercise

Use the published architecture of one deployable model to estimate KV bytes
per token.

- **Hosted track:** combine published architecture/configuration with usage
  metadata or a supplied toy trace. State which cache behavior is hidden by
  the provider.
- **Self-hosted track:** compare the estimate with an engine runtime metric,
  then run short/long prompts at increasing concurrency and plot TTFT, decode
  latency, eviction, and accepted throughput.

The disagreement between formula and observation—or the boundary the hosted
API conceals—is part of the result.

## Capstone increment

Produce a KV-capacity worksheet for the assistant's interactive and batch
workloads. Add the compatibility key and isolation assumptions for any prefix
reuse, including tenant/trust domain, model, adapter, tokenizer, and policy
version. Link the assumptions to Chapter 3's cache table.

**Definition of done:** the worksheet predicts a concurrency limit or clearly
marks the provider-owned unknown, and a cross-tenant prefix is ineligible by
construction.

Next: [Prefill versus decode](05-prefill-vs-decode.md) turns the two phases into
separate latency budgets and deployment choices.
