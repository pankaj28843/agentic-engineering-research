# 8. INT8, INT4, FP8, AWQ, and GPTQ

INT8, INT4, and FP8 describe numeric representations or precision families.
AWQ and GPTQ describe post-training methods commonly used to create
low-bit, weight-only models. These are different axes.

“The model is 4-bit” is therefore incomplete. Ask what is quantized, by which
method and granularity, using which calibration data, stored in which format,
executed by which kernel, on which hardware, and evaluated on which tasks.

## ELI5: box size versus packing method

Suppose you must pack a detailed sculpture for shipping.

- INT4, INT8, and FP8 are like the sizes and shapes of the storage slots.
- GPTQ and AWQ are packing strategies for deciding how to fit important
  details into those slots.
- The runtime kernel is the truck and unloading equipment.

A brilliant packing method is useless if the destination cannot unload its
format. A small box is not a success if the sculpture’s fingers break.

Where the analogy breaks: quantization changes numeric representation and
sometimes the executed math; it is not lossless compression.

## Precision vocabulary

### INT8

Signed INT8 has 256 integer codes. Quantization maps a range of real values to
those codes using a scale and, for asymmetric schemes, a zero point.

```text
quantize:   q = round(x / scale) + zero_point
dequantize: x̂ = scale × (q - zero_point)
```

Clipping and rounding introduce error. Per-channel scales usually preserve
more local detail than one scale for a whole tensor but add metadata and
kernel requirements.

### INT4

Signed INT4 has only 16 codes. Two four-bit values are commonly packed into
one byte. Weight storage can be roughly half INT8 and one quarter FP16 before
scales and metadata, but native four-bit arithmetic is not guaranteed.
Runtimes may unpack or dequantize weights into a higher precision for
computation.

### FP8

FP8 retains floating-point structure: sign, exponent, and mantissa. Common
variants trade precision against dynamic range. It can represent both tiny and
large magnitudes more naturally than a single uniform INT8 range, while still
using one byte.

Efficient FP8 weight-and-activation execution depends on recent hardware and
supported kernels. On unsupported hardware, conversion overhead can erase the
benefit.

