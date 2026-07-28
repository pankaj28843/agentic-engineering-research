# Interlude: minimum model vocabulary for systems engineers

You do not need to derive transformer math to design a production LLM system.
You do need a small shared vocabulary so that memory, latency, caching, and
compatibility claims have concrete causes.

## ELI5: a peculiar text machine

Imagine a machine that first breaks text into reusable pieces, turns each piece
into numbers, repeatedly lets the pieces look at earlier pieces, and then
chooses one new piece. It appends that piece and repeats.

That story is deliberately incomplete. The machine is not looking up readable
notes or proving a sentence true. It is performing learned numerical
operations that produce a distribution over possible next tokens.

## Nine terms that unlock the serving chapters

1. **Token:** a model text unit, often smaller than a word. Token count, not
   character count, drives context capacity and much inference work.
2. **Transformer:** repeated layers that update numeric token
   representations. Model details vary, but the serving chapters focus on
   causal decoder-style generation.
3. **Attention:** each position produces a **query** that is matched against
   the **keys** at positions it is permitted to attend to—normally earlier and
   current positions in the causal decoder models in scope. Those scores
   determine how the corresponding **value** vectors are combined. Keys and
   values are numeric vectors, not human-readable facts.
4. **Weight:** learned model state that is mostly static while requests run.
   Loading or quantizing weights is different from retaining request state.
5. **Activation and KV state:** dynamic numeric state created while processing
   a request. Most intermediate activations are transient; the KV cache is the
   retained subset used across next-token steps. Retaining keys and values
   avoids recomputing all prior token state at every step.
6. **Prefill:** process the supplied input tokens and build their initial KV
   state. Many token positions can be processed together.
7. **Decode:** in an ordinary non-speculative step, choose one next token per
   active sequence, append each sequence's KV state, and repeat. Different live
   requests therefore grow and finish at different times.
8. **Next-token scores and decoding policy:** the model produces a score for
   each eligible next token; application/provider decoding rules turn those
   scores into a choice. Greedy decoding selects the highest-ranked token.
   Sampling can reshape choices with temperature, limit candidates with
   top-*k*, or retain a probability-mass prefix with top-*p*. Structured
   decoding masks choices that would make the target grammar impossible.
   These rules change variability; they do not add truth or authorization.
9. **Embedding:** a numeric representation used for similarity. Nearness can
   help retrieve candidates; it does not prove equal meaning, truth,
   authorization, or tenant compatibility.

Three foundational sources pin down the vocabulary without pretending that an
older paper describes every modern serving stack:

- Ashish Vaswani and colleagues, [“Attention Is All You
  Need”](https://arxiv.org/html/1706.03762v7), describe the original
  encoder-decoder Transformer, define attention as mapping a query and
  key-value pairs to an output, and explain why decoder masking prevents a
  position from seeing later output positions. The production models in this
  guide are usually causal decoder-style descendants, not copies of that
  original translation architecture.
- Alec Radford and colleagues, [“Language Models are Unsupervised Multitask
  Learners”](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf),
  describe GPT-2's byte-level BPE as a middle ground between character- and
  word-level modeling. This grounds the “text is not tokens” distinction; it
  is not evidence about the tokenizer or performance of a current model.
- Nils Reimers and Iryna Gurevych, [“Sentence-BERT: Sentence Embeddings using
  Siamese BERT-Networks”](https://aclanthology.org/D19-1410/), show one
  concrete use of embeddings and cosine similarity for candidate search. The
  warning that similarity is not truth or authorization is a systems-security
  boundary, not a claim that their paper evaluated.

For the serving implications, [NVIDIA Dynamo documentation, “Agentic
Inference”](https://docs.nvidia.com/dynamo/dev/digest/agentic-inference)
connects KV state to long, branching agent workloads, while the
[vLLM team, “Anatomy of vLLM”](https://vllm.ai/blog/2025-09-05-anatomy-of-vllm)
connects request processing, scheduling, KV blocks, execution, and sampling.
Use these as mechanism guides, not as proof that a model understands or that
one engine fits every workload.

## One request, end to end

```text
text → tokenizer → input tokens → prefill → KV state
                                   ↓
               next-token scores → decoding policy → chosen token
                                   ↓
                            append KV → repeat
```

Suppose the input becomes 1,000 tokens and the response becomes 100 tokens.
Prefill processes the initial 1,000-token prompt. Decode then performs roughly
100 sequential next-token steps, while retaining state for an ever-growing
sequence. That is why prompt length, output length, concurrency, and cache
reuse affect different user-visible clocks.

## Compatibility is a system boundary

Text that looks identical is not sufficient for inference-state reuse. A
tokenizer decides the token IDs; model weights and architecture decide the
numeric state; adapters and serving configuration can change compatibility.
A reusable prefix or KV entry therefore needs an explicit compatibility key,
not a string-equality assumption.

Carry five distinctions forward:

- text is not tokens;
- an embedding is not evidence;
- static weights are not per-request KV state;
- faster prefill is not automatically faster decode;
- model scores are not the same thing as the policy that selects a token.

A nominally greedy or temperature-zero hosted request still needs
reproducibility checks: provider implementations, model snapshots, kernels,
batching, and undocumented tie-breaking can change. Chapter 7 uses the policy
when explaining speculative acceptance, Chapter 9 adds grammar masks, and
Chapter 15 turns output variability into repeated evaluation.

## Check yourself

Answer without looking back:

1. Why can the same visible text produce a different token sequence?
2. Which state is mostly shared across requests—weights or KV state—and which
   grows with a request?
3. For a 1,000-token input and 100-token output, which phase processes the
   supplied tokens, which phase advances sequentially, and which user-visible
   clocks can each affect?
4. Why may a nearby embedding be useful for candidate discovery but
   insufficient as evidence or authorization?
5. What must an inference-state compatibility key identify before prefix or KV
   reuse is even eligible?
6. How do greedy choice, temperature, top-*k*, top-*p*, and a grammar mask
   change the set or probability of next-token choices?

A defensible answer includes:

- text is tokenized by a specific tokenizer, so normalization, vocabulary, or
  tokenizer version can change token IDs;
- weights are learned model state shared by compatible requests, while KV state
  is request-created state that grows as tokens are processed;
- prefill handles the initial 1,000 tokens and strongly affects time to first
  token; roughly 100 ordinary decode steps generate the response and strongly
  affect inter-token delay and total generation time;
- embedding distance proposes similar candidates but does not establish source
  truth, current ACLs, or tenant scope;
- at minimum, identify model/weight artifact, tokenizer, adapter, serving or
  attention configuration, prefix token IDs, and the approved
  request/tenant/trust sharing scope;
- greedy selection takes the highest score; temperature reshapes the score
  distribution; top-*k* keeps a fixed number of candidates; top-*p* keeps the
  smallest ranked prefix reaching a probability threshold; and a grammar mask
  removes structurally impossible choices. None proves semantic correctness.

**Small trace exercise:** draw two requests with the same 1,000-token prefix.
Request A generates 100 tokens; request B is cancelled after 20. Mark what
could be reused before admission, where each request needs separate KV
ownership, when TTFT ends, and why B's remaining 80-token output budget is not
allocated work that actually occurred. Then change B's adapter or tenant and
cross out any reuse that your compatibility policy no longer permits.

Next: [KV cache](04-kv-cache.md) makes the dynamic-state memory concrete, then
[prefill versus decode](05-prefill-vs-decode.md) turns the two phases into
separate latency budgets.
