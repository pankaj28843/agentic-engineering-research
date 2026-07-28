# 7. Speculative decoding, quantization, and distillation

These techniques attack different costs:

- **Speculative decoding** changes the generation algorithm so a target model
  can verify several proposed tokens in parallel.
- **Quantization** represents weights, activations, or KV state at lower
  precision.
- **Distillation** trains a smaller or specialized student to imitate useful
  behavior from a teacher or teacher-generated data.

They can be combined. They are not interchangeable checkboxes.

## ELI5: editor, smaller print, apprentice

Imagine an expensive editor writing a report.

- With **speculation**, a fast junior proposes the next paragraph and the
  editor checks several words at once. Rejected words are replaced.
- With **quantization**, the same editor’s reference books use a more compact
  number notation. They occupy less shelf space, but rounding can lose detail.
- With **distillation**, an apprentice studies many examples from the editor
  and later writes independently. The apprentice may be cheaper and faster,
  but does not automatically preserve every capability.

The mechanisms, setup cost, and quality risks differ.

Where the analogy breaks: target verification is a numerical token-scoring
algorithm, not human editorial review; distillation is statistical training,
not transfer of a teacher's intent.

## Speculative decoding step by step

In a common draft-and-verify scheme:

1. a cheap draft model proposes several future tokens;
2. the target model scores those positions in a parallel verification pass;
3. a prefix of acceptable draft tokens is emitted;
4. at the first rejection, a corrected token is sampled;
5. the process repeats from the accepted prefix.

The acceptance rule is designed so the final samples follow the target
model’s distribution in the exact form of the algorithm. “The draft model
writes the answer” is therefore misleading: the target remains the authority.
Some approximate variants trade that guarantee for additional speed.