[Hugging Face Transformers, “Quantization concepts”](https://huggingface.co/docs/transformers/en/quantization/concept_guide)
provides clear definitions of affine mapping, symmetric/asymmetric schemes,
granularity, INT4 packing, FP8, post-training quantization, and
quantization-aware training. Check its backend-specific documentation for the
version you deploy.

## What the W, A, and KV notation means

Engine configurations often use shorthand:

- **W8A8:** weights and activations use eight-bit execution;
- **W4A16:** stored weights are four-bit, activations/computation are commonly
  higher precision;
- **KV8 or KV4:** attention key/value cache is quantized separately.

Exact implementation semantics vary. Accumulators may use higher precision,
some layers can remain unquantized, and fused kernels may have stricter shapes.
Read the artifact configuration and kernel path.

## GPTQ

GPTQ is a post-training, weight-only quantization family. It uses a calibration
set and second-order information to quantize weights while compensating for
introduced error across remaining weights. Practical implementations expose
choices such as bit width, group size, ordering, and activation handling.

The attraction is fitting large models into less memory without full
retraining. The liabilities are calibration sensitivity, conversion time,
format variants, and kernel compatibility.

## AWQ

Activation-Aware Weight Quantization identifies weight channels that matter
more based on activation behavior observed on calibration data, then uses
scaling to protect salient channels before low-bit quantization. Despite
“activation-aware” in the name, standard AWQ is normally **weight-only** at
inference; activation observations inform how weights are prepared.

This distinction is a common interview trap. AWQ is not synonymous with W8A8
activation quantization.

[General Compute, “Quantization for Inference: GPTQ, AWQ, SmoothQuant, and FP8”](https://www.generalcompute.com/blog/quantization-for-inference-gptq-awq-smoothquant-fp8)
offers a compact comparison. It contains vendor positioning and broad
recommendations, so verify every performance number and “best for” claim on
your engine and hardware.

## Calibration is a test-fixture design problem

Post-training quantization observes representative inputs to select scales or
measure sensitivity. A generic web corpus can miss your product’s outliers:
source code, tables, multilingual text, tool JSON, very long contexts, or
special tokens.

A calibration set should cover:

- actual input modalities and languages;
- short and long sequence distributions;
- common and rare task families;
- structured output and tool-use formats;
- safety and permission instructions;
- domain-specific numerical ranges.

Calibration examples are not the evaluation set. In this chapter, specify a
provisional regression slice using the fixed fixture cases, but label the
candidate **pending Chapter 15 release evaluation**. Chapter 15 turns that
slice into an independent, versioned, production-shaped golden set so the
method cannot optimize to the test.

## Quality does not fall smoothly

Lower precision introduces small numeric perturbations, but application
behavior is thresholded and autoregressive. A slightly different early token
can create a completely different tool call or long answer. Aggregate
perplexity can remain close while a narrow capability falls sharply.

The broad empirical study
[Eldar Kurtić et al., “Give Me BF16 or Give Me Death? Accuracy–Performance Trade-Offs in LLM Quantization” (arXiv:2411.02355)](https://arxiv.org/html/2411.02355v4)
compares quantization across models, precisions, and tasks and emphasizes that
outcomes depend on model size and evaluation dimension. It is an extensive
preprint, not a guarantee about a later model family or serving backend.

The current
[r/LocalLLaMA thread, “Has anyone tested the quantization quality (AWQ/GPTQ/FP8/NVFP4) for Qwen3.5?”](https://www.reddit.com/r/LocalLLaMA/comments/1s9iyrw/has_anyone_tested_the_quantization_quality/)
is useful as a demand signal and source of test ideas. The retained root post
contains a question rather than controlled results; do not promote community
impressions into comparative evidence.

## Benchmark the whole deployment

For every candidate artifact, pin:

- original model and revision;
- quantizer, version, bits, group size, and calibration set;
- serialized format and checksum;
- runtime, kernels, driver, and hardware;
- tensor/pipeline parallelism and batch configuration;
- prompt/output distributions and cache state.

Measure:

1. model load and resident memory;
2. TTFT, ITL, throughput, and goodput across concurrency;
3. energy or infrastructure cost where available;
4. task acceptance, tool correctness, schema validity, and safety;
5. tail regressions by language, length, and task class;
6. fallback and retry rate.

A weight-only artifact may reduce memory enough to fit one GPU instead of two,
which changes topology and cost more than a microbenchmark. Conversely, a
format with no optimized kernel may be smaller and slower.

## A deployment decision tree

1. **Need no compression?** Keep the higher-precision baseline and avoid an
   extra artifact lifecycle.
2. **Need broad compatibility and modest compression?** Test INT8 paths.
3. **Need the model to fit or maximize memory-bound decode capacity?** Test
   supported INT4 weight-only methods such as AWQ and GPTQ.
4. **Have native modern FP8 hardware and suitable kernels?** Test FP8
   weight-and-activation execution, especially for compute-heavy prefill.
5. **Quality fails?** Increase precision selectively, alter group/granularity,
   improve calibration, use quantization-aware training, choose another model,
   or route the affected tasks to a higher-precision lane.

The decision is empirical, reversible, and workload-specific.

## Worked example: tool-using 70B model

The BF16 model requires a costly multi-GPU deployment. A four-bit artifact fits
on one accelerator and doubles affordable replicas, but the initial benchmark
tests only short multiple-choice questions.

Before promotion, add long tool schemas, argument generation, multi-step
recovery, code editing, non-English requests, structured output, and
prompt-injection cases. Compare accepted workflow cost, not just GPU memory.
Canary the quantized lane, expose model/precision in traces, and route
consequence-heavy or low-confidence cases to the baseline.

If the single-GPU topology eliminates cross-GPU communication, record that as
a deployment benefit separate from arithmetic precision. It helps explain why
the measured gain may not transfer to another accelerator.

## Interview checkpoint

**Question:** “What is the difference between INT4, GPTQ, and AWQ?”

A strong answer says INT4 is a numeric precision/storage family, while GPTQ and
AWQ are post-training quantization approaches often used for four-bit
weight-only artifacts. It discusses scale/granularity, calibration, kernels,
hardware, what remains higher precision, and workload-specific quality.

**Explain it back:** Why can a four-bit model occupy more than exactly one
quarter of its FP16 memory and deliver less than a four-times speedup?

## Capstone increment

Create a **quantization decision/candidate card** and attach it to the selected
Chapter 7 hypothesis.

- If quantization was selected and a compatible artifact is available, record
  base model/revision, quantizer and format, precision/granularity, calibration
  data, checksum, runtime/kernel/hardware, Chapter 5–6 serving metrics,
  provisional tail slices, and fallback.
- If another optimization was selected, record `quantization_not_selected` and
  the bottleneck mismatch.
- For a hosted or stub model, record `provider_managed`, mark checksum,
  precision, calibration, and kernel fields `unknown` or
  `provider-controlled`, and state which performance claims therefore cannot
  be made.

**Definition of done:** the card makes a bounded deploy/defer/reject decision
without unsupported measurements and declares its later evaluation plan.
After Chapter 15, return to it and record the independent quality-gate result;
failure means rejection and rollback rather than a smaller-file victory.

## Part I checkpoint

- **Explain from memory:** context determines visible evidence; KV state grows
  with live tokens; scheduler and numeric format move different bottlenecks.
- **Update the capstone:** draw context/cache boundaries on the workload and
  serving diagram, including tenant-compatible reuse.
- **Keep unresolved:** how does an uncertain token stream become a bounded,
  authorized workflow? Part II supplies those contracts.

Next: [Structured outputs and recovery](09-structured-outputs-and-recovery.md)
moves from inference efficiency to the contract boundary between probabilistic
generation and deterministic application code.