[NVIDIA, “An Introduction to Speculative Decoding for Reducing Latency in AI Inference”](https://developer.nvidia.com/blog/an-introduction-to-speculative-decoding-for-reducing-latency-in-ai-inference/)
provides an accessible implementation-oriented explanation. It is vendor
guidance, so measured gains must be tied to the named hardware and stack.

## The acceptance-rate economics

Speculation helps when:

```text
time to draft + time to verify + coordination overhead
  < time for target-only steps displaced
```

A weak draft is cheap but often rejected. A strong draft is accepted more but
may cost nearly as much as the target. Long speculative blocks expose more
parallelism and risk more wasted proposals after an early rejection.

Acceptance varies with domain, temperature, language, prompt, sampling rules,
and how closely the models align. Report accepted tokens per target pass,
draft cost, verification cost, end-to-end ITL, and tail latency—not just a
headline speedup.

The survey
[Yunhai Hu et al., “Speculative Decoding and Beyond: An In-Depth Review of Techniques” (arXiv:2502.19732)](https://arxiv.org/html/2502.19732v1)
organizes draft-model, self-speculative, retrieval-assisted, and other
families. It is useful for the design space, while its cited results span
non-equivalent models and systems.

## Where distillation enters

A draft model benefits from predicting what the target would predict, not
merely being a generally capable small model. Distillation can train the draft
on the target’s distributions or outputs to raise acceptance.

[Google Research, “DistillSpec: Improving Speculative Decoding via Knowledge Distillation”](https://research.google/pubs/distillspec-improving-speculative-decoding-via-knowledge-distillation/)
connects these mechanisms directly. The retained Google page is a short
publication landing record; use the named paper for method details rather than
inferring broad production claims from the abstract.

Distillation can also produce a standalone task model. That changes behavior:
the student answers without target verification, so its quality and safety
must be evaluated independently. Training data provenance, teacher bias,
coverage, and refresh become lifecycle obligations.

## Quantization changes a different axis

Quantization reduces memory footprint and bandwidth, and sometimes uses faster
low-precision compute. It can be applied to the target, draft, student, or KV
cache.

Unlike exact speculative decoding, quantization normally changes numerical
execution and may change outputs. It may also fail to accelerate if the
hardware lacks suitable kernels or if dequantization overhead dominates.

Do not say “we use AWQ, therefore we no longer need speculation.” One can make
each model step cheaper; the other can reduce how many sequential target steps
are required.

## A comparison by engineering surface

| Dimension | Speculative decoding | Quantization | Distillation |
| --- | --- | --- | --- |
| Main intervention | Serving algorithm | Numeric representation/kernels | Training/data pipeline |
| New artifact | Draft or proposal mechanism | Quantized weights/config | Student weights |
| Quality guarantee | Exact variants preserve target distribution | Must be measured | Must be measured |
| Main dependency | Target verification parallelism and acceptance | Hardware/kernel support | Representative teacher data |
| Refresh trigger | Target/draft or workload changes | Model/kernel/hardware changes | Task/data/teacher drift |
| Typical failure | Rejection overhead erases gain | Tail capability degrades | Student misses rare behavior |

## Agentic quality is a hard tail

A compressed model can look healthy on **perplexity**—a generic measure of how
surprised it is by held-out next tokens—or common QA and fail at
long-horizon tool use, instruction following, or recovery. The ICML 2025 paper
[Peijie Dong et al., “Can Compressed LLMs Truly Act? An Empirical Evaluation of Agentic Capabilities in LLM Compression”](https://icml.cc/virtual/2025/poster/43871)
tests this concern. Its specific conclusions are bounded by the evaluated
models, compression methods, and agent tasks, but it supports a crucial rule:
evaluate the behaviors your product delegates, not only generic language
quality.

For an agent, include:

- correct tool selection and arguments;
- adherence to permission and stop rules;
- recovery after tool failure;
- consistency over long context;
- structured-output validity and semantic correctness;
- harmful action and data-leakage tests;
- accepted-task cost after retries.

## Worked decision: latency-sensitive coding assistant

The team self-hosts a target model whose decode latency feels slow.

1. **Establish the phase.** If TTFT is dominant, speculation may not address
   the problem; prefix reuse or prefill scheduling might.
2. **Test quantized target variants.** Verify kernel support and compare
   code-edit acceptance, tool behavior, and long-context tasks.
3. **Profile speculation.** Use production-shaped prompts and report
   acceptance by task class. Include draft memory and batching interference.
4. **Consider a distilled draft.** Only if acceptance, not target verification
   cost, is the limiting factor and training maintenance is justified.
5. **Compose cautiously.** A quantized draft plus quantized target may maximize
   speed while accumulating quality and kernel effects.
6. **Keep a fallback.** Route low-confidence or consequence-heavy tasks to the
   verified baseline.

Compare cost per accepted edit at p95 latency, not raw tokens per second.

## Common category errors

- “Speculation uses a smaller model, so output quality is that smaller
  model’s quality.” Not for an exact target-verification algorithm.
- “Four-bit means four times faster.” Storage reduction is not equivalent to
  end-to-end acceleration.
- “A distilled student is just a compressed copy.” It learns from a finite
  objective and data distribution.
- “Benchmark parity means agent parity.” Aggregate scores can hide rare,
  workflow-critical regressions.
- “These techniques reduce prompt tokens.” They do not fix bloated context
  assembly.

## Interview checkpoint

**Question:** “How would you choose between speculative decoding,
quantization, and distillation?”

A strong answer first identifies whether the constraint is sequential decode,
memory/bandwidth/compute, or model size/task specialization. It explains
mechanism, hardware and training dependencies, quality guarantees, workload
evals, and the fact that techniques can compose.

**Explain it back:** Why can a distilled draft improve speculative decoding
without making the distilled model the final authority?

## Capstone increment

Write an optimization hypothesis table for the assistant. Each row names the
measured bottleneck, candidate intervention, new artifact, expected metric
movement, quality/safety tail at risk, rollback, and why the other two
interventions do not address this cause.

Do not implement yet. **Definition of done:** one experiment is selected by
Chapter 5–6 evidence, with a falsifiable success threshold and an unchanged
baseline ready for rollback.

Next: [INT8, INT4, FP8, AWQ, and GPTQ](08-quantization-formats-and-methods.md)
builds the vocabulary needed to evaluate a quantized artifact rather than
trusting its filename.
